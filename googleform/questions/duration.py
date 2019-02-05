from .base import Question


class DurationQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)

        self.hours = None
        self.minutes = None
        self.seconds = None

    @staticmethod
    def is_this_question(tree):
        xpath = """.//div[contains(
            @class,
            'freebirdFormviewerViewItemsTimeTimeInputs'
        ) and not(
            .//div[contains(
                @class,
                'freebirdFormviewerViewItemsTimeSelect'
            )]
        )]"""

        if tree.xpath(xpath):
            return True
        else:
            return False

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


question = DurationQuestion
