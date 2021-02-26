import requests
from bs4 import BeautifulSoup

SPORTS_TAG = "ספורט"
SPORTS_ARTICLE_MIN_TAGS = 3


def validate_change(url: str, old: str, new: str):
    """
    Sports articles has at least 3 times <a href="https://www.israelhayom.co.il/sport">ספורט</a>
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return len(soup.findAll("a", string=SPORTS_TAG)) < SPORTS_ARTICLE_MIN_TAGS
