import pytest

from googleform.questions.dropdown import DropdownQuestion


@pytest.fixture(scope="module")
def dropdown_paths(fixture_path):
    return [
        fixture_path("dropdown.html"),
        fixture_path("required_dropdown.html"),
    ]


@pytest.fixture(scope="module")
def not_dropdown_paths(fixture_path):
    return [
        fixture_path("checkbox.html"),
        fixture_path("date_time.html"),
        fixture_path("date_year_time.html"),
        fixture_path("date_year.html"),
        fixture_path("date.html"),
        fixture_path("duration.html"),
        fixture_path("long_text.html"),
        fixture_path("other_checkbox.html"),
        fixture_path("other_radio_list.html"),
        fixture_path("radio_list.html"),
        fixture_path("radio_scale.html"),
        fixture_path("required_radio_list.html"),
        fixture_path("short_text.html"),
        fixture_path("time.html"),
    ]


@pytest.fixture(scope="module")
def dropdown_questions(get_question, dropdown_paths):
    return list(map(get_question, dropdown_paths))


@pytest.fixture(scope="module")
def not_dropdown_questions(get_question, not_dropdown_paths):
    return list(map(get_question, not_dropdown_paths))


def test_distinguish_dropdown(dropdown_questions, not_dropdown_questions):
    for question in dropdown_questions:
        assert DropdownQuestion.is_this_question(question["tree"]) is True

    for question in not_dropdown_questions:
        assert DropdownQuestion.is_this_question(question["tree"]) is False


def test_get_dropdown_options(dropdown_questions):
    for question in dropdown_questions:
        question_obj = DropdownQuestion(question["tree"])

        assert question_obj.options == question["options"]
