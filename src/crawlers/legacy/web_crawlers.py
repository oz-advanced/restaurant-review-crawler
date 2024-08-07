from abc import ABCMeta, abstractmethod
from collections import deque
# from threading import Thread
from time import sleep

import pymysql.err
from bs4 import Tag

from fetchers.fetcher import Fetcher
from crawlers.legacy.parsers import Parser

from databases import DBManager

from models import (Restaurant,
                    Blog, InsertBlogDto,
                    InsertContentDto)
from models.enums import BlogPlatform
from utils import NAVER_BLOG_URL, NAVER_BLOG_IFRAME_URL

import re


class Crawler(metaclass=ABCMeta):
    def __init__(self,
                 parser: Parser = Parser,
                 fetcher: Fetcher = Fetcher,
                 max_threads: int = 5) -> None:
        self.queue = deque()
        self.db_manager = DBManager()
        self.parser = parser
        self.fetcher = fetcher
        self.max_threads = max_threads

    @abstractmethod
    def initialize(self):
        ...

    @abstractmethod
    def crawl(self):
        ...

    def start(self):
        self.initialize()
        self.crawl()

        # threads = []
        #
        # for _ in range(self.max_threads):
        #     thread = Thread(target=self.crawl)
        #     thread.start()
        #     threads.append(thread)
        #
        # for thread in threads:
        #     thread.join()

    def stop(self):
        print("Crawler is shutting down.")

    def run(self):
        try:
            self.start()
        finally:
            self.stop()


class RestaurantInfoCrawler(Crawler):
    def __init__(self):
        super().__init__()

    def initialize(self):
        # 어디서 정보 가여
        pass

    def crawl(self):
        pass


class ReviewBlogInfoCrawler(Crawler):
    def __init__(self):
        super().__init__()

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

    @staticmethod
    def __extract_review_blog_basic_info(review_blog_result: Tag) -> tuple[str, str]:
        # 과연 이렇게 활용하는게 확장성에 유라힐 것인가 고민
        """
        review_blog_result에서 title, href 속성을 확인하여 결과를 반환한다.

        :param review_blog_result:
        :return:
        """
        title = review_blog_result.get_text()
        href = review_blog_result.get('href')

        if not title or not href:
            raise ValueError()

        return title, href

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


class BlogContentCrawler(Crawler):
    def __init__(self):
        super().__init__()

    def initialize(self):

        sql = """
        SELECT b.blog_id, b.restaurant_id, b.title, b.link, b.link_unique_key, b.blog_platform, b.crawled_dt, 
        r.name, r.branch, r.cuisine_type, r.created_dt, r.crawled_dt
        from blog b
        inner join restaurant r on b.restaurant_id = r.restaurant_id
        where b.crawled_dt is null
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
                crawled_dt=result.get('r.crawled_dt')
            )

            blog = Blog(
                blog_id=result.get('blog_id'),
                restaurant=restaurant,
                title=result.get('title'),
                link=result.get('link'),
                link_unique_key=result.get('link_unique_key'),
                blog_platform=result.get('blog_platform'),
                crawled_dt=result.get('crawled_dt')
            )

            self.queue.append(blog)

    def crawl(self):
        while self.queue:
            sleep(1)
            blog = self.queue.pop()

            fetch_html = self.fetcher.fetch_html(endpoint=blog.link)
            parsed_html = self.parser.parse_html(html=fetch_html)

            iframe = self.parser.get_element(soup=parsed_html,
                                             path='iframe',
                                             id='mainFrame')

            if not iframe:
                continue

            iframe_src = iframe.get('src')
            blog_content_url = f"{NAVER_BLOG_IFRAME_URL}{iframe_src}"

            fetch_iframe_html = self.fetcher.fetch_html(endpoint=blog_content_url)
            parsed_iframe_html = self.parser.parse_html(html=fetch_iframe_html)

            content = self.parser.get_element(soup=parsed_iframe_html,
                                              path='div',
                                              class_='se-main-container')

            if content:
                insert_content_dto = InsertContentDto(
                    blog=blog,
                    content=self.__clean_text(text=content.text)
                )

                self.__save_content(insert_content_dto=insert_content_dto)

            else:
                continue

    @staticmethod
    def __clean_text(text) -> str:
        text = text.replace('\u200b', '')

        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def __save_content(self, insert_content_dto):
        insert_sql = """
                insert into content (restaurant_id, blog_id, content)
                values (%s, %s, %s)
                """

        params = (
            insert_content_dto.blog.restaurant.restaurant_id,
            insert_content_dto.blog.blog_id,
            insert_content_dto.content
        )

        self.db_manager.insert_data(query=insert_sql, params=params)


if __name__ == '__main__':
    crawler = ReviewBlogInfoCrawler()
    crawler.initialize()
    crawler.crawl()
