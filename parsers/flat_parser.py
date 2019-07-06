from bs4 import BeautifulSoup
from locators.flat_locators import FlatLocators

class FlatParser:
    """
    Класс, который получает на входе блоки страницы и извлекает из них информацию по квартире
    """

    def __init__(self, dates_block, header, main_block):
        self.dates_block = dates_block
        self.header = header
        self.main_block = main_block

    def __repr__(self):
        return 'Даты объявления ---------------------------------------------------------------------\n' + \
               str(self.dates) + '\n' + \
               'Заголовок объявления ----------------------------------------------------------------\n' + \
               str(self.title) + '\n' + \
               'Характеристики объекта --------------------------------------------------------------\n' + \
               str(self.specs) + '\n' + \
               'Условия сделки ----------------------------------------------------------------------\n' + \
               str(self.deal_info) + '\n' + \
               'Ссылка на объявление ----------------------------------------------------------------\n' + \
               str(self.url)

    @property
    def dates(self):
        dates_raw = self.dates_block
        dates_raw = BeautifulSoup(str(dates_raw).split('<br/>')[0], 'html.parser').text
        return dates_raw

    @property
    def title(self):
        locator = FlatLocators.TITLE
        title_raw = self.header[1].select_one(locator).text.strip()
        return title_raw

    @property
    def specs(self):
        locator = FlatLocators.SPECS
        specs_raw = str(self.main_block.select_one(locator)).split('<br/>')
        areas = [BeautifulSoup(elem, 'html.parser').text.strip() for elem in specs_raw[0].split('</span>')]
        areas = list(filter(None, areas))
        specs_raw = [BeautifulSoup(elem, 'html.parser').text.strip() for elem in specs_raw]
        specs_raw.pop(0)
        return areas + specs_raw

    @property
    def deal_info(self):
        locator = FlatLocators.DEAL
        deal_info = self.main_block.select_one(locator)
        deal_info = [BeautifulSoup(elem, 'html.parser').text.strip() for elem in str(deal_info).split('<br/>')]
        deal_info = list(filter(None, deal_info))
        return deal_info

    @property
    def url(self):
        locator = FlatLocators.URL
        ad_url = self.main_block.select_one(locator).text.split(': ')[1]
        return ad_url
