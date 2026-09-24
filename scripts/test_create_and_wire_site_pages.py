import unittest
from scripts.create_and_wire_site_pages import page_html, content


class TestPageHtml(unittest.TestCase):
    def test_basic_structure(self):
        slug = "test-slug"
        title = "Test Title"
        lede = "This is a test lede."
        sections = [("Section 1", "Body text 1"), ("Section 2", "Body text 2")]

        html_out = page_html(slug, title, lede, sections)

        self.assertTrue(html_out.startswith("<!doctype html>"))
        self.assertIn("<html lang=\"en\">", html_out)
        self.assertIn("<title>Test Title | All Craft</title>", html_out)
        self.assertIn("<link rel=\"stylesheet\" href=\"styles.css\">", html_out)
        self.assertIn("<h1>Test Title</h1>", html_out)
        self.assertIn('<p class="lede">This is a test lede.</p>', html_out)

    def test_html_escaping(self):
        title = "Title <with> & 'special' \"chars\""
        lede = "Lede <with> & 'special' \"chars\""
        sections = [("Heading", "Body")]

        html_out = page_html("escape-test", title, lede, sections)

        self.assertIn("Title &lt;with&gt; &amp; &#x27;special&#x27; &quot;chars&quot;", html_out)
        self.assertIn("Lede &lt;with&gt; &amp; &#x27;special&#x27; &quot;chars&quot;", html_out)
        self.assertNotIn("<with>", html_out)

    def test_card_generation(self):
        sections = [
            ("Heading One", "Body One"),
            ("Heading Two", "Body Two"),
        ]

        html_out = page_html("cards-test", "Title", "Lede", sections)

        expected_card1 = '<section class="card"><h2>Heading One</h2><p>Body One</p></section>'
        expected_card2 = '<section class="card"><h2>Heading Two</h2><p>Body Two</p></section>'

        self.assertIn(expected_card1, html_out)
        self.assertIn(expected_card2, html_out)

    def test_empty_sections(self):
        sections = []
        html_out = page_html("empty-test", "Title", "Lede", sections)

        self.assertNotIn('<section class="card">', html_out)
        self.assertIn('<main class="container"><div class="eyebrow">All Craft information</div><h1>Title</h1><p class="lede">Lede</p></main>', html_out)

    def test_predefined_content_generation(self):
        import html
        for slug, (title, lede, sections) in content.items():
            html_out = page_html(slug, title, lede, sections)
            escaped_title = html.escape(title)
            self.assertIn(f"<title>{escaped_title} | All Craft</title>", html_out)
            self.assertIn(f"<h1>{escaped_title}</h1>", html_out)
            for heading, body in sections:
                self.assertIn(f"<h2>{heading}</h2>", html_out)


if __name__ == "__main__":
    unittest.main()
