import tempfile
from pathlib import Path
import unittest

from pipeline_ai.logger import SessionLogger, resolve_repo_root
from pipeline_ai.session import create_session
from pipeline_ai.templates import validate_columns, PACKAGE_A_COLUMNS, write_csv


class SessionAndTemplateTests(unittest.TestCase):
    def test_session_log_saves_and_validates(self):
        repo_root = resolve_repo_root()
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = SessionLogger(repo_root=repo_root, data_root=Path(tmpdir))
            session = create_session(
                package="package_c",
                task_type="navigation",
                query_text="test query",
                module_version="test",
                run_id="run_test_001",
                device_mode="WIFI",
                network_condition="normal",
                runtime="unittest",
            )
            session.set_timing(inference_ms=12.3, end_to_end_ms=12.3)
            session.finalize(success=True, confidence=0.8)
            log_path = logger.save(session, validate=True)
            self.assertTrue(log_path.exists())

    def test_video_qa_session_log_saves_and_validates(self):
        repo_root = resolve_repo_root()
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = SessionLogger(repo_root=repo_root, data_root=Path(tmpdir))
            session = create_session(
                package="package_c",
                task_type="video_qa",
                query_text="video qa query",
                module_version="navigation_task",
                run_id="run_test_vqa_001",
                device_mode="WIFI",
                network_condition="normal",
                runtime="unittest",
            )
            session.set_timing(inference_ms=8.5, end_to_end_ms=8.5)
            session.finalize(success=True, confidence=1.0)
            log_path = logger.save(session, validate=True)
            self.assertTrue(log_path.exists())

    def test_template_validation_raises_on_missing_columns(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "bad.csv"
            write_csv(csv_path, [{"run_id": "x"}], ["run_id"])
            with self.assertRaises(ValueError):
                validate_columns(csv_path, PACKAGE_A_COLUMNS)


if __name__ == "__main__":
    unittest.main()
