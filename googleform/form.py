import lxml.etree as etree
import requests

import utils
import question


class GoogleForm:
    def __init__(self, form_url, html):
        self.form_url = form_url
        self.response_url = utils.create_response_url(form_url)
        self.html = html

        # Create the question objects
        tree = etree.HTML(html)
        self.questions = question.get_questions(tree)

    def submit(self):
        payload = question.create_payload(self.questions)
        requests.post(self.response_url, data=payload)
