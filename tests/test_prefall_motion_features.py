import numpy as np

from scripts.train_prefall_multihorizon_stgcnpp import build_motion_features


def test_static_pose_has_zero_motion() -> None:
    sample = np.zeros((3, 8, 17, 1), dtype=np.float32)
    sample[0] = 0.5; sample[1] = 0.25; sample[2] = 1.0
    output = build_motion_features(sample)
    assert output.shape == (9, 8, 17, 1)
    assert np.allclose(output[3:7], 0)
    assert np.allclose(output[8], 0)


def test_linear_vertical_motion_has_velocity_but_no_acceleration() -> None:
    sample = np.zeros((3, 8, 17, 1), dtype=np.float32)
    sample[2] = 1.0
    for frame in range(8):
        sample[1, frame, :, 0] = frame * 0.1
    output = build_motion_features(sample)
    assert np.allclose(output[4, 1:, :, 0], 0.1, atol=1e-6)
    assert np.allclose(output[6, 2:, :, 0], 0, atol=1e-6)
    assert np.allclose(output[8, 1:, :, 0], 0.1, atol=1e-6)


def test_missing_joint_suppresses_derivatives() -> None:
    sample = np.zeros((3, 4, 17, 1), dtype=np.float32)
    sample[2] = 1.0; sample[0, 1:, :, 0] = 1.0
    sample[2, 1, 3, 0] = 0.0
    output = build_motion_features(sample)
    assert output[3, 1, 3, 0] == 0
    assert output[3, 2, 3, 0] == 0


def test_causal_smoothing_reduces_jitter_velocity() -> None:
    sample = np.zeros((3, 12, 17, 1), dtype=np.float32); sample[2] = 1.0
    sample[0, :, :, 0] = np.asarray([0, 1] * 6, dtype=np.float32)[:, None]
    raw = build_motion_features(sample, smooth=False)
    smooth = build_motion_features(sample, smooth=True)
    assert np.std(smooth[3, 2:, :, 0]) < np.std(raw[3, 2:, :, 0])
