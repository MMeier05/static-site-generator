import unittest
from textnode import TextNode, text_node_to_html_node, TextType
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("Some text", TextType.BOLD, "https://google.com")
        node2 = TextNode("Some other text", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode("Some text", TextType.ITALIC, "https://google.com")
        node2 = TextNode("Some text", TextType.CODE, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq3(self):
        node = TextNode("Some text", TextType.CODE)
        node2 = TextNode("Some text", TextType.CODE, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")

    def test_code(self):
        node = TextNode("This is a image node", TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "This is a image node")

    def test_invalid(self):
        node = TextNode("This node has no valid type", None)
        self.assertRaises(Exception, text_node_to_html_node, node)

if __name__ == "__main__":
    unittest.main()
