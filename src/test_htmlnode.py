import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_format(self):
        props = {"a": "avalue"}
        node = HTMLNode("tag", "value", props= props)
        expected = " a=\"avalue\""
        self.assertEqual(expected, node.props_to_html())
    
    def test_format_empty(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())
    
    def test_props_more_values(self):
        props = {
            "a": "avalue", 
            "b": "bvalue",
            "c": "cvalue",
            "d": "dvalue",
        }
        node = HTMLNode("tag", "value", props= props)
        expected = " a=\"avalue\" b=\"bvalue\" c=\"cvalue\" d=\"dvalue\""
        self.assertEqual(expected, node.props_to_html())

class TestLeafNode(unittest.TestCase):
    def test_value_props(self):
        node = LeafNode("p", "value", {"prop": "prop value"})
        expected = "<p prop=\"prop value\">value</p>"
        self.assertEqual(expected, node.to_html())
    
    def test_no_props(self):
        node = LeafNode("p", "value")
        expected = "<p>value</p>"
        self.assertEqual(expected, node.to_html())
    
    def test_no_value(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)
    
    def test_no_tag(self):
        node = LeafNode(None, "value")
        expected = "value"
        self.assertEqual(expected, node.to_html())
    
    

if __name__ == "__main__":
    unittest.main()