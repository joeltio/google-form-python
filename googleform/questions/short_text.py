from .base import Question
from googleform import utils


class ShortTextQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)

        self._answer = None

    @staticmethod
    def is_this_question(tree):
        return utils.has_freebird_div(tree, "TextShortText")

    def answer(self, text):
        self._answer = text

    def serialize(self):
        return {
            self.id: self._answer,
        }


question = ShortTextQuestion
