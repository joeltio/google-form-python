import abc

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


def get_question_id(question_tree):
    xpath = ".//*[starts-with(@name, 'entry')]"
    element = question_tree.xpath(xpath)[0]

    name = element.attrib["name"]

    return name.split("_", 1)[0]


class Question(abc.ABC):
    def __init__(self, question_tree):
        self.tree = question_tree
        self.type = get_question_type(question_tree)
        self.id = get_question_id(question_tree)

        # Get the title and the description
        self.title = get_question_title(question_tree)
        self.description = get_question_desc(question_tree)

    def _xpath(self, xpath):
        return self.tree.xpath(xpath)

    @classmethod
    def create_question(cls, question_tree):
        question_classes = {
            QUESTION_TYPE.SHORT_TEXT: ShortTextQuestion,
            QUESTION_TYPE.LONG_TEXT: LongTextQuestion,

            QUESTION_TYPE.RADIO_LIST: RadioListQuestion,
            QUESTION_TYPE.RADIO_SCALE: RadioScaleQuestion,

            QUESTION_TYPE.CHECKBOX: CheckboxQuestion,

            QUESTION_TYPE.TIME: TimeQuestion,
            QUESTION_TYPE.DURATION: DurationQuestion,

            QUESTION_TYPE.DATE: DateQuestion,
            QUESTION_TYPE.DATE_YEAR: DateQuestion,
            QUESTION_TYPE.DATE_TIME: DateQuestion,
            QUESTION_TYPE.DATE_YEAR_TIME: DateQuestion,

            QUESTION_TYPE.DROPDOWN: DropdownQuestion,
        }

        question_type = get_question_type(question_tree)
        question_class = question_classes[question_type]

        return question_class(question_tree)


class ShortTextQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.type == QUESTION_TYPE.SHORT_TEXT

        self.answer = None

    def answer(self, text):
        self.answer = text


class LongTextQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.type == QUESTION_TYPE.LONG_TEXT

        self.answer = None

    def answer(self, text):
        self.answer = text


class RadioListQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.type == QUESTION_TYPE.RADIO_LIST

        self.options = self._get_options()
        self.answer = None

    def _get_options(self):
        xpath = (".//label[contains(@class,"
                 "'freebirdFormviewerViewItemsRadioChoice')]//span")

        return list(map(lambda x: x.text, self._xpath(xpath)))

    def answer(self, option_name):
        self.answer = option_name


class RadioScaleQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.type == QUESTION_TYPE.RADIO_SCALE

        self.answer = None

    def answer(self, option_number):
        self.answer = option_number


class CheckboxQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.type == QUESTION_TYPE.CHECKBOX

        self.checked = []

    def answer(self, option):
        self.checked.append(option)


class TimeQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.type == QUESTION_TYPE.TIME

        self.hour = None
        self.minute = None

    def answer(self, hour, minute):
        self.hour = hour
        self.minute = minute


class DurationQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.type == QUESTION_TYPE.DURATION

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
        assert QUESTION_TYPE.is_date(self.type)

        self.has_year = QUESTION_TYPE.has_year(self.type)
        self.has_time = QUESTION_TYPE.has_time(self.type)

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
        assert self.type == QUESTION_TYPE.DROPDOWN

        self.answer = None

    def answer(self, option_name):
        self.answer = option_name
