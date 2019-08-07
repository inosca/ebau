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

MAIN_FORMS = [
    "baugesuch",
    "baugesuch-generell",
    "baugesuch-mit-uvp",
    "vorabklaerung-einfach",
    "vorabklaerung-vollstaendig",
]


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


@pytest.fixture
def mock_caluma_forms(mocker):
    mocker.patch(
        "camac.instance.mixins.InstanceEditableMixin._get_caluma_main_forms",
        lambda s: MAIN_FORMS,
    )


@pytest.fixture
def instance_service_construction_control(
    instance_service_factory, service_factory, service_group_factory, instance
):
    return instance_service_factory(
        instance=instance,
        service=service_factory(
            service_group=service_group_factory(name="construction-control")
        ),
    )


@pytest.mark.freeze_time("2019-05-02")
@pytest.mark.parametrize("instance_state__name", ["new"])
def test_create_instance(
    db,
    admin_client,
    mocker,
    instance_state,
    form,
    snapshot,
    use_caluma_form,
    mock_caluma_forms,
):
    recorded_requests = []

    def last_inst_id():
        return Instance.objects.order_by("-instance_id").first().instance_id

    mock_responses = [
        # first response: NG asks caluma if the form is a main form
        mocker.MagicMock(
            json=lambda: {
                "data": {
                    "allForms": {
                        "edges": [
                            {"node": {"slug": "test", "meta": {"is-main-form": True}}}
                        ]
                    }
                }
            },
            status_code=status.HTTP_200_OK,
        ),
        # second response: NG updates case with instance id
        mocker.MagicMock(
            json=lambda: {
                "data": {
                    "saveDocument": {
                        "document": {
                            "id": "RG9jdW1lbnQ6NjYxOGU5YmQtYjViZi00MTU2LWI0NWMtZTg0M2Y2MTFiZDI2",
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

    create_resp = admin_client.post(
        reverse("instance-list"),
        {
            "data": {
                "type": "instances",
                "attributes": {"caluma-form": "test"},
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
    assert create_resp.status_code == status.HTTP_201_CREATED, create_resp.content

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
        ("Service", LazyFixture("user"), {"document"}),
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
    mock_caluma_forms,
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


@pytest.mark.parametrize(
    "role__name,instance__user,instance_state__name,readable,editable",
    [
        ("Applicant", LazyFixture("admin_user"), "new", MAIN_FORMS, MAIN_FORMS),
        ("Applicant", LazyFixture("admin_user"), "rejected", MAIN_FORMS, MAIN_FORMS),
        ("Applicant", LazyFixture("admin_user"), "correction", MAIN_FORMS, []),
        ("Applicant", LazyFixture("admin_user"), "sb1", MAIN_FORMS + ["sb1"], ["sb1"]),
        (
            "Applicant",
            LazyFixture("admin_user"),
            "sb2",
            MAIN_FORMS + ["sb1", "sb2"],
            ["sb2"],
        ),
        (
            "Applicant",
            LazyFixture("admin_user"),
            "conclusion",
            MAIN_FORMS + ["sb1", "sb2"],
            [],
        ),
        ("Service", LazyFixture("admin_user"), "new", MAIN_FORMS, []),
        ("Service", LazyFixture("admin_user"), "rejected", MAIN_FORMS, []),
        ("Service", LazyFixture("admin_user"), "correction", MAIN_FORMS, []),
        ("Service", LazyFixture("admin_user"), "sb1", MAIN_FORMS, []),
        ("Service", LazyFixture("admin_user"), "sb2", MAIN_FORMS + ["sb1"], []),
        (
            "Service",
            LazyFixture("admin_user"),
            "conclusion",
            MAIN_FORMS + ["sb1", "sb2"],
            [],
        ),
        ("Municipality", LazyFixture("admin_user"), "new", MAIN_FORMS, []),
        ("Municipality", LazyFixture("admin_user"), "rejected", MAIN_FORMS, []),
        (
            "Municipality",
            LazyFixture("admin_user"),
            "correction",
            MAIN_FORMS,
            MAIN_FORMS,
        ),
        ("Municipality", LazyFixture("admin_user"), "sb1", MAIN_FORMS, []),
        ("Municipality", LazyFixture("admin_user"), "sb2", MAIN_FORMS + ["sb1"], []),
        (
            "Municipality",
            LazyFixture("admin_user"),
            "conclusion",
            MAIN_FORMS + ["sb1", "sb2"],
            [],
        ),
        ("Canton", LazyFixture("admin_user"), "new", MAIN_FORMS, []),
        ("Canton", LazyFixture("admin_user"), "rejected", MAIN_FORMS, []),
        ("Canton", LazyFixture("admin_user"), "correction", MAIN_FORMS, []),
        ("Canton", LazyFixture("admin_user"), "sb1", MAIN_FORMS, []),
        ("Canton", LazyFixture("admin_user"), "sb2", MAIN_FORMS + ["sb1"], []),
        (
            "Canton",
            LazyFixture("admin_user"),
            "conclusion",
            MAIN_FORMS + ["sb1", "sb2"],
            [],
        ),
    ],
)
def test_instance_permissions(
    admin_client,
    activation,
    applicant_factory,
    instance,
    readable,
    editable,
    use_caluma_form,
    requests_mock,
):
    requests_mock.post(
        "http://caluma:8000/graphql/",
        text=json.dumps(
            {
                "data": {
                    "allForms": {
                        "edges": [{"node": {"slug": slug}} for slug in MAIN_FORMS]
                    }
                }
            }
        ),
    )

    applicant_factory(invitee=instance.user, instance=instance)

    url = reverse("instance-detail", args=[instance.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]

    assert set(data["meta"]["readable-forms"]) == set(readable)
    assert set(data["meta"]["editable-forms"]) == set(editable)


@pytest.mark.parametrize("instance_state__name", ["new", "rejected"])
@pytest.mark.parametrize(
    "role_t__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize("new_instance_state_name", ["subm"])
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
    instance_state_factory,
    service,
    admin_user,
    new_instance_state_name,
    notification_template,
    submit_date_question,
    settings,
    mock_public_status,
    use_caluma_form,
    multilang,
    application_settings,
    mock_caluma_forms,
):

    application_settings["NOTIFICATIONS"]["SUBMIT"] = [
        {"template_id": notification_template.pk, "recipient_types": ["applicant"]}
    ]

    requests_mock.post(
        "http://caluma:8000/graphql/",
        text=json.dumps(
            {
                "data": {
                    "allDocuments": {
                        "edges": [
                            {
                                "node": {
                                    "id": "RG9jdW1lbnQ6NjYxOGU5YmQtYjViZi00MTU2LWI0NWMtZTg0M2Y2MTFiZDI2",
                                    "meta": {"camac-instance-id": instance.pk},
                                    "form": {
                                        "slug": "vorabklaerung-einfach",
                                        "name": "Baugesuch",
                                        "meta": {"is-main-form": True},
                                    },
                                    "answers": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "question": {"slug": "gemeinde"},
                                                    "value": service.pk,
                                                }
                                            }
                                        ]
                                    },
                                }
                            }
                        ]
                    }
                }
            }
        ),
    )

    instance_state_factory(name=new_instance_state_name)
    ApplicantFactory(instance=instance, user=admin_user, invitee=admin_user)

    response = admin_client.post(reverse("instance-submit", args=[instance.pk]))

    assert response.status_code == status.HTTP_200_OK

    assert len(mail.outbox) == 1
    assert instance.user.email in mail.outbox[0].recipients()

    assert mail.outbox[0].subject.startswith("[eBau Test]: ")


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


@pytest.mark.parametrize(
    "instance_state__name,expected_status",
    [("sb1", status.HTTP_200_OK), ("new", status.HTTP_403_FORBIDDEN)],
)
@pytest.mark.parametrize("new_instance_state_name", ["sb2"])
@pytest.mark.parametrize(
    "role_t__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
def test_instance_report(
    requests_mock,
    admin_client,
    role,
    instance,
    instance_state_factory,
    instance_service_construction_control,
    expected_status,
    new_instance_state_name,
    notification_template,
    application_settings,
    service,
    admin_user,
    use_caluma_form,
    multilang,
    mock_caluma_forms,
):
    application_settings["NOTIFICATIONS"]["REPORT"] = [
        {
            "template_id": notification_template.pk,
            "recipient_types": ["applicant", "construction_control"],
        }
    ]

    requests_mock.post(
        "http://caluma:8000/graphql/",
        text=json.dumps(
            {
                "data": {
                    "allDocuments": {
                        "edges": [
                            {
                                "node": {
                                    "id": "RG9jdW1lbnQ6NjYxOGU5YmQtYjViZi00MTU2LWI0NWMtZTg0M2Y2MTFiZDI2",
                                    "meta": {"camac-instance-id": instance.pk},
                                    "form": {"slug": "sb1", "name": "Baugesuch"},
                                }
                            }
                        ]
                    }
                }
            }
        ),
    )

    instance_state_factory(name=new_instance_state_name)

    ApplicantFactory(instance=instance, user=admin_user, invitee=admin_user)

    response = admin_client.post(reverse("instance-report", args=[instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert len(mail.outbox) == 1

        recipients = mail.outbox[0].recipients()

        assert instance.user.email in recipients
        assert instance_service_construction_control.service.email in recipients


@pytest.mark.parametrize(
    "instance_state__name,expected_status",
    [("sb2", status.HTTP_200_OK), ("new", status.HTTP_403_FORBIDDEN)],
)
@pytest.mark.parametrize("new_instance_state_name", ["conclusion"])
@pytest.mark.parametrize(
    "role_t__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
def test_instance_finalize(
    requests_mock,
    admin_client,
    role,
    instance,
    instance_state_factory,
    instance_service_construction_control,
    expected_status,
    new_instance_state_name,
    notification_template,
    application_settings,
    service,
    admin_user,
    use_caluma_form,
    multilang,
    mock_caluma_forms,
):
    application_settings["NOTIFICATIONS"]["FINALIZE"] = [
        {
            "template_id": notification_template.pk,
            "recipient_types": ["applicant", "construction_control"],
        }
    ]

    requests_mock.post(
        "http://caluma:8000/graphql/",
        text=json.dumps(
            {
                "data": {
                    "allDocuments": {
                        "edges": [
                            {
                                "node": {
                                    "id": "RG9jdW1lbnQ6NjYxOGU5YmQtYjViZi00MTU2LWI0NWMtZTg0M2Y2MTFiZDI2",
                                    "meta": {"camac-instance-id": instance.pk},
                                    "form": {"slug": "sb2", "name": "Baugesuch"},
                                }
                            }
                        ]
                    }
                }
            }
        ),
    )

    instance_state_factory(name=new_instance_state_name)

    ApplicantFactory(instance=instance, user=admin_user, invitee=admin_user)

    response = admin_client.post(reverse("instance-finalize", args=[instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert len(mail.outbox) == 1

        recipients = mail.outbox[0].recipients()

        assert instance.user.email in recipients
        assert instance_service_construction_control.service.email in recipients
