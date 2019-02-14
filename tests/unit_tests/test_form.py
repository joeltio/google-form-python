from googleform.form import (
    get_response_url, get_form_title, get_form_description
)


def test_get_form_response_url(form_tree, form_info):
    assert get_response_url(form_tree) == form_info["response_url"]


def test_get_form_title(form_tree, form_info):
    assert get_form_title(form_tree) == form_info["title"]


def test_get_form_description(form_tree, form_info):
    assert get_form_description(form_tree) == form_info["description"]
