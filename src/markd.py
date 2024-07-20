from htmlnode import (make_parent)
from textnode import (TextNode,
                      text_to_textnodes,
                      text_node_to_html_node)

def markdown_to_blocks(markdown):
    blocks =  markdown.split("\n\n")
    result = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        result.append(block)
    return result

def block_to_block_type(block):
    i = 0
    lines = block.split("\n")
    if block.startswith("# "):
        return "h1"
    if block.startswith("## "):
        return "h2"
    if block.startswith("### "):
        return "h3"
    if block.startswith("#### "):
        return "h4"
    if block.startswith("##### "):
        return "h5"
    if block.startswith("###### "):
        return "h6"
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "pre"
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "p"
        return "blockquote"
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return "p"
        return "ul"
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return "p"
        return "ul"
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return "p"
            i += 1
        return "ol"
    return "p"

def text_to_child(text, tag):
    if tag == "h1":
        child = text.replace("# ", "")
        return TextNode(f"{child}", "text")
    if tag == "h2":
        child = text.replace("## ", "")
        return TextNode(f"{child}", "text")
    if tag == "h3":
        child = text.replace("### ", "")
        return TextNode(f"{child}", "text")
    if tag == "h4":
        child = text.replace("#### ", "")
        return TextNode(f"{child}", "text")
    if tag == "h5":
        child = text.replace("##### ", "")
        return TextNode(f"{child}", "text")
    if tag == "h6":
        child = text.replace("###### ", "")
        return TextNode(f"{child}", "text")
    if tag == "pre":
        child = text.replace("```", "")
        return TextNode(f"<code>{child}</code>", "text")
    if tag == "blockquote":
        lines = text.split("\n")
        child = ""
        for line in lines:
            child = child + " " + line.replace("> ", "")
        return TextNode(f"{child.strip()}", "text")
    if tag == "ul":
        lines = text.split("\n")
        child = ""
        if lines[0].startswith("*"):
            for line in lines:
                child = child + line.replace("* ", "<li>", 1) + "</li>"
        if lines[0].startswith("-"):
            for line in lines:
                child = child + line.replace("- ", "<li>", 1) + "</li>"
        return TextNode(f"{child}", "text")
    if tag == "ol":
        lines = text.split("\n")
        child = ""
        i = 1
        for line in lines:
            child = child + line.replace(f"{i}. ", "<li>") + "</li>"
            i += 1
        return TextNode(f"{child}", "text")
    if tag == "p":
        lines = text.split("\n")
        child = ""
        for line in lines:
            child = child + " " + line
        return TextNode(child.strip(), "text")
        



def markdown_to_html(markdown):
    parents = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        child = []
        type = block_to_block_type(block)
        tnode = text_to_textnodes([text_to_child(block, type)])
        for node in tnode:
            child.append(text_node_to_html_node(node))
        parents.append(make_parent(type, child))
    root = make_parent("div", parents)
    return root

