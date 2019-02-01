from enum import Enum


class QUESTION_TYPE(Enum):
    SHORT_TEXT = "stext"
    LONG_TEXT = "ltext"

    RADIO_LIST = "radiolist"
    RADIO_SCALE = "radioscale"

    CHECKBOX = "checkbox"

    TIME = "time"
    DURATION = "duration"
    DATE_YEAR = "datey"
    DATE_TIME = "datet"
    DATE_YEAR_TIME = "dateyt"

    DROPDOWN = "dropdown"
