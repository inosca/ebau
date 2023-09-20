import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.instance.models import Issue


@pytest.mark.parametrize(
    "role__name,size",
    [("Applicant", 0), ("Canton", 1), ("Municipality", 1), ("Service", 1)],
)
def test_issue_list(admin_client, issue, activation, size):
    url = reverse("issue-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size
    if size > 0:
        assert json["data"][0]["id"] == str(issue.pk)


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_404_NOT_FOUND),
        ("Municipality", status.HTTP_200_OK),
        ("Canton", status.HTTP_200_OK),
        ("Service", status.HTTP_200_OK),
    ],
)
def test_issue_update(admin_client, issue, activation, status_code):
    url = reverse("issue-detail", args=[issue.pk])
    response = admin_client.patch(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Canton", status.HTTP_201_CREATED),
        ("Service", status.HTTP_201_CREATED),
        ("Municipality", status.HTTP_201_CREATED),
    ],
)
def test_issue_create(admin_client, instance, group, service, activation, status_code):
    url = reverse("issue-list")

    data = {
        "data": {
            "type": "issues",
            "id": None,
            "attributes": {"text": "Test", "deadline_date": "2018-01-01"},
            "relationships": {
                "instance": {"data": {"type": "instances", "id": instance.pk}}
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        json = response.json()
        assert json["data"]["relationships"]["group"]["data"]["id"] == (str(group.pk))
        assert json["data"]["relationships"]["service"]["data"]["id"] == (
            str(service.pk)
        )


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_404_NOT_FOUND),
        ("Municipality", status.HTTP_204_NO_CONTENT),
        ("Canton", status.HTTP_204_NO_CONTENT),
        ("Service", status.HTTP_204_NO_CONTENT),
    ],
)
def test_issue_destroy(admin_client, issue, activation, status_code):
    url = reverse("issue-detail", args=[issue.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("issue__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,size",
    [
        ("Applicant", 0),
        ("Municipality", 1),
        ("Service", 1),
    ],
)
def test_issue_visible_for(
    admin_client, request, issue, group, size, application_settings
):
    request.group = group

    application_settings["ROLE_PERMISSIONS"] = {
        "Municipality": "municipality",
        "Service": "service",
    }

    issues = (
        Issue.objects.get_queryset().visible_for(request).values_list("pk", flat=True)
    )

    assert len(issues) == size
    if size > 0:
        assert issues[0] == issue.pk
