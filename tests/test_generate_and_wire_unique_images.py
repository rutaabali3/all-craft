import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_and_wire_unique_images
from generate_and_wire_unique_images import generate


class TestGenerateAndWireUniqueImages(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.temp_path = Path(self.temp_dir.name)

        # Patch ROOT in module so files are written inside temp_path
        self.root_patcher = patch.object(generate_and_wire_unique_images, "ROOT", self.temp_path)
        self.root_patcher.start()
        self.addCleanup(self.root_patcher.stop)

        self.sample_row = {
            "slug": "test-project",
            "index": "0",
            "prompt": "a test prompt",
            "image_path": "projects/test-project/image/item.png",
        }

    @patch("time.sleep", return_value=None)
    @patch("requests.get")
    @patch("requests.post")
    def test_generate_success(self, mock_post, mock_get, mock_sleep):
        mock_post_resp = MagicMock()
        mock_post_resp.raise_for_status.return_value = None
        mock_post_resp.json.return_value = {"imageUrl": "https://example.com/test.png"}
        mock_post.return_value = mock_post_resp

        mock_get_resp = MagicMock()
        mock_get_resp.raise_for_status.return_value = None
        mock_get_resp.content = b"x" * 10_000
        mock_get.return_value = mock_get_resp

        result = generate(self.sample_row)

        self.assertEqual(result["status"], "generated")
        self.assertEqual(result["slug"], "test-project")
        self.assertEqual(result["index"], 0)
        self.assertEqual(result["bytes"], 10_000)
        self.assertEqual(result["imageUrl"], "https://example.com/test.png")
        target_path = Path(result["path"])
        self.assertTrue(target_path.exists())
        self.assertEqual(target_path.read_bytes(), b"x" * 10_000)
        self.assertEqual(target_path, self.temp_path / "projects/test-project/image/item.png")
        mock_sleep.assert_not_called()

    @patch("time.sleep", return_value=None)
    @patch("requests.get")
    @patch("requests.post")
    def test_generate_retry_then_success(self, mock_post, mock_get, mock_sleep):
        mock_post_resp = MagicMock()
        mock_post_resp.raise_for_status.return_value = None
        mock_post_resp.json.return_value = {"imageUrl": "https://example.com/test.png"}

        mock_post.side_effect = [
            RuntimeError("Transient API failure"),
            mock_post_resp,
        ]

        mock_get_resp = MagicMock()
        mock_get_resp.raise_for_status.return_value = None
        mock_get_resp.content = b"x" * 10_000
        mock_get.return_value = mock_get_resp

        result = generate(self.sample_row)

        self.assertEqual(result["status"], "generated")
        self.assertEqual(mock_post.call_count, 2)
        mock_sleep.assert_called_once_with(2)

    @patch("time.sleep", return_value=None)
    @patch("requests.post")
    def test_generate_post_failure_all_attempts(self, mock_post, mock_sleep):
        mock_post.side_effect = RuntimeError("API down")

        result = generate(self.sample_row)

        self.assertEqual(result["status"], "failed")
        self.assertIn("API down", result["error"])
        self.assertEqual(mock_post.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 3)
        mock_sleep.assert_has_calls([unittest.mock.call(2), unittest.mock.call(4), unittest.mock.call(6)])

    @patch("time.sleep", return_value=None)
    @patch("requests.post")
    def test_generate_missing_image_url(self, mock_post, mock_sleep):
        mock_post_resp = MagicMock()
        mock_post_resp.raise_for_status.return_value = None
        mock_post_resp.json.return_value = {}  # missing imageUrl key
        mock_post.return_value = mock_post_resp

        result = generate(self.sample_row)

        self.assertEqual(result["status"], "failed")
        self.assertIn("missing imageUrl", result["error"])
        self.assertEqual(mock_post.call_count, 3)

    @patch("time.sleep", return_value=None)
    @patch("requests.get")
    @patch("requests.post")
    def test_generate_download_failure(self, mock_post, mock_get, mock_sleep):
        mock_post_resp = MagicMock()
        mock_post_resp.raise_for_status.return_value = None
        mock_post_resp.json.return_value = {"imageUrl": "https://example.com/test.png"}
        mock_post.return_value = mock_post_resp

        mock_get.side_effect = RuntimeError("Connection dropped during download")

        result = generate(self.sample_row)

        self.assertEqual(result["status"], "failed")
        self.assertIn("Connection dropped during download", result["error"])
        self.assertEqual(mock_get.call_count, 3)

    @patch("time.sleep", return_value=None)
    @patch("requests.get")
    @patch("requests.post")
    def test_generate_image_too_small(self, mock_post, mock_get, mock_sleep):
        mock_post_resp = MagicMock()
        mock_post_resp.raise_for_status.return_value = None
        mock_post_resp.json.return_value = {"imageUrl": "https://example.com/test.png"}
        mock_post.return_value = mock_post_resp

        mock_get_resp = MagicMock()
        mock_get_resp.raise_for_status.return_value = None
        mock_get_resp.content = b"too small content"  # len < 10,000
        mock_get.return_value = mock_get_resp

        result = generate(self.sample_row)

        self.assertEqual(result["status"], "failed")
        self.assertIn("image too small", result["error"])
        self.assertEqual(mock_get.call_count, 3)


if __name__ == "__main__":
    unittest.main()
