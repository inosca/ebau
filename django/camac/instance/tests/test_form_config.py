from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_str
from rest_framework import status


def test_form_config_get(admin_client):
    url = reverse('form-config-download')
    config = settings.APPLICATION_DIR.file('form.json')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert force_str(response.content) == config.read()
