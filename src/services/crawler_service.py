from typing import Any

from bs4 import BeautifulSoup, Tag
from utils import NAVER_BLOG_IFRAME_URL

import requests


def __fetch_html(url: str) -> str:
    """
    전달받은 url을 기반으로 html의 text를 반환받는다

    :param str url: html을 요청할 url을 입력합니다.
    :return str: 요청한 html의 text를 반환합니다.
    :raise HTTPException: request 요청에서 400 or 500 번대 오류가 발생할 경우 발생합니다.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def __parse_html(html: str) -> BeautifulSoup:
    """
    html text를 BeautifulSoup를 인스턴화 하여 활용합니다

    :param str html: 인스턴스화에 활용할 html text를 입력합니다.
    :return BeautifulSoup:
    """
    return BeautifulSoup(html, 'html.parser')


def get_soup(url: str) -> BeautifulSoup:
    """
    주어진 URL로부터 HTML을 가져와 BeautifulSoup 객체로 반환합니다.

    :param str url: HTML을 요청할 URL을 입력합니다.
    :return BeautifulSoup: 요청한 HTML을 파싱하여 생성한 BeautifulSoup 객체를 반환합니다.
    :raise HTTPException: 요청 실행 중 오류가 발생할 경우 발생합니다.
    """

    html = __fetch_html(url=url)
    soup = __parse_html(html)

    return soup


def get_element(soup: BeautifulSoup, path: str, **kwargs: Any) -> Tag | None:
    """
    주어진 경로에 해당하는 첫 번째 HTML 요소를 찾아 반환합니다.

    :param BeautifulSoup soup: 파싱된 HTML의 BeautifulSoup 객체입니다.
    :param str path: 찾고자 하는 HTML 요소의 경로입니다.
    :param kwargs: 추가적인 필터링 조건을 위한 키워드 인수입니다.
    :return Tag | None: 찾은 HTML 요소 또는 요소가 없을 경우 None을 반환합니다.
    """
    return soup.find(path, **kwargs)


def get_elements(soup: BeautifulSoup, path: str, **kwargs: Any) -> list[Tag] | None:
    """
    주어진 경로에 해당하는 모든 HTML 요소를 찾아 리스트로 반환합니다.

    :param BeautifulSoup soup: 파싱된 HTML의 BeautifulSoup 객체입니다.
    :param str path: 찾고자 하는 HTML 요소의 경로입니다.
    :param kwargs: 추가적인 필터링 조건을 위한 키워드 인수입니다.
    :return list[Tag] | None: 찾은 HTML 요소의 리스트 또는 요소가 없을 경우 None을 반환합니다.
    """
    return soup.find_all(path, **kwargs)


def get_naver_blog_content(blog_url: str) -> str:
    """
    주어진 네이버 블로그 URL에서 블로그 콘텐츠를 추출하여 반환합니다.

    :param str blog_url: 블로그 콘텐츠를 가져올 네이버 블로그의 URL입니다.
    :return str: 블로그의 메인 콘텐츠를 반환합니다. 콘텐츠가 없을 경우 None을 반환할 수 있습니다.
    """
    soup = get_soup(blog_url)
    iframe = get_element(soup, path='iframe', id='mainFrame')

    if iframe:
        content = get_iframe_content(iframe)
        content = content.replace("\n", "")
        content = content.replace("\u200B", "")
        return content


def get_iframe_content(iframe: Tag) -> str | None:
    """
    주어진 iframe 태그에서 블로그 콘텐츠의 URL을 가져와 콘텐츠를 추출합니다.

    :param Tag iframe: 블로그 콘텐츠가 포함된 iframe 태그입니다.
    :return str | None: iframe에서 추출한 블로그 콘텐츠를 반환합니다. 콘텐츠가 없을 경우 None을 반환합니다.
    """
    iframe_src = iframe.get('src')
    blog_content_url = f"{NAVER_BLOG_IFRAME_URL}{iframe_src}"

    soup = get_soup(blog_content_url)
    content = get_element(soup, path='div', class_='se-main-container')

    if content:
        return content.text
    else:
        return None
