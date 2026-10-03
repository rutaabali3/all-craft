import unittest
import sys
from pathlib import Path

# Add repo root to sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_image_manifest import clean


class TestClean(unittest.TestCase):
    def test_clean_normal_string(self):
        self.assertEqual(clean("hello world"), "hello world")

    def test_clean_leading_and_trailing_whitespace(self):
        self.assertEqual(clean("   hello world   "), "hello world")

    def test_clean_multiple_internal_whitespace(self):
        self.assertEqual(clean("hello\t\n  world   test"), "hello world test")

    def test_clean_empty_string(self):
        self.assertEqual(clean(""), "")

    def test_clean_none_value(self):
        self.assertEqual(clean(None), "")

    def test_clean_only_whitespace(self):
        self.assertEqual(clean("   \t\n  "), "")


if __name__ == "__main__":
    unittest.main()
