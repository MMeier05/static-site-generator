from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag:str | None, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Leaf nodes must have a value!")
        elif self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"Tag: {self.tag}, Value: {self.value}, Props: {self.props}"
