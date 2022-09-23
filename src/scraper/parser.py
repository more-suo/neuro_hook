from bs4 import BeautifulSoup

from src.scraper.scraper import Scraper
from src.config import MEDIUM_URL
from src.scraper.utils import get_timestamp_now, get_domain_name_from_url


class Parser:
    def __init__(self):
        print(f"parser: initializing the scraper with the following url: {MEDIUM_URL}")
        scraper = Scraper(MEDIUM_URL)
        scraper.load_more_articles(10000)
        file_name = scraper.save_page()

        with open(file_name) as html:
            self.__soup = BeautifulSoup(html.read(), "html.parser")

    def save_titles(self, file_name: str = None):
        if file_name is None:
            timestamp = get_timestamp_now()
            file_name = (
                f"saved_titles/{get_domain_name_from_url(MEDIUM_URL)}_{timestamp}.txt"
            )

        with open(file_name, "w") as file:
            for title in self.__soup.find_all("h3", {"class": "post-title"}):
                file.write(title.text + "\n")

        print(f"parser: the file was saved here: {file_name}")


Parser().save_titles()
