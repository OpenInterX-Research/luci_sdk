import tempfile
from pathlib import Path
import unittest

from pipeline_ai.audit import run_claim_audit
from pipeline_ai.stats import paired_summary, paired_values
from pipeline_ai.templates import write_csv


class StatsAndAuditTests(unittest.TestCase):
    def test_paired_summary_computes(self):
        rows = [
            {"participant_id": "p1", "task_id": "t1", "condition": "baseline", "completion_time_s": "100"},
            {"participant_id": "p1", "task_id": "t1", "condition": "lucia", "completion_time_s": "80"},
            {"participant_id": "p2", "task_id": "t1", "condition": "baseline", "completion_time_s": "120"},
            {"participant_id": "p2", "task_id": "t1", "condition": "lucia", "completion_time_s": "95"},
        ]
        pairs = paired_values(rows, "completion_time_s", group_by_task=True)
        self.assertEqual(len(pairs), 2)
        summary = paired_summary(pairs)
        self.assertEqual(int(summary["n_pairs"]), 2)
        self.assertLess(summary["median_delta"], 0)  # lucia faster than baseline

    def test_claim_audit_fails_when_claims_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            coverage = Path(tmpdir) / "coverage.csv"
            write_csv(
                coverage,
                [
                    {
                        "claim_id": "C1",
                        "quant_metrics_count": 1,
                        "figure_ids": "Fig A1",
                        "boundary_statement": "Weak Wi-Fi degrades stability.",
                        "status": "complete",
                    }
                ],
                ["claim_id", "quant_metrics_count", "figure_ids", "boundary_statement", "status"],
            )
            result = run_claim_audit(
                coverage_csv=coverage,
                output_root=Path(tmpdir),
                command="unit-test",
            )
            self.assertFalse(result["ok"])
            report_path = Path(result["report_path"])
            self.assertTrue(report_path.exists())


if __name__ == "__main__":
    unittest.main()

