import importlib


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
