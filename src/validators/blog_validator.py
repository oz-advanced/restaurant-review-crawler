from utils import GeneralUtils
from models import InsertBlogDto
import re


class BlogValidator:
    @staticmethod
    def validate_blog(insert_blog_dto: InsertBlogDto) -> bool:
        v_title_result = BlogValidator.validate_blog_title(insert_blog_dto.restaurant.name, insert_blog_dto.title)
        v_link_result = BlogValidator.validate_blog_link(insert_blog_dto.link)

        return GeneralUtils.all_true(v_title_result, v_link_result)

    @staticmethod
    def validate_blog_title(restaurant_name: str, title: str) -> bool:
        return restaurant_name in title

    @staticmethod
    def validate_blog_link(link: str) -> bool:
        return bool(re.search(r'blog\.naver\.com', link))
