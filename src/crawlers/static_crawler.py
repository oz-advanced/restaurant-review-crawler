from abc import abstractmethod

from crawlers import Crawler
from fetchers import Fetcher
from parsers import Parser
from utils import ConsoleUtils


class StaticCrawler(Crawler):
    def __init__(self, parser: Parser, fetcher: Fetcher):
        super().__init__()
        self.parser = parser
        self.fetcher = fetcher

    @abstractmethod
    def initialize(self):
        ...

    @abstractmethod
    def crawl(self):
        ...

    def stop(self):
        ConsoleUtils.print_empty_line()
        ConsoleUtils.print_message("Crawler 종료")
        ConsoleUtils.print_empty_line()


class RestaurantInfoCrawler(StaticCrawler):
    def initialize(self):
        NotImplementedError("not implemented initialize method")

    def crawl(self):
        NotImplementedError("not implemented crawl method")
