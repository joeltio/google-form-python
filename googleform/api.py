import form
import utils


def get(form_url):
    html = utils.fetch_html(form_url)
    google_form = form.GoogleForm(form_url, html)
    return google_form
