from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class Crawler(ABC):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    @abstractmethod
    def fetch(self) -> str:
        ...

    @staticmethod
    def parse_to_bs4(html_content: str) -> BeautifulSoup:
        return BeautifulSoup(html_content, "html.parser")


class StaticCrawler(Crawler):
    def __init__(self, endpoint: str):
        super().__init__(endpoint=endpoint)

    @abstractmethod
    def fetch(self) -> str:
        ...

    @abstractmethod
    def _get_element(self):
        ...

    @abstractmethod
    def _get_elements(self):
        ...

    @abstractmethod
    def get_attribute_value(self, attribute, element) -> str:
        ...


class DynamicCrawler(StaticCrawler):
    @abstractmethod
    def load_page(self):
        ...

    @abstractmethod
    def fetch(self) -> str:
        ...

    @abstractmethod
    def _get_element(self):
        ...

    @abstractmethod
    def _get_elements(self):
        ...

    @abstractmethod
    def get_attribute_value(self, attribute, element) -> str:
        ...
