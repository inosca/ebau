import pytest
from django.urls import reverse
from rest_framework import status

from camac.document import models, permissions


@pytest.mark.parametrize(
    "role__name,attachment_section__allowed_mime_types", [("Municipality", [])]
)
def test_validate_file_name(
    admin_client,
    attachment_section,
    mocker,
    attachment_attachment_sections,
    attachment_attachment_section_factory,
):
    aasa = attachment_attachment_sections.attachment
    aasa.context = {"displayName": "test"}
    aasa.save()

    url = reverse("attachment-detail", args=[aasa.pk])

    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {
            "test": {
                "municipality": {
                    permissions.AdminPermission: [
                        section.pk for section in models.AttachmentSection.objects.all()
                    ]
                }
            }
        },
    )

    data = {
        "data": {
            "type": "attachments",
            "id": aasa.pk,
            "attributes": {"context": {"displayName": "foobar"}},
            "relationships": {
                "attachment-sections": {
                    "data": [
                        {"type": "attachment-sections", "id": attachment_section.pk}
                    ]
                }
            },
        }
    }
    response = admin_client.patch(url, data=data)
    assert response.json()["data"]["attributes"]["context"]["displayName"] == "foobar"

    # Try to rename a file with a invalid name
    data["data"]["attributes"] = {"context": {"displayName": "foo//bar"}}
    response = admin_client.patch(url, data=data)
    assert (
        response.json()["errors"][0]["detail"]
        == "Die eingegebene Bezeichnung ist kein gültiger Dateiname"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
