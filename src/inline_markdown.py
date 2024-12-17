import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.IMAGE:
            return LeafNode("image", "", {"src": text_node.url, "alt": text_node.text})
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case _:
           raise Exception("Invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            result.append(node)
            continue
        new_nodes = []
        entries = node.text.split(delimiter)
        if len(entries) % 2 == 0:
            raise Exception("delimiter not matching")
        for i in range(len(entries)):
            if entries[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(entries[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(entries[i], text_type))
        result.extend(new_nodes)
    return result

def extract_markdown_images(text):
    res = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return res

def extract_markdown_links(text):
    res = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return res

def split_nodes_match(old_nodes, extract_text, format_text, node_type):
    result = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            result.append(node)
            continue

        found = extract_text(node.text)

        if len(found) == 0:
            result.append(node)
            continue

        new_nodes = []
        current_text = node.text
        for i in range(len(found)):
            text_found = format_text(found[i]) 
            slices = current_text.split(text_found, 1)
            if slices[0] != "":
                new_nodes.append(TextNode(slices[0], TextType.TEXT))
            new_nodes.append(TextNode(found[i][0], node_type, found[i][1]))
            current_text = slices[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
        
        result.extend(new_nodes)
    return result

def split_nodes_image(old_nodes):
    format_text = lambda entry: f"![{entry[0]}]({entry[1]})"
    return split_nodes_match(
        old_nodes, extract_markdown_images, format_text, TextType.IMAGE)

def split_nodes_link(old_nodes):
    format_text = lambda entry: f"[{entry[0]}]({entry[1]})"
    return split_nodes_match(
        old_nodes, extract_markdown_links, format_text, TextType.LINK)

def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)

    text_node = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    text_node = split_nodes_delimiter(text_node, "*", TextType.ITALIC)
    text_node = split_nodes_delimiter(text_node, "`", TextType.CODE)
    text_node = split_nodes_link(text_node)
    text_node = split_nodes_image(text_node)

    return text_node