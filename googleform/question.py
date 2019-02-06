import importlib
from googleform import utils


QUESTION_TYPES = [
    "googleform.questions.checkbox",
    "googleform.questions.date",
    "googleform.questions.dropdown",
    "googleform.questions.duration",
    "googleform.questions.long_text",
    "googleform.questions.radio_list",
    "googleform.questions.radio_scale",
    "googleform.questions.short_text",
    "googleform.questions.time",
]


def create_question(tree):
    for question_type in QUESTION_TYPES:
        QuestionType = importlib.import_module(question_type).question

        if QuestionType.is_this_question(tree):
            return QuestionType(tree)


def get_questions(tree):
    xpath = ".//div[@class='freebirdFormviewerViewNumberedItemContainer']"
    elements = tree.xpath(xpath)

    return utils.eval_map(create_question, elements)


def create_payload(questions):
    payload = {}
    for question in questions:
        payload = {**payload, **question.serialize()}

    return payload
