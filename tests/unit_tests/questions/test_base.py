import pytest

from googleform.questions.base import (
    get_question_title, get_question_desc, get_question_id,
    Question,
)


def test_get_question_title(all_questions):
    for question in all_questions:
        test_title = get_question_title(question["tree"])
        expected_title = question["title"]

        assert test_title == expected_title


def test_get_question_desc(all_questions):
    for question in all_questions:
        test_desc = get_question_desc(question["tree"])
        expected_desc = question["description"]

        assert test_desc == expected_desc


def test_get_question_id(all_questions):
    for question in all_questions:
        test_id = get_question_id(question["tree"])
        expected_id = question["id"]

        assert test_id == expected_id


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

    @pytest.fixture(scope="class")
    def all_question_trees(self, all_questions):
        return list(map(lambda x: x["tree"], all_questions))

    def assert_fail_class_instantiation(self, all_question_trees, klass):
        for tree in all_question_trees:
            with pytest.raises(TypeError):
                klass(tree)

    def test_is_abstract(self, all_question_trees):
        self.assert_fail_class_instantiation(all_question_trees, Question)

    def test_requires_is_this_question_method(self, all_question_trees):
        class MyQuestion(Question):
            def serialize(self):
                pass

        self.assert_fail_class_instantiation(all_question_trees, MyQuestion)

    @pytest.mark.xfail(reason="abc does not enforce function signatures")
    def test_requires_is_this_question_static_method(self, all_question_trees):
        class MyQuestion(Question):
            def is_this_question(self):
                pass

            def serialize(self):
                pass

        self.assert_fail_class_instantiation(all_question_trees, MyQuestion)

    def test_requires_serialize_method(self, all_question_trees):
        class MyQuestion(Question):
            @staticmethod
            def is_this_question(tree):
                pass

        self.assert_fail_class_instantiation(all_question_trees, MyQuestion)

    def test_get_tree(self, working_question, all_question_trees):
        for tree in all_question_trees:
            question = working_question(tree)
            assert question.tree == tree

    def test_get_title(self, working_question, all_questions):
        for question in all_questions:
            question_obj = working_question(question["tree"])
            assert question_obj.title == question["title"]

    def test_get_desc(self, working_question, all_questions):
        for question in all_questions:
            question_obj = working_question(question["tree"])
            assert question_obj.description == question["description"]

    def test_get_id(self, working_question, all_questions):
        for question in all_questions:
            question_obj = working_question(question["tree"])
            assert question_obj.id == question["id"]

    def test_is_required(self, working_question, all_questions):
        for question in all_questions:
            question_obj = working_question(question["tree"])
            assert question_obj.is_required == question["is_required"]
