import lxml.etree as etree
from googleform.utils import (
    xpath_freebird_div, has_freebird_div,
    eval_map, get_elements_text,
)


def pytest_generate_tests(metafunc):
    try:
        funcarglist = metafunc.cls.params[metafunc.function.__name__]
    except AttributeError:
        return

    argnames = sorted(funcarglist[0])
    metafunc.parametrize(argnames, [
        [funcargs[name] for name in argnames]
        for funcargs in funcarglist])


def make_freebird_tree(class_name="", inner_tag="div"):
    class_attribute = "class='freebirdFormviewerViewItems{}'".format(
        class_name)

    if not class_name:
        class_attribute = ""

    html = """<div>
        <{0} {1}></{0}>
    </div>""".format(inner_tag, class_attribute)

    return etree.fromstring(html)


class TestXPathFreebirdDiv:
    params = {
        "test_does_not_contain": [
            dict(tree=make_freebird_tree(), find_name="foo"),
            dict(tree=make_freebird_tree("bar"), find_name="foo"),
            dict(tree=make_freebird_tree("foo", "label"), find_name="foo"),
        ],
        "test_valid": [
            dict(tree=make_freebird_tree("foo"), find_name="foo"),
        ],
        "test_not_exact_by_default": [
            dict(tree=make_freebird_tree("foo bar"), find_name="foo"),
        ],
        "test_exact_class_invalid": [
            dict(tree=make_freebird_tree("foo bar"), find_name="foo"),
        ],
        "test_exact_class_valid": [
            dict(tree=make_freebird_tree("foo"), find_name="foo"),
        ]
    }

    def test_does_not_contain(self, tree, find_name):
        result = xpath_freebird_div(tree, find_name)

        assert result == []

    def test_valid(self, tree, find_name):
        result = xpath_freebird_div(tree, find_name)

        assert len(result) == 1

    def test_not_exact_by_default(self, tree, find_name):
        result = xpath_freebird_div(tree, find_name)

        assert len(result) == 1

    def test_exact_class_invalid(self, tree, find_name):
        result = xpath_freebird_div(tree, find_name, exact=True)

        assert result == []

    def test_exact_class_valid(self, tree, find_name):
        result = xpath_freebird_div(tree, find_name, exact=True)

        assert len(result) == 1


class TestHasFreebirdDiv:
    params = {
        "test_does_not_contain": [
            dict(tree=make_freebird_tree(), find_name="foo"),
            dict(tree=make_freebird_tree("bar"), find_name="foo"),
            dict(tree=make_freebird_tree("foo", "label"), find_name="foo"),
        ],
        "test_valid": [
            dict(tree=make_freebird_tree("foo"), find_name="foo"),
        ],
        "test_not_exact_by_default": [
            dict(tree=make_freebird_tree("foo bar"), find_name="foo"),
        ],
        "test_exact_class_invalid": [
            dict(tree=make_freebird_tree("foo bar"), find_name="foo"),
        ],
        "test_exact_class_valid": [
            dict(tree=make_freebird_tree("foo"), find_name="foo"),
        ]
    }

    def test_does_not_contain(self, tree, find_name):
        result = has_freebird_div(tree, find_name)

        assert result is False

    def test_valid(self, tree, find_name):
        result = has_freebird_div(tree, find_name)

        assert result is True

    def test_not_exact_by_default(self, tree, find_name):
        result = has_freebird_div(tree, find_name)

        assert result is True

    def test_exact_class_invalid(self, tree, find_name):
        result = has_freebird_div(tree, find_name, exact=True)

        assert result is False

    def test_exact_class_valid(self, tree, find_name):
        result = has_freebird_div(tree, find_name, exact=True)

        assert result is True


class TestEvalMap:
    def test_eval_map_default_as_list(self):
        assert eval_map(lambda x: x*3, range(3)) == [0, 3, 6]

    def test_eval_map_as_list(self):
        assert eval_map(lambda x: x*2, range(3), as_tuple=False) == [0, 2, 4]

    def test_eval_map_as_tuple(self):
        assert eval_map(lambda x: x, range(3), as_tuple=True) == (0, 1, 2)


def test_get_elements_text():
    html = """<div>
        <label class='foo'>ABC</label>
        <div class='foo'>Item 1</div>
        <div class='foo'>Item 2</div>
        <div class='foo'>Item 3</div>
    </div>"""

    tree = etree.fromstring(html)
    xpath = ".//div[@class='foo']"

    assert get_elements_text(tree, xpath) == ["Item 1", "Item 2", "Item 3"]
    assert get_elements_text(tree, xpath, as_tuple=False) == \
        ["Item 1", "Item 2", "Item 3"]
    assert get_elements_text(tree, xpath, as_tuple=True) == \
        ("Item 1", "Item 2", "Item 3")
