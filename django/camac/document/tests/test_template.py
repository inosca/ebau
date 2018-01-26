import io

import pytest
from django.urls import reverse
from mailmerge import MailMerge
from pytest_factoryboy import LazyFixture
from rest_framework import status

from .data import django_file


@pytest.mark.parametrize("role__name,size", [
    ('Applicant', 0),
    ('Canton', 1),
    ('Service', 1),
    ('Municipality', 1),
])
def test_template_list(admin_client, template, size):
    url = reverse('template-list')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == size
    if size:
        assert json['data'][0]['id'] == str(template.pk)


@pytest.mark.parametrize("role__name", [
    ('Canton'),
])
def test_template_detail(admin_client, template):
    url = reverse('template-detail', args=[template.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("role__name,instance__user,status_code", [
    ('Canton', LazyFixture('user'), status.HTTP_200_OK),
    # service is not assigned to instance so not allowed to build document
    ('Service', LazyFixture('user'), status.HTTP_400_BAD_REQUEST),
])
@pytest.mark.parametrize("template__path,form_field__name", [
    (django_file('template.docx'), 'testname'),
])
def test_template_merge(admin_client, template, instance,
                        instance_locations, form_field, status_code):
    url = reverse('template-merge', args=[template.pk])
    response = admin_client.get(url, data={'instance': instance.pk})
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        docx = MailMerge(io.BytesIO(response.content))
        assert len(docx.get_merge_fields()) == 0
