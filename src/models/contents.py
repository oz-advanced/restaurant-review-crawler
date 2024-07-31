from models import Restaurant, Blog
import datetime


class Content:
    def __init__(self,
                 content_id: int,
                 restaurant: Restaurant,
                 blog: Blog,
                 content: str = None,
                 create_dt: str = datetime.datetime.now().strftime('YYYY-mm-dd HH:MM:ss')) -> None:
        self._content_id = content_id
        self._restaurant = restaurant
        self._blog = blog
        self._content = content
        self._create_dt = create_dt

    @property
    def content_id(self) -> int:
        return self._content_id

    @property
    def restaurant(self) -> Restaurant:
        return self._restaurant

    @property
    def blog(self) -> Blog:
        return self._blog

    @property
    def content(self) -> str | None:
        return self._content

    @property
    def create_dt(self) -> str:
        return self._create_dt

    def set_content(self, content: str):
        self._content = content


class InsertContentDto:
    def __init__(self,
                 blog: Blog,
                 content: str = None) -> None:
        self._blog = blog
        self._content = content

    @property
    def blog(self) -> Blog:
        return self._blog

    @property
    def content(self) -> str | None:
        return self._content
