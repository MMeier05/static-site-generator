from htmlnode import HTMLNode

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
