import io

import pytest
from django.urls import reverse
from mailmerge import MailMerge
from rest_framework import status

from .data import django_file


def test_template_list(admin_client, template):
    url = reverse('template-list')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == 1
    assert json['data'][0]['id'] == str(template.pk)


def test_template_detail(admin_client, template):
    url = reverse('template-detail', args=[template.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("role__name,template__path,form_field__name", [
    ('Canton', django_file('template.docx'), 'testname'),
])
def test_template_merge(admin_client, template, instance,
                        instance_locations, form_field):
    url = reverse('template-merge', args=[template.pk])
    response = admin_client.get(url, data={'instance': instance.pk})
    assert response.status_code == status.HTTP_200_OK
    docx = MailMerge(io.BytesIO(response.content))
    assert len(docx.get_merge_fields()) == 0
