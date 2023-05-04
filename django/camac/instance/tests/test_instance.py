import datetime
import functools
import json

import pyexcel
import pytest
import pytz
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.urls import reverse
from django.utils.timezone import make_aware
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.core.models import InstanceLocation, WorkflowEntry
from camac.instance import domain_logic, serializers
from camac.instance.models import HistoryEntryT


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
            LazyFixture("admin_user"),
            18,
            1,
            {"instance", "form", "document"},
        ),
        # reader should see instances from other users but has no editables
        ("Reader", LazyFixture("user"), 18, 1, set()),
        ("Canton", LazyFixture("user"), 18, 1, {"form", "document"}),
        ("Municipality", LazyFixture("user"), 17, 1, {"form", "document"}),
        ("Service", LazyFixture("user"), 17, 1, {"form", "document"}),
        ("Public", LazyFixture("user"), 2, 0, {}),
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


@pytest.mark.parametrize(
    "role__name,instance__user", [("Coordination", LazyFixture("user"))]
)
@pytest.mark.parametrize(
    "answer,koor_role,expected_count",
    [
        ("mbv-bund-type-pgv-seilbahn", "camac.constants.kt_uri.ROLE_KOOR_BG", 1),
        ("mbv-bund-type-pgv-eisenbahn", "camac.constants.kt_uri.ROLE_KOOR_BG", 0),
        ("mbv-bund-type-pgv-eisenbahn", "camac.constants.kt_uri.ROLE_KOOR_BD", 1),
        ("mbv-bund-type-pgv-seilbahn", "camac.constants.kt_uri.ROLE_KOOR_BD", 0),
    ],
)
def test_instance_list_for_coordination_ur(
    admin_client,
    ur_instance,
    mocker,
    group,
    group_factory,
    answer,
    question_factory,
    answer_factory,
    koor_role,
    expected_count,
):
    mocker.patch(
        "camac.constants.kt_uri.FORM_MITBERICHT_BUNDESSTELLE", ur_instance.form.pk
    )
    ur_instance.group = group_factory()  # dossier should be created by other group
    ur_instance.save()
    question = question_factory(slug="mbv-bund-type")
    answer_factory(document=ur_instance.case.document, question=question, value=answer)
    mocker.patch(koor_role, group.role.pk)
    url = reverse("instance-list")

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expected_count


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
def test_instance_detail(admin_client, instance):
    url = reverse("instance-detail", args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("instance__identifier", ["00-00-000"])
@pytest.mark.parametrize("form_field__name", ["name"])
@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
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
def test_instance_search_sanctions(
    db,
    application_settings,
    ur_instance,
    sanction_factory,
    instance_factory,
    admin_client,
):
    """Test that instances can be filtered by sanction creator and sanction
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


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
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
        ("Applicant", LazyFixture("admin_user"), False, None, False, 1),
        ("Applicant", LazyFixture("admin_user"), True, None, False, 1),
        ("Applicant", LazyFixture("admin_user"), True, None, True, 0),
        ("Applicant", LazyFixture("admin_user"), True, "test", False, 0),
        ("Applicant", LazyFixture("admin_user"), True, "test", True, 1),
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


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
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
        workflow_date=make_aware(datetime.datetime(2021, 3, 3)),
        instance=instance,
    )

    url = reverse("instance-list")

    response = admin_client.get(url, {field: submit_date})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
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


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
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
        (0, "intent1", "Large house", LazyFixture("instance")),
        (1, "intent2", "Small garden", LazyFixture("instance")),
        (2, "intent3", "Luxury tent", LazyFixture("instance")),
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


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "plot,expected_count",
    [
        ("CH9", 2),
        ("4", 2),
        ("ch967722307039  ", 1),
        (" 420", 1),
        ("7899", 1),
        # Works because of key value concatenation
        ("420 ch967722307039", 1),
        ("420  ch967722307039", 1),
        ("ch9677223070390", 0),
        ("651", 0),
    ],
)
def test_instance_plot_filter(
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
    response = admin_client.get(url, {"plot_sz": plot})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count


@pytest.mark.parametrize(
    "role__name,instance__user",
    [
        ("Municipality", LazyFixture("admin_user")),
        ("Service", LazyFixture("admin_user")),
        ("Applicant", LazyFixture("admin_user")),
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
    answer_factory,
    service_group_factory,
    settings,
    application_settings,
    location_factory,
    role,
    user_factory,
    group_factory,
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

    answer_factory(
        document=inquiry1.child_case.document,
        question_id=caluma_form_models.Question.objects.get(
            pk=sz_distribution_settings.get("QUESTIONS")["ANCILLARY_CLAUSES"]
        ),
        value="Inquiry answer 1",
    )

    answer_factory(
        document=inquiry2.child_case.document,
        question_id=caluma_form_models.Question.objects.get(
            pk=sz_distribution_settings.get("QUESTIONS")["REASON"]
        ),
        value="Inquiry answer 2",
    )

    answer_factory(
        document=inquiry3.child_case.document,
        question_id=caluma_form_models.Question.objects.get(
            pk=sz_distribution_settings.get("QUESTIONS")["REQUEST"]
        ),
        value="Inquiry answer 3",
    )

    url = reverse("instance-list")
    response = admin_client.get(url, data={"keyword_search": value})

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["data"]) == expected_count[role.name]


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize(
    "with_cantonal_participation,expected_count", [(True, 1), (False, 2)]
)
def test_with_cantonal_participation_filter(
    admin_user,
    admin_client,
    ur_instance,
    instance_with_case,
    with_cantonal_participation,
    expected_count,
    workflow_entry_factory,
    instance_factory,
):
    instance_with_case(instance_factory(user=ur_instance.user))
    instance_with_case(instance_factory(user=ur_instance.user))

    workflow_entry_factory(
        instance=ur_instance,
        workflow_date=make_aware(datetime.datetime(2021, 7, 16, 8, 0, 6)),
        group=1,
        workflow_item__pk=16,
    )

    url = reverse("instance-list")
    response = admin_client.get(
        url, data={"with_cantonal_participation": with_cantonal_participation}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == expected_count


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
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


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
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
        (LazyFixture("admin_user"), "001", "1", 1),
        (LazyFixture("admin_user"), "001", "2", 0),
        (LazyFixture("admin_user"), "001", "001", 1),
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
        (LazyFixture("admin_user"), 1),
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
        (LazyFixture("admin_user"), 1),
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
    "role__name,instance__user", [("Municipality", LazyFixture("admin_user"))]
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
    "role__name,instance__user", [("Municipality", LazyFixture("admin_user"))]
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


@pytest.mark.parametrize(
    "instance_state__name,instance__identifier", [("new", "00-00-000")]
)
@pytest.mark.parametrize(
    "role__name,instance__user,status_code",
    [
        # applicant/reader can't update their own Instance,
        # but might update FormField etc.
        ("Applicant", LazyFixture("admin_user"), status.HTTP_400_BAD_REQUEST),
        ("Reader", LazyFixture("user"), status.HTTP_403_FORBIDDEN),
        ("Canton", LazyFixture("user"), status.HTTP_403_FORBIDDEN),
        ("Municipality", LazyFixture("user"), status.HTTP_403_FORBIDDEN),
        ("Service", LazyFixture("user"), status.HTTP_403_FORBIDDEN),
        ("Unknown", LazyFixture("user"), status.HTTP_404_NOT_FOUND),
        ("Coordination", LazyFixture("user"), status.HTTP_404_NOT_FOUND),
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

    data = {
        "data": {
            "type": "instances",
            "id": instance.pk,
            "relationships": {
                "form": {"data": {"type": "forms", "id": form_factory().pk}},
                "location": {
                    "data": {"type": "locations", "id": location_factory().pk}
                },
            },
        }
    }

    response = admin_client.patch(url, data=data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,instance__user,instance_state__name",
    [("Applicant", LazyFixture("admin_user"), "new")],
)
def test_instance_update_location(admin_client, instance, location_factory):
    url = reverse("instance-detail", args=[instance.pk])

    new_location = location_factory()

    data = {
        "data": {
            "type": "instances",
            "id": instance.pk,
            "relationships": {
                "location": {"data": {"type": "locations", "id": new_location.pk}}
            },
        }
    }

    response = admin_client.patch(url, data=data)
    assert response.status_code == status.HTTP_200_OK

    assert InstanceLocation.objects.filter(
        instance=instance, location=new_location
    ).exists()


@pytest.mark.parametrize(
    "role__name,instance__user,instance_state__name,status_code",
    [
        ("Applicant", LazyFixture("admin_user"), "new", status.HTTP_204_NO_CONTENT),
        ("Applicant", LazyFixture("admin_user"), "subm", status.HTTP_403_FORBIDDEN),
        ("Reader", LazyFixture("admin_user"), "new", status.HTTP_204_NO_CONTENT),
        ("Canton", LazyFixture("user"), "new", status.HTTP_403_FORBIDDEN),
        ("Municipality", LazyFixture("user"), "new", status.HTTP_403_FORBIDDEN),
        ("Service", LazyFixture("user"), "new", status.HTTP_403_FORBIDDEN),
        ("Unknown", LazyFixture("user"), "new", status.HTTP_404_NOT_FOUND),
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
    "instance_state__name,instance__location",
    [("new", None), ("new", LazyFixture("location"))],
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

    assert json["data"]["attributes"]["modification-date"] < (
        response.json()["data"]["attributes"]["modification-date"]
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
def test_instance_create_internal_sz(
    db,
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
    [(LazyFixture("admin_user"), "1311", "new")],
)
@pytest.mark.parametrize("attachment__question", ["dokument-parzellen"])
@pytest.mark.parametrize("short_dossier_number", [True, False])
@pytest.mark.parametrize(
    "role__name,instance__location,form__name,status_code",
    [
        ("Applicant", LazyFixture("location"), "baugesuch", status.HTTP_200_OK),
        ("Applicant", LazyFixture("location"), "", status.HTTP_400_BAD_REQUEST),
        ("Applicant", None, "baugesuch", status.HTTP_400_BAD_REQUEST),
        (
            "Applicant",
            LazyFixture(lambda location_factory: location_factory()),
            "baugesuch",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "Applicant",
            LazyFixture("location"),
            "geschaeftskontrolle",
            status.HTTP_200_OK,
        ),
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

    application_settings["NOTIFICATIONS"]["SUBMIT"] = notification_template.slug
    application_settings["WORKFLOW_ITEMS"]["SUBMIT"] = workflow_item.pk
    application_settings["INSTANCE_IDENTIFIER_FORM_ABBR"] = {"vbs": "PV"}
    application_settings["SHORT_DOSSIER_NUMBER"] = short_dossier_number
    application_settings["STORE_PDF"]["SECTION"] = attachment_section.pk

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
    add_field(name="grundeigentumerschaft", value=[{"name": "Bund"}])
    add_field(name="gwr", value=[{"name": "Name", "wohnungen": [{"stockwerk": "1OG"}]}])
    add_field(
        name="punkte", value=[[{"lat": 47.02433179952733, "lng": 8.634144559228435}]]
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

        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        mail.subject == notification_template.subject

        assert WorkflowEntry.objects.filter(
            instance=instance, workflow_item=workflow_item
        ).exists()

        assert case.work_items.filter(task_id="submit", status="completed").exists()


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

    instance_1.instance_state = instance_state_factory(pk=1)
    instance_1.save()

    instance_2.instance_state = instance_state_factory(pk=2)
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

    book = pyexcel.get_book(file_content=response.content, file_type="xlsx")
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
            LazyFixture("admin_user"),
            "baugesuch",
            status.HTTP_200_OK,
            "docx",
        ),
        (
            "Applicant",
            LazyFixture("admin_user"),
            "baugesuch",
            status.HTTP_200_OK,
            "pdf",
        ),
        (
            "Applicant",
            LazyFixture("admin_user"),
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
def test_instance_generate_identifier(
    db,
    instance,
    instance_factory,
    case_factory,
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
        instance.case = case_factory(meta={"dossier-number": identifier})
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


@pytest.mark.freeze_time("2017-7-27")
@pytest.mark.parametrize(
    "role__name,instance__user,publication_entry__publication_date,publication_entry__publication_end_date,publication_entry__is_published,status_code",
    [
        (
            "Municipality",
            LazyFixture("admin_user"),
            datetime.datetime(2016, 6, 28, tzinfo=pytz.UTC),
            datetime.datetime(2016, 7, 10, tzinfo=pytz.UTC),
            True,
            status.HTTP_200_OK,
        ),
        (
            "PublicReader",
            LazyFixture("admin_user"),
            datetime.datetime(2017, 6, 28, tzinfo=pytz.UTC),
            datetime.datetime(2017, 8, 1, tzinfo=pytz.UTC),
            True,
            status.HTTP_200_OK,
        ),
        (
            "Public",
            LazyFixture("admin_user"),
            datetime.datetime(2017, 6, 28, tzinfo=pytz.UTC),
            datetime.datetime(2017, 7, 10, tzinfo=pytz.UTC),
            True,
            status.HTTP_200_OK,
        ),
        (
            "Public",
            LazyFixture("user"),
            datetime.datetime(2016, 6, 28, tzinfo=pytz.UTC),
            datetime.datetime(2017, 7, 10, tzinfo=pytz.UTC),
            True,
            status.HTTP_404_NOT_FOUND,
        ),
        (
            "PublicReader",
            LazyFixture("admin_user"),
            datetime.datetime(2017, 6, 26, tzinfo=pytz.UTC),
            datetime.datetime(2017, 7, 10, tzinfo=pytz.UTC),
            True,
            status.HTTP_404_NOT_FOUND,
        ),
        (
            "PublicReader",
            LazyFixture("admin_user"),
            datetime.datetime(2017, 6, 28, tzinfo=pytz.UTC),
            datetime.datetime(2017, 7, 10, tzinfo=pytz.UTC),
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


@pytest.mark.parametrize(
    "date,status_code",
    [
        ("2017-7-19", status.HTTP_404_NOT_FOUND),
        ("2017-7-20", status.HTTP_200_OK),
        ("2017-7-27", status.HTTP_200_OK),
        ("2017-7-28", status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.parametrize(
    "role__name,instance__user,publication_entry__publication_date,publication_entry__publication_end_date,publication_entry__is_published",
    [
        (
            "PublicReader",
            LazyFixture("admin_user"),
            datetime.datetime(2017, 7, 20, tzinfo=pytz.timezone("Europe/Zurich")),
            datetime.datetime(2017, 7, 27, tzinfo=pytz.timezone("Europe/Zurich")),
            True,
        ),
        (
            "Public",
            LazyFixture("admin_user"),
            datetime.datetime(2017, 7, 20, tzinfo=pytz.timezone("Europe/Zurich")),
            datetime.datetime(2017, 7, 27, tzinfo=pytz.timezone("Europe/Zurich")),
            True,
        ),
    ],
)
def test_instance_detail_publication_timezone(
    admin_client,
    instance,
    publication_entry,
    freezer,
    status_code,
    application_settings,
    date,
):
    application_settings["PUBLICATION_BACKEND"] = "camac-ng"
    url = reverse("instance-detail", args=[instance.pk])

    freezer.move_to(date)

    print("instance:", instance.group.role.name)
    response = admin_client.get(
        url,
        **{"HTTP_X_CAMAC_PUBLIC_ACCESS": True}
        if instance.group.role.name == "Public"
        else {},
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
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
    [("Service", "new", LazyFixture("user"), LazyFixture("service"), 1)],
)
def test_responsible_service_filters(
    admin_client,
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


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
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


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
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


@pytest.mark.parametrize("role__name", ["Coordination"])
@pytest.mark.parametrize("is_creator", [True, False])
@pytest.mark.parametrize("forbidden_states", ["current_state", [9999999]])
def test_instance_list_coordination_created(
    db,
    mocker,
    admin_client,
    instance_state,
    instance,
    is_creator,
    group_factory,
    forbidden_states,
    application_settings,
):
    """Ensure that the coordination role sees their correct dossiers.

    KOOR role can see dossiers which their group has created,
    and which are not in a forbidden state. Note that this is a workaround,
    as the acutal logic in PHP for this rule is rather more complicated,
    but we're not replicating that rule here (yet).
    """
    if forbidden_states == "current_state":
        # unfortunately cannot parametrize this :(
        forbidden_states = [instance_state.name]

    application_settings["INSTANCE_HIDDEN_STATES"] = {"coordination": forbidden_states}

    if not is_creator:
        other_group = group_factory()
        instance.group = other_group
        instance.save()

    url = reverse("instance-list")
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    if is_creator and forbidden_states == [9999999]:
        assert len(json["data"]) == 1
        assert json["data"][0]["id"] == str(instance.pk)
    else:
        assert len(json["data"]) == 0


@pytest.mark.parametrize("role__name", ["Commission"])
@pytest.mark.parametrize("has_assignment", [True, False])
def test_instance_list_commission(db, admin_client, has_assignment, request, instance):
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


@pytest.mark.parametrize("role__name", ["OrganizationReadonly"])
def test_instance_list_organization_readonly(
    db, admin_client, request, instance_factory, location_factory, form_factory, mocker
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


@pytest.mark.parametrize("instance__user", [(LazyFixture("admin_user"))])
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
def test_instance_change_form(
    db,
    mailoutbox,
    admin_client,
    admin_user,
    caluma_admin_user,
    caluma_workflow_config_sz,
    caluma_config_sz,
    application_settings,
    instance,
    instance_service,
    notification_template,
    form_factory,
    instance_state_factory,
    role,
    current_form_slug,
    new_form_slug,
    expected_status,
    starting_instance_state,
):
    notification = {
        "template_slug": notification_template.slug,
        "recipient_types": ["applicant"],
    }
    application_settings["CALUMA"]["SIMPLE_WORKFLOW"]["reject-form"][
        "notification"
    ] = notification
    application_settings["INTERCHANGEABLE_FORMS"] = [
        "vorentscheid-gemass-ss84-pbg-v2",
        "baugesuch-reklamegesuch-v2",
        "projektanderung-v2",
        "technische-bewilligung",
        "technische-bewilligung-v2",
        "baumeldung-fur-geringfugiges-vorhaben-v2",
        "baumeldung-fur-geringfugiges-vorhaben-v3",
        "baumeldung-fur-geringfugiges-vorhaben-v4",
        "anlassbewilligungen-verkehrsbewilligungen-v2",
        "anlassbewilligungen-verkehrsbewilligungen-v3",
        "projektgenehmigungsgesuch-gemass-ss15-strag-v2",
        "projektgenehmigungsgesuch-gemass-ss15-strag-v3",
    ]

    caluma_form, _ = caluma_form_models.Form.objects.get_or_create(pk="baugesuch")
    workflow = caluma_workflow_models.Workflow.objects.get(pk="building-permit")

    case = workflow_api.start_case(
        workflow=workflow,
        form=caluma_form,
        user=caluma_admin_user,
    )
    instance.case = case
    instance.save()
    work_item = caluma_workflow_models.WorkItem.objects.get(task_id="submit")
    workflow_api.complete_work_item(
        work_item=work_item,
        user=caluma_admin_user,
    )

    finished_instance_state = instance_state_factory(name="rejected")
    current_form = form_factory(name=current_form_slug)
    form_factory(name=new_form_slug)

    instance.instance_state = instance_state_factory(name=starting_instance_state)
    instance.form = current_form
    instance.save()

    response = admin_client.post(
        reverse("instance-change-form", args=[instance.pk]),
        {
            "data": {
                "type": "instance-change-forms",
                "attributes": {"form": new_form_slug},
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        instance.refresh_from_db()

        assert instance.form.name == new_form_slug
        assert len(mailoutbox) == 1
        assert instance.instance_state == finished_instance_state
        assert HistoryEntryT.objects.filter(
            history_entry__instance=instance,
            language="de",
        ).exists()
        assert caluma_workflow_models.WorkItem.objects.filter(
            task_id="formal-addition"
        ).exists()
