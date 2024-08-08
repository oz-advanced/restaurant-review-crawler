from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from abc import abstractmethod
from fetchers import BaseFetcher


class DynamicFetcher(BaseFetcher):
    @abstractmethod
    def fetch(self, endpoint: str) -> str:
        ...

    @abstractmethod
    def move_page(self, endpoint: str) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...


class SeleniumDynamicFetcher(DynamicFetcher):
    def __init__(self, driver: RemoteWebDriver) -> None:
        self.__driver = driver

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        if self.__driver:
            self.__driver.close()

    def move_page(self, endpoint: str) -> None:
        self.__driver.get(url=endpoint)

    def fetch(self, endpoint: str) -> str:
        self.move_page(endpoint=endpoint)
        return self.__driver.page_source
