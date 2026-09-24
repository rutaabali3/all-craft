import pytest
from bs4 import BeautifulSoup
from scripts.build_unique_image_manifest import clean, product_name


class TestClean:
    def test_clean_normal_string(self):
        assert clean("hello world") == "hello world"

    def test_clean_extra_spaces(self):
        assert clean("  hello   world  ") == "hello world"

    def test_clean_tabs_and_newlines(self):
        assert clean("\t hello \n world \r\n ") == "hello world"

    def test_clean_empty_or_none(self):
        assert clean("") == ""
        assert clean(None) == ""


class TestProductName:
    def test_title_with_premium_delimiter(self):
        html = "<html><head><title>Store Header - Premium Origami Paper</title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert product_name(soup, "origami-craft-paper") == "Origami Paper"

    def test_title_with_premium_and_whitespace(self):
        html = "<html><head><title>   Store   - Premium    Handmade  Notebook   </title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert product_name(soup, "handmade-craft-notebook") == "Handmade Notebook"

    def test_title_with_multiple_premium_delimiters(self):
        html = "<html><head><title>First - Premium Second - Premium Third</title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert product_name(soup, "some-slug") == "Second - Premium Third"

    def test_title_without_premium_delimiter_uses_slug_fallback(self):
        html = "<html><head><title>Craft Supplies Store</title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert product_name(soup, "origami-craft-paper-kit") == "origami paper kit"

    def test_missing_title_tag_uses_slug_fallback(self):
        html = "<html><head></head><body>No title here</body></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert product_name(soup, "ceramic-craft-mugs") == "ceramic mugs"

    def test_empty_title_tag_uses_slug_fallback(self):
        html = "<html><head><title></title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert product_name(soup, "wood-craft-carving") == "wood carving"

    def test_whitespace_title_tag_uses_slug_fallback(self):
        html = "<html><head><title>   \n  </title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert product_name(soup, "acrylic-craft-paints") == "acrylic paints"

    def test_slug_without_craft(self):
        html = "<html><head><title>Simple Store</title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert product_name(soup, "watercolor-pencils") == "watercolor pencils"

    def test_slug_with_multiple_hyphens(self):
        html = "<html><head><title>No Premium Here</title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert product_name(soup, "clay--craft--tools") == "clay tools"
