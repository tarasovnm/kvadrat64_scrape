import logging
from bs4 import BeautifulSoup

from locators.flat_locators import FlatLocators

logger = logging.getLogger('scraping.flat_page')


class FlatPage:

    def __init__(self, page_content):
        logger.debug(f'New FlatPage created from {page_content}')
        self.soup = BeautifulSoup(page_content, 'html.parser')

    @property
    def dates_block(self):
        logger.debug('Finding dates block...')
        locator = FlatLocators.DATES
        dates_block = self.soup.select_one(locator)
        logger.debug('Dates block found')
        return dates_block

    @property
    def header(self):
        logger.debug('Finding header block...')
        locator = FlatLocators.HEADER
        header = self.soup.select(locator)
        logger.debug('Header block found')
        return header

    @property
    def main_block(self):
        logger.debug('Finding main block...')
        locator = FlatLocators.MAIN
        main_block = self.soup.select_one(locator)
        logger.debug('Main block found')
        return main_block
