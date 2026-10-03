import tempfile
import unittest
from pathlib import Path
from scripts.wire_footer_links_text import wire_footer_links


class TestWireFooterLinks(unittest.TestCase):
    def test_wire_footer_links_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            project_dir = tmppath / "projects" / "test-craft"
            project_dir.mkdir(parents=True)
            html_file = project_dir / "index.html"

            sample_html = """<!doctype html>
<html>
<body>
  <footer>
    <a href="#"><i class="fab fa-twitter"></i></a>
    <a href="#"><i class="fas fa-chevron-right me-2"></i>FAQ</a>
    <a href="#">Careers</a>
  </footer>
</body>
</html>"""
            html_file.write_text(sample_html, encoding="utf-8")

            modified_count = wire_footer_links(tmppath)
            self.assertEqual(modified_count, 1)

            updated_text = html_file.read_text(encoding="utf-8")
            self.assertIn('href="https://twitter.com/"', updated_text)
            self.assertIn('href="../../pages/faq.html"', updated_text)
            self.assertIn('href="../../pages/careers.html"', updated_text)

    def test_wire_footer_links_no_placeholders_skipped(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            project_dir = tmppath / "projects" / "test-craft"
            project_dir.mkdir(parents=True)
            html_file = project_dir / "index.html"

            sample_html = """<!doctype html>
<html>
<body>
  <footer>
    <a href="https://twitter.com/"><i class="fab fa-twitter"></i></a>
  </footer>
</body>
</html>"""
            html_file.write_text(sample_html, encoding="utf-8")

            modified_count = wire_footer_links(tmppath)
            self.assertEqual(modified_count, 0)


if __name__ == "__main__":
    unittest.main()
