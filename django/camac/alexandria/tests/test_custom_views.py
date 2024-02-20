import pytest
from alexandria.core.factories import CategoryFactory
from django.urls import reverse
from rest_framework import status

from camac.alexandria.extensions.permissions.extension import MODE_CREATE


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
