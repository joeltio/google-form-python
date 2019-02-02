import _internal_util
from question_type import get_question_type, QUESTION_TYPE


def get_question_title(question_tree):
    # There is an extra space at the end of the class name to prevent matching
    # of the ItemItemTitleContainer class
    xpath = _internal_util.get_freebird_class_div("ItemItemTitle ")
    element = question_tree.xpath(xpath)[0]

    return element.text


def get_question_desc(question_tree):
    xpath = _internal_util.get_freebird_class_div("ItemItemHelpText")
    element = question_tree.xpath(xpath)[0]

    return element.text


class Question:
    def __init__(self, question_tree):
        self.tree = question_tree
        self.type = get_question_type(question_tree)

        # Get the title and the description
        self.title = get_question_title(question_tree)
        self.description = get_question_desc(question_tree)

        self.value = None

    def _xpath(self, xpath):
        return self.question_tree.xpath(xpath)
