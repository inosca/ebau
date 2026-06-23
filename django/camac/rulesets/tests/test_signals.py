import pytest
from caluma.caluma_workflow.models import WorkItem

from camac.permissions import api as permissions_api
from camac.permissions.events.core import Trigger
from camac.tests.form_utils import FormUtils


@pytest.mark.django_db
def test_assign_responsible_user_on_acl_creation(
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
    service_factory(slug="afb")
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

    # Read only: ignored access level, no assignment
    r4 = responsible_user_rule_factory(service=read_only)
    r4.application_types.set([application_type])
    permissions_api.grant(
        ag_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level="read",
        service=read_only,
    )
    assert ag_instance.responsible_services.filter(service=read_only).count() == 0


@pytest.mark.django_db
def test_assign_responsible_user_on_acl_creation_for_paper_dossiers(
    ag_instance,
    ag_permissions_settings,
    ag_rulesets_settings,
    caluma_work_item_factory,
    mocker,
    responsible_user_rule_factory,
    service_factory,
    form_utils: FormUtils,
):
    municipality = service_factory()

    assert WorkItem.objects.filter(status="ready").first().assigned_users == []
    caluma_work_item_factory(
        case=ag_instance.case,
        task_id="paper-test",
        status="ready",
        addressed_groups=[ag_instance.responsible_service().pk],
    )

    mocker.patch(
        "camac.instance.master_data.MasterData.__getattr__",
        return_value=municipality.pk,
    )

    r5 = responsible_user_rule_factory(service=ag_instance.responsible_service())
    r5.municipalities.set([municipality])
    form_utils.add_answer(ag_instance.case.document, "is-paper", "is-paper-yes")
    Trigger.instance_submitted(None, ag_instance)

    assert WorkItem.objects.filter(task_id="paper-test").first().assigned_users == [
        ag_instance.responsible_services.first().responsible_user.username
    ]
