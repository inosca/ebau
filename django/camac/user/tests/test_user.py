from django.core.urlresolvers import reverse
from rest_framework import status


def test_user_anonymous(client):
    url = reverse('user-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_detail(admin_user, admin_client):
    url = reverse('user-detail', args=[admin_user.id])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
