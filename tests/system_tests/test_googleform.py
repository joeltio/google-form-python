import pytest
import responses

import googleform
import googleform.questions as gfquestions


@pytest.fixture
def question_types():
    return {
        gfquestions.checkbox.CheckboxQuestion,
        gfquestions.date.DateQuestion,
        gfquestions.dropdown.DropdownQuestion,
        gfquestions.duration.DurationQuestion,
        gfquestions.long_text.LongTextQuestion,
        gfquestions.radio_list.RadioListQuestion,
        gfquestions.radio_scale.RadioScaleQuestion,
        gfquestions.short_text.ShortTextQuestion,
        gfquestions.time.TimeQuestion
    }


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_googleform_imports(question_types):
    assert googleform.get == googleform.api.get
    assert googleform.GoogleForm == googleform.form.GoogleForm
    assert googleform.SubmitFormError == googleform.form.SubmitFormError

    assert googleform.CheckboxQuestion is gfquestions.checkbox.CheckboxQuestion
    assert googleform.DateQuestion is gfquestions.date.DateQuestion
    assert googleform.DropdownQuestion is gfquestions.dropdown.DropdownQuestion
    assert googleform.DurationQuestion is gfquestions.duration.DurationQuestion
    assert googleform.LongTextQuestion is \
        gfquestions.long_text.LongTextQuestion
    assert googleform.RadioListQuestion is \
        gfquestions.radio_list.RadioListQuestion
    assert googleform.RadioScaleQuestion is \
        gfquestions.radio_scale.RadioScaleQuestion
    assert googleform.ShortTextQuestion is \
        gfquestions.short_text.ShortTextQuestion
    assert googleform.TimeQuestion is gfquestions.time.TimeQuestion


def test_googleform_get(mocked_responses, form_html, form_info):
    url = "http://www.somegoogleform.com/"
    mocked_responses.add(responses.GET, url, body=form_html)

    form = googleform.get(url)

    assert form.title == form_info["title"]
    assert form.description == form_info["description"]
    assert len(form.questions) == form_info["number_of_questions"]


@pytest.fixture
def form(form_html):
    return googleform.GoogleForm(form_html)


def test_identify_googleform_question(form, question_types):
    for question in form.questions:
        assert question.__class__ in question_types


def test_options_of_questions(form, question_info):
    question_types_with_options = {
        gfquestions.dropdown.DropdownQuestion,
        gfquestions.radio_list.RadioListQuestion,
        gfquestions.checkbox.CheckboxQuestion,
    }

    for question in form.questions:
        if question not in question_types_with_options:
            continue

        assert question.options == question_info[question.id]["options"]


def test_question_has_other_option(form, question_info):
    question_types_with_others = {
        gfquestions.radio_list.RadioListQuestion,
        gfquestions.checkbox.CheckboxQuestion,
    }

    for question in form.questions:
        if question not in question_types_with_others:
            continue

        assert question.has_other_option == \
            question_info[question.id]["has_other_option"]


def test_question_info(form, question_info):
    for question in form.questions:
        current_question_info = question_info[question.id]
        assert question.title == current_question_info["title"]
        assert question.description == current_question_info["description"]
        assert question.is_required is current_question_info["is_required"]


def test_submit_empty_form_when_required(mocked_responses, form):
    # Setup a 200 response to ensure that the form is not relying on the reply
    # to validate
    mocked_responses.add(
        responses.POST, form.response_url,
        body="", status=200)

    # Ensure that the form has a required question
    assert any(map(lambda x: x.is_required, form.questions))

    with pytest.raises(googleform.SubmitFormError):
        form.submit()
