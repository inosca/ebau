import functools
import mimetypes

import pytest
from django.urls import reverse
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


@pytest.mark.parametrize(
    "role__name,template__path,instance__user,status_code,to_type", [
        (
            'Canton',
            django_file('template.docx'),
            LazyFixture('user'),
            status.HTTP_200_OK,
            'docx'
        ),
        (
            'Canton',
            django_file('template.docx'),
            LazyFixture('user'),
            status.HTTP_200_OK,
            'pdf'
        ),
        (
            'Canton',
            django_file('template.docx'),
            LazyFixture('user'),
            status.HTTP_400_BAD_REQUEST,
            'invalid'
        ),
        # service is not assigned to instance so not allowed to build document
        (
            'Service',
            django_file('template.docx'),
            LazyFixture('user'),
            status.HTTP_400_BAD_REQUEST,
            'docx'
        ),
    ]
)
@pytest.mark.parametrize("form_field__name,instance__identifier,location__name", [  # noqa: 501
    ('testname', '11-18-011', 'Schwyz'),
])
def test_template_merge(admin_client, template, instance, to_type,
                        form_field, status_code, form_field_factory):

    add_field = functools.partial(form_field_factory, instance=instance)
    add_field(name='art-der-befestigten-flache', value='Lagerplatz')
    add_field(name='kategorie-des-vorhabens', value=['Anlage(n)', 'Baute(n)'])
    add_field(
        name='grundeigentumerschaft',
        value=[
            {'name': 'Hans Muster', 'firma': 'Firma Muster'},
            {'name': 'Hans Beispiel', 'firma': 'Firma Beispiel'}
        ]
    )

    url = reverse('template-merge', args=[template.pk])
    response = admin_client.get(url, data={
        'instance': instance.pk,
        'type': to_type,
    })
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert response['Content-Type'] == mimetypes.guess_type(
            'filename.' + to_type)[0]
        if to_type == 'docx':
            expected = django_file('template_result.docx')
            assert len(response.content) == len(expected.file.read()), (
                'Docx template result not equal'
            )
