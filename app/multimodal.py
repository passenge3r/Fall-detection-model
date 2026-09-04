from __future__ import annotations

import json
import re
import tempfile
import threading
import time
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np


CLASS_NAMES = ("walking", "standing", "sitting", "lying_sleeping", "falling")
SUMMARY_FALLBACK = {
    "walking": "人物正在行走，未见明显跌倒过程",
    "standing": "人物处于站立状态",
    "sitting": "人物处于坐姿",
    "lying_sleeping": "人物处于稳定躺卧状态",
    "falling": "人物出现向地面跌倒过程",
}

PROMPT = """Analyze these frames as ONE ordered video sequence from earliest to latest.
Independently review the visible human action. Do not assume a fall merely because this
clip was selected by another detector or because text overlays appear in the frames.

Choose exactly one action class: walking, standing, sitting, lying_sleeping, or falling.
- falling requires a visible uncontrolled or abrupt downward transition toward the floor.
- lying_sleeping means stable or intentional lying without a visible abrupt transition.
- use the initial, middle, and final posture; do not classify from the last frame alone.

Also assign fall_stage as normal, prefall, falling, or postfall and risk as low, medium,
or high, based only on visible temporal evidence.

Return exactly one JSON object without markdown:
{"class":"one_label","fall_stage":"one_stage","risk":"one_risk",
"confidence":0.00,"evidence":"at most 12 English words",
"summary_zh":"不超过20个汉字"}
"""


@dataclass(frozen=True)
class MultimodalReviewConfig:
    enabled: bool = False
    model_name: str = "Qwen/Qwen3-VL-2B-Instruct"
    adapter_path: Path | None = None
    device: str = "cuda"
    frames: int = 8
    buffer_frames: int = 160
    max_frame_edge: int = 640
    max_pixels: int = 128 * 32 * 32
    max_new_tokens: int = 112
    cooldown_seconds: float = 15.0
    post_trigger_seconds: float = 2.5
    trigger_levels: tuple[str, ...] = ("HIGH", "FALL_CONFIRMED")
    allow_download: bool = False


def _parse_json(text: str) -> dict[str, Any]:
    stripped = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        payload = json.loads(stripped)
        if isinstance(payload, dict):
            return payload
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
    if match:
        try:
            payload = json.loads(match.group(0))
            if isinstance(payload, dict):
                return payload
        except json.JSONDecodeError:
            pass
    # Generation can hit its token limit after emitting the useful leading fields.
    # Recover individual fields instead of turning a valid classification into a
    # parse error just because the final explanation string was truncated.
    recovered: dict[str, Any] = {}
    for key in ("class", "fall_stage", "risk", "evidence", "summary_zh"):
        field = re.search(rf'"{key}"\s*:\s*"([^"\r\n]*)', stripped)
        if field:
            recovered[key] = field.group(1)
    confidence = re.search(r'"confidence"\s*:\s*([01](?:\.\d+)?)', stripped)
    if confidence:
        recovered["confidence"] = float(confidence.group(1))
    return recovered


def _resize_for_buffer(frame: np.ndarray, max_edge: int) -> np.ndarray:
    height, width = frame.shape[:2]
    scale = min(1.0, max_edge / max(height, width))
    if scale == 1.0:
        return frame.copy()
    return cv2.resize(
        frame, (max(1, round(width * scale)), max(1, round(height * scale))),
        interpolation=cv2.INTER_AREA,
    )


class QwenVideoReviewer:
    """Lazy Qwen3-VL reviewer for short ordered RGB clips."""

    def __init__(self, config: MultimodalReviewConfig) -> None:
        self.config = config
        self.processor = None
        self.model = None

    def _load(self) -> None:
        if self.model is not None:
            return
        import torch
        from transformers import AutoProcessor, Qwen3VLForConditionalGeneration

        self.processor = AutoProcessor.from_pretrained(
            self.config.model_name,
            local_files_only=not self.config.allow_download,
        )
        self.model = Qwen3VLForConditionalGeneration.from_pretrained(
            self.config.model_name,
            dtype=torch.bfloat16,
            attn_implementation="sdpa",
            local_files_only=not self.config.allow_download,
        ).eval().to(self.config.device)
        if self.config.adapter_path is not None:
            from peft import PeftModel

            self.model = PeftModel.from_pretrained(
                self.model, self.config.adapter_path, local_files_only=True
            ).eval()

    def review(self, frames: list[np.ndarray], context: dict[str, Any]) -> dict[str, Any]:
        import torch

        started = time.perf_counter()
        self._load()
        assert self.processor is not None and self.model is not None
        indices = np.linspace(0, len(frames) - 1, self.config.frames).round().astype(int)
        selected = [
            _resize_for_buffer(frames[int(index)], self.config.max_frame_edge)
            for index in indices
        ]
        with tempfile.TemporaryDirectory(prefix="fall_qwen_review_") as temporary:
            root = Path(temporary)
            paths = []
            for index, frame in enumerate(selected):
                path = root / f"frame_{index:02d}.jpg"
                if not cv2.imwrite(str(path), frame, [cv2.IMWRITE_JPEG_QUALITY, 88]):
                    raise RuntimeError(f"Could not write review frame {index}")
                paths.append(str(path.resolve()))
            messages = [{"role": "user", "content": [
                {
                    "type": "video", "video": paths, "sample_fps": 2,
                    "min_pixels": 4 * 32 * 32, "max_pixels": self.config.max_pixels,
                },
                {"type": "text", "text": PROMPT},
            ]}]
            inputs = self.processor.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True,
                return_dict=True, return_tensors="pt",
                processor_kwargs={"videos_kwargs": {"do_sample_frames": False}},
            ).to(self.config.device)
            with torch.inference_mode():
                generated = self.model.generate(
                    **inputs, max_new_tokens=self.config.max_new_tokens, do_sample=False
                )
            raw = self.processor.batch_decode(
                generated[:, inputs.input_ids.shape[1]:],
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )[0].strip()
        payload = _parse_json(raw)
        action = str(payload.get("class", "parse_error")).strip().lower()
        if action not in CLASS_NAMES:
            action = "parse_error"
        confidence = payload.get("confidence")
        try:
            confidence = min(1.0, max(0.0, float(confidence)))
        except (TypeError, ValueError):
            confidence = None
        stage = str(payload.get("fall_stage", "unknown")).strip().lower()
        if action == "falling" and confidence is not None and confidence >= 0.6:
            review_outcome = "CORROBORATED_FALL"
        elif stage == "prefall":
            review_outcome = "CORROBORATED_PREFALL"
        elif stage == "postfall":
            review_outcome = "CORROBORATED_POSTFALL"
        elif action in {"walking", "standing", "sitting", "lying_sleeping"}:
            review_outcome = "NOT_CORROBORATED"
        else:
            review_outcome = "INCONCLUSIVE"
        evidence = str(payload.get("evidence", "")).strip()[:240]
        summary = str(payload.get("summary_zh", "")).strip()
        if not summary:
            summary = SUMMARY_FALLBACK.get(action, "多模态复核结果不明确")
            if stage == "prefall":
                summary = "人物出现跌倒前动作迹象"
        return {
            "enabled": True,
            "status": "READY",
            "model": self.config.model_name,
            "adapter": str(self.config.adapter_path) if self.config.adapter_path else None,
            "action_class": action,
            "fall_stage": stage,
            "risk_level": str(payload.get("risk", "unknown")).upper(),
            "confidence": confidence,
            "evidence": evidence,
            "summary_zh": summary,
            "review_outcome": review_outcome,
            "model_output_valid": action != "parse_error",
            "frames_reviewed": len(selected),
            "latency_seconds": time.perf_counter() - started,
            "raw_output": raw,
            "advisory_only": True,
            "completed_at_ms": int(time.time() * 1000),
        }


class MultimodalReviewService:
    """Non-blocking RGB buffer and single-job Qwen review worker."""

    def __init__(self, config: MultimodalReviewConfig) -> None:
        self.config = config
        self.reviewer = QwenVideoReviewer(config)
        self.frames: deque[np.ndarray] = deque(maxlen=config.buffer_frames)
        self._lock = threading.RLock()
        self._thread: threading.Thread | None = None
        self._pending_context: dict[str, Any] | None = None
        self._pending_frames = 0
        self._last_trigger_at = 0.0
        self._status: dict[str, Any] = {
            "enabled": config.enabled,
            "status": "IDLE" if config.enabled else "DISABLED",
            "model": config.model_name,
            "advisory_only": True,
            "config": {
                **asdict(config),
                "adapter_path": str(config.adapter_path) if config.adapter_path else None,
            },
        }

    def observe(self, frame: np.ndarray) -> None:
        if not self.config.enabled:
            return
        self.frames.append(_resize_for_buffer(frame, self.config.max_frame_edge))
        with self._lock:
            if self._pending_context is None:
                return
            self._pending_frames -= 1
            self._status["post_frames_remaining"] = max(0, self._pending_frames)
            if self._pending_frames <= 0:
                context = self._pending_context
                self._pending_context = None
                self._start_locked(context)

    def reset_buffer(self) -> None:
        self.frames.clear()
        with self._lock:
            self._pending_context = None
            self._pending_frames = 0
            if not (self._thread and self._thread.is_alive()):
                self._status = {
                    "enabled": self.config.enabled,
                    "status": "IDLE" if self.config.enabled else "DISABLED",
                    "model": self.config.model_name,
                    "advisory_only": True,
                }

    def schedule(
        self, context: dict[str, Any], post_frames: int = 0, force: bool = False
    ) -> bool:
        if not self.config.enabled or len(self.frames) < self.config.frames:
            return False
        with self._lock:
            if (self._thread and self._thread.is_alive()) or self._pending_context is not None:
                return False
            now = time.monotonic()
            if not force and now - self._last_trigger_at < self.config.cooldown_seconds:
                return False
            self._last_trigger_at = now
            if post_frames > 0:
                self._pending_context = context
                self._pending_frames = post_frames
                self._status = {
                    **self._status,
                    "status": "WAITING_POST_FRAMES",
                    "trigger_context": context,
                    "triggered_at_ms": int(time.time() * 1000),
                    "post_frames_remaining": post_frames,
                    "error": None,
                }
                return True
            self._start_locked(context)
            return True

    def trigger(self, context: dict[str, Any], force: bool = False) -> bool:
        return self.schedule(context, post_frames=0, force=force)

    def _start_locked(self, context: dict[str, Any]) -> None:
        snapshot = [frame.copy() for frame in self.frames]
        self._status = {
            **self._status,
            "status": "RUNNING",
            "trigger_context": context,
            "triggered_at_ms": int(time.time() * 1000),
            "error": None,
        }
        self._thread = threading.Thread(
            target=self._run, args=(snapshot, context), daemon=True,
            name="qwen-multimodal-review",
        )
        self._thread.start()

    def _run(self, frames: list[np.ndarray], context: dict[str, Any]) -> None:
        try:
            result = self.reviewer.review(frames, context)
            outcome = result.get("review_outcome")
            if outcome == "CORROBORATED_FALL":
                fusion = "ESCALATE_CONFIRMED"
            elif outcome in {"CORROBORATED_PREFALL", "CORROBORATED_POSTFALL"}:
                fusion = "VISUALLY_SUPPORTED"
            elif outcome == "NOT_CORROBORATED":
                fusion = "SKELETON_ONLY_CONFLICT"
            else:
                fusion = "INCONCLUSIVE"
            with self._lock:
                self._status = {
                    **result,
                    "fusion_decision": fusion,
                    "trigger_context": context,
                    "error": None,
                }
        except Exception as error:
            with self._lock:
                self._status = {
                    **self._status,
                    "status": "ERROR",
                    "error": f"{type(error).__name__}: {str(error)[:300]}",
                    "completed_at_ms": int(time.time() * 1000),
                }

    def status(self) -> dict[str, Any]:
        with self._lock:
            return dict(self._status)
