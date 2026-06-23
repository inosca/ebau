import functools
import json
from datetime import datetime

import pytest
import pytz
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.urls import reverse
from django.utils.timezone import make_aware
from pytest_lazy_fixtures import lf, lfc
from rest_framework import status

from camac.applicants.models import Applicant
from camac.conftest import parse_xlsx_response
from camac.constants import kt_uri as uri_constants
from camac.core.models import InstanceLocation, WorkflowEntry
from camac.instance import domain_logic, serializers
from camac.instance.filters import (
    ApplicationCodesFilter,
    CalumaYesNoFilter,
    CaseBabFilter,
    CaseSuspendedFilter,
)
from camac.instance.models import FormField, Instance, InstanceGroup, InstanceState
from camac.permissions import api as permissions_api
from camac.tests.form_utils import FormUtils


@pytest.mark.freeze_time("2018-04-17")
@pytest.mark.parametrize(
    "instance_state__name",
    ["new"],
)
@pytest.mark.parametrize(
    "role__name,instance__user,num_queries,num_instances,editable",
    [
        (
            "Applicant",
            lf("admin_user"),
            20,
            1,
            {"instance", "form", "document"},
        ),
        # reader should see instances from other users but has no editables
        ("Reader", lf("user"), 20, 1, set()),
        ("Canton", lf("user"), 20, 1, {"form", "document"}),
        ("Municipality", lf("user"), 19, 1, {"form", "document"}),
        ("Service", lf("user"), 19, 1, {"form", "document"}),
        ("Public", lf("user"), 2, 0, {}),
    ],
)
def test_instance_list(
    application_settings,
    admin_client,
    instance,
    activation,
    num_queries,
    num_instances,
    group,
    django_assert_num_queries,
    editable,
    group_location_factory,
    instance_service_factory,
    circulation_factory,
    activation_factory,
    gr_linked_instances_settings,
    mocker,
    snapshot,
):
    url = reverse("instance-list")

    # verify that two locations may be assigned to group
    group_location_factory(group=group)

    service = instance_service_factory(instance=instance).service
    activation_factory(service=service, circulation=instance.circulations.first())

    included = serializers.InstanceSerializer.included_serializers
    with django_assert_num_queries(num_queries):
        # Uses the SchwyzInstanceSerializer due to FORM_BACKEND "camac-ng"
        response = admin_client.get(
            url,
            data={
                "include": ",".join(included.keys()),
                "creation_date_before": "17.04.2018",
                "creation_date_after": "17.04.2018",
            },
        )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == num_instances
    if num_instances:
        assert json["data"][0]["id"] == str(instance.pk)
        assert set(json["data"][0]["meta"]["editable"]) == set(editable)
        snapshot.assert_match([i["type"] for i in json["included"]])


@pytest.mark.freeze_time("2023-12-01")
@pytest.mark.parametrize(
    "deadline_date,workitem_status,expected_count",
    [
        ("2023-12-02 00:00:00+00", "completed", 1),
        ("2023-11-30 00:00:00+00", "completed", 1),
        ("2023-11-30 00:00:00+00", "ready", 0),
    ],
)
@pytest.mark.parametrize("role__name,instance__user", [("uso", lf("user"))])
def test_instance_list_for_uso_gr(
    admin_client,
    gr_instance,
    group_factory,
    service_factory,
    caluma_case_factory,
    caluma_work_item_factory,
    workitem_status,
    role,
    deadline_date,
    expected_count,
    distribution_settings,
):
    gr_instance.case = caluma_case_factory(workflow_id="inquiry")
    gr_instance.case.work_items.add(
        caluma_work_item_factory(
            task_id="inquiry",
            addressed_groups=[gr_instance.group.service.pk],
            deadline=deadline_date,
            status=workitem_status,
        )
    )
    gr_instance.group = group_factory(service=service_factory(), role=role)
    gr_instance.save()
    url = reverse("instance-list")

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expected_count


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_instance_detail(admin_client, instance):
    url = reverse("instance-detail", args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("instance__identifier", ["00-00-000"])
@pytest.mark.parametrize("form_field__name", ["name"])
@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
@pytest.mark.parametrize(
    "form_field__value,search",
    [
        ("simpletext", "simple"),
        (["list", "value"], "list"),
        ({"key": ["l-list-d", ["b-list-d"]]}, "list"),
    ],
)
def test_instance_search(admin_client, instance, form_field, search):
    url = reverse("instance-list")

    response = admin_client.get(url, {"search": search})
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(instance.pk)


@pytest.mark.parametrize("role__name", [("Support")])
@pytest.mark.django_db
def test_instance_search_sanctions(
    application_settings,
    ur_instance,
    sanction_factory,
    instance_factory,
    admin_client,
):
    """Test that instances can be filtered correctly.

    Instances must be filter-able by sanction creator and sanction
    control instance.
    """

    application_settings["FORM_BACKEND"] = "caluma"

    sanction = sanction_factory(instance=ur_instance)

    # The following instance should not turn up in the results.
    instance_factory()

    filters = [
        {"sanction_creator": sanction.service.pk},
        {"sanction_control_instance": sanction.control_instance.pk},
    ]

    for search_filter in filters:
        url = reverse("instance-list")
        response = admin_client.get(url, search_filter)
        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json["data"]) == 1
        assert json["data"][0]["id"] == str(ur_instance.pk)


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_instance_filter_fields(admin_client, instance, form_field_factory):
    filters = {}

    for i in range(4):
        value = str(i)
        form_field_factory(name=value, value=value, instance=instance)
        filters["fields[" + value + "]"] = value

    url = reverse("instance-list")

    response = admin_client.get(url, filters)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == 1


@pytest.mark.parametrize(
    "role__name,instance__user,form_filter,form_filter_name,exclude,expected_count",
    [
        ("Applicant", lf("admin_user"), False, None, False, 1),
        ("Applicant", lf("admin_user"), True, None, False, 1),
        ("Applicant", lf("admin_user"), True, None, True, 0),
        ("Applicant", lf("admin_user"), True, "test", False, 0),
        ("Applicant", lf("admin_user"), True, "test", True, 1),
    ],
)
def test_instance_form_name_filter(
    application_settings,
    admin_client,
    instance,
    instance_factory,
    form_filter,
    form_filter_name,
    exclude,
    expected_count,
):
    url = reverse("instance-list")

    if form_filter:
        prefix = "-" if exclude else ""
        name = form_filter_name or instance.form.name
        response = admin_client.get(url, {"form_name": prefix + name})
    else:
        response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "field,submit_date,expected_count",
    [
        ("submit_date_after_sz", "2020-03-02", 1),
        ("submit_date_before_sz", "2022-03-02", 1),
        ("submit_date_after_sz", "2021-04-02", 0),
        ("submit_date_before_sz", "2021-02-02", 0),
        ("submit_date_after_sz", "2021-03-02", 1),
        ("submit_date_before_sz", "2021-03-04", 1),
        ("submit_date_after_sz", "2021-03-03", 1),
        ("submit_date_before_sz", "2021-03-03", 1),
        ("submit_date_after_sz", "2021-03-04", 0),
        ("submit_date_before_sz", "2021-03-02", 0),
    ],
)
def test_instance_submit_date_filter(
    admin_client,
    instance,
    field,
    submit_date,
    expected_count,
    workflow_item_factory,
    workflow_entry_factory,
):
    workflow_entry_factory(
        workflow_item=workflow_item_factory(pk=10),
        workflow_date=make_aware(datetime(2021, 3, 3)),
        instance=instance,
    )

    url = reverse("instance-list")

    response = admin_client.get(url, {field: submit_date})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "address,expected_count",
    [
        ("ous", 1),
        ("Large House", 1),
        ("garden  ", 1),
        ("large  garden", 0),
        ("aa", 0),
        ("hoouse", 0),
        ("Luxury tent", 0),
    ],
)
def test_instance_address_filter(
    application_settings,
    admin_client,
    instance,
    address,
    expected_count,
    form_field_factory,
):
    application_settings["ADDRESS_FORM_FIELDS"] = ["address1", "address2"]
    form_field_factory(
        name="address1",
        value="Large house",
        instance=instance,
    )
    form_field_factory(
        name="address2",
        value="Small garden",
        instance=instance,
    )
    form_field_factory(name="address3", value="Luxury tent", instance=instance)

    url = reverse("instance-list")
    response = admin_client.get(url, {"address_sz": address})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "intent,expected_count",
    [
        ("a", [1, 1, 0]),
        ("aa", [0, 0, 0]),
        ("ous", [1, 0, 0]),
        ("Large House", [1, 0, 0]),
        ("garden  ", [0, 1, 0]),
        ("large  garden", [0, 0, 0]),
        ("hoouse", [0, 0, 0]),
        ("Luxury tent", [0, 0, 0]),
    ],
)
@pytest.mark.parametrize(
    "index,form_field__name,form_field__value,form_field__instance",
    [
        (0, "intent1", "Large house", lf("instance")),
        (1, "intent2", "Small garden", lf("instance")),
        (2, "intent3", "Luxury tent", lf("instance")),
    ],
)
def test_instance_intent_filter(
    application_settings,
    admin_client,
    instance,
    intent,
    expected_count,
    index,
    form_field,
):
    application_settings["INTENT_FORM_FIELDS"] = ["intent1", "intent2"]

    url = reverse("instance-list")
    response = admin_client.get(url, {"intent_sz": intent})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count[index]


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "plot,expected_count",
    [
        ("CH9", 2),
        ("4", 1),
        ("ch967722307039  ", 1),
        ("420", 0),
        ("650", 0),
        ("7899", 1),
        ("420 ch967722307039", 0),
        ("ch9677223070390", 0),
        ("651", 0),
    ],
)
def test_instance_plot_egrid_filter(
    application_settings,
    admin_client,
    instance,
    plot,
    expected_count,
    form_field_factory,
    instance_factory,
):
    instance_1 = instance
    instance_2 = instance_factory(user=instance.user)

    form_field_factory(
        name="parzellen",
        value=[{"egrid": "CH967722307039", "number": 420, "municipality": "Schwyz"}],
        instance=instance_1,
    )
    form_field_factory(
        name="parzellen",
        value=[{"egrid": "CH912734307899", "number": 650, "municipality": "Schwyz"}],
        instance=instance_2,
    )

    url = reverse("instance-list")
    response = admin_client.get(url, {"plot_egrid_sz": plot})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "plot,expected_count",
    [
        ("CH9", 0),
        ("4", 0),
        ("ch967722307039  ", 0),
        (" 420", 1),
        ("7899", 0),
        ("420 ch967722307039", 0),
        ("ch967722307039", 0),
        ("651", 0),
        ("650", 1),
    ],
)
def test_instance_plot_number_filter(
    application_settings,
    admin_client,
    instance,
    plot,
    expected_count,
    form_field_factory,
    instance_factory,
):
    instance_1 = instance
    instance_2 = instance_factory(user=instance.user)

    form_field_factory(
        name="parzellen",
        value=[{"egrid": "CH967722307039", "number": 420, "municipality": "Schwyz"}],
        instance=instance_1,
    )
    form_field_factory(
        name="parzellen",
        value=[{"egrid": "CH912734307899", "number": 650, "municipality": "Schwyz"}],
        instance=instance_2,
    )

    url = reverse("instance-list")
    response = admin_client.get(url, {"plot_number_sz": plot})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count


@pytest.mark.parametrize(
    "role__name,instance__user",
    [
        ("Municipality", lf("admin_user")),
        ("Service", lf("admin_user")),
        ("Applicant", lf("admin_user")),
    ],
)
@pytest.mark.parametrize(
    "value,expected_count",
    [
        ("strasse", {"Municipality": 1, "Service": 1, "Applicant": 1}),
        ("beispie", {"Municipality": 1, "Service": 0, "Applicant": 0}),
        ("Foobar", {"Municipality": 0, "Service": 0, "Applicant": 0}),
        ("bau", {"Municipality": 1, "Service": 1, "Applicant": 0}),
        ("test", {"Municipality": 2, "Service": 2, "Applicant": 1}),
        ("", {"Municipality": 2, "Service": 2, "Applicant": 1}),
        ("Text1", {"Municipality": 0, "Service": 0, "Applicant": 0}),
        ("Text2", {"Municipality": 1, "Service": 1, "Applicant": 0}),
        ('"Inquiry answer 1"', {"Municipality": 1, "Service": 1, "Applicant": 0}),
        ('"Inquiry answer 2"', {"Municipality": 0, "Service": 0, "Applicant": 0}),
        ('"Inquiry answer 3"', {"Municipality": 0, "Service": 0, "Applicant": 0}),
        (
            "Inquiry answer 3",
            {"Municipality": 0, "Service": 0, "Applicant": 0},
        ),  # Search input too short
        ('"Issue A"', {"Municipality": 1, "Service": 1, "Applicant": 0}),
        ("Issue", {"Municipality": 1, "Service": 1, "Applicant": 0}),
        ('"Issue B"', {"Municipality": 0, "Service": 0, "Applicant": 0}),
    ],
)
def test_keyword_search_filter_sz(
    admin_user,
    admin_client,
    sz_instance,
    form_field_factory,
    instance_with_case,
    instance_factory,
    journal_entry_factory,
    service_factory,
    value,
    expected_count,
    sz_distribution_settings,
    active_inquiry_factory,
    caluma_answer_factory,
    service_group_factory,
    settings,
    application_settings,
    location_factory,
    role,
    user_factory,
    group_factory,
    issue_factory,
):
    settings.APPLICATION_NAME = "kt_schwyz"
    application_settings["ROLE_PERMISSIONS"] = {
        "Municipality": "municipality",
        "Service": "service",
    }
    application_settings["INTER_SERVICE_GROUP_VISIBILITIES"] = {
        admin_user.groups.first().service.service_group.pk: [0]
    }

    other_instance = instance_with_case(
        instance_factory(
            user=user_factory(),
            location=location_factory(),
            group=group_factory(),
        )
    )

    # Visible to all
    form_field_factory(
        instance=sz_instance,
        name="bauherrschaft",
        value=[{"strasse": "Teststrasse 2"}],
    )

    # Restricted to municipality
    form_field_factory(
        instance=sz_instance,
        name="einsprecher",
        value=[{"name": "Beispiel"}],
    )

    # Visible to involved service
    form_field_factory(
        instance=other_instance,
        name="kategorie-des-vorhabens",
        value=["Baute(n)", "Anlage(n)"],
    )

    # Not visible
    journal_entry_factory(
        instance=sz_instance,
        visibility="own_organization",
        service=service_factory(),
        text="Text1",
    )

    # Visible to own organisation
    journal_entry_factory(
        instance=sz_instance,
        visibility="own_organization",
        service=admin_user.groups.first().service,
        text="Text2",
    )

    # Visible to involved service
    journal_entry_factory(
        instance=sz_instance,
        visibility="authorities",
        service=service_factory(),
        text="Text3",
    )

    # Visible to involved service
    journal_entry_factory(
        instance=other_instance,
        visibility="all",
        service=service_factory(),
        text="Text4 test",
    )

    # Inquiry visible
    inquiry1 = active_inquiry_factory(
        other_instance,
        addressed_service=admin_user.groups.first().service,
        status=caluma_workflow_models.WorkItem.STATUS_COMPLETED,
    )

    # Inquiry not visible because it hasn't been completed
    inquiry2 = active_inquiry_factory(
        sz_instance,
        controlling_service=admin_user.groups.first().service,
        status=caluma_workflow_models.WorkItem.STATUS_READY,
    )

    # Inquiry not visible because of service group
    other_service = service_factory(service_group=service_group_factory())
    inquiry3 = active_inquiry_factory(
        sz_instance,
        addressed_service=other_service,
        controlling_service=service_factory(),
        status=caluma_workflow_models.WorkItem.STATUS_COMPLETED,
    )

    caluma_answer_factory(
        document=inquiry1.child_case.document,
        question_id=caluma_form_models.Question.objects.get(
            pk=sz_distribution_settings.get("QUESTIONS")["ANCILLARY_CLAUSES"]
        ),
        value="Inquiry answer 1",
    )

    caluma_answer_factory(
        document=inquiry2.child_case.document,
        question_id=caluma_form_models.Question.objects.get(
            pk=sz_distribution_settings.get("QUESTIONS")["REASON"]
        ),
        value="Inquiry answer 2",
    )

    caluma_answer_factory(
        document=inquiry3.child_case.document,
        question_id=caluma_form_models.Question.objects.get(
            pk=sz_distribution_settings.get("QUESTIONS")["REQUEST"]
        ),
        value="Inquiry answer 3",
    )

    # Visible issue
    issue_factory(
        instance=sz_instance, service=admin_user.groups.first().service, text="Issue A"
    )

    # Not visible issue
    issue_factory(instance=other_instance, service=service_factory(), text="Issue B")

    url = reverse("instance-list")
    response = admin_client.get(url, data={"keyword_search": value})

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["data"]) == expected_count[role.name]


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
@pytest.mark.parametrize(
    "with_cantonal_participation,expected_count", [(True, 1), (False, 0)]
)
def test_with_cantonal_participation_filter(
    admin_client,
    ur_instance,
    ur_distribution_settings,
    with_cantonal_participation,
    expected_count,
    caluma_work_item_factory,
):
    if with_cantonal_participation:
        caluma_work_item_factory(
            case=ur_instance.case,
            task_id=ur_distribution_settings["INQUIRY_TASK"],
            status=caluma_workflow_models.WorkItem.STATUS_READY,
            addressed_groups=[uri_constants.KOOR_BG_SERVICE_ID],
        )

    url = reverse("instance-list")
    response = admin_client.get(
        url, data={"with_cantonal_participation": with_cantonal_participation}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "form_field_name,filter_name",
    [
        ("bauherrschaft", "builder_sz"),
        ("grundeigentumerschaft", "landowner_sz"),
        ("projektverfasser-planer", "applicant_sz"),
    ],
)
@pytest.mark.parametrize(
    "search,expected_count",
    [
        (
            "a",
            {
                "bauherrschaft": 2,
                "grundeigentumerschaft": 2,
                "projektverfasser-planer": 2,
            },
        ),
        (
            "Red Stra",
            {
                "bauherrschaft": 1,
                "grundeigentumerschaft": 1,
                "projektverfasser-planer": 1,
            },
        ),
        (
            "melo  ",
            {
                "bauherrschaft": 1,
                "grundeigentumerschaft": 1,
                "projektverfasser-planer": 1,
            },
        ),
        (
            "8840",
            {
                "bauherrschaft": 0,
                "grundeigentumerschaft": 0,
                "projektverfasser-planer": 0,
            },
        ),
        (
            "ious Inc",
            {
                "bauherrschaft": 1,
                "grundeigentumerschaft": 1,
                "projektverfasser-planer": 1,
            },
        ),
        (
            "Tangerine Turbo Mixer 9000",
            {
                "bauherrschaft": 1,
                "grundeigentumerschaft": 1,
                "projektverfasser-planer": 1,
            },
        ),
        (
            "Tangerine Orange",
            {
                "bauherrschaft": 1,
                "grundeigentumerschaft": 1,
                "projektverfasser-planer": 1,
            },
        ),
        (
            "en me",
            {
                "bauherrschaft": 1,
                "grundeigentumerschaft": 1,
                "projektverfasser-planer": 1,
            },
        ),
        (
            "bananaaa",
            {
                "bauherrschaft": 0,
                "grundeigentumerschaft": 0,
                "projektverfasser-planer": 0,
            },
        ),
    ],
)
def test_instance_form_field_list_value_filter(
    application_settings,
    admin_client,
    instance,
    form_field_name,
    filter_name,
    search,
    expected_count,
    form_field_factory,
    instance_factory,
):
    instance_1 = instance
    instance_2 = instance_factory(user=instance.user)

    form_field_factory(
        name=f"{form_field_name}",
        value=[{"name": "Strawberry", "vorname": "Red", "plz": 8840}],
        instance=instance_1,
    )
    form_field_factory(
        name=f"{form_field_name}-v2",
        value=[
            {
                "vorname": "Yellow",
                "firma": "Smoothie-licious Inc.",
                "name": "Banana",
                "plz": 8670,
            }
        ],
        instance=instance_1,
    )

    form_field_factory(
        name=f"{form_field_name}-v2",
        value=[{"name": "Melon", "vorname": "Green", "plz": 8840}],
        instance=instance_2,
    )
    form_field_factory(
        name=f"{form_field_name}-override",
        value=[
            {
                "plz": 8670,
                "vorname": "Orange",
                "name": "Tangerine",
                "firma": "Turbo Mixer 9000 Corp.",
            }
        ],
        instance=instance_2,
    )

    url = reverse("instance-list")
    response = admin_client.get(url, {f"{filter_name}": search})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count[form_field_name]


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
def test_instance_form_name_versioned_filter(
    admin_client,
    instance,
    form_factory,
    instance_factory,
):
    form_0 = form_factory(name="form")
    form_0.family = form_0
    form_0.save()
    instance.form = form_0
    instance.save()

    form_1 = form_factory(family=form_0, name="form-v1")
    instance_factory(form=form_1, user=instance.user)

    form_2 = form_factory(name="form-v2")
    instance_factory(form=form_2, user=instance.user)

    url = reverse("instance-list")

    response = admin_client.get(url, {"form_name_versioned": form_0.pk})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == 2


@pytest.mark.parametrize(
    "instance__user,instance__identifier,identifier,expected_count",
    [
        (lf("admin_user"), "001", "1", 1),
        (lf("admin_user"), "001", "2", 0),
        (lf("admin_user"), "001", "001", 1),
    ],
)
def test_instance_identifier_filter(
    admin_client,
    instance,
    identifier,
    expected_count,
):
    url = reverse("instance-list")

    response = admin_client.get(url, {"identifier": identifier})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count


@pytest.mark.parametrize(
    "instance__user,expected_count",
    [
        (lf("admin_user"), 1),
    ],
)
def test_instance_service_filter_sz(
    admin_client,
    caluma_admin_user,
    instance,
    expected_count,
    sz_instance,
    service,
    active_inquiry_factory,
    distribution_settings,
):
    url = reverse("instance-list")

    case = sz_instance.case
    workflow_api.skip_work_item(
        work_item=case.work_items.get(task_id="submit"), user=caluma_admin_user
    )
    workflow_api.skip_work_item(
        work_item=case.work_items.get(task_id="complete-check"), user=caluma_admin_user
    )

    inquiry = active_inquiry_factory(sz_instance, service, status="ready")

    inquiry.case = case.work_items.get(task_id="distribution").child_case
    inquiry.save()

    response = admin_client.get(url, {"service": service.pk})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count


@pytest.mark.parametrize(
    "instance__user,expected_count",
    [
        (lf("admin_user"), 1),
    ],
)
def test_instance_service_filter_ur(
    admin_client,
    instance,
    expected_count,
    ur_instance,
    service,
    circulation_factory,
    activation_factory,
):
    url = reverse("instance-list")

    circulation_factory(instance=ur_instance)
    activation_factory(circulation=ur_instance.circulations.first(), service=service)

    response = admin_client.get(url, {"service": service.pk})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count


@pytest.mark.parametrize(
    "role__name,instance__user", [("Municipality", lf("admin_user"))]
)
def test_linked_instances(
    admin_client, instance, instance_group_factory, instance_factory
):
    instance.instance_group = instance_group_factory()
    instance.save()
    other_instance = instance_factory(
        location=instance.location, instance_group=instance.instance_group
    )
    url = reverse("instance-detail", args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    linked = json["data"]["relationships"]["linked-instances"]["data"]
    assert len(linked) == 1
    assert int(linked[0]["id"]) == other_instance.pk


@pytest.mark.parametrize(
    "role__name,instance__user", [("Municipality", lf("admin_user"))]
)
def test_involved_services(
    admin_client, group, be_instance, active_inquiry_factory, service_factory
):
    invited_service = service_factory()
    active_inquiry_factory(be_instance, invited_service)
    active_inquiry_factory(
        be_instance,
        service_factory(),
        status=caluma_workflow_models.WorkItem.STATUS_SUSPENDED,
    )
    be_instance.group = group
    be_instance.save()

    url = reverse("instance-detail", args=[be_instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    involved_services = json["data"]["relationships"]["involved-services"]["data"]
    assert len(involved_services) == 2
    assert set([str(invited_service.pk), str(group.service_id)]) == set(
        [service["id"] for service in involved_services]
    )


@pytest.mark.parametrize("main_instance_has_group", [False, True])
@pytest.mark.parametrize("other_instance_has_group", [False, True])
@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        ("Municipality", status.HTTP_200_OK),
        ("Coordination", status.HTTP_200_OK),
        ("TrustedService", status.HTTP_403_FORBIDDEN),
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Canton", status.HTTP_403_FORBIDDEN),
    ],
)
def test_instance_group_link(
    admin_client,
    instance,
    instance_factory,
    instance_group_factory,
    main_instance_has_group,
    other_instance_has_group,
    expected_status,
    mocker,
):
    mocker.patch(
        "camac.constants.kt_uri.KOOR_BG_GROUP_ID", admin_client.user.groups.first().pk
    )

    main_instance = instance
    main_instance.group = admin_client.user.groups.first()
    main_instance.save()

    main_instance_2 = instance_factory()
    other_instance = instance_factory(
        location=main_instance.location, group=admin_client.user.groups.first()
    )
    other_instance_2 = instance_factory()
    if main_instance_has_group:
        main_instance.instance_group = instance_group_factory()
        main_instance.save()
        main_instance_2.instance_group = main_instance.instance_group
        main_instance_2.save()
    if other_instance_has_group:
        other_instance.instance_group = instance_group_factory()
        other_instance.save()
        other_instance_2.instance_group = other_instance.instance_group
        other_instance_2.save()

    url = reverse("instance-link", args=[main_instance.pk])

    data = {
        "data": {
            "type": "instances",
            "attributes": {"link-to": other_instance.pk},
        }
    }

    response = admin_client.patch(
        url, data=json.dumps(data), content_type="application/json"
    )
    main_group_before = main_instance.instance_group
    other_group_before = other_instance.instance_group

    main_instance.refresh_from_db()
    main_instance_2.refresh_from_db()
    other_instance.refresh_from_db()
    other_instance_2.refresh_from_db()

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    if main_instance_has_group:
        assert main_instance.instance_group == main_group_before
        assert main_instance_2.instance_group == main_group_before
        assert other_instance.instance_group == main_group_before
        if other_instance_has_group:
            assert other_instance_2.instance_group == main_group_before
        else:
            assert other_instance_2.instance_group is None
    elif other_instance_has_group:
        assert main_instance.instance_group == other_group_before
        assert main_instance_2.instance_group is None
        assert other_instance.instance_group == other_group_before
        assert other_instance_2.instance_group == other_group_before
    else:
        assert main_instance.instance_group == other_instance.instance_group
        assert main_instance_2.instance_group is None
        assert other_instance_2.instance_group is None


@pytest.mark.parametrize("more_than_one_other_group", [False, True])
@pytest.mark.parametrize("role__name", ["Municipality", "Coordination"])
def test_instance_group_unlink(
    admin_client,
    ur_instance,
    instance_factory,
    instance_group_factory,
    more_than_one_other_group,
    mocker,
    application_settings,
    instance_state_factory,
):
    application_settings["FORM_BACKEND"] = "caluma"

    main_instance = ur_instance
    main_instance.instance_group = instance_group_factory()
    main_instance.save()

    instance_state_factory(name="comm")
    instance_state_factory(name="ext")

    other_instance = instance_factory(location=main_instance.location)
    other_instance.instance_group = main_instance.instance_group
    other_instance.save()

    mocker.patch(
        "camac.constants.kt_uri.KOOR_BG_GROUP_ID", admin_client.user.groups.first().pk
    )

    if more_than_one_other_group:
        main_group_before = main_instance.instance_group
        other_instance_2 = instance_factory(location=main_instance.location)
        other_instance_2.instance_group = main_instance.instance_group
        other_instance_2.save()

    url = reverse("instance-unlink", args=[main_instance.pk])

    response = admin_client.patch(url)

    main_instance.refresh_from_db()
    other_instance.refresh_from_db()

    if more_than_one_other_group:
        other_instance_2.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert main_instance.instance_group is None
        assert other_instance.instance_group == main_group_before
        assert other_instance_2.instance_group == main_group_before

    else:
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert main_instance.instance_group is None
        assert other_instance.instance_group is None


@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize(
    "role__name,instance__user,status_code",
    [
        # applicant/reader can't update their own Instance,
        # but might update FormField etc.
        ("Applicant", lf("admin_user"), status.HTTP_200_OK),
        ("Reader", lf("user"), status.HTTP_403_FORBIDDEN),
        ("Canton", lf("user"), status.HTTP_403_FORBIDDEN),
        ("Municipality", lf("user"), status.HTTP_403_FORBIDDEN),
        ("Service", lf("user"), status.HTTP_403_FORBIDDEN),
        ("Unknown", lf("user"), status.HTTP_404_NOT_FOUND),
        ("Coordination", lf("user"), status.HTTP_404_NOT_FOUND),
    ],
)
def test_instance_update(
    admin_client,
    instance,
    location_factory,
    form_factory,
    status_code,
    mocker,
    application_settings,
):
    application_settings["INSTANCE_HIDDEN_STATES"] = {
        "coordination": ["new"],
    }

    url = reverse("instance-detail", args=[instance.pk])

    new_location = location_factory()
    data = {
        "data": {
            "type": "instances",
            "id": instance.pk,
            "relationships": {
                "location": {"data": {"type": "locations", "id": new_location.pk}},
            },
        }
    }

    response = admin_client.patch(url, data=data)
    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        assert InstanceLocation.objects.filter(
            instance=instance, location=new_location
        ).exists()


@pytest.mark.parametrize(
    "role__name,instance__user,instance_state__name,status_code",
    [
        ("Applicant", lf("admin_user"), "new", status.HTTP_204_NO_CONTENT),
        ("Applicant", lf("admin_user"), "subm", status.HTTP_403_FORBIDDEN),
        ("Reader", lf("admin_user"), "new", status.HTTP_204_NO_CONTENT),
        ("Canton", lf("user"), "new", status.HTTP_403_FORBIDDEN),
        ("Municipality", lf("user"), "new", status.HTTP_403_FORBIDDEN),
        ("Service", lf("user"), "new", status.HTTP_403_FORBIDDEN),
        ("Unknown", lf("user"), "new", status.HTTP_404_NOT_FOUND),
    ],
)
def test_instance_destroy(
    admin_client, sz_instance, status_code, location_factory, application_settings
):
    application_settings["CALUMA"]["CREATE_IN_PROCESS"] = True

    url = reverse("instance-detail", args=[sz_instance.pk])

    """
    Add InstanceLocation relationship to make sure it also will be deleted
    when the instance is deleted (cascade deletion).
    """
    instance_location = InstanceLocation.objects.create(
        location=location_factory(), instance=sz_instance
    )

    response = admin_client.delete(url)

    assert response.status_code == status_code

    # verify deleted InstanceLocation if api query was successful
    if response.status_code == status.HTTP_204_NO_CONTENT:
        assert not InstanceLocation.objects.filter(id=instance_location.pk).exists()


@pytest.mark.parametrize(
    "service_group__name,instance__user,instance_state__name,is_paper,status_code",
    [
        ("applicant", lf("admin_user"), "new", False, status.HTTP_204_NO_CONTENT),
        ("applicant", lf("admin_user"), "subm", False, status.HTTP_403_FORBIDDEN),
        ("municipality", lf("admin_user"), "new", True, status.HTTP_204_NO_CONTENT),
        ("municipality", lf("admin_user"), "subm", True, status.HTTP_403_FORBIDDEN),
        ("unknown", lf("user"), "new", False, status.HTTP_404_NOT_FOUND),
    ],
)
def test_instance_destroy_ag(
    admin_client,
    ag_instance,
    is_paper,
    status_code,
    application_settings,
    set_application_ag,
    form_utils: FormUtils,
):
    application_settings["CALUMA"]["CREATE_IN_PROCESS"] = True

    form_utils.set_is_paper(ag_instance.case.document, is_paper)

    url = reverse("instance-detail", args=[ag_instance.pk])

    response = admin_client.delete(url)

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "instance_state__name,instance__location",
    [("new", None), ("new", lf("location"))],
)
def test_instance_create(
    admin_client, admin_user, form, instance_state, instance, caluma_workflow_config_sz
):
    url = reverse("instance-list")

    location_data = (
        {"type": "locations", "id": instance.location.pk} if instance.location else None
    )

    data = {
        "data": {
            "type": "instances",
            "id": None,
            "relationships": {
                "form": {"data": {"type": "forms", "id": form.pk}},
                "location": {"data": location_data},
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED

    json = response.json()

    url = reverse("instance-list")
    response = admin_client.post(url, data=json)
    assert response.status_code == status.HTTP_201_CREATED

    assert (
        json["data"]["attributes"]["modification-date"]
        < (response.json()["data"]["attributes"]["modification-date"])
    )

    if instance.location:
        assert InstanceLocation.objects.filter(
            instance_id=json["data"]["id"], location=instance.location
        ).exists()


@pytest.mark.parametrize(
    "role__name",
    [
        ("Municipality"),
        ("Service"),
        ("Canton"),
    ],
)
@pytest.mark.django_db
def test_instance_create_internal_sz(
    role,
    admin_client,
    application_settings,
    form,
    location,
    instance_state_factory,
    caluma_workflow_config_sz,
):
    application_settings["CALUMA"]["CREATE_IN_PROCESS"] = True

    caluma_form = caluma_form_models.Form.objects.create(
        slug="internal-form",
        meta={"visibility": {"type": "internal"}, "is_creatable": True},
        name="Test",
    )
    internal_instance_state = instance_state_factory(name="internal")
    instance_state_factory(name="new")

    url = reverse("instance-list")
    data = {
        "data": {
            "type": "instances",
            "id": "test",
            "attributes": {
                "caluma-form": caluma_form.slug,
                "caluma-workflow": "internal-document",
            },
            "relationships": {
                "form": {"data": {"type": "forms", "id": form.pk}},
                "location": {"data": {"type": "locations", "id": location.pk}},
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED

    json = response.json()
    assert (
        int(json["data"]["relationships"]["instance-state"]["data"]["id"])
        == internal_instance_state.instance_state_id
    )


@pytest.mark.freeze_time("2017-7-27")
@pytest.mark.parametrize(
    "instance__user,location__communal_federal_number,instance_state__name",
    [(lf("admin_user"), "1311", "new")],
)
@pytest.mark.parametrize("attachment__question", ["dokument-parzellen"])
@pytest.mark.parametrize("short_dossier_number", [True, False])
@pytest.mark.parametrize(
    "role__name,instance__location,form__name,status_code",
    [
        ("Applicant", lf("location"), "baugesuch", status.HTTP_200_OK),
        ("Applicant", lf("location"), "", status.HTTP_400_BAD_REQUEST),
        ("Applicant", None, "baugesuch", status.HTTP_400_BAD_REQUEST),
        (
            "Applicant",
            lfc("location_factory"),
            "baugesuch",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "Applicant",
            lf("location"),
            "geschaeftskontrolle",
            status.HTTP_200_OK,
        ),
        ("Applicant", lf("location"), "baugesuch", status.HTTP_200_OK),
    ],
)
def test_instance_submit_sz(
    admin_client,
    admin_user,
    form,
    form_field_factory,
    instance,
    instance_state,
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
    short_dossier_number,
    mocker,
    unoconv_pdf_mock,
    caluma_workflow_config_sz,
    caluma_admin_user,
    application_settings,
):
    application_settings["SHORT_NAME"] = "sz"
    application_settings["NOTIFICATIONS"]["SUBMIT"] = notification_template.slug
    application_settings["NOTIFICATIONS"]["APPLICANT"] = {
        "NEW": notification_template.slug,
        "EXISTING": notification_template.slug,
    }

    application_settings["WORKFLOW_ITEMS"]["SUBMIT"] = workflow_item.pk
    application_settings["INSTANCE_IDENTIFIER_FORM_ABBR"] = {"vbs": "PV"}
    application_settings["SHORT_DOSSIER_NUMBER"] = short_dossier_number
    application_settings["STORE_PDF"]["SECTION"] = attachment_section.pk

    form.family = form
    form.save()

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
    add_field(name="gwr", value=[{"name": "Name", "wohnungen": [{"stockwerk": "1OG"}]}])
    add_field(
        name="punkte", value=[[{"lat": 47.02433179952733, "lng": 8.634144559228435}]]
    )
    add_field(
        name="grundeigentumerschaft-v2",
        value=[
            {
                "ort": "Test village",
                "plz": 1234,
                "tel": "0123456789",
                "name": "Doe",
                "email": "invalid-email",
                "anrede": "Herr",
                "strasse": "Unterstrasse 123",
                "vorname": "John",
            }
        ],
    )
    add_field(
        name="bauherrschaft-v3",
        value=[
            {
                "ort": "Test city",
                "plz": 9952,
                "tel": "1234567890",
                "name": "Lawouza",
                "email": "test@test.test",
                "anrede": "Frau",
                "strasse": "Oberstrasse 755",
                "vorname": "Yinou",
            }
        ],
    )

    if form.name == "geschaeftskontrolle":
        add_field(name="meta", value='{"formType": "vbs"}')

    # fix permissions
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {"test": {role.name.lower(): {"admin": [attachment_section.pk]}}},
    )

    response = admin_client.post(url)
    assert response.status_code == status_code, response.content

    if status_code == status.HTTP_200_OK:
        json = response.json()

        identifier = "11-17-001" if short_dossier_number else "1311-17-001"
        if form.name == "geschaeftskontrolle":
            identifier = "PV-17-001"

        assert json["data"]["attributes"]["identifier"] == identifier
        assert set(json["data"]["meta"]["editable"]) == set()

        instance.refresh_from_db()
        assert instance.instance_state.name == "subm"

        assert len(mailoutbox) == 2
        mail = mailoutbox[0]
        mail.subject == notification_template.subject

        assert WorkflowEntry.objects.filter(
            instance=instance, workflow_item=workflow_item
        ).exists()

        assert case.work_items.filter(task_id="submit", status="completed").exists()

        involved_person_email = (
            FormField.objects.filter(name="bauherrschaft-v3", instance=instance.pk)
            .get()
            .value[0]["email"]
        )
        assert Applicant.objects.filter(
            instance=instance.pk, email=involved_person_email
        ).exists()

        invalid_person_email = (
            FormField.objects.filter(
                name="grundeigentumerschaft-v2", instance=instance.pk
            )
            .get()
            .value[0]["email"]
        )
        assert not Applicant.objects.filter(
            instance=instance.pk, email=invalid_person_email
        ).exists()


@pytest.mark.parametrize("role__name", ["Canton"])
def test_instance_export_list(
    admin_client,
    user,
    instance_factory,
    django_assert_num_queries,
    form_field_factory,
    instance_state_factory,
):
    url = reverse("instance-export-list")
    instances = instance_factory.create_batch(2, user=user)
    instance_1 = instances[0]
    instance_2 = instances[1]

    # the test situation needs the exact instance stat IDs, so we
    # better make sure they don't trigger duplicate key errors
    state_1 = InstanceState.objects.filter(pk=1).first() or instance_state_factory(pk=1)
    state_2 = InstanceState.objects.filter(pk=2).first() or instance_state_factory(pk=2)

    instance_1.instance_state = state_1
    instance_1.save()

    instance_2.instance_state = state_2
    instance_2.save()

    add_field = functools.partial(form_field_factory, instance=instance_1)
    add_field(
        name="projektverfasser-planer-v2",
        value=[{"name": "Muster Hans"}, {"name": "Beispiel Jean"}],
    )
    add_field(name="bezeichnung", value="Bezeichnung")

    with django_assert_num_queries(4):
        response = admin_client.get(
            url,
            data={
                "instance-state-ids": f"{instance_1.instance_state_id},{instance_2.instance_state_id}"
            },
        )
    assert response.status_code == status.HTTP_200_OK

    book = parse_xlsx_response(response)
    # bookdict is a dict of tuples(name, content)
    sheet = book.bookdict.popitem()[1]
    assert len(sheet) == len(instances)
    row = sheet[0]
    assert "Muster Hans, Beispiel Jean" in row
    assert "Bezeichnung" in row


@pytest.mark.parametrize("attachment__question", ["dokument-parzellen"])
@pytest.mark.parametrize(
    "role__name,instance__user,form__name,status_code,to_type",
    [
        (
            "Applicant",
            lf("admin_user"),
            "baugesuch",
            status.HTTP_200_OK,
            "docx",
        ),
        (
            "Applicant",
            lf("admin_user"),
            "baugesuch",
            status.HTTP_200_OK,
            "pdf",
        ),
        (
            "Applicant",
            lf("admin_user"),
            "baugesuch",
            status.HTTP_400_BAD_REQUEST,
            "invalid",
        ),
    ],
)
def test_instance_export_detail(
    application_settings,
    admin_client,
    form,
    instance,
    form_field_factory,
    status_code,
    to_type,
    attachment,
    unoconv_pdf_mock,
    unoconv_invalid_mock,
):
    application_settings["COORDINATE_QUESTION"] = "punkte"

    url = reverse("instance-export-detail", args=[instance.pk])

    form.family = form
    form.save()

    add_field = functools.partial(form_field_factory, instance=instance)
    add_field(
        name="grundeigentumerschaft",
        value=[{"name": "Muster Hans"}, {"name": "Beispiel Jean"}],
    )
    add_field(
        name="bauherrschaft",
        value=[{"name": "Muster Hans"}, {"firma": "Firma AG", "name": "Beispiel Jean"}],
    )
    add_field(
        name="bauherrschaft-v2",
        value=[{"name": "Muster Hans"}, {"firma": "Firma AG", "name": "Beispiel Jean"}],
    )
    add_field(name="bohrungsdaten", value="Bezeichnung")
    add_field(name="kategorie-des-vorhabens", value=["Anlage(n)", "Baute(n)"])
    add_field(name="baugeruest-errichtet-am", value="2019-20-19")
    add_field(
        name="punkte", value=[{"lat": 47.02433179952733, "lng": 8.634144559228435}]
    )

    response = admin_client.get(url, data={"type": to_type})
    assert response.status_code == status_code


@pytest.mark.freeze_time("2017-7-27")
@pytest.mark.parametrize("separator", ["-"])
@pytest.mark.parametrize(
    "short_dossier_number,use_caluma,prefix,padding,form_abbreviation,caluma_instance_forms,expected",
    (
        [True, False, None, None, None, False, "11-17-011"],
        [False, False, None, None, None, False, "1311-17-011"],
        [False, True, None, None, None, False, "1311-17-011"],
        [True, True, None, None, None, False, "11-17-011"],
        [True, False, None, None, "abbr", False, "AB-17-001"],
        [True, False, "IM", 4, "abbr", False, "AB-17-0001"],
        [True, False, "IM", 4, None, False, "IM-11-17-0011"],
        [True, False, None, None, "abbr", True, "AB-17-011"],
    ),
)
@pytest.mark.parametrize("location__communal_federal_number", ["1311"])
@pytest.mark.django_db
def test_instance_generate_identifier(
    instance,
    instance_factory,
    caluma_case_factory,
    application_settings,
    short_dossier_number,
    form_field_factory,
    use_caluma,
    prefix,
    padding,
    separator,
    form_abbreviation,
    caluma_instance_forms,
    expected,
):
    application_settings["CALUMA"]["SAVE_DOSSIER_NUMBER_IN_CALUMA"] = use_caluma
    application_settings["SHORT_DOSSIER_NUMBER"] = short_dossier_number
    application_settings["SHORT_NAME"] = "ur"

    elements = []

    if form_abbreviation:
        form_abbreviation_value = form_abbreviation[:2].upper()
        application_settings["INSTANCE_IDENTIFIER_FORM_ABBR"] = {
            form_abbreviation: form_abbreviation_value
        } or {}
        form_field_factory(
            name="meta",
            value=json.dumps({"formType": form_abbreviation}),
            instance=instance,
        )
        if caluma_instance_forms:
            application_settings["CALUMA_INSTANCE_FORMS"] = [form_abbreviation]
            elements.append(form_abbreviation_value)

    if prefix:
        elements.append(prefix)

    id_number = separator.join(["17", "010"])
    if not caluma_instance_forms:
        communal_id = short_dossier_number and "11" or "1311"
        id_number = separator.join([communal_id, id_number])

    elements.append(id_number)
    identifier = separator.join(elements)

    if use_caluma or caluma_instance_forms:
        instance.case = caluma_case_factory(meta={"dossier-number": identifier})
        instance.save()
    else:
        instance_factory(identifier=identifier)

    new_identifier = (
        padding
        and domain_logic.CreateInstanceLogic.generate_identifier(
            instance, prefix=prefix, seq_zero_padding=padding
        )
    ) or domain_logic.CreateInstanceLogic.generate_identifier(instance, prefix=prefix)

    assert new_identifier == expected


@pytest.mark.freeze_time("2023-9-20")
@pytest.mark.parametrize("separator", ["-"])
@pytest.mark.parametrize(
    "short_dossier_number,use_caluma,prefix,padding,form_abbreviation,caluma_instance_forms,internal_instance_forms,expected",
    (
        [True, False, None, None, None, False, False, "11-23-011"],
        [False, False, None, None, None, False, False, "1311-23-011"],
        [False, True, None, None, None, False, False, "1311-23-011"],
        [True, True, None, None, None, False, False, "11-23-011"],
        [True, False, None, None, "abbr", False, False, "AB-23-001"],
        [True, False, "IM", 4, "abbr", False, False, "AB-23-0001"],
        [True, False, "IM", 4, None, False, False, "IM-11-23-0011"],
        [True, False, None, None, "abbr", True, False, "AB-23-011"],
        [True, True, None, None, "abbr", True, True, "AB-4010-23-0001"],
    ),
)
@pytest.mark.parametrize("location__communal_federal_number", ["1311"])
@pytest.mark.django_db
def test_instance_generate_identifier_sz(
    instance,
    instance_factory,
    caluma_case_factory,
    application_settings,
    short_dossier_number,
    form_field_factory,
    use_caluma,
    prefix,
    padding,
    separator,
    form_abbreviation,
    caluma_instance_forms,
    internal_instance_forms,
    expected,
):
    application_settings["SHORT_NAME"] = "sz"
    application_settings["CALUMA"]["SAVE_DOSSIER_NUMBER_IN_CALUMA"] = use_caluma
    application_settings["SHORT_DOSSIER_NUMBER"] = short_dossier_number

    elements = []

    if form_abbreviation:
        form_abbreviation_value = form_abbreviation[:2].upper()
        application_settings["INSTANCE_IDENTIFIER_FORM_ABBR"] = {
            form_abbreviation: form_abbreviation_value
        } or {}
        form_field_factory(
            name="meta",
            value=json.dumps({"formType": form_abbreviation}),
            instance=instance,
        )
        if caluma_instance_forms:
            application_settings["CALUMA_INSTANCE_FORMS"] = [form_abbreviation]
            elements.append(form_abbreviation_value)
        if internal_instance_forms:
            application_settings["INTERNAL_INSTANCE_FORMS"] = [form_abbreviation]

    if prefix:
        elements.append(prefix)

    id_number = separator.join(["23", "010"])
    if not caluma_instance_forms:
        communal_id = short_dossier_number and "11" or "1311"
        id_number = separator.join([communal_id, id_number])

    elements.append(id_number)
    identifier = separator.join(elements)

    if use_caluma or caluma_instance_forms:
        instance.case = caluma_case_factory(meta={"dossier-number": identifier})
        instance.save()
    else:
        instance_factory(identifier=identifier)

    if internal_instance_forms:
        instance.group.service_id = "4010"
        instance.save()
    new_identifier = (
        padding
        and domain_logic.CreateInstanceLogic.generate_identifier(
            instance, prefix=prefix, seq_zero_padding=padding
        )
    ) or domain_logic.CreateInstanceLogic.generate_identifier(instance, prefix=prefix)

    assert new_identifier == expected


@pytest.mark.parametrize(
    "existing_dossier_numbers,expected_dossier_number",
    [
        (None, "2023-1"),
        (["2023-1"], "2023-2"),
        (["1999-9999", "2022-99999", "2023-9", "2023-10"], "2023-11"),
    ],
)
@pytest.mark.freeze_time("2023-7-27")
@pytest.mark.django_db
def test_instance_generate_identifier_gr(
    gr_instance,
    instance,
    caluma_case_factory,
    existing_dossier_numbers,
    expected_dossier_number,
    application_settings,
):
    application_settings["SHORT_NAME"] = "gr"
    if existing_dossier_numbers:
        for nr in existing_dossier_numbers:
            caluma_case_factory(meta={"dossier-number": nr})

    assert (
        domain_logic.CreateInstanceLogic.generate_identifier(instance)
        == expected_dossier_number
    )


@pytest.mark.freeze_time("2017-7-27")
@pytest.mark.parametrize(
    "role__name,instance__user,publication_entry__publication_date,publication_entry__publication_end_date,publication_entry__is_published,status_code",
    [
        (
            "Municipality",
            lf("admin_user"),
            datetime(2016, 6, 28, tzinfo=pytz.UTC),
            datetime(2016, 7, 10, tzinfo=pytz.UTC),
            True,
            status.HTTP_200_OK,
        ),
        (
            "PublicReader",
            lf("admin_user"),
            datetime(2017, 6, 28, tzinfo=pytz.UTC),
            datetime(2017, 8, 1, tzinfo=pytz.UTC),
            True,
            status.HTTP_200_OK,
        ),
        (
            "Public",
            lf("admin_user"),
            datetime(2017, 6, 28, tzinfo=pytz.UTC),
            datetime(2017, 7, 10, tzinfo=pytz.UTC),
            True,
            status.HTTP_200_OK,
        ),
        (
            "Public",
            lf("user"),
            datetime(2016, 6, 28, tzinfo=pytz.UTC),
            datetime(2017, 7, 10, tzinfo=pytz.UTC),
            True,
            status.HTTP_404_NOT_FOUND,
        ),
        (
            "PublicReader",
            lf("admin_user"),
            datetime(2017, 6, 26, tzinfo=pytz.UTC),
            datetime(2017, 7, 10, tzinfo=pytz.UTC),
            True,
            status.HTTP_404_NOT_FOUND,
        ),
        (
            "PublicReader",
            lf("admin_user"),
            datetime(2017, 6, 28, tzinfo=pytz.UTC),
            datetime(2017, 7, 10, tzinfo=pytz.UTC),
            False,
            status.HTTP_404_NOT_FOUND,
        ),
    ],
)
def test_instance_detail_publication(
    admin_client, instance, publication_entry, status_code
):
    url = reverse("instance-detail", args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_circulation_state_filter(
    application_settings,
    admin_client,
    instance,
    circulation,
    activation,
    circulation_state,
):
    url = reverse("instance-list")

    state_search = circulation_state.pk

    # first, ensure the instance is found with the correct instance state id
    response = admin_client.get(url, {"circulation_state": state_search})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1

    # second, make sure that it doesn't show up with another instance id
    response = admin_client.get(url, {"circulation_state": circulation_state.pk + 1})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 0


@pytest.mark.parametrize("role__name,", [("Applicant")])
def test_tags_filter(admin_client, admin_user, instance_factory):
    inst_a, inst_b, inst_c = instance_factory.create_batch(3, user=admin_user)
    tag_args = dict(service=admin_user.groups.first().service)

    inst_a.tags.create(name="foo", **tag_args)
    inst_a.tags.create(name="bar", **tag_args)
    inst_b.tags.create(name="bar", **tag_args)
    inst_b.tags.create(name="baz", **tag_args)
    inst_c.tags.create(name="bla", **tag_args)

    url = reverse("instance-list")

    search_expectations = {
        "": [inst_a, inst_b, inst_c],  # "empty" search should list all
        "foo": [inst_a],
        "bar": [inst_a, inst_b],
        "foo,bar": [inst_a],
        "baz,bar": [inst_b],
    }

    for search, expectation in search_expectations.items():
        response = admin_client.get(url, {"tags": search})
        assert response.status_code == status.HTTP_200_OK

        data = response.json()["data"]
        got_ids = set([row["id"] for row in data])
        expect_ids = set([str(inst.pk) for inst in expectation])
        assert got_ids == expect_ids


@pytest.mark.parametrize(
    "role__name,instance_state__name,responsible_service__responsible_user,responsible_service__service, instance_service__active",
    [("Service", "new", lf("user"), lf("service"), 1)],
)
def test_responsible_service_filters(
    admin_client,
    admin_user,
    user,
    user_factory,
    instance,
    instance_factory,
    group,
    service,
    service_factory,
    instance_service,
    instance_service_factory,
    responsible_service,
    responsible_service_factory,
    circulation_factory,
    activation,
    activation_factory,
):
    url = reverse("instance-list")

    response = admin_client.get(url)
    # can see the instance
    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["id"] == str(instance.pk)

    # service is responsible for instance
    other_service = service_factory()
    response = admin_client.get(url, data={"responsible_service": service.pk})
    data = response.json()["data"]
    assert len(data) == 1
    assert int(data[0]["id"]) == instance.pk

    # other service has no instances responsible for
    other_service = service_factory()
    response = admin_client.get(url, data={"responsible_service": other_service.pk})
    assert len(response.json()["data"]) == 0

    # user is responsible for this service
    response = admin_client.get(url, data={"responsible_service_user": user.pk})
    data = response.json()["data"]
    assert len(data) == 1
    assert int(data[0]["id"]) == instance.pk

    # no instance is left without responsible user
    response = admin_client.get(url, data={"responsible_service_user": "nobody"})
    data = response.json()["data"]
    assert len(data) == 0

    # create other_instance which is visible for "service"
    other_instance = instance_factory(instance_state__name="subm")
    activation_factory(
        circulation=circulation_factory(instance=other_instance), service=service
    )
    instance_service_factory(instance=other_instance, service=service)

    # other_instance has no responsible user
    response = admin_client.get(url, data={"responsible_service_user": "nobody"})
    data = response.json()["data"]
    assert len(data) == 1
    assert int(data[0]["id"]) == other_instance.pk

    other_user = user_factory()
    other_instance.responsible_services.create(
        service=other_service, responsible_user=other_user
    )

    # other_user of other_service is responsible, so not visible to "service"
    response = admin_client.get(url, data={"responsible_service_user": other_user.pk})
    data = response.json()["data"]
    assert len(data) == 0

    # assign admin_user (the user for admin_client) as responsible user
    responsible_service.responsible_user = admin_user
    responsible_service.save()

    # admin_user making the request is responsible user for instance
    response = admin_client.get(url, data={"responsible_service_user": "own"})
    data = response.json()["data"]
    # other_instance has other_user (and other_service) as responsible so "own" should not return it
    assert len(data) == 1
    assert int(data[0]["id"]) == instance.pk

    # assign other_user as responsible on instance under current service
    instance.responsible_services.filter(
        service=service, responsible_user=admin_user
    ).update(responsible_user=other_user)

    # "own" should now return nothing
    response = admin_client.get(url, data={"responsible_service_user": "own"})
    data = response.json()["data"]
    assert len(data) == 0


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_instance_filter_is_applicant(admin_client, instance):
    url = reverse("instance-list")

    response = admin_client.get(url, {"is_applicant": 1})
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == 1

    response = admin_client.get(url, {"is_applicant": 0})
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == 0


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
@pytest.mark.parametrize("is_finished,expected", [(True, 0), (False, 1)])
def test_instance_filter_pending_sanctions_control_instance(
    admin_client, admin_user, instance, sanction_factory, is_finished, expected
):
    url = reverse("instance-list")
    sanction = sanction_factory(instance=instance, is_finished=is_finished)

    response = admin_client.get(
        url, data={"pending_sanctions_control_instance": sanction.control_instance_id}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expected


@pytest.mark.parametrize("role__name", ["Applicant"])
def test_instance_form_field_ordering(
    admin_client, admin_user, instance_factory, form_field_factory
):
    url = reverse("instance-list")

    instances = instance_factory.create_batch(2, user=admin_user)

    add_field = functools.partial(form_field_factory, instance=instances[0])
    add_field(name="bezeichnung", value="ABC")
    add_field = functools.partial(form_field_factory, instance=instances[1])
    add_field(name="bezeichnung", value="ZYX")

    response = admin_client.get(url, {"sort_form_field": "bezeichnung"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == 2
    assert data[0]["id"] == str(instances[0].pk)
    assert data[1]["id"] == str(instances[1].pk)

    response = admin_client.get(url, {"sort_form_field": "-bezeichnung"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == 2
    assert data[0]["id"] == str(instances[1].pk)
    assert data[1]["id"] == str(instances[0].pk)


@pytest.mark.parametrize("role__name", ["Commission"])
@pytest.mark.parametrize("has_assignment", [True, False])
@pytest.mark.django_db
def test_instance_list_commission(admin_client, has_assignment, request, instance):
    """Ensure that a commission only sees dossiers which they were invited on."""

    if has_assignment:
        request.getfixturevalue("commission_assignment")

    url = reverse("instance-list")
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    if has_assignment:
        assert len(json["data"]) == 1
        assert json["data"][0]["id"] == str(instance.pk)
    else:
        assert len(json["data"]) == 0


@pytest.mark.parametrize("role__name", ["building_commission"])
@pytest.mark.django_db
def test_instance_list_building_commission(
    admin_client, request, ur_instance, caluma_work_item_factory
):
    caluma_work_item_factory(
        addressed_groups=[str(admin_client.user.groups.first().service.pk)],
        case=ur_instance.case,
    )
    url = reverse("instance-list")
    response = admin_client.get(url)
    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(ur_instance.pk)


@pytest.mark.parametrize("role__name", ["OrganizationReadonly"])
@pytest.mark.django_db
def test_instance_list_organization_readonly(
    admin_client, request, instance_factory, location_factory, form_factory, mocker
):
    """Ensure that a readonly organization only sees their own dossiers."""

    visible_form = form_factory()
    hidden_form = form_factory()
    mocker.patch("camac.constants.kt_uri.FORM_VORABKLAERUNG", visible_form.pk)

    instance = instance_factory(
        instance_state__name="new",
        form_id=visible_form.pk,
        location=admin_client.user.groups.first().locations.first(),
    )
    instance = instance_factory(
        instance_state__name="circ",
        form_id=hidden_form.pk,
        location=admin_client.user.groups.first().locations.first(),
    )
    instance = instance_factory(
        instance_state__name="circ",
        form_id=visible_form.pk,
        location=location_factory(),
    )

    instance = instance_factory(
        instance_state__name="circ",
        form_id=visible_form.pk,
        location=admin_client.user.groups.first().locations.first(),
    )

    url = reverse("instance-list")
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(instance.pk)


@pytest.mark.django_db
def test_linked_instances_ur(ur_instance, instance_factory, set_application_ur):
    instance_group = InstanceGroup.objects.create()
    other_instance = instance_factory(instance_group=instance_group)

    assert len(ur_instance.get_linked_instances()) == 0

    ur_instance.instance_group = instance_group
    ur_instance.save()

    ur_instance.refresh_from_db()
    assert list(ur_instance.get_linked_instances()) == [other_instance]


@pytest.mark.django_db
def test_is_active_or_involved_lead_authority(
    instance,
    instance_service_factory,
    service_factory,
    use_instance_service,
):
    service = service_factory()
    instance_service = instance_service_factory(
        instance=instance, service=service, active=1
    )

    assert instance.is_active_or_involved_lead_authority(service.pk)

    instance_service.active = 0
    instance_service.save()
    assert instance.is_active_or_involved_lead_authority(service.pk)

    instance_service.delete()
    assert not instance.is_active_or_involved_lead_authority(service.pk)


@pytest.mark.django_db
def test_has_inquiry(
    gr_instance,
    service_factory,
    caluma_work_item_factory,
    gr_distribution_settings,
):
    service = service_factory()
    inquiry = caluma_work_item_factory(
        task=caluma_workflow_models.Task.objects.get(slug="inquiry"),
        case=gr_instance.case,
        addressed_groups=[str(service.pk)],
        status=caluma_workflow_models.WorkItem.STATUS_READY,
    )

    assert gr_instance.has_inquiry(service.pk)

    inquiry.status = caluma_workflow_models.WorkItem.STATUS_SUSPENDED
    inquiry.save()

    assert not gr_instance.has_inquiry(service.pk)

    inquiry.status = caluma_workflow_models.WorkItem.STATUS_CANCELED
    inquiry.save()

    assert not gr_instance.has_inquiry(service.pk)

    inquiry.delete()

    assert not gr_instance.has_inquiry(service.pk)


@pytest.mark.parametrize(
    "inquiry_state,has_open_work_item,expected",
    [
        ("pending", True, 1),
        ("pending", False, 0),
        ("completed", True, 0),
        ("completed", False, 1),
    ],
)
@pytest.mark.parametrize("access_level__slug", ["distribution-service"])
def test_inquiry_state_filter(
    admin_user,
    admin_client,
    caluma_workflow_config_gr,
    instance_with_case,
    instance_factory,
    caluma_work_item_factory,
    gr_distribution_settings,
    gr_permissions_settings,
    caluma_document_factory,
    inquiry_state,
    has_open_work_item,
    expected,
    access_level,
    access_level_factory,
):
    url = reverse("instance-list")

    instance = instance_with_case(instance_factory(user=admin_user))

    # unrelated work item (wrong task)
    caluma_work_item_factory(
        case=instance.case,
        task_id="foo",
        status=caluma_workflow_models.WorkItem.STATUS_READY,
        addressed_groups=[str(admin_client.user.groups.first().service_id)],
    )
    # unrelated work item (wrong addressed group)
    caluma_work_item_factory(
        case=instance.case,
        task_id="inquiry",
        status=caluma_workflow_models.WorkItem.STATUS_READY,
        addressed_groups=["432985034"],
    )
    # unrelated work item (wrong case)
    caluma_work_item_factory(
        task_id="inquiry",
        status=caluma_workflow_models.WorkItem.STATUS_READY,
        addressed_groups=[str(admin_client.user.groups.first().service_id)],
    )
    if has_open_work_item:
        caluma_work_item_factory(
            case=instance.case,
            task_id="inquiry",
            status=caluma_workflow_models.WorkItem.STATUS_READY,
            addressed_groups=[str(admin_client.user.groups.first().service_id)],
        )

    caluma_work_item_factory(
        case=instance.case,
        task_id="inquiry",
        status=caluma_workflow_models.WorkItem.STATUS_COMPLETED,
        addressed_groups=[str(admin_client.user.groups.first().service_id)],
    )
    permissions_api.grant(
        instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level="distribution-service",
        service=admin_client.user.groups.first().service,
    )

    response = admin_client.get(url, data={"inquiry_state": inquiry_state})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expected


@pytest.mark.django_db()
def test_responsible_building_commission(
    mocker, ur_instance, group_factory, location_factory, service_factory
):
    location = location_factory()

    municipality = service_factory()
    building_commission = service_factory(
        service_group__name="Mitglieder Baukommissionen"
    )

    for service in [municipality, building_commission]:
        group = group_factory()
        group.locations.add(location)
        group.save()
        service.groups.add(group)

    mocker.patch.object(ur_instance, "municipality", municipality)

    assert ur_instance.responsible_building_commission == building_commission


@pytest.mark.parametrize(
    "suspended_for,search,expected",
    [
        ("none", None, 1),
        ("none", "0", 1),
        ("none", "1", 0),
        ("self", None, 1),
        ("self", "0", 0),
        ("self", "1", 1),
        ("other", None, 1),
        ("other", "0", 1),
        ("other", "1", 0),
    ],
)
@pytest.mark.django_db
def test_case_suspended_filter_gr(
    service_factory,
    group_factory,
    gr_instance,
    suspended_for,
    search,
    expected,
    rf,
    mocker,
    set_application_gr,
):
    service = service_factory()
    group = group_factory(service=service)
    other_service_1 = service_factory()
    other_service_2 = service_factory()

    if suspended_for == "none":
        gr_instance.case.meta = {}
    elif suspended_for == "self":
        gr_instance.case.meta = {"suspended-services": [str(service.pk)]}
    else:
        gr_instance.case.meta = {
            "suspended-services": [str(other_service_1.pk), str(other_service_2.pk)]
        }
    gr_instance.case.save()

    request = rf.request()
    request.group = group

    suspended_filter = CaseSuspendedFilter()
    parent_mock = mocker.MagicMock()
    parent_mock.request = request
    suspended_filter.parent = parent_mock

    queryset = suspended_filter.filter(queryset=Instance.objects.all(), value=search)

    cases_result = queryset.all()
    assert len(cases_result) == expected


@pytest.mark.parametrize(
    "search,expected",
    [
        ("bib", 2),
        ("bab", 1),
        (None, 3),
    ],
)
@pytest.mark.django_db
def test_case_bab_filter(
    service_factory,
    group_factory,
    instance_factory,
    caluma_case_factory,
    caluma_form_factory,
    search,
    expected,
    rf,
    mocker,
    settings,
):
    settings.BAB = {
        "ENABLED": True,
    }
    service = service_factory()
    group = group_factory(service=service)
    caluma_form_factory(slug="baugesuch-v1")

    # generate 3 instances with BaB values True,False and None
    instance_factory(
        case=caluma_case_factory(
            document__form_id="baugesuch-v1", meta={"is-bab": True}
        )
    )
    instance_factory(
        case=caluma_case_factory(
            document__form_id="baugesuch-v1", meta={"is-bab": False}
        )
    )
    instance_factory(
        case=caluma_case_factory(document__form_id="baugesuch-v1", meta={})
    )

    request = rf.request()
    request.group = group
    suspended_filter = CaseBabFilter()
    parent_mock = mocker.MagicMock()
    parent_mock.request = request
    suspended_filter.parent = parent_mock

    queryset = suspended_filter.filter(queryset=Instance.objects.all(), value=search)

    cases_result = queryset.all()
    assert len(cases_result) == expected


@pytest.mark.parametrize(
    "search,formslug,expected",
    [
        ("bib", "example", 0),
        ("bab", "example", 0),
        (None, "example", 3),
        ("bib", "baugesuch-v1", 2),
        ("bab", "baugesuch-v1", 1),
        (None, "baugesuch-v1", 3),
    ],
)
@pytest.mark.django_db
def test_case_bab_filter_gr(
    service_factory,
    group_factory,
    instance_factory,
    formslug,
    caluma_case_factory,
    caluma_form_factory,
    search,
    expected,
    rf,
    mocker,
    gr_bab_settings,
    set_application_gr,
):
    service = service_factory()
    group = group_factory(service=service)
    caluma_form_factory(slug=formslug)

    # generate 3 instances with BaB values True,False and None
    instance_factory(
        case=caluma_case_factory(document__form_id=formslug, meta={"is-bab": True})
    )
    instance_factory(
        case=caluma_case_factory(document__form_id=formslug, meta={"is-bab": False})
    )
    instance_factory(case=caluma_case_factory(document__form_id=formslug, meta={}))

    request = rf.request()
    request.group = group
    suspended_filter = CaseBabFilter()
    parent_mock = mocker.MagicMock()
    parent_mock.request = request
    suspended_filter.parent = parent_mock

    queryset = suspended_filter.filter(queryset=Instance.objects.all(), value=search)

    cases_result = queryset.all()
    assert len(cases_result) == expected


@pytest.mark.parametrize(
    "service_group_name,suspended_for,search,expected",
    [
        # filter logic for municipality, or parent service
        ("municipality", "none", "0", 1),
        ("municipality", "none", "1", 0),
        ("municipality", "self", "0", 0),
        ("municipality", "self", "1", 1),
        ("municipality", "other", "0", 1),
        ("municipality", "other", "1", 0),
        ("municipality", "parent", "0", 0),
        ("municipality", "parent", "1", 1),
        # service cantonal ignores self and other suspensions
        ("service-cantonal", "none", "0", 1),
        ("service-cantonal", "none", "1", 0),
        ("service-cantonal", "self", "0", 1),
        ("service-cantonal", "self", "1", 0),
        ("service-cantonal", "other", "0", 1),
        ("service-cantonal", "other", "1", 0),
        # service cantonal does filter for afb suspension
        ("service-cantonal", "afb", "0", 0),
        ("service-cantonal", "afb", "1", 1),
        # other services can filter for parent service suspensions
        ("service", "parent", "0", 0),
        ("service", "parent", "1", 1),
    ],
)
@pytest.mark.django_db
def test_case_suspended_filter_ag(
    service_factory,
    group_factory,
    ag_instance,
    service_group_name,
    suspended_for,
    search,
    expected,
    rf,
    mocker,
    set_application_ag,
):
    service = service_factory(service_group__slug=service_group_name)
    group = group_factory(service=service)
    other_service_1 = service_factory()
    other_service_2 = service_factory()
    service_afb = service_factory(service_group__slug="service-afb", slug="afb")

    if suspended_for == "none":
        ag_instance.case.meta = {}
    elif suspended_for == "self":
        ag_instance.case.meta = {"suspended-services": [str(service.pk)]}
    elif suspended_for == "afb":
        ag_instance.case.meta = {"suspended-services": [str(service_afb.pk)]}
    elif suspended_for == "parent":
        service_parent = service_factory()
        service.service_parent = service_parent
        service.save()
        ag_instance.case.meta = {"suspended-services": [str(service_parent.pk)]}
    else:
        ag_instance.case.meta = {
            "suspended-services": [str(other_service_1.pk), str(other_service_2.pk)]
        }
    ag_instance.case.save()

    request = rf.request()
    request.group = group

    suspended_filter = CaseSuspendedFilter()
    parent_mock = mocker.MagicMock()
    parent_mock.request = request
    suspended_filter.parent = parent_mock

    queryset = suspended_filter.filter(queryset=Instance.objects, value=search)

    cases_result = queryset.all()
    assert len(cases_result) == expected


@pytest.mark.parametrize(
    "codes,expected",
    [
        ([], 3),
        ("", 3),
        (["kantonale-pruefung-gesuchscodes-a01"], 1),
        ("kantonale-pruefung-gesuchscodes-a01", 1),
        (
            [
                "kantonale-pruefung-gesuchscodes-a01",
                "kantonale-pruefung-gesuchscodes-a02",
            ],
            2,
        ),
    ],
)
@pytest.mark.django_db
def test_application_codes_filter_ag(
    admin_client,
    rf,
    group,
    mocker,
    ag_instance,
    instance_factory,
    instance_with_case,
    caluma_work_item_factory,
    caluma_answer_factory,
    codes,
    expected,
):
    # create an instance without code answers
    instance_factory()

    cantonal_exam_work_item_1 = caluma_work_item_factory(
        task_id="cantonal-exam",
        case=ag_instance.case,
        status=caluma_workflow_models.WorkItem.STATUS_READY,
        addressed_groups=[str(admin_client.user.groups.first().service_id)],
    )
    cantonal_exam_work_item_2 = caluma_work_item_factory(
        task_id="cantonal-exam",
        case=instance_with_case(instance=instance_factory()).case,
        status=caluma_workflow_models.WorkItem.STATUS_READY,
        addressed_groups=[str(admin_client.user.groups.first().service_id)],
    )
    caluma_answer_factory(
        document=cantonal_exam_work_item_1.document,
        question_id="kantonale-pruefung-gesuchscodes",
        value=codes,
    )
    caluma_answer_factory(
        document=cantonal_exam_work_item_2.document,
        question_id="kantonale-pruefung-gesuchscodes",
        value="kantonale-pruefung-gesuchscodes-a02",
    )
    request = rf.request()
    request.group = group
    application_codes_filter = ApplicationCodesFilter()
    parent_mock = mocker.MagicMock()
    parent_mock.request = request
    application_codes_filter.parent = parent_mock

    queryset = application_codes_filter.filter(qs=Instance.objects.all(), value=codes)

    cases_result = queryset.all()
    assert len(cases_result) == expected


@pytest.mark.parametrize(
    "filter,expected",
    [
        (1, 1),
        (0, 0),
        ("", 1),
    ],
)
@pytest.mark.django_db
def test_retroactive_building_permit_filter_ag(
    rf,
    admin_client,
    group,
    mocker,
    ag_instance,
    filter,
    expected,
    caluma_work_item_factory,
    caluma_answer_factory,
):
    cantonal_exam_work_item = caluma_work_item_factory(
        task_id="cantonal-exam",
        case=ag_instance.case,
        status=caluma_workflow_models.WorkItem.STATUS_READY,
        addressed_groups=[str(admin_client.user.groups.first().service_id)],
    )
    caluma_answer_factory(
        document=cantonal_exam_work_item.document,
        question_id="kantonale-pruefung-nachtraegliches-baugesuch",
        value="kantonale-pruefung-nachtraegliches-baugesuch-ja",
    )

    request = rf.request()
    request.group = group
    caluma_yes_no_filter = CalumaYesNoFilter(
        question="kantonale-pruefung-nachtraegliches-baugesuch",
        task_id="cantonal-exam",
        yes="ja",
        no="nein",
    )
    parent_mock = mocker.MagicMock()
    parent_mock.request = request
    caluma_yes_no_filter.parent = parent_mock

    queryset = caluma_yes_no_filter.filter(
        queryset=Instance.objects.all(), value=filter
    )

    cases_result = queryset.all()
    assert len(cases_result) == expected
