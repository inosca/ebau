import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.permissions.conditions import Always, Never
from camac.permissions.models import InstanceACL
from camac.permissions.switcher import PERMISSION_MODE
from camac.tests.form_utils import FormUtils
from camac.timelines.models import FormTimeline


@pytest.mark.freeze_time("2020-12-03")
@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "ebau_number,expected_ebau_number,expected_error",
    [
        ("2020-2", "2020-2", None),
        ("", "2020-3", None),
        ("20-112", None, "Ungültiges Format"),
        (
            "2020-1",
            None,
            "Diese eBau-Nummer wurde durch eine andere Leitbehörde bereits vergeben",
        ),
        ("2020-112", None, "Diese eBau-Nummer existiert nicht"),
    ],
)
@pytest.mark.django_db
def test_set_ebau_number(
    admin_client,
    caluma_admin_user,
    be_instance,
    instance_with_case,
    role,
    instance_factory,
    instance_service_factory,
    instance_state_factory,
    service_factory,
    ebau_number,
    expected_ebau_number,
    expected_error,
):
    instance_state_factory(name="circulation_init")

    # create existing instance with ebau-number 2020-1 in a different municipality
    instance_other = instance_with_case(
        instance_service_factory(service=service_factory()).instance
    )
    instance_other.case.meta["ebau-number"] = "2020-1"
    instance_other.case.save()

    # create existing instance with ebau-number 2020-2 with same municipality involved
    instance_same = instance_with_case(instance_factory())
    instance_service_factory(
        service=be_instance.responsible_service(filter_type="municipality"),
        instance=instance_same,
        active=0,
    )
    instance_same.case.meta["ebau-number"] = "2020-2"
    instance_same.case.save()

    # instance with different municipality but also ebau-nr 2020-2
    instance_indirect = instance_with_case(
        instance_service_factory(service=service_factory()).instance
    )
    instance_indirect.case.meta["ebau-number"] = "2020-2"
    instance_indirect.case.save()

    # "submit" instance
    workflow_api.skip_work_item(
        work_item=be_instance.case.work_items.get(task_id="submit"),
        user=caluma_admin_user,
    )

    response = admin_client.post(
        reverse("instance-set-ebau-number", args=[be_instance.pk]),
        {
            "data": {
                "type": "instance-set-ebau-numbers",
                "attributes": {"ebau-number": ebau_number},
            }
        },
    )

    if expected_error:
        result = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(result["errors"])
        assert expected_error == result["errors"][0]["detail"]
    else:
        be_instance.case.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert be_instance.case.meta["ebau-number"] == expected_ebau_number


@pytest.mark.freeze_time("2020-12-03")
@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "role__name,expected_status,caluma_workflow,instance_state__name,expected_instance_state,expect_completed_work_item",
    [
        (
            "Municipality",
            status.HTTP_204_NO_CONTENT,
            "building-permit",
            "subm",
            "circulation_init",
            True,
        ),
        (
            "Municipality",
            status.HTTP_204_NO_CONTENT,
            "preliminary-clarification",
            "subm",
            "circulation_init",
            True,
        ),
        (
            "Municipality",
            status.HTTP_204_NO_CONTENT,
            "internal",
            "in_progress_internal",
            "in_progress_internal",
            True,
        ),
        (
            "Municipality",
            status.HTTP_204_NO_CONTENT,
            "building-permit",
            "circulation_init",
            "circulation_init",
            True,
        ),
        (
            "Support",
            status.HTTP_204_NO_CONTENT,
            "building-permit",
            "subm",
            "subm",
            False,
        ),
        (
            "Support",
            status.HTTP_204_NO_CONTENT,
            "preliminary-clarification",
            "subm",
            "subm",
            False,
        ),
        (
            "Support",
            status.HTTP_204_NO_CONTENT,
            "internal",
            "in_progress_internal",
            "in_progress_internal",
            False,
        ),
        (
            "Applicant",
            status.HTTP_403_FORBIDDEN,
            "building-permit",
            "subm",
            None,
            None,
        ),
    ],
)
@pytest.mark.django_db
def test_set_ebau_number_workflow(
    admin_client,
    admin_user,
    caluma_admin_user,
    caluma_workflow_config_be,
    instance,
    instance_service,
    instance_with_case,
    instance_state,
    role,
    instance_state_factory,
    expected_status,
    caluma_workflow,
    expected_instance_state,
    expect_completed_work_item,
    be_ech0211_settings,
):
    instance_state_factory(name="circulation_init")

    instance_with_case(instance, workflow=caluma_workflow)

    workflow_api.skip_work_item(
        work_item=instance.case.work_items.get(task_id="submit"), user=caluma_admin_user
    )

    response = admin_client.post(
        reverse("instance-set-ebau-number", args=[instance.pk]),
        {
            "data": {
                "type": "instance-set-ebau-numbers",
                "attributes": {"ebau-number": ""},
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        instance.case.refresh_from_db()
        instance.refresh_from_db()

        assert instance.instance_state.name == expected_instance_state
        assert instance.case.meta["ebau-number"] == "2020-1"
        assert (
            instance.case.work_items.filter(
                task_id="ebau-number",
                status=caluma_workflow_models.WorkItem.STATUS_COMPLETED,
            ).exists()
            == expect_completed_work_item
        )


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        ("Support", status.HTTP_204_NO_CONTENT),
        ("Municipality", status.HTTP_204_NO_CONTENT),
        ("Applicant", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_archive(
    admin_client,
    be_instance,
    role,
    instance_state_factory,
    expected_status,
):
    instance_state_factory(name="archived")

    response = admin_client.post(reverse("instance-archive", args=[be_instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        be_instance.case.refresh_from_db()
        be_instance.refresh_from_db()

        assert be_instance.case.status == caluma_workflow_models.Case.STATUS_CANCELED
        assert be_instance.instance_state.name == "archived"


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "service_type,expected_status",
    [
        ("municipality", status.HTTP_204_NO_CONTENT),
    ],
)
@pytest.mark.django_db
def test_reassign_distribution_and_complete_distribution_workitems(
    admin_client,
    be_instance,
    group,
    service_factory,
    notification_template,
    application_settings,
    service_type,
    expected_status,
    caluma_admin_user,
    instance_state_factory,
    be_ech0211_settings,
):
    application_settings["SHORT_NAME"] = "be"
    notification_template.slug = "03-verfahren-vorzeitig-beendet"
    notification_template.save()
    application_settings["NOTIFICATIONS"]["CHANGE_RESPONSIBLE_SERVICE"] = {
        "template_slug": notification_template.slug,
        "recipient_types": ["leitbehoerde"],
    }

    old_service = be_instance.responsible_service(filter_type=service_type)
    new_service = service_factory()

    group.service = old_service
    group.save()

    instance_state_factory(name="coordination")

    for task_id in ["submit", "ebau-number"]:
        workflow_api.complete_work_item(
            work_item=be_instance.case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
        )

    work_item = be_instance.case.work_items.get(task_id="distribution")

    workflow_api.complete_work_item(
        work_item=work_item.child_case.work_items.get(task_id="complete-distribution"),
        user=caluma_admin_user,
    )

    distribution_old = be_instance.case.work_items.get(
        addressed_groups__contains=[str(old_service.pk)], task_id="distribution"
    )

    assert distribution_old
    assert distribution_old.status == caluma_workflow_models.WorkItem.STATUS_COMPLETED

    complete_distribution_old = distribution_old.child_case.work_items.get(
        task_id="complete-distribution",
        addressed_groups__contains=[str(old_service.pk)],
    )

    assert complete_distribution_old
    assert (
        complete_distribution_old.status
        == caluma_workflow_models.WorkItem.STATUS_COMPLETED
    )

    response = admin_client.post(
        reverse("instance-change-responsible-service", args=[be_instance.pk]),
        {
            "data": {
                "type": "instance-change-responsible-services",
                "attributes": {"service-type": service_type},
                "relationships": {
                    "to": {"data": {"id": new_service.pk, "type": "services"}}
                },
            }
        },
    )

    assert response.status_code == expected_status

    be_instance.refresh_from_db()

    distribution_new = be_instance.case.work_items.get(
        addressed_groups__contains=[str(new_service.pk)], task_id="distribution"
    )

    assert distribution_new
    assert distribution_new.status == caluma_workflow_models.WorkItem.STATUS_COMPLETED

    complete_distribution_new = distribution_new.child_case.work_items.get(
        task_id="complete-distribution",
        addressed_groups__contains=[str(new_service.pk)],
    )

    assert complete_distribution_new
    assert (
        complete_distribution_new.status
        == caluma_workflow_models.WorkItem.STATUS_COMPLETED
    )


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.django_db
def test_change_responsible_service_audit_validation(
    admin_client,
    be_instance,
    instance_service,
    role,
    service_factory,
    caluma_audit,
    caluma_admin_user,
):
    new_service = service_factory()

    for task_id in ["submit", "ebau-number"]:
        workflow_api.complete_work_item(
            work_item=be_instance.case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
        )

    audit = be_instance.case.work_items.get(task_id="audit")
    invalid_document = caluma_form_models.Document.objects.create(form_id="fp-form")
    table_answer = audit.document.answers.create(
        question_id="fp-form", value=[str(invalid_document.pk)]
    )
    table_answer.documents.add(invalid_document)

    response = admin_client.post(
        reverse("instance-change-responsible-service", args=[be_instance.pk]),
        {
            "data": {
                "type": "instance-change-responsible-services",
                "attributes": {"service-type": "municipality"},
                "relationships": {
                    "to": {"data": {"id": new_service.pk, "type": "services"}}
                },
            }
        },
    )

    result = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert len(result["errors"])
    assert "Ungültige Prüfung" == result["errors"][0]["detail"]


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "role__name,expected_status,is_appeal",
    [
        ("Municipality", status.HTTP_200_OK, False),
        ("Municipality", status.HTTP_403_FORBIDDEN, True),
        ("Support", status.HTTP_200_OK, False),
        ("Applicant", status.HTTP_403_FORBIDDEN, False),
    ],
)
def test_instance_convert_modification(
    admin_client,
    caluma_answer_factory,
    be_instance,
    is_appeal,
    expected_status,
):
    be_instance.case.meta["is-appeal"] = is_appeal
    be_instance.case.save()

    caluma_answer_factory(
        question_id="beschreibung-bauvorhaben",
        value="foo",
        document_id=be_instance.case.document.pk,
    )
    caluma_answer_factory(
        question_id="projektaenderung",
        value="projektaenderung-ja",
        document_id=be_instance.case.document.pk,
    )
    caluma_answer_factory(
        question__slug="beschreibung-projektaenderung",
        value="bar",
        document_id=be_instance.case.document.pk,
    )

    response = admin_client.patch(
        reverse("instance-convert-modification", args=[be_instance.pk]),
        {
            "data": {
                "type": "instance-convert-modifications",
                "id": be_instance.pk,
                "attributes": {"content": "foobar"},
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert (
            be_instance.case.document.answers.filter(
                question_id="beschreibung-bauvorhaben"
            )
            .first()
            .value
            == "foobar"
        )
        assert (
            be_instance.case.document.answers.filter(question_id="projektaenderung")
            .first()
            .value
            == "projektaenderung-nein"
        )
        assert be_instance.case.document.source is None


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "role__name,has_inquiry,expected_status",
    [
        ("Support", False, status.HTTP_200_OK),
        ("municipality-lead", False, status.HTTP_200_OK),
        ("municipality-lead", True, status.HTTP_400_BAD_REQUEST),
        ("Applicant", False, status.HTTP_403_FORBIDDEN),
        ("Municipality", False, status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_correction(
    admin_client,
    be_instance,
    role,
    active_inquiry_factory,
    instance_state_factory,
    has_inquiry,
    expected_status,
    correction_settings,
    mocker,
    timelines_settings,
):
    timelines_settings.enabled = True
    correction_settings["REGENERATE_PDF_ON_CORRECTION"] = True
    instance_state_factory(name="correction")
    instance_state = instance_state_factory(name="subm")
    be_instance.instance_state = instance_state
    be_instance.save()

    regenerate_pdf = mocker.patch(
        "camac.instance.serializers.CalumaInstanceCorrectionSerializer._regenerate_and_store_pdf"
    )

    assert FormTimeline.objects.count() == 0

    if has_inquiry:
        active_inquiry_factory(be_instance)

    response = admin_client.post(reverse("instance-correction", args=[be_instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        be_instance.refresh_from_db()
        regenerate_pdf.assert_not_called()

        timeline = FormTimeline.objects.filter(
            instance=be_instance, timeline_type=FormTimeline.Type.CORRECTION
        ).first()
        assert timeline.end_date is None

        assert be_instance.instance_state.name == "correction"

        response = admin_client.post(
            reverse("instance-correction", args=[be_instance.pk])
        )
        be_instance.refresh_from_db()

        assert response.status_code == expected_status
        assert be_instance.instance_state.name == "subm"
        assert regenerate_pdf.call_count == 1
        assert regenerate_pdf.call_args.args[0].pk == be_instance.pk

        timeline.refresh_from_db()
        assert timeline.end_date is not None


@pytest.mark.freeze_time("2024-06-06 08:00")
@pytest.mark.parametrize(
    "role__name,instance_state__name,expected_status",
    [
        ("Applicant", "new", status.HTTP_204_NO_CONTENT),
        ("Municipality", "new", status.HTTP_403_FORBIDDEN),
        ("Applicant", "subm", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_grant_municipality_access(
    instance,
    admin_client,
    access_level_factory,
    expected_status,
    mocker,
    service,
    admin_user,
    applicant_factory,
):
    applicant_factory(instance=instance, invitee=admin_user)

    mocker.patch(
        "camac.instance.master_data.MasterData.__getattr__", return_value=service.pk
    )

    access_level = access_level_factory(slug="municipality-before-submission")

    url = reverse("instance-grant-municipality-access", args=[instance.pk])

    grant_response = admin_client.post(url)
    assert grant_response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        acl = (
            InstanceACL.currently_active()
            .filter(instance=instance, access_level=access_level, service=service)
            .first()
        )

        assert acl
        assert acl.end_time.isoformat() == "2024-06-06T16:00:00+00:00", (
            '"municipality-before-submission" permission should be revoked automatically 8 hours after creation'
        )

    revoke_response = admin_client.delete(url)
    assert revoke_response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        assert (
            not InstanceACL.currently_active()
            .filter(instance=instance, access_level=access_level, service=service)
            .exists()
        )


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize("allows_changes", [True, False])
@pytest.mark.django_db
def test_additional_demand_changes(
    admin_client,
    gr_instance,
    caluma_case_factory,
    alexandria_document_factory,
    alexandria_mark_factory,
    allows_changes,
    set_application_gr,
    gr_alexandria_settings,
    gr_additional_demand_settings,
    mocker,
    timelines_settings,
):
    timelines_settings.enabled = True
    alexandria_mark_factory(pk="void")
    created_document = alexandria_document_factory(
        metainfo={
            "camac-instance-id": str(gr_instance.pk),
            "system-generated": True,
        }
    )
    old_documents = alexandria_document_factory.create_batch(
        2,
        title=created_document.title,
        metainfo=created_document.metainfo,
    )

    # no marks should exist yet.
    assert created_document.marks.count() == 0
    assert all(
        not old_doc.marks.filter(pk="void").exists() for old_doc in old_documents
    )

    if allows_changes:
        mocker.patch(
            "camac.instance.serializers.CalumaInstanceSubmitSerializer._generate_and_store_pdf",
            return_value=created_document,
        )
        gr_instance.case.meta["additional-demand-changes"] = [
            str(caluma_case_factory().pk)
        ]
        gr_instance.case.save()

    response = admin_client.post(
        reverse("instance-additional-demand-changes-submit", args=[gr_instance.pk])
    )

    if allows_changes:
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # old documents should be marked as void
        assert all(
            old_doc.marks.filter(pk="void").exists() for old_doc in old_documents
        )
        # created document should not be marked as void
        assert created_document.marks.count() == 0
    else:
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "role__name,has_permission,expected_status",
    [
        # Permissions module: Submitting SB1 requires
        # form-sb1-submit permission
        ("Applicant", True, status.HTTP_200_OK),
        ("Applicant", False, status.HTTP_403_FORBIDDEN),
        ("Municipality", True, status.HTTP_200_OK),
        ("Municipality", False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_instance_report_permission_acl_be(
    admin_client,
    admin_user,
    role,
    be_instance,
    access_level,
    mocker,
    instance_acl_factory,
    permissions_settings,
    has_permission,
    expected_status,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL

    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            ("form-sb1-submit", Always() if has_permission else Never()),
        ],
    }

    mocker.patch(
        "camac.instance.serializers.CalumaInstanceReportSerializer.update",
        return_value=be_instance,
    )

    if role.name == "Applicant":
        instance_acl_factory(
            instance=be_instance, user=admin_user, access_level=access_level
        )
    else:
        service = admin_client.user.groups.first().service
        instance_acl_factory(
            instance=be_instance, service=service, access_level=access_level
        )

    response = admin_client.post(
        reverse("instance-report", args=[be_instance.pk]),
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "role__name,has_permission,expected_status",
    [
        # RBAC: Applicants can submit SB1 in instance state "sb1".
        # Muncipality can submit SB1 as instance service on paper instances.
        ("Applicant", True, status.HTTP_200_OK),
        ("Applicant", False, status.HTTP_403_FORBIDDEN),
        ("Municipality", True, status.HTTP_200_OK),
        ("Municipality", False, status.HTTP_403_FORBIDDEN),
        ("Service", True, status.HTTP_403_FORBIDDEN),
        ("Service", False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_instance_report_permission_rbac_be(
    admin_client,
    admin_user,
    role,
    be_instance,
    mocker,
    instance_acl_factory,
    instance_state_factory,
    instance_service_factory,
    applicant_factory,
    active_inquiry_factory,
    application_settings,
    permissions_settings,
    form_utils: FormUtils,
    has_permission,
    expected_status,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF

    service = admin_client.user.groups.first().service
    if role.name == "Applicant":
        applicant_factory(instance=be_instance, invitee=admin_user)
    elif role.name == "Municipality":
        instance_service_factory(instance=be_instance, service=service)
        form_utils.set_is_paper(be_instance.case.document, True)
        application_settings["PAPER"] = {
            "ALLOWED_ROLES": {"DEFAULT": [role.pk]},
            "ALLOWED_SERVICE_GROUPS": {"DEFAULT": [service.service_group.pk]},
        }
    else:
        active_inquiry_factory(
            for_instance=be_instance,
            addressed_service=service,
        )

    instance_state = instance_state_factory(name="sb1")
    if has_permission:
        be_instance.instance_state = instance_state
        be_instance.save()

    mocker.patch(
        "camac.instance.serializers.CalumaInstanceReportSerializer.update",
        return_value=be_instance,
    )

    response = admin_client.post(
        reverse("instance-report", args=[be_instance.pk]),
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "role__name,has_permission,expected_status",
    [
        # Permissions module: Submitting SB2 requires
        # form-sb2-submit permission
        ("Applicant", True, status.HTTP_200_OK),
        ("Applicant", False, status.HTTP_403_FORBIDDEN),
        ("Municipality", True, status.HTTP_200_OK),
        ("Municipality", False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_instance_finalize_permission_acl_be(
    admin_client,
    admin_user,
    role,
    be_instance,
    access_level,
    mocker,
    instance_acl_factory,
    permissions_settings,
    has_permission,
    expected_status,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL

    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            ("form-sb2-submit", Always() if has_permission else Never()),
        ],
    }

    mocker.patch(
        "camac.instance.serializers.CalumaInstanceFinalizeSerializer.update",
        return_value=be_instance,
    )

    if role.name == "Applicant":
        instance_acl_factory(
            instance=be_instance, user=admin_user, access_level=access_level
        )
    else:
        service = admin_client.user.groups.first().service
        instance_acl_factory(
            instance=be_instance, service=service, access_level=access_level
        )

    response = admin_client.post(
        reverse("instance-finalize", args=[be_instance.pk]),
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "role__name,has_permission,expected_status",
    [
        # RBAC: Applicants can submit SB2 in instance state "sb2".
        # Muncipality can submit SB2 as instance service on paper instances.
        ("Applicant", True, status.HTTP_200_OK),
        ("Applicant", False, status.HTTP_403_FORBIDDEN),
        ("Municipality", True, status.HTTP_200_OK),
        ("Municipality", False, status.HTTP_403_FORBIDDEN),
        ("Service", True, status.HTTP_403_FORBIDDEN),
        ("Service", False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_instance_finalize_permission_rbac_be(
    admin_client,
    admin_user,
    role,
    be_instance,
    mocker,
    instance_acl_factory,
    instance_state_factory,
    instance_service_factory,
    applicant_factory,
    active_inquiry_factory,
    application_settings,
    permissions_settings,
    form_utils: FormUtils,
    has_permission,
    expected_status,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF

    service = admin_client.user.groups.first().service
    if role.name == "Applicant":
        applicant_factory(instance=be_instance, invitee=admin_user)
    elif role.name == "Municipality":
        instance_service_factory(instance=be_instance, service=service)
        form_utils.set_is_paper(be_instance.case.document, True)
        application_settings["PAPER"] = {
            "ALLOWED_ROLES": {"DEFAULT": [role.pk]},
            "ALLOWED_SERVICE_GROUPS": {"DEFAULT": [service.service_group.pk]},
        }
    else:
        active_inquiry_factory(
            for_instance=be_instance,
            addressed_service=service,
        )

    instance_state = instance_state_factory(name="sb2")
    if has_permission:
        be_instance.instance_state = instance_state
        be_instance.save()

    mocker.patch(
        "camac.instance.serializers.CalumaInstanceFinalizeSerializer.update",
        return_value=be_instance,
    )

    response = admin_client.post(
        reverse("instance-finalize", args=[be_instance.pk]),
    )

    assert response.status_code == expected_status
