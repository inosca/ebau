import datetime
import functools

import pyexcel
import pytest
import pytz
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.core.models import InstanceLocation, WorkflowEntry
from camac.instance import serializers


@pytest.fixture(params=["user", "involved_applicants__invitee"])
def instance_user_field(settings, request):
    old_user_field = settings.APPLICATION["INSTANCE_USER_FIELD"]
    settings.APPLICATION["INSTANCE_USER_FIELD"] = request.param
    yield
    settings.APPLICATION["INSTANCE_USER_FIELD"] = old_user_field


@pytest.mark.parametrize(
    "instance_state__name,instance__creation_date,applicant__user,applicant__invitee",
    [
        (
            "new",
            "2018-04-17T09:31:56+02:00",
            LazyFixture("admin_user"),
            LazyFixture("admin_user"),
        )
    ],
)
@pytest.mark.parametrize(
    "role__name,instance__user,num_queries,editable",
    [
        ("Applicant", LazyFixture("admin_user"), 9, {"instance", "form", "document"}),
        # reader should see instances from other users but has no editables
        ("Reader", LazyFixture("user"), 9, set()),
        ("Canton", LazyFixture("user"), 9, {"form", "document"}),
        ("Municipality", LazyFixture("user"), 9, {"form", "document"}),
        ("Service", LazyFixture("user"), 9, {"document"}),
    ],
)
def test_instance_list(
    admin_client,
    instance,
    activation,
    num_queries,
    group,
    django_assert_num_queries,
    editable,
    group_location_factory,
    applicant,
    instance_user_field,
):
    url = reverse("instance-list")

    # verify that two locations may be assigned to group
    group_location_factory(group=group)

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
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(instance.pk)
    assert set(json["data"][0]["meta"]["editable"]) == set(editable)
    # included previous_instance_state and instance_state are the same
    assert len(json["included"]) == len(included) - 1


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
        ("Service", LazyFixture("user"), status.HTTP_404_NOT_FOUND),
        ("Unknown", LazyFixture("user"), status.HTTP_404_NOT_FOUND),
    ],
)
def test_instance_update(
    admin_client, instance, location_factory, form_factory, status_code
):
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


@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize(
    "role__name,instance__user,status_code",
    [
        ("Applicant", LazyFixture("admin_user"), status.HTTP_204_NO_CONTENT),
        ("Reader", LazyFixture("admin_user"), status.HTTP_204_NO_CONTENT),
        ("Canton", LazyFixture("user"), status.HTTP_403_FORBIDDEN),
        ("Municipality", LazyFixture("user"), status.HTTP_403_FORBIDDEN),
        ("Service", LazyFixture("user"), status.HTTP_404_NOT_FOUND),
        ("Unknown", LazyFixture("user"), status.HTTP_404_NOT_FOUND),
    ],
)
def test_instance_destroy(admin_client, instance, status_code, location_factory):
    url = reverse("instance-detail", args=[instance.pk])

    """
    Add InstanceLocation relationship to make sure it also will be deleted
    when the instance is deleted (cascade deletion).
    """
    instance_location = InstanceLocation.objects.create(
        location=location_factory(), instance=instance
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
def test_instance_create(admin_client, admin_user, form, instance_state, instance):
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
        ("Applicant", LazyFixture("location"), "", status.HTTP_400_BAD_REQUEST),
        ("Applicant", None, "baugesuch", status.HTTP_400_BAD_REQUEST),
        (
            "Applicant",
            LazyFixture(lambda location_factory: location_factory()),
            "baugesuch",
            status.HTTP_400_BAD_REQUEST,
        ),
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
    settings,
    group_location_factory,
    attachment,
    workflow_item,
    notification_template,
    mailoutbox,
):

    settings.APPLICATION["SUBMIT"]["NOTIFICATION_TEMPLATE"] = notification_template.pk
    settings.APPLICATION["SUBMIT"]["WORKFLOW_ITEM"] = workflow_item.pk

    # only create group in a successful run
    if status_code == status.HTTP_200_OK:
        role = role_factory(name="Municipality")
        group = group_factory(role=role)
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

    response = admin_client.post(url)
    assert response.status_code == status_code, response.content

    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert json["data"]["attributes"]["identifier"] == "11-17-001"
        assert set(json["data"]["meta"]["editable"]) == set()

        instance.refresh_from_db()
        assert instance.instance_state.name == "subm"

        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        mail.subject == notification_template.subject

        assert WorkflowEntry.objects.filter(
            instance=instance, workflow_item=workflow_item
        ).exists()


@pytest.mark.parametrize("role__name", ["Canton"])
def test_instance_export(
    admin_client, user, instance_factory, django_assert_num_queries, form_field_factory
):
    url = reverse("instance-export")
    instances = instance_factory.create_batch(2, user=user)
    instance = instances[0]

    add_field = functools.partial(form_field_factory, instance=instance)
    add_field(
        name="projektverfasser-planer",
        value=[{"name": "Muster Hans"}, {"name": "Beispiel Jean"}],
    )
    add_field(name="bezeichnung", value="Bezeichnung")

    with django_assert_num_queries(2):
        response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    book = pyexcel.get_book(file_content=response.content, file_type="xlsx")
    # bookdict is a dict of tuples(name, content)
    sheet = book.bookdict.popitem()[1]
    assert len(sheet) == len(instances)
    row = sheet[0]
    assert row[4] == "Muster Hans, Beispiel Jean"
    assert row[5] == "Bezeichnung"


@pytest.mark.freeze_time("2017-7-27")
@pytest.mark.parametrize("location__communal_federal_number", ["1311"])
def test_instance_generate_identifier(db, instance, instance_factory):
    instance_factory(identifier="11-17-010")
    serializer = serializers.InstanceSubmitSerializer(instance)
    identifier = serializer.generate_identifier()

    assert identifier == "11-17-011"


@pytest.mark.freeze_time("2017-7-27")
@pytest.mark.parametrize(
    "role__name,instance__user,publication_entry__publication_date,publication_entry__is_published,status_code",
    [
        (
            "Municipality",
            LazyFixture("admin_user"),
            datetime.datetime(2016, 6, 28, tzinfo=pytz.UTC),
            True,
            status.HTTP_200_OK,
        ),
        (
            "PublicReader",
            LazyFixture("admin_user"),
            datetime.datetime(2017, 6, 28, tzinfo=pytz.UTC),
            True,
            status.HTTP_200_OK,
        ),
        (
            "PublicReader",
            LazyFixture("admin_user"),
            datetime.datetime(2017, 6, 26, tzinfo=pytz.UTC),
            True,
            status.HTTP_404_NOT_FOUND,
        ),
        (
            "PublicReader",
            LazyFixture("admin_user"),
            datetime.datetime(2017, 6, 28, tzinfo=pytz.UTC),
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
