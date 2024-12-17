
import functools
from block_markdown import block_to_block_type, markdown_to_blocks
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_node_to_html_node, text_to_textnodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    result = []
    for block in blocks:
        result.append(make_node_for_type(block,
            block_to_block_type(block)))
    parent = ParentNode("div", result)
    return parent

def make_node_for_type(block, block_type):
    match block_type:
        case "heading":
            headings = functools.reduce(
                lambda acc, x: acc + x, filter(lambda y: y == "#", block))
            children = block_to_children(block.replace(f"{headings} ", ""))
            return ParentNode(f"h{len(headings)}",children)
        case "quote":
            children = block_to_children(block.replace("> ", ""))
            return ParentNode("blockquote", children)
        case "unordered":
            return make_list(block, "ul", 2)
        case "ordered":
            return make_list(block, "ol", 3)
        case "code":
            children = block_to_children(block[4:-3])
            return ParentNode("pre", [ParentNode("code", children)])
        case "paragraph":
            children = block_to_children(block)
            if len(children)== 0:
                return LeafNode("p", block)
            return ParentNode("p", children=children)
    raise Exception("invalid block type")

def make_list(block, tag, size):
    children = []
    for line in block.split("\n"):
        sub_children = block_to_children(line[size:])
        children.append(ParentNode("li", sub_children))
    return ParentNode(tag, children)

def block_to_children(block):
    nodes = text_to_textnodes(block)
    result = []
    for node in nodes:
        result.append(text_node_to_html_node(node))
    return result

def extract_title(markdown):
    line = list(filter(lambda x: x.startswith("# "), markdown.split("\n")))
    if len(line) == 0:
        raise Exception("no title in markdown")
    return line[0][2:]