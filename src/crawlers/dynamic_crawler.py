from abc import abstractmethod
import pymysql
from bs4 import Tag

from crawlers import Crawler
from fetchers import DynamicFetcher, Fetcher
from models import (Restaurant, Blog,
                    InsertBlogDto, InsertContentDto)
from models.enums import BlogPlatform
from parsers import Parser
from utils import (ConsoleUtils, GeneralUtils, TimeUtils,
                   NAVER_BLOG_URL, NAVER_BLOG_IFRAME_URL)
from validators import BlogValidator


class DynamicCrawler(Crawler):
    # def __init__(self, parser: Parser, fetcher: DynamicFetcher):
    def __init__(self, parser: Parser, fetcher: Fetcher):
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
        if isinstance(self.fetcher, DynamicFetcher):
            self.fetcher.close()

        ConsoleUtils.print_empty_line()
        ConsoleUtils.print_message("Crawler 종료")
        ConsoleUtils.print_empty_line()


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
            TimeUtils.sleep(1)

            restaurant = self.queue.pop()
            search_url = "{0}{1}".format(NAVER_BLOG_URL, restaurant.name)

            markup = self.fetcher.fetch(endpoint=search_url)
            soup = self.parser.parse(markup=markup)
            body_tag = self.parser.get_body_tag_by_soup(soup=soup)

            review_blog_result_tags = self.parser.get_elements_by_tag(tag=body_tag,
                                                                      path='a',
                                                                      class_='title_link')

            if not review_blog_result_tags:
                # 조회된 블로그 리스트가 없을 경우, 별도의 로깅 처리
                continue

            for review_blog_result_tag in review_blog_result_tags:
                title, href = self.__extract_review_blog_basic_info(review_blog_result_tag)

                insert_blog_dto = InsertBlogDto(
                    restaurant=restaurant,
                    title=title,
                    link=href,
                    blog_platform=BlogPlatform.NAVER  # 일단은 Naver로 하드 코딩
                )

                if not BlogValidator.validate_blog(insert_blog_dto=insert_blog_dto):
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

    def __extract_review_blog_basic_info(self, review_blog_result_tag: Tag) -> tuple[str, str]:
        title = self.parser.get_text_by_tag(tag=review_blog_result_tag)
        href = self.parser.get_attr(element=review_blog_result_tag, key="href")

        if not (title or href):
            raise ValueError("title과 href를 찾을 수 없습니다.")

        return title, href


class RestaurantReviewContentCrawler(DynamicCrawler):
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
            TimeUtils.sleep(1)
            blog = self.queue.pop()

            markup = self.fetcher.fetch(endpoint=blog.link)
            soup = self.parser.parse(markup=markup)
            body_tag = self.parser.get_body_tag_by_soup(soup=soup)

            iframe = self.parser.get_element_by_tag(tag=body_tag, path='iframe', id='mainFrame')

            if not iframe:
                continue

            iframe_src = iframe.get('src')
            blog_content_url = f"{NAVER_BLOG_IFRAME_URL}{iframe_src}"

            iframe_markup = self.fetcher.fetch(endpoint=blog_content_url)
            iframe_soup = self.parser.parse(markup=iframe_markup)
            iframe_body_tag = self.parser.get_body_tag_by_soup(soup=iframe_soup)

            content = self.parser.get_element_by_tag(tag=iframe_body_tag, path='div', class_='se-main-container')

            if content:
                insert_content_dto = InsertContentDto(
                    blog=blog,
                    content=GeneralUtils.clean_text(text=content.text)
                )

                self.__save_content(insert_content_dto=insert_content_dto)

            else:
                continue

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
