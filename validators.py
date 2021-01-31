import requests
from bs4 import BeautifulSoup


def html_validator(url: str, new: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find(new) is not None