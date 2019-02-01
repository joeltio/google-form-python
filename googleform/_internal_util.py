import requests
from urllib.parse import urlparse


def get_form_id(form_url):
    path = urlparse(form_url).path
    path_components = path.rstrip("/").split("/")

    return path_components[-2]


def fetch_html(url):
    response = requests.get(url)
    return response.text
