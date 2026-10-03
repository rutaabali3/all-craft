import unittest
from scripts.generate_and_wire_unique_images import validate_slug


class TestSlugValidation(unittest.TestCase):
    def test_valid_slugs(self):
        valid_slugs = [
            "acrylic-paint-craft",
            "calligraphy-pen-craft",
            "simple_slug",
            "slug123",
        ]
        for slug in valid_slugs:
            self.assertEqual(validate_slug(slug), slug)

    def test_invalid_slugs_path_traversal(self):
        invalid_slugs = [
            "..",
            ".",
            "../foo",
            "../../etc/passwd",
            "foo/bar",
            "foo/../bar",
            "/etc/passwd",
            "/",
            "C:\\Windows",
            "..\\foo",
            "",
            None,
            "slug\0nullbyte",
        ]
        for slug in invalid_slugs:
            with self.subTest(slug=slug):
                with self.assertRaises(ValueError):
                    validate_slug(slug)


if __name__ == "__main__":
    unittest.main()
