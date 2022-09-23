from datetime import datetime
from urllib.parse import urlparse


def get_timestamp_now():
    return datetime.now().strftime("%d-%b-%Y_%H-%M-%S")


def get_domain_name_from_url(url: str, sep: str = "-"):
    return urlparse(url).netloc.replace(".", sep)
