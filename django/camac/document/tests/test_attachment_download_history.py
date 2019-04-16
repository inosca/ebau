import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from .data import django_file


def test_attachment_download_history_list(
    admin_client, attachment_download_history_factory
):
    adhl = attachment_download_history_factory.create_batch(2)
    url = reverse("attachmentdownloadhistory-list")
    response = admin_client.get(url, {"attachment": adhl[0].attachment.pk})

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    print(json)
    assert len(json["data"]) == 1
    assert json["data"][0]["relationships"]["attachment"]["data"]["id"] == str(
        adhl[0].attachment.pk
    )


@pytest.mark.parametrize(
    "role__name,instance__user,attachment__path",
    [("Applicant", LazyFixture("admin_user"), django_file("multiple-pages.pdf"))],
)
def test_attachment_download_history_create(
    admin_client, attachment_attachment_sections, attachment_section_group_acl
):
    download_url = reverse(
        "attachment-download", args=[attachment_attachment_sections.attachment.path]
    )
    download_response = admin_client.get(download_url)
    assert download_response.status_code == status.HTTP_200_OK

    histroy_url = reverse("attachmentdownloadhistory-list")
    history_response = admin_client.get(histroy_url)

    assert history_response.status_code == status.HTTP_200_OK
    json = history_response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["relationships"]["attachment"]["data"]["id"] == str(
        attachment_attachment_sections.attachment.pk
    )
