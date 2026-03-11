"""Fixed-path video QA runner for pipeline_ai."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import uuid

from .logger import SessionLogger, resolve_repo_root
from .session import create_session


DEFAULT_TASK = "corridor_navigation"
DEFAULT_MODEL_PRESET = "qwen"
DEFAULT_FALLBACK_MODEL = "Qwen/Qwen2-VL-2B-Instruct"
VIDEO_GLOBS = ("*.mp4", "*.MP4", "*.mov", "*.MOV")
MODEL_PRESETS = {
    "qwen": DEFAULT_FALLBACK_MODEL,
    "st-r1": "navigation_task/models/ST-R1-mcq",
}


@dataclass(frozen=True)
class TaskPaths:
    task_name: str
    task_dir: Path
    questions_file: Path
    videos_dir: Path
    results_dir: Path


def resolve_task_paths(
    repo_root: Path,
    task_name: str,
    *,
    results_dir_override: Path | None = None,
) -> TaskPaths:
    task_dir = Path(repo_root) / "navigation_task" / "tasks" / task_name
    if not task_dir.exists():
        raise FileNotFoundError(f"task directory not found: {task_dir}")

    questions_file = task_dir / f"{task_name}_questions.json"
    if not questions_file.exists():
        raise FileNotFoundError(f"questions file not found: {questions_file}")

    videos_dir = task_dir / "videos"
    if not videos_dir.exists():
        raise FileNotFoundError(f"videos directory not found: {videos_dir}")

    results_dir = Path(results_dir_override) if results_dir_override else task_dir / "results"
    return TaskPaths(
        task_name=task_name,
        task_dir=task_dir,
        questions_file=questions_file,
        videos_dir=videos_dir,
        results_dir=results_dir,
    )


def resolve_model_target(repo_root: Path, model_preset: str) -> str:
    try:
        target = MODEL_PRESETS[model_preset]
    except KeyError as exc:
        allowed = ", ".join(sorted(MODEL_PRESETS))
        raise ValueError(f"unknown model preset: {model_preset} (allowed: {allowed})") from exc

    if model_preset == "st-r1":
        local_path = Path(repo_root) / target
        if not local_path.exists():
            raise FileNotFoundError(f"local ST-R1 model not found: {local_path}")
        return str(local_path)
    return target


def discover_videos(videos_dir: Path, video_name: str | None = None) -> list[Path]:
    videos: list[Path] = []
    for pattern in VIDEO_GLOBS:
        videos.extend(sorted(videos_dir.glob(pattern)))

    unique_videos = sorted({video.resolve() for video in videos})
    if video_name is None:
        return unique_videos

    selected = [
        video
        for video in unique_videos
        if video.name == video_name or video.stem == video_name
    ]
    if not selected:
        raise FileNotFoundError(f"video not found in {videos_dir}: {video_name}")
    return selected


def _load_question_config(questions_file: Path) -> dict[str, object]:
    return json.loads(questions_file.read_text(encoding="utf-8"))


def _config_hash(task_name: str, video_ref: str, model_preset: str, model_target: str) -> str:
    payload = {
        "task_name": task_name,
        "video_ref": video_ref,
        "model_preset": model_preset,
        "model_target": model_target,
    }
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _run_universal_analysis(
    *,
    repo_root: Path,
    python_cmd: str,
    questions_file: Path,
    video_file: Path,
    model_target: str,
    fallback_model: str,
) -> dict[str, object]:
    src_dir = repo_root / "navigation_task" / "src"
    command = [
        python_cmd,
        "universal_analysis.py",
        str(questions_file),
        str(video_file),
        model_target,
        fallback_model,
    ]
    proc = subprocess.run(
        command,
        cwd=src_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return json.loads(proc.stdout)


def _build_dry_run_result(
    *,
    task_name: str,
    video_ref: str,
    questions: list[dict[str, object]],
    model_preset: str,
    model_target: str,
) -> dict[str, object]:
    results: list[dict[str, object]] = []
    for question in questions:
        options = question.get("options")
        row: dict[str, object] = {
            "question_id": question.get("id"),
            "category": question.get("category", "general"),
            "question": question.get("question", ""),
        }
        if options:
            answer = "A"
            row["options"] = options
            row["answer"] = answer
            row["selected_option"] = options[0]
        else:
            row["answer"] = "dry-run answer"
        results.append(row)

    total_questions = len(questions)
    return {
        "task": task_name,
        "video": video_ref,
        "model_preset": model_preset,
        "model_target": model_target,
        "dry_run": True,
        "total_questions": total_questions,
        "successful_answers": total_questions,
        "results": results,
    }


def _result_filename(task_name: str, video_name: str) -> str:
    return f"{task_name}_{video_name}_result.json"


def _summary_payload(
    *,
    task_name: str,
    model_preset: str,
    model_target: str,
    run_rows: list[dict[str, object]],
) -> dict[str, object]:
    total_videos = len(run_rows)
    successful_videos = sum(1 for row in run_rows if bool(row["success"]))
    return {
        "task_name": task_name,
        "model_preset": model_preset,
        "model_target": model_target,
        "completion_time": datetime.now(timezone.utc).isoformat(),
        "total_videos": total_videos,
        "successful_videos": successful_videos,
        "failed_videos": total_videos - successful_videos,
        "success_rate": f"{(successful_videos * 100 // total_videos) if total_videos else 0}%",
        "runs": run_rows,
    }


def run_video_qa(
    *,
    task_name: str = DEFAULT_TASK,
    video_name: str | None = None,
    model_preset: str = DEFAULT_MODEL_PRESET,
    dry_run: bool = False,
    python_cmd: str = sys.executable,
    repo_root: Path | None = None,
    results_dir_override: Path | None = None,
    session_data_root: Path | None = None,
) -> dict[str, object]:
    repo_root = (repo_root or resolve_repo_root()).resolve()
    task_paths = resolve_task_paths(repo_root, task_name, results_dir_override=results_dir_override)
    task_paths.results_dir.mkdir(parents=True, exist_ok=True)

    config = _load_question_config(task_paths.questions_file)
    questions = list(config.get("questions", []))
    model_target = resolve_model_target(repo_root, model_preset)
    fallback_model = DEFAULT_FALLBACK_MODEL
    videos = discover_videos(task_paths.videos_dir, video_name=video_name)

    if dry_run and not videos:
        video_refs: list[str | Path] = ["dry_run"]
    elif videos:
        video_refs = videos
    else:
        raise FileNotFoundError(f"no videos found in: {task_paths.videos_dir}")

    logger = SessionLogger(repo_root=repo_root, data_root=session_data_root)
    run_rows: list[dict[str, object]] = []
    result_files: list[str] = []
    session_logs: list[str] = []

    for video_ref in video_refs:
        video_label = video_ref if isinstance(video_ref, str) else video_ref.stem
        run_id = f"vqa_{task_name}_{uuid.uuid4().hex[:10]}"
        session = create_session(
            package="package_c",
            task_type="video_qa",
            query_text=str(config.get("task_info", {}).get("description", task_name)),
            module_version="navigation_task",
            config_hash=_config_hash(task_name, str(video_ref), model_preset, model_target),
            run_id=run_id,
            device_mode="WIFI",
            network_condition="normal",
            runtime="offline",
        )

        session.set_artifacts(
            clip_path=str(video_ref) if isinstance(video_ref, Path) else str(task_paths.videos_dir / "__dry_run__")
        )

        failure_type = "none"
        failure_note = ""
        if dry_run:
            result = _build_dry_run_result(
                task_name=task_name,
                video_ref=str(video_ref),
                questions=questions,
                model_preset=model_preset,
                model_target=model_target,
            )
        else:
            try:
                assert isinstance(video_ref, Path)
                result = _run_universal_analysis(
                    repo_root=repo_root,
                    python_cmd=python_cmd,
                    questions_file=task_paths.questions_file,
                    video_file=video_ref,
                    model_target=model_target,
                    fallback_model=fallback_model,
                )
                result["model_preset"] = model_preset
                result["model_target"] = model_target
            except Exception as exc:
                failure_type = "other"
                failure_note = str(exc)
                result = {
                    "task": task_name,
                    "video": str(video_ref),
                    "model_preset": model_preset,
                    "model_target": model_target,
                    "total_questions": len(questions),
                    "successful_answers": 0,
                    "results": [],
                    "error": str(exc),
                }

        result_path = task_paths.results_dir / _result_filename(task_name, str(video_label))
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

        total_questions = int(result.get("total_questions", 0))
        successful_answers = int(result.get("successful_answers", 0))
        success = failure_type == "none"
        confidence = (
            round(successful_answers / total_questions, 3)
            if success and total_questions > 0
            else 0.0
        )
        metrics = {
            "task_name": task_name,
            "model_preset": model_preset,
            "model_target": model_target,
            "total_questions": total_questions,
            "successful_answers": successful_answers,
            "result_path": str(result_path.resolve()),
        }
        session.finalize(
            success=success,
            confidence=confidence,
            output_text=f"result_json={result_path.resolve()}",
            result_metrics=metrics,
            failure_type=failure_type,
            failure_note=failure_note,
        )
        log_path = logger.save(session, validate=True)

        result_files.append(str(result_path.resolve()))
        session_logs.append(str(log_path.resolve()))
        run_rows.append(
            {
                "run_id": run_id,
                "video": str(video_ref),
                "result_file": str(result_path.resolve()),
                "session_log": str(log_path.resolve()),
                "success": success,
                "total_questions": total_questions,
                "successful_answers": successful_answers,
            }
        )

    summary_path = task_paths.results_dir / f"{task_name}_summary.json"
    summary = _summary_payload(
        task_name=task_name,
        model_preset=model_preset,
        model_target=model_target,
        run_rows=run_rows,
    )
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "task": task_name,
        "model_preset": model_preset,
        "model_target": model_target,
        "results_dir": str(task_paths.results_dir.resolve()),
        "summary_file": str(summary_path.resolve()),
        "result_files": result_files,
        "session_logs": session_logs,
    }
