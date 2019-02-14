import lxml.etree as etree
import requests

from googleform import question


def get_response_url(tree):
    form_element = tree.xpath(".//form")[0]
    return form_element.attrib["action"]


def get_form_title(tree):
    xpath = ".//div[contains(@class, 'freebirdFormviewerViewHeaderTitle ')]"
    return tree.xpath(xpath)[0].text


def get_form_description(tree):
    xpath = ".//div[@class='freebirdFormviewerViewHeaderDescription']"
    return tree.xpath(xpath)[0].text


class GoogleForm:
    def __init__(self, html):
        self.html = html

        # Create the question objects
        tree = etree.HTML(html)
        self.questions = question.get_questions(tree)
        self.response_url = get_response_url(tree)

    def submit(self):
        payload = question.create_payload(self.questions)
        requests.post(self.response_url, data=payload)
