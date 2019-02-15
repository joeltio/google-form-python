import pytest

from googleform.questions.checkbox import CheckboxQuestion


@pytest.fixture(scope="module")
def checkbox_paths(fixture_path):
    return [
        fixture_path("checkbox.html"),
        fixture_path("other_checkbox.html"),
    ]


@pytest.fixture(scope="module")
def not_checkbox_paths(fixture_path):
    return [
        fixture_path("date_time.html"),
        fixture_path("date_year_time.html"),
        fixture_path("date_year.html"),
        fixture_path("date.html"),
        fixture_path("dropdown.html"),
        fixture_path("duration.html"),
        fixture_path("long_text.html"),
        fixture_path("other_radio_list.html"),
        fixture_path("radio_list.html"),
        fixture_path("radio_scale.html"),
        fixture_path("required_dropdown.html"),
        fixture_path("required_radio_list.html"),
        fixture_path("short_text.html"),
        fixture_path("time.html"),
    ]


@pytest.fixture(scope="module")
def checkbox_questions(get_question, checkbox_paths):
    return list(map(get_question, checkbox_paths))


@pytest.fixture(scope="module")
def not_checkbox_questions(get_question, not_checkbox_paths):
    return list(map(get_question, not_checkbox_paths))


def test_distinguish_checkbox(checkbox_questions, not_checkbox_questions):
    for question in checkbox_questions:
        assert CheckboxQuestion.is_this_question(question["tree"]) is True

    for question in not_checkbox_questions:
        assert CheckboxQuestion.is_this_question(question["tree"]) is False


def test_get_checkbox_options(checkbox_questions):
    for question in checkbox_questions:
        question_obj = CheckboxQuestion(question["tree"])

        assert question_obj.options == question["options"]


def test_checkbox_only_checks_checked(checkbox_questions):
    for question in checkbox_questions:
        question_obj = CheckboxQuestion(question["tree"])

        for option in question_obj.options:
            # All the options are not checked at first
            assert not any(question_obj.checked.values())

            question_obj.answer(option)

            assert question_obj.checked[option] is True
            for other_option in question_obj.checked:
                should_be_checked = other_option == option
                assert question_obj.checked[other_option] is should_be_checked

            # Reset the option
            question_obj.checked[option] = False


def test_checkbox_multiple_checked(checkbox_questions):
    for question in checkbox_questions:
        question_obj = CheckboxQuestion(question["tree"])

        # All the options are not checked at first
        assert not any(question_obj.checked.values())

        # Check two options
        assert len(question_obj.options) >= 2
        option_0 = question_obj.options[0]
        option_1 = question_obj.options[1]

        question_obj.answer(option_0)
        question_obj.answer(option_1)

        # Ensure only selected options are checked
        for option in question_obj.checked:
            should_be_checked = option in {option_0, option_1}
            assert question_obj.checked[option] is should_be_checked


def test_checkbox_has_other_option(checkbox_questions):
    for question in checkbox_questions:
        question_obj = CheckboxQuestion(question["tree"])

        assert question_obj.has_other_option == question["has_other_option"]


def test_checkbox_can_only_answer_other_if_has_other_option(
        checkbox_questions):
    for question in checkbox_questions:
        question_obj = CheckboxQuestion(question["tree"])

        if question_obj.has_other_option:
            question_obj.answer_other("abc")
        else:
            with pytest.raises(ValueError):
                question_obj.answer_other("abc")


def test_checkbox_serializes_other_option(checkbox_questions):
    for question in checkbox_questions:
        question_obj = CheckboxQuestion(question["tree"])

        other_option_key = question_obj.id + ".other_option_response"

        if not question_obj.has_other_option:
            serialized = question_obj.serialize()
            assert other_option_key not in serialized
        else:
            question_obj.answer_other("abc")
            serialized = question_obj.serialize()
            assert other_option_key in serialized


def test_checkbox_reset_answers(checkbox_questions):
    for question in checkbox_questions:
        question_obj = CheckboxQuestion(question["tree"])

        assert len(question_obj.options) >= 2

        # All the options are not checked at first
        assert not any(question_obj.checked.values())

        # Check the first two options
        question_obj.answer(question_obj.options[0])
        question_obj.answer(question_obj.options[1])

        # Some are checked
        assert any(question_obj.checked.values())

        # All the options are not checked after clearing
        question_obj.reset_answers()
        assert not any(question_obj.checked.values())


def test_checkbox_batch_answer(checkbox_questions):
    for question in checkbox_questions:
        question_obj = CheckboxQuestion(question["tree"])

        # All the options are not checked at first
        assert not any(question_obj.checked.values())

        # Check two options
        assert len(question_obj.options) >= 2
        option_0 = question_obj.options[0]
        option_1 = question_obj.options[1]

        question_obj.batch_answer([option_0, option_1])

        # Ensure only selected options are checked
        for option in question_obj.checked:
            should_be_checked = option in {option_0, option_1}
            assert question_obj.checked[option] is should_be_checked
