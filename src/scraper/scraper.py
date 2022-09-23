from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from src.scraper.utils import get_timestamp_now, get_domain_name_from_url


class Scraper:
    def __init__(self, url: str):
        self.__url = url
        self.__medium_name = get_domain_name_from_url(url)
        self.__driver = webdriver.Firefox()
        self.__driver.get(self.__url)

    def load_more_articles(
        self, iterations: int = 1, load_more_button: str = "btn-load-more"
    ):
        print("scraper: starting to load the articles")
        latest_button = self.__driver.find_element(By.CLASS_NAME, load_more_button)
        error_counter = 0

        for i in range(iterations):
            sleep(.5)
            if i % 5 == 0:
                print(f"scraper: {i}/{iterations}")
            try:
                latest_button.click()
            except ElementClickInterceptedException:
                error_counter += 1
                print(
                    f"scraper: fuck the element click intercepted exception! ({error_counter})"
                )
                continue

        print(
            f"scraper: {error_counter} out of {iterations} iterations went wrong {':c' if error_counter else ':)'}"
        )

    def save_page(self, name: str = None):
        page_source = self.__driver.page_source

        if name is None:
            timestamp = get_timestamp_now()
            name = f"saved_pages/{self.__medium_name}_{timestamp}.html"

        with open(name, "w") as file:
            file.write(page_source)

        print(f"scraper: the file was saved here: {name}")
        self.__driver.close()
        return name
