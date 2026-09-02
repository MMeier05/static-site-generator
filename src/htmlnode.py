class HTMLNode:

    def __init__(
            self,
            tag: str | None = None,
            value: str | None = None,
            children: list[HTMLNode] | None = None ,
            props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> Exception:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        html_str = ""
        if self.props:
            for key, value in self.props.items():
                html_str += " " + f'{key}="{value}"'
        return html_str

    def __repr__(self) -> str:
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"

    def __eq__(self, other: TextNode) -> bool:
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str | Exception:
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        if self.children is None:
            raise ValueError("Parent node must have children")
        conc_children = ""
        for child in self.children:
            if type(child) == ParentNode and self in child.children:
                child.children.remove(self)
            conc_children += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{conc_children}</{self.tag}>"

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
