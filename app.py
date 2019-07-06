import requests

from pages.all_flats_page import AllFlatsPage
from pages.flat_page import FlatPage
from parsers.flat_parser import FlatParser

base_url = 'https://kvadrat64.ru/'
flats_url = 'sellflatbank-1000-1.html'

page_content = requests.get(base_url + flats_url).content
page = AllFlatsPage(page_content)

flats_links = page.ad_links

flat_page_content = requests.get(base_url + flats_links[0]).content
flat_page = FlatPage(flat_page_content)

flat_parser = FlatParser(flat_page.dates_block, flat_page.header, flat_page.main_block)
print(flat_parser)

# План
# [] Добавить систему контроля версий
# [] Добавить обработку исключений на открытие url
# [] Добавить обработку исключений на поиск элементов по селектору
# [] Добавить код сохранения данных в csv-файл
