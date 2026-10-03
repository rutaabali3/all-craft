import unittest
import sys
from pathlib import Path

# Ensure root directory is in sys.path so scripts module can be imported
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_image_manifest import clean


class TestCleanFunction(unittest.TestCase):
    def test_clean_standard_string(self):
        self.assertEqual(clean("hello world"), "hello world")

    def test_clean_multiple_spaces(self):
        self.assertEqual(clean("hello   world"), "hello world")

    def test_clean_leading_trailing_whitespace(self):
        self.assertEqual(clean("  hello world  "), "hello world")

    def test_clean_newlines_tabs_whitespace(self):
        self.assertEqual(clean("\t hello\n\r  world \n"), "hello world")

    def test_clean_empty_string(self):
        self.assertEqual(clean(""), "")

    def test_clean_none(self):
        self.assertEqual(clean(None), "")


if __name__ == "__main__":
    unittest.main()
