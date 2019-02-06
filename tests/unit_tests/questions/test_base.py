import pytest
import os
import json
import lxml.etree as etree

from googleform.questions.base import (
    get_question_title, get_question_desc, get_question_id,
    Question,
)


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
)


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
def question_trees(question_paths):
    trees = {}

    for path in question_paths:
        with open(path, "r") as f:
            html = f.read()

        basename = os.path.basename(path)
        trees[basename] = etree.HTML(html)

    return trees


@pytest.fixture(scope="module")
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


def test_get_question_id(question_trees, question_info):
    for basename, tree in question_trees.items():
        expected_id = question_info[basename]["id"]

        assert get_question_id(tree) == expected_id


class TestQuestion:
    @pytest.fixture(scope="class")
    def working_question(self):
        class MyQuestion(Question):
            @staticmethod
            def is_this_question(tree):
                return True

            def serialize(self):
                pass

        return MyQuestion

    def assert_fail_class_instantiation(self, question_trees, klass):
        for tree in question_trees.values():
            with pytest.raises(TypeError):
                klass(tree)

    def test_is_abstract(self, question_trees):
        self.assert_fail_class_instantiation(question_trees, Question)

    def test_requires_is_this_question_method(self, question_trees):
        class MyQuestion(Question):
            def serialize(self):
                pass

        self.assert_fail_class_instantiation(question_trees, MyQuestion)

    @pytest.mark.xfail(reason="abc does not enforce function signatures")
    def test_requires_is_this_question_static_method(self, question_trees):
        class MyQuestion(Question):
            def is_this_question(self):
                pass

            def serialize(self):
                pass

        self.assert_fail_class_instantiation(question_trees, MyQuestion)

    def test_requires_serialize_method(self, question_trees):
        class MyQuestion(Question):
            @staticmethod
            def is_this_question(tree):
                pass

        self.assert_fail_class_instantiation(question_trees, MyQuestion)

    def test_get_tree(self, working_question, question_trees, question_info):
        for basename, tree in question_trees.items():
            question = working_question(tree)

            assert question.tree == tree

    def test_get_title(self, working_question, question_trees, question_info):
        for basename, tree in question_trees.items():
            question = working_question(tree)

            expected_title = question_info[basename]["title"]
            assert question.title == expected_title

    def test_get_desc(self, working_question, question_trees, question_info):
        for basename, tree in question_trees.items():
            question = working_question(tree)

            expected_desc = question_info[basename]["description"]
            assert question.description == expected_desc

    def test_get_id(self, working_question, question_trees, question_info):
        for basename, tree in question_trees.items():
            question = working_question(tree)

            expected_id = question_info[basename]["id"]
            assert question.id == expected_id
