import pytest

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


def test_googleform_imports(question_types):
    assert googleform.get == googleform.api.get
    assert googleform.GoogleForm == googleform.form.GoogleForm

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


def test_googleform_get(requests_mock, form_html, form_info):
    url = "http://www.somegoogleform.com/"
    requests_mock.get(url, text=form_html)

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
