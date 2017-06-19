import re

from bs4 import BeautifulSoup
import requests


has_point = re.compile(r'[a-zA-Z]{2,}\.( |$)')


def parse_html(url):
    try:
        if 'google' in url:
            url += '&hl=en'
        res = requests.get(url, headers={'Accept-Language': 'en-US'}).content
    except Exception as ex:
        print(ex)
        res = '<html></html>'
    return BeautifulSoup(res, 'lxml')


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'a']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


def sentence(text):
    if len(text.split()) < 5:
        return False
    if '<' in text and '>' in text:
        return False
    if has_point.search(text) is None:
        return False
    return True


def load_visible_text(url):
    soup = parse_html(url)
    if not soup:
        return []
    texts = soup.findAll(text=True)
    yield from filter(sentence, filter(visible, texts))
