import requests
import logging
import csv

import pandas as pd

from pages.all_flats_page import AllFlatsPage
from pages.flat_page import FlatPage
from parsers.flat_parser import FlatParser
from utils.queries import get_page_content
from utils.database import DataBase

logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt='%m-%d-%Y %H:%M:%S',
                    level=logging.DEBUG,
                    filename="logs.txt")

logger = logging.getLogger('scraping')

logger.info('Loading first page with ads list...')

db = DataBase()
db.open_connection()
# db.clear()

base_url = 'https://kvadrat64.ru/'

page_content = get_page_content(base_url + 'sellflatbank-50-1.html')
page = AllFlatsPage(page_content)
page_count = page.page_count
deal_type = 'Продажа'
print(f'Найдено {page_count} страниц с объявлениями о продаже квартир')

for i in range(1):
    logger.debug(f'Opening {i+1} page with ads lists...')
    page_content = get_page_content(base_url + f'sellflatbank-50-{i+1}.html')
    page = AllFlatsPage(page_content)

    flats_links = page.ad_links

    for link in flats_links:
        logger.info(f'Loading ad page: {link}...')
        if not db.is_in_db(base_url + link):
            print(f'Извлекаю информацию об объекте {base_url + link}')
            flat_page_content = get_page_content(base_url + link)
            flat_page = FlatPage(flat_page_content)
            flat_parser = FlatParser(deal_type, flat_page.dates_block, flat_page.header, flat_page.main_block)
            flat_info = flat_parser.full_info_clean
            
            db.add_item(flat_info)

db.info()
db.close_connection()