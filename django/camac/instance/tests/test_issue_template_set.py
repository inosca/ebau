import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,size",
    [("Applicant", 0), ("Canton", 1), ("Municipality", 1), ("Service", 1)],
)
def test_issue_template_set_list(admin_client, issue_template_set, activation, size):
    url = reverse("issue-template-set-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size
    if size > 0:
        assert json["data"][0]["id"] == str(issue_template_set.pk)


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_404_NOT_FOUND),
        ("Municipality", status.HTTP_200_OK),
        ("Canton", status.HTTP_200_OK),
        ("Service", status.HTTP_200_OK),
    ],
)
def test_issue_template_set_update(
    admin_client, issue_template_set, activation, status_code
):
    url = reverse("issue-template-set-detail", args=[issue_template_set.pk])
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
def test_issue_template_set_create(
    admin_client, issue_template, group, service, activation, status_code
):
    url = reverse("issue-template-set-list")

    data = {
        "data": {
            "type": "issue-template-sets",
            "id": None,
            "attributes": {"name": "Test"},
            "relationships": {
                "issue-templates": {
                    "data": [{"type": "issue-templates", "id": issue_template.pk}]
                }
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
def test_issue_template_set_destroy(
    admin_client, issue_template_set, activation, status_code
):
    url = reverse("issue-template-set-detail", args=[issue_template_set.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("role__name", [("Canton"), ("Municipality"), ("Service")])
def test_issue_template_set_generate_set(
    admin_client, issue_template_set_issue_templates, instance, activation
):
    itsit = issue_template_set_issue_templates
    set_url = reverse("issue-template-set-apply", args=[itsit.issuetemplateset.pk])

    data = {
        "data": {
            "type": "issue-template-sets-apply",
            "id": None,
            "relationships": {
                "instance": {"data": {"type": "instances", "id": instance.pk}}
            },
        }
    }

    set_response = admin_client.post(set_url, data=data)
    assert set_response.status_code == status.HTTP_204_NO_CONTENT

    response = admin_client.get(reverse("issue-list"))
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == itsit.issuetemplateset.issue_templates.count()
