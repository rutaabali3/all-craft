import unittest
import tempfile
import shutil
from pathlib import Path
from scripts.wire_footer_links_text import wire_footer_links


class TestWireFooterLinks(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.projects_dir = self.temp_dir / "projects"
        self.projects_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_wire_footer_links_replacement(self):
        project_dir = self.projects_dir / "sample-craft"
        project_dir.mkdir()
        html_file = project_dir / "index.html"

        sample_html = (
            '<html><body>'
            '<a href="#"><i class="fab fa-facebook-f"></i></a>'
            '<a href="#"><i class="fas fa-chevron-right me-2"></i>Careers</a>'
            '<a href="#">FAQ</a>'
            '</body></html>'
        )
        html_file.write_text(sample_html, encoding='utf-8')

        # Temporarily patch ROOT in wire_footer_links_text module
        import scripts.wire_footer_links_text as wfl
        original_root = wfl.ROOT
        try:
            wfl.ROOT = self.temp_dir
            wire_footer_links()
        finally:
            wfl.ROOT = original_root

        result_html = html_file.read_text(encoding='utf-8')
        self.assertIn('https://www.facebook.com/', result_html)
        self.assertIn('target="_blank"', result_html)
        self.assertIn('../../pages/careers.html', result_html)
        self.assertIn('../../pages/faq.html', result_html)
        self.assertNotIn('href="#"', result_html)

    def test_wire_footer_links_no_dummy_links(self):
        project_dir = self.projects_dir / "already-wired"
        project_dir.mkdir()
        html_file = project_dir / "index.html"

        wired_html = '<html><body><a href="https://example.com">Link</a></body></html>'
        html_file.write_text(wired_html, encoding='utf-8')

        import scripts.wire_footer_links_text as wfl
        original_root = wfl.ROOT
        try:
            wfl.ROOT = self.temp_dir
            wire_footer_links()
        finally:
            wfl.ROOT = original_root

        result_html = html_file.read_text(encoding='utf-8')
        self.assertEqual(result_html, wired_html)


if __name__ == '__main__':
    unittest.main()
