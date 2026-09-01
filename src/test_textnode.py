import unittest
from textnode import TextNode, TextType
from leafnode import LeafNode
from node_functions import text_node_to_html_node


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


if __name__ == "__main__":
    unittest.main()
