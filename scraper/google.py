import requests
from bs4 import NavigableString

from scraper.utils import handle_none_type, get_parser

GOOGLE_PLAY = 'https://play.google.com/store/apps/details?id={app_id}&hl=en'
MARKER = 'play.google.com'


@handle_none_type
def extract_genre(page):
    genre_component_attrs = {
        'name': 'span',
        'attrs': {'itemprop': 'genre'}
    }
    return get_parser(page).find(**genre_component_attrs).string


@handle_none_type
def extract_artwork_link(page):
    cover_image_component_attrs = {
        'name': 'img',
        'attrs': {'class': 'cover-image'}
    }
    url = get_parser(page).find(**cover_image_component_attrs)['src']
    if url:
        return 'https:' + url


@handle_none_type
def extract_description(page):
    description_component_attrs = {
        'name': 'div',
        'attrs': {'jsname': 'C4s9Ed'}
    }
    parts = get_parser(page).find(**description_component_attrs).contents
    return ' '.join(str(p) for p in parts if type(p) == NavigableString and len(p) > 0)


def get_page_by_id(id):
    url = GOOGLE_PLAY.format(app_id=id)
    response = requests.get(url)
    if response.status_code == 200:
        return response.content

if __name__ == '__main__':

    res = get_page_by_id('de.ada.picdumps')
    print(extract_genre(res))
    print(extract_artwork_link(res))
    print(extract_description(res))
