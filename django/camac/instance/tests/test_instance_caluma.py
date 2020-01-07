import pytest
from caluma.caluma_form import models as caluma_form_models
from django.core import mail
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.core.models import Chapter, Question, QuestionType
from camac.echbern import data_preparation
from camac.echbern.data_preparation import DocumentParser
from camac.echbern.tests.caluma_responses import full_document
from camac.instance.serializers import (
    SUBMIT_DATE_CHAPTER,
    SUBMIT_DATE_QUESTION_ID,
    CalumaInstanceSerializer,
    CalumaInstanceSubmitSerializer,
)
from camac.utils import flatten

MAIN_FORMS = [
    "baugesuch",
    "baugesuch-generell",
    "baugesuch-mit-uvp",
    "vorabklaerung-einfach",
    "vorabklaerung-vollstaendig",
]


@pytest.fixture
def caluma_forms():
    # forms
    caluma_form_models.Form.objects.create(
        slug="main-form", meta={"is-main-form": True}
    )
    caluma_form_models.Form.objects.create(slug="sb1")
    caluma_form_models.Form.objects.create(slug="sb2")
    caluma_form_models.Form.objects.create(slug="nfd")

    # questions
    caluma_form_models.Question.objects.create(slug="gemeinde")
    caluma_form_models.Question.objects.create(slug="papierdossier")

    # link questions with forms
    caluma_form_models.FormQuestion.objects.create(
        form_id="main-form", question_id="gemeinde"
    )
    caluma_form_models.FormQuestion.objects.create(
        form_id="main-form", question_id="papierdossier"
    )
    caluma_form_models.FormQuestion.objects.create(
        form_id="sb1", question_id="papierdossier"
    )
    caluma_form_models.FormQuestion.objects.create(
        form_id="sb2", question_id="papierdossier"
    )
    caluma_form_models.FormQuestion.objects.create(
        form_id="nfd", question_id="papierdossier"
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


@pytest.fixture
def mock_nfd_permissions(mocker):
    mocker.patch(
        "camac.instance.serializers.CalumaInstanceSerializer._get_nfd_form_permissions",
        lambda s, i: [],
    )


@pytest.fixture
def mock_generate_and_store_pdf(mocker):
    mocker.patch(
        "camac.instance.serializers.CalumaInstanceSubmitSerializer._generate_and_store_pdf"
    )


@pytest.mark.freeze_time("2019-05-02")
@pytest.mark.parametrize("paper,instance_state__name", [(True, "new"), (False, "new")])
def test_create_instance(
    db,
    admin_client,
    instance_state,
    form,
    use_caluma_form,
    mock_nfd_permissions,
    paper,
    group,
    caluma_forms,
    application_settings,
):
    headers = {}

    if paper:
        application_settings["PAPER"] = {
            "ALLOWED_ROLES": {"DEFAULT": [group.role.pk]},
            "ALLOWED_SERVICE_GROUPS": {"DEFAULT": [group.service.service_group.pk]},
        }
        headers.update({"x-camac-group": group.pk})

    create_resp = admin_client.post(
        reverse("instance-list"),
        {
            "data": {
                "type": "instances",
                "attributes": {"caluma-form": "main-form"},
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
        **headers,
    )

    assert create_resp.status_code == status.HTTP_201_CREATED, create_resp.content

    instance_id = int(create_resp.json()["data"]["id"])
    documents = caluma_form_models.Document.objects.filter(
        **{"meta__camac-instance-id": instance_id}
    )

    assert set([doc.form_id for doc in documents]) == set(
        ["main-form", "sb1", "sb2", "nfd"]
    )

    if paper:
        for doc in documents:
            assert doc.answers.filter(
                question_id="papierdossier", value="papierdossier-ja"
            ).exists()


@pytest.mark.parametrize(
    "instance_state__name,instance__creation_date",
    [("new", "2018-04-17T09:31:56+02:00")],
)
@pytest.mark.parametrize(
    "role__name,instance__user,editable",
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
    instance_service,
    responsible_service,
    mock_nfd_permissions,
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


@pytest.mark.parametrize("instance_state__name", ["new", "rejected"])
@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
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
    mocker,
    admin_client,
    role,
    role_factory,
    group_factory,
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
    mock_nfd_permissions,
    mock_generate_and_store_pdf,
    ech_mandatory_answers_einfache_vorabklaerung,
    requests_mock,
    caluma_forms,
):

    application_settings["NOTIFICATIONS"]["SUBMIT"] = [
        {"template_id": notification_template.pk, "recipient_types": ["applicant"]}
    ]

    document = caluma_form_models.Document.objects.create(
        form_id="main-form", meta={"camac-instance-id": instance.pk}
    )
    caluma_form_models.Answer.objects.create(
        document=document, value=service.pk, question_id="gemeinde"
    )

    group_factory(role=role_factory(name="support"))
    mocker.patch.object(
        DocumentParser,
        "parse_answers",
        return_value=ech_mandatory_answers_einfache_vorabklaerung,
    )
    mocker.patch.object(data_preparation, "get_admin_token", return_value="token")

    instance_state_factory(name=new_instance_state_name)

    requests_mock.post("http://caluma:8000/graphql/", json=full_document)
    mocker.patch.object(data_preparation, "get_admin_token", return_value="token")

    response = admin_client.post(reverse("instance-submit", args=[instance.pk]))

    assert response.status_code == status.HTTP_200_OK

    assert len(mail.outbox) == 1
    assert instance.user.email in mail.outbox[0].recipients()

    assert mail.outbox[0].subject.startswith("[eBau Test]: ")


@pytest.mark.parametrize("role__name,instance__user", [("Canton", LazyFixture("user"))])
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
    "instance_state__name,document_validity,expected_status",
    [
        ("sb1", True, status.HTTP_200_OK),
        ("new", True, status.HTTP_403_FORBIDDEN),
        # ("sb1", False, status.HTTP_400_BAD_REQUEST), TODO: reenable this when caluma document validity is fixed
    ],
)
@pytest.mark.parametrize("new_instance_state_name", ["sb2"])
@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
def test_instance_report(
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
    mock_nfd_permissions,
    mock_generate_and_store_pdf,
    document_validity,
    caluma_forms,
):
    application_settings["NOTIFICATIONS"]["REPORT"] = [
        {
            "template_id": notification_template.pk,
            "recipient_types": ["applicant", "construction_control"],
        }
    ]

    caluma_form_models.Document.objects.create(
        form_id="sb1", meta={"camac-instance-id": instance.pk}
    )

    instance_state_factory(name=new_instance_state_name)

    response = admin_client.post(reverse("instance-report", args=[instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert len(mail.outbox) == 2

        recipients = flatten([m.to for m in mail.outbox])

        assert instance.user.email in recipients
        assert instance_service_construction_control.service.email in recipients


@pytest.mark.parametrize(
    "instance_state__name,expected_status",
    [("sb2", status.HTTP_200_OK), ("new", status.HTTP_403_FORBIDDEN)],
)
@pytest.mark.parametrize("new_instance_state_name", ["conclusion"])
@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
def test_instance_finalize(
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
    mock_nfd_permissions,
    mock_generate_and_store_pdf,
    caluma_forms,
):
    application_settings["NOTIFICATIONS"]["FINALIZE"] = [
        {
            "template_id": notification_template.pk,
            "recipient_types": ["applicant", "construction_control"],
        }
    ]

    caluma_form_models.Document.objects.create(
        form_id="sb2", meta={"camac-instance-id": instance.pk}
    )

    instance_state_factory(name=new_instance_state_name)

    response = admin_client.post(reverse("instance-finalize", args=[instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert len(mail.outbox) == 2

        recipients = flatten([m.to for m in mail.outbox])

        assert instance.user.email in recipients
        assert instance_service_construction_control.service.email in recipients


@pytest.mark.parametrize("paper", [(True, False)])
@pytest.mark.parametrize(
    "has_template,matching_documents,raise_error,form_slug",
    [
        (False, 1, True, None),
        (False, 0, True, None),
        (False, 2, True, None),
        (True, 1, False, None),
        (True, 1, False, "some-form"),
        (True, 1, True, "some-other-form"),
    ],
)
def test_generate_and_store_pdf(
    db,
    instance,
    admin_user,
    group,
    attachment_section_factory,
    document_factory,
    mocker,
    has_template,
    matching_documents,
    raise_error,
    form_slug,
    paper,
    application_settings,
):
    mocker.patch("camac.caluma.CalumaApi.is_paper", lambda s, i: paper)

    attachment_section_default = attachment_section_factory()
    attachment_section_paper = attachment_section_factory()

    application_settings["PDF"] = {
        "SECTION": {
            form_slug.upper()
            if form_slug
            else "MAIN": {
                "DEFAULT": attachment_section_default.pk,
                "PAPER": attachment_section_paper.pk,
            }
        }
    }

    client = mocker.patch(
        "camac.instance.document_merge_service.DMSClient"
    ).return_value
    client.merge.return_value = b"some binary data"
    mocker.patch("camac.instance.document_merge_service.DMSVisitor.visit")
    context = mocker.patch(
        "camac.instance.serializers.CalumaInstanceSubmitSerializer.context"
    )
    context["request"].user = admin_user
    context["request"].group = group
    mocker.patch("rest_framework.authentication.get_authorization_header")

    serializer = CalumaInstanceSubmitSerializer()

    form = caluma_form_models.Form.objects.create(slug="some-form", meta={})
    if not form_slug:
        form.meta["is-main-form"] = True
    if has_template:
        form.meta["template"] = "some-template"

    form.save()

    for _ in range(matching_documents):
        document = document_factory(form=form)
        document.meta = {"camac-instance-id": instance.pk}
        document.save()

    if raise_error:
        with pytest.raises(Exception):
            serializer._generate_and_store_pdf(instance, form_slug=form_slug)
        return

    serializer._generate_and_store_pdf(instance, form_slug=form_slug)

    assert attachment_section_paper.attachments.count() == 1 if paper else 0
    assert attachment_section_default.attachments.count() == 0 if paper else 1
