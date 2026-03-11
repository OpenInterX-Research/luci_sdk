"""Session log writer with schema validation hook."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
from typing import Iterable

from .session import SessionRecord


def resolve_repo_root(start: Path | None = None) -> Path:
    probe = (start or Path(__file__).resolve()).parent
    for path in [probe, *probe.parents]:
        if (path / ".git").exists() and (path / "paper").exists():
            return path
    raise RuntimeError("failed to locate repo root (expected .git and paper/)")


@dataclass
class SessionLogger:
    """Persist session logs under the reproducibility data layout."""

    repo_root: Path | None = None
    data_root: Path | None = None
    validator_script: Path | None = None

    def __post_init__(self) -> None:
        self.repo_root = self.repo_root or resolve_repo_root()
        self.data_root = self.data_root or (self.repo_root / "data" / "raw")
        self.validator_script = self.validator_script or (
            self.repo_root / "paper" / "uist_upgrade" / "scripts" / "validate_session_log.py"
        )

    def session_dir(self, package: str, run_id: str) -> Path:
        path = self.data_root / package / run_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def save(
        self,
        record: SessionRecord,
        *,
        extra_artifacts: Iterable[str] | None = None,
        validate: bool = True,
    ) -> Path:
        run_dir = self.session_dir(record.package, record.run_id)
        log_path = run_dir / "session_log.json"

        payload = record.to_dict()
        if extra_artifacts:
            artifacts = payload.setdefault("artifacts", {})
            artifact_paths = artifacts.setdefault("frame_paths", [])
            artifact_paths.extend(list(extra_artifacts))
        payload.setdefault("metadata", {})
        payload["metadata"]["package"] = record.package
        payload["metadata"]["run_id"] = record.run_id
        payload["metadata"]["saved_at_utc"] = datetime.now(timezone.utc).isoformat()

        log_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        if validate:
            self._validate_log(log_path)
        return log_path

    def _validate_log(self, log_path: Path) -> None:
        if not self.validator_script or not self.validator_script.exists():
            raise RuntimeError(f"validator script not found: {self.validator_script}")
        proc = subprocess.run(
            [sys.executable, str(self.validator_script), str(log_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                "session log failed schema validation:\n"
                f"stdout:\n{proc.stdout}\n"
                f"stderr:\n{proc.stderr}"
            )

