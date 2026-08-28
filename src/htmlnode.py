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
