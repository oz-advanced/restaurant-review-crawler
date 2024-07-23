from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
ChromeDriverManager().install()

browser = webdriver.Chrome()
browser.get("https://product.kyobobook.co.kr/detail/S000001865118")
browser.find_element(By.CLASS_NAME, 'ico_arw').click()

RESTAURANT_NAME_LIST = browser.find_elements(By.CLASS_NAME, 'book_contents_item')

texts = []

for element in RESTAURANT_NAME_LIST :
    html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')

    #스트링을 기준으로 나누기
    for part in soup.stripped_strings :
        texts.append(part.replace(part[0:4], ''))


# 리스트를 파이썬 코드 형식으로 변환
list_as_string = repr(texts)

with open('./src/utils/__init__.py', 'a') as file :
    file.write(f'RESTAURANT_LIST = {list_as_string}')
