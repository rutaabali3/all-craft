import unittest
from scripts.build_image_manifest import clean

class TestBuildImageManifest(unittest.TestCase):
    def test_clean(self):
        # Happy paths
        self.assertEqual(clean("  Hello World  "), "Hello World")
        self.assertEqual(clean("Hello\tWorld"), "Hello World")
        self.assertEqual(clean("Hello\nWorld"), "Hello World")
        self.assertEqual(clean("Hello   World"), "Hello World")

        # Edge cases
        self.assertEqual(clean(None), "")
        self.assertEqual(clean(""), "")
        self.assertEqual(clean("   "), "")
        self.assertEqual(clean("\t\n\r"), "")

if __name__ == '__main__':
    unittest.main()
