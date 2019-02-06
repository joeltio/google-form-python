import pytest
import os
import json
import lxml.etree as etree

from googleform.questions.base import get_question_title


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
)

QUESTION_INFO = os.path.join(FIXTURE_DIR, "question_info.json")

ALL_QUESTIONS = pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "checkbox.html"),
    os.path.join(FIXTURE_DIR, "date_year_time.html"),
    os.path.join(FIXTURE_DIR, "dropdown.html"),
    os.path.join(FIXTURE_DIR, "duration.html"),
    os.path.join(FIXTURE_DIR, "long_text.html"),
    os.path.join(FIXTURE_DIR, "radio_scale.html"),
    os.path.join(FIXTURE_DIR, "radio_select.html"),
    os.path.join(FIXTURE_DIR, "short_text.html"),
    os.path.join(FIXTURE_DIR, "time.html"),
)


@pytest.mark.datafiles(QUESTION_INFO)
@ALL_QUESTIONS
def test_get_question_title(datafiles):
    question_info_basename = os.path.basename(QUESTION_INFO)
    question_info_filename = next(filter(
        lambda x: x.basename == question_info_basename,
        datafiles.listdir()
    ))

    question_info = json.load(question_info_filename)

    for path in datafiles.listdir():
        # Ignore the question info file
        if path.basename == question_info_basename:
            continue

        with open(path, "r") as f:
            html = f.read()

        tree = etree.HTML(html)
        expected_title = question_info[path.basename]["title"]

        assert get_question_title(tree) == expected_title
