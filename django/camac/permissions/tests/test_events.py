import functools

import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.permissions import events, exceptions
from camac.user import models as user_models


@pytest.mark.parametrize("instance_state__name", ["submitted"])
def test_event_handler(db, instance, instance_state, instance_state_factory, rf, user):
    class CustomEventHandler(events.PermissionEventHandler):
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


class SubmitCreatePermissions(events.PermissionEventHandler):
    def __init__(self, *args, **kwargs):
        self.call_count = 0
        super().__init__(*args, **kwargs)

    @events.decision_dispatch_method
    def instance_post_state_transition(self, instance):
        return instance.instance_state.get_name().lower()

    @instance_post_state_transition.register("subm")
    def instance_submitted(self, instance):
        municipality = instance.fields.all().get(name="municipality").value

        self.manager.grant(
            instance,
            grant_type="SERVICE",
            access_level="service",
            # municipality is a subset of all services.
            # TODO: Check if "Leitbehörde" is exactly this one or
            # if we need some indirection
            service=user_models.Service.objects.get(pk=municipality),
            event_name="instance-submitted",
        )


@pytest.mark.freeze_time("2017-7-27")
@pytest.mark.parametrize(
    "instance__user,location__communal_federal_number,instance_state__name",
    [(LazyFixture("admin_user"), "1311", "new")],
)
@pytest.mark.parametrize("attachment__question", ["dokument-parzellen"])
@pytest.mark.parametrize(
    "role__name,instance__location,form__name,status_code",
    [
        ("Applicant", LazyFixture("location"), "baugesuch", status.HTTP_200_OK),
    ],
)
def test_instance_submit(
    admin_client,
    admin_user,
    form,
    form_field_factory,
    instance,
    instance_state,
    access_level_factory,
    service,
    instance_state_factory,
    status_code,
    role_factory,
    group_factory,
    group_location_factory,
    attachment,
    workflow_item,
    notification_template,
    mailoutbox,
    attachment_section,
    role,
    mocker,
    unoconv_pdf_mock,
    caluma_workflow_config_sz,
    caluma_admin_user,
    permissions_settings,
    application_settings,
):
    # Note: This is nearly a 1:1 copy of
    # camac.instance.tests.test_instance.test_instance_submit(). We don't care
    # about the overall behaviour, just whether the permissions event gets
    # properly triggered.
    # TODO: Simplify this as much as possible
    application_settings["NOTIFICATIONS"]["SUBMIT"] = notification_template.slug
    application_settings["WORKFLOW_ITEMS"]["SUBMIT"] = workflow_item.pk
    application_settings["INSTANCE_IDENTIFIER_FORM_ABBR"] = {"vbs": "PV"}
    application_settings["SHORT_DOSSIER_NUMBER"] = False
    application_settings["STORE_PDF"]["SECTION"] = attachment_section.pk

    access_level_factory(slug="service")

    permissions_settings["EVENT_HANDLER"] = f"{__name__ }.SubmitCreatePermissions"

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="baugesuch"),
        user=caluma_admin_user,
    )
    instance.case = case
    instance.save()

    # only create group in a successful run
    if status_code == status.HTTP_200_OK:
        group = group_factory(role=role_factory(name="Municipality"))
        group_location_factory(group=group, location=instance.location)

    instance_state_factory(name="subm")
    url = reverse("instance-submit", args=[instance.pk])
    add_field = functools.partial(form_field_factory, instance=instance)

    # That's the one we care about - note
    # this is just for the infrastructure test, it's got nothing to do
    # with the actual correct relationship between municipality and service
    add_field(name="municipality", value=str(service.pk))

    # Some more stuff to make the form "acceptable"
    add_field(name="kategorie-des-vorhabens", value=["Anlage(n)"])
    add_field(name="hohe-der-anlage", value=12.5)
    add_field(name="hohe-der-anlage-gte", value="Test")
    add_field(name="kosten-der-anlage", value=10001)
    add_field(name="kosten-der-anlage-gt", value="Test")
    add_field(name="tiefe-der-bohrung", value=10)
    add_field(name="tiefe-der-bohrung-lte", value="Test")
    add_field(name="durchmesser-der-bohrung", value=9)
    add_field(name="durchmesser-der-bohrung-lt", value="Test")
    add_field(name="bezeichnung", value="Bezeichnung")
    add_field(name="bewilligung-bohrung", value="Ja")
    add_field(name="bohrungsdaten", value="Test")
    add_field(name="anlagen-mit-erheblichen-schadstoffemissionen", value="Ja")
    add_field(name="anlagen-mit-erheblichen-schadstoffemissionen-welche", value="Test")
    add_field(name="grundeigentumerschaft", value=[{"name": "Bund"}])
    add_field(name="gwr", value=[{"name": "Name", "wohnungen": [{"stockwerk": "1OG"}]}])
    add_field(
        name="punkte", value=[[{"lat": 47.02433179952733, "lng": 8.634144559228435}]]
    )

    # fix permissions
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {"test": {role.name.lower(): {"admin": [attachment_section.pk]}}},
    )

    assert not instance.acls.exists()
    response = admin_client.post(url)
    assert response.status_code == status_code, response.content
    assert instance.acls.filter(access_level_id="service").exists()
