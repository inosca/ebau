import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

FULL_PERMISSIONS = {
    "main": ["read", "write", "write-meta"],
    "sb1": ["read", "write", "write-meta"],
    "sb2": ["read", "write", "write-meta"],
}


@pytest.mark.parametrize(
    "role__name,instance__user,instance_state__name,expected_permissions",
    [
        (
            "Applicant",
            LazyFixture("admin_user"),
            "new",
            {
                "main": [
                    "read",
                    "write",
                    "write-meta",  # write-meta camac-instance-id, submit-date
                ],
                "sb1": [],
                "sb2": [],
            },
        ),
        (
            "Applicant",
            LazyFixture("admin_user"),
            "subm",
            {"main": ["read"], "sb1": [], "sb2": []},
        ),
        (
            "Applicant",
            LazyFixture("admin_user"),
            "correction",
            {"main": ["read"], "sb1": [], "sb2": []},
        ),
        (
            "Applicant",
            LazyFixture("admin_user"),
            "rejected",
            {
                "main": ["read", "write", "write-meta"],  # write-meta: submit-date
                "sb1": [],
                "sb2": [],
            },
        ),
        (
            "Applicant",
            LazyFixture("admin_user"),
            "sb1",
            {
                "main": ["read"],
                "sb1": ["read", "write", "write-meta"],  # write-meta: submit-date
                "sb2": [],
            },
        ),
        (
            "Applicant",
            LazyFixture("admin_user"),
            "sb2",
            {
                "main": ["read"],
                "sb1": ["read"],
                "sb2": ["read", "write", "write-meta"],  # write-meta: submit-date
            },
        ),
        (
            "Applicant",
            LazyFixture("admin_user"),
            "conclusion",
            {"main": ["read"], "sb1": ["read"], "sb2": ["read"]},
        ),
        (
            "Service",
            LazyFixture("admin_user"),
            "new",
            {"main": [], "sb1": [], "sb2": []},
        ),
        (
            "Service",
            LazyFixture("admin_user"),
            "subm",
            {"main": ["read"], "sb1": [], "sb2": []},
        ),
        (
            "Service",
            LazyFixture("admin_user"),
            "correction",
            {"main": ["read"], "sb1": [], "sb2": []},
        ),
        (
            "Service",
            LazyFixture("admin_user"),
            "rejected",
            {"main": ["read"], "sb1": [], "sb2": []},
        ),
        (
            "Service",
            LazyFixture("admin_user"),
            "sb1",
            {"main": ["read"], "sb1": [], "sb2": []},
        ),
        (
            "Service",
            LazyFixture("admin_user"),
            "sb2",
            {"main": ["read"], "sb1": ["read"], "sb2": []},
        ),
        (
            "Service",
            LazyFixture("admin_user"),
            "conclusion",
            {"main": ["read"], "sb1": ["read"], "sb2": ["read"]},
        ),
        (
            "Municipality",
            LazyFixture("admin_user"),
            "new",
            {"main": [], "sb1": [], "sb2": []},
        ),
        (
            "Municipality",
            LazyFixture("admin_user"),
            "subm",
            {
                "main": ["read", "write-meta"],  # write-meta: ebau-number
                "sb1": [],
                "sb2": [],
            },
        ),
        (
            "Municipality",
            LazyFixture("admin_user"),
            "correction",
            {"main": ["read", "write"], "sb1": [], "sb2": []},
        ),
        (
            "Municipality",
            LazyFixture("admin_user"),
            "rejected",
            {"main": ["read"], "sb1": [], "sb2": []},
        ),
        (
            "Municipality",
            LazyFixture("admin_user"),
            "sb1",
            {"main": ["read"], "sb1": [], "sb2": []},
        ),
        (
            "Municipality",
            LazyFixture("admin_user"),
            "sb2",
            {"main": ["read"], "sb1": ["read"], "sb2": []},
        ),
        (
            "Municipality",
            LazyFixture("admin_user"),
            "conclusion",
            {"main": ["read"], "sb1": ["read"], "sb2": ["read"]},
        ),
        ("Support", LazyFixture("admin_user"), "new", FULL_PERMISSIONS),
        ("Support", LazyFixture("admin_user"), "subm", FULL_PERMISSIONS),
        ("Support", LazyFixture("admin_user"), "correction", FULL_PERMISSIONS),
        ("Support", LazyFixture("admin_user"), "rejected", FULL_PERMISSIONS),
        ("Support", LazyFixture("admin_user"), "sb1", FULL_PERMISSIONS),
        ("Support", LazyFixture("admin_user"), "sb2", FULL_PERMISSIONS),
        ("Support", LazyFixture("admin_user"), "conclusion", FULL_PERMISSIONS),
    ],
)
def test_instance_permissions(
    admin_client,
    activation,
    applicant_factory,
    instance,
    expected_permissions,
    use_caluma_form,
):
    applicant_factory(invitee=instance.user, instance=instance)

    url = reverse("instance-detail", args=[instance.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    permissions = response.json()["data"]["meta"]["permissions"]

    assert permissions == expected_permissions
