import unittest
from bs4 import BeautifulSoup
from scripts.build_unique_image_manifest import clean, product_name


class TestBuildUniqueImageManifest(unittest.TestCase):
    def test_clean_none(self):
        self.assertEqual(clean(None), "")

    def test_clean_empty_string(self):
        self.assertEqual(clean(""), "")

    def test_clean_whitespace_only(self):
        self.assertEqual(clean("   \t\n\r  "), "")

    def test_clean_normal_string(self):
        self.assertEqual(clean("hello world"), "hello world")

    def test_clean_leading_and_trailing_whitespace(self):
        self.assertEqual(clean("   hello world   "), "hello world")

    def test_clean_multiple_internal_whitespaces(self):
        self.assertEqual(clean("hello   \t\n  world"), "hello world")

    def test_product_name_with_premium_title(self):
        soup = BeautifulSoup("<title>Origami Paper - Premium Craft Supply</title>", "html.parser")
        self.assertEqual(product_name(soup, "origami-paper-craft"), "Craft Supply")

    def test_product_name_without_premium_title(self):
        soup = BeautifulSoup("<title>Origami Paper Craft</title>", "html.parser")
        self.assertEqual(product_name(soup, "origami-paper-craft"), "origami paper")

    def test_product_name_no_title(self):
        soup = BeautifulSoup("<html><body>No title here</body></html>", "html.parser")
        self.assertEqual(product_name(soup, "origami-paper-craft"), "origami paper")


if __name__ == "__main__":
    unittest.main()
