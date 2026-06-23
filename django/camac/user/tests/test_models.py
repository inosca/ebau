import pytest

from camac.user.models import Service


@pytest.mark.django_db
def test_service_defaults(service):
    new_service = Service.objects.create(service_group_id=service.service_group_id)
    assert new_service.sort == service.sort + 1


@pytest.mark.django_db
def test_service_addressed_work_items(service, caluma_work_item_factory):
    addressed_work_item = caluma_work_item_factory(addressed_groups=[str(service.pk)])
    assert addressed_work_item in service.addressed_work_items
