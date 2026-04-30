import pytest
from caluma.caluma_workflow.models import WorkItem
from rest_framework.request import Request

from camac.instance.models import Instance
from camac.statistics.filters import InstanceFilterBackend, WorkItemFilterBackend


@pytest.fixture
def instance_qs(statistics_ag_instance):
    return Instance.objects.filter(pk=statistics_ag_instance.pk)


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "query_params,expected_count",
    [
        ({}, 1),
        ({"submit_date_after": "2025-01-01"}, 1),
        ({"submit_date_after": "2025-03-01"}, 0),
        ({"submit_date_before": "2025-12-31"}, 1),
        ({"submit_date_before": "2025-01-01"}, 0),
        ({"form": "main-form"}, 1),
        ({"form": "nonexistent"}, 0),
        ({"first_inquiry_date_after": "2024-12-01"}, 1),
        ({"first_inquiry_date_after": "2025-06-01"}, 0),
        ({"completing_date_after": "2025-01-01"}, 1),
        ({"completing_date_after": "2025-06-01"}, 0),
        ({"involved": "true"}, 1),
        ({"involved": "false"}, 0),
        ({"involved": "invalid"}, 1),
    ],
)
def test_instance_filter_backend(rf, group, instance_qs, query_params, expected_count):
    request = Request(rf.get("/", data=query_params))
    request.group = group
    backend = InstanceFilterBackend()
    pks = backend._filter_instances(request, instance_qs)
    assert len(pks) == expected_count


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_instance_filter_backend_instance_state(
    rf, group, instance_qs, statistics_ag_instance
):
    backend = InstanceFilterBackend()
    state_id = statistics_ag_instance.instance_state_id

    request = Request(rf.get("/", data={"instance_state": str(state_id)}))
    request.group = group
    assert len(backend._filter_instances(request, instance_qs)) == 1

    request = Request(rf.get("/", data={"instance_state": "99999"}))
    request.group = group
    assert len(backend._filter_instances(request, instance_qs)) == 0


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_instance_filter_backend_decision(rf, group, instance_qs, ag_decision_settings):
    backend = InstanceFilterBackend()
    approved = ag_decision_settings["ANSWERS"]["DECISION"]["APPROVED"]

    request = Request(rf.get("/", data={"decision": approved}))
    request.group = group
    assert len(backend._filter_instances(request, instance_qs)) == 1

    request = Request(rf.get("/", data={"decision": "nonexistent"}))
    request.group = group
    assert len(backend._filter_instances(request, instance_qs)) == 0


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_instance_filter_backend_queryset(rf, group, instance_qs):
    request = Request(rf.get("/"))
    request.group = group
    backend = InstanceFilterBackend()
    result = backend.filter_queryset(request, instance_qs, ["dossier_number"])
    assert result.count() == 1
    assert hasattr(result.first(), "dossier_number")


@pytest.mark.parametrize("role__name", ["Service"])
@pytest.mark.parametrize(
    "query_params,expected_count",
    [
        ({}, 1),
        ({"task": "nonexistent-task"}, 0),
        ({"role": "control"}, 0),
        ({"wi_created_at_after": "2024-12-01"}, 1),
        ({"wi_created_at_after": "2025-06-01"}, 0),
        ({"wi_closed_at_before": "2025-06-01"}, 1),
        ({"wi_closed_at_after": "2025-06-01"}, 0),
    ],
)
def test_work_item_filter_backend(
    rf,
    group,
    statistics_ag_instance_afb,
    ag_distribution_settings,
    query_params,
    expected_count,
):
    request = Request(rf.get("/", data=query_params))
    request.group = group
    backend = WorkItemFilterBackend()
    result = backend.filter_queryset(
        request, WorkItem.objects.all(), ["dossier_number"]
    )
    assert result.count() == expected_count


@pytest.mark.parametrize("role__name", ["Service"])
def test_completing_date_filter_excludes_claim_inquiries(
    rf,
    group,
    statistics_ag_instance_afb,
    ag_distribution_settings,
    caluma_answer_factory,
):
    """Inquiries answered with status `claim` don't satisfy the completing date filter."""
    instance_qs = Instance.objects.filter(pk=statistics_ag_instance_afb.pk)
    backend = InstanceFilterBackend()
    params = {"completing_date_after": "2025-01-01"}

    request = Request(rf.get("/", data=params))
    request.group = group
    assert len(backend._filter_instances(request, instance_qs)) == 1

    inquiry = WorkItem.objects.get(
        task_id=ag_distribution_settings["INQUIRY_TASK"],
        case__family=statistics_ag_instance_afb.case,
    )
    caluma_answer_factory(
        document=inquiry.child_case.document,
        question_id=ag_distribution_settings["QUESTIONS"]["STATUS"],
        value=ag_distribution_settings["ANSWERS"]["STATUS"]["CLAIM"],
    )

    request = Request(rf.get("/", data=params))
    request.group = group
    assert len(backend._filter_instances(request, instance_qs)) == 0


@pytest.mark.parametrize("role__name", ["Service"])
def test_excludes_dossiers_with_pending_inquiries(
    rf,
    group,
    statistics_ag_instance_afb,
    active_inquiry_factory,
):
    """Hide dossiers with pending inquiries only when filtering by completing date."""
    instance_qs = Instance.objects.filter(pk=statistics_ag_instance_afb.pk)
    backend = InstanceFilterBackend()
    params = {"completing_date_after": "2025-01-01"}

    request = Request(rf.get("/", data=params))
    request.group = group
    assert len(backend._filter_instances(request, instance_qs)) == 1

    active_inquiry_factory(
        for_instance=statistics_ag_instance_afb,
        addressed_service=group.service,
        status=WorkItem.STATUS_READY,
    )

    # with completing_date filter active: pending inquiry hides the dossier.
    request = Request(rf.get("/", data=params))
    request.group = group
    assert len(backend._filter_instances(request, instance_qs)) == 0

    # without completing_date filter: pending inquiry must NOT hide the dossier.
    request = Request(rf.get("/"))
    request.group = group
    assert len(backend._filter_instances(request, instance_qs)) == 1
