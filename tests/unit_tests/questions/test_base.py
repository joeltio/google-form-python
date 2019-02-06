import pytest
import os
import json
import lxml.etree as etree

from googleform.questions.base import get_question_title, get_question_desc


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
)


@pytest.fixture
def question_paths():
    return [
        os.path.join(FIXTURE_DIR, "checkbox.html"),
        os.path.join(FIXTURE_DIR, "date_year_time.html"),
        os.path.join(FIXTURE_DIR, "dropdown.html"),
        os.path.join(FIXTURE_DIR, "duration.html"),
        os.path.join(FIXTURE_DIR, "long_text.html"),
        os.path.join(FIXTURE_DIR, "radio_scale.html"),
        os.path.join(FIXTURE_DIR, "radio_select.html"),
        os.path.join(FIXTURE_DIR, "short_text.html"),
        os.path.join(FIXTURE_DIR, "time.html"),
    ]


@pytest.fixture
def question_trees(question_paths):
    trees = {}

    for path in question_paths:
        with open(path, "r") as f:
            html = f.read()

        basename = os.path.basename(path)
        trees[basename] = etree.HTML(html)

    return trees


@pytest.fixture
def question_info():
    path = os.path.join(FIXTURE_DIR, "question_info.json")

    with open(path, "r") as f:
        return json.load(f)


def test_get_question_title(question_trees, question_info):
    for basename, tree in question_trees.items():
        expected_title = question_info[basename]["title"]

        assert get_question_title(tree) == expected_title


def test_get_question_desc(question_trees, question_info):
    for basename, tree in question_trees.items():
        expected_desc = question_info[basename]["description"]

        assert get_question_desc(tree) == expected_desc
