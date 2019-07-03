import json

import pytest
from django.core import mail
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.applicants.factories import ApplicantFactory
from camac.core.models import Chapter, Question, QuestionType
from camac.instance.serializers.bern import SUBMIT_DATE_CHAPTER, SUBMIT_DATE_QUESTION_ID
from camac.instance.views import InstanceView
from camac.markers import only_bern

# module-level skip if we're not testing Bern variant
pytestmark = only_bern


@pytest.fixture
def submit_date_question(db):
    chap, _ = Chapter.objects.get_or_create(pk=SUBMIT_DATE_CHAPTER, name="Hidden")
    qtype, _ = QuestionType.objects.get_or_create(name="Date")
    question, _ = Question.objects.get_or_create(
        pk=SUBMIT_DATE_QUESTION_ID, question_type=qtype
    )
    question.trans.create(language="de", name="Einreichedatum")

    return question


@pytest.mark.parametrize(
    "instance_state__name,instance__creation_date",
    [("new", "2018-04-17T09:31:56+02:00")],
)
@pytest.mark.parametrize(
    "role_t__name,instance__user,editable",
    [
        ("Leitung Fachstelle", LazyFixture("user"), {"form", "document"}),
        ("Leitung Baukontrolle", LazyFixture("user"), {"form", "document"}),
        ("System-Betrieb", LazyFixture("user"), {"form", "document"}),
    ],
)
def test_instance_list(
    admin_client, instance, activation, group, editable, group_location_factory, mocker
):

    mocker.patch(
        "camac.instance.serializers.bern.BernInstanceSerializer.get_public_status",
        lambda s, i: "creation",
    )
    url = reverse("instance-list")
    included = InstanceView.serializer_class.included_serializers
    response = admin_client.get(
        url,
        data={
            "include": ",".join(included.keys()),
            "creation_date_before": "17.04.2018",
            "creation_date_after": "17.04.2018",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(instance.pk)
    assert set(json["data"][0]["meta"]["editable"]) == set(editable)
    # Included previous_instance_state and instance_state are the same
    assert len(json["included"]) == len(included) - 1


@pytest.mark.parametrize(
    "instance_state__name,instance__creation_date",
    [("Neu", "2018-04-17T09:31:56+02:00")],
)
@pytest.mark.parametrize(
    "role_t__name,instance__user,editable",
    [("Gesuchsteller", LazyFixture("admin_user"), {"form", "instance", "document"})],
)
def test_instance_list_as_applicant(
    admin_client,
    admin_user,
    instance,
    activation,
    group,
    editable,
    group_location_factory,
    mocker,
):

    ApplicantFactory(instance=instance, user=admin_user, invitee=admin_user)
    mocker.patch(
        "camac.instance.serializers.bern.BernInstanceSerializer.get_public_status",
        lambda s, i: "creation",
    )

    url = reverse("instance-list")
    included = InstanceView.serializer_class.included_serializers
    response = admin_client.get(
        url,
        data={
            "include": ",".join(included.keys()),
            "creation_date_before": "17.04.2018",
            "creation_date_after": "17.04.2018",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(instance.pk)
    assert set(json["data"][0]["meta"]["editable"]) == set(editable)
    # Included previous_instance_state and instance_state are the same
    assert len(json["included"]) == len(included) - 1


@pytest.mark.parametrize(
    "role_t__name,instance__user", [("Gesuchsteller", LazyFixture("admin_user"))]
)
def test_instance_detail(admin_client, admin_user, instance, mocker):
    ApplicantFactory(instance=instance, user=admin_user, invitee=admin_user)
    mocker.patch(
        "camac.instance.serializers.bern.BernInstanceSerializer.get_public_status",
        lambda s, i: "creation",
    )

    url = reverse("instance-detail", args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("instance__identifier", ["00-00-000"])
@pytest.mark.parametrize("form_field__name", ["name"])
@pytest.mark.parametrize(
    "role_t__name,instance__user", [("Gesuchsteller", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize(
    "form_field__value,search",
    [
        ("simpletext", "simple"),
        (["list", "value"], "list"),
        ({"key": ["l-list-d", ["b-list-d"]]}, "list"),
    ],
)
def test_instance_search(
    admin_client, admin_user, instance, form_field, search, mocker
):
    ApplicantFactory(instance=instance, user=admin_user, invitee=admin_user)
    url = reverse("instance-list")
    mocker.patch(
        "camac.instance.serializers.bern.BernInstanceSerializer.get_public_status",
        lambda s, i: "creation",
    )

    response = admin_client.get(url, {"search": search})
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(instance.pk)


@pytest.mark.parametrize("instance_state__name", ["Neu"])
@pytest.mark.parametrize(
    "role_t__name,instance__user,status_code",
    [
        ("Applicant", LazyFixture("admin_user"), status.HTTP_204_NO_CONTENT),
        ("Service", LazyFixture("user"), status.HTTP_403_FORBIDDEN),
        ("Fachstelle", LazyFixture("user"), status.HTTP_403_FORBIDDEN),
        # Support has access to dossier, and can also delete in this test because the instance
        # is owned by the same user
        ("Support", LazyFixture("admin_user"), status.HTTP_204_NO_CONTENT),
    ],
)
def test_instance_destroy(
    admin_client, role, admin_user, instance, status_code, location_factory
):
    ApplicantFactory(instance=instance, user=admin_user, invitee=admin_user)
    url = reverse("instance-detail", args=[instance.pk])
    response = admin_client.delete(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("instance_state__name", ["Neu", "Zurückgewiesen"])
@pytest.mark.parametrize(
    "role_t__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize(
    "new_instance_state,response_status",
    [(20000, status.HTTP_200_OK), (1, status.HTTP_400_BAD_REQUEST)],
)
@pytest.mark.parametrize(
    "notification_template__body",
    [
        """
    Guten Tag

    Im eBau gibt es einen neuen Eingang vom Typ {{FORM_NAME}} mit der Dossier-Nr. {{INSTANCE_ID}}.

    {{DOSSIER_LINK}}

    Freundliche Grüsse
    {{LEITBEHOERDE_NAME}}
    """,
        """

    Guten Tag

    Ihr/e {{FORM_NAME}} mit der Dossier-Nr. {{INSTANCE_ID}} wurde erfolgreich übermittelt. Das Verfahren wird nun ausgelöst. Sie werden über Statusänderungen informiert.

    {{DOSSIER_LINK}}

    Gerne möchten wir erfahren wie einfach die elektronische Eingabe eines Gesuches war. Wir bitten Sie daher, sich 2 - 3 Minuten Zeit zu nehmen und den folgenden Fragebogen zu beantworten. Besten Dank.

    https://www.onlineumfragen.com/login.cfm?umfrage=87201

    """,
    ],
)
def test_instance_submit(
    requests_mock,
    admin_client,
    role,
    instance,
    bern_instance_states,
    service,
    admin_user,
    response_status,
    new_instance_state,
    notification_template,
    submit_date_question,
    settings,
    mocker,
):
    mocker.patch(
        "camac.instance.serializers.bern.BernInstanceSerializer.get_public_status",
        lambda s, i: "creation",
    )

    settings.APPLICATION["NOTIFICATIONS"]["SUBMIT"] = [
        {"template_id": notification_template.pk, "recipient_types": ["applicant"]}
    ]

    requests_mock.post(
        "http://caluma:8000/graphql/",
        text=json.dumps(
            {
                "data": {
                    "node": {
                        "id": 1234,
                        "meta": {},
                        "workflow": {"id": 99999},
                        "document": {
                            "form": {"slug": "vorabklaerung-einfach"},
                            "answers": {
                                "edges": [{"node": {"stringValue": service.pk}}]
                            },
                        },
                    }
                }
            }
        ),
    )
    ApplicantFactory(instance=instance, user=admin_user, invitee=admin_user)
    url = reverse("instance-detail", args=[instance.pk])
    data = {
        "data": {
            "type": "instances",
            "id": instance.pk,
            "relationships": {
                "instance-state": {
                    "data": {"type": "instance-states", "id": new_instance_state}
                }
            },
        }
    }
    response = admin_client.patch(url, data)
    assert response.status_code == response_status

    if response_status == 200:
        assert len(mail.outbox) == 1
        assert instance.user.email in mail.outbox[0].recipients()

        assert mail.outbox[0].subject.startswith("[eBau Test]: ")
    else:
        # no mail if submission not accepted!
        assert len(mail.outbox) == 0


@pytest.mark.parametrize(
    "role_t__name,instance__user", [("System-Betrieb", LazyFixture("user"))]
)
def test_responsible_user(admin_client, instance, user, service):

    instance.responsibilities.create(user=user, service=service)

    # First make sure we can find instances with given responsible user
    resp = admin_client.get(
        reverse("instance-list"), {"responsible_user": str(user.pk)}
    )
    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert len(resp.json()["data"]) == 1

    # "nobody" filter should return nothing if all instances have a responsible user
    resp = admin_client.get(reverse("instance-list"), {"responsible_user": "NOBODY"})
    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert len(resp.json()["data"]) == 0

    # "nobody" filter should return instance where there is no responsible user
    instance.responsibilities.all().delete()
    resp = admin_client.get(reverse("instance-list"), {"responsible_user": "NOBODY"})
    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert len(resp.json()["data"]) == 1
