"""Developer productivity (Package B) paired analysis."""

from __future__ import annotations

import os
from pathlib import Path
import statistics
import tempfile

from .manifests import ManifestWriter
from .stats import paired_summary, paired_values
from .templates import PACKAGE_B_COLUMNS, validate_columns, write_csv


OBJECTIVE_METRICS = [
    ("completion_time_s", True),
    ("task_success", True),
    ("error_count", True),
    ("help_requests", True),
    ("loc_or_config_effort", True),
]

SUBJECTIVE_METRICS = [
    ("sus_score", False),
    ("nasa_tlx_score", False),
    ("extend_confidence_likert", False),
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


def analyze_package_b(
    *,
    input_csv: Path,
    output_root: Path,
    command: str,
    manifest: ManifestWriter,
) -> dict[str, Path]:
    rows = validate_columns(input_csv, PACKAGE_B_COLUMNS)
    output_root = Path(output_root)

    raw_out = output_root / "data" / "raw" / "package_b" / "package_b_participants.csv"
    raw_out.parent.mkdir(parents=True, exist_ok=True)
    raw_out.write_text(Path(input_csv).read_text(encoding="utf-8"), encoding="utf-8")

    cleaned_path = output_root / "data" / "processed" / "package_b_cleaned.csv"
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_path.write_text(Path(input_csv).read_text(encoding="utf-8"), encoding="utf-8")

    summary_rows: list[dict[str, object]] = []
    for metric, group_by_task in OBJECTIVE_METRICS + SUBJECTIVE_METRICS:
        pairs = paired_values(rows, metric, group_by_task=group_by_task)
        summary = paired_summary(pairs)
        summary_rows.append(
            {
                "metric": metric,
                "n_pairs": int(summary["n_pairs"]),
                "median_baseline": summary["median_baseline"],
                "median_lucia": summary["median_lucia"],
                "median_delta_lucia_minus_baseline": summary["median_delta"],
                "ci_low": summary["ci_low"],
                "ci_high": summary["ci_high"],
                "wilcoxon_w": summary["w_stat"],
                "approx_p_value": summary["p_value"],
                "rank_biserial": summary["rank_biserial"],
            }
        )

    table_path = output_root / "tables" / "b1_paired_stats.csv"
    write_csv(
        table_path,
        summary_rows,
        [
            "metric",
            "n_pairs",
            "median_baseline",
            "median_lucia",
            "median_delta_lucia_minus_baseline",
            "ci_low",
            "ci_high",
            "wilcoxon_w",
            "approx_p_value",
            "rank_biserial",
        ],
    )

    objective_rows = [r for r in summary_rows if r["metric"] in {m for m, _ in OBJECTIVE_METRICS}]
    subjective_rows = [r for r in summary_rows if r["metric"] in {m for m, _ in SUBJECTIVE_METRICS}]

    plt = _require_matplotlib()
    figure_path = output_root / "figures" / "b1_developer_productivity.png"
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    obj_labels = [str(r["metric"]) for r in objective_rows]
    obj_vals = [float(r["median_delta_lucia_minus_baseline"]) for r in objective_rows]
    axes[0].bar(obj_labels, obj_vals)
    axes[0].set_title("Objective median deltas")
    axes[0].tick_params(axis="x", rotation=45)

    sub_labels = [str(r["metric"]) for r in subjective_rows]
    sub_vals = [float(r["median_delta_lucia_minus_baseline"]) for r in subjective_rows]
    axes[1].bar(sub_labels, sub_vals)
    axes[1].set_title("Subjective median deltas")
    axes[1].tick_params(axis="x", rotation=45)

    fig.tight_layout()
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(figure_path)
    plt.close(fig)

    # Lightweight qualitative theme extraction for the debrief fields.
    helpful = [row.get("top_helpful_1", "").strip() for row in rows if row.get("top_helpful_1", "").strip()]
    pains = [row.get("top_pain_1", "").strip() for row in rows if row.get("top_pain_1", "").strip()]
    qual_path = output_root / "tables" / "b1_qualitative_themes.csv"
    write_csv(
        qual_path,
        [
            {
                "theme_type": "helpful",
                "example_count": len(helpful),
                "example_median_length": statistics.median([len(h) for h in helpful]) if helpful else 0,
            },
            {
                "theme_type": "pain",
                "example_count": len(pains),
                "example_median_length": statistics.median([len(p) for p in pains]) if pains else 0,
            },
        ],
        ["theme_type", "example_count", "example_median_length"],
    )

    manifest.add_table(
        table_id="Tab B1",
        package="package_b",
        output_path=table_path,
        input_files=[input_csv],
        command=command,
    )
    manifest.add_figure(
        figure_id="Fig B1",
        package="package_b",
        output_path=figure_path,
        input_files=[input_csv],
        command=command,
    )
    return {
        "raw_csv": raw_out,
        "cleaned_csv": cleaned_path,
        "summary_table": table_path,
        "qual_table": qual_path,
        "figure": figure_path,
    }
