import unittest
from markdown_blocks import(
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
)

class test_markdown_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_multiple_newlines(self):
        md = """
First paragraph with text
More text 



Paragraph after lots of indents
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph with text\nMore text",
                "Paragraph after lots of indents"
            ],
        )

    def test_markdown_to_blocks_no_text(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_starting_newlines(self): 
        md = """


First paragraph starting
More text
some more text


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph starting\nMore text\nsome more text",
            ],
        )
        
    def test_markdown_to_blocks_heading1(self):
        md_block = "# Heading"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_markdown_to_blocks_heading2(self):
        md_block = "### Heading"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_markdown_to_blocks_heading3(self):
        md_block = "####Heading"
        block_type = block_to_block_type(md_block)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_markdown_to_blocks_heading4(self):
        md_block = "###### Heading"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.HEADING)


    def test_markdown_to_blocks_code1(self):
        md_block = """```
Code block with code```"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_markdown_to_blocks_code2(self):
        md_block = """foo```
Code block with code```"""
        block_type = block_to_block_type(md_block)
        self.assertNotEqual(block_type, BlockType.CODE)

    def test_markdown_to_blocks_code3(self):
        md_block = """``
Code block with code```"""
        block_type = block_to_block_type(md_block)
        self.assertNotEqual(block_type, BlockType.CODE)

    def test_markdown_to_blocks_code4(self):
        md_block = """```Code block with code```"""
        block_type = block_to_block_type(md_block)
        self.assertNotEqual(block_type, BlockType.CODE)

    def test_markdown_to_blocks_code5(self):
        md_block = """```
Code block with code``"""
        block_type = block_to_block_type(md_block)
        self.assertNotEqual(block_type, BlockType.CODE)


    def test_markdown_to_blocks_quotes1(self):
        md_block = """>some quoted text
> more text
>     even more text"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_markdown_to_blocks_quotes2(self):
        md_block = """>some quoted text
> more text
>\neven more text"""
        block_type = block_to_block_type(md_block)
        self.assertNotEqual(block_type, BlockType.QUOTE)

    def test_markdown_to_blocks_unordered_list1(self):
        md_block = """- first line
- second line
- third line"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_markdown_to_blocks_unordered_list2(self):
        md_block = """-first line
- second line
- third line"""
        block_type = block_to_block_type(md_block)
        self.assertNotEqual(block_type, BlockType.UNORDERED_LIST)

    def test_markdown_to_blocks_ordered_list1(self):
        md_block = """1. first item
2. second item
3. third item"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_markdown_to_blocks_ordered_list2(self):
        md_block = """1.first item
2.second item
3. third item"""
        block_type = block_to_block_type(md_block)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)

    def test_markdown_to_blocks_ordered_list3(self):
        md_block = """1. first item
2. second item
4. third item"""
        block_type = block_to_block_type(md_block)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)

    def test_markdown_to_blocks_ordered_list4(self):
        md_block = """1.first item 2.second item
3. third item"""
        block_type = block_to_block_type(md_block)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)

    def test_markdown_to_blocks_paragraph1(self):
        md_block = "Just some text"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_markdown_to_blocks_paragraph2(self):
        md_block = "#Just some text"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
