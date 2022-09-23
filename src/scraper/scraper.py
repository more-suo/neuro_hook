from time import sleep
from datetime import datetime
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException


class Scraper:
    def __init__(self, url: str):
        self.__url = url
        self.__medium_name = urlparse(self.__url).netloc.replace(".", "-")
        self.__driver = webdriver.Firefox()
        self.__driver.get(self.__url)

    def load_more_articles(
        self, iterations: int = 1, load_more_button: str = "btn-load-more"
    ):
        latest_button = self.__driver.find_element(By.CLASS_NAME, load_more_button)
        error_counter = 0

        for _ in range(iterations):
            sleep(0.5)
            try:
                latest_button.click()
            except ElementClickInterceptedException:
                print("scraper: fuck the element click intercepted exception!")
                error_counter += 1
                continue

        print(
            f"scraper: {error_counter} out of {iterations} iterations went wrong {':c' if error_counter else ':)'}"
        )

    def save_page(self, name: str = None):
        page_source = self.__driver.page_source

        if name is None:
            timestamp = datetime.now().strftime("%d-%b-%Y_%H-%M-%S")
            name = f"{self.__medium_name}_{timestamp}.html"

        with open(f"saved_pages/{name}", "w") as file:
            file.write(page_source)

        print(f"scraper: the file was saved here: {name}")
        return name
