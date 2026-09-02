from enum import Enum

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
