import pytest
import os
import json
import lxml.etree as etree


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
)


@pytest.fixture(scope="module")
def fixture_path():
    def _fixture_path(*args):
        return os.path.join(FIXTURE_DIR, *args)

    return _fixture_path


@pytest.fixture(scope="module")
def question_paths(fixture_path):
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
        fixture_path("short_text.html"),
        fixture_path("time.html"),
    ]


@pytest.fixture(scope="module")
def load_html_tree():
    return etree.HTML


@pytest.fixture(scope="module")
def question_info(fixture_path):
    path = fixture_path("question_info.json")

    with open(path, "r") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def get_question(question_info, load_html_tree):
    def _get_question(path):
        basename = os.path.basename(path)
        info = question_info[basename]

        with open(path, "r") as f:
            html = f.read()

        return {
            **info,
            "tree": load_html_tree(html),
        }

    return _get_question


@pytest.fixture(scope="module")
def all_questions(get_question, question_paths):
    return list(map(get_question, question_paths))
