import requests
from django.conf import settings

from camac.utils import build_url


def convert(from_file, to_type):
    """
    Use docker-unoconv-webservice to convert document to pdf.

    Returns bytes of files or None when conversion failed.

    See: https://github.com/zrrrzzt/tfk-api-unoconv
    """
    url = build_url(settings.UNOCONV_URL, f"/unoconv/{to_type}")

    response = requests.post(url, files={"file": from_file})

    if response.status_code == 200:
        return response.content

    return None
