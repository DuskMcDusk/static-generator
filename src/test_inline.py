import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_node_to_html_node, text_to_textnodes
from textnode import TextNode, TextType


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

class TestTextNodeSplit(unittest.TestCase):

    def test_split_nomatches(self):
        node = TextNode("simple text", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual([node], result)
    
    def test_split_notext(self):
        node = TextNode("simple text", TextType.BOLD)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual([node], result)

    def test_split_notext(self):
        node = TextNode("simple bold", TextType.BOLD)
        node2 = TextNode("node *with* bold", TextType.TEXT)
        expected = [
            node, 
            TextNode("node ", TextType.TEXT),
            TextNode("with", TextType.BOLD),
            TextNode(" bold", TextType.TEXT)
        ]
        result = split_nodes_delimiter([node, node2], "*", TextType.BOLD)
        self.assertEqual(expected, result)
    
    def test_split_starts_with(self):
        node = TextNode("simple bold", TextType.BOLD)
        node2 = TextNode("*node* with bold", TextType.TEXT)
        expected = [
            node, 
            TextNode("node", TextType.BOLD),
            TextNode(" with bold", TextType.TEXT)
        ]
        result = split_nodes_delimiter([node, node2], "*", TextType.BOLD)
        self.assertEqual(expected, result)
    
    def test_split_not_matching(self):
        node = TextNode("node *without matching bold", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "*", TextType.BOLD)

        self.assertTrue("delimiter not matching" in str(context.exception))

class TestAltUrlExtraction(unittest.TestCase):
    
    def test_matches(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected)
    
    def test_link_matches(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result =extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(result, expected)

class TestImageNodeSplit(unittest.TestCase):

    def test_match_single(self):
        text = TextNode("![image](www.image.it)", TextType.TEXT)
        result = split_nodes_image([text])
        expected = [TextNode("image", TextType.IMAGE, "www.image.it")]
        self.assertEqual(result, expected)
    
    def test_match_multi(self):
        text = TextNode("![image](www.image.it) other ![image2](www.image2.it) exe", TextType.TEXT)
        result = split_nodes_image([text])
        expected = [
            TextNode("image", TextType.IMAGE, "www.image.it"),
            TextNode(" other ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "www.image2.it"),
            TextNode(" exe", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_no_match_single(self):
        text = TextNode("[image](www.image.it)", TextType.TEXT)
        result = split_nodes_image([text])
        expected = [TextNode("[image](www.image.it)", TextType.TEXT)]
        self.assertEqual(result, expected)
    
    def test_match_last(self):
        text = TextNode(" other ![image2](www.image2.it)", TextType.TEXT)
        result = split_nodes_image([text])
        expected = [
            TextNode(" other ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "www.image2.it")
        ]
        self.assertEqual(result, expected)
    
    def test_match_link(self):
        text = TextNode("[link](www.image.it) other [link2](www.image2.it)", TextType.TEXT)
        result = split_nodes_link([text])
        expected = [
            TextNode("link", TextType.LINK, "www.image.it"),
            TextNode(" other ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "www.image2.it")
        ]
        self.assertEqual(result, expected)

class TestTextSplitToNodes(unittest.TestCase):

    def test_text_is_split(self):
        result = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)
    
    def test_bold_begin(self):
        result = text_to_textnodes("**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)")
        self.assertEqual(result[0].text_type, TextType.BOLD)