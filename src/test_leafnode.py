import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_href(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")

    def test_leaf_to_html_with_href(self):
        node = LeafNode("p", "Hello, world!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<p href="https://www.google.com">Hello, world!</p>')

    def test_no_tag(self):
        node = LeafNode(tag=None, value="Hello, world!")
        self.assertEqual(node.to_html(), 'Hello, world!')

if __name__ == "__main__":
    unittest.main()
