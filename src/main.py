from textnode import TextNode, TextType

def main():
    node = TextNode("some text", TextType.ITALIC, "some url")
    print(node)

if __name__ == "__main__":
    main()
