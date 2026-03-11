"""Template ingestion and summary generation for package A/C2."""

from __future__ import annotations

from collections import defaultdict
import os
from pathlib import Path
import statistics
import tempfile

from .manifests import ManifestWriter
from .templates import (
    PACKAGE_A_COLUMNS,
    PACKAGE_C_MEAS_COLUMNS,
    validate_columns,
    write_csv,
)
from .stats import to_float


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = int(round((len(ordered) - 1) * 0.95))
    return float(ordered[idx])


def _mean(values: list[float]) -> float:
    return float(statistics.mean(values)) if values else 0.0


def _safe_num(row: dict[str, str], key: str) -> float:
    val = to_float(row.get(key))
    return float(val) if val is not None else 0.0


def _safe_success(row: dict[str, str]) -> float:
    return 1.0 if _safe_num(row, "success") >= 0.5 else 0.0


def _require_matplotlib():
    tmp = Path(tempfile.gettempdir())
    os.environ.setdefault("MPLCONFIGDIR", str(tmp / "matplotlib"))
    os.environ.setdefault("XDG_CACHE_HOME", str(tmp))
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except Exception as exc:
        raise RuntimeError("matplotlib is required for figure generation") from exc
    return plt


def ingest_package_a(
    *,
    input_csv: Path,
    output_root: Path,
    command: str,
    manifest: ManifestWriter,
) -> dict[str, Path]:
    rows = validate_columns(input_csv, PACKAGE_A_COLUMNS)
    output_root = Path(output_root)

    raw_out = output_root / "data" / "raw" / "package_a" / "package_a_runs.csv"
    raw_out.parent.mkdir(parents=True, exist_ok=True)
    raw_out.write_text(Path(input_csv).read_text(encoding="utf-8"), encoding="utf-8")

    grouped: dict[tuple[str, str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (
            row["workflow_condition"],
            row["device_mode"],
            row["network_condition"],
            row["duration_class"],
            row["task"],
        )
        grouped[key].append(row)

    summary_rows: list[dict[str, object]] = []
    for key, samples in grouped.items():
        times = [_safe_num(r, "time_ms") for r in samples]
        lat_p95 = [_safe_num(r, "latency_p95_ms") for r in samples]
        fps_vals = [_safe_num(r, "fps_achieved") for r in samples]
        drops = [_safe_num(r, "frame_drop_rate") for r in samples]
        reconnects = [_safe_num(r, "reconnect_count") for r in samples]
        success = [_safe_success(r) for r in samples]
        summary_rows.append(
            {
                "workflow_condition": key[0],
                "device_mode": key[1],
                "network_condition": key[2],
                "duration_class": key[3],
                "task": key[4],
                "n_runs": len(samples),
                "success_rate": _mean(success),
                "time_ms_mean": _mean(times),
                "time_ms_p95": _p95(times),
                "latency_p95_ms_mean": _mean(lat_p95),
                "fps_achieved_mean": _mean(fps_vals),
                "frame_drop_rate_mean": _mean(drops),
                "reconnect_count_mean": _mean(reconnects),
            }
        )

    table_path = output_root / "tables" / "a1_platform_metrics.csv"
    write_csv(
        table_path,
        summary_rows,
        [
            "workflow_condition",
            "device_mode",
            "network_condition",
            "duration_class",
            "task",
            "n_runs",
            "success_rate",
            "time_ms_mean",
            "time_ms_p95",
            "latency_p95_ms_mean",
            "fps_achieved_mean",
            "frame_drop_rate_mean",
            "reconnect_count_mean",
        ],
    )

    figure_path = output_root / "figures" / "a2_latency_distribution.png"
    plt = _require_matplotlib()
    labels = [
        f"{r['workflow_condition']}|{r['device_mode']}|{r['network_condition']}|{r['task']}"
        for r in summary_rows
    ]
    vals = [float(r["time_ms_p95"]) for r in summary_rows]
    plt.figure(figsize=(12, 5))
    plt.bar(range(len(vals)), vals)
    plt.xticks(range(len(vals)), labels, rotation=75, fontsize=7)
    plt.ylabel("time_ms_p95")
    plt.tight_layout()
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(figure_path)
    plt.close()

    manifest.add_table(
        table_id="Tab A1",
        package="package_a",
        output_path=table_path,
        input_files=[input_csv],
        command=command,
    )
    manifest.add_figure(
        figure_id="Fig A2",
        package="package_a",
        output_path=figure_path,
        input_files=[input_csv],
        command=command,
    )
    return {"raw_csv": raw_out, "summary_table": table_path, "figure": figure_path}


def ingest_package_c2(
    *,
    input_csv: Path,
    output_root: Path,
    command: str,
    manifest: ManifestWriter,
) -> dict[str, Path]:
    rows = validate_columns(input_csv, PACKAGE_C_MEAS_COLUMNS)
    output_root = Path(output_root)

    raw_out = output_root / "data" / "raw" / "package_c" / "package_c_measurement.csv"
    raw_out.parent.mkdir(parents=True, exist_ok=True)
    raw_out.write_text(Path(input_csv).read_text(encoding="utf-8"), encoding="utf-8")

    grouped: dict[tuple[str, str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (
            row["depth_variant"],
            row["object_type"],
            row["material_type"],
            row["distance_band"],
            row["lighting_condition"],
        )
        grouped[key].append(row)

    summary_rows: list[dict[str, object]] = []
    for key, samples in grouped.items():
        mae = [_safe_num(r, "size_mae_mm") for r in samples]
        rel_err = [_safe_num(r, "relative_error_percent") for r in samples]
        success = [_safe_num(r, "detection_success") for r in samples]
        holes = [_safe_num(r, "depth_hole_rate") for r in samples]
        runtime = [_safe_num(r, "runtime_ms") for r in samples]
        summary_rows.append(
            {
                "depth_variant": key[0],
                "object_type": key[1],
                "material_type": key[2],
                "distance_band": key[3],
                "lighting_condition": key[4],
                "n_runs": len(samples),
                "size_mae_mm_mean": _mean(mae),
                "relative_error_percent_mean": _mean(rel_err),
                "detection_success_rate": _mean(success),
                "depth_hole_rate_mean": _mean(holes),
                "runtime_ms_mean": _mean(runtime),
            }
        )

    table_path = output_root / "tables" / "c2_measurement_metrics.csv"
    write_csv(
        table_path,
        summary_rows,
        [
            "depth_variant",
            "object_type",
            "material_type",
            "distance_band",
            "lighting_condition",
            "n_runs",
            "size_mae_mm_mean",
            "relative_error_percent_mean",
            "detection_success_rate",
            "depth_hole_rate_mean",
            "runtime_ms_mean",
        ],
    )

    plt = _require_matplotlib()
    variants = sorted({str(r["depth_variant"]) for r in summary_rows})
    mae_vals = []
    for variant in variants:
        vals = [float(r["size_mae_mm_mean"]) for r in summary_rows if r["depth_variant"] == variant]
        mae_vals.append(_mean(vals))

    figure_path = output_root / "figures" / "c2_measurement_ablation.png"
    plt.figure(figsize=(8, 4))
    plt.bar(variants, mae_vals)
    plt.ylabel("size_mae_mm_mean")
    plt.xlabel("depth_variant")
    plt.tight_layout()
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(figure_path)
    plt.close()

    manifest.add_table(
        table_id="Tab C2",
        package="package_c",
        output_path=table_path,
        input_files=[input_csv],
        command=command,
    )
    manifest.add_figure(
        figure_id="Fig C2",
        package="package_c",
        output_path=figure_path,
        input_files=[input_csv],
        command=command,
    )
    return {"raw_csv": raw_out, "summary_table": table_path, "figure": figure_path}
