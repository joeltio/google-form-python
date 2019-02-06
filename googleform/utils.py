import requests


def fetch_html(url):
    response = requests.get(url)
    return response.text


def xpath_freebird_div(tree, name, exact=False):
    if not exact:
        xpath = ".//div[contains(@class, 'freebirdFormviewerViewItems{}')]"
    else:
        xpath = ".//div[@class='freebirdFormviewerViewItems{}']"

    full_xpath = xpath.format(name)
    return tree.xpath(full_xpath)


def has_freebird_div(tree, name, exact=False):
    result = xpath_freebird_div(tree, name, exact=exact)
    if result:
        return True
    else:
        return False


def eval_map(f, iterable, as_tuple=False):
    m = map(f, iterable)
    if as_tuple:
        return tuple(m)
    else:
        return list(m)


def get_elements_text(tree, xpath, as_tuple=False):
    return eval_map(lambda x: x.text, tree.xpath(xpath), as_tuple=as_tuple)
