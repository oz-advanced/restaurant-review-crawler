from crawlers.web_crawlers import RestaurantInfoCrawler

if __name__ == '__main__':
    ResInfo = RestaurantInfoCrawler()
    ResInfo.save_file(ResInfo.sorted_items())