from .base import Question
import _internal_util


class ShortTextQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)

        self._answer = None

    @staticmethod
    def is_this_question(tree):
        xpath = _internal_util.get_freebird_class_div("TextShortText")

        if tree.xpath(xpath):
            return True
        else:
            return False

    def answer(self, text):
        self._answer = text

    def serialize(self):
        return {
            self.id: self._answer,
        }


question = ShortTextQuestion
