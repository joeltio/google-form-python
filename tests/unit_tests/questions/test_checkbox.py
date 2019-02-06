import pytest

from googleform.questions.checkbox import CheckboxQuestion


@pytest.fixture(scope="module")
def checkbox_paths(fixture_path):
    return [
        fixture_path("checkbox.html"),
    ]


@pytest.fixture(scope="module")
def not_checkbox_paths(fixture_path):
    return [
        fixture_path("date_year_time.html"),
        fixture_path("dropdown.html"),
        fixture_path("duration.html"),
        fixture_path("long_text.html"),
        fixture_path("radio_scale.html"),
        fixture_path("radio_select.html"),
        fixture_path("short_text.html"),
        fixture_path("time.html"),
    ]


@pytest.fixture(scope="module")
def checkbox_questions(get_question, checkbox_paths):
    print(get_question)
    return list(map(get_question, checkbox_paths))


@pytest.fixture(scope="module")
def not_checkbox_questions(get_question, not_checkbox_paths):
    return list(map(get_question, not_checkbox_paths))


def test_distinguish_checkbox(checkbox_questions, not_checkbox_questions):
    for question in checkbox_questions:
        assert CheckboxQuestion.is_this_question(question["tree"]) is True

    for question in not_checkbox_questions:
        assert CheckboxQuestion.is_this_question(question["tree"]) is False
