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
flats_url = 'sellflatbank-1000-1.html'

page_content = requests.get(base_url + flats_url).content
page = AllFlatsPage(page_content)

flats_links = page.ad_links

logger.info('Loading ad page...')

flat_page_content = requests.get(base_url + flats_links[0]).content
flat_page = FlatPage(flat_page_content)

flat_parser = FlatParser(flat_page.dates_block, flat_page.header, flat_page.main_block)
print(flat_parser)

# План
# [x] Добавить систему контроля версий
# [x] Добавить логирование
# [ ] Добавить код обхода страниц и объявлений
# [ ] Добавить обработку исключений на открытие url
# [ ] Добавить обработку исключений на поиск элементов по селектору
# [ ] Добавить код сохранения данных в csv-файл
