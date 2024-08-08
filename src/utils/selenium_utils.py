from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from typing import Optional


class SeleniumUtils:
    @staticmethod
    def get_chrome_driver() -> Optional[webdriver.Chrome]:
        try:
            installed_driver_path = ChromeDriverManager().install()
            # installed_driver_path = installed_driver_path.replace("mac64", "mac64_m1")

            driver = webdriver.Chrome(service=ChromeService(installed_driver_path))
            return driver
        except Exception as e:
            print(f"Error getting Chrome driver: {e}")
            return None

    @staticmethod
    def get_firefox_driver() -> Optional[webdriver.Firefox]:
        try:
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            return driver
        except Exception as e:
            print(f"Error getting Firefox driver: {e}")
            return None

    @staticmethod
    def get_edge_driver() -> Optional[webdriver.Edge]:
        try:
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            return driver
        except Exception as e:
            print(f"Error getting Edge driver: {e}")
            return None
