"""CSV template validation and I/O helpers."""

from __future__ import annotations

from pathlib import Path
import csv


PACKAGE_A_COLUMNS = [
    "run_id",
    "workflow_condition",
    "device_mode",
    "network_condition",
    "duration_class",
    "task",
    "success",
    "time_ms",
    "latency_mean_ms",
    "latency_p50_ms",
    "latency_p95_ms",
    "fps_achieved",
    "frame_drop_rate",
    "reconnect_count",
    "reconnect_p95_ms",
    "failure_type",
    "notes",
]

PACKAGE_B_COLUMNS = [
    "participant_id",
    "order_group",
    "condition",
    "task_id",
    "completion_time_s",
    "task_success",
    "error_count",
    "help_requests",
    "loc_or_config_effort",
    "sus_score",
    "nasa_tlx_score",
    "extend_confidence_likert",
    "top_helpful_1",
    "top_helpful_2",
    "top_pain_1",
    "top_pain_2",
    "notes",
]

PACKAGE_C_NAV_COLUMNS = [
    "run_id",
    "prompt_variant",
    "route_length",
    "scene_type",
    "lighting_condition",
    "path_correctness",
    "direction_change_correctness",
    "followability_score",
    "hallucinated_landmark_rate",
    "capture_ms",
    "prompt_build_ms",
    "inference_ms",
    "render_ms",
    "end_to_end_ms",
    "failure_type",
    "notes",
]

PACKAGE_C_MEAS_COLUMNS = [
    "run_id",
    "depth_variant",
    "object_type",
    "material_type",
    "distance_band",
    "lighting_condition",
    "size_mae_mm",
    "relative_error_percent",
    "detection_success",
    "depth_hole_rate",
    "runtime_ms",
    "failure_type",
    "notes",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def validate_columns(path: Path, expected: list[str]) -> list[dict[str, str]]:
    rows = read_csv(path)
    headers = []
    if Path(path).exists():
        with Path(path).open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            headers = list(reader.fieldnames or [])
    missing = [c for c in expected if c not in headers]
    extras = [c for c in headers if c not in expected]
    if missing or extras:
        problems = []
        if missing:
            problems.append(f"missing columns: {', '.join(missing)}")
        if extras:
            problems.append(f"unexpected columns: {', '.join(extras)}")
        raise ValueError(f"template mismatch for {path}: {'; '.join(problems)}")
    return rows

