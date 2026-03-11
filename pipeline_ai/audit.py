"""Claim coverage audit for C1/C2/C3 readiness."""

from __future__ import annotations

from pathlib import Path
import csv

from .templates import write_csv


REQUIRED_CLAIMS = ["C1", "C2", "C3"]


def run_claim_audit(
    *,
    coverage_csv: Path,
    output_root: Path,
    command: str,
    claim_matrix_path: Path | None = None,
) -> dict[str, object]:
    rows = _read_csv(Path(coverage_csv))
    indexed = {row.get("claim_id", "").strip(): row for row in rows}

    report_rows: list[dict[str, object]] = []
    has_failures = False
    for claim_id in REQUIRED_CLAIMS:
        row = indexed.get(claim_id)
        if row is None:
            has_failures = True
            report_rows.append(
                {
                    "claim_id": claim_id,
                    "check": "presence",
                    "passed": False,
                    "detail": "missing claim row in coverage file",
                }
            )
            continue

        quant = _to_int(row.get("quant_metrics_count", "0"))
        figs = (row.get("figure_ids", "") or "").strip()
        boundary = (row.get("boundary_statement", "") or "").strip()
        status = (row.get("status", "") or "").strip().lower()

        checks = [
            ("quant_metrics_count > 0", quant > 0, f"value={quant}"),
            ("figure_ids non-empty", figs != "", f"value={figs!r}"),
            ("boundary_statement non-empty", boundary != "", f"value={boundary!r}"),
            ("status not planned", status not in {"planned", ""}, f"value={status!r}"),
        ]
        for check_name, passed, detail in checks:
            has_failures = has_failures or (not passed)
            report_rows.append(
                {
                    "claim_id": claim_id,
                    "check": check_name,
                    "passed": passed,
                    "detail": detail,
                }
            )

    if claim_matrix_path and claim_matrix_path.exists():
        report_rows.append(
            {
                "claim_id": "ALL",
                "check": "claim_matrix_reference",
                "passed": True,
                "detail": f"source={claim_matrix_path}",
            }
        )

    output_table = Path(output_root) / "tables" / "claim_audit_report.csv"
    write_csv(output_table, report_rows, ["claim_id", "check", "passed", "detail"])
    return {"ok": not has_failures, "report_path": output_table, "command": command}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _to_int(value: str) -> int:
    try:
        return int(float(value))
    except Exception:
        return 0

