from bs4 import BeautifulSoup
import requests


class LovenseExtensionScraper:
    url = "https://www.lovense.com/cam-model/guides/add-extension-manually-chrome"
    tag = "span"
    class_selector = "dl-ver"

    def get_lovense_page(self) -> BeautifulSoup:
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup

    def parse_text(self, text: str) -> str:
        version = text.split()
        return version[1]

    def get_lovense_version(self) -> str:
        page = self.get_lovense_page()
        version_tag = page.findAll(self.tag, class_=self.class_selector)
        return self.parse_text(version_tag[0].text)


class LovenseBrowserScraper:
    url = "https://www.lovense.com/cam-model/download"
    tag = "span"
    class_selector = "dl-ver"

    def get_lovense_page(self) -> BeautifulSoup:
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup

    def get_lovense_version(self) -> str:
        page = self.get_lovense_page()
        version_tag = page.select('.c_list_in .u-version')
        return version_tag[1].text