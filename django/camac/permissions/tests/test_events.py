import random
import re
from datetime import timedelta

import pytest
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from camac.constants import kt_gr as gr_constants
from camac.instance.models import Instance, InstanceState
from camac.instance.utils import copy_instance
from camac.permissions import api as permissions_api, events, exceptions
from camac.permissions.models import InstanceACL
from camac.permissions.switcher import PERMISSION_MODE
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
    geometer_changed = events.EventTrigger()


@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize("access_level__slug", ["service"])
def test_instance_submit(db, instance, access_level, permissions_settings):
    permissions_settings["EVENT_HANDLER"] = __name__ + ".SubmitCreatePermissions"

    assert InstanceACL.objects.filter(instance=instance).count() == 0

    CustomTrigger.instance_post_state_transition(None, instance=instance)

    assert InstanceACL.objects.filter(instance=instance).count() == 1


@pytest.mark.parametrize(
    "involve_feuerungskontrolle,expected_count", [(True, 1), (False, 0)]
)
def test_permission_event_handler_be(
    db,
    be_instance,
    involve_feuerungskontrolle,
    permissions_settings,
    expected_count,
    service_factory,
    access_level_factory,
    caluma_question_factory,
):
    access_level_factory(slug="read")
    be_instance.case.document.form.slug = "heat-generator"
    be_instance.case.document.form.save()
    be_instance.case.document.answers.create(
        question=caluma_question_factory(pk="heat-generator-combustion-database-v2"),
        value="heat-generator-combustion-database-v2-ja"
        if involve_feuerungskontrolle
        else "heat-generator-combustion-database_v2-nein",
    )
    service_factory(
        slug="feuerungskontrolle-weu",
    )

    permissions_settings["EVENT_HANDLER"] = (
        "camac.permissions.config.kt_bern.PermissionEventHandlerBE"
    )

    assert InstanceACL.objects.filter(instance=be_instance).count() == 0

    CustomTrigger.instance_submitted(None, instance=be_instance)

    be_instance.refresh_from_db()

    assert InstanceACL.objects.filter(instance=be_instance).count() == expected_count

    assert (
        InstanceACL.objects.filter(
            instance=be_instance,
            service__slug="feuerungskontrolle-weu",
            access_level_id="read",
        ).exists()
        == involve_feuerungskontrolle
    )


@pytest.mark.freeze_time("2025-11-06 15:15:15+02:00")
@pytest.mark.parametrize(
    "involve_geometer,geometer_relation_exists,expected_count,deactivated_municipality",
    [
        (True, True, 2, False),
        (True, False, 1, False),
        (False, True, 1, False),
        (True, True, 1, True),
    ],
)
def test_decision_event_handler_be(
    db,
    be_instance,
    be_permissions_settings,
    decision_factory,
    instance_state_factory,
    settings,
    application_settings,
    service_factory,
    instance_service_factory,
    caluma_dynamic_option_factory,
    caluma_admin_user,
    be_decision_settings,
    use_instance_service,
    be_ech0211_settings,
    be_access_levels,
    involve_geometer,
    geometer_relation_exists,
    expected_count,
    deactivated_municipality,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    instance_state_factory(name="sb1")
    be_permissions_settings["EVENT_HANDLER"] = (
        "camac.permissions.config.kt_bern.GeneralPermissionEventHandlerBE"
    )

    be_instance.case.document.answers.create(
        question_id="is-paper", value="is-paper-no"
    )

    municipality_service = service_factory(
        service_group__name="municipality",
        trans__name="Leitbehörde Burgdorf",
        trans__language="de",
    )

    if deactivated_municipality:
        municipality_service.meta = {
            "deactivated-municipality-at": "2025-11-04T15:15:15+02:00"
        }
        municipality_service.save()

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

    assert InstanceACL.objects.filter(instance=be_instance).count() == 0

    workflow_api.complete_work_item(
        work_item=be_instance.case.work_items.get(task_id="decision"),
        user=caluma_admin_user,
    )

    acls = InstanceACL.objects.filter(instance=be_instance)
    assert acls.count() == expected_count

    geometer_acl = acls.filter(service=geometer_service)

    # expected count includes the construction control
    assert geometer_acl.count() == expected_count - 1


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
    gr_distribution_settings,
    gr_construction_monitoring_settings,
    instance_state_factory,
    settings,
    application_settings,
    caluma_answer_factory,
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
        caluma_answer_factory(
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


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize("role__name", ["Applicant"])
@pytest.mark.parametrize("is_paper", [False, True])
def test_submit_create_acl_be(
    db,
    set_application_be,
    be_instance,
    be_permissions_settings,
    instance_state_factory,
    group_factory,
    mocker,
    multilang,
    admin_client,
    instance_acl_factory,
    service_factory,
    settings,
    application_settings,
    be_access_levels,
    disable_ech0211_settings,
    is_paper,
    utils,
    caplog,
):
    # ensure we can submit
    be_instance.instance_state.name = "new"
    be_instance.instance_state.save()

    # next state must exist
    instance_state_factory(name="subm")

    # Not testing notification here
    application_settings["NOTIFICATIONS"]["SUBMIT"] = []
    application_settings["NOTIFICATIONS"]["PERMISSION_ACL_GRANTED"] = []

    # Don't wanna do *that*
    mocker.patch(
        "camac.instance.serializers.CalumaInstanceSubmitSerializer._generate_and_store_pdf"
    )

    # Set municipality in Caluma form
    municipality_svc = service_factory(service_group__name="municipality")
    utils.add_answer(be_instance.case.document, "gemeinde", str(municipality_svc.pk))
    if is_paper:
        utils.add_answer(be_instance.case.document, "is-paper", "is-paper-yes")

    # Event handler so we actually get the ACL
    be_permissions_settings["EVENT_HANDLER"] = (
        "camac.permissions.config.kt_bern.GeneralPermissionEventHandlerBE"
    )

    be_permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.LOGGING

    # Ensure our user is applicant (both old and new permission style)
    be_instance.involved_applicants.create(
        invitee=admin_client.user, user=admin_client.user
    )
    instance_acl_factory(
        instance=be_instance,
        user=admin_client.user,
        access_level_id="applicant",
        grant_type="USER",
    )

    url = reverse("instance-submit", args=[be_instance.pk])

    # Before submission, there is no municipality access
    acl = be_instance.acls.filter(access_level="lead-authority")
    assert not acl.exists()

    resp = admin_client.post(url)
    assert resp.status_code == status.HTTP_200_OK

    # We currently expect certain discrepancies as the applicant permissions for
    # Kt. BE are not fully configured yet.
    expected_discrepancies = {
        "InstanceView.has_object_submit_permission",
        "CalumaInstanceSerializer.get_permissions",
    }

    logged_discrepancies = set(
        [
            re.match(r"Permissions module discrepancy in `(.*)`", message).group(1)
            for message in caplog.messages
            if message.startswith("Permissions module discrepancy")
        ]
    )

    assert logged_discrepancies == expected_discrepancies, (
        "There are permissions module discrepancies that are either unexpected or are expected but weren't logged"
    )

    # After submission, there must be municipality access unless it's a paper instance
    if is_paper:
        assert not acl.exists()
    else:
        assert acl.get().is_active()


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_change_responsible_service(
    db,
    be_instance,
    admin_client,
    service_factory,
    service,
    disable_ech0211_settings,
    be_access_levels,
    instance_acl_factory,
    be_permissions_settings,
):
    be_permissions_settings["EVENT_HANDLER"] = (
        "camac.permissions.config.kt_bern.GeneralPermissionEventHandlerBE"
    )
    new_responsible = service_factory()

    old_responsible = be_instance.instance_services.get(active=1).service
    old_responsible.service_group.name = "lead-authority"
    old_responsible.service_group.save()

    instance_acl_factory(
        instance=be_instance, access_level_id="lead-authority", service=old_responsible
    )

    active_acls = InstanceACL.currently_active().filter(instance=be_instance)
    involved = active_acls.filter(access_level="involved-authority")
    lead = active_acls.filter(access_level="lead-authority")

    # Check before-change situation: Old responsible must have lead,
    # new service is not assigned at all yet
    assert lead.filter(service=old_responsible).exists()
    assert not lead.filter(service=new_responsible).exists()
    assert not involved.filter(service=new_responsible).exists()
    assert not involved.filter(service=old_responsible).exists()

    url = reverse("instance-change-responsible-service", args=[be_instance.pk])
    resp = admin_client.post(
        url,
        data={
            "data": {
                "relationships": {
                    "to": {"data": {"type": "services", "id": str(new_responsible.pk)}}
                },
                "attributes": {"service-type": "municipality"},
                "id": str(be_instance.pk),
                "type": "instance-change-responsible-services",
            },
        },
    )
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    # The currently_active() method uses the timestamp at call time, so we
    # need to rebuild our QSes, as otherwise revoked ACLs will still appear as
    # active
    active_acls = InstanceACL.currently_active().filter(instance=be_instance)
    involved = active_acls.filter(access_level="involved-authority")
    lead = active_acls.filter(access_level="lead-authority")

    # Check after-change situation: Old responsible must not have lead, but must
    # have involved ACL, new service must have active lead acl
    assert not lead.filter(service=old_responsible).exists()
    assert lead.filter(service=new_responsible).exists()
    assert not involved.filter(service=new_responsible).exists()
    assert involved.filter(service=old_responsible).exists()


@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("is_paper", [False, True])
def test_create_instance_event_be(
    admin_client,
    admin_user,
    form,
    instance_state,
    be_instance,
    role_factory,
    be_access_levels,
    set_application_be,
    caluma_forms_be,
    caluma_workflow_config_be,
    be_permissions_settings,
    is_paper,
    role,
    service_group,
):
    be_permissions_settings["EVENT_HANDLER"] = (
        "camac.permissions.config.kt_bern.GeneralPermissionEventHandlerBE"
    )
    if is_paper:
        service_group.name = "municipality"
        service_group.save()

        set_application_be["PAPER"] = {
            "ALLOWED_ROLES": {"DEFAULT": [role.pk]},
            "ALLOWED_SERVICE_GROUPS": {"DEFAULT": [service_group.pk]},
        }

    url = reverse("instance-list")

    support_role = role_factory(name="support")

    data = {
        "data": {
            "type": "instances",
            "id": None,
            "attributes": {
                "caluma-form": "main-form",
                "caluma-workflow": "building-permit",
            },
            "relationships": {},
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED

    instance_id = response.json()["data"]["id"]
    inst = Instance.objects.get(pk=instance_id)

    support_acl = inst.acls.filter(access_level_id="support").get()

    assert support_acl.is_active()
    assert support_acl.role == support_role

    lead_authority_acl = inst.acls.filter(access_level_id="lead-authority")
    if is_paper:
        assert lead_authority_acl.get().is_active()
    else:
        assert not lead_authority_acl.exists()


@pytest.mark.parametrize("instance_state__name", ["circulation"])
def test_send_inquiry(
    db,
    be_instance,
    active_inquiry_factory,
    notification_template,
    service_factory,
    caluma_admin_user,
    system_operation_user,
    be_permissions_settings,
    be_access_levels,
    disable_ech0211_settings,
    mocker,
):
    be_permissions_settings["EVENT_HANDLER"] = (
        "camac.permissions.config.kt_bern.GeneralPermissionEventHandlerBE"
    )
    mocker.patch(
        "camac.notification.management.commands.send_inquiry_reminders.TEMPLATE_REMINDER_CIRCULATION",
        notification_template.slug,
    )

    inquiry: WorkItem = active_inquiry_factory(
        deadline=timezone.now() - timedelta(days=1),
        meta={"reminders": ["2022-11-30T16:00:00.000000+00:00"]},
    )
    inquiry.status = inquiry.STATUS_SUSPENDED
    inquiry.save()

    acls_before = list(be_instance.acls.all())
    count_before = len(acls_before)

    workflow_api.resume_work_item(work_item=inquiry, user=caluma_admin_user)

    acls_after = be_instance.acls.all()

    assert acls_after.count() == count_before + 1

    new_acl = acls_after.exclude(pk__in=acls_before).get()

    assert new_acl.access_level.slug == "distribution-service"
    assert new_acl.grant_type == "SERVICE"


def test_submitted_so(so_access_levels, so_instance, instance_acl_factory):
    # We test, in other places, the whole calling infra, so here we can
    # get away with just testing the event handler directly

    the_acl = instance_acl_factory(
        instance=so_instance, access_level_id="municipality-before-submission"
    )

    assert the_acl.is_active()
    events.Trigger.instance_submitted(None, so_instance)
    the_acl.refresh_from_db()
    assert not the_acl.is_active()


def test_completed_involve_tax_administration_sz(
    db,
    sz_permissions_settings,
    sz_access_levels,
    sz_instance,
    set_application_sz,
    service_factory,
    caluma_work_item_factory,
):
    tax_administration = service_factory.create(
        slug=set_application_sz["TAX_ADMINISTRATION"]
    )

    events.Trigger.instance_completed(None, sz_instance)

    acls = InstanceACL.objects.filter(
        instance=sz_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level="read",
        service=tax_administration,
    )
    assert acls.exists()


@pytest.mark.parametrize("have_geometer,expect_acl", [(True, True), (False, False)])
def test_decided_involve_geometer_sz(
    db,
    application_settings,
    caluma_admin_user,
    caluma_work_item_factory,
    expect_acl,
    form_field_factory,
    have_geometer,
    instance_state_factory,
    mocker,
    service,
    service_factory,
    settings,
    sz_access_levels,
    sz_construction_monitoring_settings,
    sz_instance,
    sz_permissions_settings,
):
    settings.APPLICATION_NAME = "kt_schwyz"
    is_redac = instance_state_factory(name="redac")
    is_done = instance_state_factory(name="done")
    mocker.patch("camac.notification.utils.send_mail", return_value=None)

    application_settings["GEOMETER_FORM_FIELDS"] = ["geometer"]
    geometer_services = service_factory.create_batch(4)
    application_settings["GEOMETER_SERVICE_MAPPING"] = {
        service.name: service.pk for service in geometer_services
    }

    sz_instance.instance_state = is_redac
    sz_instance.save()
    if have_geometer:
        geometer_service = random.choice(geometer_services)
        form_field_factory.create(
            instance=sz_instance,
            name=random.choice(application_settings["GEOMETER_FORM_FIELDS"]),
            value=geometer_service.name,
        )

    work_item = caluma_work_item_factory(
        task_id="make-decision",
        case=sz_instance.case,
        child_case=None,
        addressed_groups=[service.pk],
        controlling_groups=[service.pk],
        status=WorkItem.STATUS_READY,
    )

    any_geometer_acls = InstanceACL.objects.filter(
        instance=sz_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level="read",
        service__in=geometer_services,
    )
    assert not any_geometer_acls.exists()

    workflow_api.complete_work_item(work_item=work_item, user=caluma_admin_user)
    sz_instance.refresh_from_db()

    assert sz_instance.instance_state == is_done
    if expect_acl:
        wanted_geometer_acls = InstanceACL.objects.filter(
            instance=sz_instance,
            grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
            access_level="read",
            service=geometer_service,
        )
        assert wanted_geometer_acls.exists()
    else:
        assert not any_geometer_acls.exists()


@pytest.mark.parametrize("permission_mode", [PERMISSION_MODE.FULL, PERMISSION_MODE.OFF])
@pytest.mark.parametrize("new_meta_flag", ["is-appeal", "is-rejected-appeal", None])
@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize("instance_state__name", ["subm", "new"])
def test_copy_be(
    be_access_levels,
    be_instance,
    instance_acl_factory,
    instance_state_factory,
    admin_user,
    permission_mode,
    caluma_admin_user,
    role_factory,
    new_meta_flag,
    be_permissions_settings,
):
    be_permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    be_permissions_settings["EVENT_HANDLER"] = (
        "camac.permissions.config.kt_bern.GeneralPermissionEventHandlerBE"
    )

    # support role will get access to the new instance
    role_factory(name="Support")

    instance_acl_factory(
        instance=be_instance,
        access_level_id="lead-authority",
        service=admin_user.groups.first().service,
        grant_type="SERVICE",
    )

    # We expect these ones to be only copied conditionally
    instance_acl_factory(
        instance=be_instance,
        access_level_id="geometer",
    )
    instance_acl_factory(
        instance=be_instance,
        access_level_id="construction-control",
    )

    InstanceState.objects.get_or_create(name="new")
    InstanceState.objects.get_or_create(name="subm")

    new_instance = copy_instance(
        be_instance,
        group=admin_user.groups.first(),
        user=admin_user,
        caluma_user=caluma_admin_user,
        new_meta={"ebau-number": "2024-999", new_meta_flag: True},
        old_meta={"ebau-number": "2024-999"},
    )

    expected_acl_copies = InstanceACL.currently_active().filter(instance=be_instance)
    if new_meta_flag in ["is-appeal", "is-rejected-appeal"]:
        expected_acl_copies = expected_acl_copies.filter(
            access_level__in=["lead-authority", "applicant"]
        )
    else:
        # commandline copy - no restriction
        pass

    # regular copy - needs all active acls to be copied over
    new_active = InstanceACL.currently_active().filter(instance=new_instance)
    for old_acl in expected_acl_copies:
        assert new_active.filter(
            user=old_acl.user,
            access_level=old_acl.access_level,
            service=old_acl.service,
            role=old_acl.role,
            token=old_acl.token,
            grant_type=old_acl.grant_type,
        ).exists(), f"Missing expected copy of {old_acl}"


def test_geometer_changed_event(
    db,
    be_instance,
    service_factory,
    instance_acl_factory,
    be_permissions_settings,
):
    be_permissions_settings["EVENT_HANDLER"] = (
        "camac.permissions.config.kt_bern.GeneralPermissionEventHandlerBE"
    )
    selected_municipality = service_factory()
    selected_geometer = service_factory()
    old_instance_acl = instance_acl_factory(
        instance=be_instance, access_level__slug="geometer"
    )

    be_instance.services.add(selected_municipality)

    CustomTrigger.geometer_changed(
        None,
        instance=be_instance,
        selected_geometer=selected_geometer,
    )

    old_instance_acl.refresh_from_db()

    assert not old_instance_acl.is_active()
    assert (
        InstanceACL.currently_active()
        .filter(service=selected_geometer, access_level="geometer")
        .exists()
    )
