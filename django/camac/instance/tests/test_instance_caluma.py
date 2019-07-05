import json

import pytest
from django.core import mail
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.applicants.factories import ApplicantFactory
from camac.core.models import Chapter, Question, QuestionType
from camac.instance.models import Instance
from camac.instance.serializers import (
    SUBMIT_DATE_CHAPTER,
    SUBMIT_DATE_QUESTION_ID,
    CalumaInstanceSerializer,
)


@pytest.fixture
def submit_date_question(db):
    chap, _ = Chapter.objects.get_or_create(pk=SUBMIT_DATE_CHAPTER, name="Hidden")
    qtype, _ = QuestionType.objects.get_or_create(name="Date")
    question, _ = Question.objects.get_or_create(
        pk=SUBMIT_DATE_QUESTION_ID, question_type=qtype
    )
    question.trans.create(language="de", name="Einreichedatum")

    return question


@pytest.fixture
def mock_public_status(mocker):
    mocker.patch(
        "camac.instance.serializers.CalumaInstanceSerializer.get_public_status",
        lambda s, i: "creation",
    )


RESP_CASE_INCOMPLETE = {
    "data": {
        "node": {
            "id": "Q2FzZToxODBlMGQxNy0zZmZkLTQ1ZDMtYTU1MC1kMjVjNGVhODIxNDU=",
            "meta": {},
            "workflow": {"id": "V29ya2Zsb3c6YnVpbGRpbmctcGVybWl0"},
            "workItems": {
                "edges": [
                    {"node": {"status": "WORKING", "task": {"slug": "fill-form"}}}
                ]
            },
        }
    }
}
RESP_CASE_ALREADY_ASSIGNED = {
    "data": {
        "node": {
            "id": "Q2FzZToxODBlMGQxNy0zZmZkLTQ1ZDMtYTU1MC1kMjVjNGVhODIxNDU=",
            "meta": {"camac-instance-id": 9999},
            "workflow": {"id": "V29ya2Zsb3c6YnVpbGRpbmctcGVybWl0"},
            "workItems": {
                "edges": [
                    {"node": {"status": "COMPLETED", "task": {"slug": "fill-form"}}}
                ]
            },
        }
    }
}
RESP_CASE_COMPLETED = {
    "data": {
        "node": {
            "id": "Q2FzZToxODBlMGQxNy0zZmZkLTQ1ZDMtYTU1MC1kMjVjNGVhODIxNDU=",
            "meta": {},
            "workflow": {"id": "V29ya2Zsb3c6YnVpbGRpbmctcGVybWl0"},
            "workItems": {
                "edges": [
                    {"node": {"status": "COMPLETED", "task": {"slug": "fill-form"}}}
                ]
            },
        }
    }
}


@pytest.mark.freeze_time("2019-05-02")
@pytest.mark.parametrize(
    "work_item_resp,expected_resp",
    [
        (RESP_CASE_COMPLETED, status.HTTP_201_CREATED),
        (RESP_CASE_ALREADY_ASSIGNED, status.HTTP_400_BAD_REQUEST),
    ],
)
def test_create_instance(
    db,
    admin_client,
    mocker,
    instance_state,
    form,
    snapshot,
    work_item_resp,
    expected_resp,
    bern_instance_states,
    use_caluma_form,
):
    recorded_requests = []

    def last_inst_id():
        return Instance.objects.order_by("-instance_id").first().instance_id

    mock_responses = [
        # first response: NG asks caluma for data about our case
        mocker.MagicMock(json=lambda: work_item_resp, status_code=status.HTTP_200_OK),
        # second response: NG updates case with instance id
        mocker.MagicMock(
            json=lambda: {
                "data": {
                    "saveCase": {
                        "case": {
                            "id": "Q2FzZTphNWVlMDFjNS1kZDc0LTQ2MzQtODgzNC01NDMyNzU2MDZmYTk=",
                            "meta": {"camac-instance-id": last_inst_id()},
                        }
                    }
                }
            },
            status_code=status.HTTP_200_OK,
        ),
    ]

    def mock_post(url, *args, **kwargs):
        recorded_requests.append((url, args, kwargs))
        resp = mock_responses.pop(0)

        return resp

    mocker.patch("requests.post", mock_post)

    case_id = "Q2FzZToxODBlMGQxNy0zZmZkLTQ1ZDMtYTU1MC1kMjVjNGVhODIxNDU="
    create_resp = admin_client.post(
        reverse("instance-list"),
        {
            "data": {
                "type": "instances",
                "attributes": {"caluma-case-id": case_id},
                "relationships": {
                    "form": {"data": {"id": form.form_id, "type": "forms"}},
                    "instance-state": {
                        "data": {
                            "id": instance_state.instance_state_id,
                            "type": "instance-states",
                        }
                    },
                },
            }
        },
    )
    assert create_resp.status_code == expected_resp, create_resp.content

    if expected_resp == status.HTTP_400_BAD_REQUEST:
        # in this case, we don't need to test the rest of the procedure
        return

    # make sure meta is updated correctly
    assert json.loads(
        recorded_requests[1][2]["json"]["variables"]["input"]["meta"]
    ) == {"camac-instance-id": last_inst_id()}

    # to validate the rest, we need to "fix" the instance id to use snapshot
    recorded_requests[1][2]["json"]["variables"]["input"]["meta"] = json.dumps(
        {"camac-instance-id": "XXX"}
    )
    snapshot.assert_match(recorded_requests)


@pytest.mark.parametrize(
    "instance_state__name,instance__creation_date",
    [("new", "2018-04-17T09:31:56+02:00")],
)
@pytest.mark.parametrize(
    "role_t__name,instance__user,editable",
    [
        ("Service", LazyFixture("user"), {"form", "document"}),
        ("Canton", LazyFixture("user"), {"form", "document"}),
    ],
)
def test_instance_list(
    admin_client,
    instance,
    activation,
    group,
    editable,
    group_location_factory,
    mock_public_status,
    use_caluma_form,
    multilang,
):

    url = reverse("instance-list")
    included = CalumaInstanceSerializer.included_serializers
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
    mock_public_status,
    use_caluma_form,
    multilang,
    application_settings,
):

    application_settings["NOTIFICATIONS"]["SUBMIT"] = [
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
    "role_t__name,instance__user", [("Canton", LazyFixture("user"))]
)
def test_responsible_user(admin_client, instance, user, service, multilang):

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
