"""Navigation ablation runner (Package C1)."""

from __future__ import annotations

from collections import defaultdict
import csv
import hashlib
import json
import os
from pathlib import Path
import random
import statistics
import subprocess
import sys
import tempfile
import time
import uuid

from .logger import SessionLogger, resolve_repo_root
from .manifests import ManifestWriter
from .session import create_session
from .templates import PACKAGE_C_NAV_COLUMNS, write_csv


REQUIRED_METADATA_COLUMNS = [
    "video_file",
    "route_length",
    "scene_type",
    "lighting_condition",
]

LABEL_COLUMNS = [
    "run_id",
    "path_correctness",
    "direction_change_correctness",
    "followability_score",
    "hallucinated_landmark_rate",
    "failure_type",
    "notes",
]


def _require_matplotlib():
    tmp = Path(tempfile.gettempdir())
    os.environ.setdefault("MPLCONFIGDIR", str(tmp / "matplotlib"))
    os.environ.setdefault("XDG_CACHE_HOME", str(tmp))
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except Exception as exc:
        raise RuntimeError("matplotlib is required for figure generation") from exc
    return plt


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _ensure_columns(path: Path, required: list[str]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        headers = list(reader.fieldnames or [])
        missing = [c for c in required if c not in headers]
        if missing:
            raise ValueError(f"{path} missing columns: {', '.join(missing)}")
    return _read_csv(path)


def _config_hash(metadata_row: dict[str, str], variant: str, model_path: str) -> str:
    raw = json.dumps({"meta": metadata_row, "variant": variant, "model_path": model_path}, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _run_universal_analysis(
    *,
    repo_root: Path,
    python_cmd: str,
    questions_file: Path,
    video_file: Path,
    model_path: str,
    fallback_model: str,
    timeout_s: int,
) -> dict[str, object]:
    src_dir = repo_root / "navigation_task" / "src"
    command = [
        python_cmd,
        "universal_analysis.py",
        str(questions_file),
        str(video_file),
        model_path,
        fallback_model,
    ]
    proc = subprocess.run(
        command,
        cwd=src_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout_s,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return json.loads(proc.stdout)


def run_navigation_ablation(
    *,
    questions_file: Path,
    metadata_csv: Path,
    model_path: str,
    fallback_model: str,
    output_root: Path,
    prompt_variants: list[str],
    dry_run: bool,
    timeout_s: int,
    python_cmd: str,
    labels_csv: Path | None,
    command: str,
) -> dict[str, Path]:
    repo_root = resolve_repo_root()
    output_root = Path(output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    metadata_rows = _ensure_columns(metadata_csv, REQUIRED_METADATA_COLUMNS)
    labels_map: dict[str, dict[str, str]] = {}
    if labels_csv:
        for row in _ensure_columns(labels_csv, LABEL_COLUMNS):
            labels_map[row["run_id"]] = row

    logger = SessionLogger(repo_root=repo_root, data_root=output_root / "data" / "raw")
    manifest = ManifestWriter(output_root=output_root)
    rng = random.Random(42)

    run_rows: list[dict[str, object]] = []
    for row in metadata_rows:
        video_path = Path(row["video_file"])
        if not video_path.is_absolute():
            video_path = (metadata_csv.parent / video_path).resolve()
        if not video_path.exists() and not dry_run:
            raise FileNotFoundError(f"video file not found: {video_path}")

        for variant in prompt_variants:
            run_id = f"c1_{variant}_{uuid.uuid4().hex[:10]}"
            session = create_session(
                package="package_c",
                task_type="navigation",
                query_text=row.get("query_text") or "navigation ablation query",
                module_version=row.get("module_version") or "navigation_task",
                prompt_variant=variant,
                config_hash=_config_hash(row, variant, model_path),
                run_id=run_id,
                device_mode=(row.get("device_mode") or "WIFI").upper(),
                network_condition=row.get("network_condition") or "normal",
                runtime="offline",
            )

            t0 = time.perf_counter()
            run_failure = "none"
            run_notes = ""
            metrics: dict[str, object]
            if dry_run:
                total_q = rng.randint(8, 12)
                ok_q = rng.randint(max(1, total_q - 3), total_q)
                metrics = {"total_questions": total_q, "successful_answers": ok_q, "dry_run": True}
                time.sleep(0.001)
            else:
                try:
                    result = _run_universal_analysis(
                        repo_root=repo_root,
                        python_cmd=python_cmd,
                        questions_file=questions_file,
                        video_file=video_path,
                        model_path=model_path,
                        fallback_model=fallback_model,
                        timeout_s=timeout_s,
                    )
                    metrics = {
                        "total_questions": result.get("total_questions", 0),
                        "successful_answers": result.get("successful_answers", 0),
                    }
                except Exception as exc:
                    run_failure = "other"
                    run_notes = f"inference failed: {exc}"
                    metrics = {"total_questions": 0, "successful_answers": 0}

            end_to_end_ms = round((time.perf_counter() - t0) * 1000.0, 3)
            session.set_timing(inference_ms=end_to_end_ms, end_to_end_ms=end_to_end_ms)
            success = run_failure == "none"
            confidence = 0.75 if success else 0.0
            session.finalize(
                success=success,
                confidence=confidence,
                output_text="dry-run result" if dry_run else "",
                result_metrics=metrics,
                failure_type=run_failure,
                failure_note=run_notes,
            )
            session_log_path = logger.save(session, validate=True)

            row_out: dict[str, object] = {
                "run_id": run_id,
                "prompt_variant": variant,
                "route_length": row["route_length"],
                "scene_type": row["scene_type"],
                "lighting_condition": row["lighting_condition"],
                "path_correctness": "",
                "direction_change_correctness": "",
                "followability_score": "",
                "hallucinated_landmark_rate": "",
                "capture_ms": 0.0,
                "prompt_build_ms": 0.0,
                "inference_ms": end_to_end_ms,
                "render_ms": 0.0,
                "end_to_end_ms": end_to_end_ms,
                "failure_type": run_failure,
                "notes": run_notes,
            }
            if run_id in labels_map:
                labels = labels_map[run_id]
                for key in [
                    "path_correctness",
                    "direction_change_correctness",
                    "followability_score",
                    "hallucinated_landmark_rate",
                    "failure_type",
                    "notes",
                ]:
                    if labels.get(key, "") != "":
                        row_out[key] = labels[key]
            row_out["notes"] = f"{row_out['notes']} session_log={session_log_path}".strip()
            run_rows.append(row_out)

    raw_table = output_root / "data" / "raw" / "package_c" / "package_c_navigation.csv"
    write_csv(raw_table, run_rows, PACKAGE_C_NAV_COLUMNS)

    grouped: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in run_rows:
        grouped[(str(row["prompt_variant"]), str(row["route_length"]), str(row["scene_type"]))].append(row)

    summary_rows: list[dict[str, object]] = []
    for key, rows in grouped.items():
        path_correctness = [_as_float(r.get("path_correctness")) for r in rows]
        followability = [_as_float(r.get("followability_score")) for r in rows]
        hallucination = [_as_float(r.get("hallucinated_landmark_rate")) for r in rows]
        latency = [_as_float(r.get("end_to_end_ms")) for r in rows]
        summary_rows.append(
            {
                "prompt_variant": key[0],
                "route_length": key[1],
                "scene_type": key[2],
                "n_runs": len(rows),
                "path_correctness_mean": _mean_no_na(path_correctness),
                "followability_mean": _mean_no_na(followability),
                "hallucinated_landmark_rate_mean": _mean_no_na(hallucination),
                "end_to_end_ms_mean": _mean_no_na(latency),
            }
        )

    summary_table = output_root / "tables" / "c1_navigation_metrics.csv"
    write_csv(
        summary_table,
        summary_rows,
        [
            "prompt_variant",
            "route_length",
            "scene_type",
            "n_runs",
            "path_correctness_mean",
            "followability_mean",
            "hallucinated_landmark_rate_mean",
            "end_to_end_ms_mean",
        ],
    )

    plt = _require_matplotlib()
    variants = sorted({str(r["prompt_variant"]) for r in summary_rows})
    mean_correctness = []
    for variant in variants:
        vals = [float(r["path_correctness_mean"]) for r in summary_rows if r["prompt_variant"] == variant]
        vals = [v for v in vals if v == v]
        mean_correctness.append(statistics.mean(vals) if vals else 0.0)
    figure = output_root / "figures" / "c1_navigation_ablation.png"
    plt.figure(figsize=(8, 4))
    plt.bar(variants, mean_correctness)
    plt.ylabel("path_correctness_mean")
    plt.xlabel("prompt_variant")
    plt.tight_layout()
    figure.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(figure)
    plt.close()

    manifest.add_table(
        table_id="Tab C1",
        package="package_c",
        output_path=summary_table,
        input_files=[metadata_csv, raw_table, *( [labels_csv] if labels_csv else [])],
        command=command,
    )
    manifest.add_figure(
        figure_id="Fig C1",
        package="package_c",
        output_path=figure,
        input_files=[summary_table],
        command=command,
    )
    return {"raw_table": raw_table, "summary_table": summary_table, "figure": figure}


def _as_float(value: object) -> float:
    text = str(value).strip()
    if text == "":
        return float("nan")
    try:
        return float(text)
    except Exception:
        return float("nan")


def _mean_no_na(values: list[float]) -> float:
    filt = [v for v in values if v == v]
    return statistics.mean(filt) if filt else float("nan")
