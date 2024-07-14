import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "https://www.scoob.com")
        node2 = TextNode("This is a text node", "bold", "https://www.scoob.com")
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode("1", "2", "3")
        node2 = TextNode("1","2","3")
        self.assertEqual(node, node2)
    def test_no_url(self):
        node = TextNode("1", "2", None)
        node.__repr__()
    def test_not_eq(self):
        node = TextNode("1", "2", "3")
        node2 = TextNode("1","A","3")
        self.assertNotEqual(node,node2)

if __name__ == "__main__":
    unittest.main()
