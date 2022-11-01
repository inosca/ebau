from camac.user.models import Service


def test_service_defaults(db, service):
    new_service = Service.objects.create(service_group_id=service.service_group_id)
    assert new_service.sort == service.sort + 1
