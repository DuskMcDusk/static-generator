import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node1 = TextNode("dummy", TextType.CODE, "image")
        node2 = TextNode("dummy", TextType.CODE)
        self.assertNotEqual(node1, node2)
    
    def test_eq_none(self):
        node1 = TextNode("dummy", TextType.CODE, None)
        node2 = TextNode("dummy", TextType.CODE)
        self.assertEqual(node1, node2)
    
    

class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_leaf_bold(self):
        node = TextNode("text", TextType.BOLD)
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, "b")
        self.assertEqual(result.value, "text")
    
    def test_leaf_empty(self):
        node = TextNode("text", TextType.TEXT)
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, None)
        self.assertEqual(result.value, "text")
    
    def test_image_node(self):
        node = TextNode("image alt", TextType.IMAGE, "www.image.it")
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, "image")
        self.assertEqual(result.value, "")
        self.assertEqual(
            result.props,
            {"src": "www.image.it", "alt": "image alt"}
        )



if __name__ == "__main__":
    unittest.main()