import requests
from bs4 import BeautifulSoup


def validate_string_in_html(url: str, string_to_validate: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find(string=string_to_validate) is not None
