from bs4 import BeautifulSoup

from locators.all_flats_page import AllFlatsPageLocators

class AllFlatsPage:

    def __init__(self, page_content):
        self.soup = BeautifulSoup(page_content, 'html.parser')

    @property
    def ad_links(self):
        locator_adv = AllFlatsPageLocators.ADV_LINKS
        items_adv = self.soup.select(locator_adv)
        items_adv_links = [item.attrs['href'] for item in items_adv]
        locator = AllFlatsPageLocators.LINKS
        items = self.soup.select(locator)
        items_links = [item.attrs['href'] for item in items]
        return items_adv_links + items_links
