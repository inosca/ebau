import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.instance import models


@pytest.mark.parametrize(
    "role__name,instance__user,size",
    [
        ("Applicant", LazyFixture("admin_user"), 1),
        ("Unknown", LazyFixture("user"), 0),
        ("Support", LazyFixture("user"), 1),
        ("Service", LazyFixture("user"), 1),
        ("Public", LazyFixture("user"), 0),
        ("Municipality", LazyFixture("user"), 1),
    ],
)
@pytest.mark.parametrize("form_field__name", ["kategorie-des-vorhabens"])
def test_form_field_list(admin_client, form_field, size):
    url = reverse("form-field-list")

    if admin_client.user.groups.filter(role__name="Public"):
        response = admin_client.get(url, HTTP_X_CAMAC_PUBLIC_ACCESS=True)
    else:
        response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size
    if size > 0:
        assert json["data"][0]["id"] == str(form_field.pk)


@pytest.mark.parametrize(
    "role__name,instance__user,size",
    [
        (
            "Applicant",
            LazyFixture("admin_user"),
            {"einsprecher": 0, "kategorie-des-vorhabens": 1},
        ),
        (
            "Unknown",
            LazyFixture("user"),
            {"einsprecher": 0, "kategorie-des-vorhabens": 1},
        ),
        (
            "Support",
            LazyFixture("user"),
            {"einsprecher": 0, "kategorie-des-vorhabens": 1},
        ),
        (
            "Service",
            LazyFixture("user"),
            {"einsprecher": 0, "kategorie-des-vorhabens": 1},
        ),
        (
            "Public",
            LazyFixture("user"),
            {"einsprecher": 0, "kategorie-des-vorhabens": 1},
        ),
        (
            "Municipality",
            LazyFixture("user"),
            {"einsprecher": 1, "kategorie-des-vorhabens": 1},
        ),
    ],
)
@pytest.mark.parametrize(
    "form_field__name", [("einsprecher"), ("kategorie-des-vorhabens")]
)
def test_form_field_visible_for(
    admin_client, request, form_field, group, size, settings
):
    request.group = group

    form_fields = (
        models.FormField.objects.get_queryset()
        .visible_for(request)
        .values_list("pk", flat=True)
    )

    assert len(form_fields) == size[form_field.name]
    if size[form_field.name] > 0:
        assert form_fields[0] == form_field.pk


@pytest.mark.parametrize(
    "role__name,instance__user",
    [("Applicant", LazyFixture("admin_user")), ("Reader", LazyFixture("admin_user"))],
)
@pytest.mark.parametrize("form_field__value", [["Test1", "Test2"]])
@pytest.mark.parametrize("form_field__name", ["kategorie-des-vorhabens"])
def test_form_field_detail(admin_client, form_field, form_field__value):
    url = reverse("form-field-detail", args=[form_field.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert response.json()["data"]["attributes"]["value"] == form_field__value


@pytest.mark.parametrize(
    "role__name,instance_state__name,instance__user,form_field__name,status_code",
    [
        (
            "Applicant",
            "new",
            LazyFixture("admin_user"),
            "kategorie-des-vorhabens",
            status.HTTP_200_OK,
        ),
        (
            "Applicant",
            "new",
            LazyFixture("admin_user"),
            "unknown-question",
            status.HTTP_404_NOT_FOUND,
        ),
        (
            "Applicant",
            "new",
            LazyFixture("user"),
            "kategorie-des-vorhabens",
            status.HTTP_404_NOT_FOUND,
        ),
        (
            "Applicant",
            "comm",
            LazyFixture("admin_user"),
            "kategorie-des-vorhabens",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "Reader",
            "new",
            LazyFixture("user"),
            "kategorie-des-vorhabens",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "Reader",
            "new",
            LazyFixture("admin_user"),
            "kategorie-des-vorhabens",
            status.HTTP_403_FORBIDDEN,
        ),
    ],
)
def test_form_field_update(admin_client, form_field, status_code):
    url = reverse("form-field-detail", args=[form_field.pk])

    data = {
        "data": {
            "type": "form-fields",
            "id": form_field.pk,
            "attributes": {
                "name": form_field.name,
                "value": {"test-name": "test-value"},
            },
            "relationships": {
                "instance": {
                    "data": {"type": "instances", "id": form_field.instance.pk}
                }
            },
        }
    }

    response = admin_client.patch(url, data=data)
    assert response.status_code == status_code


@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize(
    "role__name,instance__user,form_field_name,status_code",
    [
        (
            "Applicant",
            LazyFixture("admin_user"),
            "kategorie-des-vorhabens",
            status.HTTP_201_CREATED,
        ),
        (
            "Applicant",
            LazyFixture("admin_user"),
            "einsprecher",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "Applicant",
            LazyFixture("admin_user"),
            "unknown-question",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "Applicant",
            LazyFixture("user"),
            "kategorie-des-vorhabens",
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
def test_form_field_create(admin_client, instance, form_field_name, status_code):
    url = reverse("form-field-list")

    data = {
        "data": {
            "type": "form-fields",
            "id": None,
            "attributes": {
                "name": form_field_name,
                "value": {"test-name": "test-value"},
            },
            "relationships": {
                "instance": {"data": {"type": "instances", "id": instance.pk}}
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        json = response.json()

        field = models.FormField.objects.get(pk=json["data"]["id"])
        assert (
            field.value == json["data"]["attributes"]["value"]
        ), "json value on database is not equal to what is stored in database"


@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize(
    "role__name,instance__user,status_code",
    [
        ("Applicant", LazyFixture("admin_user"), status.HTTP_403_FORBIDDEN),
        ("Canton", LazyFixture("user"), status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.parametrize("form_field__name", ["kategorie-des-vorhabens"])
def test_form_field_destroy(admin_client, form_field, status_code):
    url = reverse("form-field-detail", args=[form_field.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,egrid_query,size,instance_ids",
    [
        ("Applicant", ["CH892277844039"], 1, (2,)),
        ("Applicant", ["CH674077422224", "CH892277844039"], 2, (1, 2)),
    ],
)
def test_form_field_list_filtering(
    admin_client,
    admin_user,
    instance_factory,
    form_field_factory,
    egrid_query,
    size,
    instance_ids,
):

    instance = instance_factory(pk=1, user=admin_user)
    form_field_factory(
        instance=instance,
        name="parzellen",
        value=[
            {"egrid": "CH674077422224", "number": 1101, "municipality": "Muotathal"}
        ],
    )

    instance = instance_factory(pk=2, user=admin_user)
    form_field_factory(
        instance=instance,
        name="parzellen",
        value=[
            {"egrid": "CH674077422224", "number": 1101, "municipality": "Muotathal"},
            {"egrid": "CH892277844039", "number": 2446, "municipality": "Schwyz"},
            {"egrid": "CH_DUMMY_EGRID", "number": 1234, "municipality": "Neverland"},
        ],
    )

    url = reverse("form-field-list")
    response = admin_client.get(url, data={"egrid": ",".join(egrid_query)})

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size

    instances_from_json = set(
        int(entry["relationships"]["instance"]["data"]["id"]) for entry in json["data"]
    )
    assert set(instance_ids) == instances_from_json


@pytest.mark.parametrize(
    "role__name,instance_state__name,instance__user",
    [("Applicant", "new", LazyFixture("admin_user"))],
)
@pytest.mark.parametrize(
    "has_existing,old_value,new_value,has_history_entry",
    [
        (False, None, "New", True),
        (False, None, "", False),
        (True, "", "", False),
        (True, "", "New", True),
        (True, "Old", "", True),
        (True, "Old", "New", True),
        (True, "Old", "Old", False),
    ],
)
def test_form_field_side_effect_history_entry(
    admin_client,
    instance,
    form_field_factory,
    application_settings,
    has_existing,
    old_value,
    new_value,
    has_history_entry,
):
    form_field_name = "kategorie-des-vorhabens"

    application_settings["FORM_FIELD_HISTORY_ENTRY"] = (
        {"name": form_field_name, "title": "Test"},
    )

    data = {
        "data": {
            "type": "form-fields",
            "id": None,
            "attributes": {
                "name": form_field_name,
                "value": new_value,
            },
            "relationships": {
                "instance": {"data": {"type": "instances", "id": instance.pk}}
            },
        }
    }

    if has_existing:
        form_field = form_field_factory(
            name=form_field_name, value=old_value, instance=instance
        )

        data["data"]["id"] = form_field.pk

        response = admin_client.patch(
            reverse("form-field-detail", args=[form_field.pk]), data=data
        )

        assert response.status_code == status.HTTP_200_OK
    else:
        response = admin_client.post(reverse("form-field-list"), data=data)

        assert response.status_code == status.HTTP_201_CREATED

    assert instance.history.exists() == has_history_entry

    if has_history_entry:
        assert (
            instance.history.first().title
            == application_settings["FORM_FIELD_HISTORY_ENTRY"][0]["title"]
        )
