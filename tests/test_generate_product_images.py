from unittest.mock import MagicMock, patch
import tempfile
import unittest
from pathlib import Path

from scripts.generate_product_images import generate


class TestGenerateProductImages(unittest.TestCase):

    @patch("scripts.generate_product_images.session")
    def test_generate_success(self, mock_session):
        with tempfile.TemporaryDirectory() as tmpdir:
            target_path = Path(tmpdir) / "test_img.png"
            row = {
                "prompt": "a photo of an item",
                "image_path": str(target_path),
                "slug": "test-item"
            }

            # Mock POST response
            mock_post_res = MagicMock()
            mock_post_res.raise_for_status.return_value = None
            mock_post_res.json.return_value = {"imageUrl": "http://example.com/image.png"}

            # Mock GET response streaming 12,000 bytes in chunks
            mock_get_res = MagicMock()
            mock_get_res.raise_for_status.return_value = None
            chunk_data = b"x" * 4000
            mock_get_res.iter_content.return_value = [chunk_data, chunk_data, chunk_data]

            mock_session.post.return_value = mock_post_res
            mock_session.get.return_value = mock_get_res

            res = generate(row)

            self.assertEqual(res["status"], "generated")
            self.assertEqual(res["bytes"], 12000)
            self.assertTrue(target_path.exists())
            self.assertEqual(len(target_path.read_bytes()), 12000)
            mock_session.get.assert_called_with("http://example.com/image.png", timeout=150, stream=True)

    @patch("scripts.generate_product_images.time.sleep")
    @patch("scripts.generate_product_images.session")
    def test_generate_too_small(self, mock_session, mock_sleep):
        with tempfile.TemporaryDirectory() as tmpdir:
            target_path = Path(tmpdir) / "test_small.png"
            row = {
                "prompt": "a photo of an item",
                "image_path": str(target_path),
                "slug": "test-item-small"
            }

            mock_post_res = MagicMock()
            mock_post_res.raise_for_status.return_value = None
            mock_post_res.json.return_value = {"imageUrl": "http://example.com/small.png"}

            mock_get_res = MagicMock()
            mock_get_res.raise_for_status.return_value = None
            mock_get_res.iter_content.return_value = [b"x" * 500]  # total 500 bytes < 10,000

            mock_session.post.return_value = mock_post_res
            mock_session.get.return_value = mock_get_res

            res = generate(row)

            self.assertEqual(res["status"], "failed")
            self.assertIn("image too small: 500 bytes", res["error"])
            self.assertFalse(target_path.exists())


if __name__ == "__main__":
    unittest.main()
