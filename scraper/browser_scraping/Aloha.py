from browser_scraping.BaseScraping import BaseScraper


class Aloha(BaseScraper):
    def __init__(self):
        self.ios_version = "https://apps.apple.com/US/app/id1105317682"
        self.android_version = "https://play.google.com/store/apps/details?id=com.alohamobile.browser"

    def get_android_version(self) -> str:
        "Get android version from google play"
        page = self.get_page(self.android_version)
        version = page.findAll('span', class_='htlgb')

        return version[7].text

    def get_ios_version(self) -> str:
        "Get ios version from google play"
        page = self.get_page(self.ios_version)
        version = page.findAll('p', class_='whats-new__latest__version')[0].text.split(" ")

        return version[1]

