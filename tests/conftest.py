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


@pytest.fixture
def form_html(fixture_path):
    path = fixture_path("form.html")

    with open(path, "r") as f:
        return f.read()


@pytest.fixture
def form_tree(form_html):
    return etree.HTML(form_html)


@pytest.fixture
def form_info(fixture_path):
    path = fixture_path("form_info.json")

    with open(path, "r") as f:
        return json.load(f)


@pytest.fixture
def question_info(fixture_path):
    path = fixture_path("question_info.json")

    with open(path, "r") as f:
        return json.load(f)
