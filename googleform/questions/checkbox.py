from .base import Question
import utils


def get_options(tree):
    xpath = (".//label[contains(@class, "
             "'freebirdFormviewerViewItemsCheckboxContainer')]//span")

    return utils.get_elements_text(tree, xpath)


class CheckboxQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)

        self.options = get_options(self.tree)
        self.checked = {option: False for option in self.options}

    @staticmethod
    def is_this_question(tree):
        return utils.has_freebird_div("CheckboxChoice")

    def answer(self, option):
        self.checked[option] = True

    def serialize(self):
        checked_options = [x for x in self.checked if self.checked[x]]
        return {
            self.id: checked_options,
        }


question = CheckboxQuestion
