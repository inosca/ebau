from datetime import datetime

import pytest
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.events import send_event_with_deprecations
from caluma.caluma_workflow.models import Task, WorkItem
from caluma.caluma_workflow.utils import create_work_items
from django.utils.timezone import make_aware

from camac.caluma.api import CalumaApi
from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_ALLE_BETEILIGTEN,
    ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN,
    DECISIONS_BEWILLIGT,
    INSTANCE_RESOURCE_ZIRKULATION,
    NOTICE_TYPE_NEBENBESTIMMUNG,
    NOTICE_TYPE_STELLUNGNAHME,
)
from camac.core.models import Activation, InstanceService, Notice
from camac.ech0211.tests.utils import xml_data
from camac.instance.models import Instance

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
    TaskSendHandler,
    resolve_send_handler,
)


@pytest.mark.parametrize(
    "xml_file,expected_send_handler",
    [
        ("accompanying_report", AccompanyingReportSendHandler),
        ("change_responsibility", ChangeResponsibilitySendHandler),
        ("close_dossier", CloseArchiveDossierSendHandler),
        ("notice_ruling", NoticeRulingSendHandler),
        ("task", TaskSendHandler),
        ("kind_of_proceedings", KindOfProceedingsSendHandler),
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
    "judgement,instance_state_name,has_permission,is_vorabklaerung,active,expected_state_name",
    [
        (
            ECH_JUDGEMENT_DECLINED,
            "circulation_init",
            True,
            False,
            "leitbehoerde",
            "rejected",
        ),
        (
            ECH_JUDGEMENT_WRITTEN_OFF,
            "circulation_init",
            False,
            False,
            "leitbehoerde",
            None,
        ),
        (
            ECH_JUDGEMENT_APPROVED,
            "coordination",
            True,
            False,
            "leitbehoerde",
            "sb1",
        ),
        (
            ECH_JUDGEMENT_APPROVED,
            "circulation",
            True,
            False,
            "leitbehoerde",
            "sb1",
        ),
        (
            ECH_JUDGEMENT_APPROVED,
            "circulation",
            True,
            False,
            "rsta",
            "sb1",
        ),
        (
            ECH_JUDGEMENT_APPROVED,
            "circulation",
            True,
            True,
            "leitbehoerde",
            "evaluated",
        ),
        (
            ECH_JUDGEMENT_DECLINED,
            "subm",
            False,
            "leitbehoerde",
            False,
            None,
        ),
    ],
)
def test_notice_ruling_send_handler(
    judgement,
    instance_state_name,
    has_permission,
    is_vorabklaerung,
    active,
    expected_state_name,
    admin_user,
    set_application_be,
    ech_instance_be,
    ech_instance_case,
    instance_state_factory,
    attachment_factory,
    attachment_section_factory,
    service_factory,
    service_group_factory,
    service_group,
    instance_service_factory,
    multilang,
    caluma_admin_user,
    notification_template,
    application_settings,
    ech_snapshot,
    decision_factory,
):

    application_settings["NOTIFICATIONS"] = {
        "ECH_TASK": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["unnotified_service"],
            }
        ]
    }
    service_group_gemeinde = ech_instance_be.responsible_service().service_group
    service_group_baukontrolle = service_group_factory(name="construction-control")
    service_group_rsta = service_group_factory(name="district")

    service_gemeinde = service_factory(
        service_group=service_group_gemeinde,
        name=None,
        trans__name="Leitbehörde Burgdorf",
        trans__city="Burgdorf",
        trans__language="de",
    )
    service_baukontrolle = service_factory(
        service_group=service_group_baukontrolle,
        name=None,
        trans__name="Baukontrolle Burgdorf",
        trans__city="Burgdorf",
        trans__language="de",
    )
    service_rsta = service_factory(
        service_group=service_group_rsta,
        name=None,
        trans__name="Regierungsstatthalteramt Emmenthal",
        trans__city="Emmenthal",
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
    )
    assert handler.has_permission()[0] == has_permission

    # put case in a realistic status
    skip_tasks = ["submit"]

    if instance_state_name == "circulation_init":
        skip_tasks.append("ebau-number")
    elif instance_state_name == "circulation":
        skip_tasks.extend(["ebau-number", "init-circulation"])
    elif instance_state_name == "coordination":
        skip_tasks.extend(["ebau-number", "skip-circulation"])

    for task_id in skip_tasks:
        workflow_api.skip_work_item(
            work_item=case.work_items.get(task_id=task_id), user=caluma_admin_user
        )

    if has_permission:
        expected_state = instance_state_factory(name=expected_state_name)
        handler.apply()
        ech_instance_be.refresh_from_db()
        assert ech_instance_be.previous_instance_state == state
        assert ech_instance_be.instance_state == expected_state
        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver == ech_instance_be.responsible_service()
        ech_snapshot(message.body)
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
            assert ech_instance_be.case.work_items.filter(task_id="decision").exists()

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
    instance_state_factory,
    service_factory,
    instance_service_factory,
    ech_instance_case,
    multilang,
    caluma_admin_user,
    notification_template,
    application_settings,
    ech_snapshot,
):

    application_settings["NOTIFICATIONS"] = {
        "ECH_TASK": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["unnotified_service"],
            }
        ]
    }
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
        ("leitbehoerde", "sb1", True),
        ("baukontrolle", "conclusion", True),
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
    ech_instance_case,
    admin_user,
    instance_service_factory,
    instance_state_factory,
    circulation_factory,
    decision_factory,
    caluma_admin_user,
    ech_snapshot,
):
    instance_state_factory(name="finished")

    inst_serv = instance_service_factory(
        instance=ech_instance_be, service__name="Baukontrolle Burgdorf", active=1
    )

    ech_instance_be.instance_state = instance_state_factory(name=instance_state_name)
    ech_instance_be.save()

    circulation_factory(instance=ech_instance_be)

    case = ech_instance_case()

    for task_id in [
        "submit",
        "ebau-number",
        "init-circulation",
        "circulation",
        "start-decision",
        "decision",
    ]:
        if task_id == "decision":
            decision_factory(instance=ech_instance_be, decision=DECISIONS_BEWILLIGT)

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


@pytest.mark.freeze_time(
    make_aware(datetime(2020, 2, 23, 23, 9, 1, microsecond=123456))
)
@pytest.mark.parametrize(
    "circulation_status,has_deadline,has_service,valid_service_id,success",
    [
        ("no_existing", True, True, True, True),
        ("latest_empty", True, True, True, True),
        ("latest_running", True, True, True, True),
        ("latest_not_running", True, True, True, True),
        ("none_running", True, True, True, True),
        ("no_existing", True, False, True, False),
        ("no_existing", True, True, False, False),
        # No passed deadline
        ("no_existing", False, True, True, True),
    ],
)
def test_task_send_handler(  # noqa: C901
    circulation_status,
    has_deadline,
    has_service,
    valid_service_id,
    success,
    admin_user,
    circulation_factory,
    set_application_be,
    ech_instance_be,
    ech_instance_case,
    instance_state_factory,
    service_factory,
    circulation_state_factory,
    activation_factory,
    instance_resource_factory,
    mailoutbox,
    caluma_admin_user,
    application_settings,
    notification_template,
    ech_snapshot,
):
    application_settings["NOTIFICATIONS"] = {
        "ECH_TASK": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["unnotified_service"],
            }
        ]
    }

    instance_resource_factory(pk=INSTANCE_RESOURCE_ZIRKULATION)
    state_run = circulation_state_factory(name="RUN")
    state_done = circulation_state_factory(name="DONE")
    state = instance_state_factory(name="circulation")
    ech_instance_be.instance_state = state
    ech_instance_be.save()

    case = ech_instance_case()
    for task_id in ["submit", "ebau-number"]:
        workflow_api.skip_work_item(
            work_item=case.work_items.get(task_id=task_id), user=caluma_admin_user
        )

    group = admin_user.groups.first()
    group.service = ech_instance_be.services.first()
    group.save()

    if has_service:
        service = service_factory(pk=23, email="s1@example.com")

    if circulation_status in [
        "latest_empty",
        "latest_running",
        "latest_not_running",
        "none_running",
    ]:
        dummy_circulation = circulation_factory(instance=ech_instance_be)
        latest_circulation = circulation_factory(instance=ech_instance_be)

        # create work item for dummy circulation
        workflow_api.skip_work_item(
            work_item=case.work_items.get(task_id="init-circulation"),
            user=caluma_admin_user,
            context={"circulation-id": dummy_circulation.pk},
        )

        # create work item for latest circulation
        context = {"circulation-id": latest_circulation.pk}
        for work_item in create_work_items(
            Task.objects.filter(pk="circulation"),
            ech_instance_be.case,
            caluma_admin_user,
            None,
            context,
        ):
            send_event_with_deprecations(
                "post_create_work_item",
                sender="case_post_create",
                work_item=work_item,
                user=caluma_admin_user,
                context=context,
            )

        if circulation_status == "latest_running":
            activation_factory(
                circulation=latest_circulation,
                circulation_state=state_run,
                ech_msg_created=True,
            )

        if circulation_status in ["latest_not_running", "none_running"]:
            activation_factory(
                circulation=latest_circulation,
                circulation_state=state_done,
                ech_msg_created=True,
            )

        if circulation_status == "none_running":
            activation_factory(
                circulation=dummy_circulation,
                circulation_state=state_done,
                ech_msg_created=True,
            )

        CalumaApi().sync_circulation(dummy_circulation, caluma_admin_user)
        CalumaApi().sync_circulation(latest_circulation, caluma_admin_user)

    xml = xml_data("task")
    if not valid_service_id:
        xml = xml.replace("<serviceId>23</serviceId>", "<serviceId>string</serviceId>")

    if not has_deadline:
        xml = xml.replace("<deadline>2020-03-15</deadline>", "")

    data = CreateFromDocument(xml)

    handler = TaskSendHandler(
        data=data,
        queryset=Instance.objects,
        user=admin_user,
        group=group,
        auth_header="Bearer: some token",
        caluma_user=caluma_admin_user,
    )
    assert handler.has_permission()[0] is True

    if success:
        handler.apply()
        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver == service
        ech_snapshot(message.body)

        activations = Activation.objects.exclude(
            circulation_state__name="DONE"
        ).order_by("-pk")

        if circulation_status == "latest_running":
            assert activations.count() == 2
        else:
            assert activations.count() == 1

        activation = activations.first()
        assert activation.service == service

        # This should be the current datetime in UTC - since the freezed time is
        # in the winter it should be 23:09:01 minus one hour (Europe/Zurich with
        # daylight saving)
        assert activation.start_date.isoformat() == "2020-02-23T22:09:01+00:00"

        if has_deadline:
            # This should be the end of the day (23:59:00 to be consistent with
            # PHP) that was given as input (2020-03-15) minus one hour
            # (Europe/Zurich with daylight saving)
            assert activation.deadline_date.isoformat() == "2020-03-15T22:59:00+00:00"
        else:
            # This should be the end of the current day (2020-02-23 23:59:00 to
            # be consistent with PHP) minus one hour (Europe/Zurich with
            # daylight saving) plus 30 days
            assert activation.deadline_date.isoformat() == "2020-03-24T22:59:00+00:00"

        assert (
            WorkItem.objects.filter(
                **{
                    "case__family": ech_instance_be.case,
                    "status": WorkItem.STATUS_READY,
                    "task_id": "activation",
                    "meta__activation-id": activation.pk,
                }
            ).count()
            == 1
        )

        if circulation_status in ["latest_empty", "latest_running"]:
            assert activation.circulation == latest_circulation

        assert len(mailoutbox) == 1

        assert activation.ech_msg_created is True
        assert service.email in mailoutbox[0].to

    else:
        with pytest.raises(SendHandlerException):
            handler.apply()


def test_task_send_handler_no_permission(
    admin_user,
    ech_instance_be,
    caluma_admin_user,
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
    )
    assert handler.has_permission()[0] is False


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize("has_permission", [True, False])
def test_kind_of_proceedings_send_handler(
    has_permission,
    attachment_section_factory,
    attachment_factory,
    admin_user,
    set_application_be,
    ech_instance_be,
    ech_instance_case,
    instance_state_factory,
    instance_resource_factory,
    caluma_admin_user,
    notification_template,
    application_settings,
    mailoutbox,
    ech_snapshot,
):
    application_settings["NOTIFICATIONS"] = {
        "ECH_KIND_OF_PROCEEDINGS": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["applicant"],
            }
        ]
    }

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

    state = instance_state_factory(name="subm")
    if has_permission:
        state = instance_state_factory(name="circulation_init")
    ech_instance_be.instance_state = state
    ech_instance_be.save()

    case = ech_instance_case()

    for task_id in ["submit", "ebau-number"]:
        workflow_api.skip_work_item(
            work_item=case.work_items.get(task_id=task_id), user=caluma_admin_user
        )

    instance_state_factory(name="circulation")
    instance_resource_factory(pk=INSTANCE_RESOURCE_ZIRKULATION)

    data = CreateFromDocument(xml_data("kind_of_proceedings"))

    handler = KindOfProceedingsSendHandler(
        data=data,
        queryset=Instance.objects,
        user=admin_user,
        group=group,
        auth_header=None,
        caluma_user=caluma_admin_user,
    )
    assert handler.has_permission()[0] is has_permission

    if has_permission:
        handler.apply()
        assert ech_instance_be.circulations.exists()
        assert (
            ech_instance_be.circulations.first().service
            == ech_instance_be.responsible_service(filter_type="municipality")
        )
        ech_instance_be.refresh_from_db()
        assert ech_instance_be.previous_instance_state.name == "circulation_init"
        assert ech_instance_be.instance_state.name == "circulation"

        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver == ech_instance_be.responsible_service()
        ech_snapshot(message.body)

        attachment.refresh_from_db()
        assert attachment.attachment_sections.get(
            pk=ATTACHMENT_SECTION_ALLE_BETEILIGTEN
        )

        assert (
            ech_instance_be.involved_applicants.first().invitee.email
            in mailoutbox[0].to
        )


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize("has_attachment", [True, False])
@pytest.mark.parametrize("has_activation", [True, False])
def test_accompanying_report_send_handler(
    has_attachment,
    has_activation,
    admin_user,
    set_application_be,
    ech_instance_be,
    ech_instance_case,
    attachment_factory,
    attachment_section_factory,
    circulation_state_factory,
    circulation_answer_factory,
    instance_state_factory,
    activation_factory,
    user_group_factory,
    notice_type_factory,
    caluma_admin_user,
    notification_template,
    application_settings,
    service,
    mailoutbox,
    ech_snapshot,
):
    application_settings["NOTIFICATIONS"] = {
        "ECH_ACCOMPANYING_REPORT": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["activation_service_parent"],
            }
        ]
    }

    user_group = user_group_factory(default_group=1)

    notice_type_factory(pk=NOTICE_TYPE_STELLUNGNAHME)
    notice_type_factory(pk=NOTICE_TYPE_NEBENBESTIMMUNG)

    if has_activation:
        activation_factory(
            circulation__instance=ech_instance_be,
            circulation_state=circulation_state_factory(pk=1, name="RUN"),
            service=user_group.group.service,
            user=user_group.user,
            circulation_answer=None,
            service_parent=service,
        )

    done_state = circulation_state_factory(pk=2, name="DONE")
    unknown_answer = circulation_answer_factory(name="unknown")

    support_group = admin_user.groups.first()
    support_group.service = ech_instance_be.services.first()
    support_group.save()

    state = instance_state_factory(name="circulation")
    ech_instance_be.instance_state = state
    ech_instance_be.save()
    ech_instance_case()

    if has_attachment:
        attachment = attachment_factory(
            name="MyFile.pdf", uuid="00000000-0000-0000-0000-000000000000"
        )
        attachment.attachment_sections.add(attachment_section_factory(pk=7))

    data = CreateFromDocument(xml_data("accompanying_report"))

    handler = AccompanyingReportSendHandler(
        data=data,
        queryset=Instance.objects,
        user=user_group.user,
        group=user_group.group,
        auth_header=None,
        caluma_user=caluma_admin_user,
    )
    if not has_activation:
        assert handler.has_permission()[0] is False
        return

    assert handler.has_permission()[0] is True

    if has_attachment:
        handler.apply()

        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver == support_group.service
        ech_snapshot(message.body)
        assert Activation.objects.count() == 1
        activation = Activation.objects.first()
        assert activation.circulation_state == done_state
        assert activation.circulation_answer == unknown_answer
        assert Notice.objects.count() == 2

        assert service.email in mailoutbox[0].to

    else:
        with pytest.raises(SendHandlerException):
            handler.apply()
