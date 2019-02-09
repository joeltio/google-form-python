import pytest

from googleform.form import create_response_url


class TestCreateResponseURL:
    def test_url_with_trailing_slash(self):
        url = ("https://docs.google.com/forms/d/e/1FAIpJLSfOjI2wTW7w6DS3QAQF"
               "rMBtj0bJZVGHfjCgxmJgQ9FCXco1Xw/viewform/")
        correct_url = ("https://docs.google.com/forms/d/e/1FAIpJLSfOjI2wTW7w6"
                       "DS3QAQFrMBtj0bJZVGHfjCgxmJgQ9FCXco1Xw/formResponse")
        assert create_response_url(url) == correct_url

    def test_url_without_trailing_slash(self):
        url = ("https://docs.google.com/forms/d/e/1FAIpJLSfOjI2wTW7w6DS3QAQF"
               "rMBtj0bJZVGHfjCgxmJgQ9FCXco1Xw/viewform")
        correct_url = ("https://docs.google.com/forms/d/e/1FAIpJLSfOjI2wTW7w6"
                       "DS3QAQFrMBtj0bJZVGHfjCgxmJgQ9FCXco1Xw/formResponse")
        assert create_response_url(url) == correct_url

    def test_url_with_query(self):
        url = ("https://docs.google.com/forms/d/e/1FAIpJLSfOjI2wTW7w6DS3QAQF"
               "rMBtj0bJZVGHfjCgxmJgQ9FCXco1Xw/viewform?abc=3")
        correct_url = ("https://docs.google.com/forms/d/e/1FAIpJLSfOjI2wTW7w6"
                       "DS3QAQFrMBtj0bJZVGHfjCgxmJgQ9FCXco1Xw/formResponse")
        assert create_response_url(url) == correct_url

    def test_url_with_fragment(self):
        url = ("https://docs.google.com/forms/d/e/1FAIpJLSfOjI2wTW7w6DS3QAQF"
               "rMBtj0bJZVGHfjCgxmJgQ9FCXco1Xw/viewform#asdf")
        correct_url = ("https://docs.google.com/forms/d/e/1FAIpJLSfOjI2wTW7w6"
                       "DS3QAQFrMBtj0bJZVGHfjCgxmJgQ9FCXco1Xw/formResponse")
        assert create_response_url(url) == correct_url

    def test_url_without_viewform_with_trailing_slash(self):
        url = ("https://docs.google.com/forms/d/e/1FAIpJLSfOjI2wTW7w6DS3QAQF"
               "rMBtj0bJZVGHfjCgxmJgQ9FCXco1Xw/")
        correct_url = ("https://docs.google.com/forms/d/e/1FAIpJLSfOjI2wTW7w6"
                       "DS3QAQFrMBtj0bJZVGHfjCgxmJgQ9FCXco1Xw/formResponse")
        assert create_response_url(url) == correct_url

    def test_url_without_viewform_without_trailing_slash(self):
        url = ("https://docs.google.com/forms/d/e/1FAIpJLSfOjI2wTW7w6DS3QAQF"
               "rMBtj0bJZVGHfjCgxmJgQ9FCXco1Xw")
        correct_url = ("https://docs.google.com/forms/d/e/1FAIpJLSfOjI2wTW7w6"
                       "DS3QAQFrMBtj0bJZVGHfjCgxmJgQ9FCXco1Xw/formResponse")
        assert create_response_url(url) == correct_url

    def test_reject_bad_url(self):
        url = "https://docs.google.com/forms/d/e/"

        with pytest.raises(ValueError):
            create_response_url(url)
