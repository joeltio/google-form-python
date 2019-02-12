import pytest

from googleform.questions.radio_list import RadioListQuestion


@pytest.fixture(scope="module")
def radio_list_paths(fixture_path):
    return [
        fixture_path("radio_list.html"),
        fixture_path("required_radio_list.html"),
        fixture_path("other_radio_list.html"),
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
        fixture_path("other_checkbox.html"),
        fixture_path("radio_scale.html"),
        fixture_path("required_dropdown.html"),
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


def test_radio_list_has_other_option(radio_list_questions):
    for question in radio_list_questions:
        question_obj = RadioListQuestion(question["tree"])

        assert question_obj.has_other_option == question["has_other_option"]


def test_radio_list_can_only_answer_other_if_has_other_option(
        radio_list_questions):
    for question in radio_list_questions:
        question_obj = RadioListQuestion(question["tree"])

        if question_obj.has_other_option:
            question_obj.answer_other("abc")
        else:
            with pytest.raises(ValueError):
                question_obj.answer_other("abc")


def test_radio_list_serializes_other_option(radio_list_questions):
    for question in radio_list_questions:
        question_obj = RadioListQuestion(question["tree"])

        other_option_key = question_obj.id + ".other_option_response"

        if not question_obj.has_other_option:
            serialized = question_obj.serialize()
            assert other_option_key not in serialized
        else:
            question_obj.answer_other("abc")
            serialized = question_obj.serialize()
            assert other_option_key in serialized
