import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.constants import kt_uri as uri_constants
from camac.core.models import BuildingAuthorityButtonstate, WorkflowEntry
from camac.document import permissions

from .data import django_file


def test_attachment_download_history_list(
    admin_client, attachment_download_history_factory
):
    adhl = attachment_download_history_factory.create_batch(2)
    url = reverse("attachmentdownloadhistory-list")
    response = admin_client.get(url, {"attachment": adhl[0].attachment.pk})

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    print(json)
    assert len(json["data"]) == 1
    assert json["data"][0]["relationships"]["attachment"]["data"]["id"] == str(
        adhl[0].attachment.pk
    )


@pytest.mark.parametrize(
    "instance__user,attachment__path,role__name",
    [(LazyFixture("admin_user"), django_file("multiple-pages.pdf"), "Applicant")],
)
@pytest.mark.parametrize(
    "is_decision,expected_workflow_entries", [(True, 1), (False, 0)]
)
def test_attachment_download_history_create(
    admin_client,
    attachment_attachment_sections,
    role,
    mocker,
    application_settings,
    building_authority_button_factory,
    workflow_item_factory,
    is_decision,
    expected_workflow_entries,
):
    attachment = attachment_attachment_sections.attachment

    if is_decision:
        attachment.context["isDecision"] = True
        attachment.save()

    workflow_item_factory(pk=uri_constants.WORKFLOW_ENTRY_RECEIVED_DECISION)
    building_authority_button_factory(
        pk=uri_constants.BUILDINGAUTHORITY_BUTTON_DECISION
    )
    buttonstate = BuildingAuthorityButtonstate(
        instance=attachment.instance,
        building_authority_button_id=uri_constants.BUILDINGAUTHORITY_BUTTON_DECISION,
        is_clicked=True,
    )
    buttonstate.save()

    application_settings["APPLICANT_GROUP_ID"] = admin_client.user.groups.first().pk

    # fix permissions
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {
            "demo": {
                role.name.lower(): {
                    permissions.AdminPermission: [
                        attachment_attachment_sections.attachmentsection_id
                    ]
                }
            }
        },
    )

    download_url = reverse("attachment-download", args=[attachment.path])
    download_response = admin_client.get(download_url)
    assert download_response.status_code == status.HTTP_200_OK

    histroy_url = reverse("attachmentdownloadhistory-list")
    history_response = admin_client.get(histroy_url)

    assert (
        WorkflowEntry.objects.filter(
            instance=attachment.instance,
            workflow_item_id=uri_constants.WORKFLOW_ENTRY_RECEIVED_DECISION,
        ).count()
        == expected_workflow_entries
    )

    assert history_response.status_code == status.HTTP_200_OK
    json = history_response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["relationships"]["attachment"]["data"]["id"] == str(
        attachment.pk
    )
