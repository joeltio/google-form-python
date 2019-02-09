import pytest

from googleform.questions.radio_list import RadioListQuestion


@pytest.fixture(scope="module")
def radio_list_paths(fixture_path):
    return [
        fixture_path("radio_list.html"),
    ]


@pytest.fixture(scope="module")
def not_radio_list_paths(fixture_path):
    return [
        fixture_path("checkbox.html"),
        fixture_path("date_time.html"),
        fixture_path("date_year_time.html"),
        fixture_path("date_year.html"),
        fixture_path("date.html"),
        fixture_path("dropdown.html"),
        fixture_path("duration.html"),
        fixture_path("long_text.html"),
        fixture_path("radio_scale.html"),
        fixture_path("short_text.html"),
        fixture_path("time.html"),
    ]


@pytest.fixture(scope="module")
def radio_list_questions(get_question, radio_list_paths):
    return list(map(get_question, radio_list_paths))


@pytest.fixture(scope="module")
def not_radio_list_questions(get_question, not_radio_list_paths):
    return list(map(get_question, not_radio_list_paths))


def test_distinguish_radio_list(radio_list_questions,
                                not_radio_list_questions):
    for question in radio_list_questions:
        assert RadioListQuestion.is_this_question(question["tree"]) is True

    for question in not_radio_list_questions:
        assert RadioListQuestion.is_this_question(question["tree"]) is False


def test_get_radio_list_options(radio_list_questions):
    for question in radio_list_questions:
        question_obj = RadioListQuestion(question["tree"])

        assert question_obj.options == question["options"]
