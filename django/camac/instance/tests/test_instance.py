import pytest
from django.core.urlresolvers import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status


@pytest.mark.parametrize("role__name,instance__user,size", [
    ('Applicant', LazyFixture('admin_user'), 1),
    ('Canton', LazyFixture('user'), 1),
    ('Municipality', LazyFixture('user'), 1),
    ('Service', LazyFixture('user'), 1),
    ('Unknown', LazyFixture('user'), 0),
])
def test_instance_list(admin_client, instance, instance_locations, activation,
                       size):
    url = reverse('instance-list')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == size
    if size > 0:
        assert json['data'][0]['id'] == str(instance.pk)


@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
])
def test_instance_detail(admin_client, instance):
    url = reverse('instance-detail', args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("role__name", [
    'Applicant',
])
def test_instance_create(admin_client, admin_user, form, instance_state):
    url = reverse('instance-list')

    data = {
        'data': {
            'type': 'instances',
            'id': None,
            'relationships': {
                'form': {
                    'data': {
                        'type': 'forms',
                        'id': form.pk
                    }
                },
            }
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED

    json = response.json()

    url = reverse('instance-detail', args=[json['data']['id']])
    response = admin_client.patch(url, data=json)
    assert response.status_code == status.HTTP_200_OK

    assert json['data']['attributes']['modification-date'] < (
        response.json()['data']['attributes']['modification-date']
    )
