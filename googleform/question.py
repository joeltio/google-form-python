import _internal_util
from question_type import get_question_type, QUESTION_TYPE


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


class Question:
    def __init__(self, question_tree):
        self.tree = question_tree
        self.type = get_question_type(question_tree)

        # Get the title and the description
        self.title = get_question_title(question_tree)
        self.description = get_question_desc(question_tree)

        self.value = None

    def _xpath(self, xpath):
        return self.question_tree.xpath(xpath)


class ShortTextQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.SHORT_TEXT

        self.value = ""

    def answer(self, text):
        self.value = text


class LongTextQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.LONG_TEXT

        self.value = ""

    def answer(self, text):
        self.value = text


class RadioListQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.RADIO_LIST


class RadioScaleQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.RADIO_SCALE


class CheckboxQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.CHECKBOX


class TimeQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.TIME


class DurationQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.DURATION


class DateQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type.startswith(QUESTION_TYPE.DATE)

        self.has_year = QUESTION_TYPE.DATE_YEAR_MODIFIER in self.question_type
        self.has_time = QUESTION_TYPE.DATE_TIME_MODIFIER in self.question_type


class DropdownQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.DROPDOWN
