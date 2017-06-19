from functools import lru_cache

from bs4 import BeautifulSoup


@lru_cache(512)
def get_parser(page):
    return BeautifulSoup(page, 'lxml')


def handle_none_type(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except AttributeError:
            return
        except TypeError:
            return
        except Exception:
            raise
        return res
    return wrapper
