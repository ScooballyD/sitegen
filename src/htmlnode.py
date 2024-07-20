class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        if self.props == None:
            return ""
        for key, value in self.props.items():
            result = result + (f' {key}="{value}"')
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__()
        self.tag = tag
        self.value = value
        self.props = props
    
    def to_html(self):
        if self.value == None:
            raise ValueError("No value provided")
        if self.tag == None or self.tag == "":
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
         
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__()
        self.children = children
        self.tag = tag
        self.props = props
    
    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("No tag provided")
        if self.children == None or self.children == "":
            raise ValueError("No children provided")
        childsum = ""
        for child in self.children:
            childsum = childsum + child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{childsum}</{self.tag}>"

def make_parent(parent, children):
    return ParentNode(parent, children)

