import requests
from bs4 import BeautifulSoup


def validate_change(url: str, old: str, new: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find(string=new) is not None
