import requests

from fetchers.fetcher import Fetcher
from utils import ValidateUtil


class RequestsFetcher(Fetcher):
    def __init__(self):
        self.fetcher: requests = requests

    def fetch_html(self, endpoint: str) -> str:
        if ValidateUtil.validate_endpoint(endpoint=endpoint):
            return self.fetcher.get(endpoint).text
