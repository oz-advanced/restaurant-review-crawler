from services import get_soup, get_elements, get_naver_blog_content
from models.blogs import Blog
from databases import DBManager
from utils import RESTAURANT_LIST, NAVER_BLOG_URL
import time


soup_dict = {}
blog_dict = {}


def main():
    db_manager = DBManager()

    # 최초 식당 이름 별 식당 검색 URL 생성
    print("start to generate url")
    for r in RESTAURANT_LIST:
        url = NAVER_BLOG_URL + r
        soup_dict[r] = url

    # 식당 dict에 정보를 채워주는 로직
    print("start to full dict")
    for r_name, r_url in soup_dict.items():
        print(f"running {r_name}")

        # 중간 중단부
        # if r_name == "쟈니덤플링":
        #     break

        blog_list = []

        soup = get_soup(r_url)
        results = get_elements(soup=soup, path='a', class_='title_link')
        for result in results:
            title = result.get_text()
            href = result.get('href')

            blog = Blog(title=title, link=href)
            blog_list.append(blog)

            if len(blog_list) >= 30:
                break

        blog_dict[r_name] = blog_list
        time.sleep(1)

    print("start to full blog")
    for r_name, blog_list in blog_dict.items():
        for blog in blog_list:
            print(f"running {r_name, blog.title}")
            content = get_naver_blog_content(blog.link)

            if not content:
                print(f"pass blog name {blog.title}")
                continue

            blog.set_content(content=content)

            query = "insert into blog (title, link, content) values (%s, %s, %s)"
            values = (blog.title, blog.link, blog.content)

            # db에 데이터 저장
            db_manager.insert_data(query=query, params=values)

    print(blog_dict)


if __name__ == "__main__":
    main()
