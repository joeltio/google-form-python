import form
import _internal_util


def get(form_url):
    html = _internal_util.fetch_html(form_url)
    google_form = form.GoogleForm(form_url, html)
    return google_form
