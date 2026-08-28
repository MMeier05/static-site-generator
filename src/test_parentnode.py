import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):

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

if __name__ == "__main__":
    unittest.main()
