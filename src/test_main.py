import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_output(self):
        node = "# A simple heading\na paragraph\n\nsome text\nso cool"
        node2 = "Random junk at the start\n\n# A simple heading\na paragraph\n\nsome text\nso cool"
        self.assertEqual(extract_title(node), "A simple heading")
        self.assertEqual(extract_title(node2), "A simple heading")


if __name__ == "__main__":
    unittest.main()