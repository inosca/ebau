from functools import partial

import pytest
from alexandria.core import models as alexandria_models
from django.apps import apps
from django.core.management import call_command
from django.urls import reverse

from camac.document.models import AttachmentSection
from camac.permissions.switcher import PERMISSION_MODE


@pytest.mark.freeze_time("2025-11-22")
@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize("instance_state__name", ["subm"])
def test_document_visibilities_camac(
    db,
    set_document_backend,
    attachment_factory,
    be_instance,
    set_application_be,
    admin_user,
    user_factory,
    service_factory,
    admin_client,
    settings,
):
    set_document_backend("camac-ng")
    # We need the BE document sections
    call_command("loaddata", settings.ROOT_DIR("kt_bern/config/document.json"))

    # make instance accessible to our user
    user_service = admin_user.get_default_group().service
    be_instance.responsible_services.create(
        service=user_service, responsible_user=admin_user
    )

    # We create a bunch of attachments, some of which our user is allowed
    # to see, and some not.
    # Basically, ensure the switching endpoint uses the same permissions
    # as the old document endpoint
    #

    internal = AttachmentSection.objects.get(trans__name="Intern")
    all_involved = AttachmentSection.objects.get(trans__name="Alle Beteiligten")
    submission_docs = AttachmentSection.objects.get(trans__name="Beilagen zum Gesuch")

    doc_a0 = attachment_factory(instance=be_instance)
    doc_s0 = attachment_factory(instance=be_instance)
    doc_i0 = attachment_factory(instance=be_instance, service=service_factory())
    doc_i1 = attachment_factory(instance=be_instance, service=user_service)
    doc_a0.attachment_sections.set([all_involved])
    doc_s0.attachment_sections.set([submission_docs])
    doc_i0.attachment_sections.set([internal])
    doc_i1.attachment_sections.set([internal])

    url = reverse("ech-document-list")

    # While we're at it, verify that pagination is enforced
    unpaginated_data = admin_client.get(url, {"include": "category"}).json()
    assert unpaginated_data["errors"][0]["detail"] == "Pagination is required"

    ech_docs = admin_client.get(url, {"include": "category", "page[number]": 1}).json()

    # We (municipality) should be able to see the internal (only own service),
    # submission docs and everything in "all involved". Note we're not fully
    # testing the visibility here, just making sure they're "in the loop"
    expected_pks = [
        f"{all_involved.pk}-{doc_a0.pk}",
        f"{submission_docs.pk}-{doc_s0.pk}",
        f"{internal.pk}-{doc_i1.pk}",
    ]

    received_ids = [doc["id"] for doc in ech_docs["data"]]

    assert sorted(expected_pks) == sorted(received_ids)

    # Just ensure (only) the expected categories show up in the included objects
    received_categories = sorted(
        [
            obj["id"]
            for obj in ech_docs["included"]
            if obj["type"] == "ech0211-document-categories"
        ]
    )

    expected_categories = sorted(
        [
            str(internal.pk),
            str(all_involved.pk),
            str(submission_docs.pk),
        ]
    )

    assert received_categories == expected_categories


@pytest.mark.freeze_time("2025-11-22")
@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize("instance_state__name", ["subm"])
def test_document_visibilities_alexandria(
    db,
    set_document_backend,
    instance_acl_factory,
    be_instance,
    admin_user,
    user_factory,
    be_alexandria_settings,
    be_permissions_settings,
    group_factory,
    service_factory,
    admin_client,
    settings,
    be_access_levels,
    alexandria_document_factory,
):
    # Setup environment correctly:
    # - enable full permission mode
    # - use Alexandria permissions v2
    be_permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL

    set_document_backend("alexandria")
    call_command("loaddata", settings.ROOT_DIR("kt_bern/config/alexandria_core.json"))
    settings.GENERIC_PERMISSIONS_PERMISSION_CLASSES = [
        "camac.alexandria.extensions.permissions_v2.AlexandriaPermissions"
    ]
    apps.get_app_config("generic_permissions").ready()

    # Setup the instance (more-or-less) correctly:
    # - set user's service as responsible service
    # - add a lead-authority ACL
    user_service = admin_user.get_default_group().service
    be_instance.responsible_services.create(
        service=user_service, responsible_user=admin_user
    )
    instance_acl_factory(
        instance=be_instance,
        service=user_service,
        access_level_id="lead-authority",
        grant_type="SERVICE",
    )

    user_group = admin_user.get_default_group()

    internal = alexandria_models.Category.objects.get(slug="intern")
    all_involved = alexandria_models.Category.objects.get(slug="alle-beteiligten")
    plans = alexandria_models.Category.objects.get(
        slug="beilagen-zum-gesuch-projektplaene"
    )

    doc_factory = partial(
        alexandria_document_factory, metainfo={"camac-instance-id": be_instance.pk}
    )

    # yeah "group" here means service. I don't make the rules
    int_own = doc_factory(category=internal, created_by_group=user_group.service_id)
    int_other = doc_factory(
        category=internal, created_by_group=group_factory().service_id
    )
    plan0 = doc_factory(category=plans, created_by_user=user_factory().pk)
    inv0 = doc_factory(category=all_involved, created_by_user=user_factory().pk)

    url = reverse("ech-document-list")
    ech_docs = admin_client.get(url, {"include": "category", "page[number]": 1}).json()
    assert ech_docs["data"]

    received_ids = [doc["id"] for doc in ech_docs["data"]]

    assert str(inv0.pk) in received_ids
    assert str(plan0.pk) in received_ids
    assert str(int_own.pk) in received_ids

    assert str(int_other.pk) not in received_ids
