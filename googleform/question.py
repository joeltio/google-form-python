import importlib
import utils


QUESTION_TYPES = [
    "questions.checkbox",
    "questions.date",
    "questions.dropdown",
    "questions.duration",
    "questions.long_text",
    "questions.radio_list",
    "questions.radio_scale",
    "questions.short_text",
    "questions.time",
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
