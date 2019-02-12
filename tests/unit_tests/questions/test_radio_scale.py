import pytest

from googleform.questions.radio_scale import RadioScaleQuestion


@pytest.fixture(scope="module")
def radio_scale_paths(fixture_path):
    return [
        fixture_path("radio_scale.html"),
    ]


@pytest.fixture(scope="module")
def not_radio_scale_paths(fixture_path):
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
        fixture_path("required_dropdown.html"),
        fixture_path("required_radio_list.html"),
        fixture_path("short_text.html"),
        fixture_path("time.html"),
    ]


@pytest.fixture(scope="module")
def radio_scale_questions(get_question, radio_scale_paths):
    return list(map(get_question, radio_scale_paths))


@pytest.fixture(scope="module")
def not_radio_scale_questions(get_question, not_radio_scale_paths):
    return list(map(get_question, not_radio_scale_paths))


def test_distinguish_radio_scale(radio_scale_questions,
                                 not_radio_scale_questions):
    for question in radio_scale_questions:
        assert RadioScaleQuestion.is_this_question(question["tree"]) is True

    for question in not_radio_scale_questions:
        assert RadioScaleQuestion.is_this_question(question["tree"]) is False
