import copy
import re
from datetime import datetime
from unittest.mock import Mock

import pytest
import requests
from alexandria.core import factories as alexandria_factories
from alexandria.core.factories import CategoryFactory, MarkFactory
from caluma.caluma_form.models import Question
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.models import WorkItem
from django.core.management import call_command
from django.utils.timezone import make_aware

from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_ALLE_BETEILIGTEN,
    ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN,
)
from camac.core.models import InstanceService
from camac.document.tests.data import django_file
from camac.ech0211.tests.utils import xml_data
from camac.instance.document_merge_service import DMSHandler
from camac.instance.models import Instance, InstanceState
from camac.permissions import api as permissions_api

from ..constants import (
    ECH_JUDGEMENT_APPROVED,
    ECH_JUDGEMENT_DECLINED,
    ECH_JUDGEMENT_WRITTEN_OFF,
)
from ..models import Message
from ..schema.ech_0211_2_0 import CreateFromDocument
from ..send_handlers import (
    AccompanyingReportSendHandler,
    ChangeResponsibilitySendHandler,
    CloseArchiveDossierSendHandler,
    KindOfProceedingsSendHandler,
    NoticeRulingSendHandler,
    SendHandlerException,
    SubmitPlanningPermissionApplicationSendHandler,
    TaskSendHandler,
    resolve_send_handler,
)


@pytest.fixture
def mock_request_get(mocker):
    response = Mock(spec=requests.models.Response)
    response.status_code = 200
    response.content = (
        b"%PDF-1.\ntrailer<</Root<</Pages<</Kids[<</MediaBox[0 0 3 3]>>]>>>>>>"
    )
    mocker.patch.object(requests, "get", return_value=response)


@pytest.mark.parametrize(
    "xml_file,expected_send_handler",
    [
        ("accompanying_report", AccompanyingReportSendHandler),
        ("change_responsibility", ChangeResponsibilitySendHandler),
        ("close_dossier", CloseArchiveDossierSendHandler),
        ("notice_ruling", NoticeRulingSendHandler),
        ("task", TaskSendHandler),
        ("kind_of_proceedings", KindOfProceedingsSendHandler),
        (
            "submit_planning_permission_application",
            SubmitPlanningPermissionApplicationSendHandler,
        ),
        ("accompanying_report", None),
    ],
)
def test_resolve_send_handler(xml_file, expected_send_handler):
    data = CreateFromDocument(xml_data(xml_file))
    if not expected_send_handler:
        data.eventAccompanyingReport = None
        with pytest.raises(SendHandlerException):
            resolve_send_handler(data)
    else:
        assert resolve_send_handler(data) == expected_send_handler


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize("service_group__name", ["municipality"])
@pytest.mark.parametrize(
    "judgement,instance_state_name,has_permission,is_vorabklaerung,active,expected_state_name,document_backend,has_alexandria_move_permission",
    [
        (
            ECH_JUDGEMENT_DECLINED,
            "circulation_init",
            True,
            False,
            "leitbehoerde",
            "rejected",
            "camac-ng",
            False,
        ),
        (
            ECH_JUDGEMENT_WRITTEN_OFF,
            "circulation_init",
            False,
            False,
            "leitbehoerde",
            None,
            "camac-ng",
            False,
        ),
        (
            ECH_JUDGEMENT_APPROVED,
            "coordination",
            True,
            False,
            "leitbehoerde",
            "sb1",
            "camac-ng",
            False,
        ),
        (
            ECH_JUDGEMENT_APPROVED,
            "circulation",
            True,
            False,
            "leitbehoerde",
            "sb1",
            "camac-ng",
            False,
        ),
        (
            ECH_JUDGEMENT_APPROVED,
            "circulation",
            True,
            False,
            "rsta",
            "sb1",
            "camac-ng",
            False,
        ),
        (
            ECH_JUDGEMENT_APPROVED,
            "circulation",
            True,
            True,
            "leitbehoerde",
            "evaluated",
            "camac-ng",
            False,
        ),
        (
            ECH_JUDGEMENT_APPROVED,
            "circulation",
            True,
            True,
            "leitbehoerde",
            "evaluated",
            "alexandria",
            False,
        ),
        (
            ECH_JUDGEMENT_APPROVED,
            "circulation",
            True,
            True,
            "leitbehoerde",
            "evaluated",
            "alexandria",
            True,
        ),
        (
            ECH_JUDGEMENT_DECLINED,
            "subm",
            False,
            False,
            "leitbehoerde",
            None,
            "camac-ng",
            False,
        ),
    ],
)
def test_notice_ruling_send_handler(
    judgement,
    instance_state_name,
    has_permission,
    has_alexandria_move_permission,
    is_vorabklaerung,
    active,
    expected_state_name,
    admin_user,
    set_application_be,
    ech_instance_be,
    be_ech0211_settings,
    ech_instance_case,
    instance_state_factory,
    attachment_factory,
    attachment_section_factory,
    service_factory,
    instance_service_factory,
    multilang,
    caluma_admin_user,
    notification_template_factory,
    be_distribution_settings,
    ech_snapshot,
    decision_factory,
    settings,
    be_decision_settings,
    application_settings,
    document_backend,
    mock_request_get,
    mocked_request_object,
    mocker,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["DOCUMENT_BACKEND"] = document_backend
    if is_vorabklaerung:
        notification_template_factory(slug="08-beurteilung-zu-voranfrage-gesuchsteller")
        notification_template_factory(
            slug="08-beurteilung-zu-voranfrage-gesuchsteller-nicht-registriert"
        )
        notification_template_factory(slug="08-beurteilung-zu-voranfrage-behoerden")
    else:
        notification_template_factory(slug="08-entscheid-gesuchsteller")
        notification_template_factory(
            slug="08-entscheid-gesuchsteller-nicht-registriert"
        )
        notification_template_factory(slug="08-entscheid-behoerden")

    service_gemeinde = service_factory(
        service_group__name="municipality",
        name=None,
        trans__name="Leitbehörde Test",
        trans__city="Test",
        trans__language="de",
    )
    service_baukontrolle = service_factory(
        service_group__name="construction-control",
        name=None,
        trans__name="Baukontrolle Test",
        trans__city="Test",
        trans__language="de",
    )
    service_rsta = service_factory(
        service_group__name="district",
        name=None,
        trans__name="Regierungsstatthalteramt Test",
        trans__city="Test",
        trans__language="de",
    )
    active_service = service_gemeinde
    if active == "rsta":
        active_service = service_rsta
        instance_service_factory(
            active=0, service=service_gemeinde, instance=ech_instance_be
        )

    ech_instance_service = InstanceService.objects.get(
        instance=ech_instance_be, active=1
    )
    ech_instance_service.service = active_service
    ech_instance_service.save()

    category = CategoryFactory()
    mark = MarkFactory()
    be_ech0211_settings["NOTICE_RULING"]["ALEXANDRIA_CATEGORY"] = category.pk
    be_ech0211_settings["NOTICE_RULING"]["ALEXANDRIA_MARK"] = mark.pk
    mocker.patch(
        "camac.ech0211.send_handlers.has_alexandria_create_permission",
        return_value=True,
    )
    mocker.patch(
        "camac.ech0211.send_handlers.has_alexandria_move_permission",
        return_value=has_alexandria_move_permission,
    )
    existing_alexandria_file = alexandria_factories.FileFactory(
        document=alexandria_factories.DocumentFactory(
            id="e39500fd-3eb1-48a5-afe4-0e3b03c4f13a",
            metainfo={"camac-instance-id": ech_instance_be.pk},
            title="test.pdf",
            # assign to a random category at first.
            category=alexandria_factories.CategoryFactory(),
        ),
        name="existing.pdf",
    )
    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility.filter_queryset_for_document",
        side_effect=lambda queryset, request: queryset,
    )
    assert category.documents.count() == 0

    attachment_section_beteiligte_behoerden = attachment_section_factory(
        pk=ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN
    )
    attachment_section_factory(pk=ATTACHMENT_SECTION_ALLE_BETEILIGTEN)
    attachment = attachment_factory(
        uuid="00000000-0000-0000-0000-000000000000",
        name="myFile.pdf",
        instance=ech_instance_be,
    )
    attachment.attachment_sections.add(attachment_section_beteiligte_behoerden)

    case = ech_instance_case(is_vorabklaerung)

    data = CreateFromDocument(xml_data("notice_ruling"))

    data.eventNotice.decisionRuling.judgement = judgement

    # append an existing alexandria document, to check that it is moved
    # to the configured category via the notice ruling event.
    if document_backend == "alexandria":
        new_doc = data.eventNotice.document[0]
        existing_doc = copy.deepcopy(new_doc)
        existing_doc.uuid = str(existing_alexandria_file.document.pk)
        data.eventNotice.document.append(existing_doc)

    state = instance_state_factory(name=instance_state_name)
    ech_instance_be.instance_state = state
    ech_instance_be.save()

    group = admin_user.groups.first()
    group.service = ech_instance_be.responsible_service()
    group.save()

    handler = NoticeRulingSendHandler(
        data=data,
        queryset=Instance.objects,
        user=admin_user,
        group=admin_user.groups.first(),
        auth_header=None,
        caluma_user=caluma_admin_user,
        request=mocked_request_object,
    )
    assert handler.has_permission()[0] == has_permission

    # put case in a realistic status
    skip_tasks = ["submit"]

    if instance_state_name in ["circulation_init", "circulation"]:
        skip_tasks.append("ebau-number")
    elif instance_state_name == "coordination":
        skip_tasks.extend(["ebau-number", "distribution"])

    for task_id in skip_tasks:
        workflow_api.skip_work_item(
            work_item=WorkItem.objects.filter(
                task_id=task_id,
                case__family=case,
                status=WorkItem.STATUS_READY,
            ).first(),
            user=caluma_admin_user,
        )

    if has_permission:
        expected_state = instance_state_factory(name=expected_state_name)

        if document_backend == "alexandria" and not has_alexandria_move_permission:
            with pytest.raises(SendHandlerException):
                handler.apply()

            return

        handler.apply()
        ech_instance_be.refresh_from_db()
        assert ech_instance_be.previous_instance_state == state
        assert ech_instance_be.instance_state == expected_state
        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver == ech_instance_be.responsible_service()
        ech_snapshot(message.body)
        if document_backend == "alexandria":
            # both the new and the existing file must be assigned to
            # the configured category and have the mark.
            assert category.documents.filter(marks=mark).count() == 2
        else:
            attachment.refresh_from_db()
            assert attachment.attachment_sections.get(
                pk=ATTACHMENT_SECTION_ALLE_BETEILIGTEN
            )

        if expected_state_name == "rejected":
            # if the instance is rejected, there should not be a decision work item
            assert not ech_instance_be.case.work_items.filter(
                task_id="decision"
            ).exists()
        else:
            assert (
                decision_workitem := ech_instance_be.case.work_items.filter(
                    task_id="decision"
                ).first()
            )
            # Decision-Geometer question must be answered
            assert decision_workitem.document.answers.filter(
                question_id="decision-geometer"
            ).first()

        expected_service = (
            active_service
            if is_vorabklaerung or expected_state_name == "rejected"
            else service_baukontrolle
        )
        assert ech_instance_be.responsible_service() == expected_service


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize(
    "service_exists,instance_state_name,has_permission,success",
    [
        (True, "circulation_init", True, True),
        (True, "sb1", False, False),
        (False, "circulation_init", True, False),
    ],
)
def test_change_responsibility_send_handler(
    service_exists,
    instance_state_name,
    has_permission,
    success,
    admin_user,
    set_application_be,
    be_ech0211_settings,
    mocked_request_object,
    instance_state_factory,
    service_factory,
    instance_service_factory,
    ech_instance_case,
    multilang,
    caluma_admin_user,
    notification_template_factory,
    ech_snapshot,
    be_distribution_settings,
):
    notification_template_factory(slug="02-benachrichtigung-baubewilligungsbehorde")

    ech_instance = ech_instance_case().instance
    instance_state = instance_state_factory(name=instance_state_name)
    ech_instance.instance_state = instance_state
    ech_instance.save()
    burgdorf = ech_instance.responsible_service()

    group = admin_user.groups.first()
    group.service = ech_instance.services.first()
    group.save()

    if instance_state_name == "sb1":
        service_baukontrolle = service_factory(
            service_group__name="construction-control",
            name=None,
            trans__name="Baukontrolle Burgdorf",
            trans__city="Burgdorf",
            trans__language="de",
        )
        instance_service_factory(
            instance=ech_instance, service=service_baukontrolle, active=1
        )
        group.service = service_baukontrolle
        group.save()

    if service_exists:
        madiswil = service_factory(
            pk=20351,
            name="Madiswil",
            service_group=ech_instance.responsible_service().service_group,
        )

    data = CreateFromDocument(xml_data("change_responsibility"))

    handler = ChangeResponsibilitySendHandler(
        data=data,
        queryset=Instance.objects,
        user=admin_user,
        group=group,
        auth_header=None,
        caluma_user=caluma_admin_user,
        request=mocked_request_object,
    )
    assert handler.has_permission()[0] is has_permission

    if not has_permission:
        return

    if success:
        handler.apply()
        assert ech_instance.responsible_service() == madiswil
        assert InstanceService.objects.get(
            instance=ech_instance, service=burgdorf, active=0
        )
        assert InstanceService.objects.get(
            instance=ech_instance, service=madiswil, active=1
        )
        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver == madiswil
        ech_snapshot(message.body)
    else:
        with pytest.raises(SendHandlerException):
            handler.apply()


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize(
    "requesting_service,instance_state_name,success",
    [
        ("leitbehoerde", "sb1", False),
        ("baukontrolle", "conclusion", True),
        ("baukontrolle", "coordination", False),
        ("baukontrolle", "sb1", True),
        ("leitbehoerde", "coordination", False),
        ("nobody", "conclusion", False),
    ],
)
def test_close_dossier_send_handler(
    requesting_service,
    instance_state_name,
    success,
    set_application_be,
    ech_instance_be,
    be_ech0211_settings,
    ech_instance_case,
    admin_user,
    instance_service_factory,
    instance_state_factory,
    circulation_factory,
    decision_factory,
    caluma_admin_user,
    snapshot,
    ech_snapshot,
    be_decision_settings,
    application_settings,
):
    for inst_state in [
        "coordination",
        "sb1",
        "sb2",
        "conclusion",
        "construction-acceptance",
        "finished",
    ]:
        instance_state_factory(name=inst_state)

    inst_serv = instance_service_factory(
        instance=ech_instance_be, service__name="Baukontrolle Burgdorf", active=1
    )

    ech_instance_be.instance_state = InstanceState.objects.get(name=instance_state_name)
    ech_instance_be.save()

    circulation_factory(instance=ech_instance_be)

    case = ech_instance_case()

    for task_id in [
        "submit",
        "ebau-number",
        "distribution",
        "decision",
    ]:
        if task_id == "decision":
            decision_factory(
                instance=ech_instance_be,
                decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"],
            )

        workflow_api.skip_work_item(
            work_item=case.work_items.get(task_id=task_id), user=caluma_admin_user
        )

    group = admin_user.groups.first()

    if requesting_service == "leitbehoerde":
        group.service = ech_instance_be.services.first()
    elif requesting_service == "baukontrolle":
        group.service = inst_serv.service

    group.save()

    data = CreateFromDocument(xml_data("close_dossier"))

    handler = CloseArchiveDossierSendHandler(
        data=data,
        queryset=Instance.objects,
        user=admin_user,
        group=group,
        auth_header=None,
        caluma_user=caluma_admin_user,
        request=None,
    )

    assert handler.has_permission()[0] is success

    if success:
        handler.apply()
        ech_instance_be.refresh_from_db()

        assert ech_instance_be.instance_state.name == "finished"
        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver == ech_instance_be.responsible_service()
        ech_snapshot(message.body)
    else:
        snapshot.assert_match(handler.has_permission()[1])


@pytest.mark.freeze_time("2020-02-23")
@pytest.mark.parametrize(
    "test_case,success",
    [
        (None, True),
        ("no_deadline", True),
        ("no_service", False),
        ("invalid_service_id", False),
        ("no_create_inquiry", False),
        ("multiple_create_inquiry", False),
        ("same_service", False),
    ],
)
def test_task_send_handler(
    db,
    admin_user,
    be_distribution_settings,
    caluma_admin_user,
    ech_instance_be,
    be_ech0211_settings,
    ech_snapshot,
    test_case,
    success,
    instance_state_factory,
    mailoutbox,
    notification_template_factory,
    service_factory,
    set_application_be,
    caluma_work_item_factory,
    set_document_backend,
):
    set_document_backend("camac-ng")
    notification_template_factory(slug="03-verfahrensablauf-fachstelle")

    state = instance_state_factory(name="circulation")
    ech_instance_be.instance_state = state
    ech_instance_be.save()

    for task_id in ["submit", "ebau-number"]:
        workflow_api.skip_work_item(
            work_item=ech_instance_be.case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
        )

    distribution_case = ech_instance_be.case.work_items.get(
        task_id=be_distribution_settings["DISTRIBUTION_TASK"]
    ).child_case

    # This would be done by the notice kind of proceedings send handler
    workflow_api.skip_work_item(
        work_item=distribution_case.work_items.get(
            task_id=be_distribution_settings["DISTRIBUTION_INIT_TASK"]
        ),
        user=caluma_admin_user,
    )

    group = admin_user.groups.first()
    group.service = ech_instance_be.services.first()
    group.save()

    xml = xml_data("task")

    if test_case == "no_deadline":
        xml = xml.replace("<deadline>2020-03-15</deadline>", "")
    elif test_case == "no_create_inquiry":
        distribution_case.work_items.filter(
            task_id=be_distribution_settings["INQUIRY_CREATE_TASK"]
        ).delete()
    elif test_case == "multiple_create_inquiry":
        caluma_work_item_factory(
            task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
            status=WorkItem.STATUS_READY,
            case=distribution_case,
            addressed_groups=[str(group.service.pk)],
        )
    elif test_case == "invalid_service_id":
        xml = xml.replace(
            "<organisationId>23</organisationId>",
            "<organisationId>string</organisationId>",
        )
    elif test_case == "same_service":
        xml = xml.replace(
            "<organisationId>23</organisationId>",
            f"<organisationId>{group.service.pk}</organisationId>",
        )

    if test_case != "no_service":
        service = service_factory(email="s1@example.com")
        xml = xml.replace(
            "<organisationId>23</organisationId>",
            f"<organisationId>{service.pk}</organisationId>",
        )

    data = CreateFromDocument(xml)

    handler = TaskSendHandler(
        data=data,
        queryset=Instance.objects,
        user=admin_user,
        group=group,
        auth_header="Bearer: some token",
        caluma_user=caluma_admin_user,
        request=None,
    )
    assert handler.has_permission()[0] is True

    if success:
        inquiries = WorkItem.objects.filter(
            task_id=be_distribution_settings["INQUIRY_TASK"],
            case__family__instance=ech_instance_be,
        )

        assert inquiries.count() == 0

        handler.apply()

        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver == service
        ech_snapshot(message.body)

        assert inquiries.count() == 1

        inquiry = inquiries.first()

        assert inquiry.addressed_groups == [str(service.pk)]
        assert inquiry.created_at.isoformat() == "2020-02-23T00:00:00+00:00"

        if test_case == "no_deadline":
            assert inquiry.deadline.isoformat() == "2020-03-24T00:00:00+00:00"
        else:
            assert inquiry.deadline.isoformat() == "2020-03-15T00:00:00+00:00"

        inquiry.document.answers.filter(
            question_id=be_distribution_settings["QUESTIONS"]["REMARK"]
        ).values == "Anforderung einer Stellungnahme"

        assert len(mailoutbox) == 1
        assert service.email in mailoutbox[0].to
    else:
        with pytest.raises(SendHandlerException):
            handler.apply()


def test_task_send_handler_gr_skips_formal_exam(
    db,
    admin_user,
    caluma_admin_user,
    ech_instance_gr,
    instance_state_factory,
    notification_template_factory,
    service_factory,
    set_application_gr,
    gr_distribution_settings,
    gr_ech0211_settings,
    gr_additional_demand_settings,
):
    notification_template_factory(slug="verfahrensablauf-fachstelle")
    notification_template_factory(slug="verfahrensablauf-uso")
    notification_template_factory(slug="bericht-erstellt")
    notification_template_factory(slug="zirkulation-abgebrochen")

    state = instance_state_factory(name="subm")
    instance_state_factory(name="circulation")
    ech_instance_gr.instance_state = state
    ech_instance_gr.save()

    group = admin_user.groups.first()
    group.service = ech_instance_gr.services.first()
    target_service = service_factory()
    group.save()

    workflow_api.complete_work_item(
        work_item=ech_instance_gr.case.work_items.first(),  # submit work item
        user=caluma_admin_user,
    )

    xml = xml_data("task")
    xml = xml.replace(
        "<organisationId>23</organisationId>",
        f"<organisationId>{target_service.pk}</organisationId>",
    )
    data = CreateFromDocument(xml)

    handler = TaskSendHandler(
        data=data,
        queryset=Instance.objects,
        user=admin_user,
        group=group,
        auth_header="Bearer: some token",
        caluma_user=caluma_admin_user,
        request=None,
    )

    handler.apply()

    assert (
        ech_instance_gr.case.work_items.get(task_id="formal-exam").status
        == WorkItem.STATUS_SKIPPED
    )


def test_task_send_handler_no_permission(
    admin_user,
    ech_instance_be,
    be_ech0211_settings,
    caluma_admin_user,
    set_application_be,
):
    group = admin_user.groups.first()
    group.service = ech_instance_be.services.first()
    group.save()

    data = CreateFromDocument(xml_data("task"))

    handler = TaskSendHandler(
        data=data,
        queryset=Instance.objects,
        user=None,
        group=group,
        auth_header=None,
        caluma_user=caluma_admin_user,
        request=None,
    )
    assert handler.has_permission()[0] is False


@pytest.mark.parametrize(
    "test_case,success",
    [
        ("claim_not_enabled", False),
        ("wrong_state", False),
        ("no_access", False),
        ("ok", True),
    ],
)
@pytest.mark.parametrize(
    "access_level__slug", ["distribution-service", "lead-authority"]
)
def test_task_send_claim_handler(
    rf,
    db,
    set_application_gr,
    admin_user,
    caluma_admin_user,
    ech_instance_gr,
    instance_state_factory,
    notification_template_factory,
    gr_additional_demand_settings,
    gr_permissions_settings,
    gr_ech0211_settings,
    application_settings,
    mocker,
    mailoutbox,
    test_case,
    success,
    access_level,
    mock_request_get,
):
    mocker.patch(
        "camac.ech0211.send_handlers.has_alexandria_create_permission",
        return_value=True,
    )

    # workflow notification templates
    caluma_send_notification = notification_template_factory()
    caluma_fill_notification = notification_template_factory()
    application_settings["CALUMA"]["CALUMA_WORKFLOW_NOTIFICATIONS"][
        "send-additional-demand"
    ] = [
        {
            "event": "completed",
            "notification": {
                "template_slug": caluma_send_notification.slug,
                "recipient_types": ["applicant"],
            },
        },
        {
            "event": "completed",
            "notification": {
                "template_slug": caluma_send_notification.slug,
                "recipient_types": ["additional_demand_inviter"],
            },
        },
    ]
    application_settings["CALUMA"]["SIMPLE_WORKFLOW"]["fill-additional-demand"][
        "notification"
    ]["template_slug"] = caluma_fill_notification.slug

    # enable/disable claim settings based on the test case
    gr_ech0211_settings["CLAIM"]["ENABLED"] = test_case != "claim_not_enabled"

    # user/group permissions for ech claim call
    group = admin_user.groups.first()
    group.service = ech_instance_gr.responsible_service()
    group.save()

    if not test_case == "no_access":
        permissions_api.grant(
            ech_instance_gr,
            grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
            access_level=access_level,
            service=group.service,
        )

    # ech0211 claim alexandria category
    alexandria_category = CategoryFactory()
    gr_ech0211_settings["CLAIM"]["ALEXANDRIA_CATEGORY"] = alexandria_category.pk

    # prepare instance state
    workflow_api.complete_work_item(
        work_item=ech_instance_gr.case.work_items.get(task_id="submit"),
        user=caluma_admin_user,
    )
    state = instance_state_factory(name="circulation")
    ech_instance_gr.instance_state = state
    ech_instance_gr.save()

    # override instance state to invalid state to test wrong_state case
    if test_case == "wrong_state":
        state = instance_state_factory(name="other")
        ech_instance_gr.instance_state = state
        ech_instance_gr.save()

    # prepare claim handler with xml template
    request = rf.request()
    request.user = admin_user
    request.group = group
    request.role = group.role
    xml = xml_data("claim")
    data = CreateFromDocument(xml)
    handler = TaskSendHandler(
        data=data,
        queryset=Instance.objects,
        user=admin_user,
        group=group,
        auth_header="Bearer: some token",
        caluma_user=caluma_admin_user,
        request=request,
    )

    # check for permission boolean based on success
    assert handler.has_permission()[0] is success

    if test_case in ["wrong_state", "no_access"]:
        assert (
            handler.has_permission()[1] == "You don't have permission to send a claim."
        )
    elif test_case == "claim_not_enabled":
        assert (
            handler.has_permission()[1] == "Claim is not enabled for this application."
        )
    elif success:
        # on success the permission message should be None and apply should succeed
        assert handler.has_permission()[1] is None
        handler.apply()
        assert len(mailoutbox) == 2
        assert caluma_send_notification.subject in mailoutbox[0].subject
        assert ech_instance_gr.user.email in mailoutbox[0].to
        assert caluma_send_notification.subject in mailoutbox[1].subject
        assert admin_user.email in mailoutbox[1].to
        # no eCH message yet, only after filling by applicant
        assert Message.objects.count() == 0

        # created workitem contains the ech meta data
        fill_work_item = WorkItem.objects.get(
            meta__has_key="ech-init-workitem",
            case__family=ech_instance_gr.case,
            task_id=gr_additional_demand_settings["FILL_TASK"],
        )
        ech_answer = fill_work_item.document.answers.filter(
            question_id="additional-demand-ech0211"
        ).first()
        assert ech_answer and ech_answer.value == "true", (
            "additional demand work item ech answer should be created"
        )


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize(
    "has_permission,document_backend",
    [(True, "alexandria"), (True, "camac-ng"), (False, "camac-ng")],
)
def test_kind_of_proceedings_send_handler(
    db,
    admin_user,
    attachment_factory,
    attachment_section_factory,
    be_distribution_settings,
    caluma_admin_user,
    ech_instance_be,
    be_ech0211_settings,
    ech_snapshot,
    has_permission,
    instance_state_factory,
    mailoutbox,
    notification_template_factory,
    set_application_be,
    document_backend,
    mock_request_get,
    mocked_request_object,
    mocker,
):
    notification_template_factory(slug="03-verfahrensablauf-gesuchsteller")

    set_application_be["DOCUMENT_BACKEND"] = document_backend
    category = CategoryFactory()
    be_ech0211_settings["KIND_OF_PROCEEDINGS"] = {"ALEXANDRIA_CATEGORY": category.pk}
    mocker.patch(
        "camac.ech0211.send_handlers.has_alexandria_create_permission",
        return_value=True,
    )

    attachment_section_beteiligte_behoerden = attachment_section_factory(
        pk=ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN
    )
    attachment_section_factory(pk=ATTACHMENT_SECTION_ALLE_BETEILIGTEN)
    attachment = attachment_factory(
        uuid="00000000-0000-0000-0000-000000000000",
        name="myFile.pdf",
        instance=ech_instance_be,
    )
    attachment.attachment_sections.add(attachment_section_beteiligte_behoerden)

    group = admin_user.groups.first()
    group.service = ech_instance_be.services.first()
    group.save()

    instance_state_factory(name="circulation")
    state = instance_state_factory(name="subm")
    if has_permission:
        state = instance_state_factory(name="circulation_init")
    ech_instance_be.instance_state = state
    ech_instance_be.save()

    for task_id in ["submit", "ebau-number"]:
        workflow_api.skip_work_item(
            work_item=ech_instance_be.case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
        )

    data = CreateFromDocument(xml_data("kind_of_proceedings"))

    handler = KindOfProceedingsSendHandler(
        data=data,
        queryset=Instance.objects,
        user=admin_user,
        group=group,
        auth_header=None,
        caluma_user=caluma_admin_user,
        request=mocked_request_object,
    )
    assert handler.has_permission()[0] is has_permission

    if has_permission:
        distribution_init = WorkItem.objects.get(
            task_id=be_distribution_settings["DISTRIBUTION_INIT_TASK"],
            case__family__instance=ech_instance_be,
        )

        assert distribution_init.status == WorkItem.STATUS_READY

        handler.apply()

        distribution_init.refresh_from_db()
        ech_instance_be.refresh_from_db()
        attachment.refresh_from_db()

        assert distribution_init.status == WorkItem.STATUS_COMPLETED
        assert ech_instance_be.previous_instance_state.name == "circulation_init"
        assert ech_instance_be.instance_state.name == "circulation"

        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver == ech_instance_be.responsible_service()
        ech_snapshot(message.body)

        if document_backend == "alexandria":
            assert category.documents.count() == 1
        else:
            assert attachment.attachment_sections.get(
                pk=ATTACHMENT_SECTION_ALLE_BETEILIGTEN
            )

        assert (
            ech_instance_be.involved_applicants.first().invitee.email
            in mailoutbox[0].to
        )


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize(
    "has_inquiry,has_attachment,document_backend,documents_available",
    (
        (True, False, "camac-ng", True),
        (True, True, "camac-ng", True),
        (False, False, "camac-ng", True),
        (True, True, "alexandria", True),
        (True, True, "alexandria", False),
    ),
)
def test_accompanying_report_send_handler(
    db,
    active_inquiry_factory,
    admin_user,
    attachment_factory,
    attachment_section_factory,
    be_distribution_settings,
    caluma_admin_user,
    ech_instance_be,
    be_ech0211_settings,
    ech_snapshot,
    mailoutbox,
    notification_template_factory,
    service,
    set_application_be,
    user_group_factory,
    caluma_work_item_factory,
    caluma_form_question_factory,
    caluma_question_option_factory,
    settings,
    #
    has_attachment,
    has_inquiry,
    document_backend,
    documents_available,
    mocker,
    mock_remote_file,
    group_factory,
):
    notification_template_factory(slug="05-bericht-erstellt")
    settings.APPLICATION["DOCUMENT_BACKEND"] = document_backend
    be_ech0211_settings["ACCOMPANYING_REPORT"]["EXTENSION_MAPPING"] = {
        "inquiry-text-answer": {
            "tag": "situation",
        },
        "inquiry-checkbox": {
            "tag": "documentsAvailable",
            "true_value": "inquiry-checked",
        },
    }
    be_ech0211_settings["ACCOMPANYING_REPORT"]["ENABLE_ORGANISATION_EXTENSION"] = True
    CategoryFactory(slug="beteiligte-behoerden")
    be_ech0211_settings["ACCOMPANYING_REPORT"]["ALEXANDRIA_CATEGORY"] = (
        "beteiligte-behoerden"
    )
    mocker.patch(
        "camac.ech0211.send_handlers.AlexandriaDocumentMixin.check_alexandria_category_permission"
    )
    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility.filter_queryset_for_document",
        side_effect=lambda queryset, request: queryset,
    )
    caluma_form_question_factory(
        form=ech_instance_be.case.document.form,
        question__slug="inquiry-text-answer",
        question__type=Question.TYPE_TEXT,
    )
    q = caluma_form_question_factory(
        form=ech_instance_be.case.document.form,
        question__slug="inquiry-checkbox",
        question__type=Question.TYPE_CHOICE,
    ).question
    caluma_question_option_factory(
        question=q,
        option__slug="inquiry-checked",
    )

    user_group = user_group_factory(default_group=1)

    # the inviting service needs to have at least one group,
    # otherwise event_handlers.py::get_fake_request returns None
    inviting_group = group_factory()
    inviting_service = inviting_group.service
    if has_inquiry:
        existing_inquiry = active_inquiry_factory(
            for_instance=ech_instance_be,
            addressed_service=user_group.group.service,
            controlling_service=inviting_service,
        )

        caluma_work_item_factory(
            task_id=be_distribution_settings["INQUIRY_ANSWER_FILL_TASK"],
            case=existing_inquiry.child_case,
            child_case=None,
            status=WorkItem.STATUS_READY,
        )

    support_group = admin_user.groups.first()
    support_group.service = ech_instance_be.services.first()
    support_group.save()

    if has_attachment:
        if document_backend == "camac-ng":
            attachment = attachment_factory(
                name="MyFile.pdf", uuid="00000000-0000-0000-0000-000000000000"
            )
            attachment.attachment_sections.add(attachment_section_factory(pk=7))

        if document_backend == "alexandria":
            alexandria_factories.FileFactory(
                document=alexandria_factories.DocumentFactory(
                    id="e39500fd-3eb1-48a5-afe4-0e3b03c4f13a",
                    metainfo={"camac-instance-id": ech_instance_be.pk},
                    category__metainfo={},
                    title="hidden.pdf",
                ),
                name="hidden.pdf",
            )
            existing_doc = alexandria_factories.DocumentFactory(
                id="12345678-1234-1234-1234-000000000000",
                metainfo={"camac-instance-id": ech_instance_be.pk},
                category__metainfo={
                    "access": {support_group.role.name: {"visibility": "all"}}
                },
                title="existing.pdf",
            )
            existing_doc.created_at = make_aware(datetime(2022, 5, 2, 12, 0))
            existing_doc.save()
            alexandria_factories.FileFactory(document=existing_doc, name="existing.pdf")

    xml = xml_data("accompanying_report")
    if not documents_available:
        xml = xml.replace(
            "<documentsAvailable>true</documentsAvailable>",
            "<documentsAvailable>false</documentsAvailable>",
        )
    data = CreateFromDocument(xml)

    handler = AccompanyingReportSendHandler(
        data=data,
        queryset=Instance.objects,
        user=user_group.user,
        group=user_group.group,
        auth_header=None,
        caluma_user=caluma_admin_user,
        request=None,
    )

    if not has_inquiry:
        assert handler.has_permission()[0] is False
        return

    assert handler.has_permission()[0] is True

    if has_attachment:
        handler.apply()

        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver == inviting_service

        xml = message.body
        if document_backend == "alexandria":
            # replace UUIDs because some of them are generated on upload
            # and can't be snapshotted deterministically
            xml = re.sub(r"(<ns\d+:uuid>).+?(</ns\d+:uuid>)", r"\1<!-- UUID -->\2", xml)
        ech_snapshot(xml)

        inquiries = WorkItem.objects.filter(
            task_id=be_distribution_settings["INQUIRY_TASK"],
            case__family__instance=ech_instance_be,
        )

        assert inquiries.count() == 1
        inquiry = inquiries.first()
        assert inquiry.status == WorkItem.STATUS_COMPLETED
        assert inquiry.child_case.document.answers.filter(
            question_id=be_distribution_settings["QUESTIONS"]["STATUS"],
            value=be_distribution_settings["ANSWERS"]["STATUS"]["UNKNOWN"],
        ).exists()
        assert inquiry.child_case.document.answers.filter(
            question_id=be_distribution_settings["QUESTIONS"]["STATEMENT"]
        ).exists()
        assert inquiry.child_case.document.answers.filter(
            question_id=be_distribution_settings["QUESTIONS"]["ANCILLARY_CLAUSES"]
        ).exists()
        assert inquiry.child_case.document.answers.filter(
            question_id="inquiry-text-answer"
        ).exists()
        assert inquiry.child_case.document.answers.filter(
            question_id="inquiry-checkbox"
        ).exists()

        assert inviting_service.email in mailoutbox[0].to

    else:
        with pytest.raises(SendHandlerException):
            handler.apply()


def test_get_instance_id_error(admin_user, group, caluma_admin_user):
    xml = xml_data("task").replace(
        "<ns2:dossierIdentification>2323</ns2:dossierIdentification>",
        "<ns2:dossierIdentification>string</ns2:dossierIdentification>",
    )
    data = CreateFromDocument(xml)

    with pytest.raises(SendHandlerException):
        TaskSendHandler(
            data=data,
            queryset=Instance.objects,
            user=admin_user,
            group=group,
            auth_header="Bearer: some token",
            caluma_user=caluma_admin_user,
            request=None,
        )


@pytest.mark.freeze_time("2024-04-24")
@pytest.mark.parametrize(
    "role__name,has_create_permission,pass_permission,test_case,success",
    [
        ("municipality-lead", True, True, "submit", True),
        ("municipality-lead", True, True, "file subsequently", False),
        ("municipality-lead", False, True, "submit", False),
        ("service-lead", False, False, "submit", False),
    ],
)
def test_submit_send_handler(
    db,
    role,
    settings,
    gr_ech0211_settings,
    gr_dms_settings,
    set_application_gr,
    caluma_workflow_config_gr,
    ech_instance_gr,
    admin_user,
    caluma_admin_user,
    ech_snapshot,
    instance_state_factory,
    caluma_question_factory,
    mocked_request_object,
    mailoutbox,
    notification_template_factory,
    mocker,
    form,
    has_create_permission,
    pass_permission,
    test_case,
    success,
):
    notification_template_factory(slug="empfang-anfragebaugesuch-gesuchsteller")
    notification_template_factory(slug="empfang-anfragebaugesuch-behorden")
    CategoryFactory(slug="beilagen-zum-gesuch")
    CategoryFactory(slug="beilagen-zum-gesuch-weitere-gesuchsunterlagen")
    gr_ech0211_settings["SUBMIT_PLANNING_PERMISSION_APPLICATION"]["FORM_ID"] = form.pk
    instance_state_factory(name="new")
    instance_state_factory(name="subm")
    caluma_question_factory(slug="material-question-exam")
    caluma_question_factory(slug="complete-material-exam")
    caluma_question_factory(slug="oeffentliche-auflage")
    caluma_question_factory(slug="fuer-gvg-freigeben")
    call_command(
        "loaddata",
        settings.ROOT_DIR("kt_gr/config/caluma_form.json"),
        settings.ROOT_DIR("kt_gr/config/caluma_form_v2.json"),
        settings.ROOT_DIR("kt_gr/config/caluma_form_common.json"),
    )
    response = Mock(spec=requests.models.Response)
    response.status_code = 200
    response.content = (
        b"%PDF-1.\ntrailer<</Root<</Pages<</Kids[<</MediaBox[0 0 3 3]>>]>>>>>>"
    )
    generate_pdf_mock = mocker.patch(
        "camac.instance.serializers.CalumaInstanceSubmitSerializer._generate_and_store_pdf"
    )
    mocker.patch.object(requests, "get", return_value=response)
    mocker.patch(
        "camac.ech0211.send_handlers.has_alexandria_create_permission",
        return_value=has_create_permission,
    )
    file = django_file("multiple-pages.pdf")
    file.content_type = "application/pdf"
    mocker.patch.object(
        DMSHandler,
        "generate_pdf",
        return_value=file,
    )

    group = admin_user.groups.first()
    group.service = ech_instance_gr.services.first()
    group.save()

    xml = xml_data("submit_planning_permission_application")
    if test_case == "file subsequently":
        xml = xml.replace(
            "<ns1:eventType>submit</ns1:eventType>",
            "<ns1:eventType>file subsequently</ns1:eventType>",
        )
        xml = xml.replace(
            "<ns1:dossierIdentification>2323</ns1:dossierIdentification>",
            f"<ns1:dossierIdentification>{ech_instance_gr.pk}</ns1:dossierIdentification>",
        )

    data = CreateFromDocument(xml)
    handler = SubmitPlanningPermissionApplicationSendHandler(
        data=data,
        queryset=Instance.objects,
        user=admin_user,
        group=group,
        auth_header="Bearer: some token",
        caluma_user=caluma_admin_user,
        request=mocked_request_object,
    )
    assert handler.has_permission()[0] is pass_permission
    if not pass_permission:
        return

    if success:
        instance = handler.apply()

        requests.get.assert_called()
        assert (
            instance.case.document.answers.get(question_id="parzelle")
            .documents.first()
            .answers.get(question_id="parzellennummer")
            .value
            == "1586"
        )
        assert (
            instance.case.document.answers.get(
                question_id="beschreibung-bauvorhaben"
            ).value
            == "Testbeschreibung"
        )

        applicant_person = (
            instance.case.document.answers.get(
                question_id="personalien-gesuchstellerin"
            )
            .documents.filter(
                answers__question_id="juristische-person-gesuchstellerin",
                answers__value="juristische-person-gesuchstellerin-nein",
            )
            .first()
        )
        assert (
            applicant_person.answers.get(question_id="name-gesuchstellerin").value
            == "Muster"
        )
        applicant_org = (
            instance.case.document.answers.get(
                question_id="personalien-gesuchstellerin"
            )
            .documents.filter(
                answers__question_id="juristische-person-gesuchstellerin",
                answers__value="juristische-person-gesuchstellerin-ja",
            )
            .first()
        )
        assert (
            applicant_org.answers.get(
                question_id="name-juristische-person-gesuchstellerin"
            ).value
            == "BAUAG"
        )

        assert instance.alexandria_instance_documents.count() == 1
        alexandria_document = instance.alexandria_instance_documents.first().document
        assert alexandria_document.title == "dummy"
        assert alexandria_document.files.count() == 2

        # Prevent some race conditions on which file is returned first
        assert alexandria_document.files.order_by("-name").first().name == "photo.jpg"

        assert len(mailoutbox) == 0
        assert Message.objects.count() == 0

        generate_pdf_mock.assert_called_once_with(instance)
    else:
        with pytest.raises(SendHandlerException):
            handler.apply()
