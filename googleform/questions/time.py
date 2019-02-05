from .base import Question


class TimeQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)

        self.hour = None
        self.minute = None

    @staticmethod
    def is_this_question(tree):
        xpath = """.//div[contains(
            @class,
            'freebirdFormviewerViewItemsTimeTimeInputs'
        )]//div[contains(
            @class,
            'freebirdFormviewerViewItemsTimeSelect'
        )]
        """

        if tree.xpath(xpath):
            return True
        else:
            return False

    def answer(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def serialize(self):
        return {
            "{}_hour".format(self.id): self.hour,
            "{}_minute".format(self.id): self.minute,
        }


question = TimeQuestion
