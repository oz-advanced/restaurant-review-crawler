from abc import ABC, abstractmethod
from collections import deque

from databases import DBManager


class Crawler(ABC):
    def __init__(self):
        self.queue = deque()
        self.db_manager = DBManager()

    @abstractmethod
    def initialize(self):
        ...

    @abstractmethod
    def crawl(self):
        ...

    @abstractmethod
    def stop(self):
        ...

    def run(self):
        try:
            self.initialize()
            self.crawl()
        finally:
            self.stop()
