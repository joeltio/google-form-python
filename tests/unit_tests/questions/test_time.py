import pytest

from googleform.questions.time import TimeQuestion


@pytest.fixture(scope="module")
def time_paths(fixture_path):
    return [
        fixture_path("time.html"),
    ]


@pytest.fixture(scope="module")
def not_time_paths(fixture_path):
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
        fixture_path("other_radio_list.html"),
        fixture_path("radio_list.html"),
        fixture_path("radio_scale.html"),
        fixture_path("required_dropdown.html"),
        fixture_path("required_radio_list.html"),
        fixture_path("short_text.html"),
    ]


@pytest.fixture(scope="module")
def time_questions(get_question, time_paths):
    return list(map(get_question, time_paths))


@pytest.fixture(scope="module")
def not_time_questions(get_question, not_time_paths):
    return list(map(get_question, not_time_paths))


def test_distinguish_time(time_questions, not_time_questions):
    for question in time_questions:
        assert TimeQuestion.is_this_question(question["tree"]) is True

    for question in not_time_questions:
        assert TimeQuestion.is_this_question(question["tree"]) is False
