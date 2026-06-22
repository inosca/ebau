import pytest

from camac.sanctions.models import Sanction


@pytest.mark.django_db
def test_sanction_manager_for_instance_id(instance, new_sanction_factory):
    new_sanction_factory()
    expected = new_sanction_factory(instance=instance)

    queryset = Sanction.objects.for_instance_id(instance.pk)

    assert queryset.count() == 1
    assert queryset.first() == expected


@pytest.mark.django_db
def test_sanction_manager_assigned_to_service_id(service, new_sanction_factory):
    new_sanction_factory()
    expected = new_sanction_factory(assigned_service=service)

    queryset = Sanction.objects.assigned_to_service_id(service.pk)

    assert queryset.count() == 1
    assert queryset.first() == expected


@pytest.mark.django_db
def test_sanction_manager_pending(new_sanction_factory):
    new_sanction_factory(controlled=True)
    expected = new_sanction_factory(controlled=False)

    queryset = Sanction.objects.pending()

    assert queryset.count() == 1
    assert queryset.first() == expected


@pytest.mark.django_db
def test_sanction_manager_for_step(new_sanction_factory):
    expected_step = Sanction.CONTROL_STEPS[0][0]
    other_step = Sanction.CONTROL_STEPS[1][0]

    new_sanction_factory(control_step=other_step)
    expected = new_sanction_factory(control_step=expected_step)

    queryset = Sanction.objects.for_step(expected_step)

    assert queryset.count() == 1
    assert queryset.first() == expected
