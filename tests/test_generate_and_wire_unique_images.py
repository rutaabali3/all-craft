import tempfile
import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import requests

from scripts.generate_and_wire_unique_images import generate


class TestGenerateAndWireUniqueImages(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.temp_path = Path(self.temp_dir.name)

        self.row = {
            "slug": "test-product",
            "index": "1",
            "prompt": "A test prompt for image generation",
            "image_path": "projects/test-product/image/item1.png",
        }

    @patch("scripts.generate_and_wire_unique_images.time.sleep")
    @patch("scripts.generate_and_wire_unique_images.requests.get")
    @patch("scripts.generate_and_wire_unique_images.requests.post")
    def test_generate_success(self, mock_post, mock_get, mock_sleep):
        # Setup mock post response
        mock_post_resp = MagicMock()
        mock_post_resp.raise_for_status.return_value = None
        mock_post_resp.json.return_value = {"imageUrl": "https://example.com/generated_image.png"}
        mock_post.return_value = mock_post_resp

        # Setup mock get response with > 10,000 bytes content
        mock_get_resp = MagicMock()
        mock_get_resp.raise_for_status.return_value = None
        image_bytes = b"X" * 10001
        mock_get_resp.content = image_bytes
        mock_get.return_value = mock_get_resp

        with patch("scripts.generate_and_wire_unique_images.ROOT", self.temp_path):
            result = generate(self.row)

        expected_target = self.temp_path / self.row["image_path"]
        self.assertTrue(expected_target.exists())
        self.assertEqual(expected_target.read_bytes(), image_bytes)
        self.assertEqual(
            result,
            {
                "slug": "test-product",
                "index": 1,
                "status": "generated",
                "path": str(expected_target),
                "bytes": len(image_bytes),
                "imageUrl": "https://example.com/generated_image.png",
            },
        )
        mock_post.assert_called_once_with("https://ahm7xmakki.com/api/tti", json={"prompt": self.row["prompt"], "ratio": "1:1"}, timeout=180)
        mock_get.assert_called_once_with("https://example.com/generated_image.png", timeout=180)
        mock_sleep.assert_not_called()

    @patch("scripts.generate_and_wire_unique_images.time.sleep")
    @patch("scripts.generate_and_wire_unique_images.requests.post")
    def test_generate_missing_image_url(self, mock_post, mock_sleep):
        mock_post_resp = MagicMock()
        mock_post_resp.raise_for_status.return_value = None
        mock_post_resp.json.return_value = {}  # missing imageUrl
        mock_post.return_value = mock_post_resp

        with patch("scripts.generate_and_wire_unique_images.ROOT", self.temp_path):
            result = generate(self.row)

        expected_target = self.temp_path / self.row["image_path"]
        self.assertFalse(expected_target.exists())
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["slug"], "test-product")
        self.assertEqual(result["index"], 1)
        self.assertIn("missing imageUrl", result["error"])
        self.assertEqual(mock_post.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 3)

    @patch("scripts.generate_and_wire_unique_images.time.sleep")
    @patch("scripts.generate_and_wire_unique_images.requests.get")
    @patch("scripts.generate_and_wire_unique_images.requests.post")
    def test_generate_image_too_small(self, mock_post, mock_get, mock_sleep):
        mock_post_resp = MagicMock()
        mock_post_resp.raise_for_status.return_value = None
        mock_post_resp.json.return_value = {"imageUrl": "https://example.com/generated_image.png"}
        mock_post.return_value = mock_post_resp

        mock_get_resp = MagicMock()
        mock_get_resp.raise_for_status.return_value = None
        mock_get_resp.content = b"small_image_content"  # < 10,000 bytes
        mock_get.return_value = mock_get_resp

        with patch("scripts.generate_and_wire_unique_images.ROOT", self.temp_path):
            result = generate(self.row)

        self.assertEqual(result["status"], "failed")
        self.assertIn("image too small", result["error"])
        self.assertEqual(mock_post.call_count, 3)
        self.assertEqual(mock_get.call_count, 3)

    @patch("scripts.generate_and_wire_unique_images.time.sleep")
    @patch("scripts.generate_and_wire_unique_images.requests.post")
    def test_generate_http_error(self, mock_post, mock_sleep):
        mock_post.side_effect = requests.RequestException("Connection error")

        with patch("scripts.generate_and_wire_unique_images.ROOT", self.temp_path):
            result = generate(self.row)

        self.assertEqual(result["status"], "failed")
        self.assertIn("Connection error", result["error"])
        self.assertEqual(mock_post.call_count, 3)

    @patch("scripts.generate_and_wire_unique_images.time.sleep")
    @patch("scripts.generate_and_wire_unique_images.requests.get")
    @patch("scripts.generate_and_wire_unique_images.requests.post")
    def test_generate_retry_recovery(self, mock_post, mock_get, mock_sleep):
        # First post fails, second post succeeds
        mock_post_fail = MagicMock()
        mock_post_fail.raise_for_status.side_effect = requests.HTTPError("500 Server Error")

        mock_post_success = MagicMock()
        mock_post_success.raise_for_status.return_value = None
        mock_post_success.json.return_value = {"imageUrl": "https://example.com/image.png"}

        mock_post.side_effect = [mock_post_fail, mock_post_success]

        mock_get_resp = MagicMock()
        mock_get_resp.raise_for_status.return_value = None
        image_bytes = b"Y" * 12000
        mock_get_resp.content = image_bytes
        mock_get.return_value = mock_get_resp

        with patch("scripts.generate_and_wire_unique_images.ROOT", self.temp_path):
            result = generate(self.row)

        self.assertEqual(result["status"], "generated")
        self.assertEqual(mock_post.call_count, 2)
        self.assertEqual(mock_sleep.call_count, 1)


if __name__ == "__main__":
    unittest.main()
