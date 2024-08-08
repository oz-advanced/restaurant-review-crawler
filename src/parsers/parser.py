from bs4 import BeautifulSoup, Tag
from typing import Optional, List, Union


class Parser:
    @staticmethod
    def parse(markup: str, features: str = "html.parser") -> BeautifulSoup:
        """
        주어진 HTML 마크업 문자열을 파싱하여 BeautifulSoup 객체를 반환합니다.

        :param str markup: 파싱할 HTML 콘텐츠.
        :param str features: 사용할 파서의 종류. 기본값은 "html.parser".
        :return: 파싱된 BeautifulSoup 객체.
        """
        return BeautifulSoup(markup, features)

    @staticmethod
    def get_body_tag_by_soup(soup: BeautifulSoup) -> Optional[Tag]:
        """
        주어진 BeautifulSoup 객체에서 <body> 태그를 반환합니다.

        :param BeautifulSoup soup: 검색할 BeautifulSoup 객체.
        :return: <body> 태그가 있으면 반환하고, 없으면 None을 반환합니다.
        """
        return Parser.get_element_by_soup(soup, selector="body")

    @staticmethod
    def get_element_by_soup(soup: BeautifulSoup, selector: str) -> Optional[Tag]:
        """
        주어진 CSS 선택자와 일치하는 첫 번째 요소를 BeautifulSoup 객체에서 반환합니다.

        :param BeautifulSoup soup: 검색할 BeautifulSoup 객체.
        :param str selector: 일치할 CSS 선택자.
        :return: 첫 번째 일치하는 요소가 있으면 반환하고, 없으면 None을 반환합니다.
        """
        return soup.select_one(selector)

    @staticmethod
    def get_elements_by_soup(soup: BeautifulSoup, selector: str) -> Optional[List[Tag]]:
        """
        주어진 CSS 선택자와 일치하는 모든 요소를 BeautifulSoup 객체에서 반환합니다.

        :param BeautifulSoup soup: 검색할 BeautifulSoup 객체.
        :param str selector: 일치할 CSS 선택자.
        :return: 모든 일치하는 요소의 리스트를 반환하고, 없으면 빈 리스트를 반환합니다.
        """
        return soup.select(selector)

    @staticmethod
    def get_element_by_tag(tag: Tag, path: str, **kwargs: any) -> Optional[Tag]:
        """
        주어진 태그 이름과 추가 필터와 일치하는 첫 번째 요소를 반환합니다.

        :param Tag tag: 검색할 부모 태그.
        :param str path: 일치할 태그 이름.
        :param any kwargs: 검색을 필터링할 추가 키워드 인자.
        :return: 첫 번째 일치하는 요소가 있으면 반환하고, 없으면 None을 반환합니다.
        """
        return tag.find(name=path, **kwargs)

    @staticmethod
    def get_elements_by_tag(tag: Tag, path: str, **kwargs: any) -> Optional[List[Tag]]:
        """
        주어진 태그 이름과 추가 필터와 일치하는 모든 요소를 반환합니다.

        :param Tag tag: 검색할 부모 태그.
        :param str path: 일치할 태그 이름.
        :param any kwargs: 검색을 필터링할 추가 키워드 인자.
        :return: 모든 일치하는 요소의 리스트를 반환하고, 없으면 빈 리스트를 반환합니다.
        """
        return tag.find_all(name=path, **kwargs)

    @staticmethod
    def get_text_by_tag(tag: Tag) -> str:
        """
        주어진 BeautifulSoup 객체에서 텍스트 콘텐츠를 추출하여 반환합니다.

        :param tag: 텍스트를 추출할 Tag 객체.
        :return: 추출된 텍스트 콘텐츠.
        """
        return tag.getText()

    @staticmethod
    def get_attr(element: Union[BeautifulSoup, Tag], key: str) -> Optional[str]:
        """
        주어진 속성 키의 값을 BeautifulSoup 객체에서 반환합니다.

        :param Union[BeautifulSoup, Tag] element: 속성을 가져올 BeautifulSoup 객체.
        :param str key: 값을 가져올 속성 키.
        :return: 속성 값이 있으면 반환하고, 없으면 None을 반환합니다.
        """
        if not element.has_attr(key):
            return None

        return element.__getitem__(key=key)
