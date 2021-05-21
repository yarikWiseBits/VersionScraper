from JiraConnector import JiraConnector
from lovense_scraping.lovense_scraper import LovenseExtensionScraper, LovenseBrowserScraper
from browser_scraping.Firefox import Firefox
from browser_scraping.Chrome import Chrome
from browser_scraping.Aloha import Aloha
from DbConnector import DbConnector
from datetime import datetime


class Runner():
    def __init__(self):
        self.lovense_extension = LovenseExtensionScraper()
        self.lovense_browser = LovenseBrowserScraper()
        self.firefox = Firefox()
        self.chrome = Chrome()
        self.aloha = Aloha()
        self.db = DbConnector().create_table_versions()
        self.versions = self.get_new_versions()
        self.jira = JiraConnector()

    def get_new_versions(self):
        scrapped_versions = {
            "lovenseExtension": self.lovense_extension.get_lovense_version(),
            "lovenseBrowser": self.lovense_browser.get_lovense_version(),
            "firefoxDesktop": self.firefox.get_desktop_version(),
            "firefoxAndroid": self.firefox.get_android_version(),
            "firefoxIOS": self.firefox.get_ios_version(),
            "chrome": self.chrome.get_desktop_version(),
            "alohaAndroid": self.aloha.get_ios_version(),
            "alohaIOS": self.aloha.get_android_version()
        }

        return scrapped_versions

    def check_versions_in_db(self):
        new_versions = self.get_new_versions()
        db_versions = self.db.select_all_versions()
        versions_to_test = {}
        print(db_versions)

        if not db_versions:
            new_versions['date'] = datetime.today().strftime("%Y-%m-%d")
            self.db.insert_new_data(new_versions)
            return {}

        for key in new_versions:
            if new_versions[key] != db_versions[key]:
                versions_to_test[key] = new_versions[key]

        print(versions_to_test)

        return versions_to_test

    def add_new_versions_to_db(self, versions):

        if versions:
            self.versions['date'] = datetime.today().strftime("%Y-%m-%d")
            self.db.insert_new_data(self.versions)

        return versions

    def create_jira_tickets(self, versions):

        for key in versions:
            self.jira.create_issue_for_testing(key, versions[key])


if __name__ == "__main__":
    runner = Runner()

    versions = runner.check_versions_in_db()
    runner.create_jira_tickets(versions)
    runner.add_new_versions_to_db(versions)
