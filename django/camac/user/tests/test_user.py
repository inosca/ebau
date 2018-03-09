from django.core.urlresolvers import reverse
from rest_framework import status


def test_check_password(admin_user):
    assert admin_user.check_password('password')
    assert not admin_user.check_password('invalid')


def test_me(admin_client, admin_user):
    admin_user.groups.all().delete()
    url = reverse('me')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['data']['attributes']['username'] == admin_user.username
