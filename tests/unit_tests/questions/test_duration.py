import pytest

from googleform.questions.duration import DurationQuestion


@pytest.fixture(scope="module")
def duration_paths(fixture_path):
    return [
        fixture_path("duration.html"),
    ]


@pytest.fixture(scope="module")
def not_duration_paths(fixture_path):
    return [
        fixture_path("checkbox.html"),
        fixture_path("date_time.html"),
        fixture_path("date_year_time.html"),
        fixture_path("date_year.html"),
        fixture_path("date.html"),
        fixture_path("dropdown.html"),
        fixture_path("long_text.html"),
        fixture_path("other_checkbox.html"),
        fixture_path("other_radio_list.html"),
        fixture_path("radio_list.html"),
        fixture_path("radio_scale.html"),
        fixture_path("required_dropdown.html"),
        fixture_path("required_radio_list.html"),
        fixture_path("short_text.html"),
        fixture_path("time.html"),
    ]


@pytest.fixture(scope="module")
def duration_questions(get_question, duration_paths):
    return list(map(get_question, duration_paths))


@pytest.fixture(scope="module")
def not_duration_questions(get_question, not_duration_paths):
    return list(map(get_question, not_duration_paths))


def test_distinguish_duration(duration_questions, not_duration_questions):
    for question in duration_questions:
        assert DurationQuestion.is_this_question(question["tree"]) is True

    for question in not_duration_questions:
        assert DurationQuestion.is_this_question(question["tree"]) is False
