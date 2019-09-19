import requests
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header


class CalumaClient:
    def __init__(self, auth_token):
        self.auth_token = auth_token

    def query_caluma(self, query, variables=None, add_headers=None):
        variables = variables if variables is not None else {}
        add_headers = add_headers if add_headers is not None else {}
        headers = {"Authorization": self.auth_token}
        headers.update(add_headers)

        response = requests.post(
            settings.CALUMA_URL,
            json={"query": query, "variables": variables},
            headers=headers,
        )

        response.raise_for_status()
        result = response.json()
        if result.get("errors"):  # pragma: no cover
            raise exceptions.ValidationError(
                _("Error while querying caluma: %(errors)s")
                & {"errors": result.get("errors")}
            )

        return result


class CalumaSerializerMixin:
    def query_caluma(self, query, variables=None):
        variables = variables if variables is not None else {}
        client = CalumaClient(get_authorization_header(self.context["request"]))
        return client.query_caluma(query, variables)
