from unittest.mock import patch
import unittest

from pipeline_ai.cli import main


class CLITests(unittest.TestCase):
    @patch("pipeline_ai.cli.run_video_qa")
    def test_video_qa_run_does_not_require_output_root(self, mock_run_video_qa):
        mock_run_video_qa.return_value = {
            "task": "corridor_navigation",
            "model_preset": "qwen",
            "model_target": "Qwen/Qwen2-VL-2B-Instruct",
            "results_dir": "/tmp/results",
            "summary_file": "/tmp/summary.json",
            "result_files": [],
            "session_logs": [],
        }

        exit_code = main(["video-qa-run", "--task", "corridor_navigation", "--dry-run"])

        self.assertEqual(exit_code, 0)
        mock_run_video_qa.assert_called_once()


if __name__ == "__main__":
    unittest.main()
