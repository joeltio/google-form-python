from .base import Question
from googleform import utils


def get_options(tree):
    xpath = (".//label[contains(@class,"
             "'freebirdFormviewerViewItemsRadioChoice')]//span")

    return utils.get_elements_text(tree, xpath)


class RadioListQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)

        self.options = get_options(self.tree)
        self._answer = None

    @staticmethod
    def is_this_question(tree):
        xpath = """.//content[@role='presentation']
                   /div[not(@class='freebirdMaterialScalecontentContainer')]"""

        if tree.xpath(xpath):
            return True
        else:
            return False

    def answer(self, option_name):
        self._answer = option_name

    def serialize(self):
        return {
            self.id: self._answer,
        }


question = RadioListQuestion
