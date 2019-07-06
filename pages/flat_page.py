from bs4 import BeautifulSoup

from locators.flat_locators import FlatLocators


class FlatPage:

    def __init__(self, page_content):
        self.soup = BeautifulSoup(page_content, 'html.parser')

    @property
    def dates_block(self):
        locator = FlatLocators.DATES
        dates_block = self.soup.select_one(locator)
        return dates_block

    @property
    def header(self):
        locator = FlatLocators.HEADER
        header = self.soup.select(locator)
        return header

    @property
    def main_block(self):
        locator = FlatLocators.MAIN
        main_block = self.soup.select_one(locator)
        return main_block
