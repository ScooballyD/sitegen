import unittest
from markd import (markdown_to_blocks,
                   block_to_block_type,
                   markdown_to_html)

class TestMarkdowntoBlocks(unittest.TestCase):
    def test_output(self):
        node = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        test = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        self.assertEqual(markdown_to_blocks(node), test)
        self.assertEqual(len(markdown_to_blocks(node)), 3)

class TestBlockType(unittest.TestCase):
    def test_heading(self):
        node = "## lots of heading stuff"
        node2 = "####### lots of heading stuff"
        self.assertEqual(block_to_block_type(node), "h2")
        self.assertEqual(block_to_block_type(node2), "p")
    def test_code(self):
        node = "```\nlots of block stuff\n```"
        node2 = "```lots of block stuff``"
        self.assertEqual(block_to_block_type(node), "pre")
        self.assertEqual(block_to_block_type(node2), "p")
    def test_quote(self):
        node = ">lots of block stuff\n>and more"
        node2 = ">lots of block stuff\n#and more"
        node3 = ">should work"
        self.assertEqual(block_to_block_type(node), "blockquote")
        self.assertEqual(block_to_block_type(node2), "p")
        self.assertEqual(block_to_block_type(node3), "blockquote")
    def test_unordered_list(self):
        node = "* lots of block stuff\n* and more"
        node2 = "* lots of block stuff\n= not right"
        node3 = "- stuff\n- and more stuff"
        self.assertEqual(block_to_block_type(node), "ul")
        self.assertEqual(block_to_block_type(node2), "p")
        self.assertEqual(block_to_block_type(node3), "ul")
    def test_ordered_list(self):
        node = "1. lots of block stuff\n2. another line"
        node2 = "a. lots of block stuff\nb. very wrong"
        node3 = "1. lots of block stuff\n3. another line"
        self.assertEqual(block_to_block_type(node), "ol")
        self.assertEqual(block_to_block_type(node2), "p")
        self.assertEqual(block_to_block_type(node3), "p")

class TestMarkdowntoHtml(unittest.TestCase):
    def test_header(self):
        node = """
# this is an h1

this is paragraph text

## this is an h2
"""
        self.assertEqual(markdown_to_html(node).to_html(), "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>")
    def test_paragraph(self):
        node = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""
        self.assertEqual(markdown_to_html(node).to_html(), "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")
    def test_quote(self):
        node = """
> This is a
> blockquote block

this is paragraph text

"""
        self.assertEqual(markdown_to_html(node).to_html(), "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>")
    

if __name__ == "__main__":
    unittest.main()