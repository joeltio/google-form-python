import abc

import _internal_util


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


def get_question_id(question_tree):
    xpath = ".//*[starts-with(@name, 'entry')]"
    element = question_tree.xpath(xpath)[0]

    name = element.attrib["name"]

    return name.split("_", 1)[0]


class Question(abc.ABC):
    def __init__(self, question_tree):
        self.tree = question_tree
        self.id = get_question_id(question_tree)

        # Get the title and the description
        self.title = get_question_title(question_tree)
        self.description = get_question_desc(question_tree)

    def _xpath(self, xpath):
        return self.tree.xpath(xpath)

    @staticmethod
    @abc.abstractmethod
    def is_this_question(tree):
        pass

    @abc.abstractmethod
    def serialize(self):
        pass
