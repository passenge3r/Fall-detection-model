"""Standalone COCO-17 ST-GCN++ and CTR-GCN backbones.

The layer structure follows OpenMMLab MMAction2's ST-GCN++ configuration and
the official Uason-Chen/CTR-GCN implementation. Framework-specific registry,
configuration, and data code were removed so the benchmark runs on current
PyTorch without MMCV.
"""

from __future__ import annotations

import math

import numpy as np
import torch
from torch import nn


COCO_INWARD = [
    (15, 13), (13, 11), (16, 14), (14, 12), (11, 5), (12, 6),
    (9, 7), (7, 5), (10, 8), (8, 6), (5, 0), (6, 0),
    (1, 0), (3, 1), (2, 0), (4, 2),
]


def normalize_digraph(matrix: np.ndarray) -> np.ndarray:
    degree = np.sum(matrix, axis=0)
    inverse = np.zeros_like(degree)
    inverse[degree > 0] = degree[degree > 0] ** -1
    return matrix @ np.diag(inverse)


def edge_matrix(edges: list[tuple[int, int]], nodes: int = 17) -> np.ndarray:
    matrix = np.zeros((nodes, nodes), dtype=np.float32)
    for source, target in edges:
        matrix[target, source] = 1
    return matrix


def coco_adjacency() -> np.ndarray:
    identity = edge_matrix([(index, index) for index in range(17)])
    inward = normalize_digraph(edge_matrix(COCO_INWARD))
    outward = normalize_digraph(edge_matrix([(target, source) for source, target in COCO_INWARD]))
    return np.stack((identity, inward, outward)).astype(np.float32)


def conv_init(layer: nn.Conv2d) -> None:
    nn.init.kaiming_normal_(layer.weight, mode="fan_out")
    if layer.bias is not None:
        nn.init.constant_(layer.bias, 0)


def bn_init(layer: nn.modules.batchnorm._BatchNorm, scale: float = 1.0) -> None:
    nn.init.constant_(layer.weight, scale)
    nn.init.constant_(layer.bias, 0)


class TemporalConv(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 9,
                 stride: int = 1, dilation: int = 1) -> None:
        super().__init__()
        padding = (kernel_size + (kernel_size - 1) * (dilation - 1) - 1) // 2
        self.conv = nn.Conv2d(
            in_channels, out_channels, (kernel_size, 1),
            padding=(padding, 0), stride=(stride, 1), dilation=(dilation, 1)
        )
        self.bn = nn.BatchNorm2d(out_channels)
        conv_init(self.conv)
        bn_init(self.bn)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.bn(self.conv(x))


class MultiScaleTemporalConv(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, stride: int = 1,
                 kernel_size: int = 5, dilations: tuple[int, ...] = (1, 2),
                 residual: bool = False) -> None:
        super().__init__()
        branch_count = len(dilations) + 2
        if out_channels % branch_count:
            raise ValueError("out_channels must be divisible by temporal branch count")
        branch_channels = out_channels // branch_count
        self.branches = nn.ModuleList()
        for dilation in dilations:
            self.branches.append(nn.Sequential(
                nn.Conv2d(in_channels, branch_channels, 1),
                nn.BatchNorm2d(branch_channels),
                nn.ReLU(inplace=True),
                TemporalConv(branch_channels, branch_channels, kernel_size, stride, dilation),
            ))
        self.branches.append(nn.Sequential(
            nn.Conv2d(in_channels, branch_channels, 1),
            nn.BatchNorm2d(branch_channels),
            nn.ReLU(inplace=True),
            nn.MaxPool2d((3, 1), stride=(stride, 1), padding=(1, 0)),
            nn.BatchNorm2d(branch_channels),
        ))
        self.branches.append(nn.Sequential(
            nn.Conv2d(in_channels, branch_channels, 1, stride=(stride, 1)),
            nn.BatchNorm2d(branch_channels),
        ))
        if not residual:
            self.residual = lambda x: 0
        elif in_channels == out_channels and stride == 1:
            self.residual = lambda x: x
        else:
            self.residual = TemporalConv(in_channels, out_channels, 1, stride)
        self.apply(self._init_branch)

    @staticmethod
    def _init_branch(module: nn.Module) -> None:
        if isinstance(module, nn.Conv2d):
            conv_init(module)
        elif isinstance(module, nn.BatchNorm2d):
            bn_init(module)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.cat([branch(x) for branch in self.branches], dim=1) + self.residual(x)


class AdaptiveGraphConv(nn.Module):
    """ST-GCN++ graph unit: learnable initial topology and internal residual."""

    def __init__(self, in_channels: int, out_channels: int, adjacency: np.ndarray,
                 with_residual: bool = True) -> None:
        super().__init__()
        subsets = adjacency.shape[0]
        self.subsets = subsets
        self.A = nn.Parameter(torch.tensor(adjacency, dtype=torch.float32))
        self.conv = nn.Conv2d(in_channels, out_channels * subsets, 1)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        if not with_residual:
            self.residual = lambda x: 0
        elif in_channels == out_channels:
            self.residual = lambda x: x
        else:
            self.residual = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1), nn.BatchNorm2d(out_channels)
            )
        conv_init(self.conv)
        bn_init(self.bn)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        n, _, t, v = x.shape
        features = self.conv(x).view(n, self.subsets, -1, t, v)
        features = torch.einsum("nkctv,kvw->nctw", features, self.A).contiguous()
        return self.relu(self.bn(features) + self.residual(x))


class STGCNPPBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, adjacency: np.ndarray,
                 stride: int = 1, residual: bool = True) -> None:
        super().__init__()
        self.gcn = AdaptiveGraphConv(in_channels, out_channels, adjacency, with_residual=True)
        self.tcn = MultiScaleTemporalConv(out_channels, out_channels, stride=stride, residual=False)
        if not residual:
            self.residual = lambda x: 0
        elif in_channels == out_channels and stride == 1:
            self.residual = lambda x: x
        else:
            self.residual = TemporalConv(in_channels, out_channels, 1, stride)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.relu(self.tcn(self.gcn(x)) + self.residual(x))


class STGCNPP(nn.Module):
    def __init__(self, num_class: int = 2, in_channels: int = 3,
                 num_point: int = 17, num_person: int = 1,
                 base_channels: int = 64, dropout: float = 0.5) -> None:
        super().__init__()
        adjacency = coco_adjacency()
        self.num_person = num_person
        self.num_point = num_point
        self.data_bn = nn.BatchNorm1d(in_channels * num_point)
        channels = [base_channels] * 4 + [base_channels * 2] * 3 + [base_channels * 4] * 3
        strides = [1, 1, 1, 1, 2, 1, 1, 2, 1, 1]
        blocks = []
        current = in_channels
        for index, (output, stride) in enumerate(zip(channels, strides)):
            blocks.append(STGCNPPBlock(current, output, adjacency, stride, residual=index != 0))
            current = output
        self.blocks = nn.ModuleList(blocks)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(current, num_class)
        bn_init(self.data_bn)
        # The official 60-class initialization is too wide when num_class=2.
        nn.init.normal_(self.fc.weight, 0, 0.01)
        nn.init.constant_(self.fc.bias, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        n, c, t, v, m = x.shape
        x = x.permute(0, 4, 3, 1, 2).contiguous().view(n * m, v * c, t)
        x = self.data_bn(x)
        x = x.view(n, m, v, c, t).permute(0, 1, 3, 4, 2).reshape(n * m, c, t, v)
        for block in self.blocks:
            x = block(x)
        x = x.view(n, m, x.size(1), -1).mean(-1).mean(1)
        return self.fc(self.dropout(x))


class CTRGraphConv(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, rel_reduction: int = 8) -> None:
        super().__init__()
        rel_channels = 8 if in_channels in (3, 9) else max(8, in_channels // rel_reduction)
        self.conv1 = nn.Conv2d(in_channels, rel_channels, 1)
        self.conv2 = nn.Conv2d(in_channels, rel_channels, 1)
        self.conv3 = nn.Conv2d(in_channels, out_channels, 1)
        self.conv4 = nn.Conv2d(rel_channels, out_channels, 1)
        self.tanh = nn.Tanh()
        for module in self.modules():
            if isinstance(module, nn.Conv2d):
                conv_init(module)

    def forward(self, x: torch.Tensor, adjacency: torch.Tensor, alpha: torch.Tensor) -> torch.Tensor:
        x1 = self.conv1(x).mean(-2)
        x2 = self.conv2(x).mean(-2)
        x3 = self.conv3(x)
        relation = self.tanh(x1.unsqueeze(-1) - x2.unsqueeze(-2))
        relation = self.conv4(relation) * alpha + adjacency[None, None]
        return torch.einsum("ncuv,nctv->nctu", relation, x3)


class CTRUnitGCN(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, adjacency: np.ndarray) -> None:
        super().__init__()
        self.PA = nn.Parameter(torch.tensor(adjacency, dtype=torch.float32))
        self.alpha = nn.Parameter(torch.zeros(1))
        self.convs = nn.ModuleList(
            [CTRGraphConv(in_channels, out_channels) for _ in range(adjacency.shape[0])]
        )
        self.bn = nn.BatchNorm2d(out_channels)
        if in_channels == out_channels:
            self.down = lambda x: x
        else:
            self.down = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1), nn.BatchNorm2d(out_channels)
            )
        self.relu = nn.ReLU(inplace=True)
        bn_init(self.bn, 1e-6)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        output = sum(conv(x, self.PA[index], self.alpha) for index, conv in enumerate(self.convs))
        return self.relu(self.bn(output) + self.down(x))


class CTRBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, adjacency: np.ndarray,
                 stride: int = 1, residual: bool = True) -> None:
        super().__init__()
        self.gcn = CTRUnitGCN(in_channels, out_channels, adjacency)
        self.tcn = MultiScaleTemporalConv(out_channels, out_channels, stride=stride, residual=False)
        if not residual:
            self.residual = lambda x: 0
        elif in_channels == out_channels and stride == 1:
            self.residual = lambda x: x
        else:
            self.residual = TemporalConv(in_channels, out_channels, 1, stride)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.relu(self.tcn(self.gcn(x)) + self.residual(x))


class CTRGCN(nn.Module):
    def __init__(self, num_class: int = 2, in_channels: int = 3,
                 num_point: int = 17, num_person: int = 1,
                 base_channels: int = 64, dropout: float = 0.5) -> None:
        super().__init__()
        adjacency = coco_adjacency()
        self.data_bn = nn.BatchNorm1d(num_person * in_channels * num_point)
        channels = [base_channels] * 4 + [base_channels * 2] * 3 + [base_channels * 4] * 3
        strides = [1, 1, 1, 1, 2, 1, 1, 2, 1, 1]
        blocks = []
        current = in_channels
        for index, (output, stride) in enumerate(zip(channels, strides)):
            blocks.append(CTRBlock(current, output, adjacency, stride, residual=index != 0))
            current = output
        self.blocks = nn.ModuleList(blocks)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(current, num_class)
        bn_init(self.data_bn)
        nn.init.normal_(self.fc.weight, 0, 0.01)
        nn.init.constant_(self.fc.bias, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        n, c, t, v, m = x.shape
        x = x.permute(0, 4, 3, 1, 2).contiguous().view(n, m * v * c, t)
        x = self.data_bn(x)
        x = x.view(n, m, v, c, t).permute(0, 1, 3, 4, 2).reshape(n * m, c, t, v)
        for block in self.blocks:
            x = block(x)
        x = x.view(n, m, x.size(1), -1).mean(-1).mean(1)
        return self.fc(self.dropout(x))


def build_model(name: str, **kwargs: object) -> nn.Module:
    if name == "stgcnpp":
        return STGCNPP(**kwargs)
    if name == "ctrgcn":
        return CTRGCN(**kwargs)
    raise ValueError(f"Unknown model: {name}")
