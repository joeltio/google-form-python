from .base import Question
import _internal_util


def get_options(tree):
    xpath = (".//label[contains(@class, "
             "'freebirdFormviewerViewItemsCheckboxContainer')]//span")

    return list(map(lambda x: x.text, tree.xpath(xpath)))


class CheckboxQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)

        self.options = get_options(self.tree)
        self.checked = {option: False for option in self.options}

    @staticmethod
    def is_this_question(tree):
        xpath = _internal_util.get_freebird_class_div("CheckboxChoice")

        if tree.xpath(xpath):
            return True
        else:
            return False

    def answer(self, option):
        self.checked[option] = True

    def serialize(self):
        checked_options = [x for x in self.checked if self.checked[x]]
        return {
            self.id: checked_options,
        }


question = CheckboxQuestion
