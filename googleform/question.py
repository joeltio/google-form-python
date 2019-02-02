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

    def _xpath(self, xpath):
        return self.question_tree.xpath(xpath)


class ShortTextQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.SHORT_TEXT

        self.answer = None

    def answer(self, text):
        self.answer = text


class LongTextQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.LONG_TEXT

        self.answer = None

    def answer(self, text):
        self.answer = text


class RadioListQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.RADIO_LIST

        self.answer = None

    def answer(self, option_name):
        self.answer = option_name


class RadioScaleQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.RADIO_SCALE

        self.answer = None

    def answer(self, option_number):
        self.answer = option_number


class CheckboxQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.CHECKBOX

        self.checked = []

    def answer(self, option):
        self.checked.append(option)


class TimeQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.TIME

        self.hour = None
        self.minute = None

    def answer(self, hour, minute):
        self.hour = hour
        self.minute = minute


class DurationQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.DURATION

        self.hours = None
        self.minutes = None
        self.seconds = None

    def answer(self, hours, minutes, seconds):
        self.hours = hours
        self.minutes = minutes 
        self.seconds = seconds


class DateQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type.startswith(QUESTION_TYPE.DATE)

        self.has_year = QUESTION_TYPE.DATE_YEAR_MODIFIER in self.question_type
        self.has_time = QUESTION_TYPE.DATE_TIME_MODIFIER in self.question_type

        self.day = None
        self.month = None
        self.year = None

        self.hour = None
        self.minute = None

    def answer(self, day, month, year=None, hour=None, minute=None):
        self.day = day
        self.month = month

        if self.has_year:
            self.year = year

        if self.has_time:
            self.hour = hour
            self.minute = minute


class DropdownQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.question_type == QUESTION_TYPE.DROPDOWN

        self.answer = None

    def answer(self, option_name):
        self.answer = option_name
