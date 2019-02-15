from googleform import form
from googleform import utils


def get(form_url):
    html = utils.fetch_html(form_url)
    google_form = form.GoogleForm(html)
    return google_form
