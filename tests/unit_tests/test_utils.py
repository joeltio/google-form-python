import lxml.etree as etree
from googleform.utils import xpath_freebird_div


class TestXPathFreebirdDiv:
    def test_does_not_contain(self):
        html = "<div><div></div></div>"
        tree = etree.fromstring(html)

        result = xpath_freebird_div(tree, "abc")

        assert result == []

    def test_wrong_class_suffix(self):
        html = "<div><div class='freebirdFormviewerViewItemscba'></div></div>"
        tree = etree.fromstring(html)

        result = xpath_freebird_div(tree, "abc")

        assert result == []

    def test_different_tag(self):
        html = """<div>
            <label class='freebirdFormviewerViewItemsabc'></label>
        </div>"""
        tree = etree.fromstring(html)

        result = xpath_freebird_div(tree, "abc")

        assert result == []

    def test_valid(self):
        html = "<div><div class='freebirdFormviewerViewItemsabc'></div></div>"
        tree = etree.fromstring(html)

        result = xpath_freebird_div(tree, "abc")

        assert len(result) == 1

    def test_not_exact_by_default(self):
        html = """<div>
            <div class='freebirdFormviewerViewItemsabc foo'></div>
        </div>"""
        tree = etree.fromstring(html)

        result = xpath_freebird_div(tree, "abc")

        assert len(result) == 1

    def test_exact_class_with_multiple_classes(self):
        html = """<div>
            <div class='freebirdFormviewerViewItemsabc foo'></div>
        </div>"""
        tree = etree.fromstring(html)

        result = xpath_freebird_div(tree, "abc", exact=True)

        assert result == []

    def test_exact_class_valid(self):
        html = """<div>
            <div class='freebirdFormviewerViewItemsabc'></div>
        </div>"""
        tree = etree.fromstring(html)

        result = xpath_freebird_div(tree, "abc", exact=True)

        assert len(result) == 1
