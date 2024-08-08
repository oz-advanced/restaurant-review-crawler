import re


class GeneralUtils:
    @staticmethod
    def all_true(*args: bool) -> bool:
        """
        모든 인자가 True인지 확인합니다.

        :param args: 검증 결과를 나타내는 불리언 값들.
        :return: 모든 인자가 True이면 True를 반환하고, 하나라도 False이면 False를 반환합니다.
        """
        return all(args)

    @staticmethod
    def clean_text(text) -> str:
        text = text.replace('\u200b', '')

        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\s+', ' ', text)

        return text.strip()
