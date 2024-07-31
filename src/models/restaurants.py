from models.enums import RestaurantCuisineType


class Restaurant:
    def __init__(self,
                 restaurant_id: int,
                 name: str,
                 branch: None | str = None,
                 cuisine_type: None | RestaurantCuisineType = None,
                 crawled_dt: None | str = None) -> None:
        self._restaurant_id = restaurant_id
        self._name = name
        self._branch = branch
        self._cuisine_type = cuisine_type
        self._crawled_dt = crawled_dt

    @property
    def restaurant_id(self) -> int:
        return self._restaurant_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def branch(self) -> str:
        return self._branch

    @property
    def cuisine_type(self) -> str:
        return self._cuisine_type.value()

    @property
    def crawled_dt(self) -> str:
        return self._crawled_dt
