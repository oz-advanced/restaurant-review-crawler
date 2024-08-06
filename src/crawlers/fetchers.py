from abc import ABC, abstractmethod

import requests

from utils import ValidateUtil


class Fetcher(ABC):
    def __init__(self, endpoint: str) -> None:
        self.__endpoint = endpoint

    @property
    def endpoint(self):
        return self.__endpoint

    @abstractmethod
    def fetch(self, **kwargs: any) -> str:
        ...


class DynamicFetcher(Fetcher):
    def __init__(self, endpoint: str, driver: any):
        super().__init__(endpoint=endpoint)
        self.__driver = driver

    @abstractmethod
    def move_page(self, endpoint: str) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...


class RequestsFetcher(Fetcher):
    def __init__(self, endpoint: str) -> None:
        super().__init__(endpoint)

    def fetch(self, **kwargs: any) -> str:
        ValidateUtil.validate_endpoint(self.__endpoint)
        return requests.get(url=self.__endpoint, **kwargs).text


class SeleniumDynamicFetcher(DynamicFetcher):
    def __init__(self, endpoint: str, driver: any):
        super().__init__(endpoint, driver)

    def __del__(self):
        self.close()

    def close(self) -> None:
        if self.__driver:
            self.__driver.close()

    def set_endpoint(self, endpoint: str):
        self.__endpoint = endpoint

    def move_page(self, endpoint: str = None) -> None:
        if endpoint:
            self.__driver.get(url=endpoint)
        self.__driver.get(url=self.__endpoint)

    def fetch(self, **kwargs: any) -> str:
        if kwargs.get("endpoint"):
            self.move_page(endpoint=kwargs.get("endpoint"))
        else:
            self.move_page()
        return self.__driver.page_source
