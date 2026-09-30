import unittest
from bs4 import BeautifulSoup
from scripts.build_unique_image_manifest import clean, product_name


class TestClean(unittest.TestCase):
    def test_clean_normal_string(self):
        self.assertEqual(clean("  hello   world  "), "hello world")

    def test_clean_empty_or_none(self):
        self.assertEqual(clean(""), "")
        self.assertEqual(clean(None), "")

    def test_clean_newlines_and_tabs(self):
        self.assertEqual(clean("hello\n\t world\r\n"), "hello world")


class TestProductName(unittest.TestCase):
    def test_product_name_with_premium_title(self):
        html = "<html><head><title>  Brand Name - Premium Craft Glue </title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        result = product_name(soup, "craft-glue-craft")
        self.assertEqual(result, "Craft Glue")

    def test_product_name_without_premium_title(self):
        html = "<html><head><title> Just Some Title </title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        result = product_name(soup, "craft-glue-craft")
        self.assertEqual(result, "craft glue")

    def test_product_name_missing_title_tag(self):
        html = "<html><head></head><body>No title</body></html>"
        soup = BeautifulSoup(html, "html.parser")
        result = product_name(soup, "paintbrushes-craft")
        self.assertEqual(result, "paintbrushes")

    def test_product_name_empty_title_tag(self):
        html = "<html><head><title></title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        result = product_name(soup, "watercolor-paper-craft")
        self.assertEqual(result, "watercolor paper")

    def test_product_name_slug_formatting_without_craft(self):
        html = "<html><head></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        result = product_name(soup, "fountain-pen-ink")
        self.assertEqual(result, "fountain pen ink")

    def test_product_name_multiple_premium_delimiters(self):
        html = "<html><head><title>Site - Premium Category - Premium Wooden Scissors</title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        result = product_name(soup, "wooden-scissors-craft")
        self.assertEqual(result, "Category - Premium Wooden Scissors")


if __name__ == "__main__":
    unittest.main()
