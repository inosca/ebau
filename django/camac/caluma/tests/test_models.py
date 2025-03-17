import pytest
from caluma.caluma_workflow.models import WorkItem
from pytest_lazy_fixtures import lf

from camac.caluma.models import Inquiry, build_array_filter, to_groups


def test_inquiry(
    db,
    caluma_task_factory,
    caluma_work_item_factory,
    distribution_settings,
):
    caluma_work_item_factory.create_batch(5)

    inquiry_task = caluma_task_factory(pk=distribution_settings["INQUIRY_TASK"])
    inquiries = caluma_work_item_factory.create_batch(5, task=inquiry_task)

    queryset = Inquiry.objects.all()

    assert WorkItem.objects.count() == 10
    assert queryset.count() == 5
    assert set(queryset.values_list("pk", flat=True)) == set([i.pk for i in inquiries])


@pytest.fixture
def service_one(service_factory):
    return service_factory(pk=998)


@pytest.fixture
def service_two(service_factory):
    return service_factory(pk=999)


@pytest.mark.parametrize(
    "input,output",
    [
        # Simple types
        ("1", ["1"]),
        (1, ["1"]),
        (None, []),
        (lf("service_one"), ["998"]),
        # List types
        (["1", "2"], ["1", "2"]),
        ([1, 2], ["1", "2"]),
        ([1, 2], ["1", "2"]),
        ([None, None], []),
        ([lf("service_one"), lf("service_two")], ["998", "999"]),
        # Mixed list type
        (["1", 2, None, lf("service_one")], ["1", "2", "998"]),
    ],
)
def test_to_groups(db, input, output):
    assert to_groups(input) == output


@pytest.mark.parametrize(
    "values,expected_key",
    [
        ([], "addressed_groups__contains"),
        (["1"], "addressed_groups__contains"),
        (["1", "2"], "addressed_groups__overlap"),
    ],
)
def test_build_array_filter(values, expected_key):
    q_obj = build_array_filter("addressed_groups", values)
    assert len(q_obj.children) == 1
    assert q_obj.children[0][0] == expected_key
