import pathlib
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch, call
import requests

# Ensure root directory is in sys.path
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.generate_product_images import generate, session


class TestGenerateProductImages(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.base_path = pathlib.Path(self.temp_dir.name)

        self.row = {
            "slug": "test-product",
            "prompt": "A beautiful test image prompt",
            "image_path": "projects/test-product/image/item.png",
        }

    @patch("scripts.generate_product_images.ROOT")
    @patch("scripts.generate_product_images.time.sleep")
    def test_generate_success(self, mock_sleep, mock_root):
        mock_root.__truediv__.side_effect = lambda path: self.base_path / path

        mock_post_resp = MagicMock()
        mock_post_resp.raise_for_status.return_value = None
        mock_post_resp.json.return_value = {"imageUrl": "http://example.com/img.png"}

        mock_get_resp = MagicMock()
        mock_get_resp.raise_for_status.return_value = None
        mock_get_resp.content = b"A" * 10000

        with patch.object(session, "post", return_value=mock_post_resp) as mock_post, \
             patch.object(session, "get", return_value=mock_get_resp) as mock_get:
            result = generate(self.row)

        target_file = self.base_path / self.row["image_path"]
        self.assertTrue(target_file.exists())
        self.assertEqual(target_file.read_bytes(), b"A" * 10000)

        self.assertEqual(result["slug"], "test-product")
        self.assertEqual(result["status"], "generated")
        self.assertEqual(result["bytes"], 10000)
        self.assertEqual(result["imageUrl"], "http://example.com/img.png")
        self.assertEqual(result["path"], str(target_file))

        mock_post.assert_called_once_with(
            "https://ahm7xmakki.com/api/tti",
            json={"prompt": self.row["prompt"], "ratio": "1:1"},
            timeout=150,
        )
        mock_get.assert_called_once_with("http://example.com/img.png", timeout=150)
        mock_sleep.assert_not_called()

    @patch("scripts.generate_product_images.ROOT")
    @patch("scripts.generate_product_images.time.sleep")
    def test_generate_missing_image_url(self, mock_sleep, mock_root):
        mock_root.__truediv__.side_effect = lambda path: self.base_path / path

        mock_post_resp = MagicMock()
        mock_post_resp.raise_for_status.return_value = None
        mock_post_resp.json.return_value = {}  # missing imageUrl

        with patch.object(session, "post", return_value=mock_post_resp) as mock_post:
            result = generate(self.row)

        self.assertEqual(result["slug"], "test-product")
        self.assertEqual(result["status"], "failed")
        self.assertIn("missing imageUrl", result["error"])

        self.assertEqual(mock_post.call_count, 3)
        self.assertEqual(mock_sleep.call_args_list, [call(2), call(4), call(6)])

    @patch("scripts.generate_product_images.ROOT")
    @patch("scripts.generate_product_images.time.sleep")
    def test_generate_image_too_small(self, mock_sleep, mock_root):
        mock_root.__truediv__.side_effect = lambda path: self.base_path / path

        mock_post_resp = MagicMock()
        mock_post_resp.raise_for_status.return_value = None
        mock_post_resp.json.return_value = {"imageUrl": "http://example.com/tiny.png"}

        mock_get_resp = MagicMock()
        mock_get_resp.raise_for_status.return_value = None
        mock_get_resp.content = b"too small"  # 9 bytes < 10000

        with patch.object(session, "post", return_value=mock_post_resp), \
             patch.object(session, "get", return_value=mock_get_resp):
            result = generate(self.row)

        self.assertEqual(result["slug"], "test-product")
        self.assertEqual(result["status"], "failed")
        self.assertIn("image too small", result["error"])
        self.assertEqual(mock_sleep.call_args_list, [call(2), call(4), call(6)])

    @patch("scripts.generate_product_images.ROOT")
    @patch("scripts.generate_product_images.time.sleep")
    def test_generate_post_http_error(self, mock_sleep, mock_root):
        mock_root.__truediv__.side_effect = lambda path: self.base_path / path

        mock_post_resp = MagicMock()
        mock_post_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Internal Server Error")

        with patch.object(session, "post", return_value=mock_post_resp) as mock_post:
            result = generate(self.row)

        self.assertEqual(result["slug"], "test-product")
        self.assertEqual(result["status"], "failed")
        self.assertIn("500 Internal Server Error", result["error"])
        self.assertEqual(mock_post.call_count, 3)
        self.assertEqual(mock_sleep.call_args_list, [call(2), call(4), call(6)])

    @patch("scripts.generate_product_images.ROOT")
    @patch("scripts.generate_product_images.time.sleep")
    def test_generate_get_http_error(self, mock_sleep, mock_root):
        mock_root.__truediv__.side_effect = lambda path: self.base_path / path

        mock_post_resp = MagicMock()
        mock_post_resp.raise_for_status.return_value = None
        mock_post_resp.json.return_value = {"imageUrl": "http://example.com/bad.png"}

        mock_get_resp = MagicMock()
        mock_get_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

        with patch.object(session, "post", return_value=mock_post_resp), \
             patch.object(session, "get", return_value=mock_get_resp) as mock_get:
            result = generate(self.row)

        self.assertEqual(result["slug"], "test-product")
        self.assertEqual(result["status"], "failed")
        self.assertIn("404 Not Found", result["error"])
        self.assertEqual(mock_get.call_count, 3)
        self.assertEqual(mock_sleep.call_args_list, [call(2), call(4), call(6)])

    @patch("scripts.generate_product_images.ROOT")
    @patch("scripts.generate_product_images.time.sleep")
    def test_generate_recovery_on_retry(self, mock_sleep, mock_root):
        mock_root.__truediv__.side_effect = lambda path: self.base_path / path

        # Attempt 1 fails with missing imageUrl; Attempt 2 succeeds
        resp_fail = MagicMock()
        resp_fail.raise_for_status.return_value = None
        resp_fail.json.return_value = {}

        resp_success = MagicMock()
        resp_success.raise_for_status.return_value = None
        resp_success.json.return_value = {"imageUrl": "http://example.com/img.png"}

        mock_get_resp = MagicMock()
        mock_get_resp.raise_for_status.return_value = None
        mock_get_resp.content = b"B" * 12000

        with patch.object(session, "post", side_effect=[resp_fail, resp_success]), \
             patch.object(session, "get", return_value=mock_get_resp):
            result = generate(self.row)

        self.assertEqual(result["status"], "generated")
        self.assertEqual(result["bytes"], 12000)
        mock_sleep.assert_called_once_with(2)


if __name__ == "__main__":
    unittest.main()
