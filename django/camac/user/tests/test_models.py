from camac.user.models import Service


def test_service_defaults(db, service):
    new_service = Service.objects.create(service_group_id=service.service_group_id)
    assert new_service.sort == service.sort + 1


def test_service_addressed_work_items(db, service, work_item_factory):
    addressed_work_item = work_item_factory(addressed_groups=[str(service.pk)])
    assert addressed_work_item in service.addressed_work_items
