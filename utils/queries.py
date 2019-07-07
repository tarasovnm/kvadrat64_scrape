import requests
import sys


def get_page_content(url):
    try:
        page_content = requests.get(url).content
        return page_content
    except requests.exceptions.Timeout:
        print(f'Превышен таймаут открытия страницы: {url}')
    except requests.exceptions.TooManyRedirects:
        print(f'Слишком много редиректов по адресу: {url}')
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit(1)


def get_soup_element(parent, locator):
    try:
        element = parent.select_one(locator)
        return element
    except Exception as err:
        print(err)


def get_soup_elements(parent, locator):
    try:
        elements = parent.select(locator)
        return elements
    except Exception as err:
        print(err)
