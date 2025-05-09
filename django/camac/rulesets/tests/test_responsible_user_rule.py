import pytest
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.rulesets.models import ResponsibleUserRule
from camac.user.models import Service


@pytest.fixture
def valid_municipality(service_factory):
    return service_factory(service_group__name="municipality")


@pytest.fixture
def invalid_municipality(service_factory):
    return service_factory()


@pytest.fixture
def valid_application_type(caluma_form_factory):
    return caluma_form_factory(is_published=True, meta={"is-main-form": True})


@pytest.fixture
def invalid_application_type(caluma_form_factory):
    return caluma_form_factory()


@pytest.fixture
def valid_user(service, user_group_factory, user):
    user_group_factory(group__service=service, user=user)

    return user


@pytest.fixture
def invalid_user(user_factory):
    return user_factory()


@pytest.mark.parametrize(
    "application_type,municipality,expected_user",
    [
        ("form1", "municipality1", "user1"),
        ("form2", "municipality1", "user2"),
        ("form2", "municipality2", "user2"),
        ("form2", "municipality3", "user3"),
        ("form2", "municipality4", None),
    ],
)
def test_responsible_user_for_instance(
    db,
    ag_instance,
    ag_master_data_settings,
    application_type,
    caluma_form_factory,
    expected_user,
    municipality,
    responsible_user_rule_factory,
    service_factory,
    service,
    user_factory,
    utils,
):
    form1 = caluma_form_factory(pk="form1")
    caluma_form_factory(pk="form2")
    caluma_form_factory(pk="form3")

    municipality1 = service_factory(name="municipality1")
    municipality2 = service_factory(name="municipality2")
    municipality3 = service_factory(name="municipality3")
    service_factory(name="municipality4")
    user1 = user_factory(username="user1")
    user2 = user_factory(username="user2")
    user3 = user_factory(username="user3")

    type_rule = responsible_user_rule_factory(
        service=service, responsible_user=user1, sort=0
    )
    type_rule.application_types.set([form1])

    municipality_rule_1 = responsible_user_rule_factory(
        service=service, responsible_user=user2, sort=1
    )
    municipality_rule_1.municipalities.set([municipality1, municipality2])

    municipality_rule_2 = responsible_user_rule_factory(
        service=service, responsible_user=user3, sort=2
    )
    municipality_rule_2.municipalities.set([municipality3])

    ag_instance.case.document.form_id = application_type
    ag_instance.case.document.save()

    utils.add_municipality(
        ag_instance.case.document,
        "gemeinde",
        Service.objects.get(name=municipality),
    )

    result = ResponsibleUserRule.objects.get_responsible_user_for_instance(
        ag_instance,
        service,
    )

    if expected_user is None:
        assert result is None
    else:
        assert result.username == expected_user


@pytest.mark.parametrize(
    "role__name,expected_count",
    [
        ("municipality-clerk", 0),
        ("municipality-admin", 3),
    ],
)
def test_responsible_user_rule_list(
    db,
    admin_client,
    ag_rulesets_settings,
    expected_count,
    responsible_user_rule_factory,
    service_factory,
    service,
):
    responsible_user_rule_factory.create_batch(5, service=service_factory())
    visible = responsible_user_rule_factory.create_batch(3, service=service)

    response = admin_client.get(reverse("responsible-user-rule-list"))

    assert response.status_code == status.HTTP_200_OK

    result = response.json()["data"]
    assert len(result) == expected_count

    if expected_count > 0:
        assert set([entry.pk for entry in visible]) == set(
            [int(entry["id"]) for entry in result]
        )


@pytest.mark.parametrize(
    "role__name,municipalities,application_types,responsible_user,expected_status",
    [
        (
            "municipality-admin",
            [lf("valid_municipality")],
            [],
            lf("valid_user"),
            status.HTTP_201_CREATED,
        ),
        (
            "municipality-admin",
            [],
            [lf("valid_application_type")],
            lf("valid_user"),
            status.HTTP_201_CREATED,
        ),
        # Forbidden role
        (
            "municipality-clerk",
            [],
            [lf("valid_application_type")],
            lf("valid_user"),
            status.HTTP_403_FORBIDDEN,
        ),
        # Invalid values
        (
            "municipality-admin",
            [lf("invalid_municipality")],
            [],
            lf("valid_user"),
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "municipality-admin",
            [],
            [lf("invalid_application_type")],
            lf("valid_user"),
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "municipality-admin",
            [],
            [lf("valid_application_type")],
            lf("invalid_user"),
            status.HTTP_400_BAD_REQUEST,
        ),
        # Both empty
        ("municipality-admin", [], [], lf("valid_user"), status.HTTP_400_BAD_REQUEST),
        # Both set
        (
            "municipality-admin",
            [lf("valid_municipality")],
            [lf("valid_application_type")],
            lf("valid_user"),
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
def test_responsible_user_rule_create(
    db,
    admin_client,
    ag_rulesets_settings,
    application_types,
    expected_status,
    municipalities,
    responsible_user,
    responsible_user_rule_factory,
    service,
):
    responsible_user_rule_factory(sort=99, service=service)

    response = admin_client.post(
        reverse("responsible-user-rule-list"),
        data={
            "data": {
                "type": "responsible-user-rules",
                "relationships": {
                    "responsible-user": {
                        "data": {
                            "id": responsible_user.pk,
                            "type": "users",
                        }
                    },
                    "application-types": {
                        "data": [
                            {
                                "id": i.pk,
                                "type": "application-types",
                            }
                            for i in application_types
                        ]
                    },
                    "municipalities": {
                        "data": [
                            {
                                "id": i.pk,
                                "type": "public-services",
                            }
                            for i in municipalities
                        ]
                    },
                },
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        new_rule = ResponsibleUserRule.objects.get(pk=response.json()["data"]["id"])

        assert new_rule.service == service
        assert new_rule.sort == 100


@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        ("municipality-admin", status.HTTP_200_OK),
        ("municipality-clerk", status.HTTP_404_NOT_FOUND),
    ],
)
def test_responsible_user_rule_update(
    db,
    admin_client,
    ag_rulesets_settings,
    expected_status,
    responsible_user_rule_factory,
    service_factory,
    service,
    user_factory,
    user_group_factory,
    user,
):
    responsible_user_rule = responsible_user_rule_factory(
        responsible_user=user,
        service=service,
    )
    responsible_user_rule.municipalities.add(
        service_factory(service_group__name="municipalities")
    )

    new_user = user_factory()
    user_group_factory(group__service=service, user=new_user)

    response = admin_client.patch(
        reverse("responsible-user-rule-detail", args=[responsible_user_rule.pk]),
        data={
            "data": {
                "id": responsible_user_rule.pk,
                "type": "responsible-user-rules",
                "attributes": {"sort": 9999},
                "relationships": {
                    "responsible-user": {
                        "data": {
                            "id": new_user.pk,
                            "type": "users",
                        }
                    },
                },
            }
        },
    )

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_200_OK:
        responsible_user_rule.refresh_from_db()
        assert responsible_user_rule.responsible_user == new_user
        assert responsible_user_rule.sort != 9999


@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        ("municipality-admin", status.HTTP_204_NO_CONTENT),
        ("municipality-clerk", status.HTTP_404_NOT_FOUND),
    ],
)
def test_responsible_user_rule_destroy(
    db,
    admin_client,
    ag_rulesets_settings,
    expected_status,
    responsible_user_rule_factory,
    service,
):
    responsible_user_rule_factory(sort=0, service=service)
    responsible_user_rule = responsible_user_rule_factory(sort=1, service=service)
    responsible_user_rule_factory(sort=2, service=service)

    response = admin_client.delete(
        reverse("responsible-user-rule-detail", args=[responsible_user_rule.pk])
    )

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_204_NO_CONTENT:
        with pytest.raises(ResponsibleUserRule.DoesNotExist):
            responsible_user_rule.refresh_from_db()

        # Existing rules were reordered
        assert list(
            ResponsibleUserRule.objects.filter(service=service).values_list(
                "sort", flat=True
            )
        ) == [0, 1]


@pytest.mark.parametrize(
    "role__name,new_order,expected_status",
    [
        ("municipality-admin", [2, 0, 1], status.HTTP_204_NO_CONTENT),
        ("municipality-admin", [1, 2, 0], status.HTTP_204_NO_CONTENT),
        ("municipality-admin", [0, 1], status.HTTP_400_BAD_REQUEST),
        ("municipality-admin", [0, 1, 2, "99"], status.HTTP_400_BAD_REQUEST),
        ("municipality-clerk", [2, 0, 1], status.HTTP_403_FORBIDDEN),
    ],
)
def test_responsible_user_rule_reorder(
    db,
    admin_client,
    ag_rulesets_settings,
    expected_status,
    new_order,
    responsible_user_rule_factory,
    service,
):
    rules = [
        responsible_user_rule_factory(sort=sort, service=service)
        for sort in range(0, 3)
    ]

    response = admin_client.post(
        reverse("responsible-user-rule-reorder"),
        data={
            "data": {
                "type": "responsible-user-rule-reorders",
                "attributes": {
                    "order": [
                        rules[i].pk if isinstance(i, int) else int(i) for i in new_order
                    ]
                },
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        for expected_sort, i in enumerate(new_order):
            rule = rules[i]
            rule.refresh_from_db()

            assert rule.sort == expected_sort
