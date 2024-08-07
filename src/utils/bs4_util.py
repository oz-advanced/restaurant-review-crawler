from bs4.element import Tag


def is_tag(obj: object) -> bool:
    return isinstance(obj, Tag)
