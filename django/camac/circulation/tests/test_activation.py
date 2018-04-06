import pyexcel
import pytest
from django.core.urlresolvers import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.circulation import serializers


@pytest.mark.parametrize("role__name,instance__user,num_queries,size", [
    ('Applicant', LazyFixture('admin_user'), 7, 1),
    ('Canton', LazyFixture('user'), 7, 1),
    ('Municipality', LazyFixture('user'), 7, 1),
    ('Service', LazyFixture('user'), 7, 1),
])
def test_activation_list(admin_client, activation, size, num_queries,
                         django_assert_num_queries):
    url = reverse('activation-list')

    included = serializers.ActivationSerializer.included_serializers
    with django_assert_num_queries(num_queries):
        response = admin_client.get(
            url, data={'include': ','.join(included.keys())})
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == size
    if size > 0:
        assert json['data'][0]['id'] == str(activation.pk)
        assert len(json['included']) == len(included)


@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
])
def test_activation_detail(admin_client, activation):
    url = reverse('activation-detail', args=[activation.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("role__name", ['Canton'])
def test_instance_export(admin_client, user, activation_factory,
                         django_assert_num_queries):
    url = reverse('activation-export')
    activations = activation_factory.create_batch(2)

    with django_assert_num_queries(7):
        response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    book = pyexcel.get_book(
        file_content=response.content,
        file_type='xlsx'
    )
    # bookdict is a dict of tuples(name, content)
    sheet = book.bookdict.popitem()[1]
    assert len(sheet) == len(activations)
