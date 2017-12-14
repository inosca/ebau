from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient


def test_user_detail(admin_user):
    url = reverse('user-detail', args=[admin_user.id])

    client = APIClient()
    client.login(username='admin', password='password')

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
