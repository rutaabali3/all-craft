import unittest
from scripts.create_and_wire_site_pages import page_html, content


class TestPageHtml(unittest.TestCase):
    def test_basic_structure(self):
        slug = "test-slug"
        title = "Test Title"
        lede = "Test Lede Description"
        sections = [("Section 1", "Body 1")]

        html_out = page_html(slug, title, lede, sections)

        self.assertTrue(html_out.startswith("<!doctype html>"))
        self.assertIn("<html lang=\"en\">", html_out)
        self.assertIn("<title>Test Title | All Craft</title>", html_out)
        self.assertIn("<h1>Test Title</h1>", html_out)
        self.assertIn("<p class=\"lede\">Test Lede Description</p>", html_out)
        self.assertIn("<section class=\"card\"><h2>Section 1</h2><p>Body 1</p></section>", html_out)
        self.assertTrue(html_out.endswith("</html>"))

    def test_html_escaping_in_title_and_lede(self):
        title = "Terms & Conditions <Draft>"
        lede = "For \"All Craft\" & 'Partners'"
        sections = []

        html_out = page_html("terms", title, lede, sections)

        self.assertIn("<title>Terms &amp; Conditions &lt;Draft&gt; | All Craft</title>", html_out)
        self.assertIn("<h1>Terms &amp; Conditions &lt;Draft&gt;</h1>", html_out)
        self.assertIn("<p class=\"lede\">For &quot;All Craft&quot; &amp; &#x27;Partners&#x27;</p>", html_out)

    def test_empty_sections(self):
        html_out = page_html("empty", "Title", "Lede", [])
        self.assertIn("<main class=\"container\"><div class=\"eyebrow\">All Craft information</div><h1>Title</h1><p class=\"lede\">Lede</p></main>", html_out)

    def test_multiple_sections(self):
        sections = [
            ("Heading 1", "Body text 1"),
            ("Heading 2", "Body text 2"),
            ("Heading 3", "Body text 3"),
        ]
        html_out = page_html("multi", "Title", "Lede", sections)

        expected_cards = "\n".join(
            f'<section class="card"><h2>{h}</h2><p>{b}</p></section>'
            for h, b in sections
        )
        self.assertIn(expected_cards, html_out)

    def test_raw_html_in_sections(self):
        sections = [
            ("Core pages", '<a href="../index.html">All Craft home</a> · <code>code</code>')
        ]
        html_out = page_html("sitemap", "Sitemap", "Directory", sections)
        self.assertIn('<section class="card"><h2>Core pages</h2><p><a href="../index.html">All Craft home</a> · <code>code</code></p></section>', html_out)

    def test_predefined_content_generation(self):
        for slug, (title, lede, sections) in content.items():
            html_out = page_html(slug, title, lede, sections)
            self.assertIn(f"<title>{title} | All Craft</title>", html_out)
            self.assertIn(f"<h1>{title}</h1>", html_out)


if __name__ == "__main__":
    unittest.main()
