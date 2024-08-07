from abc import ABC, abstractmethod


class Fetcher(ABC):
    @abstractmethod
    def fetch_html(self, endpoint: str) -> str:
        ...
