
import functools

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None: return ""
        format_string = lambda x: f" {x[0]}=\"{x[1]}\""
        aggregate_entries = lambda acc, s: acc + s
        return functools.reduce(
            aggregate_entries, map(
                format_string,
                self.props.items()
            )
        )
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props}, {self.children})"
    
    def __eq__(self, value):
        return (
            self.tag == value.tag and self.value == value.value
            and self.props == value.props and self.children == value.children
        )
    
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value.")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag.")
        if not self.children:
            raise ValueError("Parent node must have a children")
        
        result = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        return result