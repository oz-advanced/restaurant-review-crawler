import datetime

from models.restaurants import Restaurant
from models.enums import BlogPlatform


class Blog:
    def __init__(self,
                 blog_id: int,
                 restaurant: Restaurant,
                 title: str,
                 link: str,
                 link_unique_key: str,
                 blog_platform: BlogPlatform,
                 created_dt: str = datetime.datetime.now().strftime('YYYY-mm-dd HH:MM:ss'),
                 crawled_dt: str | None = None) -> None:
        self._blog_id = blog_id
        self._restaurant = restaurant
        self._title = title
        self._link = link
        self._blog_platform = blog_platform
        self._created_dt = created_dt
        self._crawled_dt = crawled_dt
        self._link_unique_key = link_unique_key

    @property
    def blog_id(self) -> int:
        return self._blog_id

    @property
    def restaurant(self) -> Restaurant:
        return self._restaurant

    @property
    def title(self) -> str:
        return self._title

    @property
    def link(self) -> str:
        return self._link

    @property
    def link_unique_key(self) -> int:
        return self._link_unique_key

    @property
    def blog_platform(self) -> str:
        return self._blog_platform.value()

    @property
    def created_dt(self) -> str:
        return self._created_dt

    @property
    def crawled_dt(self) -> str:
        return self._crawled_dt


class InsertBlogDto:
    def __init__(self,
                 restaurant: Restaurant,
                 title: str,
                 link: str,
                 blog_platform: BlogPlatform) -> None:
        self._restaurant = restaurant
        self._title = title
        self._link = link
        self._blog_platform = blog_platform
        self._link_unique_key = self.__extract_link_unique_key()

    def __extract_link_unique_key(self) -> str:
        return "_".join(self._link.split('/')[-2:])

    @property
    def restaurant(self) -> Restaurant:
        return self._restaurant

    @property
    def title(self) -> str:
        return self._title

    @property
    def link(self) -> str:
        return self._link

    @property
    def link_unique_key(self) -> str:
        return self._link_unique_key

    @property
    def blog_platform(self) -> str:
        return self._blog_platform.value

    # TODO: Dto -> Entity 변환 Static Method 개발
