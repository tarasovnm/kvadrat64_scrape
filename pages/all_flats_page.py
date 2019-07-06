import logging
from bs4 import BeautifulSoup

from locators.all_flats_page import AllFlatsPageLocators

logger = logging.getLogger('scraping.all_flats_page')

class AllFlatsPage:

    def __init__(self, page_content):
        logger.debug('Parsing page content with BeautifulSoup HTML parser')
        self.soup = BeautifulSoup(page_content, 'html.parser')

    @property
    def ad_links(self):
        logger.debug(f'Finding all links to ads in the page using {AllFlatsPageLocators.ADV_LINKS}')
        locator_adv = AllFlatsPageLocators.ADV_LINKS
        items_adv = self.soup.select(locator_adv)
        items_adv_links = [item.attrs['href'] for item in items_adv]

        logger.debug(f'Finding all links to ads in the page using {AllFlatsPageLocators.LINKS}')
        locator = AllFlatsPageLocators.LINKS
        items = self.soup.select(locator)
        items_links = [item.attrs['href'] for item in items]

        return items_adv_links + items_links

    @property
    def page_count(self):
        logging.debug('Finding all number of pages...')
        locator = AllFlatsPageLocators.PAGE_COUNT
        page_num_list = [int(item.text) for item in self.soup.select(locator)]
        page_num = page_num_list[-1]
        logging.info(f'Found number of pages available: {page_num}')
        return page_num