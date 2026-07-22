from __future__ import annotations

import numpy as np


COCO17_INWARD = [
    (15, 13), (13, 11), (16, 14), (14, 12), (11, 12),
    (5, 11), (6, 12), (5, 6), (5, 7), (6, 8), (7, 9),
    (8, 10), (1, 2), (0, 1), (0, 2), (1, 3), (2, 4),
    (3, 5), (4, 6),
]


def edge_to_matrix(edges: list[tuple[int, int]], joints: int = 17) -> np.ndarray:
    matrix = np.zeros((joints, joints), dtype=np.float32)
    for source, target in edges:
        matrix[target, source] = 1.0
    return matrix


def normalize_digraph(matrix: np.ndarray) -> np.ndarray:
    degree = matrix.sum(axis=0)
    inverse = np.zeros_like(degree)
    inverse[degree > 0] = 1.0 / degree[degree > 0]
    return matrix @ np.diag(inverse)


def coco17_spatial_adjacency() -> np.ndarray:
    self_links = [(joint, joint) for joint in range(17)]
    outward = [(target, source) for source, target in COCO17_INWARD]
    return np.stack(
        [
            edge_to_matrix(self_links),
            normalize_digraph(edge_to_matrix(COCO17_INWARD)),
            normalize_digraph(edge_to_matrix(outward)),
        ]
    ).astype(np.float32)
