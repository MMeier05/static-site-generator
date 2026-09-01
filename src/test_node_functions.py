import unittest
from textnode import TextNode, TextType
from leafnode import LeafNode
from node_functions import (
    text_node_to_html_node, 
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    )

class TestNodeFunctions(unittest.TestCase):
    #Testing text_node_to_html_node
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

    #Testing split_nodes_delimiter
    def test_split_middle(self):
        node = TextNode("This _is_ text with a italic words word", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC).__repr__()
        self.assertEqual(new_nodes,"[TextNode(This , plain, None), TextNode(is, italic, None), TextNode( text with a italic words word, plain, None)]")

    def test_split_middle_multiple(self):
        node = TextNode("This _is_ _some_ text", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC).__repr__()
        self.assertEqual(new_nodes, "[TextNode(This , plain, None), TextNode(is, italic, None), TextNode( , plain, None), TextNode(some, italic, None), TextNode( text, plain, None)]")

    def test_split_only_one_word(self):
        node = TextNode("_some_", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC).__repr__()
        self.assertEqual(new_nodes, "[TextNode(some, italic, None)]")

    def test_split_at_start(self):
        node = TextNode("_some_ text", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC).__repr__()
        self.assertEqual(new_nodes, "[TextNode(some, italic, None), TextNode( text, plain, None)]")

    def test_split_at_end(self):
        node = TextNode("some _text_", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC).__repr__()
        self.assertEqual(new_nodes, "[TextNode(some , plain, None), TextNode(text, italic, None)]")

    def test_multiple_nodes(self):
        node = TextNode("some **text**", TextType.TEXT, None)
        node2 = TextNode("foo **bar**", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD).__repr__()
        self.assertEqual(new_nodes, "[TextNode(some , plain, None), TextNode(text, bold, None), TextNode(foo , plain, None), TextNode(bar, bold, None)]")
    
    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"**", TextType.BOLD)
        self.assertListEqual([], new_nodes)

    #Testing extract_markdown_images
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_string(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links2(self):
        matches = extract_markdown_links(
            "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links_empty_string(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_wrong_syntax(self):
        matches = extract_markdown_links("some text ![link1](https://link1.com) and [image1](https://link2.png)")
        self.assertListEqual(
            [("image1", "https://link2.png")], matches
        )

    #Testing split_nodes_image
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_images_no_text(self):
        node = TextNode(
            "![image1](https://link1.png)![image2](https://link2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://link1.png"),
                TextNode("image2", TextType.IMAGE, "https://link2.png"),
            ],
            new_nodes,
        )

    def test_split_images_text_at_end(self):
        node = TextNode(
            "![image1](https://link1.png)![image2](https://link2.png) some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://link1.png"),
                TextNode("image2", TextType.IMAGE, "https://link2.png"),
                TextNode(" some text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_image_no_images(self):
        node = TextNode("just some text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("just some text", TextType.TEXT)], new_nodes
        )

    def test_split_image_wrong_synax(self):
        node = TextNode(
            "some text [link1](https://link1.com) and ![image1](https://link2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("some text [link1](https://link1.com) and ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://link2.png"),
            ],
            new_nodes,
        )
    
    def test_split_image_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [], new_nodes
        )
    #Testing split_nodes_link
    def test_split_link(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_link_no_text(self):
        node = TextNode(
            "[image1](https://link1.png)[image2](https://link2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.LINK, "https://link1.png"),
                TextNode("image2", TextType.LINK, "https://link2.png"),
            ],
            new_nodes,
        )
    def test_split_link_no_images(self):
        node = TextNode("just some text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("just some text", TextType.TEXT)], new_nodes
        )

    def test_split_link_wrong_synax(self):
        node = TextNode(
            "some text ![link1](https://link1.com) and [image1](https://link2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("some text ![link1](https://link1.com) and ", TextType.TEXT),
                TextNode("image1", TextType.LINK, "https://link2.png"),
            ],
            new_nodes,
        )
    
    def test_split_link_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [], new_nodes
        )

if __name__ == "__main__":
    unittest.main()
