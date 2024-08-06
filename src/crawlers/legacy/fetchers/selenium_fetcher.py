from selenium import webdriver

from crawlers.fetchers import Fetcher
from utils import get_chrome_driver, ValidateUtil


class SeleniumFetcher(Fetcher):
    def __init__(self):
        self.fetcher: webdriver.Chrome = get_chrome_driver()

    def __del__(self):
        self.fetcher.close()

    def fetch_html(self, endpoint: str) -> str:
        if ValidateUtil.validate_endpoint(endpoint=endpoint):
            self.fetcher.get(endpoint)
            return self.fetcher.page_source
