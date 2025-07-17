from datetime import datetime

import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow.models import Task, WorkItem
from django.utils.timezone import make_aware
from django.utils.translation import gettext as _

from camac.caluma.extensions.events import deadlines
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
        ("municipality", "municipality-lead", "responsible", "2025-02-02"),
        (ARE_SERVICE_GROUP, "service-lead", "invited", "2025-03-03"),
        ("municipality", "municipality-lead", "none", None),
    ],
)
def test_events_deadlines_publication_inquiry_gr(
    db,
    admin_user,
    gr_instance,
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

    For the municipality, the deadline should be created and the start date should equal the publication date.
    For the ARE the deadline should be created and the start date should equal the inquiry date.
    Otherwise no deadline should be created.
    """
    group = admin_user.groups.first()
    service = group.service
    case = gr_instance.case

    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if test_case == "responsible" else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=test_case == "invited",
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

    workitem_inquiry = caluma_work_item_factory(
        case=gr_instance.case,
        task=Task.objects.get(slug="inquiry"),
        addressed_groups=[str(service.pk)],
    )
    workitem_inquiry.created_at = make_aware(
        datetime.strptime("2025-03-03", "%Y-%m-%d")
    )
    workitem_inquiry.save()

    workitem_fill_inquiry = caluma_work_item_factory(
        case=gr_instance.case,
        task=Task.objects.get(slug="fill-inquiry"),
        addressed_groups=[str(service.pk)],
    )
    workitem_fill_inquiry.created_at = make_aware(
        datetime.strptime("2025-03-03", "%Y-%m-%d")
    )
    workitem_fill_inquiry.save()

    if test_case == "responsible":
        # manually create for test, normally created by submitting dossier.
        deadlines_models.InstanceDeadline.objects.create_deadline(
            instance=gr_instance, service=service
        )
        deadlines.post_complete_publication(
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
    "current_enddate,expected_date",
    [
        # if decision is made and deadline enddate is set, keep it
        ("2025-03-03", "2025-03-03"),
        # if no enddate is set during decision, set it to the decision date
        (None, "2025-02-02"),
    ],
)
def test_events_deadlines_decision_gr(
    db,
    admin_user,
    gr_instance,
    caluma_work_item_factory,
    current_enddate,
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

    assert deadlines_models.Suspension.objects.count() == 0
    assert deadlines_models.InstanceDeadline.objects.count() == 0

    deadline = instance_deadline_factory(
        instance=case.family.instance,
        service=service,
        start_date="2025-01-01",
        process_deadline_date=make_aware(datetime.strptime(current_enddate, "%Y-%m-%d"))
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
    assert deadline.instance == case.family.instance
    assert str(deadline.process_deadline_date) == expected_date
