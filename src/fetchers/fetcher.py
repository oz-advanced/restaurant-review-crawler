from abc import ABC, abstractmethod, ABCMeta
from validators import HttpValidator

import requests


class BaseFetcher(metaclass=ABCMeta):
    ...


class Fetcher(BaseFetcher):
    @staticmethod
    @abstractmethod
    def fetch(**kwargs: any) -> str:
        ...


class RequestsFetcher(Fetcher):
    @staticmethod
    def fetch(endpoint: str, **kwargs: any) -> str:
        HttpValidator.validate_endpoint(endpoint)
        return requests.get(url=endpoint, **kwargs).text
