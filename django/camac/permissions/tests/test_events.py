import pytest
from caluma.caluma_workflow import api as workflow_api

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
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    instance_state_factory(name="sb1")
    permissions_settings[
        "EVENT_HANDLER"
    ] = "camac.permissions.config.kt_bern.PermissionEventHandlerBE"

    municipality_service = service_factory(
        service_group__name="municipality",
    )

    geometer_service = service_factory(
        service_group__name="geometer",
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
    decision = decision_factory()
    AccessLevel.objects.create(slug="geometer")

    decision.document.answers.create(
        question_id="decision-geometer",
        value="decision-geometer-yes" if involve_geometer else "decision-geometer-no",
    )

    assert InstanceACL.objects.filter(instance=be_instance).count() == 0

    workflow_api.complete_work_item(
        work_item=be_instance.case.work_items.get(task_id="decision"),
        user=caluma_admin_user,
    )

    acls = InstanceACL.objects.filter(instance=be_instance)
    assert acls.count() == expected_count

    geometer_acl = acls.filter(service=geometer_service)
    assert geometer_acl.count() == expected_count
