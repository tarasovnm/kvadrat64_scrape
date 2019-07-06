import requests
import logging

from pages.all_flats_page import AllFlatsPage
from pages.flat_page import FlatPage
from parsers.flat_parser import FlatParser

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H%:%M:%S',
                    level=logging.DEBUG,
                    filename='logs.txt')

logger = logging.getLogger('scraping')

logger.info('Loading first page with ads list...')

base_url = 'https://kvadrat64.ru/'

page_content = requests.get(base_url + 'sellflatbank-1000-1.html').content
page = AllFlatsPage(page_content)
page_count = 2 # page.page_count

for i in range(page_count):
    logger.debug(f'Opening {i+1} page with ads lists...')
    page_content = requests.get(base_url + f'sellflatbank-1000-{i+1}.html').content
    page = AllFlatsPage(page_content)

    flats_links = page.ad_links

    for link in flats_links:
        logger.info(f'Loading ad page: {link}...')

        flat_page_content = requests.get(base_url + link).content
        flat_page = FlatPage(flat_page_content)

        flat_parser = FlatParser(flat_page.dates_block, flat_page.header, flat_page.main_block)
        print(flat_parser)

# План
# [x] Добавить систему контроля версий
# [x] Добавить логирование
# [x] Добавить код обхода страниц и объявлений
# [ ] Доработать код извлечения информации со страницы об объекте
# [ ] Добавить обработку исключений на открытие url
# [ ] Добавить обработку исключений на поиск элементов по селектору
# [ ] Добавить код сохранения данных в csv-файл
