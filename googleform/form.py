import lxml.etree as etree

import _internal_util
import question


def get_questions(tree):
    xpath = ".//div[@class='freebirdFormviewerViewNumberedItemContainer']"
    elements = tree.xpath(xpath)

    return map(question.Question, elements)


class GoogleForm:
    def __init__(self, form_url, html):
        self.form_id = _internal_util.get_form_id(form_url)
        self.form_url = form_url
        self.html = html

        # Create the question objects
        tree = etree.HTML(html)
        self.questions = list(get_questions(tree))
