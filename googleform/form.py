import lxml.etree as etree
import requests
import urllib.urlparse as urlparse

import question


def create_response_url(form_url):
    url_parts = list(urlparse.urlsplit(form_url))
    path_components = url_parts[2].rstrip("/").split("/")

    new_path = path_components[:-1]
    new_path.append("formResponse")

    url_parts[2] = "/".join(new_path)

    return urlparse.urlunsplit(url_parts)


class GoogleForm:
    def __init__(self, form_url, html):
        self.form_url = form_url
        self.response_url = create_response_url(form_url)
        self.html = html

        # Create the question objects
        tree = etree.HTML(html)
        self.questions = question.get_questions(tree)

    def submit(self):
        payload = question.create_payload(self.questions)
        requests.post(self.response_url, data=payload)
