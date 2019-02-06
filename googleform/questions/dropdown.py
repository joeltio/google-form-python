from .base import Question
from googleform import utils


def get_options(tree):
    xpath = (".//div[contains(@class, "
             "'freebirdThemedSelectOptionDarkerDisabled')]//content")

    # Ignore the first element, it is the "unselected" option
    option_elements = tree.xpath(xpath)[1:]

    return utils.eval_map(lambda x: x.text, option_elements)


class DropdownQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)

        self.options = get_options(self.tree)
        self._answer = None

    @staticmethod
    def is_this_question(tree):
        xpath = (".//div[contains(@class,"
                 "'freebirdFormviewerViewItemsSelectSelect')]")

        if tree.xpath(xpath):
            return True
        else:
            return False

    def answer(self, option_name):
        self._answer = option_name

    def serialize(self):
        return {
            self.id: self._answer
        }


question = DropdownQuestion
