import pytest
from alexandria.core.factories import CategoryFactory
from django.urls import reverse
from rest_framework import status

from camac.alexandria.extensions.permissions.extension import MODE_CREATE
from camac.conftest import reload_urlconf
from camac.permissions.api import GRANT_CHOICES, grant
from camac.permissions.conditions import Always, IsPaper, Never, RequireInstanceState
from camac.permissions.switcher import PERMISSION_MODE


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    ("instance_state__name", "has_create_permission"), [("new", True), ("other", False)]
)
def test_category_permission_view(admin_client, instance, has_create_permission):
    category = CategoryFactory(
        metainfo={
            "access": {
                "Municipality": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "condition": {
                                "InstanceState": "new",
                            },
                        },
                    ],
                },
            }
        }
    )

    response = admin_client.get(
        reverse("category-permissions", args=[category.pk]),
        data={"instance": instance.pk},
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert (MODE_CREATE in response.json()) == has_create_permission


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    ("instance_state__name", "has_create_permission"), [("new", True), ("other", False)]
)
def test_category_permission_view_v2(
    admin_client,
    instance,
    service,
    access_level_factory,
    has_create_permission,
    alexandria_settings,
    permissions_alexandria_settings,
    permissions_settings,
):
    alexandria_settings["USE_V2_PERMISSIONS"] = True
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL

    access_level = access_level_factory()
    grant(
        instance,
        grant_type=GRANT_CHOICES.SERVICE.value,
        access_level=access_level,
        service=service,
    )
    category = CategoryFactory(
        metainfo={
            "access": {
                "Municipality": {"visibility": "all"},
            }
        }
    )
    permissions_alexandria_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            (f"{category.pk}:create", RequireInstanceState("new")),
        ]
    }

    response = admin_client.get(
        reverse("category-permissions", args=[category.pk]),
        data={"instance": instance.pk},
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert (MODE_CREATE in response.json()) == has_create_permission


def test_category_permission_view_without_instance(admin_client):
    response = admin_client.get(
        reverse("category-permissions", args=[CategoryFactory().pk]),
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[0]["detail"] == "'instance' query parameter must be passed"


@pytest.mark.parametrize("by", ["category", "access_level"])
@pytest.mark.django_db
def test_alexandria_permissions_debugger_view(
    access_level_factory,
    alexandria_category_factory,
    alexandria_mark_factory,
    by,
    client,
    settings,
    snapshot,
    permissions_alexandria_settings,
    reload_urlconf_after,
):
    settings.DEBUG = True
    reload_urlconf("camac.urls")

    access_level_factory(pk="level-1", name="Level 1")
    access_level_factory(pk="level-2", name="Level 2")
    alexandria_category_factory(pk="category-1", name="Category 1", sort=1)
    alexandria_category_factory(pk="category-2", name="Category 2", sort=2)
    alexandria_mark_factory(pk="mark-1")
    alexandria_mark_factory(pk="mark-2")

    permissions_alexandria_settings["ACCESS_LEVELS"] = {
        "level-1": [
            ("category-1:create", Always()),
            ("category-1:delete", Never()),
            ("category-1:update", IsPaper()),
            ("category-1:update", IsPaper()),
            ("category-1:mark:mark-1", Always()),
        ],
        "level-2": [
            ("category-1:mark:all", Always()),
            ("category-2:all", Always()),
        ],
    }

    response = client.get(reverse("alexandria-permissions-debugger"), data={"by": by})

    assert response.status_code == status.HTTP_200_OK
    assert response.text == snapshot


@pytest.mark.parametrize("by", ["category", "role"])
@pytest.mark.django_db
def test_alexandria_visibilities_debugger_view(
    access_level_factory,
    alexandria_category_factory,
    alexandria_mark_factory,
    service_group_factory,
    role_factory,
    by,
    client,
    settings,
    alexandria_settings,
    snapshot,
):
    settings.DEBUG = True
    reload_urlconf("camac.urls")

    role_factory(slug="role-1", name="Role 1")
    role_factory(slug="role-2", name="Role 2")
    service_group_factory(slug="authority-bab", name="Authority BAB")
    alexandria_settings["PERMISSION_KEY"] = {
        "SERVICE_GROUP_MAPPING": {"authority-bab": "are"}
    }

    alexandria_category_factory(
        pk="category-1",
        name="Category 1",
        sort=1,
        metainfo={
            "access": {
                "role-1": {
                    "visibility": "all",
                },
                "role-2": {
                    "visibility": "none",
                },
                "are": {
                    "visibility": "service",
                },
            }
        },
    )
    alexandria_category_factory(
        pk="category-2",
        name="Category 2",
        sort=2,
        metainfo={
            "access": {
                "role-1": {
                    "visibility": "all",
                },
                "role-2": {
                    "visibility": "none",
                },
            }
        },
    )

    response = client.get(reverse("alexandria-visibilities-debugger"), data={"by": by})

    assert response.status_code == status.HTTP_200_OK
    assert response.text == snapshot
