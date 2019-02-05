import requests


def fetch_html(url):
    response = requests.get(url)
    return response.text


def get_freebird_class_div(name, contains=True):
    if contains:
        xpath = ".//div[contains(@class, 'freebirdFormviewerViewItems{}')]"
    else:
        xpath = ".//div[@class='freebirdFormviewerViewItems{}']"

    return xpath.format(name)


def eval_map(f, iterable, as_tuple=False):
    m = map(f, iterable)
    if as_tuple:
        return tuple(m)
    else:
        return list(m)


def get_elements_text(tree, xpath, as_tuple=False):
    return eval_map(lambda x: x.text, tree.xpath(xpath), as_tuple=as_tuple)
