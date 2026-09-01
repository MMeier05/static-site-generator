from textnode import TextNode, TextType
from leafnode import LeafNode
import re

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, None)
        case TextType.IMAGE:
            return LeafNode("img", text_node.text, None)
        case _:
            raise Exception("Not a valid type")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            converted_nodes = []
            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
                converted_nodes.append(TextNode(split_text[i], TextType.TEXT if i % 2 == 0 else text_type))
            new_nodes.extend(converted_nodes)
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        image_text = node.text
        delimiters = extract_markdown_images(image_text)
        if not image_text:
            continue
        if not delimiters:
            new_nodes.append(node)
            continue
        for delimiter in delimiters:
            image_alt, image = delimiter
            image_text = image_text.split(f"![{image_alt}]({image})", 1)
            first_part = image_text.pop(0)
            if first_part:
                new_nodes.append(TextNode(first_part, TextType.TEXT, None))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image))
            rest = image_text.pop(0)
            image_text = rest
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        link_text = node.text
        delimiters = extract_markdown_links(link_text)
        if not link_text:
            continue
        if not delimiters:
            new_nodes.append(node)
            continue
        for delimiter in delimiters:
            link_alt, link = delimiter
            link_text = link_text.split(f"[{link_alt}]({link})", 1)
            first_part = link_text.pop(0)
            if first_part:
                new_nodes.append(TextNode(first_part, TextType.TEXT, None))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link))
            rest = link_text.pop(0)
            link_text = rest
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    alt_text = re.findall(r"!\[(.*?)\]", text)
    link = re.findall(r"!\[.*?\]\((.*?)\)", text)
    return list(zip(alt_text, link))

def extract_markdown_links(text: str) -> list[tuple]:
    alt_text = re.findall(r"(?<!!)\[(.*?)\]", text)
    link = re.findall(r"(?<!!)\[.*?\]\((.*?)\)", text)
    return list(zip(alt_text, link))

def text_to_textnodes(text: str) -> list[TextNode]:
    pass
