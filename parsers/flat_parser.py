import logging
from bs4 import BeautifulSoup
from locators.flat_locators import FlatLocators
from utils.queries import get_soup_element, get_soup_elements
from utils.cleaners import *

logger = logging.getLogger('scraping.flat_parser')


class FlatParser:
    """
    Класс, который получает на входе блоки страницы и извлекает из них информацию по квартире
    """

    def __init__(self, deal_type, dates_block, header, main_block):
        logger.debug('New FlatScraper created')
        self.deal_type = deal_type
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
        logger.debug(f'Dates found: {dates_raw}'.encode("utf-8"))
        dates = {elem.split(' ')[0].capitalize(): elem.split(' ')[1] for elem in dates_raw}
        return dates

    @property
    def title(self):
        logger.debug('Finding title...')
        locator = FlatLocators.TITLE
        title_raw = get_soup_element(self.header[1], locator).text.strip()
        title_list = title_raw.split('м²')
        title_list = [elem.strip() for elem in title_list]
        logger.debug(f'Title found: {title_list}'.encode("utf-8"))

        area = title_list[0].split(' ')[-1]
        object_type = title_list[0].replace(area, '').strip()

        address = title_list[1]
        if address[0] == ',':
            address = address[1:]
        address = address.replace('на карте', '').strip()

        return {'Название': object_type, 'Площадь': area, 'Адрес': address}

    @property
    def specs(self):
        logger.debug('Finding specs...')
        locator = FlatLocators.SPECS
        specs_raw = str(get_soup_element(self.main_block, locator)).split('<br/>')
        areas = [BeautifulSoup(elem, 'html.parser').text.strip() for elem in specs_raw[0].split('</span>')]
        areas = list(filter(None, areas))
        specs_raw = [BeautifulSoup(elem, 'html.parser').text.strip() for elem in specs_raw]
        specs_raw = list(filter(None, specs_raw))
        specs_raw.pop(0)
        specs = areas + specs_raw
        logger.debug(f'Specs found: {specs}'.encode("utf-8"))
        specs = {spec.split(':')[0]:spec.split(':')[1].replace('м²', '').strip() for spec in specs}
        return specs

    @property
    def deal_info(self):
        logger.debug('Finding deal info...')
        locator = FlatLocators.DEAL
        deal_info_raw = get_soup_element(self.main_block, locator)
        deal_info_raw = [BeautifulSoup(elem, 'html.parser').text.strip() for elem in str(deal_info_raw).replace('</span>','<br/>').split('<br/>')]
        deal_info_raw = list(filter(None, deal_info_raw))
        logger.debug(f'Deal info found: {deal_info_raw}'.encode("utf-8"))

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
        ad_url = get_soup_element(self.main_block, locator).text.split(': ')[1]
        logger.debug(f'Url found: {ad_url}')
        return ad_url

    @property
    def full_info(self):
        return {**self.dates, **self.title, **self.specs, **self.deal_info, **self.url}

    @property
    def full_info_clean(self):
        object_info = {}

        # Какие свойства объекта мы должны вернуть после очистки и предобработки:

        # Блок дат :::::::::::::::
        # Создано
        object_info['Создано'] = self.dates['Создано']
        # Обновлено
        object_info['Обновлено'] = self.dates['Обновлено']

        # Блок заголовка :::::::::::::::
        # Тип объекта
        object_info['Тип объекта'] = 'Квартира'
        # Название объекта
        object_info['Название'] = self.title['Название']
        # Назначение объекта
        object_info['Назначение'] = 'Жилое'
        # Количество комнат
        object_info['Количество комнат'] = parse_rooms(self.title['Название'])
        # Адрес
        object_info['Адрес'] = self.title['Адрес']

        # Основной блок :::::::::::::::
        # Характеристики объекта ----------
        # Площадь
        object_info['Площадь'] = parse_area(self.title['Площадь'])
        # Жилая
        object_info['Жилая площадь'] = parse_area(self.specs['Жилая'])
        # Кухня
        object_info['Площадь кухни'] = parse_area(self.specs['Кухня'])
        # Планировка
        object_info['Планировка квартиры'] = self.specs['Планировка квартиры'] if 'Планировка квартиры' in self.specs else ''
        # Комнаты
        object_info['Комнаты'] = self.specs['Комнаты'] if 'Комнаты' in self.specs else ''
        # Санузел
        object_info['Санузел'] = self.specs['Санузел'] if 'Санузел' in self.specs else ''
        # Окна
        # Балкон
        object_info['Балкон'] = self.specs['Балкон'] if 'Балкон' in self.specs else ''
        # Дом(строение)
        object_info['Дом(строение)'] = self.specs['Дом(строение)'] if 'Дом(строение)' in self.specs else ''
        # Коммуникации
        # Этаж
        object_info['Этаж'] = parse_floor(self.specs['Этаж/этажей в доме'])
        # Этажей в доме
        object_info['Этажей в доме'] = parse_num_of_floors(self.specs['Этаж/этажей в доме'])
        # Лифт
        # Мусоропровод
        # Вторичное жильё
        object_info['Вторичное жилье'] = self.specs['Вторичное жилье'] if 'Вторичное жилье' in self.specs else ''
        # Стадия строительства
        object_info['Стадия строительства'] = self.specs['Стадия строительства'] if 'Стадия строительства' in self.specs else ''
        # Дата сдачи
        object_info['Дата сдачи'] = self.specs['Дата сдачи'] if 'Дата сдачи' in self.specs else ''
        # Застройщик

        # Условия сделки -------------
        object_info['Предложение'] = self.deal_type
        # Цена
        object_info['Стоимость'] = int(self.deal_info['Цена'].replace(' ', '').strip())

        # url
        object_info['url'] = self.url

        return object_info
