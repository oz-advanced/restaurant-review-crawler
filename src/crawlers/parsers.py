from bs4 import BeautifulSoup, Tag
from typing import Any


class Parser:
    @staticmethod
    def parse_html(html: str) -> BeautifulSoup:
        """
        html text를 BeautifulSoup를 인스턴화 하여 활용합니다

        :param str html: 인스턴스화에 활용할 html text를 입력합니다.
        :return BeautifulSoup:
        """
        return BeautifulSoup(html, 'html.parser')

    @staticmethod
    def get_element(soup: BeautifulSoup, path: str, **kwargs: Any) -> Tag | None:
        """
        주어진 경로에 해당하는 첫 번째 HTML 요소를 찾아 반환합니다.

        :param BeautifulSoup soup: 파싱된 HTML의 BeautifulSoup 객체입니다.
        :param str path: 찾고자 하는 HTML 요소의 경로입니다.
        :param kwargs: 추가적인 필터링 조건을 위한 키워드 인수입니다.
        :return Tag | None: 찾은 HTML 요소 또는 요소가 없을 경우 None을 반환합니다.
        """
        return soup.find(path, **kwargs)

    @staticmethod
    def get_elements(soup: BeautifulSoup, path: str, **kwargs: Any) -> list[Tag] | None:
        """
        주어진 경로에 해당하는 모든 HTML 요소를 찾아 리스트로 반환합니다.

        :param BeautifulSoup soup: 파싱된 HTML의 BeautifulSoup 객체입니다.
        :param str path: 찾고자 하는 HTML 요소의 경로입니다.
        :param kwargs: 추가적인 필터링 조건을 위한 키워드 인수입니다.
        :return list[Tag] | None: 찾은 HTML 요소의 리스트 또는 요소가 없을 경우 None을 반환합니다.
        """
        return soup.find_all(path, **kwargs)
