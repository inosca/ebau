import io
import itertools
from urllib.parse import parse_qsl

import requests
from django.conf import settings
from docxtpl import DocxTemplate
from rest_framework import exceptions

from camac import jinja
from camac.constants import kt_uri as uri_constants


class DocxRenderer:
    """Render docx templates with the specified data.

    :param path: Path to the template
    :type  path: str
    :param data: Data to render the template with
    :type  data: dict
    """

    def __init__(self, path, data):
        self.path = path

        self.buffer = io.BytesIO()
        doc = DocxTemplate(path)
        doc.render(data, jinja.get_jinja_env())
        doc.save(self.buffer)

    @property
    def buffer(self):
        self.__buffer.seek(0)
        return self.__buffer

    @buffer.setter
    def buffer(self, value):
        self.__buffer = value

    def convert(self, to_type="docx"):
        """Convert template to given format using unoconv.

        See: https://github.com/zrrrzzt/tfk-api-unoconv

        :param to_type: File type to convert the template to.
        :type  to_type: str

        :return: Buffer of converted templated.
        :rtype: io.BytesIO
        """

        if to_type == "docx":
            return self.buffer

        url = build_url(settings.UNOCONV_URL, f"/unoconv/{to_type}")

        response = requests.post(url, files={"file": self.buffer})

        if response.status_code != 200:
            raise exceptions.ParseError(
                f"Unoconv failed to convert document {self.path} to type {to_type}"
            )

        result = io.BytesIO(response.content)
        result.seek(0)

        return result


def flatten(data):
    return list(itertools.chain(*data))


def build_url(*fragments, **options):
    separator = options.get("separator", "/")

    url = separator.join([fragment.strip(separator) for fragment in fragments])

    if options.get("trailing", False):
        url += separator

    return url


def filters(request):
    """Extract Camac NG filters from request.

    The filters are expected to be a URLencoded string (foo=bar&baz=blah).
    """
    return dict(parse_qsl(request.META.get("HTTP_X_CAMAC_FILTERS", "")))


def headers(info):  # pragma: todo cover
    # TODO: Will be included in coverage again in refactoring of caluma extensions.
    """Extract headers from request."""
    return {
        "x-camac-group": info.context.META.get("HTTP_X_CAMAC_GROUP", None),
        "authorization": info.context.META.get("HTTP_AUTHORIZATION", None),
    }


def get_paper_settings(key=None):
    roles = settings.APPLICATION.get("PAPER", {}).get("ALLOWED_ROLES", {})
    service_groups = settings.APPLICATION.get("PAPER", {}).get(
        "ALLOWED_SERVICE_GROUPS", {}
    )

    if isinstance(key, str):
        key = key.upper()

    return {
        "ALLOWED_ROLES": roles.get(key, roles.get("DEFAULT", [])),
        "ALLOWED_SERVICE_GROUPS": service_groups.get(
            key, service_groups.get("DEFAULT", [])
        ),
    }


def get_responsible_koor_service_id(form_id):
    for service_id, forms in uri_constants.RESPONSIBLE_KOORS.items():
        if form_id in forms:
            return service_id

    raise RuntimeError(
        f"No responsible KOOR found for form id {form_id}"
    )  # pragma: no cover
