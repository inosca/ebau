import copy

import pytest
from django.urls import reverse
from rest_framework import status

from camac.document import permissions


@pytest.fixture
def document_permissions():
    before = permissions.PERMISSIONS
    permissions.PERMISSIONS = copy.deepcopy(before)
    yield permissions.PERMISSIONS
    permissions.PERMISSIONS = before


@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize(
    "is_active, is_involved, expect_success",
    # Not all of the combinations make sense, but we
    # wanna test exhaustively nonetheless
    [
        (False, False, False),
        (False, True, True),
        (True, False, False),  # makes no sense, just for completeness
        (True, True, True),
    ],
)
def test_set_geometer_flag(
    # fixtures
    db,
    be_instance,
    set_application_be,
    attachment_factory,
    instance_service_factory,
    instance_factory,
    service_factory,
    admin_client,
    document_permissions,
    attachment_section_factory,
    # params
    is_active,
    is_involved,
    expect_success,
):
    # Parametrisation
    if is_involved:
        # TODO it seems there's allready a correct InstanceService
        # here, no need to add it again. But need to verify
        instance_service_factory(
            instance=be_instance,
            active=is_active,
            service=admin_client.user.get_default_group().service,
        )
    else:
        # move the instances to a new, unrelated service.
        # We shouldn't drop them, as this may cause fallbacks leading
        # to "our" service again, defeating the purpose
        be_instance.instance_services.all().update(service=service_factory())

    # Data setup
    section = attachment_section_factory()
    attachment = attachment_factory(instance=be_instance)
    attachment.attachment_sections.set([section])

    # Patching Env to make settings work
    document_permissions["kt_bern"]["municipality-lead"][
        permissions.AdminServiceBeforeDecisionPermission
    ].append(section.pk)

    url = reverse("attachment-detail", args=[attachment.pk])
    resp = admin_client.patch(
        f"{url}?instance={be_instance.pk}",
        data={
            "data": {
                "id": str(attachment.pk),
                "type": "attachments",
                "attributes": {"context": {"for_geometer": True}},
            },
        },
    )

    if expect_success:
        assert resp.status_code == status.HTTP_200_OK, resp.json()
        assert resp.json()["data"]["attributes"]["context"]["for_geometer"]
    else:
        # response must be in HTTP/40x range
        assert resp.status_code >= status.HTTP_400_BAD_REQUEST
        assert resp.status_code < status.HTTP_500_INTERNAL_SERVER_ERROR
