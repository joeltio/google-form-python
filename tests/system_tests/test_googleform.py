import googleform


def test_googleform_imports():
    assert googleform.get == googleform.api.get
    assert googleform.GoogleForm == googleform.form.GoogleForm


def test_googleform_get(requests_mock, form_html, form_info):
    url = "http://www.somegoogleform.com/"
    requests_mock.get(url, text=form_html)

    form = googleform.get(url)

    assert form.title == form_info["title"]
    assert form.description == form_info["description"]
    assert len(form.questions) == form_info["number_of_questions"]
