from __future__ import annotations

import os
import time
from dataclasses import dataclass

import requests


BASE_URL = "https://open.ys7.com"


class EzvizError(RuntimeError):
    """A sanitized EZVIZ Open API error (never contains credentials or stream URLs)."""


@dataclass(frozen=True)
class LiveAddress:
    url: str
    url_id: str | None
    expire_time: str | None


class EzvizClient:
    def __init__(
        self,
        app_key: str | None = None,
        app_secret: str | None = None,
        access_token: str | None = None,
        timeout_seconds: float = 15.0,
    ) -> None:
        self.app_key = app_key or os.getenv("YS7_APP_KEY")
        self.app_secret = app_secret or os.getenv("YS7_APP_SECRET")
        self._token = access_token or os.getenv("YS7_ACCESS_TOKEN")
        self._token_expire_ms = 0
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()

    def _post(self, path: str, data: dict[str, object]) -> dict:
        try:
            response = self.session.post(
                BASE_URL + path,
                data=data,
                timeout=self.timeout_seconds,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
            payload = response.json()
        except (requests.RequestException, ValueError) as error:
            raise EzvizError(f"EZVIZ request failed: {type(error).__name__}") from error
        if str(payload.get("code")) != "200":
            code = str(payload.get("code", "unknown"))
            message = str(payload.get("msg", "API error"))[:160]
            raise EzvizError(f"EZVIZ API error {code}: {message}")
        return payload

    def access_token(self, force_refresh: bool = False) -> str:
        now_ms = int(time.time() * 1000)
        if self._token and not force_refresh and (
            not self._token_expire_ms or now_ms < self._token_expire_ms - 300_000
        ):
            return self._token
        if not self.app_key or not self.app_secret:
            raise EzvizError(
                "YS7_APP_KEY/YS7_APP_SECRET (or YS7_ACCESS_TOKEN) is not configured"
            )
        payload = self._post(
            "/api/lapp/token/get",
            {"appKey": self.app_key, "appSecret": self.app_secret},
        )
        data = payload.get("data") or {}
        token = data.get("accessToken")
        if not token:
            raise EzvizError("EZVIZ token response did not contain accessToken")
        self._token = str(token)
        self._token_expire_ms = int(data.get("expireTime") or 0)
        return self._token

    def list_devices(self, page_start: int = 0, page_size: int = 50) -> dict:
        if page_start < 0 or not 1 <= page_size <= 50:
            raise ValueError("page_start must be >= 0 and page_size must be 1..50")
        payload = self._post(
            "/api/lapp/device/list",
            {
                "accessToken": self.access_token(),
                "pageStart": page_start,
                "pageSize": page_size,
            },
        )
        devices = []
        for item in payload.get("data") or []:
            devices.append(
                {
                    "device_serial": item.get("deviceSerial"),
                    "device_name": item.get("deviceName"),
                    "device_type": item.get("deviceType"),
                    "online": item.get("status") == 1,
                    "risk_level": item.get("riskLevel"),
                }
            )
        page = payload.get("page") or {}
        return {"devices": devices, "total": int(page.get("total") or len(devices))}

    def live_address(
        self,
        device_serial: str,
        channel_no: int = 1,
        protocol: int = 2,
        quality: int = 2,
        expire_seconds: int = 3600,
        device_code: str | None = None,
    ) -> LiveAddress:
        if protocol not in {1, 2, 3, 4, 5}:
            raise ValueError("protocol must be 1..5")
        body: dict[str, object] = {
            "accessToken": self.access_token(),
            "deviceSerial": device_serial,
            "channelNo": channel_no,
            "protocol": protocol,
            "quality": quality,
            "expireTime": expire_seconds,
            "type": "1",
            "supportH265": 0,
            "mute": 1,
        }
        code = device_code or os.getenv("YS7_DEVICE_CODE")
        if code:
            body["code"] = code
        payload = self._post("/api/lapp/v2/live/address/get", body)
        data = payload.get("data") or {}
        url = data.get("url")
        if not url:
            raise EzvizError("EZVIZ live-address response did not contain a URL")
        return LiveAddress(
            url=str(url),
            url_id=str(data.get("id")) if data.get("id") is not None else None,
            expire_time=str(data.get("expireTime")) if data.get("expireTime") else None,
        )
