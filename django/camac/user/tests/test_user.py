from django.core.urlresolvers import reverse
from rest_framework import status


def test_user_anonymous(client):
    url = reverse('user-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_detail(auth_client):
    user = auth_client.user
    url = reverse('user-detail', args=[user.id])

    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
