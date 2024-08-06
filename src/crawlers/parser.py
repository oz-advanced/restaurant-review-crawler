from bs4 import BeautifulSoup, Tag


class Parser:
    def __init__(self, markup: str):
        self.__markup = markup
        self.__soup = self.parse_markup()

    def parse_markup(self) -> BeautifulSoup:
        return BeautifulSoup(self.__markup, 'html.parser')

    def get_element(self, path: str, **kwargs: any) -> Tag | None:
        return self.__soup.find(path, **kwargs)

    def get_elements(self, path: str, **kwargs: any) -> list[Tag] | None:
        return self.__soup.find_all(path, **kwargs)


