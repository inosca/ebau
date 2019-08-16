import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

FULL_PERMISSIONS = {
    "main": ["read", "write", "write-meta"],
    "sb1": ["read", "write", "write-meta"],
    "sb2": ["read", "write", "write-meta"],
    "nfd": ["read", "write", "write-meta"],
}


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,instance_state__name,expected_permissions",
    [
        (
            "Applicant",
            "new",
            {
                "main": [
                    "read",
                    "write",
                    "write-meta",  # write-meta camac-instance-id, submit-date
                ],
                "sb1": [],
                "sb2": [],
                "nfd": [],
            },
        ),
        ("Applicant", "subm", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        (
            "Applicant",
            "correction",
            {"main": ["read"], "sb1": [], "sb2": [], "nfd": []},
        ),
        (
            "Applicant",
            "rejected",
            {
                "main": ["read", "write", "write-meta"],  # write-meta: submit-date
                "sb1": [],
                "sb2": [],
                "nfd": [],
            },
        ),
        (
            "Applicant",
            "sb1",
            {
                "main": ["read"],
                "sb1": ["read", "write", "write-meta"],  # write-meta: submit-date
                "sb2": [],
                "nfd": [],
            },
        ),
        (
            "Applicant",
            "sb2",
            {
                "main": ["read"],
                "sb1": ["read"],
                "sb2": ["read", "write", "write-meta"],  # write-meta: submit-date
                "nfd": [],
            },
        ),
        (
            "Applicant",
            "conclusion",
            {"main": ["read"], "sb1": ["read"], "sb2": ["read"], "nfd": []},
        ),
        (
            "Applicant",
            "nfd",
            {"main": ["read"], "sb1": [], "sb2": [], "nfd": ["read", "write"]},
        ),
        ("Service", "new", {"main": [], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "subm", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "correction", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "rejected", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "sb1", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "sb2", {"main": ["read"], "sb1": ["read"], "sb2": [], "nfd": []}),
        (
            "Service",
            "conclusion",
            {"main": ["read"], "sb1": ["read"], "sb2": ["read"], "nfd": []},
        ),
        ("Service", "nfd", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        (
            "Municipality",
            "new",
            {"main": [], "sb1": [], "sb2": [], "nfd": ["write", "write-meta"]},
        ),
        (
            "Municipality",
            "subm",
            {
                "main": ["read", "write-meta"],  # write-meta: ebau-number
                "sb1": [],
                "sb2": [],
                "nfd": ["write", "write-meta"],
            },
        ),
        (
            "Municipality",
            "correction",
            {
                "main": ["read", "write"],
                "sb1": [],
                "sb2": [],
                "nfd": ["write", "write-meta"],
            },
        ),
        (
            "Municipality",
            "rejected",
            {"main": ["read"], "sb1": [], "sb2": [], "nfd": ["write", "write-meta"]},
        ),
        (
            "Municipality",
            "sb1",
            {"main": ["read"], "sb1": [], "sb2": [], "nfd": ["write", "write-meta"]},
        ),
        (
            "Municipality",
            "sb2",
            {
                "main": ["read"],
                "sb1": ["read"],
                "sb2": [],
                "nfd": ["write", "write-meta"],
            },
        ),
        (
            "Municipality",
            "conclusion",
            {
                "main": ["read"],
                "sb1": ["read"],
                "sb2": ["read"],
                "nfd": ["write", "write-meta"],
            },
        ),
        (
            "Municipality",
            "nfd",
            {"main": ["read"], "sb1": [], "sb2": [], "nfd": ["write", "write-meta"]},
        ),
        ("Support", "new", FULL_PERMISSIONS),
        ("Support", "subm", FULL_PERMISSIONS),
        ("Support", "correction", FULL_PERMISSIONS),
        ("Support", "rejected", FULL_PERMISSIONS),
        ("Support", "sb1", FULL_PERMISSIONS),
        ("Support", "sb2", FULL_PERMISSIONS),
        ("Support", "conclusion", FULL_PERMISSIONS),
        ("Support", "nfd", FULL_PERMISSIONS),
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
