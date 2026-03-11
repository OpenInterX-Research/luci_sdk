"""Session envelope contract aligned with Lucia log schema."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import time
import uuid
from typing import Any


VALID_DEVICE_MODES = {"USB", "WIFI"}
VALID_TASK_TYPES = {"navigation", "measurement", "video_qa"}
VALID_NETWORK_CONDITIONS = {"normal", "weak", "lossy"}
VALID_FAILURE_TYPES = {
    "none",
    "connect_fail",
    "stream_init_fail",
    "frame_drop_high",
    "reconnect_slow",
    "sync_drift",
    "long_horizon_error",
    "landmark_hallucination",
    "repetitive_corridor_confusion",
    "instruction_not_actionable",
    "reflective_surface_fail",
    "textureless_fail",
    "mask_error",
    "depth_hole",
    "scale_alignment_fail",
    "other",
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _new_session_id() -> str:
    return str(uuid.uuid4())


def _to_ms(value_seconds: float) -> float:
    return round(value_seconds * 1000.0, 3)


@dataclass
class SessionRecord:
    """Mutable run record that serializes to the schema envelope."""

    payload: dict[str, Any]
    package: str
    run_id: str
    _started_at: float

    def set_timing(
        self,
        capture_ms: float = 0.0,
        prompt_build_ms: float = 0.0,
        inference_ms: float = 0.0,
        postprocess_ms: float = 0.0,
        render_ms: float = 0.0,
        end_to_end_ms: float | None = None,
    ) -> None:
        timing = self.payload["timing_ms"]
        timing["capture"] = float(capture_ms)
        timing["prompt_build"] = float(prompt_build_ms)
        timing["inference"] = float(inference_ms)
        timing["postprocess"] = float(postprocess_ms)
        timing["render"] = float(render_ms)
        timing["end_to_end"] = (
            float(end_to_end_ms)
            if end_to_end_ms is not None
            else float(capture_ms + prompt_build_ms + inference_ms + postprocess_ms + render_ms)
        )

    def set_stream_metrics(
        self,
        resolution: str | None = None,
        fps_target: float | None = None,
        fps_achieved: float | None = None,
        latency_mean_ms: float | None = None,
        latency_p50_ms: float | None = None,
        latency_p95_ms: float | None = None,
        frame_drop_rate: float | None = None,
        reconnect_count: int | None = None,
        reconnect_time_ms_p95: float | None = None,
    ) -> None:
        stream = self.payload["stream"]
        latency = stream["latency_ms"]
        if resolution is not None:
            stream["resolution"] = resolution
        if fps_target is not None:
            stream["fps_target"] = float(fps_target)
        if fps_achieved is not None:
            stream["fps_achieved"] = float(fps_achieved)
        if latency_mean_ms is not None:
            latency["mean"] = float(latency_mean_ms)
        if latency_p50_ms is not None:
            latency["p50"] = float(latency_p50_ms)
        if latency_p95_ms is not None:
            latency["p95"] = float(latency_p95_ms)
        if frame_drop_rate is not None:
            stream["frame_drop_rate"] = float(frame_drop_rate)
        if reconnect_count is not None:
            stream["reconnect_count"] = int(reconnect_count)
        if reconnect_time_ms_p95 is not None:
            stream["reconnect_time_ms_p95"] = float(reconnect_time_ms_p95)

    def finalize(
        self,
        success: bool,
        confidence: float = 0.0,
        output_text: str = "",
        result_metrics: dict[str, Any] | None = None,
        failure_type: str = "none",
        failure_note: str = "",
    ) -> None:
        if failure_type not in VALID_FAILURE_TYPES:
            raise ValueError(f"invalid failure type: {failure_type}")
        if not 0.0 <= float(confidence) <= 1.0:
            raise ValueError("confidence must be in [0, 1]")

        elapsed_ms = _to_ms(time.perf_counter() - self._started_at)
        if self.payload["timing_ms"]["end_to_end"] == 0:
            self.payload["timing_ms"]["end_to_end"] = elapsed_ms

        self.payload["result"]["success"] = bool(success)
        self.payload["result"]["confidence"] = float(confidence)
        self.payload["result"]["output_text"] = output_text
        self.payload["result"]["metrics"] = result_metrics or {}

        self.payload["failure"]["failed"] = failure_type != "none"
        self.payload["failure"]["type"] = failure_type
        self.payload["failure"]["note"] = failure_note

    def set_artifacts(
        self,
        frame_paths: list[str] | None = None,
        clip_path: str | None = None,
        stereo_pair_paths: list[str] | None = None,
    ) -> None:
        artifacts = self.payload.setdefault("artifacts", {})
        if frame_paths is not None:
            artifacts["frame_paths"] = frame_paths
        if clip_path is not None:
            artifacts["clip_path"] = clip_path
        if stereo_pair_paths is not None:
            artifacts["stereo_pair_paths"] = stereo_pair_paths

    def to_dict(self) -> dict[str, Any]:
        return self.payload

    def to_json(self) -> str:
        return json.dumps(self.payload, ensure_ascii=False, indent=2)


def create_session(
    *,
    package: str,
    task_type: str,
    query_text: str,
    module_version: str,
    prompt_variant: str | None = None,
    config_hash: str | None = None,
    run_id: str | None = None,
    session_id: str | None = None,
    timestamp_utc: str | None = None,
    device_mode: str = "WIFI",
    network_condition: str = "normal",
    runtime: str = "offline",
    resolution: str = "0x0",
    fps_target: float = 0.0,
) -> SessionRecord:
    if task_type not in VALID_TASK_TYPES:
        raise ValueError(f"invalid task type: {task_type}")
    if device_mode not in VALID_DEVICE_MODES:
        raise ValueError(f"invalid device mode: {device_mode}")
    if network_condition not in VALID_NETWORK_CONDITIONS:
        raise ValueError(f"invalid network condition: {network_condition}")

    payload: dict[str, Any] = {
        "session_id": session_id or _new_session_id(),
        "timestamp": timestamp_utc or _utc_now_iso(),
        "device_mode": device_mode,
        "stream": {
            "resolution": resolution,
            "fps_target": float(fps_target),
            "latency_ms": {"mean": 0.0, "p50": 0.0, "p95": 0.0},
            "frame_drop_rate": 0.0,
            "reconnect_count": 0,
            "reconnect_time_ms_p95": 0.0,
        },
        "sync": {
            "enabled": False,
            "delta_t_ms": {"mean": 0.0, "p95": 0.0},
            "sync_fail_rate": 0.0,
        },
        "task": {
            "type": task_type,
            "query_text": query_text,
            "module_version": module_version,
        },
        "timing_ms": {
            "capture": 0.0,
            "prompt_build": 0.0,
            "inference": 0.0,
            "postprocess": 0.0,
            "render": 0.0,
            "end_to_end": 0.0,
        },
        "result": {"success": False, "confidence": 0.0},
        "failure": {"failed": False, "type": "none", "note": ""},
        "env": {"network_condition": network_condition, "runtime": runtime},
    }
    if prompt_variant is not None:
        payload["task"]["prompt_variant"] = prompt_variant
    if config_hash is not None:
        payload["task"]["config_hash"] = config_hash

    return SessionRecord(
        payload=payload,
        package=package,
        run_id=run_id or _new_session_id(),
        _started_at=time.perf_counter(),
    )
