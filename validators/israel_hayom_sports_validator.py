import requests
from bs4 import BeautifulSoup

SPORTS_TAG = "ספורט"
NON_SPORTS_TAGS_COUNT = 2


def validate_change(url: str, old: str, new: str):
    """
    Sports articles has at least 3 times <a href="https://www.israelhayom.co.il/sport">ספורט</a>
    while a regular article has 2 in the header
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return len(soup.findAll("a", string=SPORTS_TAG)) <= NON_SPORTS_TAGS_COUNT
