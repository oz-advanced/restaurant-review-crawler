from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver():
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        return driver
    except Exception as e:
        print(e.__traceback__)
