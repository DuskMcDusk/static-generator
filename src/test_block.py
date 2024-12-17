import unittest

from block_markdown import block_to_block_type, markdown_to_blocks
from htmlnode import LeafNode, ParentNode
from markdown import markdown_to_html_node
from textnode import TextNode, TextType


class TestMarkdownBlock(unittest.TestCase):
    def test_eq(self):
        text = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""
        result = markdown_to_blocks(text)
        self.assertTrue(len(result) == 3)

class TestMarkdownConversion(unittest.TestCase):

    def test_block_matches(self):
        text =[
            ("# This is a heading", "heading"),
            ("""This is a paragraph of text. It has some **bold** 
             and *italic* words inside of it.""", "paragraph"),
            ("""* This is the first list item in a list block
- This is a list item
* This is another list item""", "unordered"),
            ("```code block```", "code"),
            ("""1. one
2. two
3. three""", "ordered"),
            ("> unordered", "quote")
        ]
        for entry in text:
            result = block_to_block_type(entry[0])
            self.assertEqual(result, entry[1])

class TextMarkdownToHTML(unittest.TestCase):
    def test_markdown_match(self):
        text = "# This is a heading\n\n" \
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n" \
            "* This is the first list item in a list block\n" \
            "* This is a list item\n" \
            "* This is another list item"
        result = markdown_to_html_node(text)
        expected = ParentNode("div",[
                ParentNode("h1", [LeafNode(None,"This is a heading")]),
                ParentNode("p", [
                            LeafNode(None,"This is a paragraph of text. It has some "),
                            LeafNode("b","bold"), 
                            LeafNode(None, " and "), 
                            LeafNode("i", "italic"),
                            LeafNode(None, " words inside of it."),
                        ]),
                ParentNode("ul", [
                    ParentNode("li", [LeafNode(None, "This is the first list item in a list block")]),
                    ParentNode("li", [LeafNode(None, "This is a list item")]),
                    ParentNode("li", [LeafNode(None, "This is another list item")])
                ])
            ])
        
        self.assertEqual(result, expected)

    def test_headings(self):
        text = "# a"
        result = markdown_to_html_node(text)
        expected = ParentNode("div", [
            ParentNode("h1", [LeafNode(None, "a")])
        ])
        self.assertEqual(result, expected)
   
if __name__ == "__main__":
    unittest.main()
