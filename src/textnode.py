from htmlnode import LeafNode
import re

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    if text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    if text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    if text_node.text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception("Text type not valid")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type == "text":
            splits = (node.text.split(delimiter))
            if len(splits) % 2 == 0:
                raise Exception("Invalid Markdown syntax")
            for i in range(0, len(splits)):
                if i == 0 or (i % 2) == 0:
                    result.append(TextNode(splits[i], "text"))
                else:
                    result.append(TextNode(splits[i], text_type))
        else:
            result.append(node)
    return result

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        splits = [node.text]
        links = extract_markdown_links(node.text)
        if links == []:
            result.append(node)
        else:
            for i in range(0, len(links)):
                splits = splits[i].split(f"[{links[i][0]}]({links[i][1]})")
                for split in splits:
                    if extract_markdown_links(split) == [] and split != "":
                        result.append(TextNode(split, "text"))
                    if TextNode(links[i][0], "link", links[i][1]) not in result:
                        result.append(TextNode(links[i][0], "link", links[i][1]))
    return result
def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        splits = [node.text]
        links = extract_markdown_images(node.text)
        if links == []:
            result.append(node)
        else:
            for i in range(0, len(links)):
                splits = splits[i].split(f"![{links[i][0]}]({links[i][1]})")
                for split in splits:
                    if extract_markdown_images(split) == [] and split != "":
                        result.append(TextNode(split, "text"))
                    if TextNode(links[i][0], "image", links[i][1]) not in result:
                        result.append(TextNode(links[i][0], "image", links[i][1]))
    return result

def text_to_textnodes(text):
    result = split_nodes_delimiter(text, "**", "bold")
    result = split_nodes_delimiter(result, "*", "italic")
    result = split_nodes_delimiter(result, "`", "code")
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    return result

        