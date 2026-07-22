from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import cv2
import numpy as np


COCO_KEYPOINTS = [
    "nose", "left_eye", "right_eye", "left_ear", "right_ear",
    "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_hip", "right_hip",
    "left_knee", "right_knee", "left_ankle", "right_ankle",
]


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sample_video(
    path: Path, frames: int, start_frame: int | None = None, end_frame: int | None = None
) -> tuple[list[np.ndarray], np.ndarray, tuple[int, int]]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {path}")
    total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if total <= 0:
        raise RuntimeError(f"Invalid frame count: {path}")
    start = 0 if start_frame is None else start_frame
    end = total - 1 if end_frame is None else end_frame
    if start < 0 or end < start or end >= total:
        raise RuntimeError(f"Invalid frame interval [{start}, {end}] for {path} ({total} frames)")
    indices = np.rint(np.linspace(start, end, frames)).astype(np.int32)
    decoded: list[np.ndarray] = []
    decoded_by_index: dict[int, np.ndarray] = {}
    for index in indices:
        key = int(index)
        if key not in decoded_by_index:
            capture.set(cv2.CAP_PROP_POS_FRAMES, key)
            ok, image = capture.read()
            if not ok or image is None:
                capture.release()
                raise RuntimeError(f"Cannot decode frame {index}: {path}")
            decoded_by_index[key] = image
        decoded.append(decoded_by_index[key])
    capture.release()
    height, width = decoded[0].shape[:2]
    return decoded, indices, (height, width)


class YoloPoseBackend:
    def __init__(self, model_path: str, device: str, confidence: float) -> None:
        import os

        # Keep Ultralytics settings inside the project so sandboxed and shared
        # runs do not depend on a user's roaming AppData permissions.
        config_dir = Path(__file__).resolve().parent.parent / ".ultralytics"
        config_dir.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("YOLO_CONFIG_DIR", str(config_dir))
        from ultralytics import YOLO

        self.model = YOLO(model_path)
        self.device = device
        self.confidence = confidence

    def __call__(self, image: np.ndarray) -> np.ndarray:
        result = self.model.predict(
            image, device=self.device, conf=self.confidence, verbose=False
        )[0]
        if result.keypoints is None or result.boxes is None or len(result.boxes) == 0:
            return np.zeros((17, 3), dtype=np.float32)
        boxes = result.boxes.xyxy.detach().cpu().numpy()
        areas = np.maximum(0, boxes[:, 2] - boxes[:, 0]) * np.maximum(0, boxes[:, 3] - boxes[:, 1])
        selected = int(np.argmax(areas))
        points = result.keypoints.data[selected].detach().cpu().numpy().astype(np.float32)
        if points.shape != (17, 3):
            raise RuntimeError(f"Expected YOLO COCO-17 keypoints, got {points.shape}")
        return points


class RTMPoseBackend:
    def __init__(self, mode: str, device: str, one_stage: bool = False) -> None:
        self._dll_handles = []
        if device.lower().startswith("cuda"):
            import os
            import onnxruntime as ort

            # Windows CUDA wheels use a shared ``nvidia/cu13`` directory rather
            # than the Linux-oriented ``*-cu13`` distribution names that ORT's
            # automatic discovery expects. Load both wheel directories explicitly.
            nvidia_root = Path(ort.__file__).resolve().parent.parent / "nvidia"
            dll_dirs = [nvidia_root / "cu13" / "bin" / "x86_64", nvidia_root / "cudnn" / "bin"]
            for dll_dir in dll_dirs:
                if dll_dir.is_dir():
                    self._dll_handles.append(os.add_dll_directory(str(dll_dir)))
            if hasattr(ort, "preload_dlls"):
                for dll_dir in dll_dirs:
                    if dll_dir.is_dir():
                        ort.preload_dlls(directory=str(dll_dir))
        from rtmlib import Body

        self.model = Body(
            pose="rtmo" if one_stage else None,
            mode=mode,
            backend="onnxruntime",
            device=device,
            to_openpose=False,
        )
        sessions = []
        for component in vars(self.model).values():
            session = getattr(component, "session", None)
            if hasattr(session, "get_providers"):
                sessions.append(session)
        providers = [session.get_providers() for session in sessions]
        if providers:
            name = "RTMO" if one_stage else "RTMPose"
            print(f"{name} execution providers: {providers}", flush=True)

    def __call__(self, image: np.ndarray) -> np.ndarray:
        keypoints, scores = self.model(image)
        keypoints = np.asarray(keypoints, dtype=np.float32)
        scores = np.asarray(scores, dtype=np.float32)
        if keypoints.size == 0:
            return np.zeros((17, 3), dtype=np.float32)
        if keypoints.ndim == 2:
            keypoints = keypoints[None, ...]
        if scores.ndim == 1:
            scores = scores[None, ...]
        if keypoints.shape[1] != 17:
            raise RuntimeError(f"Expected RTMPose COCO-17 keypoints, got {keypoints.shape}")
        quality = []
        for person_points, person_scores in zip(keypoints, scores):
            valid = person_scores >= 0.2
            if not np.any(valid):
                quality.append(0.0)
                continue
            extent = np.ptp(person_points[valid], axis=0)
            quality.append(float(extent[0] * extent[1] * np.mean(person_scores[valid])))
        selected = int(np.argmax(quality))
        return np.concatenate([keypoints[selected], scores[selected, :, None]], axis=1).astype(np.float32)


class MMPoseHourglassBackend:
    """Top-down MMPose Hourglass52 with a YOLO person-box frontend."""

    def __init__(self, config: str, checkpoint: str, detector: str,
                 device: str, confidence: float) -> None:
        import os
        import importlib.util
        import sys
        import types

        config_dir = Path(__file__).resolve().parent.parent / ".ultralytics"
        config_dir.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("YOLO_CONFIG_DIR", str(config_dir))
        # MMPose 1.3 eagerly imports EDPose even when building Hourglass.
        # EDPose needs compiled mmcv ops, while Hourglass uses only standard
        # PyTorch layers.  Stub that unused registration when running mmcv-lite.
        if importlib.util.find_spec("mmcv._ext") is None:
            module_name = "mmpose.models.heads.transformer_heads"
            stub = types.ModuleType(module_name)
            stub.EDPoseHead = None
            sys.modules.setdefault(module_name, stub)
        from mmpose.apis import inference_topdown, init_model
        from ultralytics import YOLO

        self.detector = YOLO(detector)
        self.model = init_model(config, checkpoint, device=device)
        self.inference_topdown = inference_topdown
        self.device = device
        self.confidence = confidence

    def __call__(self, image: np.ndarray) -> np.ndarray:
        detected = self.detector.predict(
            image, device=self.device, conf=self.confidence, verbose=False
        )[0]
        if detected.boxes is None or len(detected.boxes) == 0:
            return np.zeros((17, 3), dtype=np.float32)
        boxes = detected.boxes.xyxy.detach().cpu().numpy()
        areas = np.maximum(0, boxes[:, 2] - boxes[:, 0]) * np.maximum(0, boxes[:, 3] - boxes[:, 1])
        bbox = boxes[int(np.argmax(areas))][None, :]
        samples = self.inference_topdown(
            self.model, image, bboxes=bbox, bbox_format="xyxy"
        )
        if not samples:
            return np.zeros((17, 3), dtype=np.float32)
        instances = samples[0].pred_instances
        keypoints = np.asarray(instances.keypoints, dtype=np.float32)
        scores = np.asarray(instances.keypoint_scores, dtype=np.float32)
        if keypoints.ndim == 3:
            keypoints = keypoints[0]
        if scores.ndim == 2:
            scores = scores[0]
        if keypoints.shape != (17, 2) or scores.shape != (17,):
            raise RuntimeError(
                f"Expected Hourglass COCO-17 output, got {keypoints.shape} and {scores.shape}"
            )
        return np.concatenate([keypoints, scores[:, None]], axis=1).astype(np.float32)


class OpenPoseBackend:
    """Official OpenPose COCO Caffe model with a shared YOLO person box."""

    # OpenPose COCO-18 -> COCO-17 (neck is intentionally omitted).
    COCO17_FROM_OPENPOSE = (0, 15, 14, 17, 16, 5, 2, 6, 3, 7, 4, 11, 8, 12, 9, 13, 10)

    def __init__(self, prototxt: str, checkpoint: str, detector: str,
                 device: str, confidence: float, input_size: int) -> None:
        import os

        config_dir = Path(__file__).resolve().parent.parent / ".ultralytics"
        config_dir.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("YOLO_CONFIG_DIR", str(config_dir))
        from ultralytics import YOLO

        self.detector = YOLO(detector)
        self.net = cv2.dnn.readNetFromCaffe(prototxt, checkpoint)
        self.device = device
        self.confidence = confidence
        self.input_size = input_size

    def __call__(self, image: np.ndarray) -> np.ndarray:
        detected = self.detector.predict(
            image, device=self.device, conf=self.confidence, verbose=False
        )[0]
        if detected.boxes is None or len(detected.boxes) == 0:
            return np.zeros((17, 3), dtype=np.float32)
        boxes = detected.boxes.xyxy.detach().cpu().numpy()
        areas = np.maximum(0, boxes[:, 2] - boxes[:, 0]) * np.maximum(0, boxes[:, 3] - boxes[:, 1])
        x1, y1, x2, y2 = boxes[int(np.argmax(areas))]
        height, width = image.shape[:2]
        x1, y1 = max(0, int(np.floor(x1))), max(0, int(np.floor(y1)))
        x2, y2 = min(width, int(np.ceil(x2))), min(height, int(np.ceil(y2)))
        if x2 <= x1 or y2 <= y1:
            return np.zeros((17, 3), dtype=np.float32)
        crop = image[y1:y2, x1:x2]
        blob = cv2.dnn.blobFromImage(
            crop, 1.0 / 255.0, (self.input_size, self.input_size),
            (0, 0, 0), swapRB=False, crop=False,
        )
        self.net.setInput(blob)
        output = self.net.forward()
        if output.ndim != 4 or output.shape[1] < 18:
            raise RuntimeError(f"Unexpected OpenPose output: {output.shape}")
        heat_h, heat_w = output.shape[2:]
        points = np.zeros((18, 3), dtype=np.float32)
        for joint in range(18):
            _, peak, _, location = cv2.minMaxLoc(output[0, joint])
            points[joint] = (
                x1 + location[0] * (x2 - x1) / heat_w,
                y1 + location[1] * (y2 - y1) / heat_h,
                peak,
            )
        return points[np.asarray(self.COCO17_FROM_OPENPOSE)].copy()


class TorchOpenPoseBackend:
    """GPU PyTorch port converted directly from the CMU OpenPose Caffe model."""

    COCO17_FROM_OPENPOSE = OpenPoseBackend.COCO17_FROM_OPENPOSE

    def __init__(self, repo: str, checkpoint: str, detector: str,
                 device: str, confidence: float, input_size: int,
                 batch_size: int) -> None:
        import os
        import sys
        import torch

        config_dir = Path(__file__).resolve().parent.parent / ".ultralytics"
        config_dir.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("YOLO_CONFIG_DIR", str(config_dir))
        sys.path.insert(0, repo)
        from src.model import bodypose_model
        from ultralytics import YOLO

        self.model = bodypose_model()
        converted = torch.load(checkpoint, map_location="cpu")
        transferred = {
            name: converted[".".join(name.split(".")[1:])]
            for name in self.model.state_dict()
        }
        self.model.load_state_dict(transferred)
        self.model.to(device).eval()
        self.detector = YOLO(detector)
        self.torch = torch
        self.device = device
        self.confidence = confidence
        self.input_size = input_size
        self.batch_size = batch_size

    def __call__(self, image: np.ndarray) -> np.ndarray:
        return self.batch([image])[0]

    def batch(self, images: list[np.ndarray]) -> list[np.ndarray]:
        results = [np.zeros((17, 3), dtype=np.float32) for _ in images]
        detected_batch = self.detector.predict(
            images, device=self.device, conf=self.confidence,
            verbose=False, batch=self.batch_size,
        )
        tensors = []
        selected_boxes = []
        positions = []
        for position, (image, detected) in enumerate(zip(images, detected_batch)):
            if detected.boxes is None or len(detected.boxes) == 0:
                continue
            boxes = detected.boxes.xyxy.detach().cpu().numpy()
            areas = np.maximum(0, boxes[:, 2] - boxes[:, 0]) * np.maximum(0, boxes[:, 3] - boxes[:, 1])
            x1, y1, x2, y2 = boxes[int(np.argmax(areas))]
            height, width = image.shape[:2]
            x1, y1 = max(0, int(np.floor(x1))), max(0, int(np.floor(y1)))
            x2, y2 = min(width, int(np.ceil(x2))), min(height, int(np.ceil(y2)))
            if x2 <= x1 or y2 <= y1:
                continue
            crop = cv2.resize(
                image[y1:y2, x1:x2], (self.input_size, self.input_size),
                interpolation=cv2.INTER_CUBIC,
            )
            tensor = self.torch.from_numpy(
                np.ascontiguousarray(crop.transpose(2, 0, 1))
            ).float().div_(256.0).sub_(0.5)
            tensors.append(tensor)
            selected_boxes.append((x1, y1, x2, y2))
            positions.append(position)

        mapping = np.asarray(self.COCO17_FROM_OPENPOSE)
        for start in range(0, len(tensors), self.batch_size):
            end = start + self.batch_size
            batch = self.torch.stack(tensors[start:end]).to(self.device)
            with self.torch.no_grad():
                _, heatmaps = self.model(batch)
            heatmaps = heatmaps[:, :18]
            flat = heatmaps.flatten(2)
            scores, indices = flat.max(dim=2)
            heat_w = heatmaps.shape[3]
            xs = (indices % heat_w).float()
            ys = (indices // heat_w).float()
            for offset in range(len(heatmaps)):
                source = start + offset
                x1, y1, x2, y2 = selected_boxes[source]
                points = self.torch.stack(
                    [
                        x1 + xs[offset] * (x2 - x1) / heat_w,
                        y1 + ys[offset] * (y2 - y1) / heatmaps.shape[2],
                        scores[offset].clamp_min(0),
                    ],
                    dim=1,
                ).cpu().numpy().astype(np.float32)
                results[positions[source]] = points[mapping].copy()
        return results


class AlphaPoseBackend:
    """Official AlphaPose FastPose-ResNet50 with the shared YOLO person box."""

    def __init__(self, repo: str, config: str, checkpoint: str, detector: str,
                 device: str, confidence: float, batch_size: int) -> None:
        import os
        import sys

        config_dir = Path(__file__).resolve().parent.parent / ".ultralytics"
        config_dir.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("YOLO_CONFIG_DIR", str(config_dir))
        sys.path.insert(0, repo)

        import torch
        import torchvision.models as torchvision_models
        from alphapose.models import builder
        from alphapose.utils.config import update_config
        from alphapose.utils.presets import SimpleTransform
        from alphapose.utils.transforms import heatmap_to_coord_simple
        from ultralytics import YOLO

        cfg = update_config(config)
        # FastPose's constructor requests an ImageNet ResNet even though the
        # complete official checkpoint is loaded immediately afterwards. Avoid
        # a redundant network download by constructing that temporary backbone
        # with random weights.
        original_resnet50 = torchvision_models.resnet50
        torchvision_models.resnet50 = lambda pretrained=True, **kwargs: original_resnet50(weights=None)
        try:
            self.model = builder.build_sppe(cfg.MODEL, preset_cfg=cfg.DATA_PRESET)
        finally:
            torchvision_models.resnet50 = original_resnet50
        self.model.load_state_dict(torch.load(checkpoint, map_location=device))
        self.model.to(device).eval()

        class CocoLayout:
            joint_pairs = [[1, 2], [3, 4], [5, 6], [7, 8],
                           [9, 10], [11, 12], [13, 14], [15, 16]]

        self.transform = SimpleTransform(
            CocoLayout(), scale_factor=0, add_dpg=False,
            input_size=cfg.DATA_PRESET.IMAGE_SIZE,
            output_size=cfg.DATA_PRESET.HEATMAP_SIZE,
            rot=0, sigma=cfg.DATA_PRESET.SIGMA, train=False,
        )
        self.detector = YOLO(detector)
        self.heatmap_to_coord = heatmap_to_coord_simple
        self.torch = torch
        self.device = device
        self.confidence = confidence
        self.batch_size = batch_size

    def __call__(self, image: np.ndarray) -> np.ndarray:
        return self.batch([image])[0]

    def batch(self, images: list[np.ndarray]) -> list[np.ndarray]:
        """Batch detector and pose inference to keep the GPU saturated."""
        results = [np.zeros((17, 3), dtype=np.float32) for _ in images]
        detected_batch = self.detector.predict(
            images, device=self.device, conf=self.confidence,
            verbose=False, batch=self.batch_size,
        )
        inputs = []
        cropped_boxes = []
        positions = []
        for position, (image, detected) in enumerate(zip(images, detected_batch)):
            if detected.boxes is None or len(detected.boxes) == 0:
                continue
            boxes = detected.boxes.xyxy.detach().cpu().numpy()
            areas = np.maximum(0, boxes[:, 2] - boxes[:, 0]) * np.maximum(0, boxes[:, 3] - boxes[:, 1])
            bbox = boxes[int(np.argmax(areas))]
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            inp, cropped_box = self.transform.test_transform(rgb, bbox)
            inputs.append(inp)
            cropped_boxes.append(cropped_box)
            positions.append(position)
        for start in range(0, len(inputs), self.batch_size):
            end = start + self.batch_size
            batch = self.torch.stack(inputs[start:end]).to(self.device)
            with self.torch.no_grad():
                heatmaps = self.model(batch).cpu()
            for offset, heatmap in enumerate(heatmaps):
                source = start + offset
                coords, scores = self.heatmap_to_coord(heatmap, cropped_boxes[source])
                scores = np.asarray(scores, dtype=np.float32).reshape(17, 1)
                results[positions[source]] = np.concatenate(
                    [np.asarray(coords, dtype=np.float32), scores], axis=1
                )
        return results

def safe_stem(relative_path: str) -> str:
    path = Path(relative_path)
    return "__".join(path.with_suffix("").parts).replace(" ", "_")


def cache_stem(row: dict[str, str]) -> str:
    stem = safe_stem(row["path"])
    if row.get("start_frame") and row.get("end_frame"):
        stem += f"__f{row['start_frame']}_{row['end_frame']}"
    return stem


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--video-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    parser.add_argument(
        "--backend", choices=("yolo", "rtmpose", "rtmo", "hourglass", "openpose", "alphapose"), required=True
    )
    parser.add_argument("--frames", type=int, default=64)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--yolo-model", default="yolo26n-pose.pt")
    parser.add_argument("--yolo-conf", type=float, default=0.1)
    parser.add_argument("--rtmpose-mode", choices=("lightweight", "balanced", "performance"), default="balanced")
    parser.add_argument(
        "--hourglass-config",
        default="vendor_sources/mmpose/configs/body_2d_keypoint/topdown_heatmap/coco/"
                "td-hm_hourglass52_8xb32-210e_coco-256x256.py",
    )
    parser.add_argument(
        "--hourglass-checkpoint",
        default="https://download.openmmlab.com/mmpose/top_down/hourglass/"
                "hourglass52_coco_256x256-4ec713ba_20200709.pth",
    )
    parser.add_argument("--hourglass-detector", default="yolo26n-pose.pt")
    parser.add_argument(
        "--openpose-prototxt",
        default="vendor_sources/openpose/models/pose/coco/pose_deploy_linevec.prototxt",
    )
    parser.add_argument(
        "--openpose-checkpoint",
        default="vendor_sources/openpose/models/pose/coco/pose_iter_440000.caffemodel",
    )
    parser.add_argument("--openpose-detector", default="yolo26n-pose.pt")
    parser.add_argument("--openpose-input-size", type=int, default=256)
    parser.add_argument("--openpose-runtime", choices=("torch", "caffe"), default="torch")
    parser.add_argument("--openpose-torch-repo", default="vendor_sources/pytorch-openpose")
    parser.add_argument("--openpose-torch-checkpoint", default="models/openpose_body_pose_model.pth")
    parser.add_argument("--openpose-batch-size", type=int, default=8)
    parser.add_argument("--alphapose-repo", default="vendor_sources/AlphaPose")
    parser.add_argument(
        "--alphapose-config",
        default="vendor_sources/AlphaPose/configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml",
    )
    parser.add_argument(
        "--alphapose-checkpoint",
        default="models/alphapose/fast_res50_256x192.pth",
    )
    parser.add_argument("--alphapose-detector", default="yolo26n-pose.pt")
    parser.add_argument("--alphapose-batch-size", type=int, default=32)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--path-contains")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    rows = read_manifest(args.manifest)
    if args.path_contains:
        rows = [row for row in rows if args.path_contains in row["path"]]
    if args.limit is not None:
        rows = rows[: args.limit]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    if args.backend == "yolo":
        backend = YoloPoseBackend(args.yolo_model, args.device, args.yolo_conf)
    elif args.backend == "hourglass":
        backend = MMPoseHourglassBackend(
            args.hourglass_config, args.hourglass_checkpoint,
            args.hourglass_detector, args.device, args.yolo_conf,
        )
    elif args.backend == "openpose":
        if args.openpose_runtime == "torch":
            backend = TorchOpenPoseBackend(
                args.openpose_torch_repo, args.openpose_torch_checkpoint,
                args.openpose_detector, args.device, args.yolo_conf,
                args.openpose_input_size, args.openpose_batch_size,
            )
        else:
            backend = OpenPoseBackend(
                args.openpose_prototxt, args.openpose_checkpoint,
                args.openpose_detector, args.device, args.yolo_conf,
                args.openpose_input_size,
            )
    elif args.backend == "alphapose":
        backend = AlphaPoseBackend(
            args.alphapose_repo, args.alphapose_config,
            args.alphapose_checkpoint, args.alphapose_detector,
            args.device, args.yolo_conf, args.alphapose_batch_size,
        )
    else:
        backend = RTMPoseBackend(
            args.rtmpose_mode, args.device, one_stage=args.backend == "rtmo"
        )

    output_rows = []
    for item_number, row in enumerate(rows, start=1):
        video_path = args.video_root / row["path"]
        output_path = args.output_dir / f"{cache_stem(row)}.npz"
        if not output_path.exists() or args.overwrite:
            start_frame = int(row["start_frame"]) if row.get("start_frame") else None
            end_frame = int(row["end_frame"]) if row.get("end_frame") else None
            images, indices, image_size = sample_video(
                video_path, args.frames, start_frame=start_frame, end_frame=end_frame
            )
            # Short annotated intervals can contain fewer unique frames than the
            # fixed output length. Infer each source frame once, then repeat its
            # cached pose at the requested temporal positions.
            unique_images: dict[int, np.ndarray] = {}
            for frame_index, image in zip(indices, images):
                unique_images.setdefault(int(frame_index), image)
            if hasattr(backend, "batch"):
                keys = list(unique_images)
                inferred = dict(zip(keys, backend.batch([unique_images[key] for key in keys])))
            else:
                inferred = {key: backend(image) for key, image in unique_images.items()}
            pose_sequence = [inferred[int(frame_index)] for frame_index in indices]
            poses = np.stack(pose_sequence).astype(np.float32)
            np.savez_compressed(
                output_path,
                keypoints=poses,
                frame_indices=indices,
                image_size=np.asarray(image_size, dtype=np.int32),
                keypoint_names=np.asarray(COCO_KEYPOINTS),
            )
        with np.load(output_path) as cached:
            poses = cached["keypoints"]
        confidence = poses[:, :, 2]
        output_rows.append(
            {
                **row,
                "pose_path": output_path.as_posix(),
                "backend": args.backend,
                "frames": str(args.frames),
                "zero_pose_frames": str(int(np.sum(np.max(confidence, axis=1) == 0))),
                "mean_confidence": f"{float(np.mean(confidence)):.6f}",
            }
        )
        print(f"[{item_number}/{len(rows)}] {row['path']}", flush=True)

    fields = list(output_rows[0]) if output_rows else []
    with args.output_manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)
    summary = {
        "backend": args.backend,
        "videos": len(output_rows),
        "frames_per_video": args.frames,
        "zero_pose_frames": sum(int(row["zero_pose_frames"]) for row in output_rows),
        "mean_confidence": float(np.mean([float(row["mean_confidence"]) for row in output_rows])),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
