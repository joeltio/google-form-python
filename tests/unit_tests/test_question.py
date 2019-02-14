import pytest
import os
import lxml.etree as etree
import json

from googleform.questions.base import Question
from googleform.question import create_payload, get_questions


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
def form_tree(fixture_path):
    path = fixture_path("form.html")

    with open(path, "r") as f:
        return etree.HTML(f.read())


@pytest.fixture
def form_info(fixture_path):
    path = fixture_path("form_info.json")

    with open(path, "r") as f:
        return json.load(f)


def test_get_questions(form_tree, form_info):
    questions = get_questions(form_tree)
    assert form_info["number_of_questions"] == len(questions)


def test_create_payload_combines_question_serialization():
    class MyQuestion(Question):
        def __init__(self, id, answer):
            self.id = id
            self._answer = answer

        @staticmethod
        def is_this_question(tree):
            return True

        def serialize(self):
            return {
                self.id: self._answer
            }

    questions = [MyQuestion("entry.1", "abc"), MyQuestion("entry.2", "cba")]

    expected_payload = {
        "entry.1": "abc",
        "entry.2": "cba",
    }

    assert create_payload(questions) == expected_payload
