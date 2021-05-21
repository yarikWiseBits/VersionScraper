from browser_scraping.BaseScraping import BaseScraper


class Firefox(BaseScraper):
    def __init__(self):
        self.base_url = "https://www.mozilla.org"
        self.desktop_version_url = self.base_url + "/en-US/firefox/releases/"
        self.mobile_version_url = self.base_url + "/en-US/firefox/notes"

    def get_desktop_version(self) -> str:
        page = self.get_page(self.desktop_version_url)
        version_tag = page.find("ol", class_="c-release-list")

        return version_tag.find_all('a')[0].text

    def get_list_of_tags(self) -> list:
        page = self.get_page(self.mobile_version_url)
        list_of_tags = page.find_all('a', class_="mzp-c-menu-title")

        return list_of_tags

    def get_mobile_version(self, system_name) -> str:
        list_of_tags = self.get_list_of_tags()

        for name in list_of_tags:
            if name.text == system_name:
                page = self.get_page(self.base_url + name.get('href'))
                version_tag = page.find_all('div', class_="c-release-version")

                return version_tag[0].text

    def get_android_version(self) -> str:
        return self.get_mobile_version('Android')

    def get_ios_version(self) -> str:
        return self.get_mobile_version('iOS')
