import pytest
from caluma.caluma_form.models import Form
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.instance.models import HistoryEntryT
from camac.instance.utils import get_changeable_forms
from camac.permissions import api as permissions_api


@pytest.mark.parametrize("instance__user", [(lf("admin_user"))])
@pytest.mark.parametrize(
    "role__name,current_form_slug,new_form_slug,starting_instance_state,expected_status",
    [
        (
            "Municipality",
            "baugesuch-reklamegesuch-v2",
            "projektanderung-v2",
            "subm",
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "Municipality",
            "anlassbewilligungen-verkehrsbewilligungen-v3",
            "projektgenehmigungsgesuch-gemass-ss15-strag-v3",
            "subm",
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "Municipality",
            "baugesuch-reklamegesuch-v2",
            "baugesuch-reklamegesuch-v2",
            "subm",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "Municipality",
            "konzession-fur-wasserentnahme",
            "baugesuch-reklamegesuch-v2",
            "subm",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "Municipality",
            "baugesuch-reklamegesuch-v2",
            "konzession-fur-wasserentnahme",
            "subm",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "Municipality",
            "baugesuch-reklamegesuch-v2",
            "projektanderung-v2",
            "circ",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "Applicant",
            "baugesuch-reklamegesuch-v2",
            "projektanderung-v2",
            "subm",
            status.HTTP_403_FORBIDDEN,
        ),
    ],
)
@pytest.mark.django_db
def test_change_form_legacy(
    admin_client,
    application_settings,
    caluma_admin_user,
    current_form_slug,
    expected_status,
    form_factory,
    instance_state_factory,
    mailoutbox,
    new_form_slug,
    notification_template,
    starting_instance_state,
    sz_change_form_settings,
    sz_instance,
):
    notification = {
        "template_slug": notification_template.slug,
        "recipient_types": ["applicant"],
    }
    application_settings["CALUMA"]["SIMPLE_WORKFLOW"]["reject-form"]["notification"] = (
        notification
    )

    complete_work_item(
        work_item=sz_instance.case.work_items.get(task_id="submit"),
        user=caluma_admin_user,
    )

    finished_instance_state = instance_state_factory(name="rejected")
    new_form = form_factory(name=new_form_slug)

    sz_instance.instance_state = instance_state_factory(name=starting_instance_state)
    sz_instance.form = form_factory(name=current_form_slug)
    sz_instance.save()

    response = admin_client.post(
        reverse("instance-change-form", args=[sz_instance.pk]),
        {
            "data": {
                "type": "instance-change-forms",
                "attributes": {"form": new_form_slug},
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        sz_instance.refresh_from_db()

        assert sz_instance.form == new_form
        assert len(mailoutbox) == 1
        assert sz_instance.instance_state == finished_instance_state
        assert HistoryEntryT.objects.filter(
            history_entry__instance=sz_instance,
            language="de",
        ).exists()
        assert WorkItem.objects.filter(task_id="formal-addition").exists()


@pytest.mark.parametrize(
    "role__name,current_form_slug,new_form_slug,expected_status",
    [
        ("Municipality", "baugesuch", "baugesuch-mit-uvp", status.HTTP_204_NO_CONTENT),
        ("Support", "baugesuch", "baugesuch-mit-uvp", status.HTTP_204_NO_CONTENT),
        ("Municipality", "baugesuch", "baugesuch", status.HTTP_400_BAD_REQUEST),
        (
            "Municipality",
            "baugesuch",
            "einfache-vorabklaerung",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "Municipality",
            "einfache-vorabklaerung",
            "baugesuch",
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
@pytest.mark.django_db
def test_change_form(
    admin_client,
    be_change_form_settings,
    be_instance,
    current_form_slug,
    expected_status,
    new_form_slug,
):
    current_form, _ = Form.objects.get_or_create(pk=current_form_slug)
    new_form, _ = Form.objects.get_or_create(pk=new_form_slug)

    workflow = be_instance.case.workflow
    workflow.allow_forms.add(current_form, new_form)

    be_instance.case.document.form = current_form
    be_instance.case.document.save()

    response = admin_client.post(
        reverse("instance-change-form", args=[be_instance.pk]),
        {
            "data": {
                "type": "instance-change-forms",
                "id": be_instance.pk,
                "attributes": {"form": new_form_slug},
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        be_instance.case.refresh_from_db()

        assert be_instance.case.document.form_id == new_form_slug


@pytest.mark.parametrize(
    "instance_state__name,expected_status",
    [
        ("subm", status.HTTP_200_OK),
        ("decision", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_change_form_permissions(
    access_level_factory,
    admin_client,
    ag_instance,
    ag_permissions_settings,
    caluma_form_factory,
    caluma_form_question_factory,
    change_form_settings,
    expected_status,
    service,
):
    permissions_api.grant(
        ag_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level=access_level_factory(pk="lead-authority"),
        service=service,
    )

    new_form = caluma_form_factory()
    current_form = ag_instance.case.document.form

    # Add required question to new form in order to trigger an error in the
    # validation step which will cause the status code to be 200 instead of 204
    caluma_form_question_factory(form=new_form, question__is_required="true")

    change_form_settings["INTERCHANGEABLE_FORMS"] = [[current_form.pk, new_form.pk]]

    response = admin_client.post(
        reverse("instance-change-form", args=[ag_instance.pk]),
        {
            "data": {
                "type": "instance-change-forms",
                "id": ag_instance.pk,
                "attributes": {"form": new_form.slug},
            }
        },
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.django_db
def test_changable_forms(
    admin_client, be_instance, caluma_form_factory, change_form_settings, snapshot
):
    change_form_settings["INTERCHANGEABLE_FORMS"] = [
        [
            be_instance.case.document.form_id,
            caluma_form_factory().pk,
            caluma_form_factory().pk,
        ]
    ]

    response = admin_client.get(
        reverse("instance-changeable-forms", args=[be_instance.pk])
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == snapshot


def test_get_changeable_forms(change_form_settings):
    change_form_settings["INTERCHANGEABLE_FORMS"] = [
        ["foo", "bar"],
        ["foo", "baz"],
    ]

    assert get_changeable_forms("foo") == {"foo", "bar", "baz"}
    assert get_changeable_forms("bar") == {"foo", "bar"}
    assert get_changeable_forms("baz") == {"foo", "baz"}
    assert get_changeable_forms("nope") == set()
