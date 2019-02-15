from .base import Question
from googleform import utils


def get_options(tree):
    xpath = (".//label[contains(@class, "
             "'freebirdFormviewerViewItemsCheckboxContainer')]//span")

    return utils.get_elements_text(tree, xpath)


def has_other_option(tree):
    return utils.has_freebird_div(tree, "CheckboxOtherInputElement")


class CheckboxQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)

        self.options = get_options(self.tree)
        self.checked = {option: False for option in self.options}
        self._other_answer = None
        self.has_other_option = has_other_option(self.tree)

    @staticmethod
    def is_this_question(tree):
        return utils.has_freebird_div(tree, "CheckboxChoice")

    def answer(self, option):
        self.checked[option] = True

    def batch_answer(self, answers):
        for answer in answers:
            self.answer(answer)

    def reset_answers(self):
        self.checked = {option: False for option in self.options}

    def answer_other(self, other_answer):
        if not self.has_other_option:
            raise ValueError("The CheckboxQuestion does not have an 'other' "
                             "option")
        self.checked["__other_option__"] = True
        self._other_answer = other_answer

    def serialize(self):
        checked_options = [x for x in self.checked if self.checked[x]]
        serialized_payload = {
            self.id: checked_options,
        }

        if self.checked.get("__other_option__") is not None:
            other_option_key = self.id + ".other_option_response"
            serialized_payload[other_option_key] = self._other_answer

        return serialized_payload


question = CheckboxQuestion
