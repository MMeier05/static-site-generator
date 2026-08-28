import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(props={ "href": "https://www.google.com", "target": "_blank", })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_not_eq(self):
        node = HTMLNode("h1", "some text", props= {"href": "https://www.google.com"})
        node2 = HTMLNode("h2", "some text", props= {"href": "https://www.google.com"})
        self.assertNotEqual(node, node2) 

    def test_eq(self):
        node = HTMLNode("h1", "some text", props= {"href": "https://www.google.com"})
        node2 = HTMLNode("h1", "some text", props= {"href": "https://www.google.com"})
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()


