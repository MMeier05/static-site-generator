import unittest
from main import extract_title

class TestMain(unittest.TestCase):

    def test_extract_title(self):
        md = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts
"""
        title = extract_title(md)
        self.assertEqual(title, "Tolkien Fan Club")

if __name__ == '__main__':
    unittest.main()
