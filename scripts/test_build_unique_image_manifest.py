from bs4 import BeautifulSoup
from scripts.build_unique_image_manifest import clean, product_name

def test_clean_strips_spaces():
    assert clean("  hello   world  ") == "hello world"

def test_clean_handles_none():
    assert clean(None) == ""

def test_clean_handles_newlines():
    assert clean("hello\nworld") == "hello world"

def test_clean_handles_empty_string():
    assert clean("") == ""

def test_product_name_extracts_from_premium_title():
    html = "<title>Some Store - Premium Notebooks</title>"
    soup = BeautifulSoup(html, "html.parser")
    assert product_name(soup, "notebooks-craft") == "Notebooks"

def test_product_name_extracts_from_premium_title_with_extra_spaces():
    html = "<title>   Some Store   - Premium   Notebooks   </title>"
    soup = BeautifulSoup(html, "html.parser")
    assert product_name(soup, "notebooks-craft") == "Notebooks"

def test_product_name_uses_title_when_no_premium():
    html = "<title>Cool Notebooks Store</title>"
    soup = BeautifulSoup(html, "html.parser")
    assert product_name(soup, "notebooks-craft") == "notebooks"

def test_product_name_fallback_to_slug_when_no_title():
    html = "<div>No title here</div>"
    soup = BeautifulSoup(html, "html.parser")
    assert product_name(soup, "cool-notebooks-craft") == "cool notebooks"

def test_product_name_fallback_to_slug_when_empty_title():
    html = "<title></title>"
    soup = BeautifulSoup(html, "html.parser")
    assert product_name(soup, "awesome-pens-craft") == "awesome pens"
