from __future__ import annotations

import math

import torch
import torch.nn as nn

from .graph import coco17_spatial_adjacency


def conv_init(module: nn.Conv2d) -> None:
    nn.init.kaiming_normal_(module.weight, mode="fan_out")
    if module.bias is not None:
        nn.init.constant_(module.bias, 0)


def bn_init(module: nn.modules.batchnorm._BatchNorm, scale: float = 1.0) -> None:
    nn.init.constant_(module.weight, scale)
    nn.init.constant_(module.bias, 0)


class TemporalConv(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 9,
                 stride: int = 1, dilation: int = 1, norm: bool = True) -> None:
        super().__init__()
        padding = (kernel_size + (kernel_size - 1) * (dilation - 1) - 1) // 2
        self.conv = nn.Conv2d(
            in_channels, out_channels, (kernel_size, 1),
            stride=(stride, 1), padding=(padding, 0), dilation=(dilation, 1)
        )
        self.bn = nn.BatchNorm2d(out_channels) if norm else nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.bn(self.conv(x))


class MultiScaleTemporalConv(nn.Module):
    """Multi-branch temporal module used by ST-GCN++ and CTR-GCN."""

    def __init__(self, in_channels: int, out_channels: int, stride: int = 1,
                 kernel_size: int = 3, dilations: tuple[int, ...] = (1, 2, 3, 4),
                 dropout: float = 0.0, transform: bool = False) -> None:
        super().__init__()
        branches = len(dilations) + 2
        mid = out_channels // branches
        remainder = out_channels - mid * (branches - 1)
        modules: list[nn.Module] = []
        for index, dilation in enumerate(dilations):
            branch_channels = remainder if index == 0 else mid
            modules.append(
                nn.Sequential(
                    nn.Conv2d(in_channels, branch_channels, 1),
                    nn.BatchNorm2d(branch_channels),
                    nn.ReLU(inplace=True),
                    TemporalConv(branch_channels, branch_channels, kernel_size, stride, dilation),
                )
            )
        modules.append(
            nn.Sequential(
                nn.Conv2d(in_channels, mid, 1), nn.BatchNorm2d(mid), nn.ReLU(inplace=True),
                nn.MaxPool2d((3, 1), stride=(stride, 1), padding=(1, 0)),
                nn.BatchNorm2d(mid),
            )
        )
        modules.append(
            nn.Sequential(
                nn.Conv2d(in_channels, mid, 1, stride=(stride, 1)), nn.BatchNorm2d(mid)
            )
        )
        self.branches = nn.ModuleList(modules)
        self.transform = (
            nn.Sequential(nn.BatchNorm2d(out_channels), nn.ReLU(inplace=True), nn.Conv2d(out_channels, out_channels, 1))
            if transform else nn.Identity()
        )
        self.out_bn = nn.BatchNorm2d(out_channels) if transform else nn.Identity()
        self.dropout = nn.Dropout(dropout, inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = torch.cat([branch(x) for branch in self.branches], dim=1)
        return self.dropout(self.out_bn(self.transform(x)))


class STUnitGCN(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, adjacency: torch.Tensor) -> None:
        super().__init__()
        self.subsets = adjacency.shape[0]
        self.A = nn.Parameter(adjacency.clone())
        self.conv = nn.Conv2d(in_channels, out_channels * self.subsets, 1)
        self.bn = nn.BatchNorm2d(out_channels)
        self.inner_residual = (
            nn.Identity() if in_channels == out_channels
            else nn.Sequential(nn.Conv2d(in_channels, out_channels, 1), nn.BatchNorm2d(out_channels))
        )
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = self.inner_residual(x)
        n, _, t, v = x.shape
        x = self.conv(x).view(n, self.subsets, -1, t, v)
        x = torch.einsum("nkctv,kvw->nctw", x, self.A).contiguous()
        return self.relu(self.bn(x) + residual)


class STGCNBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, adjacency: torch.Tensor,
                 stride: int = 1, residual: bool = True, dropout: float = 0.0) -> None:
        super().__init__()
        self.gcn = STUnitGCN(in_channels, out_channels, adjacency)
        self.tcn = MultiScaleTemporalConv(
            out_channels, out_channels, stride=stride, dropout=dropout, transform=True
        )
        if not residual:
            self.residual = None
        elif in_channels == out_channels and stride == 1:
            self.residual = nn.Identity()
        else:
            self.residual = TemporalConv(in_channels, out_channels, 1, stride)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = 0 if self.residual is None else self.residual(x)
        return self.relu(self.tcn(self.gcn(x)) + residual)


class STGCNPlusPlus(nn.Module):
    def __init__(self, classes: int = 2, in_channels: int = 3, base_channels: int = 64,
                 dropout: float = 0.25) -> None:
        super().__init__()
        adjacency = torch.tensor(coco17_spatial_adjacency())
        self.data_bn = nn.BatchNorm1d(in_channels * 17)
        channels = [base_channels] * 4 + [base_channels * 2] * 3 + [base_channels * 4] * 3
        strides = [1, 1, 1, 1, 2, 1, 1, 2, 1, 1]
        blocks = []
        current = in_channels
        for index, (output, stride) in enumerate(zip(channels, strides)):
            blocks.append(
                STGCNBlock(current, output, adjacency, stride, residual=index != 0, dropout=dropout)
            )
            current = output
        self.blocks = nn.ModuleList(blocks)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(current, classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        n, c, t, v, m = x.shape
        x = x.permute(0, 4, 3, 1, 2).contiguous().view(n * m, v * c, t)
        x = self.data_bn(x)
        x = x.view(n * m, v, c, t).permute(0, 2, 3, 1).contiguous()
        for block in self.blocks:
            x = block(x)
        x = x.view(n, m, x.shape[1], -1).mean(dim=(1, 3))
        return self.fc(self.dropout(x))


class CTRGraphConv(nn.Module):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        relation_channels = 8 if in_channels in (3, 9) else max(8, in_channels // 8)
        self.conv1 = nn.Conv2d(in_channels, relation_channels, 1)
        self.conv2 = nn.Conv2d(in_channels, relation_channels, 1)
        self.conv3 = nn.Conv2d(in_channels, out_channels, 1)
        self.conv4 = nn.Conv2d(relation_channels, out_channels, 1)
        self.tanh = nn.Tanh()

    def forward(self, x: torch.Tensor, adjacency: torch.Tensor, alpha: torch.Tensor) -> torch.Tensor:
        x1 = self.conv1(x).mean(-2)
        x2 = self.conv2(x).mean(-2)
        features = self.conv3(x)
        relation = self.tanh(x1.unsqueeze(-1) - x2.unsqueeze(-2))
        relation = self.conv4(relation) * alpha + adjacency[None, None]
        return torch.einsum("ncuv,nctv->nctu", relation, features)


class CTRUnitGCN(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, adjacency: torch.Tensor) -> None:
        super().__init__()
        self.convs = nn.ModuleList(
            [CTRGraphConv(in_channels, out_channels) for _ in range(adjacency.shape[0])]
        )
        self.A = nn.Parameter(adjacency.clone())
        self.alpha = nn.Parameter(torch.zeros(1))
        self.bn = nn.BatchNorm2d(out_channels)
        bn_init(self.bn, 1e-6)
        self.residual = (
            nn.Identity() if in_channels == out_channels
            else nn.Sequential(nn.Conv2d(in_channels, out_channels, 1), nn.BatchNorm2d(out_channels))
        )
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        output = sum(conv(x, self.A[index], self.alpha) for index, conv in enumerate(self.convs))
        return self.relu(self.bn(output) + self.residual(x))


class CTRGCNBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, adjacency: torch.Tensor,
                 stride: int = 1, residual: bool = True) -> None:
        super().__init__()
        self.gcn = CTRUnitGCN(in_channels, out_channels, adjacency)
        self.tcn = MultiScaleTemporalConv(
            out_channels, out_channels, stride=stride, kernel_size=5, dilations=(1, 2)
        )
        if not residual:
            self.residual = None
        elif in_channels == out_channels and stride == 1:
            self.residual = nn.Identity()
        else:
            self.residual = TemporalConv(in_channels, out_channels, 1, stride)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = 0 if self.residual is None else self.residual(x)
        return self.relu(self.tcn(self.gcn(x)) + residual)


class CTRGCN(nn.Module):
    def __init__(self, classes: int = 2, in_channels: int = 3, base_channels: int = 64,
                 dropout: float = 0.25) -> None:
        super().__init__()
        adjacency = torch.tensor(coco17_spatial_adjacency())
        self.data_bn = nn.BatchNorm1d(in_channels * 17)
        channels = [base_channels] * 4 + [base_channels * 2] * 3 + [base_channels * 4] * 3
        strides = [1, 1, 1, 1, 2, 1, 1, 2, 1, 1]
        blocks = []
        current = in_channels
        for index, (output, stride) in enumerate(zip(channels, strides)):
            blocks.append(CTRGCNBlock(current, output, adjacency, stride, residual=index != 0))
            current = output
        self.blocks = nn.ModuleList(blocks)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(current, classes)
        nn.init.normal_(self.fc.weight, 0, math.sqrt(2.0 / classes))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        n, c, t, v, m = x.shape
        x = x.permute(0, 4, 3, 1, 2).contiguous().view(n * m, v * c, t)
        x = self.data_bn(x)
        x = x.view(n * m, v, c, t).permute(0, 2, 3, 1).contiguous()
        for block in self.blocks:
            x = block(x)
        x = x.view(n, m, x.shape[1], -1).mean(dim=(1, 3))
        return self.fc(self.dropout(x))


def build_model(name: str, classes: int = 2, **kwargs: object) -> nn.Module:
    if name == "stgcnpp":
        return STGCNPlusPlus(classes=classes, **kwargs)
    if name == "ctrgcn":
        return CTRGCN(classes=classes, **kwargs)
    raise ValueError(f"Unknown model: {name}")
