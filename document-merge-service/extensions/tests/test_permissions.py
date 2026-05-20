import json

import pytest
from django.urls import reverse
from rest_framework import status

from document_merge_service.api.data import django_file
from document_merge_service.api.models import Template


@pytest.mark.parametrize(
    ("meta", "mock_service_data", "expected_status"),
    [
        # Regular template
        pytest.param(
            {"service": "1"},
            {},
            status.HTTP_201_CREATED,
            id="regular",
        ),
        pytest.param(
            {"service": "10"},
            {},
            status.HTTP_403_FORBIDDEN,
            id="regular_other",
        ),
        # Shared template
        pytest.param(
            {"service_group": "district"},
            {"is_shared_admin": True},
            status.HTTP_201_CREATED,
            id="shared",
        ),
        pytest.param(
            {"service_group": "district"},
            {},
            status.HTTP_403_FORBIDDEN,
            id="shared_no_admin",
        ),
        pytest.param(
            {"service_group": "something"},
            {"is_shared_admin": True},
            status.HTTP_403_FORBIDDEN,
            id="shared_other",
        ),
        pytest.param(
            {"service_group": "something"},
            {},
            status.HTTP_403_FORBIDDEN,
            id="shared_other_no_admin",
        ),
        # System template
        pytest.param(
            {},
            {"is_support": True},
            status.HTTP_201_CREATED,
            id="system",
        ),
        pytest.param(
            {},
            {},
            status.HTTP_403_FORBIDDEN,
            id="system_no_support",
        ),
    ],
    indirect=["mock_service_data"],
)
def test_custom_create_permission(
    admin_client,
    expected_status,
    meta,
    mock_service_data,
):
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


@pytest.mark.parametrize("action", ["patch", "put"])
@pytest.mark.parametrize(
    ("dms_template__meta", "mock_service_data", "expected_status"),
    [
        # Regular template
        pytest.param(
            {"service": "1"},
            {},
            status.HTTP_200_OK,
            id="regular",
        ),
        # Shared template
        pytest.param(
            {"service_group": "district"},
            {"is_shared_admin": True},
            status.HTTP_200_OK,
            id="shared",
        ),
        pytest.param(
            {"service_group": "district"},
            {},
            status.HTTP_403_FORBIDDEN,
            id="shared_no_admin",
        ),
        # System template
        pytest.param(
            {},
            {"is_support": True},
            status.HTTP_200_OK,
            id="system",
        ),
        pytest.param(
            {},
            {},
            status.HTTP_403_FORBIDDEN,
            id="system_no_support",
        ),
    ],
    indirect=["mock_service_data"],
)
def test_custom_update_permission(
    action,
    admin_client,
    expected_status,
    mock_service_data,
    dms_template,
):
    data = {
        "description": "Test",
        "template": django_file("docx-template.docx").file,
        "meta": json.dumps(dms_template.meta),
    }
    client_fn = getattr(admin_client, action)

    if action == "put":
        # For PUT, we need to pass all attributes as it's not a partial update
        data.update({"slug": dms_template.slug, "engine": dms_template.engine})

    response = client_fn(
        reverse("template-detail", args=[dms_template.pk]),
        data=data,
        format="multipart",
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    ("dms_template__meta", "mock_service_data", "expected_status"),
    [
        # Regular template
        pytest.param(
            {"service": "1"},
            {},
            status.HTTP_204_NO_CONTENT,
            id="regular",
        ),
        # Shared template
        pytest.param(
            {"service_group": "district"},
            {"is_shared_admin": True},
            status.HTTP_204_NO_CONTENT,
            id="shared",
        ),
        pytest.param(
            {"service_group": "district"},
            {},
            status.HTTP_403_FORBIDDEN,
            id="shared_no_admin",
        ),
        # System template
        pytest.param(
            {},
            {"is_support": True},
            status.HTTP_204_NO_CONTENT,
            id="system",
        ),
        pytest.param(
            {},
            {},
            status.HTTP_403_FORBIDDEN,
            id="system_no_support",
        ),
    ],
    indirect=["mock_service_data"],
)
def test_custom_delete_permission(
    admin_client,
    dms_template,
    expected_status,
    mock_service_data,
):
    response = admin_client.delete(
        reverse("template-detail", args=[dms_template.pk]),
    )

    assert response.status_code == expected_status


def test_custom_merge_permission(admin_client, dms_template, mock_service_data):
    response = admin_client.post(
        reverse("template-merge", args=[dms_template.pk]),
        data={"data": {"test": "Test input"}},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert (
        response.get("content-type")
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@pytest.mark.parametrize(
    "mock_service_data",
    [{"is_support": True}],
    indirect=["mock_service_data"],
)
def test_create_permission_support_not_allowed(
    admin_client,
    mock_service_data,
    shared_template_settings,
):
    shared_template_settings["ENABLE_SYSTEM_TEMPLATE_EDITING"] = False

    response = admin_client.post(
        reverse("template-list"),
        data={
            "slug": "test-slug",
            "template": django_file("docx-template.docx").file,
            "engine": Template.DOCX_TEMPLATE,
            "meta": json.dumps({}),
        },
        format="multipart",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
