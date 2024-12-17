import unittest

from htmlnode import ParentNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_print(self):
        node = ParentNode("p", [LeafNode("i", "value")], {"prop": "value"})
        expected = "<p prop=\"value\"><i>value</i></p>"
        self.assertEqual(expected, node.to_html())

    def test_nested(self):
        node = ParentNode("p", 
            [ParentNode("a",
                [LeafNode("i", "value")])
            ]
        )
        expected = "<p><a><i>value</i></a></p>"
        self.assertEqual(expected, node.to_html())
    
    def test_empty_tag(self):
        node = ParentNode(None, [LeafNode("i", "value")])
        with self.assertRaises(Exception) as context:
            node.to_html()
        self.assertTrue('Parent node must have a tag.' in str(context.exception))

    def test_empty_children(self):
        node = ParentNode("p", [])
        with self.assertRaises(Exception) as context:
            node.to_html()
        self.assertTrue('Parent node must have a children' in str(context.exception))
        

if __name__ == "__main__":
    unittest.main()