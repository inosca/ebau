from datetime import date, datetime

import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow.models import Task, WorkItem
from django.utils.timezone import make_aware
from django.utils.translation import gettext as _

from camac.caluma.extensions.events import deadlines
from camac.caluma.extensions.events.deadlines import (
    post_complete_inquiry_fill_ag,
    post_create_inquiry,
    post_create_withdrawal_check_closes_suspensions,
    post_redo_inquiry_ag,
)
from camac.constants.kt_gr import ARE_SERVICE_GROUP
from camac.deadlines import models as deadlines_models


@pytest.mark.parametrize(
    "service_group__name,role__name,expected_count",
    [
        ("municipality", "municipality-lead", 1),
        (ARE_SERVICE_GROUP, "service-lead", 1),
        ("service", "service-lead", 0),
    ],
)
@pytest.mark.parametrize(
    "close_action",
    ["complete", "cancel"],
)
def test_events_deadlines_additional_demand_suspensions_gr(
    db,
    admin_user,
    gr_instance,
    service,
    caluma_work_item_factory,
    service_factory,
    gr_additional_demand_settings,
    gr_deadlines_settings,
    gr_permissions_settings,
    set_application_gr,
    close_action,
    expected_count,
    mocker,
):
    """Test suspension creation for additional demand work item.

    When a workitem for additional demand is created, a deadline suspension should
    be automatically created if the service is either the responsible service or
    the ARE.
    """
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service
        if service.service_group.name == "municipality"
        else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=service.service_group.name == ARE_SERVICE_GROUP,
    )

    case = gr_instance.case
    workitem = caluma_work_item_factory(
        case=case,
        task=Task.objects.get(slug=gr_additional_demand_settings["FILL_TASK"]),
    )
    main_workitem = caluma_work_item_factory(
        case=case,
        child_case=case,
        task=Task.objects.get(slug=gr_additional_demand_settings["TASK"]),
        created_by_group=str(service.pk),
    )
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.trigger_side_effect",
        return_value=False,
    )

    deadlines_models.InstanceDeadline.objects.create_deadline(
        instance=gr_instance, service=service
    )

    # trigger the event for a new additional demand work item
    deadlines.post_create_fill_additional_demand(
        sender=None, work_item=workitem, user=None, context=None
    )

    assert deadlines_models.Suspension.objects.count() == expected_count
    assert deadlines_models.InstanceDeadline.objects.count() == expected_count

    if expected_count > 0:
        suspension = deadlines_models.Suspension.objects.first()
        assert suspension.deadline.service == service
        assert suspension.deadline.instance == case.family.instance
        assert suspension.work_item == main_workitem
        assert suspension.end_date is None
        assert (
            suspension.reason
            == deadlines_models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_ADDITIONAL_DEMAND
        )
        assert suspension.deadline.service == service
        assert suspension.group is None
        assert suspension.user is None
        assert suspension.author_formatted == _("Automatic")

        # trigger the event for completing the additional demand work item
        if close_action == "complete":
            deadlines.post_complete_fill_additional_demand(
                sender=None, work_item=workitem, user=None, context=None
            )
        else:
            deadlines.post_cancel_additional_demand(
                sender=None, work_item=main_workitem, user=None, context=None
            )

        assert deadlines_models.Suspension.objects.count() == 1, (
            "still only one suspension should exist"
        )
        suspension.refresh_from_db()
        assert suspension.end_date is not None


@pytest.mark.parametrize(
    "service_group__name,role__name,test_case,expected_date",
    [
        # No formal exam, set to submit date
        ("municipality", "municipality-lead", "responsible", "2025-01-01"),
        # Simplified formal exam, set to submit date
        ("municipality", "municipality-lead", "responsible_simplified", "2025-01-01"),
        # Not simplified formal exam, set to publication date.
        (
            "municipality",
            "municipality-lead",
            "responsible_not_simplified",
            "2025-02-02",
        ),
        # Inquiry, set to inquiry date.
        (ARE_SERVICE_GROUP, "service-lead", "invited", "2025-03-03"),
        # Not allowed service, don't create deadline
        ("municipality", "municipality-lead", "none", None),
    ],
)
def test_events_deadlines_publication_inquiry_gr(
    db,
    admin_user,
    gr_instance,
    caluma_case_factory,
    caluma_work_item_factory,
    test_case,
    expected_date,
    service_factory,
    gr_distribution_settings,
    gr_additional_demand_settings,
    gr_deadlines_settings,
    set_application_gr,
    mocker,
    utils,
):
    """Test deadline creation and the defined start date for the municipality/ARE.

    For the municipality, the deadline should be created and the start date
    should equal the submit date.
    But if a formal exam is done and it's not simplified, the start date should
    equal the formal exam date.
    For the ARE the deadline should be created and the start date should equal
    the inquiry date.
    Otherwise no deadline should be created.
    """
    group = admin_user.groups.first()
    service = group.service
    case = gr_instance.case
    gr_instance.case.meta["submit-date"] = "2025-01-01T12:00:00+0000"
    gr_instance.case.save()

    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service
        if test_case.startswith("responsible")
        else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=test_case == "invited",
    )
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.trigger_side_effect",
        return_value=False,
    )

    workitem_publication = caluma_work_item_factory(
        case=gr_instance.case,
        task=Task.objects.get(slug="fill-publication"),
        created_by_group=str(service.pk),
        status=WorkItem.STATUS_COMPLETED,
    )
    utils.add_answer(
        workitem_publication.document,
        "ende-publikationsorgan-gemeinde",
        "2025-02-02",
        question_type=caluma_form_models.Question.TYPE_DATE,
    )

    workitem_fill_inquiry = caluma_work_item_factory(
        case=caluma_case_factory(family=gr_instance.case.family),
        task=Task.objects.get(slug="fill-inquiry"),
        addressed_groups=[str(service.pk)],
    )
    workitem_fill_inquiry.created_at = make_aware(datetime(2025, 3, 3, 12, 0))
    workitem_fill_inquiry.save()

    workitem_inquiry = caluma_work_item_factory(
        child_case=workitem_fill_inquiry.case,
        case=gr_instance.case,
        task=Task.objects.get(slug=gr_distribution_settings["INQUIRY_TASK"]),
        addressed_groups=[str(service.pk)],
    )
    workitem_inquiry.created_at = make_aware(datetime(2025, 3, 3, 12, 0))
    workitem_inquiry.save()

    if test_case.startswith("responsible_"):
        workitem_formal_exam = caluma_work_item_factory(
            case=gr_instance.case,
            task=Task.objects.get(slug="formal-exam"),
            created_by_group=str(service.pk),
            status=WorkItem.STATUS_COMPLETED,
        )
        utils.add_answer(
            workitem_formal_exam.document,
            "verfahrensart",
            "verfahrensart-ordentliches-baubewilligungsverfahren"
            if test_case == "responsible_not_simplified"
            else "verfahrensart-vereinfachtes-baubewilligungsverfahren",
        )

    if test_case.startswith("responsible"):
        # manually create for test, normally created by submitting dossier.
        deadlines_models.InstanceDeadline.objects.create_deadline(
            instance=gr_instance, service=service
        )
        deadlines.post_create_publication(
            sender=None, work_item=workitem_publication, user=None, context=None
        )
        deadlines.post_complete_publication_or_formal_exam(
            sender=None, work_item=workitem_publication, user=None, context=None
        )
    else:
        deadlines.post_create_inquiry(
            sender=None, work_item=workitem_fill_inquiry, user=None, context=None
        )
        deadlines.post_complete_inquiry(
            sender=None, work_item=workitem_inquiry, user=None, context=None
        )

    if test_case == "none":
        assert deadlines_models.InstanceDeadline.objects.count() == 0
    else:
        assert deadlines_models.InstanceDeadline.objects.count() == 1
        deadline = deadlines_models.InstanceDeadline.objects.first()
        assert deadline.instance == case.family.instance
        assert str(deadline.start_date) == expected_date


@pytest.mark.parametrize(
    "service_group__name,role__name", [("municipality", "municipality-lead")]
)
@pytest.mark.parametrize(
    "current_enddate,current_enddate_override,expected_date",
    [
        # if decision is made and deadline enddate is not overridden, update it
        ("2025-03-03", False, "2025-02-02"),
        # if decision is made and deadline enddate is overridden, keep it
        ("2025-03-03", True, "2025-03-03"),
        # if no enddate is set during decision, set it to the decision date
        # regardless of override
        (None, False, "2025-02-02"),
        (None, True, "2025-02-02"),
    ],
)
def test_events_deadlines_decision_gr(
    db,
    admin_user,
    gr_instance,
    caluma_work_item_factory,
    current_enddate,
    current_enddate_override,
    expected_date,
    service_factory,
    instance_deadline_factory,
    gr_distribution_settings,
    gr_additional_demand_settings,
    gr_deadlines_settings,
    gr_decision_settings,
    set_application_gr,
    mocker,
    utils,
):
    group = admin_user.groups.first()
    service = group.service
    case = gr_instance.case

    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service
        if service.service_group.name == "municipality"
        else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=service.service_group.name != "municipality",
    )
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.trigger_side_effect",
        return_value=False,
    )

    assert deadlines_models.Suspension.objects.count() == 0
    assert deadlines_models.InstanceDeadline.objects.count() == 0

    deadline = instance_deadline_factory(
        instance=case.family.instance,
        service=service,
        start_date=date(2025, 1, 1),
        completed=False,
        process_deadline_date_override=current_enddate_override,
        process_deadline_date=date.fromisoformat(current_enddate)
        if current_enddate
        else None,
    )

    workitem_decision = caluma_work_item_factory(
        case=gr_instance.case,
        task=Task.objects.get(slug="decision"),
        created_by_group=str(service.pk),
        status=WorkItem.STATUS_COMPLETED,
    )
    utils.add_answer(
        workitem_decision.document,
        "decision-date",
        "2025-02-02",
        question_type=caluma_form_models.Question.TYPE_DATE,
    )

    deadlines.post_complete_decision(
        sender=None, work_item=workitem_decision, user=None, context=None
    )

    deadline.refresh_from_db()
    assert deadline.completed is True
    assert deadline.instance == case.family.instance
    assert str(deadline.process_deadline_date) == expected_date


@pytest.mark.parametrize(
    "service_group__name,role__name", [("municipality", "municipality-lead")]
)
def test_post_create_inquiry_ag_creates_deadline(
    db,
    admin_user,
    ag_instance,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_case_factory,
    caluma_admin_user,
    service_factory,
    ag_deadlines_settings,
    ag_distribution_settings,
    set_application_ag,
    mocker,
):
    """Test deadline creation when inquiry answer fill work item is created.

    When an inquiry work item is created and no deadline exists,
    a new deadline should be created for the service.
    """
    service = admin_user.groups.first().service

    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service,
    )
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.trigger_side_effect",
        return_value=False,
    )

    inquiry_fill_work_item = caluma_work_item_factory(
        case=caluma_case_factory(family=ag_instance.case.family),
        task=Task.objects.get(
            slug=ag_distribution_settings["INQUIRY_ANSWER_FILL_TASK"]
        ),
        addressed_groups=[str(service.pk)],
        document=caluma_document_factory(),
    )
    caluma_work_item_factory(
        child_case=inquiry_fill_work_item.case,
        case=ag_instance.case,
        task=Task.objects.get(slug=ag_distribution_settings["INQUIRY_TASK"]),
        addressed_groups=[str(service.pk)],
        document=caluma_document_factory(),
    )

    assert ag_instance.deadlines.count() == 0

    post_create_inquiry(
        sender=None,
        work_item=inquiry_fill_work_item,
        user=caluma_admin_user,
        context={},
    )

    # Verify deadline was created
    assert ag_instance.deadlines.count() == 1
    deadline = ag_instance.deadlines.first()
    assert deadline.service == service
    assert deadline.instance == ag_instance


@pytest.mark.parametrize("has_open_suspension", [False, True])
@pytest.mark.parametrize(
    "trigger_action,has_previous_inquiry,inquiry_answer_claim",
    [
        ("redo", False, False),
        ("redo", False, True),
        ("create", False, False),
        ("create", True, False),
        ("create", False, True),
        ("create", True, True),
    ],
)
@pytest.mark.parametrize(
    "service_group__name,role__name", [("service-afb", "service-lead")]
)
def test_post_create_or_redo_inquiry_ag_claim_suspensions(
    db,
    admin_user,
    ag_instance,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_case_factory,
    caluma_admin_user,
    service_factory,
    instance_deadline_factory,
    ag_deadlines_settings,
    ag_distribution_settings,
    set_application_ag,
    has_previous_inquiry,
    inquiry_answer_claim,
    has_open_suspension,
    trigger_action,
    mocker,
):
    """Test suspension end date when post_create_inquiry is triggered.

    When an inquiry work item is created and a deadline already exists,
    any open suspensions should be closed.
    """
    service = admin_user.groups.first().service
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service_factory(),
    )
    mocker.patch("camac.instance.models.Instance.has_inquiry", return_value=True)
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.trigger_side_effect",
        return_value=False,
    )

    deadline = instance_deadline_factory(
        instance=ag_instance,
        service=service,
    )
    inquiry_fill_work_item = caluma_work_item_factory(
        case=caluma_case_factory(family=ag_instance.case.family),
        task=Task.objects.get(
            slug=ag_distribution_settings["INQUIRY_ANSWER_FILL_TASK"]
        ),
        addressed_groups=[str(service.pk)],
        document=caluma_document_factory(),
        closed_at=make_aware(datetime(2025, 1, 2, 12, 0)),
    )
    inquiry_fill_work_item.case.document.answers.create(
        question=caluma_form_models.Question.objects.get(
            slug=ag_distribution_settings["QUESTIONS"]["STATUS"]
        ),
        value=ag_distribution_settings["ANSWERS"]["STATUS"]["CLAIM"]
        if inquiry_answer_claim
        else ag_distribution_settings["ANSWERS"]["STATUS"]["POSITIVE"],
    )
    inquiry_work_item = caluma_work_item_factory(
        child_case=inquiry_fill_work_item.case,
        case=ag_instance.case,
        task=Task.objects.get(slug=ag_distribution_settings["INQUIRY_TASK"]),
        addressed_groups=[str(service.pk)],
        document=caluma_document_factory(),
        created_at=make_aware(datetime(2025, 1, 2, 12, 0)),
        status=WorkItem.STATUS_COMPLETED,
        closed_at=make_aware(datetime(2025, 1, 1, 12, 0)),
    )

    previous_inquiry_work_item = None
    if has_previous_inquiry:
        previous_inquiry_fill_work_item = caluma_work_item_factory(
            case=caluma_case_factory(family=ag_instance.case.family),
            task=Task.objects.get(
                slug=ag_distribution_settings["INQUIRY_ANSWER_FILL_TASK"]
            ),
            addressed_groups=[str(service.pk)],
            document=caluma_document_factory(),
        )
        previous_inquiry_work_item = caluma_work_item_factory(
            case=ag_instance.case,
            child_case=previous_inquiry_fill_work_item.case,
            task=Task.objects.get(slug=ag_distribution_settings["INQUIRY_TASK"]),
            addressed_groups=[str(service.pk)],
            document=caluma_document_factory(),
            created_at=make_aware(datetime(2025, 1, 1, 12, 0)),
            status=WorkItem.STATUS_COMPLETED,
            closed_at=make_aware(datetime(2025, 1, 1, 12, 0)),
        )
        previous_inquiry_fill_work_item.case.document.answers.create(
            question=caluma_form_models.Question.objects.get(
                slug=ag_distribution_settings["QUESTIONS"]["STATUS"]
            ),
            value=ag_distribution_settings["ANSWERS"]["STATUS"]["CLAIM"]
            if inquiry_answer_claim
            else ag_distribution_settings["ANSWERS"]["STATUS"]["POSITIVE"],
        )

    previous_suspension = None
    if has_open_suspension:
        previous_suspension = deadlines_models.Suspension.objects.create(
            deadline=deadline,
            work_item=previous_inquiry_work_item
            if trigger_action == "create"
            else inquiry_work_item,
            start_date=datetime.now().date(),
            reason=deadlines_models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_INQUIRY_CLAIM,
        )

    suspension = deadlines_models.Suspension.objects.create(
        deadline=deadline,
        work_item=inquiry_work_item
        if trigger_action == "create"
        else previous_inquiry_work_item,
        start_date=datetime.now().date(),
        reason=deadlines_models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_INQUIRY_CLAIM,
    )

    assert suspension.end_date is None
    assert deadline.suspensions.count() == (2 if previous_suspension else 1)

    if trigger_action == "create":
        post_create_inquiry(
            sender=None,
            work_item=inquiry_fill_work_item,
            user=caluma_admin_user,
            context={},
        )
    else:
        post_redo_inquiry_ag(
            sender=None,
            work_item=inquiry_work_item,
            user=caluma_admin_user,
            context={},
        )

    suspension.refresh_from_db()
    last_suspension = deadline.suspensions.order_by("-created_at").first()
    assert last_suspension.end_date is not None

    if (
        (trigger_action == "create" and not has_previous_inquiry)
        or inquiry_answer_claim
        or has_open_suspension
    ):
        # new suspension should only be created if the answer was not claim
        # and no open suspension already exists for the workitem.
        assert str(last_suspension.pk == suspension.pk)
        assert last_suspension.start_date == suspension.start_date
    else:
        assert str(last_suspension.pk != suspension.pk)
        assert last_suspension.start_date == (
            previous_inquiry_work_item.closed_at.date()
            if trigger_action == "create"
            else inquiry_fill_work_item.closed_at.date()
        )

    assert ag_instance.deadlines.count() == 1


@pytest.mark.parametrize(
    "service_group__name,role__name", [("municipality", "municipality-lead")]
)
@pytest.mark.parametrize(
    "action,has_suspension",
    [
        ("no_answer", False),
        ("no_deadline", False),
        ("ok", True),
    ],
)
def test_post_complete_inquiry_fill_ag_creates_deadline(
    db,
    admin_user,
    ag_instance,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_case_factory,
    caluma_admin_user,
    service_factory,
    instance_deadline_factory,
    ag_deadlines_settings,
    ag_distribution_settings,
    set_application_ag,
    action,
    has_suspension,
    mocker,
    utils,
):
    """Test suspension created for deadline on completing the fill task.

    When the inquiry fill work item is completed and a deadline already exists,
    a suspension should be created.
    """
    service = admin_user.groups.first().service

    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=False,
    )
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.trigger_side_effect",
        return_value=False,
    )
    if action != "no_deadline":
        instance_deadline_factory(
            instance=ag_instance,
            service=service,
        )

    assert deadlines_models.Suspension.objects.count() == 0

    inquiry_fill_work_item = caluma_work_item_factory(
        case=caluma_case_factory(family=ag_instance.case.family),
        task=Task.objects.get(
            slug=ag_distribution_settings["INQUIRY_ANSWER_FILL_TASK"]
        ),
        addressed_groups=[str(service.pk)],
        document=caluma_document_factory(),
    )
    if action != "no_answer":
        utils.add_answer(
            inquiry_fill_work_item.case.document,
            ag_distribution_settings["QUESTIONS"]["STATUS"],
            "inquiry-answer-status-claim",
            question_type=caluma_form_models.Question.TYPE_CHOICE,
        )

    post_complete_inquiry_fill_ag(
        sender=None,
        work_item=inquiry_fill_work_item,
        user=caluma_admin_user,
        context={},
    )

    if has_suspension:
        deadlines_models.Suspension.objects.count() == 1
        suspension = deadlines_models.Suspension.objects.first()
        assert suspension.deadline.service == service
    else:
        assert deadlines_models.Suspension.objects.count() == 0


@pytest.mark.parametrize(
    "service_group__name,role__name",
    [
        ("municipality", "municipality-lead"),
        ("service-afb", "service-lead"),
    ],
)
def test_post_create_withdrawal_check_closes_suspensions(
    db,
    admin_user,
    ag_instance,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_admin_user,
    service_factory,
    caluma_task_factory,
    instance_deadline_factory,
    suspension_factory,
    ag_deadlines_settings,
    ag_distribution_settings,
    set_application_ag,
    mocker,
):
    """Test open suspensions are closed when any new workitem is created."""
    service = admin_user.groups.first().service

    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service
        if service.service_group.name == "municipality"
        else service_factory(),
    )

    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=service.service_group.name != "municipality",
    )
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.trigger_side_effect",
        return_value=False,
    )

    deadline = instance_deadline_factory(
        instance=ag_instance,
        service=service,
    )
    suspension_factory(
        deadline=deadline,
        start_date=datetime.now().date(),
        end_date=None,
        reason=deadlines_models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_MANUAL,
    )
    suspension_factory(
        deadline=deadline,
        start_date=datetime.now().date(),
        end_date=datetime.now().date(),
        reason=deadlines_models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_MANUAL,
    )

    assert (
        deadlines_models.Suspension.objects.for_deadline(deadline=deadline)
        .only_open()
        .count()
        == 1
    )

    addressed_to_groups = [str(service.pk)]
    controlling_groups = []
    task = Task.objects.filter(slug="withdrawal-check").first() or caluma_task_factory(
        slug="withdrawal-check"
    )

    post_create_withdrawal_check_closes_suspensions(
        sender=None,
        work_item=caluma_work_item_factory(
            case=ag_instance.case,
            task=task,
            addressed_groups=addressed_to_groups,
            controlling_groups=controlling_groups,
            document=caluma_document_factory(),
        ),
        user=caluma_admin_user,
        context={},
    )

    assert (
        deadlines_models.Suspension.objects.for_deadline(deadline=deadline)
        .only_open()
        .count()
        == 0
    )
