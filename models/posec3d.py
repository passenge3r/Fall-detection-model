from __future__ import annotations

import torch
from torch import nn


class Residual3DBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int,
                 stride: tuple[int, int, int] = (1, 1, 1)) -> None:
        super().__init__()
        self.conv1 = nn.Conv3d(
            in_channels, out_channels, 3, stride=stride, padding=1, bias=False
        )
        self.bn1 = nn.BatchNorm3d(out_channels)
        self.conv2 = nn.Conv3d(out_channels, out_channels, 3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm3d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.projection = (
            nn.Identity()
            if in_channels == out_channels and stride == (1, 1, 1)
            else nn.Sequential(
                nn.Conv3d(in_channels, out_channels, 1, stride=stride, bias=False),
                nn.BatchNorm3d(out_channels),
            )
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = self.projection(x)
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        return self.relu(x + residual)


class PoseC3D(nn.Module):
    """PoseC3D-style classifier using joint heatmap volumes and a 3D CNN.

    The fixed heatmap projection lets the model consume the same normalized
    COCO-17 skeleton tensors as the graph baselines while retaining PoseC3D's
    defining heatmap-volume representation.
    """

    def __init__(self, num_class: int = 2, base_channels: int = 64,
                 dropout: float = 0.5, heatmap_size: int = 32,
                 heatmap_extent: float = 4.0, sigma: float = 1.25,
                 **_: object) -> None:
        super().__init__()
        stem_channels = max(16, base_channels // 2)
        self.heatmap_size = heatmap_size
        self.heatmap_extent = heatmap_extent
        self.sigma = sigma
        grid = torch.arange(heatmap_size, dtype=torch.float32)
        self.register_buffer("grid_x", grid.view(1, 1, 1, 1, heatmap_size), persistent=False)
        self.register_buffer("grid_y", grid.view(1, 1, 1, heatmap_size, 1), persistent=False)
        self.stem = nn.Sequential(
            nn.Conv3d(17, stem_channels, (3, 5, 5), stride=(1, 2, 2),
                      padding=(1, 2, 2), bias=False),
            nn.BatchNorm3d(stem_channels),
            nn.ReLU(inplace=True),
        )
        self.backbone = nn.Sequential(
            Residual3DBlock(stem_channels, stem_channels),
            Residual3DBlock(stem_channels, stem_channels * 2, (2, 2, 2)),
            Residual3DBlock(stem_channels * 2, stem_channels * 4, (2, 2, 2)),
            Residual3DBlock(stem_channels * 4, stem_channels * 8, (2, 2, 2)),
        )
        self.pool = nn.AdaptiveAvgPool3d(1)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(stem_channels * 8, num_class)

    def skeleton_to_heatmaps(self, x: torch.Tensor) -> torch.Tensor:
        # x: [N, C=3, T, V=17, M=1] -> [N, V, T, H, W]
        xy = x[:, :2, :, :, 0].clamp(-self.heatmap_extent, self.heatmap_extent)
        confidence = x[:, 2, :, :, 0].clamp(0, 1)
        scale = (self.heatmap_size - 1) / (2 * self.heatmap_extent)
        px = ((xy[:, 0] + self.heatmap_extent) * scale).permute(0, 2, 1)
        py = ((xy[:, 1] + self.heatmap_extent) * scale).permute(0, 2, 1)
        weight = confidence.permute(0, 2, 1)
        px = px[..., None, None]
        py = py[..., None, None]
        distance = (self.grid_x - px).square() + (self.grid_y - py).square()
        heatmaps = torch.exp(-distance / (2 * self.sigma * self.sigma))
        return heatmaps * weight[..., None, None]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.skeleton_to_heatmaps(x)
        x = self.stem(x)
        x = self.backbone(x)
        x = self.pool(x).flatten(1)
        return self.fc(self.dropout(x))
