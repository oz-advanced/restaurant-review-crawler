import requests


class Fetcher:
    @staticmethod
    def fetch_html(url: str) -> str:
        """
        전달받은 url을 기반으로 html의 text를 반환받는다

        :param str url: html을 요청할 url을 입력합니다.
        :return str: 요청한 html의 text를 반환합니다.
        :raise HTTPException: request 요청에서 400 or 500 번대 오류가 발생할 경우 발생합니다.
        """
        response = requests.get(url)
        response.raise_for_status()
        return response.text
