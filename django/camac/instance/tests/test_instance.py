from django.core.urlresolvers import reverse
from rest_framework import status


def test_instance_list(auth_client, instance):
    url = reverse('instance-list')

    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == 1
    assert json['data'][0]['id'] == str(instance.pk)


def test_instance_detail(auth_client, instance):
    url = reverse('instance-detail', args=[instance.pk])

    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_instance_create(auth_client, form, instance_state):
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

    response = auth_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED

    json = response.json()

    url = reverse('instance-detail', args=[json['data']['id']])
    response = auth_client.patch(url, data=json)
    assert response.status_code == status.HTTP_200_OK

    assert json['data']['attributes']['modification-date'] < (
        response.json()['data']['attributes']['modification-date']
    )
