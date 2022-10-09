from time import sleep

import requests

from bs4 import BeautifulSoup
import pandas as pd

from src.config import MEDIUM_URL
from src.parser.utils import get_timestamp_now, get_domain_name_from_url


def save_titles(iterations: int = 4150, file_name: str = None):
    if file_name is None:
        timestamp = get_timestamp_now()
        file_name = (
            f"saved_titles/{get_domain_name_from_url(MEDIUM_URL)}_{timestamp}.csv"
        )

    all_titles = []
    for i in range(1, iterations):
        req = requests.get(MEDIUM_URL.replace("{PAGE}", str(i)))
        soup = BeautifulSoup(req.text, "html.parser")
        titles = soup.find_all("h3", {"class": "post-title entry-title"})

        if len(titles) != 9:
            print(len(titles), "Seems there's something wrong :c")
            print(req.text)
            df = pd.DataFrame(all_titles, columns=["headline_text"])
            df.to_csv(file_name, index=False)
            sleep(120)

        for title in titles:
            all_titles.append(title.text)

        if i % 10 == 0:
            print(f"{i} out of {iterations} pages were scraped")

        sleep(0.5)

    df = pd.DataFrame(all_titles, columns=["headline_text"])
    df.to_csv(file_name, index=False)


save_titles()
