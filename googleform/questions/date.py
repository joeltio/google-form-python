from .base import Question
import _internal_util


def has_year(tree):
    xpath = _internal_util.get_freebird_class_div("DateYearInput")

    if tree.xpath(xpath):
        return True
    else:
        return False


def has_time(tree):
    xpath = _internal_util.get_freebird_class_div("DateTimeInputs")

    if tree.xpath(xpath):
        return True
    else:
        return False


class DateQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)

        self.has_year = has_year(self.tree)
        self.has_time = has_time(self.tree)

        self.day = None
        self.month = None
        self.year = None

        self.hour = None
        self.minute = None

    @staticmethod
    def is_this_question(tree):
        xpath = _internal_util.get_freebird_class_div("DateDateInput")

        if tree.xpath(xpath):
            return True
        else:
            return False

    def answer(self, day, month, year=None, hour=None, minute=None):
        self.day = day
        self.month = month

        if self.has_year:
            self.year = year

        if self.has_time:
            self.hour = hour
            self.minute = minute

    def serialize(self):
        serialized = {
            "{}_day".format(self.id): self.day,
            "{}_month".format(self.id): self.month,
        }

        if self.has_year:
            serialized["{}_year".format(self.id)] = self.year

        if self.has_time:
            serialized["{}_hour".format(self.id)] = self.hour
            serialized["{}_minute".format(self.id)] = self.minute

        return serialized


question = DateQuestion
