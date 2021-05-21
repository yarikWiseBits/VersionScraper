from browser_scraping.BaseScraping import BaseScraper
import re


class Chrome(BaseScraper):
    def __init__(self):
        self.url = "https://www.chromestatus.com/features/schedule"

    def get_desktop_version(self) -> str:
        "Get desktop version"
        page = self.get_page(self.url)
        version_tag = page.findAll('script')[4].prettify()
        version = re.findall(r'version.*\d', version_tag)[4].split(" ")[1]

        return version