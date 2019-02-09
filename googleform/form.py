import lxml.etree as etree
import requests
import urllib.parse as urlparse

from googleform import question


def create_response_url(form_url):
    url_parts = list(urlparse.urlsplit(form_url, allow_fragments=False))
    path_components = url_parts[2].strip("/").split("/")

    # Ensure that there are at least 4 elements
    # forms / d / e / <id>
    if len(path_components) < 4:
        raise ValueError("Bad form url given. Expected at least 4 path "
                         "components")

    new_path = path_components[:4]
    new_path.append("formResponse")

    url_parts[2] = "/".join(new_path)
    # Remove query strings (fragments have already been removed through
    # allow_fragments=False)
    url_parts[3] = ""

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
