from abc import ABC, abstractmethod
from utils import ValidateUtil

import requests


class Fetcher(ABC):
    def __init__(self, endpoint: str) -> None:
        self.__endpoint = endpoint

    @property
    def endpoint(self):
        return self.__endpoint

    @abstractmethod
    def fetch(self, **kwargs: any) -> str:
        ...


class RequestsFetcher(Fetcher):
    def __init__(self, endpoint: str) -> None:
        super().__init__(endpoint)

    def fetch(self, **kwargs: any) -> str:
        ValidateUtil.validate_endpoint(self.__endpoint)
        return requests.get(url=self.__endpoint, **kwargs).text

