import unittest
from bs4 import BeautifulSoup
from scripts.create_and_wire_site_pages import page_html


class TestPageHtml(unittest.TestCase):
    def test_page_html_basic_structure(self):
        slug = "test-page"
        title = "Test Title"
        lede = "This is a test lede."
        sections = [("Section 1", "Content 1")]

        html_out = page_html(slug, title, lede, sections)

        self.assertTrue(html_out.startswith("<!doctype html>"))
        self.assertIn('<html lang="en">', html_out)
        self.assertIn('<meta charset="utf-8">', html_out)
        self.assertIn('<meta name="viewport" content="width=device-width, initial-scale=1">', html_out)
        self.assertIn("<title>Test Title | All Craft</title>", html_out)
        self.assertIn('<link rel="stylesheet" href="styles.css">', html_out)

        soup = BeautifulSoup(html_out, "html.parser")

        h1 = soup.find("h1")
        self.assertIsNotNone(h1)
        self.assertEqual(h1.string, "Test Title")

        p_lede = soup.find("p", class_="lede")
        self.assertIsNotNone(p_lede)
        self.assertEqual(p_lede.string, "This is a test lede.")

        eyebrow = soup.find("div", class_="eyebrow")
        self.assertIsNotNone(eyebrow)
        self.assertEqual(eyebrow.string, "All Craft information")

    def test_page_html_sections_rendering(self):
        slug = "multi-section"
        title = "Multi Section Page"
        lede = "Overview of sections"
        sections = [
            ("First Section", "First body text."),
            ("Second Section", "Second body text."),
            ("Third Section", "Third body text."),
        ]

        html_out = page_html(slug, title, lede, sections)
        soup = BeautifulSoup(html_out, "html.parser")

        cards = soup.find_all("section", class_="card")
        self.assertEqual(len(cards), 3)

        headings = [card.find("h2").text for card in cards]
        bodies = [card.find("p").text for card in cards]

        self.assertEqual(headings, ["First Section", "Second Section", "Third Section"])
        self.assertEqual(bodies, ["First body text.", "Second body text.", "Third body text."])

    def test_page_html_empty_sections(self):
        slug = "empty-sections"
        title = "Empty Sections Page"
        lede = "Page with no sections"
        sections = []

        html_out = page_html(slug, title, lede, sections)
        soup = BeautifulSoup(html_out, "html.parser")

        cards = soup.find_all("section", class_="card")
        self.assertEqual(len(cards), 0)
        self.assertEqual(soup.find("h1").string, "Empty Sections Page")
        self.assertEqual(soup.find("p", class_="lede").string, "Page with no sections")

    def test_page_html_escaping(self):
        slug = "escaping-test"
        title = "Terms & Conditions <script>alert(1)</script>"
        lede = "A & B < C > D"
        sections = [("Heading <1>", "Body & 2")]

        html_out = page_html(slug, title, lede, sections)

        self.assertIn("Terms &amp; Conditions &lt;script&gt;alert(1)&lt;/script&gt; | All Craft", html_out)
        self.assertIn("<h1>Terms &amp; Conditions &lt;script&gt;alert(1)&lt;/script&gt;</h1>", html_out)
        self.assertIn('<p class="lede">A &amp; B &lt; C &gt; D</p>', html_out)

        # Confirm script tag is not parsed as actual script element by BeautifulSoup
        soup = BeautifulSoup(html_out, "html.parser")
        self.assertIsNone(soup.find("script"))

    def test_page_html_nav_and_footer_links(self):
        html_out = page_html("test", "Title", "Lede", [])
        soup = BeautifulSoup(html_out, "html.parser")

        header = soup.find("header", class_="site-header")
        self.assertIsNotNone(header)

        brand = header.find("a", class_="brand")
        self.assertIsNotNone(brand)
        self.assertEqual(brand.get("href"), "../index.html")

        nav_links = header.find("div", class_="nav-links").find_all("a")
        link_texts = [a.string for a in nav_links]
        self.assertIn("Home", link_texts)
        self.assertIn("FAQ", link_texts)
        self.assertIn("Shipping", link_texts)
        self.assertIn("Returns", link_texts)
        self.assertIn("Privacy", link_texts)
        self.assertIn("Terms", link_texts)

        footer = soup.find("footer", class_="site-footer")
        self.assertIsNotNone(footer)
        footer_links = [a.string for a in footer.find_all("a")]
        self.assertEqual(footer_links, ["Privacy", "Terms", "Cookies", "Sitemap"])


if __name__ == "__main__":
    unittest.main()
