import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()