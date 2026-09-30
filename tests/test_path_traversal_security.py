import unittest
from pathlib import Path
from scripts.generate_and_wire_unique_images import generate as generate_unique
from scripts.generate_product_images import generate as generate_product


class TestPathTraversalSecurity(unittest.TestCase):
    def test_unique_images_absolute_path_traversal(self):
        row = {
            "image_path": "/etc/passwd",
            "prompt": "test prompt",
            "slug": "test-slug",
            "index": "1",
        }
        with self.assertRaises(ValueError) as ctx:
            generate_unique(row)
        self.assertIn("Path traversal detected", str(ctx.exception))

    def test_unique_images_relative_path_traversal(self):
        row = {
            "image_path": "../../../etc/passwd",
            "prompt": "test prompt",
            "slug": "test-slug",
            "index": "1",
        }
        with self.assertRaises(ValueError) as ctx:
            generate_unique(row)
        self.assertIn("Path traversal detected", str(ctx.exception))

    def test_product_images_absolute_path_traversal(self):
        row = {
            "image_path": "/etc/shadow",
            "prompt": "test prompt",
            "slug": "test-slug",
        }
        with self.assertRaises(ValueError) as ctx:
            generate_product(row)
        self.assertIn("Path traversal detected", str(ctx.exception))

    def test_product_images_relative_path_traversal(self):
        row = {
            "image_path": "../../tmp/malicious.png",
            "prompt": "test prompt",
            "slug": "test-slug",
        }
        with self.assertRaises(ValueError) as ctx:
            generate_product(row)
        self.assertIn("Path traversal detected", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
