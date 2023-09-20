import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.core import mail
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.ech0211.models import Message
from camac.instance.models import HistoryEntry


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
def test_set_ebau_number(
    db,
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
@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
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
def test_set_ebau_number_workflow(
    db,
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


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        ("Support", status.HTTP_204_NO_CONTENT),
        ("Municipality", status.HTTP_204_NO_CONTENT),
        ("Applicant", status.HTTP_403_FORBIDDEN),
    ],
)
def test_archive(
    db,
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


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,current_form_slug,new_form_slug,expected_status",
    [
        (
            "Support",
            "baugesuch-v2",
            "baugesuch-generell-v2",
            status.HTTP_204_NO_CONTENT,
        ),
        ("Support", "baugesuch", "baugesuch-generell", status.HTTP_204_NO_CONTENT),
        ("Support", "baugesuch", "baugesuch-mit-uvp", status.HTTP_204_NO_CONTENT),
        ("Support", "baugesuch-generell", "baugesuch", status.HTTP_204_NO_CONTENT),
        (
            "Support",
            "baugesuch-generell",
            "baugesuch-mit-uvp",
            status.HTTP_204_NO_CONTENT,
        ),
        ("Support", "baugesuch-mit-uvp", "baugesuch", status.HTTP_204_NO_CONTENT),
        (
            "Support",
            "baugesuch-mit-uvp",
            "baugesuch-generell",
            status.HTTP_204_NO_CONTENT,
        ),
        ("Support", "einfache-vorabklaerung", "baugesuch", status.HTTP_400_BAD_REQUEST),
        ("Support", "baugesuch", "einfache-vorabklaerung", status.HTTP_400_BAD_REQUEST),
        ("Support", "baugesuch", "baugesuch-v2", status.HTTP_400_BAD_REQUEST),
        ("Municipality", "baugesuch", "baugesuch-generell", status.HTTP_204_NO_CONTENT),
    ],
)
def test_change_form(
    db,
    admin_client,
    admin_user,
    caluma_admin_user,
    caluma_workflow_config_be,
    instance,
    instance_with_case,
    instance_service,
    role,
    current_form_slug,
    new_form_slug,
    expected_status,
):
    current_form, _ = caluma_form_models.Form.objects.get_or_create(
        pk=current_form_slug
    )
    new_form, _ = caluma_form_models.Form.objects.get_or_create(pk=new_form_slug)

    workflow = caluma_workflow_models.Workflow.objects.get(pk="building-permit")
    workflow.allow_forms.add(current_form, new_form)

    instance_with_case(instance, form=current_form)

    response = admin_client.post(
        reverse("instance-change-form", args=[instance.pk]),
        {
            "data": {
                "type": "instance-change-forms",
                "id": instance.pk,
                "attributes": {"form": new_form_slug},
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        instance.case.refresh_from_db()

        assert instance.case.document.form_id == new_form_slug


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "service_type,expected_status",
    [
        ("municipality", status.HTTP_204_NO_CONTENT),
        ("construction_control", status.HTTP_204_NO_CONTENT),
        ("invalidtype", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_change_responsible_service(
    db,
    admin_client,
    admin_user,
    be_instance,
    notification_template,
    role,
    group,
    service_factory,
    user_factory,
    user_group_factory,
    application_settings,
    service_type,
    expected_status,
    caluma_admin_user,
    be_distribution_settings,
):
    application_settings["DOSSIER_IMPORT"]["PROD_URL"] = "ebau.local"
    application_settings["ECH0211"]["API_ACTIVE"] = True
    application_settings["NOTIFICATIONS"]["CHANGE_RESPONSIBLE_SERVICE"] = {
        "template_slug": notification_template.slug,
        "recipient_types": ["leitbehoerde"],
    }

    if expected_status == status.HTTP_400_BAD_REQUEST:
        old_service = be_instance.responsible_service()
    else:
        old_service = be_instance.responsible_service(filter_type=service_type)
    new_service = service_factory()

    group.service = old_service
    group.save()

    for task_id in ["submit", "ebau-number"]:
        workflow_api.complete_work_item(
            work_item=be_instance.case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
        )

    # other user is no member of the new service
    other_user = user_factory()
    # admin user is a member of the new service
    user_group_factory(user=admin_user, group__service=new_service)

    init_distribution = caluma_workflow_models.WorkItem.objects.get(
        task_id=be_distribution_settings["DISTRIBUTION_INIT_TASK"],
        case__family=be_instance.case,
    )
    init_distribution.assigned_users = [admin_user.username, other_user.username]
    init_distribution.save()

    assert (
        be_instance.case.work_items.filter(
            status="ready", addressed_groups__contains=[str(old_service.pk)]
        ).count()
        == 7
    )
    assert (
        be_instance.case.work_items.filter(
            status="ready", addressed_groups__contains=[str(new_service.pk)]
        ).count()
        == 0
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

    if expected_status == status.HTTP_204_NO_CONTENT:
        be_instance.refresh_from_db()

        # responsible service changed
        assert not be_instance.instance_services.filter(
            active=1, service=old_service
        ).exists()
        assert be_instance.responsible_service(filter_type=service_type) == new_service

        # notification was sent
        assert len(mail.outbox) == 1
        assert new_service.email in mail.outbox[0].recipients()

        # history entry was created
        history = HistoryEntry.objects.filter(instance=be_instance).last()
        assert (
            history.trans.get(language="de").title
            == f"Neue Leitbehörde: {new_service.trans.get(language='de').name}"
        )

        # caluma work items are reassigned
        assert (
            be_instance.case.work_items.filter(
                status="ready", addressed_groups__contains=[str(old_service.pk)]
            ).count()
            == 0
        )
        assert (
            be_instance.case.work_items.filter(
                status="ready", addressed_groups__contains=[str(new_service.pk)]
            ).count()
            == 7
        )

        assert caluma_workflow_models.WorkItem.objects.filter(
            task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
            status=caluma_workflow_models.WorkItem.STATUS_READY,
            addressed_groups__overlap=[str(new_service.pk)],
        ).exists()

        assert not caluma_workflow_models.WorkItem.objects.filter(
            task_id__in=[
                be_distribution_settings["INQUIRY_CREATE_TASK"],
                be_distribution_settings["INQUIRY_REDO_TASK"],
            ],
            status=caluma_workflow_models.WorkItem.STATUS_READY,
            addressed_groups__overlap=[str(old_service.pk)],
        ).exists()

        # assigned users are filtered
        init_distribution.refresh_from_db()
        assert admin_user.username in init_distribution.assigned_users
        assert other_user.username not in init_distribution.assigned_users
        if service_type == "municipality":
            assert Message.objects.count() == 1
        else:
            assert Message.objects.count() == 0
    elif expected_status == status.HTTP_400_BAD_REQUEST:
        assert (
            response.data[0]["detail"]
            == f"{service_type} is not a valid service type - valid types are: municipality, construction_control"
        )


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "service_type,expected_status",
    [
        ("municipality", status.HTTP_204_NO_CONTENT),
    ],
)
def test_reassign_distribution_and_complete_distribution_workitems(
    db,
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
):
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
def test_change_responsible_service_audit_validation(
    db,
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


@pytest.mark.xfail
@pytest.mark.parametrize(
    "instance__user,service_group__name", [(LazyFixture("admin_user"), "municipality")]
)
@pytest.mark.parametrize("dry", [True, False])
@pytest.mark.parametrize(
    "role__name,instance_state__name,expected_status,expected_work_items",
    [
        ("Support", "subm", status.HTTP_200_OK, ["ebau-number"]),
        (
            "Support",
            "circulation_init",
            status.HTTP_200_OK,
            ["skip-circulation", "init-circulation"],
        ),
        ("Support", "sb1", status.HTTP_200_OK, ["sb1"]),
        ("Municipality", "subm", status.HTTP_403_FORBIDDEN, None),
    ],
)
def test_fix_work_items(
    db,
    admin_client,
    be_instance,
    instance_state,
    service_group,
    snapshot,
    role,
    dry,
    expected_status,
    expected_work_items,
):
    # simulate broken state
    be_instance.case.work_items.all().delete()

    response = admin_client.post(
        reverse("instance-fix-work-items", args=[be_instance.pk]),
        {
            "data": {
                "type": "instance-fix-work-items",
                "attributes": {"dry": dry},
            }
        },
    )

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_200_OK:
        raw_output = response.json()["data"]["attributes"]["output"]

        snapshot.assert_match(raw_output.replace(str(be_instance.pk), "INSTANCE_ID"))

        be_instance.case.refresh_from_db()

        if dry:
            assert be_instance.case.work_items.count() == 0
        else:
            assert sorted(
                be_instance.case.work_items.values_list("task_id", flat=True)
            ) == sorted(expected_work_items)


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        ("Municipality", status.HTTP_200_OK),
        ("Support", status.HTTP_200_OK),
        ("Applicant", status.HTTP_403_FORBIDDEN),
    ],
)
def test_instance_convert_modification(
    admin_client,
    answer_factory,
    be_instance,
    expected_status,
):
    answer_factory(
        question_id="beschreibung-bauvorhaben",
        value="foo",
        document_id=be_instance.case.document.pk,
    )
    answer_factory(
        question_id="projektaenderung",
        value="projektaenderung-ja",
        document_id=be_instance.case.document.pk,
    )
    answer_factory(
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


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
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
def test_correction(
    db,
    admin_client,
    be_instance,
    role,
    active_inquiry_factory,
    instance_state_factory,
    application_settings,
    has_inquiry,
    expected_status,
):
    application_settings["INSTANCE_STATE_CORRECTION_ALLOWED"] = ["subm"]
    instance_state_factory(name="correction")
    instance_state = instance_state_factory(name="subm")
    be_instance.instance_state = instance_state
    be_instance.save()

    be_instance.case.meta["camac-instance-id"] = be_instance.pk
    be_instance.case.save()

    if has_inquiry:
        active_inquiry_factory(be_instance)

    response = admin_client.post(reverse("instance-correction", args=[be_instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        be_instance.refresh_from_db()

        assert be_instance.instance_state.name == "correction"

        response = admin_client.post(
            reverse("instance-correction", args=[be_instance.pk])
        )
        be_instance.refresh_from_db()

        assert response.status_code == expected_status
        assert be_instance.instance_state.name == "subm"
