import logging
from bs4 import BeautifulSoup
from locators.flat_locators import FlatLocators

logger = logging.getLogger('scraping.flat_parser')


class FlatParser:
    """
    Класс, который получает на входе блоки страницы и извлекает из них информацию по квартире
    """

    def __init__(self, dates_block, header, main_block):
        logger.debug('New FlatScraper created')
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
        logger.debug('Finding dates...')
        dates_raw = self.dates_block
        dates_raw = BeautifulSoup(str(dates_raw).split('<br/>')[0], 'html.parser').text
        logger.debug(f'Dates found: {dates_raw}')
        return dates_raw

    @property
    def title(self):
        logger.debug('Finding title...')
        locator = FlatLocators.TITLE
        title_raw = self.header[1].select_one(locator).text.strip()
        logger.debug(f'Title found: {title_raw}')
        return title_raw

    @property
    def specs(self):
        logger.debug('Finding specs...')
        locator = FlatLocators.SPECS
        specs_raw = str(self.main_block.select_one(locator)).split('<br/>')
        areas = [BeautifulSoup(elem, 'html.parser').text.strip() for elem in specs_raw[0].split('</span>')]
        areas = list(filter(None, areas))
        specs_raw = [BeautifulSoup(elem, 'html.parser').text.strip() for elem in specs_raw]
        specs_raw = list(filter(None, specs_raw))
        specs_raw.pop(0)
        logger.debug(f'Specs found: {areas + specs_raw}')
        return areas + specs_raw

    @property
    def deal_info(self):
        logger.debug('Finding deal info...')
        locator = FlatLocators.DEAL
        deal_info = self.main_block.select_one(locator)
        deal_info = [BeautifulSoup(elem, 'html.parser').text.strip() for elem in str(deal_info).split('<br/>')]
        deal_info = list(filter(None, deal_info))
        logger.debug(f'Deal info found: {deal_info}')
        return deal_info

    @property
    def url(self):
        logger.debug('Finding url...')
        locator = FlatLocators.URL
        ad_url = self.main_block.select_one(locator).text.split(': ')[1]
        logger.debug(f'Url found: {ad_url}')
        return ad_url
