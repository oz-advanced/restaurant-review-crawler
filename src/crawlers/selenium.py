from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
ChromeDriverManager().install()

from crawlers.parsers import Parser


class SeleniumCrawler:
    def __init__(self, url: str, click_cls_name: str):
        """
        :param url: 'https://product.kyobobook.co.kr/detail/S000001865118'
        :param click_cls_name: 'ico_arw'
        """
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.driver.find_element(By.CLASS_NAME, click_cls_name).click()

    def get_items(self, cls_name: str) -> list:
        """
        :param cls_name: 'book_contents_item'
        :return: list
        """
        items = self.driver.find_elements(By.CLASS_NAME, cls_name)

        return items

    @staticmethod
    def sort_items(get_items: list):
        """
        get_items 메소드로 가져온 items를 정렬하는 메소드
        :param get_items: list
        :return: list
        """
        items = get_items
        sorted_items = []

        for element in items:
            html = element.get_attribute('outerHTML')
            soup = Parser.parse_html(html)

            # 스트링을 기준으로 나누기
            for part in soup.stripped_strings:
                sorted_items.append(part.replace(part[0:4], ''))

        sorted_items = repr(sorted_items)

        return sorted_items

