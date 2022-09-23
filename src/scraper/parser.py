from bs4 import BeautifulSoup

from src.scraper.scraper import Scraper
from src.config import MEDIUM_URL


class Parser:
    def __init__(self):
        scraper = Scraper(MEDIUM_URL)
        scraper.load_more_articles(10)
        file_name = scraper.save_page()

        with open(file_name) as html:
            self.__soup = BeautifulSoup(html.read(), "html")
