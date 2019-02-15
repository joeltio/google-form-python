import abc
import re

from googleform import utils


def get_question_title(question_tree):
    # There is an extra space at the end of the class name to prevent matching
    # of the ItemItemTitleContainer class
    element = utils.xpath_freebird_div(question_tree, "ItemItemTitle ")

    # GoogleForm will add a space at the end of the question if it is required
    title = element[0].text.rstrip(" ")

    return title


def get_question_desc(question_tree):
    element = utils.xpath_freebird_div(question_tree, "ItemItemHelpText")[0]

    return element.text


def get_question_id(question_tree):
    xpath = ".//*[starts-with(@name, 'entry')]"
    element = question_tree.xpath(xpath)[0]

    name = element.attrib["name"]
    entry_id = re.match(r"entry\.\d+", name).group(0)

    return entry_id


def get_is_required(question_tree):
    xpath = ".//span[@class='freebirdFormviewerViewItemsItemRequiredAsterisk']"

    if question_tree.xpath(xpath):
        return True
    else:
        return False


class Question(abc.ABC):
    def __init__(self, question_tree):
        self.tree = question_tree
        self.id = get_question_id(question_tree)

        # Get the title and the description
        self.is_required = get_is_required(question_tree)
        self.title = get_question_title(question_tree)
        self.description = get_question_desc(question_tree)

    @staticmethod
    @abc.abstractmethod
    def is_this_question(tree):
        pass

    @abc.abstractmethod
    def serialize(self):
        pass
