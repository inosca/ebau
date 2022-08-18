import pytest
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.models import WorkItem

from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_ALLE_BETEILIGTEN,
    ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN,
    DECISIONS_BEWILLIGT,
)
from camac.core.models import InstanceService
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
    notification_template_factory,
    be_distribution_settings,
    ech_snapshot,
    decision_factory,
):
    if is_vorabklaerung:
        notification_template_factory(
            slug="08-stellungnahme-zu-voranfrage-gesuchsteller"
        )
        notification_template_factory(slug="08-stellungnahme-zu-voranfrage-behoerden")
    else:
        notification_template_factory(slug="08-entscheid-gesuchsteller")
        notification_template_factory(slug="08-entscheid-behoerden")

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
        "distribution",
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
    ech_snapshot,
    test_case,
    success,
    instance_state_factory,
    mailoutbox,
    notification_template_factory,
    service_factory,
    set_application_be,
    work_item_factory,
):
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

    if test_case != "no_service":
        service = service_factory(pk=23, email="s1@example.com")
    if test_case == "no_deadline":
        xml = xml.replace("<deadline>2020-03-15</deadline>", "")
    elif test_case == "invalid_service_id":
        xml = xml.replace("<serviceId>23</serviceId>", "<serviceId>string</serviceId>")
    elif test_case == "no_create_inquiry":
        distribution_case.work_items.filter(
            task_id=be_distribution_settings["INQUIRY_CREATE_TASK"]
        ).delete()
    elif test_case == "multiple_create_inquiry":
        work_item_factory(
            task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
            status=WorkItem.STATUS_READY,
            case=distribution_case,
            addressed_groups=[str(group.service.pk)],
        )
    elif test_case == "same_service":
        xml = xml.replace(
            "<serviceId>23</serviceId>", f"<serviceId>{group.service.pk}</serviceId>"
        )

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

        assert len(mailoutbox) == 1
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
    db,
    admin_user,
    attachment_factory,
    attachment_section_factory,
    be_distribution_settings,
    caluma_admin_user,
    ech_instance_be,
    ech_snapshot,
    has_permission,
    instance_state_factory,
    mailoutbox,
    notification_template_factory,
    set_application_be,
):
    notification_template_factory(slug="03-verfahrensablauf-gesuchsteller")

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

        assert attachment.attachment_sections.get(
            pk=ATTACHMENT_SECTION_ALLE_BETEILIGTEN
        )

        assert (
            ech_instance_be.involved_applicants.first().invitee.email
            in mailoutbox[0].to
        )


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize("has_attachment", [True, False])
@pytest.mark.parametrize("has_inquiry", [True, False])
def test_accompanying_report_send_handler(
    db,
    active_inquiry_factory,
    admin_user,
    attachment_factory,
    attachment_section_factory,
    be_distribution_settings,
    caluma_admin_user,
    ech_instance_be,
    ech_snapshot,
    has_attachment,
    has_inquiry,
    mailoutbox,
    notification_template_factory,
    service,
    set_application_be,
    user_group_factory,
    work_item_factory,
):
    notification_template_factory(slug="05-bericht-erstellt")

    user_group = user_group_factory(default_group=1)

    if has_inquiry:
        existing_inquiry = active_inquiry_factory(
            for_instance=ech_instance_be,
            addressed_service=user_group.group.service,
        )

        work_item_factory(
            task_id=be_distribution_settings["INQUIRY_ANSWER_FILL_TASK"],
            case=existing_inquiry.child_case,
            child_case=None,
            status=WorkItem.STATUS_READY,
        )

    support_group = admin_user.groups.first()
    support_group.service = ech_instance_be.services.first()
    support_group.save()

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

    if not has_inquiry:
        assert handler.has_permission()[0] is False
        return

    assert handler.has_permission()[0] is True

    if has_attachment:
        handler.apply()

        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver == support_group.service
        ech_snapshot(message.body)

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

        assert service.email in mailoutbox[0].to

    else:
        with pytest.raises(SendHandlerException):
            handler.apply()
