import unittest

from textnode import (TextNode, 
                      text_node_to_html_node, 
                      split_nodes_delimiter, 
                      extract_markdown_images, 
                      extract_markdown_links, 
                      split_nodes_link, 
                      split_nodes_image,
                      text_to_textnodes)


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

class TestTextNodetoHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("Sample Text", "text")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, None)
        leaf.to_html()
    def test_bold(self):
        node = TextNode("Sample Text", "bold")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "b")
        leaf.to_html()
    def test_italic(self):
        node = TextNode("Sample Text", "italic")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "i")
        leaf.to_html()
    def test_code(self):
        node = TextNode("Sample Text", "code")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "code")
        leaf.to_html()
    def test_link(self):
        node = TextNode("Sample Text", "link", "https://www.scoob.com")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "a")
        leaf.to_html()
    def test_image(self):
        node = TextNode("Sample Text", "image", "https://www.scoob.com")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "img")
        self.assertEqual(leaf.props, {"src": "https://www.scoob.com", "alt": "Sample Text"})
        leaf.to_html()
    def test_type_not_valid(self):
        node = TextNode("Sample Text", "cat")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

class TestSplitNodesDelim(unittest.TestCase):
    def test_bold(self):
        node = TextNode("Some text with **bold** in the middle.", "text")
        test = [TextNode("Some text with ", "text"), TextNode("bold", "bold"), TextNode(" in the middle.", "text")]
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(new_nodes, test)
    def test_code(self):
        node = TextNode("Some text with `code` in the middle.", "text")
        test = [TextNode("Some text with ", "text"), TextNode("code", "code"), TextNode(" in the middle.", "text")]
        new_nodes = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(new_nodes, test)
    def test_italic(self):
        node = TextNode("Some text with *italic* in the middle.", "text")
        test = [TextNode("Some text with ", "text"), TextNode("italic", "italic"), TextNode(" in the middle.", "text")]
        new_nodes = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(new_nodes, test)
    def test_multi_type(self):
        node = TextNode("Some text with **bold** in the middle", "text")
        node1 = TextNode("===This is bold.===", "bold")
        node2 = TextNode("More text with `code` in it", "text")
        test = [
                TextNode("Some text with ", "text"),
                TextNode("bold", "bold"), 
                TextNode(" in the middle", "text"), 
                TextNode("===This is bold.===", "bold"), 
                TextNode("More text with `code` in it", "text")
                ]
        new_nodes = split_nodes_delimiter([node, node1, node2], "**", "bold")
        self.assertEqual(new_nodes, test)
    def test_invalid_markdown(self):
        node = TextNode("Some text with **bold in the middle", "text")
        with self.assertRaises(Exception):
            split_nodes_delimiter([node])

class test_markdown_extract(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        test = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), test)
    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        test = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), test)

class TestSplitImageLink(unittest.TestCase):
    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to scoob](https://www.scoob.com) and [to twitter](https://www.twitter.com)",
            "text"
        )
        node2 = TextNode(
            "This is text with a link [to scoob](https://www.scoob.com) and some text after",
            "text"
        )
        test = [
            TextNode("This is text with a link ", "text", None), 
            TextNode("to scoob", "link", "https://www.scoob.com"), 
            TextNode(" and ", "text", None), 
            TextNode("to twitter", "link", "https://www.twitter.com")
        ]
        test2 = [
            TextNode("This is text with a link ", "text", None), 
            TextNode("to scoob", "link", "https://www.scoob.com"), 
            TextNode(" and some text after", "text", None)
        ]
        self.assertEqual(split_nodes_link([node]), test)
        self.assertEqual(split_nodes_link([node2]), test2)
    def test_split_image(self):
        node = TextNode(
            "This is text with a link ![to scoob](https://www.scoob.com) and ![to twitter](https://www.twitter.com)",
            "text"
        )
        node2 = TextNode(
            "This is text with a link ![to scoob](https://www.scoob.com) and some text after",
            "text"
        )
        test = [
            TextNode("This is text with a link ", "text", None), 
            TextNode("to scoob", "image", "https://www.scoob.com"), 
            TextNode(" and ", "text", None), 
            TextNode("to twitter", "image", "https://www.twitter.com")
        ]
        test2 = [
            TextNode("This is text with a link ", "text", None), 
            TextNode("to scoob", "image", "https://www.scoob.com"), 
            TextNode(" and some text after", "text", None)
        ]
        self.assertEqual(split_nodes_image([node]), test)
        self.assertEqual(split_nodes_image([node]), test)
    def test_no_url(self):
        node = [TextNode("Just some text", "text")]
        self.assertEqual(split_nodes_link(node), node)
        self.assertEqual(split_nodes_image(node), node)
        nodes = [
            TextNode("Just some text", "text"), 
            TextNode(
            "This is text with a link [to scoob](https://www.scoob.com) and some text after",
            "text")
            ]
        test = [
            TextNode("Just some text", "text"), 
            TextNode("This is text with a link ", "text", None), 
            TextNode("to scoob", "link", "https://www.scoob.com"), 
            TextNode(" and some text after", "text", None)
        ]
        self.assertEqual(split_nodes_link(nodes), test)
        nodes2 = [
            TextNode("Just some text", "text"), 
            TextNode(
            "This is text with a link ![to scoob](https://www.scoob.com) and some text after",
            "text")
            ]
        test2 = [
            TextNode("Just some text", "text"), 
            TextNode("This is text with a link ", "text", None), 
            TextNode("to scoob", "image", "https://www.scoob.com"), 
            TextNode(" and some text after", "text", None)
        ]
        self.assertEqual(split_nodes_image(nodes2), test2)

class TestTexttoTextnodes(unittest.TestCase):
    def variety_test(self):
        node = [TextNode("This is **bold** text with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://scoob.com)", "text")]
        test = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://scoob.com"),
        ]
        self.assertEqual(text_to_textnodes(node), test)
    def invalid_markdown_test(self):
        node = [TextNode("This is *bold** text with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://scoob.com)", "text")]
        node2 = [TextNode("This is **bold** text with an italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://scoob.com)", "text")]
        node3 = [TextNode("This is **bold** text with an *italic* word and a code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://scoob.com)", "text")]
        with self.assertRaises(Exception):
            text_to_textnodes(node)
            text_to_textnodes(node2)
            text_to_textnodes(node3)
    

if __name__ == "__main__":
    unittest.main()
