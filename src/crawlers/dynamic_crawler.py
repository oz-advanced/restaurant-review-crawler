import re
from abc import abstractmethod
from time import sleep

import pymysql
from bs4 import Tag

from crawlers import Crawler
from fetchers import DynamicFetcher
from models import Restaurant, InsertBlogDto
from models.enums import BlogPlatform
from parsers import Parser
from utils import ConsoleUtil, NAVER_BLOG_URL


class DynamicCrawler(Crawler):
    def __init__(self, parser: Parser, fetcher: DynamicFetcher):
        super().__init__()
        self.parser = parser
        self.fetcher = fetcher

    @abstractmethod
    def initialize(self):
        ...

    @abstractmethod
    def crawl(self):
        ...

    def stop(self):
        self.fetcher.close()
        ConsoleUtil.print_empty_line()
        ConsoleUtil.print_message("Crawler 종료")
        ConsoleUtil.print_empty_line()


class RestaurantReviewBlogInfoCrawler(DynamicCrawler):
    def initialize(self):
        sql = """
        SELECT restaurant_id, name, branch, cuisine_type, crawled_dt
        from restaurant
        where date_add(crawled_dt, interval 30 day) < NOW() or crawled_dt is null
        """
        results = self.db_manager.execute_query(query=sql)

        if not results:
            return

        for result in results:
            restaurant = Restaurant(
                restaurant_id=result.get('restaurant_id'),
                name=result.get('name'),
                branch=result.get('branch'),
                cuisine_type=result.get('cuisine_type'),
                crawled_dt=result.get('crawled_dt'),
            )

            self.queue.append(restaurant)

    def crawl(self):
        while self.queue:
            sleep(1)

            restaurant = self.queue.pop()
            search_url = "{0}{1}".format(NAVER_BLOG_URL, restaurant.name)

            fetch_html = self.fetcher.fetch_html(endpoint=search_url)
            parsed_html = self.parser.parse_html(html=fetch_html)

            review_blog_results = self.parser.get_elements(soup=parsed_html, path='a', class_='title_link')

            if not review_blog_results:
                # 조회된 블로그 리스트가 없을 경우, 별도의 로깅 처리
                continue

            for review_blog_result in review_blog_results:
                title, href = self.__extract_review_blog_basic_info(review_blog_result)

                insert_blog_dto = InsertBlogDto(
                    restaurant=restaurant,
                    title=title,
                    link=href,
                    blog_platform=BlogPlatform.NAVER  # 일단은 Naver로 하드 코딩
                )

                if not self.__validate_blog(insert_blog_dto=insert_blog_dto):
                    # 유효성 검사에 통과하지 못한 경우 넘어감
                    continue

                self.__save_review_blog(insert_blog_dto)

    def __save_review_blog(self, insert_blog_dto: InsertBlogDto) -> None:
        try:
            insert_sql = """
                    insert into blog (restaurant_id, title, link, link_unique_key, blog_platform)
                    values (%s, %s, %s, %s, %s)
                    """

            params = (
                insert_blog_dto.restaurant.restaurant_id,
                insert_blog_dto.title,
                insert_blog_dto.link,
                insert_blog_dto.link_unique_key,
                insert_blog_dto.blog_platform
            )

            self.db_manager.insert_data(query=insert_sql, params=params)
        except pymysql.err.IntegrityError as ie:
            print(ie)

    def __extract_review_blog_basic_info(self, review_blog_result) -> tuple[str, str]:
        title = self.parser.get_text_by_tag(review_blog_result)
        href = self.parser.get_attr_by_tag(review_blog_result, "href")

        if not (title or href):
            raise ValueError("title과 href를 찾을 수 없습니다.")

        return title, href

    # TODO: Validate 기능 별도 Util
    def __validate_blog(self, insert_blog_dto: InsertBlogDto) -> bool:
        v_title_result = self.__validate_blog_title(insert_blog_dto.restaurant.name, insert_blog_dto.title)
        v_link_result = self.__validate_blog_link(insert_blog_dto.link)

        return v_title_result and v_link_result

    @staticmethod
    def __validate_blog_title(restaurant_name: str, title: str) -> bool:
        return restaurant_name in title

    @staticmethod
    def __validate_blog_link(link: str) -> bool:
        if not re.search(r'blog\.naver\.com', link):
            return False

        return True


class RestaurantReviewContentCrawler(DynamicCrawler):
    def initialize(self):
        pass

    def crawl(self):
        pass
