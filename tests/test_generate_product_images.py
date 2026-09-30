from unittest.mock import MagicMock, call, patch
import os
import tempfile
import unittest

import requests

from scripts.generate_product_images import generate, session


class TestGenerateProductImages(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = os.path.join(self.temp_dir.name, "test_image.jpg")
        self.row = {
            "slug": "test-product",
            "prompt": "A test prompt for product image",
            "image_path": self.test_path,
        }

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("scripts.generate_product_images.time.sleep")
    @patch.object(session, "post")
    @patch.object(session, "get")
    def test_generate_success(self, mock_get, mock_post, mock_sleep):
        # Setup post response
        mock_post_resp = MagicMock()
        mock_post_resp.json.return_value = {"imageUrl": "https://example.com/test.png"}
        mock_post.return_value = mock_post_resp

        # Setup get response
        mock_get_resp = MagicMock()
        mock_get_resp.content = b"x" * 12000
        mock_get.return_value = mock_get_resp

        result = generate(self.row)

        self.assertEqual(result["status"], "generated")
        self.assertEqual(result["slug"], "test-product")
        self.assertEqual(result["bytes"], 12000)
        self.assertEqual(result["imageUrl"], "https://example.com/test.png")
        self.assertEqual(result["path"], self.test_path)
        self.assertTrue(os.path.exists(self.test_path))

        mock_post.assert_called_once()
        mock_get.assert_called_once_with("https://example.com/test.png", timeout=150)
        mock_sleep.assert_not_called()

    @patch("scripts.generate_product_images.time.sleep")
    @patch.object(session, "post")
    def test_generate_error_path_retries_and_failure(self, mock_post, mock_sleep):
        mock_post.side_effect = requests.RequestException("Connection timed out")

        result = generate(self.row)

        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["slug"], "test-product")
        self.assertEqual(result["path"], self.test_path)
        self.assertIn("RequestException", result["error"])
        self.assertIn("Connection timed out", result["error"])

        # Check retries and sleep backoff (2, 4, 6)
        self.assertEqual(mock_post.call_count, 3)
        mock_sleep.assert_has_calls([call(2), call(4), call(6)])
        self.assertEqual(mock_sleep.call_count, 3)

    @patch("scripts.generate_product_images.time.sleep")
    @patch.object(session, "post")
    @patch.object(session, "get")
    def test_generate_retry_success_on_later_attempt(self, mock_get, mock_post, mock_sleep):
        mock_post_resp = MagicMock()
        mock_post_resp.json.return_value = {"imageUrl": "https://example.com/retry.png"}

        # Fail on first call, succeed on second call
        mock_post.side_effect = [
            requests.RequestException("Temporary failure"),
            mock_post_resp,
        ]

        mock_get_resp = MagicMock()
        mock_get_resp.content = b"y" * 15000
        mock_get.return_value = mock_get_resp

        result = generate(self.row)

        self.assertEqual(result["status"], "generated")
        self.assertEqual(result["bytes"], 15000)
        self.assertEqual(mock_post.call_count, 2)
        mock_sleep.assert_called_once_with(2)

    @patch("scripts.generate_product_images.time.sleep")
    @patch.object(session, "post")
    def test_generate_missing_image_url(self, mock_post, mock_sleep):
        mock_post_resp = MagicMock()
        mock_post_resp.json.return_value = {"status": "ok"}  # Missing imageUrl
        mock_post.return_value = mock_post_resp

        result = generate(self.row)

        self.assertEqual(result["status"], "failed")
        self.assertIn("missing imageUrl", result["error"])
        self.assertEqual(mock_post.call_count, 3)
        mock_sleep.assert_has_calls([call(2), call(4), call(6)])

    @patch("scripts.generate_product_images.time.sleep")
    @patch.object(session, "post")
    @patch.object(session, "get")
    def test_generate_image_too_small(self, mock_get, mock_post, mock_sleep):
        mock_post_resp = MagicMock()
        mock_post_resp.json.return_value = {"imageUrl": "https://example.com/small.png"}
        mock_post.return_value = mock_post_resp

        mock_get_resp = MagicMock()
        mock_get_resp.content = b"small" * 10  # 50 bytes < 10,000
        mock_get.return_value = mock_get_resp

        result = generate(self.row)

        self.assertEqual(result["status"], "failed")
        self.assertIn("image too small", result["error"])
        self.assertEqual(mock_post.call_count, 3)
        self.assertEqual(mock_get.call_count, 3)
        mock_sleep.assert_has_calls([call(2), call(4), call(6)])


if __name__ == "__main__":
    unittest.main()
