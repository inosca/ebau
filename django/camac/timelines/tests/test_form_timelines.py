import pytest
from django.urls import reverse
from rest_framework import status

from camac.timelines.models import FormTimeline


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_form_timelines_list(
    db,
    admin_client,
    form_timeline_factory,
    instance_factory,
    admin_user,
    caluma_case_factory,
    instance_service_factory,
    instance,
):
    """Test the form timelines list api with instance/permission filtering."""

    group = admin_user.groups.first()
    service = group.service
    instance2 = instance_factory(case=caluma_case_factory())
    instance2.instance_services.add(instance_service_factory(service=service))
    instance3 = instance_factory()

    case1 = caluma_case_factory()
    case2 = caluma_case_factory()
    case3 = caluma_case_factory()

    # timelines for instances with permission.
    timeline1 = form_timeline_factory(
        instance=instance,
        timeline_type=FormTimeline.Type.SUBMIT_AFTER_REJECTION,
    )
    timeline1.cases.add(case1)
    timeline1.save()
    timeline2 = form_timeline_factory(
        instance=instance2,
        timeline_type=FormTimeline.Type.ADDITIONAL_DEMAND,
    )
    timeline2.cases.add(case2)
    timeline2.cases.add(case3)
    timeline2.save()
    # timeline for instance without permission.
    form_timeline_factory(instance=instance3)

    # list all, should only see timelines for instances 1 and 2.
    response = admin_client.get(reverse("form-timelines-list"))
    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    assert len(result) == 2
    ids = {item["id"] for item in result}
    assert ids == {str(timeline1.id), str(timeline2.id)}

    # filter by instance, should only see timeline1.
    response = admin_client.get(
        reverse("form-timelines-list"), {"instance": str(instance.pk)}
    )
    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    assert len(result) == 1
    ids = {item["id"] for item in result}
    assert ids == {str(timeline1.id)}


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_form_timelines_list_missing_annotate(
    db,
    admin_client,
    form_timeline_factory,
    caluma_case_factory,
    instance,
    mocker,
):
    case1 = caluma_case_factory()
    timeline1 = form_timeline_factory(
        instance=instance,
        timeline_type=FormTimeline.Type.SUBMIT_AFTER_REJECTION,
    )
    timeline1.cases.add(case1)
    timeline1.save()

    url = reverse("form-timelines-list")

    # it works like normal
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    # when the queryset is missing the annotate, it fails
    mocker.patch(
        "camac.timelines.views.FormTimelineView.get_base_queryset",
        return_value=FormTimeline.objects.all(),
    )
    with pytest.raises(
        AttributeError, match="The label property requires the cases_count annotation"
    ):
        response = admin_client.get(url)


def test_formtimeline_manager(
    db,
    caluma_work_item_factory,
    caluma_case_factory,
    caluma_task_factory,
    instance_factory,
    additional_demand_settings,
):
    """Test opening and closing additional demand timelines."""
    instance = instance_factory(case=caluma_case_factory())
    caluma_task_factory(pk=additional_demand_settings["TASK"])
    work_item = caluma_work_item_factory(
        task_id=additional_demand_settings["TASK"],
        case=instance.case.family,
        child_case=caluma_case_factory(),
    )

    # first additional demand timeline
    timeline = FormTimeline.objects.open_additional_demand(work_item)
    assert timeline.end_date is None
    assert set(instance.case.meta.get("additional-demand-changes")) == set(
        [str(work_item.child_case.pk)]
    )
    assert timeline.cases.count() == 1

    # second addtional demand while timeline is still open,
    # doesn't create a new timeline, but appends to the existing one.
    work_item2 = caluma_work_item_factory(
        task_id=additional_demand_settings["TASK"],
        case=instance.case.family,
        child_case=caluma_case_factory(),
    )
    timeline2 = FormTimeline.objects.open_additional_demand(work_item2)

    # Should return the same timeline
    assert timeline2.pk == timeline.pk
    assert timeline2.end_date is None
    assert set(instance.case.meta.get("additional-demand-changes")) == set(
        [str(work_item.child_case.pk), str(work_item2.child_case.pk)]
    )
    assert set([str(pk) for pk in timeline2.cases.values_list("pk", flat=True)]) == set(
        [str(work_item.child_case.pk), str(work_item2.child_case.pk)]
    )

    # closing first additional demand, timeline should remain open
    FormTimeline.objects.close_additional_demand(work_item)
    timeline.refresh_from_db()

    assert timeline.end_date is None
    assert str(work_item.child_case.pk) not in instance.case.meta.get(
        "additional-demand-changes"
    )
    assert str(work_item.child_case.pk) not in [
        str(pk) for pk in timeline.cases.values_list("pk", flat=True)
    ]

    # closing second additional demand, timeline should be closed
    FormTimeline.objects.close_additional_demand(work_item2)
    timeline.refresh_from_db()
    assert timeline.end_date is not None
    assert not instance.case.meta.get("additional-demand-changes")
    assert not timeline.cases.exists()

    # creating a new addtional demand should create a new timeline
    work_item3 = caluma_work_item_factory(
        task_id=additional_demand_settings["TASK"],
        case=instance.case.family,
        child_case=caluma_case_factory(),
    )
    timeline3 = FormTimeline.objects.open_additional_demand(work_item3)
    assert timeline3.pk != timeline.pk
    assert timeline3.end_date is None
    assert set(instance.case.meta.get("additional-demand-changes")) == set(
        [str(work_item3.child_case.pk)]
    )
    assert set([str(pk) for pk in timeline3.cases.values_list("pk", flat=True)]) == set(
        [str(work_item3.child_case.pk)]
    )
