import pytest
from django.urls import reverse
from rest_framework import status

from camac.markers import only_schwyz

pytestmark = only_schwyz


@pytest.mark.parametrize(
    "role__name,num_queries,size",
    [("Applicant", 1, 0), ("Fachstelle", 2, 1), ("Gemeinde", 2, 1), ("Kanton", 2, 1)],
)
def test_notification_template_list(
    admin_client, notification_template, num_queries, django_assert_num_queries, size
):
    url = reverse("notificationtemplate-list")
    with django_assert_num_queries(num_queries):
        response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    if size > 0:
        json = response.json()
        assert len(json["data"]) == size
        assert json["data"][0]["id"] == str(notification_template.pk)


@pytest.mark.parametrize("role__name", ["Kanton"])
def test_notification_template_detail(admin_client, notification_template):
    url = reverse("notificationtemplate-detail", args=[notification_template.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "notification_template__body", ["{{identifier}} {{answer_period_date}}"]
)
@pytest.mark.parametrize(
    "role__name,instance__identifier,notification_template__subject,status_code",
    [
        ("Kanton", "identifier", "{{identifier}}", status.HTTP_200_OK),
        ("Kanton", "identifier", "{{$invalid}}", status.HTTP_400_BAD_REQUEST),
    ],
)
@pytest.mark.freeze_time("2017-1-1")
def test_notification_template_merge(
    admin_client,
    instance,
    notification_template,
    status_code,
    activation,
    billing_entry,
    settings,
):
    url = reverse("notificationtemplate-merge", args=[notification_template.pk])

    response = admin_client.get(url, data={"instance": instance.pk})
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert (
            json["data"]["attributes"]["subject"]
            == settings.EMAIL_PREFIX_SUBJECT + instance.identifier
        )
        assert (
            json["data"]["attributes"]["body"]
            == settings.EMAIL_PREFIX_BODY + "identifier 21.01.2017"
        )
        assert json["data"]["id"] == "{0}-{1}".format(
            notification_template.pk, instance.pk
        )
        assert json["data"]["type"] == "notification-template-merges"


@pytest.mark.parametrize(
    "user__email,service__email", [("user@example.com", "service@example.com")]
)
@pytest.mark.parametrize(
    "notification_template__subject,instance__identifier",
    [("{{identifier}}", "identifer")],
)
@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Kanton", status.HTTP_204_NO_CONTENT),
        ("Gemeinde", status.HTTP_204_NO_CONTENT),
        ("Fachstelle", status.HTTP_204_NO_CONTENT),
        ("Applicant", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_notification_template_sendmail(
    admin_client,
    instance,
    notification_template,
    status_code,
    mailoutbox,
    activation,
    settings,
):

    url = reverse("notificationtemplate-sendmail", args=[notification_template.pk])

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "id": None,
            "attributes": {
                "body": "Test body",
                "recipient-types": ["applicant", "municipality", "service"],
            },
            "relationships": {
                "instance": {"data": {"type": "instances", "id": instance.pk}}
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_204_NO_CONTENT:
        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        assert set(mail.bcc) == {
            "user@example.com",
            "service@example.com",
            "service@example.com",
        }
        assert mail.subject == settings.EMAIL_PREFIX_SUBJECT + instance.identifier
        assert mail.body == settings.EMAIL_PREFIX_BODY + "Test body"
