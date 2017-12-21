import pytest
from django.core.urlresolvers import reverse
from rest_framework import status


def test_form_field_list(auth_client, form_field):
    url = reverse('form-field-list')

    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == 1
    assert json['data'][0]['id'] == str(form_field.pk)


@pytest.mark.parametrize("form_field__value", [["Test1", "Test2"]])
def test_form_field_detail(auth_client, form_field, form_field__value):
    url = reverse('form-field-detail', args=[form_field.pk])

    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert response.json()['data']['attributes']['value'] == form_field__value


def test_form_field_create(auth_client, instance):
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

    response = auth_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED
