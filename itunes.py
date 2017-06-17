import requests
from bs4 import NavigableString

from utils import handle_none_type, get_parser

GOOGLE_PLAY = 'https://play.google.com/store/apps/details?id={app_id}&hl=en'
MARKER = 'itunes.apple.com'


@handle_none_type
def extract_genre(page):
    genre_component_attrs = {
        'name': 'span',
        'attrs': {'itemprop': 'applicationCategory'}
    }
    return get_parser(page).find(**genre_component_attrs).string


@handle_none_type
def extract_artwork_link(page):
    left_bar_attrs = {
        'name': 'div',
        'id': 'left-stack'
    }
    cover_image_component_attrs = {
        'name': 'div',
        'attrs': {'class': 'artwork'}
    }
    return get_parser(page).find(**left_bar_attrs).find(**cover_image_component_attrs).img['src-swap']


@handle_none_type
def extract_description(page):
    description_component_attrs = {
        'name': 'p',
        'attrs': {'itemprop': 'description'}
    }
    parts = get_parser(page).find(**description_component_attrs).contents
    return ' '.join(str(p) for p in parts if type(p) == NavigableString and len(p) > 0)


if __name__ == '__main__':
    url = 'https://itunes.apple.com/us/app/bubbu-cat-my-virtual-pet/id1055590420?mt=8'
    res = requests.get(url).content
    print(extract_genre(res))
    print(extract_artwork_link(res))
    print(extract_description(res))
