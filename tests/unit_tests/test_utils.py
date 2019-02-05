import lxml.etree as etree
from googleform.utils import xpath_freebird_div


def pytest_generate_tests(metafunc):
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
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
