import requests
import logging
import json

from pages.all_flats_page import AllFlatsPage
from pages.flat_page import FlatPage
from parsers.flat_parser import FlatParser
from utils.queries import get_page_content

logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt='%m-%d-%Y %H:%M:%S',
                    level=logging.DEBUG,
                    filename="logs.txt")

logger = logging.getLogger('scraping')

logger.info('Loading first page with ads list...')

base_url = 'https://kvadrat64.ru/'

page_content = get_page_content(base_url + 'sellflatbank-50-1.html')
page = AllFlatsPage(page_content)
page_count = page.page_count
deal_type = 'Продажа'
print(f'Найдено {page_count} страниц с объявлениями о продаже квартир')

# ВРЕМЕННЫЙ БЛОК КОДА БЕЗ ОБХОДА ВСЕХ СТРАНИЦ С ОБЪЯВЛЕНИЯМИ 
# ================================================================================
print('Собираю ссылки на объявления с первой страницы')
ads_list = []
page_content = get_page_content(base_url + f'sellflatbank-50-1.html')
page = AllFlatsPage(page_content)
flats_links = page.ad_links

for link in flats_links:
    flat_page_content = get_page_content(base_url + link)
    flat_page = FlatPage(flat_page_content)
    flat_parser = FlatParser(deal_type, flat_page.dates_block, flat_page.header, flat_page.main_block)
    print('=======================================================================')
    # print(flat_parser.specs)
    objec_description = flat_parser.full_info_clean
    for key in objec_description:
      print(key, objec_description[key])

# КОНЕЦ ВРЕМЕННОГО БЛОКА КОДА
# ================================================================================

# for i in range(page_count):
#     logger.debug(f'Opening {i+1} page with ads lists...')
#     page_content = get_page_content(base_url + f'sellflatbank-1000-{i+1}.html')
#     page = AllFlatsPage(page_content)
#
#     flats_links = page.ad_links
#
#     for link in flats_links:
#         logger.info(f'Loading ad page: {link}...')
#         flat_page_content = get_page_content(base_url + link)
#         flat_page = FlatPage(flat_page_content)
#
#         flat_parser = FlatParser(flat_page.dates_block, flat_page.header, flat_page.main_block)
#         print(flat_parser.full_info)
#         ads_list.append(flat_parser.full_info)

# with open('living_realty.json', 'w') as json_file:
#     json.dump(ads_list , json_file)