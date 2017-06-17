from parse_utils import parse_html


def search_with_yahoo(query, threshfold):
    try:
        soup = parse_html('https://search.yahoo.com/search?p={}&ei=UTF-8'.format(query))
    except Exception as ex:
        print(ex)
        return []

    results = []
    for h3 in soup.find_all('h3'):
        if h3.a and 'r.search.yahoo.com' not in h3.a['href']:
            results.append(h3.a['href'])
            if len(results) >= threshfold:
                break
    return results
