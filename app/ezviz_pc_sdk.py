from __future__ import annotations

import ctypes
import json
import os
import threading
import time
from dataclasses import dataclass
from pathlib import Path


MESSAGE_PLAY_EXCEPTION = 0
MESSAGE_PLAY_START = 3
MESSAGE_PLAY_STOP = 4
CONFIG_OPEN_STREAMTRANS = 2
CONFIG_CLOSE_P2P = 3
CONFIG_VTDU_STREAM = 17
CONFIG_P2P_LIMIT = 19
NET_DVR_SYSHEAD = 1
NET_DVR_STREAMDATA = 2


class EzvizPcSdkError(RuntimeError):
    """Sanitized PC SDK error that never contains credentials."""


@dataclass(frozen=True)
class PcSdkCaptureResult:
    output_path: Path
    bytes_written: int
    callback_chunks: int
    stream_headers: int
    stream_chunks: int
    play_started: bool
    elapsed_seconds: float
    messages: tuple[dict[str, int], ...]


def default_sdk_root() -> Path:
    configured = os.getenv("EZVIZ_PC_SDK_ROOT")
    if configured:
        return Path(configured)
    project = Path(__file__).resolve().parents[1]
    return (
        project
        / "vendor_sources/ezviz_pc_sdk/v5.13.1"
        / "EZPCOpenSDK_v5.13.1_build20250714"
    )


class EzvizPcSdkRecorder:
    """Minimal ctypes bridge for encrypted EZOPEN live-stream capture on Windows."""

    def __init__(
        self,
        app_key: str,
        access_token: str,
        device_serial: str,
        device_code: str,
        channel_no: int = 1,
        sdk_root: Path | None = None,
    ) -> None:
        if os.name != "nt":
            raise EzvizPcSdkError("EZVIZ PC SDK bridge currently requires Windows")
        if not all((app_key, access_token, device_serial, device_code)):
            raise EzvizPcSdkError("app key, token, device serial and device code are required")
        self.app_key = app_key.encode("ascii")
        self.access_token = access_token.encode("ascii")
        self.device_serial = device_serial.encode("ascii")
        self.device_code = device_code.encode("ascii")
        self.channel_no = channel_no
        self.sdk_root = (sdk_root or default_sdk_root()).resolve()
        self.lib_dir = self.sdk_root / "lib/win64"
        self.dll_path = self.lib_dir / "OpenNetStream.dll"
        if not self.dll_path.is_file():
            raise EzvizPcSdkError("OpenNetStream.dll was not found; set EZVIZ_PC_SDK_ROOT")

        self._dll_directory = os.add_dll_directory(str(self.lib_dir))
        try:
            self.dll = ctypes.WinDLL(str(self.dll_path))
        except OSError as error:
            self._dll_directory.close()
            raise EzvizPcSdkError("OpenNetStream.dll or a dependency could not be loaded") from error

        self._message_callback_type = ctypes.WINFUNCTYPE(
            None,
            ctypes.c_char_p,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_char_p,
            ctypes.c_void_p,
        )
        self._data_callback_type = ctypes.WINFUNCTYPE(
            None,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_char),
            ctypes.c_int,
            ctypes.c_void_p,
            ctypes.c_char_p,
        )
        self._configure_signatures()
        self._messages: list[dict[str, int]] = []
        self._message_event = threading.Event()
        self._data_event = threading.Event()
        self._lock = threading.Lock()
        self._file = None
        self._bytes_written = 0
        self._callback_chunks = 0
        self._stream_headers = 0
        self._stream_chunks = 0
        self._message_callback = self._message_callback_type(self._on_message)
        self._data_callback = self._data_callback_type(self._on_data)
        self._session: bytes | None = None
        self._initialized = False

    def _configure_signatures(self) -> None:
        dll = self.dll
        dll.OpenSDK_Init.argtypes = [ctypes.c_char_p]
        dll.OpenSDK_Init.restype = ctypes.c_int
        dll.OpenSDK_FiniLib.argtypes = []
        dll.OpenSDK_FiniLib.restype = ctypes.c_int
        dll.OpenSDK_SetAccessToken.argtypes = [ctypes.c_char_p]
        dll.OpenSDK_SetAccessToken.restype = ctypes.c_int
        dll.OpenSDK_SetConfigInfo.argtypes = [ctypes.c_int, ctypes.c_int]
        dll.OpenSDK_SetConfigInfo.restype = None
        dll.OpenSDK_AllocSessionEx.argtypes = [
            self._message_callback_type,
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_char_p),
            ctypes.POINTER(ctypes.c_int),
        ]
        dll.OpenSDK_AllocSessionEx.restype = ctypes.c_int
        dll.OpenSDK_Data_Free.argtypes = [ctypes.c_void_p]
        dll.OpenSDK_Data_Free.restype = ctypes.c_int
        dll.OpenSDK_FreeSession.argtypes = [ctypes.c_char_p]
        dll.OpenSDK_FreeSession.restype = ctypes.c_int
        dll.OpenSDK_SetSessionConfig.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
        dll.OpenSDK_SetSessionConfig.restype = None
        dll.OpenSDK_SetDataCallBack.argtypes = [
            ctypes.c_char_p,
            self._data_callback_type,
            ctypes.c_void_p,
        ]
        dll.OpenSDK_SetDataCallBack.restype = ctypes.c_int
        dll.OpenSDK_StartRealPlayEx.argtypes = [
            ctypes.c_char_p,
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
        ]
        dll.OpenSDK_StartRealPlayEx.restype = ctypes.c_int
        dll.OpenSDK_StopRealPlayEx.argtypes = [ctypes.c_char_p]
        dll.OpenSDK_StopRealPlayEx.restype = ctypes.c_int
        dll.OpenSDK_GetLastErrorCode.argtypes = []
        dll.OpenSDK_GetLastErrorCode.restype = ctypes.c_int
        dll.OpenSDK_Data_GetP2PDeviceInfo.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_void_p),
            ctypes.POINTER(ctypes.c_int),
        ]
        dll.OpenSDK_Data_GetP2PDeviceInfo.restype = ctypes.c_int

    def _raise_last_error(self, operation: str, result: int) -> None:
        code = int(self.dll.OpenSDK_GetLastErrorCode())
        raise EzvizPcSdkError(f"{operation} failed (result={result}, sdk_code={code})")

    def _on_message(
        self,
        _session: bytes | None,
        message_type: int,
        error_code: int,
        _message_info: bytes | None,
        _user: int | None,
    ) -> None:
        with self._lock:
            self._messages.append(
                {"message_type": int(message_type), "error_code": int(error_code)}
            )
        self._message_event.set()

    def _on_data(
        self,
        data_type: int,
        data: ctypes.POINTER(ctypes.c_char),
        length: int,
        _user: int | None,
        _session: bytes | None,
    ) -> None:
        if not data or length <= 0:
            return
        payload = ctypes.string_at(data, length)
        with self._lock:
            if self._file is not None:
                self._file.write(payload)
                self._bytes_written += len(payload)
            self._callback_chunks += 1
            if data_type == NET_DVR_SYSHEAD:
                self._stream_headers += 1
            elif data_type == NET_DVR_STREAMDATA:
                self._stream_chunks += 1
        self._data_event.set()

    def initialize(self) -> None:
        result = int(self.dll.OpenSDK_Init(self.app_key))
        if result != 0:
            self._raise_last_error("OpenSDK_Init", result)
        self._initialized = True
        self.dll.OpenSDK_SetConfigInfo(CONFIG_CLOSE_P2P, 0)
        self.dll.OpenSDK_SetConfigInfo(CONFIG_VTDU_STREAM, 0)
        self.dll.OpenSDK_SetConfigInfo(CONFIG_P2P_LIMIT, 0)
        result = int(self.dll.OpenSDK_SetAccessToken(self.access_token))
        if result != 0:
            self.close()
            self._raise_last_error("OpenSDK_SetAccessToken", result)

        session_pointer = ctypes.c_char_p()
        session_length = ctypes.c_int()
        result = int(
            self.dll.OpenSDK_AllocSessionEx(
                self._message_callback,
                None,
                ctypes.byref(session_pointer),
                ctypes.byref(session_length),
            )
        )
        if result != 0 or not session_pointer.value:
            self.close()
            self._raise_last_error("OpenSDK_AllocSessionEx", result)
        try:
            self._session = bytes(session_pointer.value)
        finally:
            self.dll.OpenSDK_Data_Free(ctypes.cast(session_pointer, ctypes.c_void_p))

        self.dll.OpenSDK_SetSessionConfig(
            self._session, CONFIG_OPEN_STREAMTRANS, 1
        )
        result = int(
            self.dll.OpenSDK_SetDataCallBack(
                self._session, self._data_callback, None
            )
        )
        if result != 0:
            self.close()
            self._raise_last_error("OpenSDK_SetDataCallBack", result)

    def p2p_capabilities(self) -> dict[str, object]:
        """Return a whitelist-only view of the device P2P capability response."""
        if not self._initialized:
            self.initialize()
        output = ctypes.c_void_p()
        length = ctypes.c_int()
        result = int(
            self.dll.OpenSDK_Data_GetP2PDeviceInfo(
                self.access_token,
                self.device_serial,
                ctypes.byref(output),
                ctypes.byref(length),
            )
        )
        if result != 0 or not output.value:
            self._raise_last_error("OpenSDK_Data_GetP2PDeviceInfo", result)
        try:
            raw = ctypes.string_at(output, length.value)
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                text = raw.decode("gb18030")
            payload = json.loads(text.rstrip("\x00"))
        finally:
            self.dll.OpenSDK_Data_Free(output)
        result_payload = payload.get("result") or {}
        data = result_payload.get("data") or {}
        encoded_capabilities = data.get("ezDeviceCapability") or "{}"
        try:
            capabilities = json.loads(encoded_capabilities)
        except (TypeError, ValueError):
            capabilities = {}
        allowed = {
            "V3",
            "V3Sec",
            "V3Playback",
            "V3Download",
            "V3Talk",
            "DirectPlayback_EndFlag",
            "support_channel_number",
        }
        return {
            "api_code": str(result_payload.get("code", "")),
            "capabilities": {
                key: capabilities.get(key) for key in sorted(allowed) if key in capabilities
            },
        }

    def record(self, output_path: Path, duration_seconds: float = 15.0) -> PcSdkCaptureResult:
        if not self._session:
            self.initialize()
        output_path = output_path.resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        started = time.perf_counter()
        self._file = output_path.open("wb")
        result = int(
            self.dll.OpenSDK_StartRealPlayEx(
                self._session,
                None,
                self.device_serial,
                self.channel_no,
                self.device_code,
            )
        )
        if result != 0:
            self._file.close()
            self._file = None
            output_path.unlink(missing_ok=True)
            self._raise_last_error("OpenSDK_StartRealPlayEx", result)
        failed = False
        try:
            deadline = time.monotonic() + max(duration_seconds + 30.0, 45.0)
            play_started_at: float | None = None
            while time.monotonic() < deadline:
                with self._lock:
                    play_started = any(
                        item["message_type"] == MESSAGE_PLAY_START
                        for item in self._messages
                    )
                    exception = next(
                        (
                            item
                            for item in self._messages
                            if item["message_type"] == MESSAGE_PLAY_EXCEPTION
                        ),
                        None,
                    )
                if exception is not None:
                    raise EzvizPcSdkError(
                        "EZOPEN preview failed "
                        f"(sdk_error={exception['error_code']})"
                    )
                if play_started and play_started_at is None:
                    play_started_at = time.monotonic()
                if play_started_at is not None and self._data_event.is_set():
                    if time.monotonic() - play_started_at >= duration_seconds:
                        break
                self._message_event.wait(0.1)
                self._message_event.clear()
            if not self._data_event.is_set():
                raise EzvizPcSdkError("EZOPEN preview started but no stream data arrived")
        except BaseException:
            failed = True
            raise
        finally:
            self.dll.OpenSDK_StopRealPlayEx(self._session)
            time.sleep(0.5)
            with self._lock:
                if self._file is not None:
                    self._file.flush()
                    self._file.close()
                    self._file = None
            if failed:
                output_path.unlink(missing_ok=True)

        with self._lock:
            messages = tuple(self._messages)
            bytes_written = self._bytes_written
            callback_chunks = self._callback_chunks
            stream_headers = self._stream_headers
            stream_chunks = self._stream_chunks
            play_started = any(
                item["message_type"] == MESSAGE_PLAY_START for item in messages
            )
        if bytes_written <= 0:
            raise EzvizPcSdkError("EZOPEN capture produced an empty output")
        return PcSdkCaptureResult(
            output_path=output_path,
            bytes_written=bytes_written,
            callback_chunks=callback_chunks,
            stream_headers=stream_headers,
            stream_chunks=stream_chunks,
            play_started=play_started,
            elapsed_seconds=time.perf_counter() - started,
            messages=messages,
        )

    def close(self) -> None:
        if self._session:
            self.dll.OpenSDK_FreeSession(self._session)
            self._session = None
        if self._initialized:
            self.dll.OpenSDK_FiniLib()
            self._initialized = False
        if self._dll_directory is not None:
            self._dll_directory.close()
            self._dll_directory = None

    def __enter__(self) -> "EzvizPcSdkRecorder":
        self.initialize()
        return self

    def __exit__(self, _type, _value, _traceback) -> None:
        self.close()
