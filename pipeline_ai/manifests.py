"""Figure/table manifest utilities for reproducibility tracking."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import csv


MANIFEST_COLUMNS = [
    "id",
    "package",
    "output_path",
    "input_files",
    "command",
    "created_utc",
]


@dataclass
class ManifestWriter:
    output_root: Path

    def __post_init__(self) -> None:
        self.output_root = Path(self.output_root).resolve()
        (self.output_root / "figures").mkdir(parents=True, exist_ok=True)
        (self.output_root / "tables").mkdir(parents=True, exist_ok=True)

    def add_figure(
        self,
        *,
        figure_id: str,
        package: str,
        output_path: Path,
        input_files: list[Path],
        command: str,
    ) -> None:
        self._upsert(
            self.output_root / "figures" / "figure_manifest.csv",
            {
                "id": figure_id,
                "package": package,
                "output_path": str(Path(output_path).resolve()),
                "input_files": ";".join(str(Path(p).resolve()) for p in input_files),
                "command": command,
                "created_utc": datetime.now(timezone.utc).isoformat(),
            },
        )

    def add_table(
        self,
        *,
        table_id: str,
        package: str,
        output_path: Path,
        input_files: list[Path],
        command: str,
    ) -> None:
        self._upsert(
            self.output_root / "tables" / "table_manifest.csv",
            {
                "id": table_id,
                "package": package,
                "output_path": str(Path(output_path).resolve()),
                "input_files": ";".join(str(Path(p).resolve()) for p in input_files),
                "command": command,
                "created_utc": datetime.now(timezone.utc).isoformat(),
            },
        )

    def _upsert(self, path: Path, row: dict[str, str]) -> None:
        existing: list[dict[str, str]] = []
        if path.exists():
            with path.open("r", encoding="utf-8", newline="") as fh:
                existing = list(csv.DictReader(fh))

        updated = [r for r in existing if r.get("id") != row["id"]]
        updated.append(row)
        updated.sort(key=lambda item: item["id"])

        with path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=MANIFEST_COLUMNS)
            writer.writeheader()
            writer.writerows(updated)

