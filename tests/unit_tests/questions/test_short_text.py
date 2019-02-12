import pytest

from googleform.questions.short_text import ShortTextQuestion


@pytest.fixture(scope="module")
def short_text_paths(fixture_path):
    return [
        fixture_path("short_text.html"),
    ]


@pytest.fixture(scope="module")
def not_short_text_paths(fixture_path):
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
        fixture_path("time.html"),
    ]


@pytest.fixture(scope="module")
def short_text_questions(get_question, short_text_paths):
    return list(map(get_question, short_text_paths))


@pytest.fixture(scope="module")
def not_short_text_questions(get_question, not_short_text_paths):
    return list(map(get_question, not_short_text_paths))


def test_distinguish_short_text(short_text_questions,
                                not_short_text_questions):
    for question in short_text_questions:
        assert ShortTextQuestion.is_this_question(question["tree"]) is True

    for question in not_short_text_questions:
        assert ShortTextQuestion.is_this_question(question["tree"]) is False
