import pytest
from django.core.urlresolvers import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.instance import serializers


@pytest.mark.parametrize("role__name,instance__user,num_queries,size", [
    ('Applicant', LazyFixture('admin_user'), 9, 1),
    ('Canton', LazyFixture('user'), 9, 1),
    ('Municipality', LazyFixture('user'), 9, 1),
    ('Service', LazyFixture('user'), 9, 1),
    ('Unknown', LazyFixture('user'), 2, 0),
])
def test_instance_list(admin_client, instance, instance_locations, activation,
                       size, num_queries, django_assert_num_queries):
    url = reverse('instance-list')

    included = serializers.InstanceSerializer.included_serializers
    with django_assert_num_queries(num_queries):
        response = admin_client.get(url, data={
            'include': ','.join(included.keys())
        })
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == size
    if size > 0:
        assert json['data'][0]['id'] == str(instance.pk)
        # included previous_instance_state and instance_state are the same
        assert len(json['included']) == len(included) - 1


@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
])
def test_instance_detail(admin_client, instance):
    url = reverse('instance-detail', args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
    ('Canton', LazyFixture('user')),
    ('Municipality', LazyFixture('user')),
    ('Service', LazyFixture('user')),
    ('Unknown', LazyFixture('user')),
])
def test_instance_update(admin_client, instance):
    url = reverse('instance-detail', args=[instance.pk])

    response = admin_client.patch(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
    ('Canton', LazyFixture('user')),
    ('Municipality', LazyFixture('user')),
    ('Service', LazyFixture('user')),
    ('Unknown', LazyFixture('user')),
])
def test_instance_destroy(admin_client, instance):
    url = reverse('instance-detail', args=[instance.pk])

    response = admin_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("role__name,status_code", [
    ('Applicant', status.HTTP_201_CREATED),
    ('Canton', status.HTTP_403_FORBIDDEN),
    ('Municipality', status.HTTP_403_FORBIDDEN),
    ('Service', status.HTTP_403_FORBIDDEN),
])
def test_instance_create(admin_client, admin_user, form, instance_state,
                         status_code):
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
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        json = response.json()

        url = reverse('instance-list')
        response = admin_client.post(url, data=json)
        assert response.status_code == status.HTTP_201_CREATED

        assert json['data']['attributes']['modification-date'] < (
            response.json()['data']['attributes']['modification-date']
        )
