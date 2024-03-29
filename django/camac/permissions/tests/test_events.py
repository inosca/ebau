import pytest
from caluma.caluma_workflow import api as workflow_api

from camac.constants import kt_gr as gr_constants
from camac.permissions import events, exceptions
from camac.permissions.models import AccessLevel, InstanceACL
from camac.user.models import ServiceRelation


@pytest.mark.parametrize("instance_state__name", ["submitted"])
def test_event_handler(db, instance, instance_state, instance_state_factory, rf, user):
    class CustomEventHandler(events.EmptyEventHandler):
        def __init__(self, *args, **kwargs):
            self.call_count = 0
            super().__init__(*args, **kwargs)

        @events.decision_dispatch_method
        def instance_post_state_transition(self, instance):
            return instance.instance_state.get_name().lower()

        @instance_post_state_transition.register("submitted")
        def instance_submitted(self, instance):
            self.call_count += 1

    rf.user = user

    handler = CustomEventHandler.from_request(rf)

    handler.instance_post_state_transition(instance=instance)

    assert handler.call_count == 1

    new_state = instance_state_factory(name="rejected")
    instance.instance_state = new_state
    instance.save()

    with pytest.raises(exceptions.MissingEventHandler) as exc:
        handler.instance_post_state_transition(instance=instance)
    assert exc.match("No implementation registered for 'rejected'")


class SubmitCreatePermissions(events.EmptyEventHandler):
    def __init__(self, *args, **kwargs):
        self.call_count = 0
        super().__init__(*args, **kwargs)

    @events.decision_dispatch_method
    def instance_post_state_transition(self, instance):
        return instance.instance_state.get_name().lower()

    @instance_post_state_transition.register("subm")
    def instance_submitted(self, instance):
        # not actual implementation of something real
        municipality = instance.group.service

        self.manager.grant(
            instance,
            grant_type="SERVICE",
            access_level="service",
            service=municipality,
            event_name="instance-submitted",
        )


class CustomTrigger(events.Trigger):
    instance_post_state_transition = events.EventTrigger()


@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize("access_level__slug", ["service"])
def test_instance_submit(db, instance, access_level, permissions_settings):
    permissions_settings["EVENT_HANDLER"] = __name__ + ".SubmitCreatePermissions"

    assert InstanceACL.objects.filter(instance=instance).count() == 0

    CustomTrigger.instance_post_state_transition(None, instance=instance)

    assert InstanceACL.objects.filter(instance=instance).count() == 1


@pytest.mark.parametrize(
    "involve_geometer,geometer_relation_exists,expected_count",
    [(True, True, 1), (True, False, 0), (False, True, 0)],
)
def test_decision_event_handler_be(
    db,
    be_instance,
    involve_geometer,
    geometer_relation_exists,
    expected_count,
    permissions_settings,
    decision_factory,
    instance_state_factory,
    settings,
    application_settings,
    service_factory,
    instance_service_factory,
    caluma_admin_user,
    be_decision_settings,
    use_instance_service,
    be_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    instance_state_factory(name="sb1")
    permissions_settings[
        "EVENT_HANDLER"
    ] = "camac.permissions.config.kt_bern.PermissionEventHandlerBE"

    be_instance.case.document.answers.create(
        question_id="is-paper", value="is-paper-no"
    )

    municipality_service = service_factory(
        service_group__name="municipality",
        trans__name="Leitbehörde Burgdorf",
        trans__language="de",
    )

    service_factory(
        service_group__name="construction-control",
        trans__name="Baukontrolle Burgdorf",
        trans__language="de",
    )

    geometer_service = service_factory(
        service_group__name="Nachführungsgeometer",
    )

    if geometer_relation_exists:
        ServiceRelation.objects.create(
            function=ServiceRelation.FUNCTION_GEOMETER,
            receiver=municipality_service,
            provider=geometer_service,
        )

    instance_service_factory(
        instance=be_instance, service=municipality_service, active=1
    )

    application_settings["ACTIVE_SERVICES"]["MUNICIPALITY"]["FILTERS"] = {
        "service__service_group__name__in": [
            "municipality",
        ]
    }

    for task_id in [
        "submit",
        "ebau-number",
        "distribution",
    ]:
        workflow_api.skip_work_item(
            work_item=be_instance.case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
        )

    instance_state_factory(name="finished")
    decision_factory(
        decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"],
        decision_geometer=(
            "decision-geometer-yes" if involve_geometer else "decision-geometer-no"
        ),
    )
    AccessLevel.objects.create(slug="geometer")

    assert InstanceACL.objects.filter(instance=be_instance).count() == 0

    workflow_api.complete_work_item(
        work_item=be_instance.case.work_items.get(task_id="decision"),
        user=caluma_admin_user,
    )

    acls = InstanceACL.objects.filter(instance=be_instance)
    assert acls.count() == expected_count

    geometer_acl = acls.filter(service=geometer_service)
    assert geometer_acl.count() == expected_count


@pytest.mark.parametrize(
    "checkbox_checked,expected_count",
    [(True, 1), (False, 0)],
)
def test_decision_event_handler_gr(
    db,
    gr_instance,
    checkbox_checked,
    expected_count,
    gr_permissions_settings,
    instance_state_factory,
    settings,
    application_settings,
    answer_factory,
    service_factory,
    caluma_admin_user,
    access_level_factory,
    gr_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_gr"
    gvg_service = service_factory(name=gr_constants.GVG_SERVICE_SLUG)

    for task_id in [
        "submit",
        "formal-exam",
        "distribution",
    ]:
        workflow_api.skip_work_item(
            work_item=gr_instance.case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
        )

    if checkbox_checked:
        answer_factory(
            document=gr_instance.case.work_items.filter(task_id="decision")
            .first()
            .document,
            question__slug="fuer-gvg-freigeben",
            value=["fuer-gvg-freigeben-ja"],
        )
    access_level_factory(slug="read")
    instance_state_factory(name="finished")

    assert InstanceACL.objects.filter(instance=gr_instance).count() == 0

    workflow_api.complete_work_item(
        work_item=gr_instance.case.work_items.get(task_id="decision"),
        user=caluma_admin_user,
    )

    acls = InstanceACL.objects.filter(instance=gr_instance)
    assert acls.count() == expected_count

    gvg_acl = acls.filter(service=gvg_service)
    assert gvg_acl.count() == expected_count


@pytest.mark.parametrize(
    "checkbox_checked,expected_count",
    [(True, 1), (False, 0)],
)
def test_construction_acceptance_event_handler_gr(
    db,
    gr_instance,
    checkbox_checked,
    expected_count,
    gr_permissions_settings,
    instance_state_factory,
    settings,
    answer_factory,
    service_factory,
    caluma_admin_user,
    gr_decision_settings,
    access_level_factory,
    gr_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_gr"
    aib_service = service_factory(name=gr_constants.AIB_SERVICE_SLUG)

    for task_id in [
        "submit",
        "formal-exam",
        "distribution",
    ]:
        workflow_api.skip_work_item(
            work_item=gr_instance.case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
        )

    instance_state_factory(name="construction-acceptance")

    answer_factory(
        document=gr_instance.case.work_items.filter(task_id="decision")
        .first()
        .document,
        question__slug="decision-decision",
        value="decision-decision-approved",
    )

    workflow_api.complete_work_item(
        work_item=gr_instance.case.work_items.get(task_id="decision"),
        user=caluma_admin_user,
    )

    if checkbox_checked:
        answer_factory(
            document=gr_instance.case.work_items.filter(
                task_id="construction-acceptance"
            )
            .first()
            .document,
            question__slug="fuer-aib-freigeben",
            value=["fuer-aib-freigeben-ja"],
        )
    access_level_factory(slug="read")
    instance_state_factory(name="finished")

    assert InstanceACL.objects.filter(instance=gr_instance).count() == 0

    workflow_api.complete_work_item(
        work_item=gr_instance.case.work_items.get(task_id="construction-acceptance"),
        user=caluma_admin_user,
    )

    acls = InstanceACL.objects.filter(instance=gr_instance)
    assert acls.count() == expected_count

    aib_acl = acls.filter(service=aib_service)
    assert aib_acl.count() == expected_count
