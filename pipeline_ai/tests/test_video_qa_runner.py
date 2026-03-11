import tempfile
from pathlib import Path
import unittest

from pipeline_ai.logger import resolve_repo_root
from pipeline_ai.video_qa_runner import resolve_model_target, run_video_qa


class VideoQARunnerTests(unittest.TestCase):
    def test_resolve_model_target_supports_qwen_and_st_r1(self):
        repo_root = resolve_repo_root()
        qwen_target = resolve_model_target(repo_root, "qwen")
        st_r1_target = resolve_model_target(repo_root, "st-r1")

        self.assertEqual(qwen_target, "Qwen/Qwen2-VL-2B-Instruct")
        self.assertTrue(Path(st_r1_target).exists())

    def test_run_video_qa_dry_run_writes_outputs(self):
        repo_root = resolve_repo_root()
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            result = run_video_qa(
                task_name="corridor_navigation",
                model_preset="qwen",
                dry_run=True,
                repo_root=repo_root,
                results_dir_override=tmp / "results",
                session_data_root=tmp / "data",
            )

            summary_file = Path(result["summary_file"])
            result_files = [Path(path) for path in result["result_files"]]
            session_logs = [Path(path) for path in result["session_logs"]]

            self.assertTrue(summary_file.exists())
            self.assertEqual(len(result_files), 1)
            self.assertTrue(result_files[0].exists())
            self.assertEqual(len(session_logs), 1)
            self.assertTrue(session_logs[0].exists())


if __name__ == "__main__":
    unittest.main()
