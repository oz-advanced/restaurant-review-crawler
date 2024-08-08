from crawlers import (RestaurantInfoCrawler,
                      RestaurantReviewBlogInfoCrawler, RestaurantReviewContentCrawler)
from fetchers import RequestsFetcher, SeleniumDynamicFetcher
from utils import SeleniumUtils
from parsers import Parser


class CrawlApplication:
    def __init__(self):
        self.ric = generate_restaurant_info_crawler()
        self.rrbic = generate_restaurant_review_blog_info_crawler()
        self.rrcc = generate_restaurant_review_content_crawler()

    def run(self):
        self.ric.run()
        self.rrbic.run()
        self.rrcc.run()


# TODO: 해당 generate function들은 추후 CrawlerFactory로 한번에 처리 변경
def generate_restaurant_info_crawler() -> RestaurantInfoCrawler:
    parser = Parser()
    fetcher = RequestsFetcher()

    return RestaurantInfoCrawler(
        parser=parser,
        fetcher=fetcher
    )


def generate_restaurant_review_blog_info_crawler() -> RestaurantReviewBlogInfoCrawler:
    parser = Parser()
    fetcher = RequestsFetcher()
    # fetcher = SeleniumDynamicFetcher(driver=SeleniumUtils.get_chrome_driver())

    return RestaurantReviewBlogInfoCrawler(
        parser=parser,
        fetcher=fetcher
    )


def generate_restaurant_review_content_crawler() -> RestaurantReviewContentCrawler:
    parser = Parser()
    fetcher = RequestsFetcher()
    # fetcher = SeleniumDynamicFetcher(driver=SeleniumUtils.get_chrome_driver())

    return RestaurantReviewContentCrawler(
        parser=parser,
        fetcher=fetcher
    )
