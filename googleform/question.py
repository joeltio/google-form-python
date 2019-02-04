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

    @abc.abstractmethod
    def serialize(self):
        pass

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

        self._answer = None

    def answer(self, text):
        self._answer = text

    def serialize(self):
        return {
            self.id: self._answer,
        }


class LongTextQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.type == QUESTION_TYPE.LONG_TEXT

        self._answer = None

    def answer(self, text):
        self._answer = text

    def serialize(self):
        return {
            self.id: self._answer,
        }


class RadioListQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.type == QUESTION_TYPE.RADIO_LIST

        self.options = self._get_options()
        self._answer = None

    def _get_options(self):
        xpath = (".//label[contains(@class,"
                 "'freebirdFormviewerViewItemsRadioChoice')]//span")

        return list(map(lambda x: x.text, self._xpath(xpath)))

    def answer(self, option_name):
        self._answer = option_name

    def serialize(self):
        return {
            self.id: self._answer,
        }


class RadioScaleQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.type == QUESTION_TYPE.RADIO_SCALE

        self.scale = self._get_scale_label()
        self._answer = None

    def _get_scale_label(self):
        xpath = ".//div[@class='freebirdMaterialScalecontentRangeLabel']"

        return tuple(map(lambda x: x.text, self._xpath(xpath)))

    def answer(self, option_number):
        self._answer = option_number

    def serialize(self):
        return {
            self.id: self._answer,
        }


class CheckboxQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.type == QUESTION_TYPE.CHECKBOX

        self.options = self._get_options()
        self.checked = {option: False for option in self.options}

    def _get_options(self):
        xpath = (".//label[contains(@class, "
                 "'freebirdFormviewerViewItemsCheckboxContainer')]//span")

        return list(map(lambda x: x.text, self._xpath(xpath)))

    def answer(self, option):
        self.checked[option] = True

    def serialize(self):
        checked_options = [x for x in self.checked if self.checked[x]]
        return {
            self.id: checked_options,
        }


class TimeQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.type == QUESTION_TYPE.TIME

        self.hour = None
        self.minute = None

    def answer(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def serialize(self):
        return {
            "{}_hour".format(self.id): self.hour,
            "{}_minute".format(self.id): self.minute,
        }


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

    def serialize(self):
        return {
            "{}_hour".format(self.id): self.hours,
            "{}_minute".format(self.id): self.minutes,
            "{}_second".format(self.id): self.seconds,
        }


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


class DropdownQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)
        assert self.type == QUESTION_TYPE.DROPDOWN

        self.options = self._get_options()
        self._answer = None

    def _get_options(self):
        xpath = (".//div[contains(@class, "
                 "'freebirdThemedSelectOptionDarkerDisabled')]//content")

        # Ignore the first element, it is the "unselected" option
        option_elements = self._xpath(xpath)[1:]

        return list(map(lambda x: x.text, option_elements))

    def answer(self, option_name):
        self._answer = option_name

    def serialize(self):
        return {
            self.id: self._answer
        }
