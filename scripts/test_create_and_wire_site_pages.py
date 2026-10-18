import pytest
from scripts.create_and_wire_site_pages import page_html

def test_page_html_basic():
    slug = "test-page"
    title = "Test Title"
    lede = "Test Lede"
    sections = [("Section 1", "Body 1"), ("Section 2", "Body 2")]

    html = page_html(slug, title, lede, sections)

    assert "<title>Test Title | All Craft</title>" in html
    assert "<h1>Test Title</h1>" in html
    assert '<p class="lede">Test Lede</p>' in html
    assert '<section class="card"><h2>Section 1</h2><p>Body 1</p></section>' in html
    assert '<section class="card"><h2>Section 2</h2><p>Body 2</p></section>' in html

def test_page_html_escaping():
    slug = "xss-page"
    title = "<script>alert('title')</script>"
    lede = "<script>alert('lede')</script>"
    sections = []

    html = page_html(slug, title, lede, sections)

    assert "<title>&lt;script&gt;alert(&#x27;title&#x27;)&lt;/script&gt; | All Craft</title>" in html
    assert "<h1>&lt;script&gt;alert(&#x27;title&#x27;)&lt;/script&gt;</h1>" in html
    assert '<p class="lede">&lt;script&gt;alert(&#x27;lede&#x27;)&lt;/script&gt;</p>' in html
    # Ensure raw script tags are NOT present for the title and lede
    assert "<script>alert('title')</script>" not in html
    assert "<script>alert('lede')</script>" not in html

def test_page_html_empty_sections():
    slug = "empty-page"
    title = "Empty"
    lede = "No sections here"
    sections = []

    html = page_html(slug, title, lede, sections)

    assert "<title>Empty | All Craft</title>" in html
    assert "<h1>Empty</h1>" in html
    assert '<p class="lede">No sections here</p>' in html
    assert '<section class="card">' not in html
