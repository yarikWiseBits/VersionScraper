from bs4 import BeautifulSoup
import requests


class BaseScraper:
    @staticmethod
    def get_page(url) -> BeautifulSoup:
        "Get page for parsing"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup





