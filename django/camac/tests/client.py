import json

from django.core.urlresolvers import reverse
from rest_framework import exceptions, status
from rest_framework.test import APIClient
from rest_framework_jwt.settings import api_settings


class JSONAPIClient(APIClient):
    """Base API client for testing CRUD methods with JSONAPI format."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._content_type = 'application/vnd.api+json'

    def _parse_data(self, data):
        return json.dumps(data) if data else data

    def get(self, path, data=None, **kwargs):
        """Patched GET method to enforce JSONAPI format.
        :param str  path: The URL to call
        :param dict data: The data of the request
        """
        return super().get(
            path=path,
            data=data,
            content_type=self._content_type,
            **kwargs
        )

    def post(self, path, data=None, **kwargs):  # pragma: todo cover
        """Patched POST method to enforce JSONAPI format.
        :param str  path: The URL to call
        :param dict data: The data of the request
        """
        return super().post(
            path=path,
            data=self._parse_data(data),
            content_type=self._content_type,
            **kwargs
        )

    def delete(self, path, data=None, **kwargs):  # pragma: todo cover
        """Patched DELETE method to enforce JSONAPI format.
        :param str  path: The URL to call
        :param dict data: The data of the request
        """
        return super().delete(
            path=path,
            data=self._parse_data(data),
            content_type=self._content_type,
            **kwargs
        )

    def patch(self, path, data=None, **kwargs):  # pragma: todo cover
        """Patched PATCH method to enforce JSONAPI format.
        :param str  path: The URL to call
        :param dict data: The data of the request
        """
        return super().patch(
            path=path,
            data=self._parse_data(data),
            content_type=self._content_type,
            **kwargs
        )

    def login(self, username, password):
        """Authenticate a user.
        :param str username: Username of the user
        :param str password: Password of the user
        :raises:             exceptions.AuthenticationFailed
        """
        data = {
            'data': {
                'attributes': {
                    'username': username,
                    'password': password
                },
                'type': 'obtain-json-web-tokens',
            }
        }

        response = self.post(reverse('login'), data)

        if response.status_code != status.HTTP_200_OK:  # pragma: todo cover
            raise exceptions.AuthenticationFailed()

        self.credentials(
            HTTP_AUTHORIZATION='{0} {1}'.format(
                api_settings.JWT_AUTH_HEADER_PREFIX,
                response.data['token']
            )
        )
