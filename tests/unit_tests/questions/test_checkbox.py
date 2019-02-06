import pytest
import os
import lxml.etree as etree

from googleform.questions.checkbox import CheckboxQuestion


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
)

CHECKBOX_FILES = [
    os.path.join(FIXTURE_DIR, "checkbox.html"),
]

NOT_CHECKBOX_FILES = [
    os.path.join(FIXTURE_DIR, "date_year_time.html"),
    os.path.join(FIXTURE_DIR, "dropdown.html"),
    os.path.join(FIXTURE_DIR, "duration.html"),
    os.path.join(FIXTURE_DIR, "long_text.html"),
    os.path.join(FIXTURE_DIR, "radio_scale.html"),
    os.path.join(FIXTURE_DIR, "radio_select.html"),
    os.path.join(FIXTURE_DIR, "short_text.html"),
    os.path.join(FIXTURE_DIR, "time.html"),
]


def load_html_tree(filename):
    with open(filename, "r") as f:
        html = f.read()

    return etree.HTML(html)


@pytest.fixture(scope="module")
def checkbox_tree():
    return list(map(load_html_tree, CHECKBOX_FILES))


@pytest.fixture(scope="module")
def not_checkbox_tree():
    return list(map(load_html_tree, NOT_CHECKBOX_FILES))


def test_distinguish_checkbox(checkbox_tree, not_checkbox_tree):
    for tree in checkbox_tree:
        assert CheckboxQuestion.is_this_question(tree) is True

    for tree in not_checkbox_tree:
        assert CheckboxQuestion.is_this_question(tree) is False
