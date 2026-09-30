import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Ensure repo root is in python path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.generate_product_images import generate
from scripts.generate_and_wire_unique_images import generate as generate_unique


class TestGenerateProductImagesSecurity(unittest.TestCase):

    def test_absolute_path_rejected(self):
        row = {"image_path": "/etc/passwd", "prompt": "test prompt", "slug": "test-slug"}
        with self.assertRaises(ValueError) as ctx:
            generate(row)
        self.assertIn("Absolute path not allowed", str(ctx.exception))

    def test_path_traversal_relative_rejected(self):
        row = {"image_path": "../../etc/passwd", "prompt": "test prompt", "slug": "test-slug"}
        with self.assertRaises(ValueError) as ctx:
            generate(row)
        self.assertIn("Path traversal detected", str(ctx.exception))

    def test_current_dir_rejected(self):
        row = {"image_path": ".", "prompt": "test prompt", "slug": "test-slug"}
        with self.assertRaises(ValueError) as ctx:
            generate(row)
        self.assertIn("Path traversal detected", str(ctx.exception))

    def test_empty_path_rejected(self):
        row = {"image_path": "", "prompt": "test prompt", "slug": "test-slug"}
        with self.assertRaises(ValueError) as ctx:
            generate(row)
        self.assertIn("Path traversal detected", str(ctx.exception))

    @patch("pathlib.Path.write_bytes")
    @patch("pathlib.Path.mkdir")
    @patch("scripts.generate_product_images.session")
    def test_valid_relative_path_accepted(self, mock_session, mock_mkdir, mock_write_bytes):
        mock_response_post = MagicMock()
        mock_response_post.raise_for_status.return_value = None
        mock_response_post.json.return_value = {"imageUrl": "https://example.com/img.png"}

        mock_response_get = MagicMock()
        mock_response_get.raise_for_status.return_value = None
        mock_response_get.content = b"x" * 10001

        mock_session.post.return_value = mock_response_post
        mock_session.get.return_value = mock_response_get

        valid_rel_path = "projects/acrylic-paints-craft/image/item.png"
        row = {"image_path": valid_rel_path, "prompt": "test prompt", "slug": "acrylic-paints-craft"}

        result = generate(row)
        self.assertEqual(result["status"], "generated")
        self.assertTrue(result["path"].endswith(valid_rel_path))
        mock_write_bytes.assert_called_once_with(b"x" * 10001)

    def test_generate_unique_security_checks(self):
        # Verify generate_and_wire_unique_images also rejects traversal
        row = {"image_path": "/etc/passwd", "prompt": "test prompt", "slug": "test-slug", "index": "1"}
        with self.assertRaises(ValueError) as ctx:
            generate_unique(row)
        self.assertIn("Absolute path not allowed", str(ctx.exception))

        row_traversal = {"image_path": "../../etc/passwd", "prompt": "test prompt", "slug": "test-slug", "index": "1"}
        with self.assertRaises(ValueError) as ctx:
            generate_unique(row_traversal)
        self.assertIn("Path traversal detected", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
