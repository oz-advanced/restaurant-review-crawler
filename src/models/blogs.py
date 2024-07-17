class Blog:
    def __init__(self, title: str, link: str, content: str = None) -> None:
        self._title = title
        self._link = link
        self._content = content

    @property
    def title(self) -> str:
        return self._title

    @property
    def link(self) -> str:
        return self._link

    @property
    def content(self) -> str | None:
        return self._content

    def set_content(self, content: str):
        self._content = content

