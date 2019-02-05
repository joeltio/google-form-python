from .base import Question


def get_scale_label(tree):
    xpath = ".//div[@class='freebirdMaterialScalecontentRangeLabel']"

    return tuple(map(lambda x: x.text, tree.xpath(xpath)))


class RadioScaleQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)

        self.scale = get_scale_label(self.tree)
        self._answer = None

    @staticmethod
    def is_this_question(tree):
        xpath = ".//div[@class='freebirdMaterialScalecontentContainer']"

        if tree.xpath(xpath):
            return True
        else:
            return False

    def answer(self, option_number):
        self._answer = option_number

    def serialize(self):
        return {
            self.id: self._answer,
        }


question = RadioScaleQuestion
