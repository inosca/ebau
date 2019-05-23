import pytest
from django.urls import reverse
from rest_framework import status

from camac.markers import only_schwyz

# module-level skip if we're not testing Schwyz variant
pytestmark = only_schwyz


@pytest.mark.parametrize(
    "role__name,size",
    [("Applicant", 0), ("Kanton", 1), ("Gemeinde", 1), ("Fachstelle", 1)],
)
def test_issue_template_template_list(admin_client, issue_template, activation, size):
    url = reverse("issue-template-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size
    if size > 0:
        assert json["data"][0]["id"] == str(issue_template.pk)


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_404_NOT_FOUND),
        ("Gemeinde", status.HTTP_200_OK),
        ("Kanton", status.HTTP_200_OK),
        ("Fachstelle", status.HTTP_200_OK),
    ],
)
def test_issue_template_update(admin_client, issue_template, activation, status_code):
    url = reverse("issue-template-detail", args=[issue_template.pk])
    response = admin_client.patch(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Kanton", status.HTTP_201_CREATED),
        ("Fachstelle", status.HTTP_201_CREATED),
        ("Gemeinde", status.HTTP_201_CREATED),
    ],
)
def test_issue_template_create(admin_client, group, service, activation, status_code):
    url = reverse("issue-template-list")

    data = {
        "data": {
            "type": "issue-templates",
            "id": None,
            "attributes": {"text": "Test", "deadline_length": "2"},
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
        ("Gemeinde", status.HTTP_204_NO_CONTENT),
        ("Kanton", status.HTTP_204_NO_CONTENT),
        ("Fachstelle", status.HTTP_204_NO_CONTENT),
    ],
)
def test_issue_template_destroy(admin_client, issue_template, activation, status_code):
    url = reverse("issue-template-detail", args=[issue_template.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code
