import pytest
from alexandria.core.factories import CategoryFactory
from django.urls import reverse
from rest_framework import status

from camac.alexandria.extensions.permissions.extension import MODE_CREATE
from camac.conftest import reload_urlconf
from camac.permissions.conditions import Always, IsPaper, Never


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "instance_state__name,has_create_permission", [("new", True), ("other", False)]
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


def test_category_permission_view_without_instance(admin_client):
    response = admin_client.get(
        reverse("category-permissions", args=[CategoryFactory().pk]),
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[0]["detail"] == "'instance' query parameter must be passed"


@pytest.mark.parametrize("by", ["category", "access_level"])
def test_alexandria_permissions_debugger_view(
    db,
    access_level_factory,
    alexandria_category_factory,
    alexandria_mark_factory,
    by,
    client,
    settings,
    snapshot,
):
    settings.DEBUG = True
    reload_urlconf("camac.urls")

    access_level_factory(pk="level-1", name="Level 1")
    access_level_factory(pk="level-2", name="Level 2")
    alexandria_category_factory(pk="category-1", name="Category 1")
    alexandria_category_factory(pk="category-2", name="Category 2")
    alexandria_mark_factory(pk="mark-1")
    alexandria_mark_factory(pk="mark-2")

    settings.PERMISSIONS_ALEXANDRIA["ACCESS_LEVELS"] = {
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
