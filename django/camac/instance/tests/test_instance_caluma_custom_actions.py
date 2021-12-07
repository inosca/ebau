import pathlib

import pyexcel
import pytest
from caluma.caluma_form import api as form_api, models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from caluma.caluma_workflow.models import Task
from django.core import mail
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.caluma.api import CalumaApi
from camac.constants import kt_bern as constants
from camac.instance.models import HistoryEntry


@pytest.fixture
def ebau_number_question(db, camac_question_factory, camac_chapter_factory):
    camac_question_factory(question_id=constants.QUESTION_EBAU_NR)
    camac_chapter_factory(chapter_id=constants.CHAPTER_EBAU_NR)


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
    ebau_number_question,
    camac_answer_factory,
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
    camac_answer_factory(
        instance=instance_other,
        question_id=constants.QUESTION_EBAU_NR,
        chapter_id=constants.CHAPTER_EBAU_NR,
        answer="2020-1",
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
    camac_answer_factory(
        instance=instance_same,
        question_id=constants.QUESTION_EBAU_NR,
        chapter_id=constants.CHAPTER_EBAU_NR,
        answer="2020-2",
    )
    instance_same.case.meta["ebau-number"] = "2020-2"
    instance_same.case.save()

    # instance with different municipality but also ebau-nr 2020-2
    instance_indirect = instance_with_case(
        instance_service_factory(service=service_factory()).instance
    )
    camac_answer_factory(
        instance=instance_indirect,
        question_id=constants.QUESTION_EBAU_NR,
        chapter_id=constants.CHAPTER_EBAU_NR,
        answer="2020-2",
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
    ebau_number_question,
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
    "instance_state__name,should_sync", [("circulation", True), ("sb1", False)]
)
def test_change_responsible_service_circulations(
    db,
    admin_client,
    role,
    be_instance,
    instance_state,
    service_factory,
    circulation_factory,
    activation_factory,
    work_item_factory,
    should_sync,
    caluma_admin_user,
):
    old_service = be_instance.responsible_service()
    sub_service = service_factory(service_parent=old_service)
    new_service = service_factory()
    some_service = service_factory()

    c1 = circulation_factory(instance=be_instance, service=old_service)
    c2 = circulation_factory(instance=be_instance, service=old_service)

    # from the old service to some service, stays
    a1 = activation_factory(circulation=c1, service_parent=old_service)
    # from some other service to some other service, stays
    a2 = activation_factory(circulation=c1, service_parent=some_service)
    # should be deleted since the new service is now responsible
    a3 = activation_factory(
        circulation=c1, service_parent=old_service, service=new_service
    )
    # should be deleted since it's to a sub service of the old services
    activation_factory(circulation=c2, service_parent=old_service, service=sub_service)

    for task_id in ["submit", "ebau-number", "init-circulation"]:
        workflow_api.complete_work_item(
            work_item=be_instance.case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
        )

    for circulation in [c1, c2]:
        work_item_factory(
            case=be_instance.case,
            child_case=None,  # this will be properly created in the sync method
            task=Task.objects.get(pk="circulation"),
            meta={"circulation-id": circulation.pk},
        )

        CalumaApi().sync_circulation(circulation, caluma_admin_user)

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

    assert response.status_code == status.HTTP_204_NO_CONTENT

    if should_sync:
        assert be_instance.circulations.filter(pk=c1.pk).exists()
        assert not be_instance.circulations.filter(pk=c2.pk).exists()

        c1.refresh_from_db()

        assert c1.activations.filter(pk=a1.pk).exists()
        assert c1.activations.filter(pk=a2.pk).exists()
        assert not c1.activations.filter(pk=a3.pk).exists()

        a1.refresh_from_db()
        a2.refresh_from_db()

        assert a1.service_parent == new_service
        assert a2.service_parent == some_service


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
):
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

    init_circulation = be_instance.case.work_items.get(task_id="init-circulation")
    init_circulation.assigned_users = [admin_user.username, other_user.username]
    init_circulation.save()

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

        # assigned users are filtered
        init_circulation.refresh_from_db()
        assert admin_user.username in init_circulation.assigned_users
        assert other_user.username not in init_circulation.assigned_users
    elif expected_status == status.HTTP_400_BAD_REQUEST:
        assert (
            response.data[0]["detail"]
            == f"{service_type} is not a valid service type - valid types are: municipality, construction_control"
        )


@pytest.mark.parametrize(
    "instance__user,service_group__name", [(LazyFixture("admin_user"), "municipality")]
)
@pytest.mark.parametrize("dry", [True, False])
@pytest.mark.parametrize(
    "role__name,instance_state__name,sync_circulation,expected_status,expected_work_items",
    [
        ("Support", "subm", False, status.HTTP_200_OK, ["ebau-number"]),
        (
            "Support",
            "circulation_init",
            False,
            status.HTTP_200_OK,
            ["skip-circulation", "init-circulation"],
        ),
        ("Support", "sb1", False, status.HTTP_200_OK, ["sb1"]),
        ("Municipality", "subm", False, status.HTTP_403_FORBIDDEN, None),
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
    sync_circulation,
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
                "attributes": {"dry": dry, "sync_circulation": sync_circulation},
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


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("service__name", ["Leitbehörde Burgdorf"])
def test_caluma_export_be(
    db,
    admin_client,
    be_instance,
    instance_service_factory,
    service,
    application_settings,
    settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["MUNICIPALITY_DATA_SHEET"] = settings.ROOT_DIR(
        "kt_bern",
        pathlib.Path(settings.APPLICATIONS["kt_bern"]["MUNICIPALITY_DATA_SHEET"]).name,
    )

    instance_service_factory(
        instance=be_instance, service=admin_client.user.groups.first().service
    )

    be_instance.case.document.answers.create(
        value=str(service.pk), question_id="gemeinde"
    )

    row_doc = form_api.save_document(
        caluma_form_models.Form.objects.get(pk="personalien-tabelle")
    )
    form_api.save_answer(
        caluma_form_models.Question.objects.get(pk="vorname-gesuchstellerin"),
        row_doc,
        value="Max",
    )
    form_api.save_answer(
        caluma_form_models.Question.objects.get(pk="name-gesuchstellerin"),
        row_doc,
        value="Muster",
    )

    form_api.save_answer(
        caluma_form_models.Question.objects.get(pk="personalien-gesuchstellerin"),
        be_instance.case.document,
        value=[str(row_doc.pk)],
    )

    url = reverse("instance-export")
    response = admin_client.get(url, {"instance_id": be_instance.pk})
    assert response.status_code == status.HTTP_200_OK
    book = pyexcel.get_book(file_content=response.content, file_type="xlsx")
    assert be_instance.pk in book.get_dict()["pyexcel sheet"][1]


@pytest.mark.parametrize(
    "query",
    [
        {},
        {"foo": "bar"},
        {"instance_id": ""},
        {"instance_id": ",".join(str(i) for i in range(10000, 11001))},
    ],
)
def test_caluma_export_bad_request(admin_client, query):
    url = reverse("instance-export")
    resp = admin_client.get(url, query)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
