import json

import pytest
from django.urls import reverse
from document_merge_service.api.data import django_file
from document_merge_service.api.models import Template
from rest_framework import status


@pytest.mark.parametrize(
    "service_id,expected_status",
    [
        ("1", status.HTTP_201_CREATED),
        (None, status.HTTP_403_FORBIDDEN),
        ("10", status.HTTP_403_FORBIDDEN),
    ],
)
def test_custom_create_permission(
    admin_client,
    expected_status,
    mock_services,
    service_id,
):
    response = admin_client.post(
        reverse("template-list"),
        data={
            "slug": "test-slug",
            "template": django_file("docx-template.docx").file,
            "engine": Template.DOCX_TEMPLATE,
            "meta": json.dumps({"service": service_id} if service_id else {}),
        },
        format="multipart",
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "template__engine,template__template",
    [(Template.DOCX_TEMPLATE, django_file("docx-template.docx"))],
)
@pytest.mark.parametrize(
    "template__meta,expected_status",
    [
        ({"service": "1"}, status.HTTP_200_OK),
        ({}, status.HTTP_403_FORBIDDEN),
        ({"service": "10"}, status.HTTP_403_FORBIDDEN),
    ],
)
def test_custom_update_permission(
    admin_client,
    expected_status,
    mock_services,
    template,
):
    response = admin_client.patch(
        reverse("template-detail", args=[template.pk]),
        data={
            "description": "Test",
            "template": django_file("docx-template.docx").file,
            "meta": json.dumps(template.meta),
        },
        format="multipart",
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "template__engine,template__template,template__meta",
    [(Template.DOCX_TEMPLATE, django_file("docx-template.docx"), {})],
)
def test_custom_merge_permission(admin_client, mock_services, template):
    response = admin_client.post(
        reverse("template-merge", args=[template.pk]),
        data={"data": {"test": "Test input"}},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert (
        response.get("content-type")
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
