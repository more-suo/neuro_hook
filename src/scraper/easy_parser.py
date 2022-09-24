import requests

from bs4 import BeautifulSoup
import pandas as pd

from src.config import MEDIUM_URL
from src.scraper.utils import get_timestamp_now, get_domain_name_from_url


def save_titles(iterations: int = 4150, file_name: str = None):
    if file_name is None:
        timestamp = get_timestamp_now()
        file_name = (
            f"saved_titles/{get_domain_name_from_url(MEDIUM_URL)}_{timestamp}.csv"
        )

    titles = []
    for i in range(1, iterations):
        req = requests.get(MEDIUM_URL.replace("{PAGE}", str(i)))
        soup = BeautifulSoup(req.text, "html.parser")
        for link in soup.find_all("h3", {"class": "post-title"}):
            titles.append(link.text)

        if i % 10 == 0:
            print(f"{i} out of {iterations} pages were scraped")

    df = pd.DataFrame(titles, columns=["headline_text"])
    df.to_csv(file_name, index=False)


save_titles()
