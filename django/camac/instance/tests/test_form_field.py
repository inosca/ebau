import pytest
from django.core.urlresolvers import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status


@pytest.mark.parametrize("role__name,instance__user,size", [
    ('Applicant', LazyFixture('admin_user'), 1),
    ('Unknown', LazyFixture('user'), 0),
])
def test_form_field_list(admin_client, form_field, size):
    url = reverse('form-field-list')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == size
    if size > 0:
        assert json['data'][0]['id'] == str(form_field.pk)


@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
])
@pytest.mark.parametrize("form_field__value", [["Test1", "Test2"]])
def test_form_field_detail(admin_client, form_field, form_field__value):
    url = reverse('form-field-detail', args=[form_field.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert response.json()['data']['attributes']['value'] == form_field__value


@pytest.mark.parametrize("role__name,instance_state__name,instance__user,status_code", [  # noqa: E501
    ('Applicant', 'new', LazyFixture('admin_user'), status.HTTP_200_OK),
    ('Applicant', 'new', LazyFixture('user'), status.HTTP_404_NOT_FOUND),
    ('Applicant', 'comm', LazyFixture('admin_user'), status.HTTP_403_FORBIDDEN)
])
def test_form_field_update(admin_client, form_field, status_code):
    url = reverse('form-field-detail', args=[form_field.pk])

    response = admin_client.patch(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("role__name,instance__user,status_code", [
    ('Applicant', LazyFixture('admin_user'), status.HTTP_201_CREATED),
    ('Applicant', LazyFixture('user'), status.HTTP_400_BAD_REQUEST),
])
def test_form_field_create(admin_client, instance, status_code):
    url = reverse('form-field-list')

    data = {
        'data': {
            'type': 'form-fields',
            'id': None,
            'attributes': {
                'name': 'Test',
                'value': ['Test1', 'Test2']
            },
            'relationships': {
                'instance': {
                    'data': {
                        'type': 'instances',
                        'id': instance.pk
                    }
                },
            }
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status_code


@pytest.mark.parametrize("instance_state__name", [
    'new'
])
@pytest.mark.parametrize("role__name,instance__user,status_code", [
    ('Applicant', LazyFixture('admin_user'), status.HTTP_204_NO_CONTENT),
    ('Canton', LazyFixture('user'), status.HTTP_403_FORBIDDEN),
])
def test_form_field_destroy(admin_client, form_field, status_code):
    url = reverse('form-field-detail', args=[form_field.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code
