import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

from generate_and_wire_unique_images import generate

class TestGenerateUniqueImages(unittest.TestCase):
    def setUp(self):
        self.row = {
            "slug": "test-project",
            "index": "1",
            "prompt": "test prompt",
            "image_path": "projects/test-project/image/item_1.png"
        }

    @patch("generate_and_wire_unique_images.time.sleep")
    @patch("generate_and_wire_unique_images.requests.get")
    @patch("generate_and_wire_unique_images.requests.post")
    @patch("generate_and_wire_unique_images.Path.write_bytes")
    def test_generate_happy_path(self, mock_write_bytes, mock_post, mock_get, mock_sleep):
        # Mock post response
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {"imageUrl": "http://example.com/image.png"}
        mock_post.return_value = mock_post_response

        # Mock get response with large enough content
        mock_get_response = MagicMock()
        mock_get_response.content = b"x" * 15000
        mock_get.return_value = mock_get_response

        result = generate(self.row)

        self.assertEqual(result["status"], "generated")
        self.assertEqual(result["slug"], "test-project")
        self.assertEqual(result["index"], 1)
        self.assertEqual(result["bytes"], 15000)
        self.assertEqual(result["imageUrl"], "http://example.com/image.png")
        self.assertTrue("projects/test-project/image/item_1.png" in result["path"])

        mock_post.assert_called_once()
        mock_get.assert_called_once_with("http://example.com/image.png", timeout=180)
        mock_write_bytes.assert_called_once_with(b"x" * 15000)
        mock_sleep.assert_not_called()

    @patch("generate_and_wire_unique_images.time.sleep")
    @patch("generate_and_wire_unique_images.requests.get")
    @patch("generate_and_wire_unique_images.requests.post")
    def test_generate_image_too_small(self, mock_post, mock_get, mock_sleep):
        # Mock post response
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {"imageUrl": "http://example.com/image.png"}
        mock_post.return_value = mock_post_response

        # Mock get response with too small content
        mock_get_response = MagicMock()
        mock_get_response.content = b"x" * 5000
        mock_get.return_value = mock_get_response

        result = generate(self.row)

        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["slug"], "test-project")
        self.assertEqual(result["index"], 1)
        self.assertIn("image too small: 5000 bytes", result["error"])

        self.assertEqual(mock_post.call_count, 3)
        self.assertEqual(mock_get.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 3)

    @patch("generate_and_wire_unique_images.time.sleep")
    @patch("generate_and_wire_unique_images.requests.post")
    def test_generate_post_failure(self, mock_post, mock_sleep):
        # Mock post response to raise an exception
        mock_post.side_effect = Exception("API Error")

        result = generate(self.row)

        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["slug"], "test-project")
        self.assertEqual(result["index"], 1)
        self.assertIn("Exception('API Error')", result["error"])

        self.assertEqual(mock_post.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 3)


if __name__ == "__main__":
    unittest.main()
