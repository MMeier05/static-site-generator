import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode

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

    #Parentnode tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child", props={ "href": "https://www.google.com", "target": "_blank", })
        parent_node = ParentNode("div", [child_node], props={ "href": "https://www.google.com", "target": "_blank", })
        self.assertEqual(parent_node.to_html(), 
                         '<div href="https://www.google.com" target="_blank"><span href="https://www.google.com" target="_blank">child</span></div>'
                         )
        
    def test_nested_parents(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("a",[child_node])
        child_node.children.append(parent_node)
        self.assertEqual(parent_node.to_html(), "<a><span><b>grandchild</b></span></a>")

    def test_no_children(self):
        parent_node = ParentNode("a",[])
        self.assertEqual(parent_node.to_html(), "<a></a>")

    #Leafnode tests
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


