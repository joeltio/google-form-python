import pytest

from googleform.questions.date import DateQuestion


@pytest.fixture(scope="module")
def date_paths(fixture_path):
    return [
        fixture_path("date_time.html"),
        fixture_path("date_year_time.html"),
        fixture_path("date_year.html"),
        fixture_path("date.html"),
    ]


@pytest.fixture(scope="module")
def not_date_paths(fixture_path):
    return [
        fixture_path("checkbox.html"),
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
        fixture_path("time.html"),
    ]


@pytest.fixture(scope="module")
def date_questions(get_question, date_paths):
    return list(map(get_question, date_paths))


@pytest.fixture(scope="module")
def not_date_questions(get_question, not_date_paths):
    return list(map(get_question, not_date_paths))


def test_distinguish_date(date_questions, not_date_questions):
    for question in date_questions:
        assert DateQuestion.is_this_question(question["tree"]) is True

    for question in not_date_questions:
        assert DateQuestion.is_this_question(question["tree"]) is False


def test_determine_date_has_year(date_questions):
    for question in date_questions:
        question_obj = DateQuestion(question["tree"])

        should_have_year = question["has_year"]
        assert question_obj.has_year == should_have_year


def test_determine_date_has_time(date_questions):
    for question in date_questions:
        question_obj = DateQuestion(question["tree"])

        should_have_time = question["has_time"]
        assert question_obj.has_time == should_have_time


def test_date_answer_only_sets_existing_fields(date_questions):
    for question in date_questions:
        question_obj = DateQuestion(question["tree"])

        question_obj.answer(1, 1, year=1, hour=1, minute=1)

        if not question_obj.has_year:
            assert question_obj.year is None
        if not question_obj.has_time:
            assert question_obj.hour is None
            assert question_obj.minute is None
