import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_no_prop(self):
        node = HTMLNode("1", "2", "3")
        node.__repr__()
    def test_no_val(self):
        node = HTMLNode(tag="1", children="3", props={"5": "6"})
        node.__repr__()
    def test_not_eq(self):
        node = HTMLNode("1", "2", "3", {"5": "6"})
        node2 = HTMLNode("1","A","3", {"5": "6"})
        self.assertNotEqual(node,node2)
    def test_prop_to_html(self):
        node = HTMLNode("tag", "val", "child", {"key": "prop"})
        node.props_to_html()
    def test_prop_to_html2(self):
        node = HTMLNode("tag", "val", "child", {
        "href": "https://www.google.com", 
        "target": "_blank",
        })
        node.props_to_html()

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph")
        node.to_html()
    def test_to_html2(self):
        node = LeafNode("a", "Click Me!", {"href": "https://www.google.com"})
        node.to_html()
    def test_to_html3(self):
        node = LeafNode(None, "Plain Text")
        node.to_html()
    def test_no_value(self):
        node = LeafNode("p","")
        self.assertRaises(ValueError, node.to_html)

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node.to_html()
    def test_to_html2(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text", {"href": "https://www.google.com"}),
            ],
        )
        node.to_html()
    def test_to_html3(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text", {"href": "https://www.google.com"}),
            ], {"Pprop": "https://www.parent.com"}
        )
        node.to_html()
    def test_no_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text", {"href": "https://www.google.com"}),
            ],
        )
        self.assertRaises(ValueError, node.to_html)
    def test_no_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)
    def test_no_childval(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", None),
                LeafNode(None, "Normal text", {"href": "https://www.google.com"}),
            ],
        )
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()