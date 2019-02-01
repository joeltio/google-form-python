from enum import Enum


class QUESTION_TYPE(Enum):
    SHORT_TEXT = "stext"
    LONG_TEXT = "ltext"

    RADIO_LIST = "radiolist"
    RADIO_SCALE = "radioscale"

    CHECKBOX = "checkbox"

    TIME = "time"
    DURATION = "duration"

    DATE = "date"
    DATE_YEAR_MODIFIER = "y"
    DATE_TIME_MODIFIER = "t"
    DATE_YEAR = DATE + DATE_YEAR_MODIFIER
    DATE_TIME = DATE + DATE_YEAR_MODIFIER
    DATE_YEAR_TIME = DATE + DATE_YEAR_MODIFIER + DATE_TIME_MODIFIER

    DROPDOWN = "dropdown"


def get_question_type(question_tree):
    freebird_class_div = \
        ".//div[contains(@class 'freebirdFormviewerViewItems{}')]"

    xpaths = {
        # Text Questions
        QUESTION_TYPE.SHORT_TEXT: freebird_class_div.format("TextShortText"),
        QUESTION_TYPE.LONG_TEXT: freebird_class_div.format("TextLongText"),

        # List Select Questions
        QUESTION_TYPE.RADIO_LIST:
            """.//content[@role='presentation']
                /div[not(@class='freebirdMaterialScalecontentContainer')]
            """,
        QUESTION_TYPE.RADIO_SCALE:
            ".//div[@class='freebirdMaterialScalecontentContainer']",

        QUESTION_TYPE.CHECKBOX: freebird_class_div.format("CheckboxChoice"),
        QUESTION_TYPE.DROPDOWN: freebird_class_div.format("SelectSelect"),

        QUESTION_TYPE.DURATION:
            """.//div[contains(
                @class,
                'freebirdFormviewerViewItemsTimeTimeInputs'
            ) and not(
                .//div[contains(
                    @class,
                    'freebirdFormviewerViewItemsTimeSelect'
                )]
            )]""",
        QUESTION_TYPE.TIME:
            """.//div[contains(
                @class,
                'freebirdFormviewerViewItemsTimeTimeInputs'
            )]//div[contains(
                @class,
                'freebirdFormviewerViewItemsTimeSelect'
            )]
            """,
    }

    for question_type, xpath in xpaths.items():
        if question_tree.xpath(xpath):
            return question_type

    date_xpath = ".//div[@class='freebirdFormviewerViewItemsDateDateInput']"
    time_xpath = ".//div[@class='freebirdFormviewerViewItemsDateTimeInputs']"
    year_xpath = (".//div[contains(@class,"
                  "'freebirdFormviewerViewItemsDateYearInput')]")

    question_type = None
    if question_tree.xpath(date_xpath):
        question_type = QUESTION_TYPE.DATE
        if question_tree.xpath(year_xpath):
            question_type += QUESTION_TYPE.DATE_YEAR_MODIFIER
        if question_tree.xpath(time_xpath):
            question_type += QUESTION_TYPE.DATE_TIME_MODIFIER

    return question_type


class Question:
    def __init__(self, question_type, question_tree, title, description):
        self.question_type = question_type
        self.question_tree = question_tree
        self.title = title
        self.description = description

    def _xpath(self, xpath):
        return self.question_tree.xpath(xpath)
