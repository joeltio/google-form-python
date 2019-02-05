import requests
import urllib.parse as urlparse


def create_response_url(form_url):
    url_parts = list(urlparse.urlsplit(form_url))
    path_components = url_parts[2].rstrip("/").split("/")

    new_path = path_components[:-1]
    new_path.append("formResponse")

    url_parts[2] = "/".join(new_path)

    return urlparse.urlunsplit(url_parts)


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
