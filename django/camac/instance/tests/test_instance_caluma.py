from pathlib import Path

import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.core import mail
from django.urls import clear_url_caches, reverse
from django.urls.exceptions import NoReverseMatch
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.conftest import CALUMA_FORM_TYPES_SLUGS
from camac.constants import kt_bern as be_constants, kt_uri as ur_constants
from camac.core.models import Chapter, ProposalActivation, Question, QuestionType
from camac.echbern import event_handlers
from camac.echbern.data_preparation import DocumentParser
from camac.echbern.tests.caluma_document_data import baugesuch_data
from camac.instance import urls
from camac.instance.models import Instance
from camac.instance.serializers import (
    SUBMIT_DATE_CHAPTER,
    SUBMIT_DATE_QUESTION_ID,
    WORKFLOW_ITEM_DOSSIEREINGANG_UR,
    CalumaInstanceSerializer,
    CalumaInstanceSubmitSerializer,
)
from camac.user.models import Location
from camac.utils import flatten


@pytest.fixture
def enable_public_urls(application_settings):
    application_settings["ENABLE_PUBLIC_ENDPOINTS"] = True
    urls.enable_public_caluma_instances()
    clear_url_caches()
    yield
    urls.urlpatterns.pop()
    clear_url_caches()


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
def construction_control_for(service_factory):
    def wrapper(service):
        service.trans.update(name="Leitbehörde XY")

        return service_factory(
            trans__name="Baukontrolle XY", service_group__name="construction-control"
        )

    return wrapper


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
@pytest.mark.parametrize("service_group__name", ["municipality"])
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("paper", [False, True])
@pytest.mark.parametrize(
    "copy,modification,extend_validity",
    [(False, False, True), (True, False, False), (True, True, False)],
)
@pytest.mark.parametrize("role__name", ["Municipality", "Coordination"])
def test_create_instance_caluma_be(
    db,
    admin_client,
    instance_state,
    instance_state_factory,
    form,
    mock_nfd_permissions,
    group,
    caluma_workflow_config_be,
    application_settings,
    attachment,
    paper,
    copy,
    modification,
    user_factory,
    extend_validity,
    instance_service_factory,
):
    headers = {}

    if paper:
        application_settings["PAPER"] = {
            "ALLOWED_ROLES": {"DEFAULT": [group.role.pk]},
            "ALLOWED_SERVICE_GROUPS": {"DEFAULT": [group.service.service_group.pk]},
        }
        headers.update({"x-camac-group": group.pk})

    instance_state_factory(name="old")

    application_settings["CALUMA"]["MODIFICATION_ALLOW_FORMS"] = ["main-form"]
    application_settings["ARCHIVE_FORMS"] = [form.pk]

    location = Location.objects.first()
    body = {
        "attributes": {"caluma-form": "main-form"},
        "relationships": {
            "location": {
                "data": {
                    "type": "locations",
                    "id": location.pk,
                },
            },
        },
    }

    data = {"data": {"type": "instances", **body}, "extend_validity_for": 1}

    create_resp = admin_client.post(reverse("instance-list"), data, **headers)

    assert create_resp.status_code == status.HTTP_201_CREATED, create_resp.content

    instance_id = int(create_resp.json()["data"]["id"])
    case = caluma_workflow_models.Case.objects.get(
        **{"meta__camac-instance-id": instance_id}
    )

    assert (
        case.document.answers.filter(
            question_id="is-paper", value="is-paper-yes"
        ).exists()
        == paper
    )

    instance = Instance.objects.get(pk=instance_id)

    # questions for application extension of validity period
    caluma_form_models.Question.objects.create(
        slug="dossiernummer",
        type=caluma_form_models.Question.TYPE_INTEGER,
    )
    QuestionType.objects.create(question_type_id=1, name="Text")
    Question.objects.create(
        question_id=be_constants.QUESTION_EBAU_NR, question_type_id=1
    )
    QuestionType.objects.create(question_type_id=5, name="Radiobox")
    Question.objects.create(
        question_id=be_constants.QUESTION_EBAU_NR_EXISTS, question_type_id=5
    )

    # chapter for application extension of validity period
    Chapter.objects.create(pk=be_constants.INSTANCE_STATE_EBAU_NUMMER_VERGEBEN)

    if extend_validity:
        data["data"]["attributes"].update({"extend-validity-for": str(instance_id)})
        resp = admin_client.post(reverse("instance-list"), data, **headers)

        assert resp.status_code == status.HTTP_201_CREATED, resp.content
        new_instance_id = int(resp.json()["data"]["id"])
        new_instance = Instance.objects.get(pk=new_instance_id)

        new_case = caluma_workflow_models.Case.objects.get(
            **{"meta__camac-instance-id": new_instance_id}
        )
        assert (
            instance.pk
            == [
                answer
                for answer in new_case.document.answers.all()
                if answer.question_id == "dossiernummer"
            ][0].value
        )

    # do a second request including pk, copying the existing instance
    if copy:
        # link attachment to old instance
        attachment.instance_id = instance_id
        attachment.save()

        # assume invitees were created by someone else (bug EBAUBE-2081)
        instance.involved_applicants.update(user_id=user_factory())

        instance_service_factory(
            instance=instance, service=admin_client.user.groups.first().service
        )

        if not modification:
            old_instance = instance
            old_instance.instance_state = instance_state_factory(name="rejected")
            old_instance.save()

        data["data"]["attributes"].update(
            {"copy-source": str(instance_id), "is-modification": modification}
        )

        copy_resp = admin_client.post(reverse("instance-list"), data, **headers)

        assert copy_resp.status_code == status.HTTP_201_CREATED, create_resp.content
        new_instance_id = int(copy_resp.json()["data"]["id"])
        new_instance = Instance.objects.get(pk=new_instance_id)

        new_case = caluma_workflow_models.Case.objects.get(
            **{"meta__camac-instance-id": new_instance_id}
        )

        if modification:
            assert new_instance.attachments.count() == 0
            assert new_case.document.answers.filter(
                question_id="projektaenderung", value="projektaenderung-ja"
            ).exists()
        else:
            new_attachment = new_instance.attachments.first()

            assert attachment.name == new_attachment.name
            assert attachment.uuid != new_attachment.uuid
            assert attachment.path.name != new_attachment.path.name


@pytest.mark.freeze_time("2019-05-02")
@pytest.mark.parametrize("service_group__name", ["municipality"])
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("archive", [False, True])
@pytest.mark.parametrize(
    "copy,modification",
    [(False, False), (True, False), (True, True)],
)
@pytest.mark.parametrize("role__name", ["Municipality", "Coordination"])
def test_create_instance_caluma_ur(
    db,
    admin_client,
    instance_state,
    instance_state_factory,
    form,
    mock_nfd_permissions,
    group,
    caluma_workflow_config_ur,
    application_settings,
    attachment,
    copy,
    archive,
    modification,
    user_factory,
    instance_service_factory,
    mocker,
):
    # Uri states
    instance_state_factory(name="comm")
    instance_state_factory(name="old")
    instance_state_factory(name="ext")

    application_settings["CALUMA"]["MODIFICATION_ALLOW_FORMS"] = ["main-form"]
    if archive:
        application_settings["ARCHIVE_FORMS"] = [form.pk]

    location = Location.objects.first()
    mocker.patch.dict(
        ur_constants.CALUMA_FORM_MAPPING,
        {form.pk: "camac-form"},
    )
    body = {
        "attributes": {"caluma-form": "main-form", "location": location.pk, "lead": 1},
        "relationships": {
            "form": {
                "data": {
                    "type": "forms",
                    "id": form.pk,
                },
            },
            "location": {
                "data": {
                    "type": "locations",
                    "id": location.pk,
                },
            },
        },
    }

    data = {"data": {"type": "instances", **body}}

    create_resp = admin_client.post(reverse("instance-list"), data)

    assert create_resp.status_code == status.HTTP_201_CREATED, create_resp.content

    instance_id = int(create_resp.json()["data"]["id"])
    case = caluma_workflow_models.Case.objects.get(
        **{"meta__camac-instance-id": instance_id}
    )

    instance = Instance.objects.get(pk=instance_id)
    assert instance.location == admin_client.user.groups.first().locations.first()

    assert "dossier-number" in case.meta

    assert instance.instance_state.name == "old" if archive else "new"

    # do a second request including pk, copying the existing instance
    if copy:
        # link attachment to old instance
        attachment.instance_id = instance_id
        attachment.save()

        instance_service_factory(
            instance=instance, service=admin_client.user.groups.first().service
        )

        if not modification:
            old_instance = instance
            old_instance.instance_state = instance_state_factory(name="rejected")
            old_instance.save()

        data["data"]["attributes"].update(
            {"copy-source": str(instance_id), "is-modification": modification}
        )

        if not archive:
            copy_resp = admin_client.post(reverse("instance-list"), data)

            assert copy_resp.status_code == status.HTTP_201_CREATED, create_resp.content
            new_instance_id = int(copy_resp.json()["data"]["id"])
            new_instance = Instance.objects.get(pk=new_instance_id)

            new_case = caluma_workflow_models.Case.objects.get(
                **{"meta__camac-instance-id": new_instance_id}
            )

            if modification:
                assert new_instance.attachments.count() == 0
                assert new_case.document.answers.filter(
                    question_id="projektaenderung", value="projektaenderung-ja"
                ).exists()
            else:
                new_attachment = new_instance.attachments.first()

                assert attachment.name == new_attachment.name
                assert attachment.uuid != new_attachment.uuid
                assert attachment.path.name != new_attachment.path.name


@pytest.mark.parametrize("instance_state__name", ["new"])
def test_copy_without_permission(
    admin_client,
    instance_state,
    caluma_workflow_config_be,
    instance_factory,
    group_factory,
):
    instance = instance_factory(group=group_factory())

    data = {
        "data": {
            "type": "instances",
            "attributes": {
                "copy-source": str(instance.instance_id),
                "caluma-form": "main-form",
            },
        },
    }

    copy_resp = admin_client.post(reverse("instance-list"), data)
    assert copy_resp.status_code == status.HTTP_400_BAD_REQUEST


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


@pytest.mark.parametrize("service_group__name", ["municipality"])
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize("new_instance_state_name", ["subm"])
@pytest.mark.parametrize("has_personalien_sb1", [True, False])
@pytest.mark.parametrize("has_personalien_gesuchstellerin", [True, False])
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
def test_instance_submit_be(
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
    multilang,
    application_settings,
    mock_nfd_permissions,
    mock_generate_and_store_pdf,
    ech_mandatory_answers_einfache_vorabklaerung,
    caluma_workflow_config_be,
    has_personalien_sb1,
    has_personalien_gesuchstellerin,
    caluma_admin_user,
):
    application_settings["NOTIFICATIONS"]["SUBMIT"] = [
        {"template_slug": notification_template.slug, "recipient_types": ["applicant"]}
    ]

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    case.document.answers.create(value=str(service.pk), question_id="gemeinde")

    group_factory(role=role_factory(name="support"))
    mocker.patch.object(
        DocumentParser,
        "parse_answers",
        return_value=ech_mandatory_answers_einfache_vorabklaerung,
    )
    instance_state_factory(name=new_instance_state_name)

    mocker.patch.object(event_handlers, "get_document", return_value=baugesuch_data)

    response = admin_client.post(reverse("instance-submit", args=[instance.pk]))

    assert response.status_code == status.HTTP_200_OK

    assert len(mail.outbox) == 1
    assert instance.user.email in mail.outbox[0].recipients()

    assert mail.outbox[0].subject.startswith("[eBau Test]: ")


@pytest.mark.parametrize("service_group__name", ["municipality"])
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize("new_instance_state_name", ["subm"])
@pytest.mark.parametrize("has_personalien_gesuchstellerin", [True, False])
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
def test_instance_submit_ur(
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
    multilang,
    application_settings,
    mock_nfd_permissions,
    mock_generate_and_store_pdf,
    ech_mandatory_answers_einfache_vorabklaerung,
    caluma_workflow_config_ur,
    has_personalien_gesuchstellerin,
    caluma_admin_user,
    location_factory,
    workflow_item_factory,
):
    application_settings["NOTIFICATIONS"]["SUBMIT"] = [
        {"template_slug": notification_template.slug, "recipient_types": ["applicant"]}
    ]
    application_settings["SET_SUBMIT_DATE_CAMAC_WORKFLOW"] = True
    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False

    workflow_item_factory(workflow_item_id=WORKFLOW_ITEM_DOSSIEREINGANG_UR)

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )
    location = location_factory(location_id="1")

    case.document.answers.create(value=str(location.pk), question_id="municipality")

    group_factory(role=role_factory(name="support"))
    mocker.patch.object(
        DocumentParser,
        "parse_answers",
        return_value=ech_mandatory_answers_einfache_vorabklaerung,
    )
    instance_state_factory(name=new_instance_state_name)

    mocker.patch.object(event_handlers, "get_document", return_value=baugesuch_data)

    response = admin_client.post(reverse("instance-submit", args=[instance.pk]))

    instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK

    assert len(mail.outbox) == 1
    assert instance.user.email in mail.outbox[0].recipients()

    assert mail.outbox[0].subject.startswith("[eBau Test]: ")

    assert instance.instance_state.name == "subm"


@pytest.mark.parametrize("service_group__name", ["municipality"])
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize(
    "is_building_police_procedure,is_extend_validity", [(True, False), (False, True)]
)
def test_instance_submit_state_change_be(
    mocker,
    admin_client,
    role,
    role_factory,
    group_factory,
    instance,
    instance_state_factory,
    service,
    admin_user,
    submit_date_question,
    settings,
    mock_public_status,
    multilang,
    application_settings,
    mock_nfd_permissions,
    mock_generate_and_store_pdf,
    ech_mandatory_answers_einfache_vorabklaerung,
    caluma_workflow_config_be,
    notification_template,
    is_building_police_procedure,
    is_extend_validity,
    caluma_admin_user,
):
    application_settings["NOTIFICATIONS"]["SUBMIT"] = [
        {"template_slug": notification_template.slug, "recipient_types": ["applicant"]}
    ]

    for slug in CALUMA_FORM_TYPES_SLUGS:
        caluma_form_models.Form.objects.create(slug=slug)

    if is_extend_validity:
        form = caluma_form_models.Form.objects.get(pk="verlaengerung-geltungsdauer")

        workflow = caluma_workflow_models.Workflow.objects.get(pk="building-permit")
        workflow.slug = "building-permit"

        instance_state_factory(name="circulation_init")

    if is_building_police_procedure:
        form = caluma_form_models.Form.objects.get(pk="baupolizeiliches-verfahren")

        workflow = caluma_workflow_models.Workflow.objects.get(pk="building-permit")
        workflow.slug = "internal"

        instance_state_factory(name="in_progress_internal")

    workflow.allow_forms.add(form)
    workflow.save()
    case = workflow_api.start_case(
        workflow=workflow,
        form=form,
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    case.document.answers.create(value=str(service.pk), question_id="gemeinde")

    group_factory(role=role_factory(name="support"))
    mocker.patch.object(
        DocumentParser,
        "parse_answers",
        return_value=ech_mandatory_answers_einfache_vorabklaerung,
    )
    instance_state_factory(name="subm")
    mocker.patch.object(event_handlers, "get_document", return_value=baugesuch_data)

    admin_client.post(reverse("instance-submit", args=[instance.pk]))

    instance.refresh_from_db()

    if is_extend_validity:
        assert instance.instance_state.name == "circulation_init"

    if is_building_police_procedure:
        assert instance.instance_state.name == "in_progress_internal"


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
    "role__name,instance__user,service_group__name",
    [("Applicant", LazyFixture("admin_user"), "municipality")],
)
@pytest.mark.parametrize(
    "instance_state__name,expected_status",
    [("sb1", status.HTTP_200_OK), ("new", status.HTTP_403_FORBIDDEN)],
)
def test_instance_report(
    admin_client,
    role,
    instance,
    instance_service,
    service_group,
    instance_state,
    instance_state_factory,
    construction_control_for,
    expected_status,
    notification_template,
    application_settings,
    multilang,
    mock_nfd_permissions,
    mock_generate_and_store_pdf,
    caluma_workflow_config_be,
    docx_decision_factory,
    caluma_admin_user,
):
    instance_state_factory(name="coordination")
    instance_state_factory(name="sb2")

    application_settings["NOTIFICATIONS"]["REPORT"] = [
        {
            "template_slug": notification_template.slug,
            "recipient_types": ["applicant", "construction_control"],
        }
    ]

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    if instance_state.name == "sb1":
        docx_decision_factory(
            decision=be_constants.DECISIONS_BEWILLIGT, instance=instance.pk
        )

        service = instance.responsible_service()
        construction_control = construction_control_for(service)

        for task_id in ["submit", "ebau-number", "skip-circulation", "decision"]:
            workflow_api.complete_work_item(
                work_item=case.work_items.get(task_id=task_id),
                user=caluma_admin_user,
                context={"group-id": service.pk},
            )

    response = admin_client.post(reverse("instance-report", args=[instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert len(mail.outbox) == 2

        recipients = flatten([m.to for m in mail.outbox])

        assert instance.user.email in recipients
        assert construction_control.email in recipients

        case.refresh_from_db()
        assert case.status == "running"
        assert case.work_items.filter(task_id="sb2", status="ready").exists()


@pytest.mark.parametrize(
    "role__name,instance__user,service_group__name",
    [("Applicant", LazyFixture("admin_user"), "municipality")],
)
@pytest.mark.parametrize(
    "instance_state__name,expected_status",
    [("sb2", status.HTTP_200_OK), ("new", status.HTTP_403_FORBIDDEN)],
)
def test_instance_finalize(
    admin_client,
    role,
    instance,
    instance_service,
    service_group,
    instance_state,
    instance_state_factory,
    construction_control_for,
    expected_status,
    notification_template,
    application_settings,
    multilang,
    mock_nfd_permissions,
    mock_generate_and_store_pdf,
    caluma_workflow_config_be,
    docx_decision_factory,
    caluma_admin_user,
):
    instance_state_factory(name="coordination")
    instance_state_factory(name="sb1")
    instance_state_factory(name="conclusion")

    application_settings["NOTIFICATIONS"]["FINALIZE"] = [
        {
            "template_slug": notification_template.slug,
            "recipient_types": ["applicant", "construction_control"],
        }
    ]

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    if instance_state.name == "sb2":
        docx_decision_factory(
            decision=be_constants.DECISIONS_BEWILLIGT, instance=instance.pk
        )

        service = instance.responsible_service()
        construction_control = construction_control_for(service)

        for task_id in [
            "submit",
            "ebau-number",
            "skip-circulation",
            "decision",
            "sb1",
        ]:
            workflow_api.complete_work_item(
                work_item=case.work_items.get(task_id=task_id),
                user=caluma_admin_user,
                context={"group-id": service.pk},
            )

        instance.instance_state = instance_state
        instance.save()

    response = admin_client.post(reverse("instance-finalize", args=[instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert len(mail.outbox) == 2

        recipients = flatten([m.to for m in mail.outbox])

        assert instance.user.email in recipients
        assert construction_control.email in recipients

        assert sorted(
            case.work_items.filter(status="ready").values_list("task_id", flat=True)
        ) == sorted(
            [
                "check-sb1",
                "check-sb2",
                "complete",
                "create-manual-workitems",
                "create-publication",
            ]
        )


@pytest.mark.parametrize("paper", [(True, False)])
@pytest.mark.parametrize("form_slug", [(None), ("nfd")])
def test_generate_and_store_pdf(
    db,
    instance,
    admin_user,
    group,
    attachment_section_factory,
    document_factory,
    mocker,
    form_slug,
    paper,
    application_settings,
    caluma_workflow_config_be,
    caluma_admin_user,
):
    mocker.patch("camac.caluma.api.CalumaApi.is_paper", lambda s, i: paper)

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

    application_settings["DOCUMENT_MERGE_SERVICE"] = {
        "main-form": {"template": "some-template"},
        "nfd": {"template": "some-template"},
    }

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    if form_slug:
        workflow_api.complete_work_item(
            work_item=case.work_items.get(task_id="submit"), user=caluma_admin_user
        )

    serializer._generate_and_store_pdf(instance, form_slug=form_slug)

    assert attachment_section_paper.attachments.count() == 1 if paper else 0
    assert attachment_section_default.attachments.count() == 0 if paper else 1


@pytest.mark.parametrize("role__name", ["Applicant"])
@pytest.mark.parametrize("is_paper,expected_count", [("1", 1), ("0", 2), ("", 3)])
def test_caluma_instance_list_filter(
    admin_client,
    instance_factory,
    is_paper,
    expected_count,
    role,
    admin_user,
    mock_public_status,
    mock_nfd_permissions,
    caluma_workflow_config_be,
    caluma_admin_user,
):
    # not paper instances
    instance_factory(user=admin_user)
    instance_factory(user=admin_user)

    # paper instance
    paper_instance = instance_factory(user=admin_user)
    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": paper_instance.pk},
        user=caluma_admin_user,
    )
    case.document.answers.create(question_id="is-paper", value="is-paper-yes")

    url = reverse("instance-list")
    response = admin_client.get(url, data={"is_paper": is_paper})

    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    assert len(json["data"]) == expected_count


@pytest.mark.parametrize("role__name", ["Applicant"])
@pytest.mark.parametrize(
    "has_pending_billing_entry,expected_count", [("1", 1), ("0", 2), ("", 3)]
)
def test_has_pending_billing_entry_filter(
    admin_user,
    admin_client,
    instance_factory,
    caluma_admin_user,
    billing_entry_factory,
    has_pending_billing_entry,
    expected_count,
    use_caluma_form,
):

    # instances without pending billing entry
    billing_entry_factory(instance=instance_factory(user=admin_user), invoiced=1)
    billing_entry_factory(instance=instance_factory(user=admin_user), invoiced=1)

    # instance with pending billing entry
    instance_with_pending_billing_entry = instance_factory(user=admin_user)
    billing_entry_factory(instance=instance_with_pending_billing_entry, invoiced=0)

    url = reverse("instance-list")
    response = admin_client.get(
        url, data={"has_pending_billing_entry": has_pending_billing_entry}
    )

    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    assert len(json["data"]) == expected_count


@pytest.mark.parametrize("role__name", ["Applicant"])
@pytest.mark.parametrize(
    "has_pending_sanction,expected_count", [("1", 1), ("0", 2), ("", 3)]
)
def test_has_pending_sanction_filter(
    admin_user,
    admin_client,
    instance_factory,
    caluma_admin_user,
    has_pending_sanction,
    expected_count,
    use_caluma_form,
    sanction_factory,
):

    # instances without pending sanction
    sanction_factory(instance=instance_factory(user=admin_user), is_finished=1)
    sanction_factory(instance=instance_factory(user=admin_user), is_finished=1)

    # instance with pending sanction
    instance_with_pending_sanction = instance_factory(user=admin_user)
    sanction_factory(instance=instance_with_pending_sanction, is_finished=0)

    url = reverse("instance-list")
    response = admin_client.get(
        url, data={"has_pending_sanction": has_pending_sanction}
    )

    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "form_slug,has_document_id,expected_status",
    [
        (None, False, status.HTTP_200_OK),
        (None, True, status.HTTP_200_OK),
        ("nfd", False, status.HTTP_200_OK),
        ("something", False, status.HTTP_400_BAD_REQUEST),
    ],
)
@pytest.mark.parametrize("role__name,instance__user", [("Canton", LazyFixture("user"))])
def test_generate_pdf_action(
    db,
    mocker,
    admin_client,
    user,
    group,
    instance,
    caluma_form,
    document_factory,
    form_factory,
    form_slug,
    expected_status,
    application_settings,
    caluma_workflow_config_be,
    caluma_admin_user,
    has_document_id,
):
    content = b"some binary data"

    client = mocker.patch(
        "camac.instance.document_merge_service.DMSClient"
    ).return_value
    client.merge.return_value = content
    mocker.patch("camac.instance.document_merge_service.DMSVisitor.visit")
    context = mocker.patch(
        "camac.instance.serializers.CalumaInstanceSubmitSerializer.context"
    )
    context["request"].user = user
    context["request"].group = group
    mocker.patch("rest_framework.authentication.get_authorization_header")

    application_settings["DOCUMENT_MERGE_SERVICE"] = {
        "main-form": {"template": "some-template"},
        "nfd": {"template": "some-template"},
        "mp-form": {"template": "some-template"},
    }

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    if form_slug:
        workflow_api.complete_work_item(
            work_item=case.work_items.get(task_id="submit"), user=caluma_admin_user
        )

    url = reverse("instance-generate-pdf", args=[instance.pk])
    data = {"form-slug": form_slug} if form_slug else {}

    if has_document_id:
        document_id = document_factory(form__slug="mp-form").pk
        data = {"document-id": document_id}

    response = admin_client.get(url, data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert response.status_code == status.HTTP_200_OK
        assert "X-Sendfile" in response
        with open(response["X-Sendfile"]) as fh:
            assert fh.read() == content.decode("utf-8")


@pytest.mark.freeze_time("2020-03-19")
@pytest.mark.parametrize(
    "role__name,paper", [("Applicant", False), ("Municipality", True)]
)
def test_instance_delete(
    db,
    admin_client,
    admin_user,
    group,
    instance_state,
    instance_state_factory,
    form,
    mock_nfd_permissions,
    caluma_workflow_config_be,
    application_settings,
    attachment,
    paper,
):
    instance_state_factory(name="new")
    instance_state_factory(name="comm")
    # first create instance with all documents
    headers = {}

    if paper:
        application_settings["PAPER"] = {
            "ALLOWED_ROLES": {"DEFAULT": [group.role.pk]},
            "ALLOWED_SERVICE_GROUPS": {"DEFAULT": [group.service.service_group.pk]},
        }
        headers.update({"x-camac-group": group.pk})

    data = {
        "data": {
            "type": "instances",
            "attributes": {"caluma-form": "main-form"},
        }
    }

    create_resp = admin_client.post(reverse("instance-list"), data, **headers)

    instance_id = int(create_resp.json()["data"]["id"])
    instance = Instance.objects.get(pk=instance_id)
    instance.attachments.set([attachment])

    url = reverse("instance-detail", args=[instance_id])
    response = admin_client.get(url, **headers)
    assert response.status_code == status.HTTP_200_OK

    path = Path(attachment.path.path)
    assert path.is_file()

    response = admin_client.delete(url, **headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Instance.objects.filter(pk=instance_id).exists()

    with pytest.raises(attachment.DoesNotExist):
        attachment.refresh_from_db()

    assert not path.is_file()


@pytest.mark.parametrize("service_group__name", ["municipality"])
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize("new_instance_state_name", ["subm"])
@pytest.mark.parametrize(
    "sugg_config,sugg_answer_values,expected_services",
    [
        ([], [], []),
        (
            [("non-existing-question", "foo", [0])],
            [("baubeschrieb", ["baubeschrieb-erweiterung-anbau"])],
            [],
        ),
        (
            [("baubeschrieb", "baubeschrieb-erweiterung-anbau", [1234])],
            [("baubeschrieb", ["baubeschrieb-um-ausbau"])],
            [],
        ),
        (
            [
                ("baubeschrieb", "baubeschrieb-erweiterung-anbau", [1234]),
                ("baubeschrieb", "baubeschrieb-um-ausbau", [5678]),
                ("non-existing-question", "foo", [0]),
            ],
            [("baubeschrieb", ["baubeschrieb-erweiterung-anbau"])],
            [1234],
        ),
        (
            [
                ("baubeschrieb", "baubeschrieb-erweiterung-anbau", [1234]),
                ("art-versickerung-dach", "oberflaechengewaesser", [5678]),
            ],
            [
                ("baubeschrieb", ["baubeschrieb-erweiterung-anbau"]),
                ("art-versickerung-dach", "oberflaechengewaesser"),
            ],
            [1234, 5678],
        ),
        (
            [
                ("baubeschrieb", "baubeschrieb-erweiterung-anbau", [1234, 5678]),
                ("art-versickerung-dach", "some value", [999]),
                ("non-existing-question", "foo", [0]),
            ],
            [
                (
                    "baubeschrieb",
                    ["baubeschrieb-erweiterung-anbau", "baubeschrieb-um-ausbau"],
                ),
                ("art-versickerung-dach", "some value"),
            ],
            [1234, 5678, 999],
        ),
    ],
)
def test_instance_submit_suggestions(
    mocker,
    admin_client,
    role,
    role_factory,
    group_factory,
    instance,
    instance_state_factory,
    service,
    service_factory,
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
    caluma_workflow_config_be,
    circulation_state_factory,
    circulation_type_factory,
    sugg_config,
    sugg_answer_values,
    expected_services,
    caluma_admin_user,
):
    circulation_state_factory(
        circulation_state_id=be_constants.CIRCULATION_STATE_WORKING
    )
    circulation_type_factory(circulation_type_id=be_constants.CIRCULATION_TYPE_STANDARD)
    application_settings["NOTIFICATIONS"]["SUBMIT"] = [
        {"template_slug": notification_template.slug, "recipient_types": ["applicant"]}
    ]

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    case.document.answers.create(value=str(service.pk), question_id="gemeinde")

    if sugg_config:
        application_settings["SUGGESTIONS"] = sugg_config
        for config in sugg_config:
            for service_id in config[2]:
                service_factory(pk=service_id)

        for ans in sugg_answer_values:
            case.document.answers.create(question_id=ans[0], value=ans[1])

    group_factory(role=role_factory(name="support"))
    mocker.patch.object(
        DocumentParser,
        "parse_answers",
        return_value=ech_mandatory_answers_einfache_vorabklaerung,
    )
    instance_state_factory(name=new_instance_state_name)

    mocker.patch.object(event_handlers, "get_document", return_value=baugesuch_data)

    response = admin_client.post(reverse("instance-submit", args=[instance.pk]))

    assert response.status_code == status.HTTP_200_OK

    assert (
        list(ProposalActivation.objects.values_list("service_id", flat=True))
        == expected_services
    )


@pytest.mark.parametrize("service_group__name", ["municipality"])
def test_rejection(
    db,
    admin_client,
    instance_state_factory,
    form,
    service,
    service_group,
    mock_nfd_permissions,
    caluma_workflow_config_be,
    mock_generate_and_store_pdf,
    application_settings,
    ech_mandatory_answers_einfache_vorabklaerung,
    mocker,
    submit_date_question,
):
    application_settings["NOTIFICATIONS"]["SUBMIT"] = []

    new_state = instance_state_factory(name="new")
    subm_state = instance_state_factory(name="subm")
    rejected_state = instance_state_factory(name="rejected")
    finished_state = instance_state_factory(
        name=application_settings["INSTANCE_STATE_REJECTION_COMPLETE"]
    )

    create_response = admin_client.post(
        reverse("instance-list"),
        {"data": {"type": "instances", "attributes": {"caluma-form": "main-form"}}},
    )

    assert (
        create_response.status_code == status.HTTP_201_CREATED
    ), create_response.content

    source_instance_id = int(create_response.json()["data"]["id"])
    source_instance = Instance.objects.get(pk=source_instance_id)
    source_instance.instance_state = rejected_state
    source_instance.save()

    copy_response = admin_client.post(
        reverse("instance-list"),
        {
            "data": {
                "type": "instances",
                "attributes": {
                    "copy-source": str(source_instance_id),
                    "is-modification": False,
                },
            }
        },
    )

    assert copy_response.status_code == status.HTTP_201_CREATED, copy_response.content

    new_instance_id = int(copy_response.json()["data"]["id"])
    new_instance = Instance.objects.get(pk=new_instance_id)

    assert new_instance.instance_state == new_state

    case = caluma_workflow_models.Case.objects.get(
        **{"meta__camac-instance-id": new_instance.pk}
    )

    case.document.answers.create(value=str(service.pk), question_id="gemeinde")
    mocker.patch.object(
        DocumentParser,
        "parse_answers",
        return_value=ech_mandatory_answers_einfache_vorabklaerung,
    )
    mocker.patch.object(event_handlers, "get_document", return_value=baugesuch_data)

    submit_response = admin_client.post(
        reverse("instance-submit", args=[new_instance.pk])
    )

    assert submit_response.status_code == status.HTTP_200_OK

    new_instance.refresh_from_db()
    source_instance.refresh_from_db()

    assert new_instance.instance_state == subm_state
    assert source_instance.instance_state == finished_state


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("is_paper", [True, False])
@pytest.mark.parametrize("is_modification", [True, False])
@pytest.mark.parametrize("is_migrated", [True, False])
def test_instance_name(
    admin_client,
    instance,
    instance_service,
    group,
    role,
    multilang,
    caluma_workflow_config_be,
    is_paper,
    is_modification,
    is_migrated,
    caluma_admin_user,
):
    def yes_no_german(boolean):
        return "ja" if boolean else "nein"

    def yes_no_english(boolean):
        return "yes" if boolean else "no"

    if is_migrated:
        workflow = caluma_workflow_models.Workflow.objects.get(pk="migrated")
        form = caluma_form_models.Form.objects.get(pk="migriertes-dossier")
    else:
        workflow = caluma_workflow_models.Workflow.objects.get(pk="building-permit")
        form = caluma_form_models.Form.objects.get(pk="main-form")

    case = workflow_api.start_case(
        workflow=workflow,
        form=form,
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    if is_migrated:
        case.document.answers.create(
            question_id="geschaeftstyp",
            value="geschaeftstyp-baupolizeiliches-verfahren",
        )
    else:
        case.document.answers.create(
            question_id="is-paper", value=f"is-paper-{yes_no_english(is_paper)}"
        )
        case.document.answers.create(
            question_id="projektaenderung",
            value=f"projektaenderung-{yes_no_german(is_modification)}",
        )

    url = reverse("instance-detail", args=[instance.pk])

    response = admin_client.get(url, data={"fields[instances]": "name"})

    assert response.status_code == status.HTTP_200_OK

    name = response.json()["data"]["attributes"]["name"]

    if is_migrated:
        assert name == "Baupolizeiliches Verfahren (Migriert)"
    else:
        assert "Baugesuch" in name
        if is_paper:
            assert "(Papier)" in name
        if is_modification:
            assert "(Projektänderung)" in name


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_change_responsible_service_audit_validation(
    db,
    admin_client,
    admin_user,
    instance,
    instance_service,
    notification_template,
    role,
    group,
    service_factory,
    user_factory,
    user_group_factory,
    caluma_audit,
    application_settings,
    caluma_admin_user,
):
    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )
    new_service = service_factory()

    for task_id in ["submit", "ebau-number"]:
        workflow_api.complete_work_item(
            work_item=case.work_items.get(task_id=task_id), user=caluma_admin_user
        )

    audit = case.work_items.get(task_id="audit")
    invalid_document = caluma_form_models.Document.objects.create(form_id="fp-form")
    table_answer = audit.document.answers.create(
        question_id="fp-form", value=[str(invalid_document.pk)]
    )
    table_answer.documents.add(invalid_document)

    response = admin_client.post(
        reverse("instance-change-responsible-service", args=[instance.pk]),
        {
            "data": {
                "type": "instance-change-responsible-services",
                "attributes": {"service-type": "municipality"},
                "relationships": {
                    "to": {"data": {"id": new_service.pk, "type": "services"}}
                },
            }
        },
    )

    result = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert len(result["errors"])
    assert "Invalid audit" == result["errors"][0]["detail"]


@pytest.mark.parametrize("service_group__name", ["municipality"])
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize(
    "role__name,expected_status,error",
    [
        ("Municipality", status.HTTP_201_CREATED, None),
        (
            "Applicant",
            status.HTTP_400_BAD_REQUEST,
            "The form 'main-form' can only be used by an internal role",
        ),
    ],
)
def test_create_instance_caluma_internal_forms(
    db,
    admin_client,
    instance_state,
    instance_state_factory,
    form,
    role,
    mock_nfd_permissions,
    group,
    caluma_workflow_config_be,
    application_settings,
    expected_status,
    error,
):
    application_settings["CALUMA"]["INTERNAL_FORMS"] = ["main-form"]

    if role.name == "Municipality":
        application_settings["PAPER"] = {
            "ALLOWED_ROLES": {"DEFAULT": [group.role.pk]},
            "ALLOWED_SERVICE_GROUPS": {"DEFAULT": [group.service.service_group.pk]},
        }
        headers = {"x-camac-group": group.pk}
    else:
        headers = {}

    response = admin_client.post(
        reverse("instance-list"),
        {"data": {"type": "instances", "attributes": {"caluma-form": "main-form"}}},
        **headers,
    )

    assert response.status_code == expected_status

    if error:
        assert error in response.json()["errors"][0]["detail"]


@pytest.mark.parametrize("role__name", ["Applicant"])
@pytest.mark.parametrize(
    "caluma_form,expected_status",
    [
        ("verlaerungerung-geltungsdauer", status.HTTP_400_BAD_REQUEST),
        ("baugesuch", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_create_instance_caluma_modification(
    db,
    admin_client,
    instance_state,
    instance_state_factory,
    role,
    form,
    mock_nfd_permissions,
    caluma_workflow_config_be,
    application_settings,
    caluma_form,
    expected_status,
):
    instance_state_factory(name="new")

    workflow = caluma_workflow_models.Workflow.objects.get(pk="building-permit")
    workflow.allow_forms.add(
        caluma_form_models.Form.objects.create(slug="baugesuch"),
        caluma_form_models.Form.objects.create(slug="verlaerungerung-geltungsdauer"),
    )

    application_settings["CALUMA"]["MODIFICATION_ALLOW_FORMS"] = ["baugesuch"]
    application_settings["CALUMA"]["MODIFICATION_DISALLOW_STATES"] = ["new"]

    create_response = admin_client.post(
        reverse("instance-list"),
        {
            "data": {
                "type": "instances",
                "attributes": {
                    "caluma_form": caluma_form,
                },
            }
        },
    )
    instance_id = create_response.json()["data"]["id"]

    response = admin_client.post(
        reverse("instance-list"),
        {
            "data": {
                "type": "instances",
                "attributes": {
                    "copy-source": str(instance_id),
                    "is-modification": True,
                },
            }
        },
    )

    assert response.status_code == expected_status
    assert "Projektänderung nicht erlaubt" in response.json()["errors"][0]["detail"]


@pytest.mark.parametrize("with_client", ["public", "admin"])
def test_public_caluma_instance_enabled_empty_qs(
    db,
    client,
    admin_client,
    application_settings,
    instance_factory,
    with_client,
    enable_public_urls,
):
    instance_factory.create_batch(5)
    url = reverse("public-caluma-instance")
    if with_client == "public":
        resp = client.get(url)
    else:
        resp = admin_client.get(url)

    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()["data"]) == 0


def test_public_caluma_instance_disabled():
    with pytest.raises(NoReverseMatch):
        reverse("public-caluma-instance")
