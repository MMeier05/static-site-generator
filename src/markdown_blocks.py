from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from node_functions import text_to_textnodes, text_node_to_html_node
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    new_strings = markdown.split("\n\n")
    new_strings = map(lambda string: string.strip(), new_strings)
    filtered_strings = list(filter(lambda string: string, new_strings))
    return filtered_strings

def block_to_block_type(md_block: str) -> BlockType:

    hashtag_cnt = md_block.count('#', 0, 6)
    if 7 > hashtag_cnt > 0:
        if md_block[hashtag_cnt] == ' ':
            return BlockType.HEADING
    
    if md_block.startswith("```\n") and md_block.endswith("```"):
        return BlockType.CODE

    quotes = md_block.split("\n")
    is_quote_block = True
    for quote in quotes:
        if not quote.startswith(">"):
            is_quote_block = False
    if is_quote_block:
        return BlockType.QUOTE

    u_list = md_block.split("\n")
    is_unordered_list = True
    for line in u_list:
        if not line.startswith("- "):
            is_unordered_list = False
    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    o_list = md_block.split("\n")
    is_o_list = True
    for num, index in enumerate(o_list, start=1):
        if not index.startswith(str(num) + '. '):
            is_o_list = False
    if is_o_list:
        return BlockType.ORDERED_LIST
    #Base case
    return BlockType.PARAGRAPH

def ul_block_to_nodes(block: str) -> ParentNode:
    u_list = block.replace("\n", "").split("- ")
    nodes: list[list[TextNode]] = []
    for elem in u_list[1:]:
        nodes.append(text_to_textnodes(elem))
    children = []
    for node in nodes:
        p_node = ParentNode("li", list(map(text_node_to_html_node, node)))
        children.append(p_node)
    return ParentNode("ul", children)

def ol_block_to_nodes(block: str) -> ParentNode:
    block = block.replace("\n", "")
    o_list = re.split(r"\d{1}. ", block)
    nodes: list[list[TextNode]] = []
    for elem in o_list[1:]:
        nodes.append(text_to_textnodes(elem))
    children = []
    for node in nodes:
        p_node = ParentNode("li", list(map(text_node_to_html_node, node)))
        children.append(p_node)
    return ParentNode("ol", children)

def quote_block_to_nodes(block) -> ParentNode:
    quote_list = block.replace("\n", "").split("> ")
    node_list = []
    for quote in quote_list:
        nodes = text_to_textnodes(quote)
        if nodes:
            node_list.append(nodes)
    children = []
    for node in node_list:
        if len(node) > 1:
            p_node = ParentNode(None, list(map(text_node_to_html_node, node)))
            children.append(p_node)
        else:
            html_node = text_node_to_html_node(node[0])
            children.append(html_node)
    return ParentNode("blockquote", children)

def code_block_to_nodes(block: str) -> ParentNode:
    text = block[4:-3]
    child = LeafNode("code", text)
    parent = ParentNode("pre", [child])
    return parent

def paragraph_block_to_nodes(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    nodes = text_to_textnodes(paragraph)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return ParentNode("p", children)

def heading_block_to_nodes(block: str) -> ParentNode:
    hashtag_cnt = block.count('#', 0, 6)
    child = LeafNode("h"+ str(hashtag_cnt), block.strip("#"*hashtag_cnt + " "))
    return child

def markdown_to_html_node(markdown: str) -> ParentNode:
    md_blocks = markdown_to_blocks(markdown)
    children = []
    for block in md_blocks:
        b_type = block_to_block_type(block)
        match b_type:
            case BlockType.PARAGRAPH:
                children.append(paragraph_block_to_nodes(block))
            case BlockType.HEADING:
                children.append(heading_block_to_nodes(block))
            case BlockType.CODE:
                children.append(code_block_to_nodes(block))
            case BlockType.QUOTE:
                children.append(quote_block_to_nodes(block))
            case BlockType.UNORDERED_LIST:
                children.append(ul_block_to_nodes(block))
            case BlockType.ORDERED_LIST:
                children.append(ol_block_to_nodes(block))

    return ParentNode("div", children)
