from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

import cv2
import numpy as np
from fastapi.testclient import TestClient

from app.ezviz import EzvizClient, EzvizError
from app.stream_service import probe_video_source, validate_source
from app.prefall import risk_level
from app.webapp import app


class EzvizClientTests(unittest.TestCase):
    def test_token_and_sanitized_device_list(self) -> None:
        client = EzvizClient(app_key="key", app_secret="secret")
        client._post = Mock(side_effect=[
            {"code": "200", "data": {"accessToken": "token", "expireTime": 9999999999999}},
            {"code": "200", "data": [{"deviceSerial": "D1", "deviceName": "cam",
              "deviceType": "C", "status": 1, "riskLevel": 0}], "page": {"total": 1}},
        ])
        result = client.list_devices()
        self.assertEqual(result["devices"][0]["device_serial"], "D1")
        self.assertTrue(result["devices"][0]["online"])
        self.assertNotIn("accessToken", str(result))

    def test_missing_credentials(self) -> None:
        client = EzvizClient(app_key="", app_secret="", access_token="")
        with self.assertRaises(EzvizError):
            client.access_token()


class StreamProbeTests(unittest.TestCase):
    def test_rejects_unknown_scheme(self) -> None:
        with self.assertRaises(ValueError):
            validate_source("file+unsafe://camera")

    def test_decodes_local_video(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "probe.avi"
            writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"MJPG"), 10, (64, 48))
            for value in range(12):
                writer.write(np.full((48, 64, 3), value * 10, dtype=np.uint8))
            writer.release()
            result = probe_video_source(str(path), frames=5)
            self.assertEqual(result["decoded_frames"], 5)
            self.assertEqual((result["width"], result["height"]), (64, 48))


class WebAppTests(unittest.TestCase):
    def test_health(self) -> None:
        response = TestClient(app).get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])


class PreFallStateTests(unittest.TestCase):
    def test_risk_level_uses_earliest_positive_horizon(self) -> None:
        self.assertEqual(risk_level([2, 4, 4], 2), "HIGH")
        self.assertEqual(risk_level([1, 2, 4], 2), "MEDIUM")
        self.assertEqual(risk_level([0, 1, 2], 2), "LOW")
        self.assertEqual(risk_level([0, 1, 1], 2), "NORMAL")


if __name__ == "__main__":
    unittest.main()
