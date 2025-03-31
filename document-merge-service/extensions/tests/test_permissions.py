import json

import pytest
from django.urls import reverse
from rest_framework import status

from document_merge_service.api.data import django_file
from document_merge_service.api.models import Template


@pytest.mark.parametrize(
    "service_id,service_group_slug,is_admin_service,expected_status",
    [
        ("1", None, True, status.HTTP_201_CREATED),
        (None, None, False, status.HTTP_403_FORBIDDEN),
        ("10", None, False, status.HTTP_403_FORBIDDEN),
        (None, "district", True, status.HTTP_201_CREATED),
        (None, "district", False, status.HTTP_403_FORBIDDEN),
        (None, "something", True, status.HTTP_403_FORBIDDEN),
        (None, "something", False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_custom_create_permission(
    admin_client,
    is_admin_service,  # only relevant for shared templates (with service_group)
    expected_status,
    mock_services,
    service_id,
    service_group_slug,
    dms_settings,
):
    meta = {}
    if service_id:
        meta["service"] = service_id
    if service_group_slug:
        meta["service_group"] = service_group_slug

    if is_admin_service:
        dms_settings["SHARED_TEMPLATE_ADMIN_SERVICES_FOR_SERVICE_GROUP"] = {
            "district": ["rsta-test"]
        }
    response = admin_client.post(
        reverse("template-list"),
        data={
            "slug": "test-slug",
            "template": django_file("docx-template.docx").file,
            "engine": Template.DOCX_TEMPLATE,
            "meta": json.dumps(meta),
        },
        format="multipart",
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "template__engine,template__template",
    [(Template.DOCX_TEMPLATE, django_file("docx-template.docx"))],
)
@pytest.mark.parametrize(
    "template__meta,is_admin_service,expected_status",
    [
        ({"service": "1"}, False, status.HTTP_200_OK),
        ({"service_group": "district"}, True, status.HTTP_200_OK),
        ({"service_group": "district"}, False, status.HTTP_403_FORBIDDEN),
        ({}, False, status.HTTP_403_FORBIDDEN),
        ({"service": "10"}, False, status.HTTP_403_FORBIDDEN),
        ({"service_group": "something"}, True, status.HTTP_404_NOT_FOUND),
        ({"service_group": "something"}, False, status.HTTP_404_NOT_FOUND),
    ],
)
def test_custom_update_permission(
    admin_client,
    is_admin_service,  # only relevant for shared templates (with service_group)
    expected_status,
    mock_services,
    template,
    dms_settings,
):
    if is_admin_service:
        dms_settings["SHARED_TEMPLATE_ADMIN_SERVICES_FOR_SERVICE_GROUP"] = {
            "district": ["rsta-test"]
        }
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
    "template__engine,template__template",
    [(Template.DOCX_TEMPLATE, django_file("docx-template.docx"))],
)
@pytest.mark.parametrize(
    "template__meta,is_admin_service,expected_status",
    [
        ({"service": "1"}, False, status.HTTP_204_NO_CONTENT),
        ({}, False, status.HTTP_403_FORBIDDEN),
        ({"service_group": "district"}, True, status.HTTP_204_NO_CONTENT),
        ({"service_group": "district"}, False, status.HTTP_403_FORBIDDEN),
        ({"service": "10"}, False, status.HTTP_404_NOT_FOUND),
        ({"service_group": "something"}, True, status.HTTP_404_NOT_FOUND),
        ({"service_group": "something"}, False, status.HTTP_404_NOT_FOUND),
    ],
)
def test_custom_delete_permission(
    admin_client,
    is_admin_service,  # only relevant for shared templates (with service_group)
    expected_status,
    mock_services,
    template,
    dms_settings,
):
    if is_admin_service:
        dms_settings["SHARED_TEMPLATE_ADMIN_SERVICES_FOR_SERVICE_GROUP"] = {
            "district": ["rsta-test"]
        }
    response = admin_client.delete(
        reverse("template-detail", args=[template.pk]),
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
