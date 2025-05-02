from camac.permissions import api as permissions_api
from camac.permissions.events import Trigger


def test_assign_responsible_user_on_acl_creation(
    db,
    access_level_factory,
    ag_instance,
    ag_permissions_settings,
    ag_rulesets_settings,
    caluma_form_factory,
    caluma_work_item_factory,
    mocker,
    responsible_user_rule_factory,
    service_factory,
):
    municipality = service_factory()
    service_1 = service_factory()
    service_2 = service_factory()
    read_only = service_factory()

    access_level_factory(pk="lead-authority")
    access_level_factory(pk="distribution-service")
    access_level_factory(pk="read")

    application_type = caluma_form_factory()

    ag_instance.case.document.form = application_type
    ag_instance.case.document.save()

    mocker.patch(
        "camac.instance.models.Instance.responsible_service", return_value=municipality
    )
    mocker.patch(
        "camac.instance.master_data.MasterData.__getattr__",
        return_value=municipality.pk,
    )
    mocker.patch("camac.permissions.api.PermissionManager.has_all", return_value=True)

    assert ag_instance.responsible_services.count() == 0

    # Municipality: assign via application type
    r1 = responsible_user_rule_factory(service=municipality)
    r1.application_types.set([application_type])
    Trigger.instance_submitted(None, ag_instance)
    assert ag_instance.responsible_services.filter(service=municipality).count() == 1

    # Service 1: assign via municipality
    r2 = responsible_user_rule_factory(service=service_1)
    r2.municipalities.set([municipality])
    Trigger.inquiry_sent(
        None,
        ag_instance,
        caluma_work_item_factory(addressed_groups=[str(service_1.pk)]),
    )
    assert ag_instance.responsible_services.filter(service=service_1).count() == 1

    # Service 2: application type doesn't match
    r3 = responsible_user_rule_factory(service=service_2)
    r3.application_types.set([caluma_form_factory()])
    Trigger.inquiry_sent(
        None,
        ag_instance,
        caluma_work_item_factory(addressed_groups=[str(service_2.pk)]),
    )
    assert ag_instance.responsible_services.filter(service=service_2).count() == 0

    # Read only: assign via application type
    r4 = responsible_user_rule_factory(service=read_only)
    r4.application_types.set([application_type])
    permissions_api.grant(
        ag_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level="read",
        service=read_only,
    )
    assert ag_instance.responsible_services.filter(service=read_only).count() == 1
