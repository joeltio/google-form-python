import lxml.etree as etree
import requests

import _internal_util
from question import create_question


def get_questions(tree):
    xpath = ".//div[@class='freebirdFormviewerViewNumberedItemContainer']"
    elements = tree.xpath(xpath)

    return list(map(create_question, elements))


class GoogleForm:
    def __init__(self, form_url, html):
        self.form_url = form_url
        self.response_url = _internal_util.create_response_url(form_url)
        self.html = html

        # Create the question objects
        tree = etree.HTML(html)
        self.questions = get_questions(tree)

    def submit(self):
        payload = {}
        for question in self.questions:
            payload = {**payload, **question.serialize()}

        requests.post(self.response_url, data=payload)
