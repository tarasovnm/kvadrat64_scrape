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
        dates_raw = BeautifulSoup(str(dates_raw).split('<br/>')[0], 'html.parser').text.split(', ')
        logger.debug(f'Dates found: {dates_raw}')
        dates = {elem.split(' ')[0].capitalize(): elem.split(' ')[1] for elem in dates_raw}
        return dates

    @property
    def title(self):
        logger.debug('Finding title...')
        locator = FlatLocators.TITLE
        title_raw = self.header[1].select_one(locator).text.strip()
        title_list = title_raw.split('м²')
        title_list = [elem.strip() for elem in title_list]
        logger.debug(f'Title found: {title_list}')

        area = title_list[0].split(' ')[-1]
        object_type = title_list[0].replace(area, '').strip()

        address = title_list[1]
        if address[0] == ',':
            address = address[1:]
        address = address.replace('на карте', '').strip()

        return {'Тип': object_type, 'Площадь': area, 'Адрес': address}

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
        specs = areas + specs_raw
        logger.debug(f'Specs found: {specs}')
        specs = {spec.split(':')[0]:spec.split(':')[1].replace('м²', '').strip() for spec in specs}
        return specs

    @property
    def deal_info(self):
        logger.debug('Finding deal info...')
        locator = FlatLocators.DEAL
        deal_info_raw = self.main_block.select_one(locator)
        deal_info_raw = [BeautifulSoup(elem, 'html.parser').text.strip() for elem in str(deal_info_raw).replace('</span>','<br/>').split('<br/>')]
        deal_info_raw = list(filter(None, deal_info_raw))
        logger.debug(f'Deal info found: {deal_info_raw}')

        deal_info = {}
        for elem in deal_info_raw:
            splited_elem = elem.split(':')
            if len(splited_elem) > 1:
                if elem.split(':')[1].strip() != '':
                    part_one = elem.split(':')[0].strip()
                    part_two = elem.split(':')[1].replace('рублей', '').replace('за м²', '').strip()
                    deal_info[part_one] = part_two

        return deal_info

    @property
    def url(self):
        logger.debug('Finding url...')
        locator = FlatLocators.URL
        ad_url = self.main_block.select_one(locator).text.split(': ')[1]
        logger.debug(f'Url found: {ad_url}')
        return {'url': ad_url}

    @property
    def full_info(self):
        return {**self.dates, **self.title, **self.specs, **self.deal_info, **self.url}
