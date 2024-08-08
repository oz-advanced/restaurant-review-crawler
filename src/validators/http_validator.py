import requests
from requests import HTTPError


class HttpValidator:
    @staticmethod
    def validate_endpoint(endpoint: str) -> bool:
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            return True
        except HTTPError:
            return False
        except not HTTPError:
            raise ValueError("Value Error")
