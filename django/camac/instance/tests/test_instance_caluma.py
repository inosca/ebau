import itertools
from datetime import date, datetime
from pathlib import Path

import pytest
from alexandria.core.factories import CategoryFactory, MarkFactory
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_form.api import save_answer
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.core import mail
from django.urls import reverse
from django.utils.timezone import make_aware
from mock import call
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.applicants.models import ROLE_CHOICES
from camac.caluma.api import CalumaApi
from camac.conftest import CALUMA_FORM_TYPES_SLUGS
from camac.constants import (
    kt_bern as be_constants,
    kt_uri as ur_constants,
    kt_uri as uri_constants,
)
from camac.core.models import Chapter, Question, QuestionType
from camac.instance.models import Instance
from camac.instance.serializers import (
    SUBMIT_DATE_CHAPTER,
    SUBMIT_DATE_FORMAT,
    SUBMIT_DATE_QUESTION_ID,
    CalumaInstanceSerializer,
    CalumaInstanceSubmitSerializer,
)
from camac.permissions import api as permissions_api
from camac.permissions.conditions import (
    HasApplicantRole,
)
from camac.permissions.switcher import PERMISSION_MODE
from camac.user.models import Location, Service
from camac.utils import flatten


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
@pytest.mark.parametrize("convert_to_building_permit", [False, True])
@pytest.mark.parametrize("role__name", ["Municipality"])
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
    convert_to_building_permit,
    project_modification_settings,
):
    headers = {}

    if paper:
        application_settings["PAPER"] = {
            "ALLOWED_ROLES": {"DEFAULT": [group.role.pk]},
            "ALLOWED_SERVICE_GROUPS": {"DEFAULT": [group.service.service_group.pk]},
        }
        headers.update({"x-camac-group": group.pk})

    instance_state_factory(name="old")

    project_modification_settings["ALLOW_FORMS"] = ["main-form"]

    location = Location.objects.first()
    body = {
        "attributes": {"caluma-form": "main-form"},
        "relationships": {
            "location": {"data": {"type": "locations", "id": location.pk}}
        },
    }

    data = {"data": {"type": "instances", **body}, "extend_validity_for": 1}

    create_resp = admin_client.post(reverse("instance-list"), data, **headers)

    assert create_resp.status_code == status.HTTP_201_CREATED, create_resp.content

    instance_id = int(create_resp.json()["data"]["id"])
    case = caluma_workflow_models.Case.objects.get(instance__pk=instance_id)

    assert (
        case.document.answers.filter(
            question_id="is-paper", value="is-paper-yes"
        ).exists()
        == paper
    )

    instance = Instance.objects.get(pk=instance_id)

    # questions for application extension of validity period
    caluma_form_models.Question.objects.create(
        slug="dossiernummer", type=caluma_form_models.Question.TYPE_INTEGER
    )
    QuestionType.objects.create(question_type_id=1, name="Text")

    # chapter for application extension of validity period
    Chapter.objects.create(pk=be_constants.INSTANCE_STATE_EBAU_NUMMER_VERGEBEN)

    if extend_validity:
        data["data"]["attributes"].update({"extend-validity-for": str(instance_id)})
        resp = admin_client.post(reverse("instance-list"), data, **headers)

        assert resp.status_code == status.HTTP_201_CREATED, resp.content
        new_instance_id = int(resp.json()["data"]["id"])
        new_instance = Instance.objects.get(pk=new_instance_id)

        new_case = caluma_workflow_models.Case.objects.get(instance__pk=new_instance_id)
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
        # convert vollstaendige vorabklaerung to building permit
        if convert_to_building_permit:
            instance.case.document.form = caluma_form_models.Form.objects.create(
                pk="vorabklaerung-vollstaendig-v3"
            )
            instance.case.document.save()

        # link attachment to old instance
        attachment.instance_id = instance_id
        attachment.save()

        # assume invitees were created by someone else (bug EBAUBE-2081)
        instance.involved_applicants.update(user_id=user_factory())

        instance_service_factory(
            instance=instance, service=admin_client.user.groups.first().service
        )

        old_instance = instance
        old_instance.instance_state = instance_state_factory(
            name="subm" if modification else "rejected"
        )
        old_instance.save()

        data["data"]["attributes"].update(
            {"copy-source": str(instance_id), "is-modification": modification}
        )

        copy_resp = admin_client.post(reverse("instance-list"), data, **headers)

        assert copy_resp.status_code == status.HTTP_201_CREATED, create_resp.content
        new_instance_id = int(copy_resp.json()["data"]["id"])
        new_instance = Instance.objects.get(pk=new_instance_id)

        new_case = caluma_workflow_models.Case.objects.get(instance__pk=new_instance_id)

        if modification:
            assert new_instance.attachments.count() == instance.attachments.count()
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
@pytest.mark.parametrize("archive", [False, True])
@pytest.mark.parametrize("paper", [False, True])
@pytest.mark.parametrize(
    "copy,modification,generate_identifier",
    [
        (False, False, False),
        (True, False, False),
        (True, True, False),
        (True, False, True),
    ],
)
@pytest.mark.parametrize("role__name", ["Municipality", "Coordination"])
def test_create_instance_caluma_ur(  # noqa: C901
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
    generate_identifier,
    user_factory,
    instance_service_factory,
    mocker,
    workflow_item_factory,
    authority_factory,
    settings,
    paper,
    project_modification_settings,
):
    headers = {}

    if paper:
        application_settings["PAPER"] = {
            "ALLOWED_ROLES": {"DEFAULT": [group.role.pk]},
            "ALLOWED_SERVICE_GROUPS": {"DEFAULT": [group.service.service_group.pk]},
        }
        headers.update({"x-camac-group": group.pk})

    settings.APPLICATION_NAME = "kt_uri"
    # Uri states
    state_comm = instance_state_factory(name="comm")
    instance_state_factory(name="old")
    instance_state_factory(name="ext")
    instance_state_factory(name="new")

    project_modification_settings["ALLOW_FORMS"] = ["main-form"]
    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False
    application_settings["SET_SUBMIT_DATE_CAMAC_WORKFLOW"] = True

    role = admin_client.user.groups.first().role
    if role.name == "Municipality":
        mocker.patch("camac.constants.kt_uri.ROLE_MUNICIPALITY", role.pk)
    elif role.name == "Coordination":
        mocker.patch("camac.constants.kt_uri.ROLE_KOOR_NP", role.pk)

    authority_factory(name="Foo")

    workflow_item_factory(workflow_item_id=ur_constants.WORKFLOW_ITEM_DOSSIER_ERFASST)

    if archive:
        application_settings["ARCHIVE_FORMS"] = [form.pk]

    location = Location.objects.first()
    mocker.patch.dict(ur_constants.CALUMA_FORM_MAPPING, {form.pk: "camac-form"})
    body = {
        "attributes": {"caluma-form": "main-form", "location": location.pk, "lead": 1},
        "relationships": {
            "form": {"data": {"type": "forms", "id": form.pk}},
            "location": {"data": {"type": "locations", "id": location.pk}},
        },
    }

    data = {"data": {"type": "instances", **body}}

    create_resp = admin_client.post(reverse("instance-list"), data)

    assert create_resp.status_code == status.HTTP_201_CREATED, create_resp.content

    instance_id = int(create_resp.json()["data"]["id"])
    case = caluma_workflow_models.Case.objects.get(instance__pk=instance_id)

    instance = Instance.objects.get(pk=instance_id)
    assert instance.location == admin_client.user.groups.first().locations.first()

    assert (
        case.document.answers.filter(
            question_id="is-paper", value="is-paper-yes"
        ).exists()
        == paper
    )

    assert instance.instance_state.name == "old" if archive else "new"

    # do a second request including pk, copying the existing instance
    if copy:
        # link attachment to old instance
        attachment.instance_id = instance_id
        attachment.save()

        instance_service_factory(
            instance=instance, service=admin_client.user.groups.first().service
        )

        old_instance = instance
        old_instance.instance_state = (
            state_comm if modification else instance_state_factory(name="rejected")
        )
        old_instance.save()

        data["data"]["attributes"].update(
            {
                "copy-source": str(instance_id),
                "is-modification": modification,
                "generate_identifier": generate_identifier,
            }
        )

        if not archive:
            copy_resp = admin_client.post(reverse("instance-list"), data, **headers)

            assert copy_resp.status_code == status.HTTP_201_CREATED, create_resp.content
            new_instance_id = int(copy_resp.json()["data"]["id"])
            new_instance = Instance.objects.get(pk=new_instance_id)

            new_case = caluma_workflow_models.Case.objects.get(
                instance__pk=new_instance_id
            )

            if modification:
                assert new_instance.attachments.count() == instance.attachments.count()
                assert new_case.document.answers.filter(
                    question_id="projektaenderung", value="projektaenderung-ja"
                ).exists()
            else:
                new_attachment = new_instance.attachments.first()

                assert attachment.name == new_attachment.name
                assert attachment.uuid != new_attachment.uuid
                assert attachment.path.name != new_attachment.path.name
                assert new_instance.instance_state.name == "new"

            assert ("dossier-number" in new_case.meta) == generate_identifier


@pytest.mark.parametrize("service_group__name", ["municipality"])
@pytest.mark.parametrize("role__name", ["Municipality"])
def test_create_instance_caluma_ur_wrong_location(
    db,
    admin_client,
    instance_state_factory,
    form,
    location_factory,
    caluma_workflow_config_ur,
):
    instance_state_factory(name="comm")
    instance_state_factory(name="new")

    location = location_factory()

    body = {
        "attributes": {"caluma-form": "main-form", "location": location.pk, "lead": 1},
        "relationships": {
            "form": {"data": {"type": "forms", "id": form.pk}},
            "location": {"data": {"type": "locations", "id": location.pk}},
        },
    }

    data = {"data": {"type": "instances", **body}}

    resp = admin_client.post(reverse("instance-list"), data)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        resp.json()["errors"][0]["detail"]
        == "Provided location is not present in group locations"
    )


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
        }
    }

    copy_resp = admin_client.post(reverse("instance-list"), data)
    assert copy_resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize("instance_state__name", ["new"])
def test_create_identifier_without_permisssion(
    admin_client,
    instance_state,
    caluma_workflow_config_ur,
    instance_factory,
    group_factory,
):
    instance = instance_factory(group=group_factory())

    data = {
        "data": {
            "type": "instances",
            "attributes": {
                "copy-source": str(instance.instance_id),
                "generate-identifier": True,
            },
        }
    }

    copy_resp = admin_client.post(reverse("instance-list"), data)
    assert copy_resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.freeze_time("2018-04-17")
@pytest.mark.parametrize(
    "instance_state__name",
    ["new"],
)
@pytest.mark.parametrize(
    "role__name,instance__user,editable",
    [
        ("Service", lf("user"), {"form", "document"}),
        ("Canton", lf("user"), {"form", "document"}),
    ],
)
def test_instance_list(
    admin_client,
    be_instance,
    active_inquiry_factory,
    editable,
    mock_public_status,
    multilang,
    mock_nfd_permissions,
):
    active_inquiry_factory(be_instance)

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
    assert json["data"][0]["id"] == str(be_instance.pk)
    assert set(json["data"][0]["meta"]["editable"]) == set(editable)


@pytest.mark.parametrize("service_group__name", ["municipality"])
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
@pytest.mark.parametrize("has_personalien_sb1", [True, False])
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
    """,
    ],
)
def test_instance_submit_be(
    set_application_be,
    admin_client,
    role,
    role_factory,
    group_factory,
    be_instance,
    instance_state_factory,
    service,
    admin_user,
    notification_template,
    submit_date_question,
    settings,
    mock_public_status,
    multilang,
    application_settings,
    mock_nfd_permissions,
    mock_generate_and_store_pdf,
    caluma_workflow_config_be,
    has_personalien_sb1,
    caluma_admin_user,
    disable_ech0211_settings,
):
    application_settings["NOTIFICATIONS"]["SUBMIT"] = [
        {"template_slug": notification_template.slug, "recipient_types": ["applicant"]}
    ]

    be_instance.case.document.answers.create(
        value=str(service.pk), question_id="gemeinde"
    )

    group_factory(role=role_factory(name="support"))
    instance_state_factory(name="subm")

    response = admin_client.post(reverse("instance-submit", args=[be_instance.pk]))

    assert response.status_code == status.HTTP_200_OK

    assert len(mail.outbox) == 1
    assert be_instance.user.email in mail.outbox[0].recipients()

    assert mail.outbox[0].subject.startswith("[eBau Test]: ")


@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "role__name,service_group__name,form_slug,special_case",
    [
        ("Municipality", "municipality", "main-form", {"special_location": True}),
        ("Applicant", None, "main-form", {}),
        ("Municipality", "municipality", "main-form", {}),
        (
            "Municipality",
            "municipality",
            "oereb-verfahren-gemeinde",
            {"special_location": True},
        ),
        ("Coordination", "coordination", "oereb", {}),
        ("Coordination", "coordination", "oereb", {"custom_leitbehoerde": True}),
        ("Coordination", "coordination", "oereb", {"special_location": True}),
        ("Coordination", "coordination", "oereb", {"is_federal": True}),
    ],
)
def test_instance_submit_ur(
    mocker,
    admin_client,
    role,
    role_factory,
    group_factory,
    ur_instance,
    instance_state_factory,
    instance_service_factory,
    service,
    admin_user,
    notification_template,
    submit_date_question,
    settings,
    mock_public_status,
    multilang,
    application_settings,
    mock_nfd_permissions,
    mock_generate_and_store_pdf,
    caluma_workflow_config_ur,
    caluma_admin_user,
    location_factory,
    workflow_item_factory,
    authority_location_factory,
    authority,
    form_slug,
    special_case,
    disable_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_uri"
    application_settings["NOTIFICATIONS"]["SUBMIT"] = [
        {"template_slug": notification_template.slug, "recipient_types": ["applicant"]}
    ]
    application_settings["SET_SUBMIT_DATE_CAMAC_WORKFLOW"] = True
    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False
    application_settings["PAPER"]["ALLOWED_SERVICE_GROUPS"]["DEFAULT"] = [
        ur_instance.group.service.service_group_id
    ]
    application_settings["PAPER"]["ALLOWED_ROLES"]["DEFAULT"] = [
        ur_instance.group.role.pk
    ]

    mocker.patch.object(
        uri_constants,
        "BUNDESSTELLE_SERVICE_ID",
        (
            ur_instance.group.service_id
            if special_case.get("is_federal")
            else ur_instance.group.service_id + 1
        ),
    )

    if form_slug != "main-form":
        ur_instance.case.document.form_id = form_slug
        ur_instance.case.document.save()

    instance_state_factory(name="ext")
    instance_state_factory(name="comm")

    instance_service_factory(
        active=1, instance=ur_instance, service=ur_instance.group.service
    )

    workflow_item_factory(workflow_item_id=ur_constants.WORKFLOW_ITEM_DOSSIER_ERFASST)

    location = location_factory(
        communal_federal_number=(
            "1222" if special_case.get("special_location") else "1224"
        )
    )

    ur_instance.case.document.answers.create(
        value=str(location.communal_federal_number), question_id="municipality"
    )
    if special_case.get("special_location"):
        authority_location = authority_location_factory(
            location=admin_user.groups.first().locations.first()
        )
    else:
        authority_location = authority_location_factory(location=location)

    if special_case.get("custom_leitbehoerde"):
        dynamic_option = caluma_form_models.DynamicOption.objects.create(
            document=ur_instance.case.document,
            question_id="leitbehoerde-internal-form",
            slug=str(authority_location.authority.pk),
            label="Musterdorf",
        )

        ur_instance.case.document.answers.create(
            value=dynamic_option.slug,
            question_id="leitbehoerde-internal-form",
        )

    if ur_instance.group.role.name in ["Municipality", "Coordination"]:
        ur_instance.case.document.answers.create(
            question_id="is-paper", value="is-paper-yes"
        )

    group_factory(role=role_factory(name="support"))
    instance_state_factory(name="subm")

    response = admin_client.post(reverse("instance-submit", args=[ur_instance.pk]))

    ur_instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK

    assert len(mail.outbox) == 1
    assert ur_instance.user.email in mail.outbox[0].recipients()

    assert mail.outbox[0].subject.startswith("[eBau Test]: ")

    found_authority = (
        ur_instance.case.document.answers.filter(question_id="leitbehoerde")
        .first()
        .value
    )

    if special_case.get("custom_leitbehoerde"):
        assert int(found_authority) == int(authority_location.authority.pk)
    elif special_case.get("special_location") and "oereb" in form_slug:
        # this is a special "diverse gemeinden" or "alle gemeinden" dossier
        # this is therefore an ÖREB dossier and in this case the leitbehörde
        # is the KOOR NP
        assert int(found_authority) == int(ur_constants.KOOR_NP_AUTHORITY_ID)
    else:
        assert int(found_authority) == int(authority_location.authority.pk)

    if ur_instance.group.role.name == "Coordination":
        assert ur_instance.instance_state.name == (
            "comm" if special_case.get("is_federal") else "ext"
        )
    elif ur_instance.group.role.name == "Municipality":
        assert ur_instance.instance_state.name == "comm"
    else:
        assert ur_instance.instance_state.name == "subm"


@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("instance__user", [lf("admin_user")])
def test_instance_submit_ur_without_camac_form_id(
    admin_client,
    ur_instance,
    settings,
    caluma_workflow_config_ur,
    instance_state_factory,
    authority_location_factory,
):
    settings.APPLICATION_NAME = "kt_uri"
    instance_state_factory(name="subm")

    ur_instance.case.document.answers.create(
        value=str(ur_instance.group.locations.first().communal_federal_number),
        question_id="municipality",
    )
    authority_location_factory(location=ur_instance.group.locations.first())

    form = caluma_form_factories.FormFactory()
    ur_instance.case.document.form = form
    ur_instance.case.document.form.save()

    data = {
        "data": {
            "type": "instances",
            "attributes": {"caluma-form": ur_instance.case.document.form.slug},
        }
    }

    response = admin_client.post(
        reverse("instance-submit", args=[ur_instance.pk]), data
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize("service_group__name", ["coordination"])
@pytest.mark.parametrize("submit_to", ["KOOR_BD", "KOOR_SD"])
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_instance_submit_cantonal_territory_usage_ur(
    mocker,
    admin_client,
    settings,
    ur_instance,
    notification_template,
    application_settings,
    mock_generate_and_store_pdf,
    location_factory,
    group_factory,
    instance_state_factory,
    submit_to,
    service_factory,
    authority_location_factory,
    caluma_workflow_config_ur,
    disable_ech0211_settings,
    ur_master_data_case,
):
    settings.APPLICATION_NAME = "kt_uri"

    caluma_form_factories.FormFactory(slug="personalien")
    ur_instance.case.document.form_id = "cantonal-territory-usage"
    ur_instance.case.document.save()

    koor_service = service_factory(email=f"{submit_to}@example.com")
    mocker.patch(f"camac.constants.kt_uri.{submit_to}_SERVICE_ID", koor_service.pk)
    koor_group = group_factory(service=koor_service)
    mocker.patch(f"camac.constants.kt_uri.{submit_to}_GROUP_ID", koor_group.pk)
    mocker.patch("camac.constants.kt_uri.KOOR_GROUP_IDS", [koor_group.pk])
    koor_email = koor_group.service.email

    veranstaltung = "umzug" if submit_to == "KOOR_BD" else "sportanlass"
    ur_instance.case.document.answers.get(question_id="veranstaltung-art").delete()
    ur_instance.case.document.answers.create(
        value=f"veranstaltung-art-{veranstaltung}", question_id="veranstaltung-art"
    )

    application_settings["NOTIFICATIONS"] = {
        "SUBMIT_KOOR": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["municipality"],
            },
        ],
    }
    application_settings["SET_SUBMIT_DATE_CAMAC_WORKFLOW"] = True
    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False

    location = location_factory(communal_federal_number="1")

    authority_location_factory(location=location)

    instance_state_factory(name="ext")
    instance_state_factory(name="subm")

    response = admin_client.post(reverse("instance-submit", args=[ur_instance.pk]))

    ur_instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK

    assert len(mail.outbox) == 1
    assert koor_email in mail.outbox[0].recipients()

    assert ur_instance.instance_state.name == "ext"
    assert ur_instance.location_id == location.pk
    assert ur_instance.group == koor_group


@pytest.mark.parametrize("service_group__name", ["coordination"])
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_instance_submit_mitbericht_bund_ur(
    mocker,
    admin_client,
    settings,
    ur_instance,
    notification_template,
    application_settings,
    mock_generate_and_store_pdf,
    location_factory,
    group_factory,
    instance_state_factory,
    service_factory,
    authority_location_factory,
    caluma_workflow_config_ur,
    disable_ech0211_settings,
    ur_master_data_case,
):
    settings.APPLICATION_NAME = "kt_uri"

    caluma_form_factories.FormFactory(slug="personalien")
    ur_instance.case.document.form_id = "mitbericht-bund"
    ur_instance.case.document.save()

    koor_service = service_factory(email="koor-bg@example.com")
    mocker.patch("camac.constants.kt_uri.KOOR_BG_SERVICE_ID", koor_service.pk)
    koor_group = group_factory(service=koor_service)
    mocker.patch("camac.constants.kt_uri.KOOR_BG_GROUP_ID", koor_group.pk)
    mocker.patch("camac.constants.kt_uri.KOOR_GROUP_IDS", [koor_group.pk])
    koor_email = koor_group.service.email

    ur_instance.group = koor_group
    ur_instance.save()

    application_settings["NOTIFICATIONS"] = {
        "SUBMIT_KOOR": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["municipality"],
            },
        ],
    }
    application_settings["SET_SUBMIT_DATE_CAMAC_WORKFLOW"] = True
    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False

    location = location_factory(communal_federal_number="1")

    authority_location_factory(location=location)

    instance_state_factory(name="ext")
    instance_state_factory(name="subm")

    response = admin_client.post(reverse("instance-submit", args=[ur_instance.pk]))

    ur_instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK

    assert len(mail.outbox) == 1
    assert koor_email in mail.outbox[0].recipients()

    assert ur_instance.location_id == location.pk
    assert ur_instance.group == koor_group


@pytest.mark.parametrize("service_group__name", ["coordination"])
@pytest.mark.parametrize(
    "form_slug", ["konzession-waermeentnahme", "bohrbewilligung-waermeentnahme"]
)
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_instance_submit_heat_extraction_ur(
    mocker,
    admin_client,
    settings,
    caluma_workflow_config_ur,
    ur_instance,
    notification_template,
    application_settings,
    mock_generate_and_store_pdf,
    workflow_item_factory,
    location_factory,
    group_factory,
    role_factory,
    instance_factory,
    question_factory,
    instance_state_factory,
    service_factory,
    authority_location_factory,
    form_slug,
    ur_master_data_settings,
    disable_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_uri"

    ur_instance.case.document.form_id = form_slug
    ur_instance.case.document.save()
    caluma_form_factories.FormFactory(slug="personalien")
    ur_instance.case.document.save()

    koor_service = service_factory(email="KOOR_AFE@example.com")
    mocker.patch("camac.constants.kt_uri.KOOR_AFE_SERVICE_ID", koor_service.pk)
    koor_group = group_factory(service=koor_service)
    mocker.patch("camac.constants.kt_uri.KOOR_AFE_GROUP_ID", koor_group.pk)
    mocker.patch("camac.constants.kt_uri.KOOR_GROUP_IDS", [koor_group.pk])
    koor_email = koor_group.service.email

    application_settings["NOTIFICATIONS"] = {
        "SUBMIT_KOOR": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["municipality"],
            },
        ],
    }
    application_settings["SET_SUBMIT_DATE_CAMAC_WORKFLOW"] = True
    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False

    workflow_item_factory(workflow_item_id=ur_constants.WORKFLOW_ITEM_DOSSIER_ERFASST)

    location = location_factory()

    ur_instance.case.document.answers.create(
        value=str(location.communal_federal_number), question_id="municipality"
    )

    if form_slug == "konzession-waermeentnahme":
        source_instance = instance_factory()

        instance_id_question = question_factory(
            slug="dossier-id-der-bohrbewilligung",
            type=caluma_form_models.Question.TYPE_INTEGER,
        )

        ur_instance.case.document.answers.create(
            value=source_instance.pk, question=instance_id_question
        )

    authority_location_factory(location=location)

    instance_state_factory(name="ext")
    instance_state_factory(name="subm")

    response = admin_client.post(reverse("instance-submit", args=[ur_instance.pk]))

    ur_instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK

    assert len(mail.outbox) == 1
    assert koor_email in mail.outbox[0].recipients()

    assert ur_instance.instance_state.name == "ext"
    assert ur_instance.location_id == location.pk
    assert ur_instance.group == koor_group

    if form_slug == "konzession-waermeentnahme":
        source_instance.refresh_from_db()
        assert (
            ur_instance.instance_group == source_instance.instance_group
        ), 'for "konzessionsgesuche" the "konzessionsdossier" should be linked with the "bohrbewilligungsdossier"'


@pytest.mark.parametrize("service_group__name", ["applicant"])
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_instance_submit_pgv_gemeindestrasse_ur(
    mocker,
    admin_client,
    settings,
    caluma_workflow_config_ur,
    ur_instance,
    notification_template,
    application_settings,
    mock_generate_and_store_pdf,
    workflow_item_factory,
    location_factory,
    group_factory,
    instance_state_factory,
    service_factory,
    authority_location_factory,
    ur_master_data_settings,
    disable_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_uri"

    ur_instance.case.document.form_id = "pgv-gemeindestrasse"
    ur_instance.case.document.save()

    koor_service = service_factory(email="KOOR_BD@example.com")
    mocker.patch("camac.constants.kt_uri.KOOR_BD_SERVICE_ID", koor_service.pk)
    koor_group = group_factory(service=koor_service)
    mocker.patch("camac.constants.kt_uri.KOOR_BD_GROUP_ID", koor_group.pk)
    mocker.patch("camac.constants.kt_uri.KOOR_GROUP_IDS", [koor_group.pk])
    koor_email = koor_group.service.email

    application_settings["NOTIFICATIONS"] = {
        "SUBMIT_KOOR": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["municipality"],
            },
        ],
    }
    application_settings["SET_SUBMIT_DATE_CAMAC_WORKFLOW"] = True
    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False

    workflow_item_factory(workflow_item_id=ur_constants.WORKFLOW_ITEM_DOSSIER_ERFASST)

    location = location_factory()

    ur_instance.case.document.answers.create(
        value=str(location.communal_federal_number), question_id="municipality"
    )
    mocker.patch(
        "camac.constants.kt_uri.BAUDIREKTION_AUTHORITY_ID",
        location.communal_federal_number,
    )

    instance_state_factory(name="ext")
    instance_state_factory(name="subm")

    response = admin_client.post(reverse("instance-submit", args=[ur_instance.pk]))

    ur_instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK

    assert len(mail.outbox) == 1
    assert koor_email in mail.outbox[0].recipients()

    assert ur_instance.instance_state.name == "ext"
    assert ur_instance.location_id == location.pk
    assert ur_instance.group == koor_group


@pytest.mark.parametrize(
    "instance_state__name,instance__user,service_group__name",
    [("new", lf("admin_user"), "Sekretariate Gemeindebaubehörden")],
)
def test_instance_submit_mitbericht_kanton_doesnt_send_mail(
    admin_client,
    ur_instance,
    application_settings,
    mock_generate_and_store_pdf,
    location_factory,
    instance_state_factory,
    authority_location_factory,
    disable_ech0211_settings,
    set_application_ur,
    ur_master_data_case,
):
    ur_instance.case.document.form_id = "mitbericht-kanton"
    ur_instance.case.document.save()

    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False

    location = location_factory()

    ur_instance.case.document.answers.get(question_id="municipality").delete()
    caluma_form_factories.DynamicOptionFactory(
        question_id="municipality",
        document=ur_instance.case.document,
        slug=str(location.communal_federal_number),
        label={"de": "Some place"},
    )
    ur_instance.case.document.answers.create(
        value=str(location.communal_federal_number), question_id="municipality"
    )

    authority_location_factory(location=location)
    Service.objects.first().groups.first().locations.set([location])

    instance_state_factory(name="ext")
    instance_state_factory(name="subm")

    response = admin_client.post(reverse("instance-submit", args=[ur_instance.pk]))

    assert response.status_code == status.HTTP_200_OK

    assert len(mail.outbox) == 0


@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "role__name,service_group__name", [("Applicant", "coordination")]
)
def test_instance_authority_by_submission_for_koor_afg(
    mocker,
    admin_client,
    settings,
    ur_instance,
    application_settings,
    location_factory,
    group_factory,
    instance_state_factory,
    service_factory,
    authority_location_factory,
    disable_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_uri"
    application_settings["STORE_PDF"] = False
    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False

    ur_instance.case.document.form_id = "bgbb"
    ur_instance.case.document.save()

    koor_service = service_factory(email="KOOR_AFG@example.com")
    mocker.patch("camac.constants.kt_uri.KOOR_AFG_SERVICE_ID", koor_service.pk)
    koor_group = group_factory(service=koor_service)
    mocker.patch("camac.constants.kt_uri.KOOR_AFG_GROUP_ID", koor_group.pk)
    ur_instance.group = koor_group
    ur_instance.save()

    location = location_factory()

    authority_location_factory(location=location)

    ur_instance.case.document.answers.create(
        value=str(location.communal_federal_number), question_id="municipality"
    )

    instance_state_factory(name="ext")
    instance_state_factory(name="subm")

    response = admin_client.post(reverse("instance-submit", args=[ur_instance.pk]))

    ur_instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK

    assert ur_instance.case.document.answers.get(
        question_id="leitbehoerde"
    ).value == str(uri_constants.KOOR_AFG_AUTHORITY_ID)


@pytest.mark.parametrize("service_group__name", ["Sekretariate Gemeindebaubehörden"])
def test_set_instance_service_ur_bgbb(
    db, ur_instance, mocker, set_application_ur, group_factory, utils
):
    # if form is "bgbb" and the form was submitted by the AFG
    # AFG should be the responsible service. Otherwise it is the
    # municipality where it was submitted.
    ur_instance.case.document.form_id = "bgbb"
    ur_instance.case.document.form.save()

    koor_afg_group = group_factory(
        service__name="KOOR AFG", service__service_group__name="Koordinationsstellen"
    )

    utils.add_answer(
        ur_instance.case.document,
        "municipality",
        ur_instance.group.locations.first().communal_federal_number,
    )

    ur_instance.group = koor_afg_group
    mocker.patch("camac.constants.kt_uri.KOOR_AFG_GROUP_ID", koor_afg_group.pk)
    mocker.patch(
        "camac.constants.kt_uri.KOOR_AFG_SERVICE_ID", koor_afg_group.service.pk
    )

    serializer = CalumaInstanceSubmitSerializer()
    serializer.instance = ur_instance

    assert ur_instance.responsible_service() is None
    serializer._set_instance_service(ur_instance.case, ur_instance)
    assert (
        ur_instance.responsible_service() == koor_afg_group.service
    ), "should assign the KOOR AFG as the responsible service"


@pytest.mark.parametrize("form_slug", ["oereb", "oereb-verfahren-gemeinde"])
@pytest.mark.parametrize("service_group__name", [("municipality", "coordination")])
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_oereb_instance_copy_for_koor_afj(
    mocker,
    admin_client,
    settings,
    caluma_workflow_config_ur,
    ur_instance,
    notification_template,
    application_settings,
    mock_generate_and_store_pdf,
    workflow_item_factory,
    location_factory,
    group_factory,
    form_factory,
    instance_state_factory,
    service_factory,
    authority_location_factory,
    form_slug,
    attachment_factory,
    utils,
    disable_ech0211_settings,
    ur_master_data_case,
):
    settings.APPLICATION_NAME = "kt_uri"  # can't use set_application_ur here because we already use ur_master_data_case (the two factories conflict with each other)

    ur_instance.form = form_factory(name="camac-form")
    ur_instance.save()

    ur_instance.case.document.form_id = form_slug
    ur_instance.case.document.save()

    mocker.patch(
        "camac.constants.kt_uri.CALUMA_FORM_MAPPING",
        {ur_instance.form.pk: ur_instance.form.name},
    )

    koor_afj_service = service_factory(email="KOOR_AFJ@example.com")
    mocker.patch("camac.constants.kt_uri.KOOR_AFJ_SERVICE_ID", koor_afj_service.pk)
    koor_afj_group = group_factory(service=koor_afj_service)
    mocker.patch("camac.constants.kt_uri.KOOR_AFJ_GROUP_ID", koor_afj_group.pk)
    mocker.patch("camac.constants.kt_uri.KOOR_GROUP_IDS", [koor_afj_group.pk])

    koor_np_service = service_factory(email="KOOR_NP@example.com", name="KOOR NP")
    mocker.patch("camac.constants.kt_uri.KOOR_NP_SERVICE_ID", koor_np_service.pk)

    location = location_factory()
    authority_location_factory(location=location)

    ur_instance.case.document.answers.get(question_id="municipality").delete()
    caluma_form_factories.DynamicOptionFactory(
        question_id="municipality",
        document=ur_instance.case.document,
        slug=str(location.communal_federal_number),
        label={"de": "Some place"},
    )

    gbb_altdorf_service = service_factory(
        email="gbb-altdorf@example.com",
        name="GBB Altdorf",
        service_group__name="Sekretariate Gemeindebaubehörden",
    )
    gbb_group = group_factory()
    gbb_group.locations.set([location])
    gbb_group.save()
    gbb_altdorf_service.groups.set([gbb_group])
    gbb_altdorf_service.save()

    mocker.patch(
        "camac.constants.kt_uri.GBB_ALTDORF_SERVICE_ID", gbb_altdorf_service.pk
    )

    ur_instance.case.document.answers.create(
        value=str(location.communal_federal_number), question_id="municipality"
    )

    if form_slug == "oereb":
        group = group_factory(service=koor_np_service)
        ur_instance.group = group
        ur_instance.save()
        mocker.patch("camac.constants.kt_uri.KOOR_NP_GROUP_ID", group.pk)
        email = group.service.email

        utils.add_answer(
            ur_instance.case.document,
            "waldfeststellung-mit-statischen-waldgrenzen-kanton",
            "waldfeststellung-mit-statischen-waldgrenzen-kanton-ja",
        )
    elif form_slug == "oereb-verfahren-gemeinde":
        group = group_factory(service=gbb_altdorf_service)
        ur_instance.group = group
        ur_instance.save()
        mocker.patch("camac.constants.kt_uri.GBB_ALTDORF_SERVICE_ID", group.pk)
        email = group.service.email

        utils.add_answer(
            ur_instance.case.document,
            "waldfeststellung-mit-statischen-waldgrenzen-gemeinde",
            "waldfeststellung-mit-statischen-waldgrenzen-gemeinde-ja",
        )

    application_settings["SET_SUBMIT_DATE_CAMAC_WORKFLOW"] = True
    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False

    instance_state_factory(name="ext")
    instance_state_factory(name="comm")
    instance_state_factory(name="subm")

    assert len(Instance.objects.all()) == 1

    response = admin_client.post(reverse("instance-submit", args=[ur_instance.pk]))

    assert response.status_code == status.HTTP_200_OK

    assert len(Instance.objects.all()) == 2

    copied_instance = Instance.objects.exclude(
        group__service__name__in=["KOOR NP", "GBB Altdorf"]
    ).first()

    assert copied_instance.group == koor_afj_group
    assert copied_instance.location_id == location.pk
    assert copied_instance.instance_state.name == "ext"

    ur_instance.refresh_from_db()

    if form_slug == "oereb":
        assert len(mail.outbox) == 2
        assert email in list(itertools.chain(*[m.recipients() for m in mail.outbox]))

    assert ur_instance.instance_state.name == "subm"
    assert ur_instance.location_id == location.pk
    assert ur_instance.group == group


@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_instance_submit_message_building_services_ur(
    admin_client,
    settings,
    caluma_workflow_config_ur,
    ur_instance,
    notification_template,
    application_settings,
    mock_generate_and_store_pdf,
    workflow_item_factory,
    group_factory,
    role_factory,
    instance_state_factory,
    service_factory,
    instance_factory,
    authority_location,
    disable_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_uri"
    application_settings["CALUMA"]["USE_LOCATION"] = True
    application_settings["CALUMA"]["GENERATE_IDENTIFIER"] = False
    application_settings["USE_INSTANCE_SERVICE"] = False
    application_settings["NOTIFICATIONS"] = {"SUBMIT": []}

    message_building_services_form = caluma_form_factories.FormFactory(
        slug="technische-bewilligung"
    )
    caluma_form_factories.FormFactory(slug="form-gebaeudetechnik")
    ur_instance.case.document.form = message_building_services_form
    ur_instance.case.document.save()

    ur_instance.case.document.form.questions.create(
        slug="dossier-id-laufendes-verfahren",
        type=caluma_form_models.Question.TYPE_INTEGER,
    )

    source_instance = instance_factory()

    ur_instance.case.document.answers.create(
        value=source_instance.pk, question_id="dossier-id-laufendes-verfahren"
    )

    application_settings["SET_SUBMIT_DATE_CAMAC_WORKFLOW"] = True
    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False

    workflow_item_factory(workflow_item_id=ur_constants.WORKFLOW_ITEM_DOSSIER_ERFASST)

    ur_instance.case.document.answers.create(
        value=str(authority_location.location.communal_federal_number),
        question_id="municipality",
    )

    instance_state_factory(name="subm")

    response = admin_client.post(reverse("instance-submit", args=[ur_instance.pk]))

    ur_instance.refresh_from_db()
    source_instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK

    assert ur_instance.instance_state.name == "subm"
    assert ur_instance.location == authority_location.location
    assert ur_instance.instance_group == source_instance.instance_group


@pytest.mark.parametrize("service_group__name", ["municipality"])
@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
@pytest.mark.parametrize(
    "is_building_police_procedure,is_extend_validity", [(True, False), (False, True)]
)
def test_instance_submit_state_change_be(
    admin_client,
    role,
    role_factory,
    group_factory,
    be_instance,
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

    be_instance.case.workflow = workflow
    be_instance.case.save()
    be_instance.case.document.form = form
    be_instance.case.document.save()

    be_instance.case.document.answers.create(
        value=str(service.pk), question_id="gemeinde"
    )

    group_factory(role=role_factory(name="support"))
    instance_state_factory(name="subm")

    admin_client.post(reverse("instance-submit", args=[be_instance.pk]))

    be_instance.refresh_from_db()

    if is_extend_validity:
        assert be_instance.instance_state.name == "circulation_init"

    if is_building_police_procedure:
        assert be_instance.instance_state.name == "in_progress_internal"


@pytest.mark.parametrize("role__name,instance__user", [("Canton", lf("user"))])
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
    [("Applicant", lf("admin_user"), "municipality")],
)
@pytest.mark.parametrize(
    "instance_state__name,geometer_is_unnecessary,expected_status,expected_emails",
    [
        ("sb1", False, status.HTTP_200_OK, 3),
        ("sb1", True, status.HTTP_200_OK, 2),
        ("new", False, status.HTTP_403_FORBIDDEN, 0),
    ],
)
def test_instance_report(
    admin_client,
    role,
    be_instance,
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
    caluma_admin_user,
    decision_factory,
    settings,
    be_decision_settings,
    be_ech0211_settings,
    service_factory,
    question_factory,
    instance_acl_factory,
    access_level_factory,
    work_item_factory,
    permissions_settings,
    geometer_is_unnecessary,
    expected_emails,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    instance_state_factory(name="coordination")
    instance_state_factory(name="sb2")

    application_settings["NOTIFICATIONS"]["REPORT"] = [
        {
            "template_slug": notification_template.slug,
            "recipient_types": ["applicant", "construction_control"],
        },
        {
            "template_slug": notification_template.slug,
            "recipient_types": ["geometer_acl_services"],
        },
    ]

    if instance_state.name == "sb1":
        service = be_instance.responsible_service()
        construction_control = construction_control_for(service)

        geometer_service = service_factory(email="geometer@example.ch")
        instance_acl_factory(
            instance=be_instance,
            access_level=access_level_factory(slug="geometer"),
            service=geometer_service,
            metainfo={"disable-notification-on-creation": True},
        )
        permissions_settings["geometer"] = [("foo", ["*"])]

        geometer_work_item = work_item_factory(
            task_id="geometer",
            status="completed",
            case=be_instance.case,
        )

        geometer_value = "geometer-beurteilung-notwendigkeit-vermessung-notwendig"
        if geometer_is_unnecessary:
            geometer_value = (
                "geometer-beurteilung-notwendigkeit-vermessung-nicht-notwendig"
            )

        save_answer(
            question=question_factory(
                slug="geometer-beurteilung-notwendigkeit-vermessung"
            ),
            document=geometer_work_item.document,
            value=geometer_value,
        )

        for task_id, fn in [
            ("submit", workflow_api.complete_work_item),
            ("ebau-number", workflow_api.complete_work_item),
            ("distribution", workflow_api.skip_work_item),
            ("decision", workflow_api.complete_work_item),
        ]:
            if task_id == "decision":
                decision_factory(
                    decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"]
                )

            fn(
                work_item=be_instance.case.work_items.get(task_id=task_id),
                user=caluma_admin_user,
                context={"group-id": service.pk},
            )

    response = admin_client.post(reverse("instance-report", args=[be_instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert len(mail.outbox) == expected_emails

        recipients = flatten([m.to for m in mail.outbox])

        assert be_instance.user.email in recipients
        assert construction_control.email in recipients
        if not geometer_is_unnecessary:
            assert geometer_service.email in recipients

        be_instance.case.refresh_from_db()
        assert be_instance.case.status == "running"
        assert be_instance.case.work_items.filter(
            task_id="sb2", status="ready"
        ).exists()


@pytest.mark.parametrize(
    "role__name,instance__user,service_group__name",
    [("Applicant", lf("admin_user"), "municipality")],
)
@pytest.mark.parametrize(
    "instance_state__name,geometer_is_unnecessary,expected_status,expected_emails",
    [
        ("sb2", False, status.HTTP_200_OK, 3),
        ("sb2", True, status.HTTP_200_OK, 2),
        ("new", False, status.HTTP_403_FORBIDDEN, 0),
    ],
)
@pytest.mark.parametrize(
    "create_awa_workitem",
    [True, False],
)
def test_instance_finalize(
    admin_client,
    role,
    be_instance,
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
    caluma_admin_user,
    create_awa_workitem,
    form_question_factory,
    decision_factory,
    settings,
    be_decision_settings,
    be_ech0211_settings,
    service_factory,
    question_factory,
    instance_acl_factory,
    access_level_factory,
    work_item_factory,
    permissions_settings,
    geometer_is_unnecessary,
    expected_emails,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    instance_state_factory(name="coordination")
    instance_state_factory(name="sb1")
    instance_state_factory(name="conclusion")

    application_settings["NOTIFICATIONS"]["FINALIZE"] = [
        {
            "template_slug": notification_template.slug,
            "recipient_types": [
                "applicant",
                "construction_control",
            ],
        },
        {
            "template_slug": notification_template.slug,
            "recipient_types": ["geometer_acl_services"],
        },
    ]

    be_instance.case.meta.update(
        {
            "submit-date": be_instance.creation_date.strftime(SUBMIT_DATE_FORMAT),
            "paper-submit-date": be_instance.creation_date.strftime(SUBMIT_DATE_FORMAT),
        }
    )
    be_instance.case.save()

    if instance_state.name == "sb2":
        service = be_instance.responsible_service()
        construction_control = construction_control_for(service)

        geometer_service = service_factory(email="geometer@example.ch")
        instance_acl_factory(
            instance=be_instance,
            access_level=access_level_factory(slug="geometer"),
            service=geometer_service,
            metainfo={"disable-notification-on-creation": True},
        )
        permissions_settings["geometer"] = [("foo", ["*"])]

        geometer_work_item = work_item_factory(
            task_id="geometer",
            status="completed",
            case=be_instance.case,
        )

        geometer_value = "geometer-beurteilung-notwendigkeit-vermessung-notwendig"
        if geometer_is_unnecessary:
            geometer_value = (
                "geometer-beurteilung-notwendigkeit-vermessung-nicht-notwendig"
            )

        save_answer(
            question=question_factory(
                slug="geometer-beurteilung-notwendigkeit-vermessung"
            ),
            document=geometer_work_item.document,
            value=geometer_value,
        )

        for task_id, fn in [
            ("submit", workflow_api.complete_work_item),
            ("ebau-number", workflow_api.complete_work_item),
            ("distribution", workflow_api.skip_work_item),
            ("decision", workflow_api.complete_work_item),
            ("sb1", workflow_api.complete_work_item),
        ]:
            if task_id == "decision":
                decision_factory(
                    decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"]
                )

            fn(
                work_item=be_instance.case.work_items.get(task_id=task_id),
                user=caluma_admin_user,
                context={"group-id": service.pk},
            )

        be_instance.instance_state = instance_state
        be_instance.save()

    if create_awa_workitem:
        table_form = caluma_form_models.Form.objects.create(
            slug="lagerung-von-stoffen-tabelle-v2"
        )
        form_question_factory(
            form=be_instance.case.document.form,
            question=caluma_form_models.Question.objects.create(
                slug="lagerung-von-stoffen-v2",
                type=caluma_form_models.Question.TYPE_TABLE,
                row_form=table_form,
            ),
        )
        table = be_instance.case.document.answers.create(
            question_id="lagerung-von-stoffen-v2"
        )
        row = caluma_form_models.Document.objects.create(
            form_id="lagerung-von-stoffen-tabelle-v2"
        )

        table.documents.add(row)

    response = admin_client.post(reverse("instance-finalize", args=[be_instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK and not create_awa_workitem:
        assert len(mail.outbox) == expected_emails

        recipients = flatten([m.to for m in mail.outbox])

        assert be_instance.user.email in recipients
        assert construction_control.email in recipients
        if not geometer_is_unnecessary:
            assert geometer_service.email in recipients

        assert sorted(
            be_instance.case.work_items.filter(status="ready").values_list(
                "task_id", flat=True
            )
        ) == sorted(
            [
                "check-sb1",
                "check-sb2",
                "complete",
                "create-manual-workitems",
                "create-publication",
            ]
        )
    elif expected_status == status.HTTP_200_OK and create_awa_workitem:
        assert caluma_workflow_models.WorkItem.objects.get(
            name__de="Meldeformular an AWA weiterleiten"
        )


@pytest.mark.parametrize("paper", [(True, False)])
@pytest.mark.parametrize("form_slug", [(None), ("nfd")])
@pytest.mark.parametrize("service_group__name", ["municipality"])
def test_generate_and_store_pdf(
    db,
    be_instance,
    admin_user,
    service,
    group,
    attachment_section_factory,
    document_factory,
    mocker,
    form_slug,
    paper,
    application_settings,
    caluma_workflow_config_be,
    caluma_admin_user,
    dms_settings,
):
    application_settings["DOCUMENT_BACKEND"] = "camac-ng"
    mocker.patch("camac.caluma.api.CalumaApi.is_paper", lambda s, i: paper)

    attachment_section_default = attachment_section_factory()
    attachment_section_paper = attachment_section_factory()

    application_settings["STORE_PDF"] = {
        "SECTION": {
            form_slug.upper() if form_slug else "MAIN": {
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
    context["request"].caluma_info.context.user = caluma_admin_user
    mocker.patch("rest_framework.authentication.get_authorization_header")

    serializer = CalumaInstanceSubmitSerializer()

    dms_settings["FORM"] = {
        "main-form": {"template": "some-template"},
        "nfd": {"template": "some-template"},
    }

    be_instance.case.document.answers.create(
        value=str(service.pk), question_id="gemeinde"
    )

    if form_slug:
        workflow_api.complete_work_item(
            work_item=be_instance.case.work_items.get(task_id="submit"),
            user=caluma_admin_user,
        )

    serializer._generate_and_store_pdf(be_instance, form_slug=form_slug)

    assert attachment_section_paper.attachments.count() == 1 if paper else 0
    assert attachment_section_default.attachments.count() == 0 if paper else 1


def test_generate_and_store_pdf_in_alexandria(
    db,
    admin_user,
    application_settings,
    alexandria_settings,
    dms_settings,
    gr_instance,
    group,
    mocker,
):
    sensitive_mark = MarkFactory()
    alexandria_category = CategoryFactory()
    application_settings["STORE_PDF"] = {
        "SECTION": {
            "MAIN": {"DEFAULT": alexandria_category.pk, "PAPER": alexandria_category.pk}
        },
    }
    alexandria_settings["MARK_VISIBILITY"]["SENSITIVE"] = [sensitive_mark.pk]
    application_settings["DOCUMENT_BACKEND"] = "alexandria"

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

    serializer = CalumaInstanceSubmitSerializer()

    dms_settings["ADD_HEADER_DATA"] = False
    dms_settings["FORM"] = {
        "main-form": {"template": "some-template"},
    }

    serializer._generate_and_store_pdf(gr_instance)

    assert alexandria_category.documents.count() == 1
    assert sensitive_mark in alexandria_category.documents.first().marks.all()


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
@pytest.mark.parametrize("is_paper,expected_count", [("1", 1), ("0", 2), ("", 3)])
def test_caluma_instance_list_filter(
    admin_client,
    instance_factory,
    instance_with_case,
    be_instance,
    is_paper,
    expected_count,
    role,
    admin_user,
    mock_public_status,
    mock_nfd_permissions,
):
    for instance, paper in [
        (instance_with_case(instance_factory(user=admin_user)), False),
        (instance_with_case(instance_factory(user=admin_user)), False),
        (be_instance, True),
    ]:
        instance.case.document.answers.create(
            question_id="is-paper", value=f"is-paper-{'yes' if paper else 'no'}"
        )

    url = reverse("instance-list")
    response = admin_client.get(url, data={"is_paper": is_paper})

    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    assert len(json["data"]) == expected_count


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
@pytest.mark.parametrize(
    "has_pending_billing_entry,expected_count", [("1", 1), ("0", 2), ("", 3)]
)
def test_has_pending_billing_entry_filter(
    admin_user,
    admin_client,
    ur_instance,
    instance_with_case,
    instance_factory,
    billing_entry_factory,
    has_pending_billing_entry,
    expected_count,
):
    # instances without pending billing entry
    billing_entry_factory(
        instance=instance_with_case(instance_factory(user=admin_user)), invoiced=1
    )
    billing_entry_factory(
        instance=instance_with_case(instance_factory(user=admin_user)), invoiced=1
    )

    # instance with pending billing entry
    billing_entry_factory(instance=ur_instance, invoiced=0, type=1)

    url = reverse("instance-list")
    response = admin_client.get(
        url, data={"has_pending_billing_entry": has_pending_billing_entry}
    )

    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "objection_received,expected_count",
    [(True, 2), ("", 3), (False, 3)],
)
def test_objection_received_filter(
    admin_user,
    admin_client,
    sz_instance,
    instance_with_case,
    instance_factory,
    objection_factory,
    objection_received,
    expected_count,
):
    # instances with objections
    objection_factory(instance=instance_with_case(instance_factory(user=admin_user)))
    objection_factory(instance=instance_with_case(instance_factory(user=admin_user)))

    # instance without objection
    instance_factory(user=admin_user)

    url = reverse("instance-list")
    response = admin_client.get(url, data={"objection_received": objection_received})

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["data"]) == expected_count


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
@pytest.mark.parametrize(
    "filter,expected",
    [
        ("typ-des-verfahrens-anpassung", 2),
        ("typ-des-verfahrens-festsetzung", 1),
        ("typ-des-verfahrens-festsetzung,typ-des-verfahrens-anpassung", 3),
        ("", 3),
        ("test123", 0),
    ],
)
def test_oereb_legal_state_filter_ur(
    admin_user,
    admin_client,
    ur_instance,
    instance_with_case,
    question_factory,
    answer_factory,
    instance_factory,
    filter,
    expected,
):
    instance_1 = ur_instance
    instance_2 = instance_with_case(instance_factory(user=admin_user))
    instance_3 = instance_with_case(instance_factory(user=admin_user))

    question = question_factory(
        slug="typ-des-verfahrens",
        type=caluma_form_models.Question.TYPE_CHOICE,
    )
    answer_factory(
        document=instance_1.case.document,
        question=question,
        value="typ-des-verfahrens-anpassung",
    )
    answer_factory(
        document=instance_2.case.document,
        question=question,
        value="typ-des-verfahrens-festsetzung",
    )
    answer_factory(
        document=instance_3.case.document,
        question=question,
        value="typ-des-verfahrens-anpassung",
    )

    url = reverse("instance-list")
    response = admin_client.get(url, data={"oereb_legal_state": filter})

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["data"]) == expected


@pytest.mark.parametrize(
    "value,expected_count",
    [("innerhalb", 2), ("ausserhalb", 1), ("beides", 0), ("", 3)],
)
def test_construction_zone_location_filter_sz(
    admin_user,
    admin_client,
    sz_instance,
    form_field_factory,
    instance_with_case,
    instance_factory,
    value,
    expected_count,
    application_settings,
):
    application_settings["CONSTRUCTION_ZONE_LOCATION_FORM_FIELD"] = "lage"
    form_field_factory(
        instance=instance_with_case(instance_factory(user=admin_user)),
        name="lage",
        value="innerhalb",
    )
    form_field_factory(
        instance=instance_with_case(instance_factory(user=admin_user)),
        name="lage",
        value="innerhalb",
    )
    form_field_factory(
        instance=instance_with_case(instance_factory(user=admin_user)),
        name="lage",
        value="ausserhalb",
    )

    url = reverse("instance-list")
    response = admin_client.get(url, data={"construction_zone_location_sz": value})

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["data"]) == expected_count


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
@pytest.mark.parametrize(
    "has_pending_sanction,expected_count", [("1", 1), ("0", 2), ("", 3)]
)
def test_has_pending_sanction_filter(
    admin_user,
    admin_client,
    ur_instance,
    instance_with_case,
    instance_factory,
    sanction_factory,
    has_pending_sanction,
    expected_count,
):
    # instances without pending sanction
    sanction_factory(
        instance=instance_with_case(instance_factory(user=admin_user)), is_finished=1
    )
    sanction_factory(
        instance=instance_with_case(instance_factory(user=admin_user)), is_finished=1
    )

    # instance with pending sanction
    sanction_factory(instance=ur_instance, is_finished=0)

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
@pytest.mark.parametrize("role__name,instance__user", [("Canton", lf("user"))])
def test_generate_pdf_action(
    db,
    mocker,
    admin_client,
    user,
    group,
    be_instance,
    caluma_form,
    document_factory,
    form_factory,
    form_slug,
    expected_status,
    caluma_workflow_config_be,
    caluma_admin_user,
    has_document_id,
    dms_settings,
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

    dms_settings["FORM"] = {
        "main-form": {"template": "some-template"},
        "nfd": {"template": "some-template"},
        "mp-form": {"template": "some-template"},
    }

    if form_slug:
        workflow_api.complete_work_item(
            work_item=be_instance.case.work_items.get(task_id="submit"),
            user=caluma_admin_user,
        )

    url = reverse("instance-generate-pdf", args=[be_instance.pk])
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


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "patch_data,expected",
    [
        ({"relationships": {"keywords": {"data": []}}}, status.HTTP_200_OK),
        ({"attributes": {"name": "foo"}}, status.HTTP_403_FORBIDDEN),
    ],
)
def test_instance_update(
    db,
    admin_client,
    admin_user,
    be_instance,
    keyword_factory,
    patch_data,
    expected,
):
    kw = keyword_factory(service=admin_user.groups.first().service)
    kw.instances.set([be_instance])
    kw.save()

    request_json = {
        "data": {
            "id": str(be_instance.pk),
            "type": "instances",
            **patch_data,
        }
    }
    url = reverse("instance-detail", args=[be_instance.pk])
    response = admin_client.patch(url, request_json)
    assert response.status_code == expected
    if expected == status.HTTP_200_OK:
        assert response.json()["data"]["relationships"]["keywords"] == {
            "data": [],
            "meta": {"count": 0},
        }


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

    data = {"data": {"type": "instances", "attributes": {"caluma-form": "main-form"}}}

    create_resp = admin_client.post(reverse("instance-list"), data, **headers)

    instance_id = int(create_resp.json()["data"]["id"])
    instance = Instance.objects.get(pk=instance_id)
    instance.attachments.set([attachment])

    case = instance.case
    document = case.document

    url = reverse("instance-detail", args=[instance_id])
    response = admin_client.get(url, **headers)
    assert response.status_code == status.HTTP_200_OK

    path = Path(attachment.path.path)
    assert path.is_file()

    response = admin_client.delete(url, **headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    with pytest.raises(attachment.DoesNotExist):
        attachment.refresh_from_db()

    assert not path.is_file()

    with pytest.raises(attachment.DoesNotExist):
        attachment.refresh_from_db()

    with pytest.raises(document.DoesNotExist):
        document.refresh_from_db()

    with pytest.raises(case.DoesNotExist):
        case.refresh_from_db()

    with pytest.raises(instance.DoesNotExist):
        instance.refresh_from_db()


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
    submit_date_question,
    rejection_settings,
    caluma_admin_user,
    disable_ech0211_settings,
):
    application_settings["NOTIFICATIONS"]["SUBMIT"] = []

    new_state = instance_state_factory(name="new")
    subm_state = instance_state_factory(name="subm")
    rejected_state = instance_state_factory(name="rejected")
    finished_state = instance_state_factory(
        name=rejection_settings["INSTANCE_STATE_REJECTION_COMPLETE"]
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
    workflow_api.suspend_case(source_instance.case, caluma_admin_user)

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

    case = new_instance.case

    case.document.answers.create(value=str(service.pk), question_id="gemeinde")

    submit_response = admin_client.post(
        reverse("instance-submit", args=[new_instance.pk])
    )

    assert submit_response.status_code == status.HTTP_200_OK

    new_instance.refresh_from_db()
    source_instance.refresh_from_db()

    assert new_instance.instance_state == subm_state
    assert source_instance.instance_state == finished_state


@pytest.mark.parametrize("service_group__name", ["municipality"])
def test_be_copy_responsible_user_on_submit(
    db,
    admin_client,
    instance_state_factory,
    form,
    service,
    mock_nfd_permissions,
    caluma_workflow_config_be,
    mock_generate_and_store_pdf,
    application_settings,
    submit_date_question,
    rejection_settings,
    work_item_factory,
    user_factory,
    disable_ech0211_settings,
):
    application_settings["NOTIFICATIONS"]["SUBMIT"] = []
    application_settings["COPY_RESPONSIBLE_PERSON_ON_SUBMIT"] = True

    new_state = instance_state_factory(name="new")
    subm_state = instance_state_factory(name="subm")
    rejected_state = instance_state_factory(name="rejected")
    instance_state_factory(name=rejection_settings["INSTANCE_STATE_REJECTION_COMPLETE"])

    create_response = admin_client.post(
        reverse("instance-list"),
        {"data": {"type": "instances", "attributes": {"caluma-form": "main-form"}}},
    )

    assert (
        create_response.status_code == status.HTTP_201_CREATED
    ), create_response.content

    source_instance_id = int(create_response.json()["data"]["id"])
    source_instance = Instance.objects.get(pk=source_instance_id)

    # Create active and responsible service for source instance
    source_instance.instance_services.create(service=service, active=1)
    source_instance.responsible_services.create(
        service=service,
        responsible_user=user_factory(name="testuser"),
    )

    # Create Work Item
    work_item_factory(case=source_instance.case, addressed_groups=[service.pk])

    # Assign state
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

    case = new_instance.case
    case.document.answers.create(value=str(service.pk), question_id="gemeinde")

    submit_response = admin_client.post(
        reverse("instance-submit", args=[new_instance.pk])
    )

    assert submit_response.status_code == status.HTTP_200_OK

    new_instance.refresh_from_db()

    assert new_instance.instance_state == subm_state

    # Check responsible user was assigned to new_instance
    assert (
        new_instance.responsible_services.first().responsible_user.pk
        == source_instance.responsible_services.first().responsible_user.pk
    )

    # Check work item of new_instance addresed to same service was assigned to responsible_user
    new_work_item = caluma_workflow_models.WorkItem.objects.filter(
        case__family__instance__pk=new_instance.pk,
        addressed_groups=[new_instance.responsible_services.first().service.pk],
        status=caluma_workflow_models.WorkItem.STATUS_READY,
    ).first()

    assert (
        new_work_item.assigned_users[0]
        == source_instance.responsible_services.first().responsible_user.username
    )


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("is_paper", [True, False])
@pytest.mark.parametrize("is_modification", [True, False])
@pytest.mark.parametrize("is_migrated", [True, False])
@pytest.mark.parametrize("is_kog", [True, False])
@pytest.mark.parametrize("is_appeal", [True, False])
@pytest.mark.parametrize("is_ech", [True, False])
def test_instance_name(
    admin_client,
    caluma_workflow_config_be,
    instance,
    instance_with_case,
    group,
    instance_service_factory,
    role,
    multilang,
    is_paper,
    is_modification,
    is_migrated,
    is_kog,
    is_appeal,
    is_ech,
):
    def yes_no_german(boolean):
        return "ja" if boolean else "nein"

    def yes_no_english(boolean):
        return "yes" if boolean else "no"

    instance = instance_with_case(
        instance,
        "migrated" if is_migrated else "building-permit",
        "migriertes-dossier" if is_migrated else "main-form",
        {"instance": instance.pk},
    )

    if is_appeal:
        instance.case.meta.update({"is-appeal": True})
        instance.case.save()

    service_group = instance_service_factory(instance=instance).service.service_group

    if is_migrated:
        instance.case.document.answers.create(
            question_id="geschaeftstyp",
            value="geschaeftstyp-baupolizeiliches-verfahren",
        )
    else:
        instance.case.document.answers.create(
            question_id="is-paper", value=f"is-paper-{yes_no_english(is_paper)}"
        )
        instance.case.document.answers.create(
            question_id="projektaenderung",
            value=f"projektaenderung-{yes_no_german(is_modification)}",
        )

    if is_kog:
        service_group.name = "lead-service"
        service_group.save()

    if is_ech:
        instance.case.meta["ech0211-submitted"] = True
        instance.case.save()

    url = reverse("instance-detail", args=[instance.pk])

    response = admin_client.get(url, data={"fields[instances]": "name"})

    assert response.status_code == status.HTTP_200_OK

    name = response.json()["data"]["attributes"]["name"]

    if is_migrated:
        assert name == "Baupolizeiliches Verfahren (Migriert)"
    else:
        assert "Baugesuch" in name

        assert ("(Papier)" in name) == (is_paper and not is_ech)
        assert ("(Projektänderung)" in name) == is_modification
        assert ("(KoG)" in name) == is_kog
        assert ("(Beschwerdeverfahren)" in name) == is_appeal
        assert ("(Schnittstelle)" in name) == is_ech


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
    caluma_form,
    expected_status,
    project_modification_settings,
):
    instance_state_factory(name="new")

    workflow = caluma_workflow_models.Workflow.objects.get(pk="building-permit")
    workflow.allow_forms.add(
        caluma_form_models.Form.objects.create(slug="baugesuch"),
        caluma_form_models.Form.objects.create(slug="verlaerungerung-geltungsdauer"),
    )

    project_modification_settings["ALLOW_FORMS"] = ["main-form"]
    project_modification_settings["DISALLOW_STATES"] = ["new"]

    create_response = admin_client.post(
        reverse("instance-list"),
        {"data": {"type": "instances", "attributes": {"caluma_form": caluma_form}}},
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


@pytest.mark.freeze_time("2019-05-02")
@pytest.mark.parametrize("instance_state__name", ["new"])
def test_instance_create_caluma_sz(
    admin_client, admin_user, form, instance_state, instance, caluma_workflow_config_sz
):
    url = reverse("instance-list")

    location_data = (
        {"type": "locations", "id": instance.location.pk} if instance.location else None
    )

    data = {
        "data": {
            "type": "instances",
            "id": None,
            "relationships": {
                "form": {"data": {"type": "forms", "id": form.pk}},
                "location": {"data": location_data},
            },
            "attributes": {
                "caluma_workflow": "internal-document",
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize("role__name,instance__user", [("Applicant", lf("admin_user"))])
def test_create_instance_from_modification(
    db,
    admin_client,
    be_instance,
    instance_state_factory,
    role,
    mock_nfd_permissions,
    project_modification_settings,
):
    instance_state_factory(name="new")

    project_modification_settings["ALLOW_FORMS"] = ["main-form"]

    caluma_form_models.Answer.objects.create(
        document=be_instance.case.document,
        question_id="projektaenderung",
        value="projektaenderung-ja",
    )

    response = admin_client.post(
        reverse("instance-list"),
        {
            "data": {
                "type": "instances",
                "attributes": {
                    "copy-source": str(be_instance.pk),
                },
            }
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert CalumaApi().is_modification(
        Instance.objects.get(pk=response.json()["data"]["id"])
    )


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_filter_decision_date(
    db,
    admin_client,
    decision_factory,
    instance_factory,
    instance_service_factory,
    instance_with_case,
    service,
    be_decision_settings,
):
    for decision_date in [
        date(2022, 8, 18),
        date(2022, 8, 17),
        date(2022, 8, 7),
        date(2022, 7, 30),
    ]:
        instance = instance_with_case(instance=instance_factory())
        instance_service_factory(instance=instance, service=service)

        decision_factory(
            instance=instance,
            decision_date=decision_date,
        )

    for filters, expected_count in [
        ({"decision_date_after": "2022-08-17"}, 2),
        ({"decision_date_before": "2022-08-17"}, 3),
    ]:
        response = admin_client.get(reverse("instance-list"), data=filters)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["data"]) == expected_count


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_filter_decision(
    db,
    admin_client,
    decision_factory,
    instance_factory,
    instance_service_factory,
    instance_with_case,
    service,
    be_decision_settings,
):
    for decision in [
        "decision-decision-assessment-accepted",
        "decision-decision-assessment-negative",
        "decision-decision-assessment-positive",
    ]:
        instance = instance_with_case(instance=instance_factory())
        instance_service_factory(instance=instance, service=service)

        decision_factory(instance=instance, decision=decision)

    for filters, expected_count in [
        ({"decision": ""}, 4),
        ({"decision": "decision-decision-assessment-accepted"}, 1),
        (
            {
                "decision": "decision-decision-assessment-positive,decision-decision-assessment-negative"
            },
            2,
        ),
    ]:
        response = admin_client.get(reverse("instance-list"), data=filters)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["data"]) == expected_count


@pytest.mark.parametrize("role__name", ["Service"])
def test_filter_inquiry_dates(db, active_inquiry_factory, admin_client, be_instance):
    active_inquiry_factory(
        for_instance=be_instance,
        created_at=make_aware(datetime(2022, 9, 1)),
        closed_at=make_aware(datetime(2022, 9, 10)),
    )
    active_inquiry_factory(
        for_instance=be_instance,
        created_at=make_aware(datetime(2022, 9, 2)),
        closed_at=make_aware(datetime(2022, 9, 9)),
    )

    for filters, expected_count in [
        ({"inquiry_created_after": "2022-09-03"}, 0),
        ({"inquiry_created_before": "2022-08-31"}, 0),
        ({"inquiry_created_after": "2022-09-01"}, 1),
        ({"inquiry_created_before": "2022-09-01"}, 1),
        ({"inquiry_completed_after": "2022-09-11"}, 0),
        ({"inquiry_completed_before": "2022-09-08"}, 0),
        ({"inquiry_completed_after": "2022-09-10"}, 1),
        ({"inquiry_completed_before": "2022-09-10"}, 1),
    ]:
        response = admin_client.get(reverse("instance-list"), data=filters)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["data"]) == expected_count


@pytest.mark.parametrize("role__name", ["Service"])
def test_filter_inquiry_answer(
    db,
    be_instance,
    admin_client,
    active_inquiry_factory,
    instance_factory,
    instance_service_factory,
    instance_with_case,
    service,
    distribution_settings,
    answer_factory,
):
    for inquiry_answer in [
        "inquiry-answer-status-claim",
        "inquiry-answer-status-negative",
        "inquiry-answer-status-positive",
    ]:
        instance = instance_with_case(instance=instance_factory())
        instance_service_factory(instance=instance, service=service)

        inquiry = active_inquiry_factory(for_instance=instance)

        answer_factory(
            document=inquiry.child_case.document,
            question_id=distribution_settings["QUESTIONS"]["STATUS"],
            value=inquiry_answer,
        )

    for filters, expected_count in [
        ({"inquiry_answer": ""}, 3),
        ({"inquiry_answer": "inquiry-answer-status-positive"}, 1),
        (
            {
                "inquiry_answer": "inquiry-answer-status-positive,inquiry-answer-status-negative"
            },
            2,
        ),
    ]:
        response = admin_client.get(reverse("instance-list"), data=filters)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["data"]) == expected_count


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_inquiry_and_decision_data(
    db,
    snapshot,
    active_inquiry_factory,
    admin_client,
    be_instance,
    decision_factory,
    be_decision_settings,
):
    active_inquiry_factory(created_at=make_aware(datetime(2022, 9, 1)))
    decision_factory(decision_date=date(2022, 11, 16))

    response = admin_client.get(
        reverse("instance-list"),
        data={"fields[instances]": "decision,decision_date,involved_at"},
    )

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json()["data"][0]["attributes"])


@pytest.mark.parametrize(
    "role__name,instance_state__name,instance__user",
    [("Applicant", "new", lf("admin_user"))],
)
@pytest.mark.parametrize(
    "form_slug,expected_instance_state,expected_work_items",
    [
        (
            "main-form",
            "subm",
            {"create-manual-workitems", "formal-exam", "init-additional-demand"},
        ),
        (
            "voranfrage",
            "init-distribution",
            {"create-manual-workitems", "distribution"},
        ),
        (
            "meldung",
            "decision",
            {"create-manual-workitems", "decision"},
        ),
        (
            "meldung-pv",
            "subm",
            {"create-manual-workitems", "formal-exam", "init-additional-demand"},
        ),
    ],
)
def test_instance_submit_so(
    admin_client,
    application_settings,
    disable_ech0211_settings,
    expected_instance_state,
    expected_work_items,
    form_slug,
    instance_state_factory,
    mock_generate_and_store_pdf,
    mocker,
    settings,
    so_instance,
):
    settings.APPLICATION_NAME = "kt_so"
    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False
    application_settings["SET_SUBMIT_DATE_CAMAC_WORKFLOW"] = False
    application_settings["NOTIFICATIONS"] = {"SUBMIT": [], "SUBMIT_OTHERS": []}

    instance_state_factory(name="init-distribution")
    instance_state_factory(name="decision")
    instance_state_factory(name="subm")

    mocker.patch(
        "camac.instance.serializers.CalumaInstanceSubmitSerializer._send_notification"
    )

    so_instance.case.document.form_id = form_slug
    so_instance.case.document.save()

    response = admin_client.post(reverse("instance-submit", args=[so_instance.pk]))

    so_instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK

    work_items = so_instance.case.work_items.filter(
        status=caluma_workflow_models.WorkItem.STATUS_READY
    ).values_list("task_id", flat=True)

    assert so_instance.instance_state.name == expected_instance_state
    assert set(work_items) == expected_work_items


@pytest.mark.parametrize(
    "role__name,instance_state__name,instance__user",
    [("Applicant", "new", lf("admin_user"))],
)
@pytest.mark.parametrize("bab_question", ["bab", "aushublagerplaetze-oder-baupisten"])
def test_instance_submit_so_bab(
    admin_client,
    application_settings,
    bab_question,
    disable_ech0211_settings,
    instance_state_factory,
    master_data_is_visible_mock,
    mock_generate_and_store_pdf,
    mocker,
    settings,
    so_bab_settings,
    so_instance,
    so_master_data_settings,
    service_factory,
    utils,
):
    settings.APPLICATION_NAME = "kt_so"
    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False
    application_settings["SET_SUBMIT_DATE_CAMAC_WORKFLOW"] = False
    application_settings["NOTIFICATIONS"] = {"SUBMIT": [], "SUBMIT_OTHERS": []}

    service_factory(service_group__name=so_bab_settings["SERVICE_GROUP"])

    instance_state_factory(name="subm")
    mocker.patch(
        "camac.instance.serializers.CalumaInstanceSubmitSerializer._send_notification"
    )

    utils.add_answer(so_instance.case.document, bab_question, f"{bab_question}-ja")

    response = admin_client.post(reverse("instance-submit", args=[so_instance.pk]))

    so_instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert so_instance.case.meta.get("is-bab") is True


@pytest.mark.parametrize(
    "role__name,instance_state__name,instance__user",
    [("Applicant", "new", lf("admin_user"))],
)
def test_instance_submit_so_canton(
    admin_client,
    application_settings,
    disable_ech0211_settings,
    dynamic_option_factory,
    instance_state_factory,
    master_data_is_visible_mock,
    mock_generate_and_store_pdf,
    mocker,
    service_factory,
    set_application_so,
    settings,
    so_bab_settings,
    so_instance,
    so_master_data_settings,
    utils,
):
    settings.APPLICATION_NAME = "kt_so"
    application_settings["SET_SUBMIT_DATE_CAMAC_ANSWER"] = False
    application_settings["SET_SUBMIT_DATE_CAMAC_WORKFLOW"] = False
    application_settings["NOTIFICATIONS"] = {"SUBMIT": [], "SUBMIT_OTHERS": []}

    municipality_service = service_factory(service_group__name="municipality")
    canton_service = service_factory(service_group__name="canton")
    service_factory(service_group__name="service-bab")
    service_factory(service_group__name="canton", service_parent=canton_service)

    instance_state_factory(name="subm")
    mocker.patch(
        "camac.instance.serializers.CalumaInstanceSubmitSerializer._send_notification"
    )

    dynamic_option_factory(
        question_id="gemeinde",
        document=so_instance.case.document,
        slug=str(municipality_service.pk),
        label={"de": municipality_service.name},
    )
    utils.add_answer(
        so_instance.case.document, "gemeinde", str(municipality_service.pk)
    )
    utils.add_answer(
        so_instance.case.document, "kanton-leitbehoerde", "kanton-leitbehoerde-ja"
    )

    response = admin_client.post(reverse("instance-submit", args=[so_instance.pk]))

    so_instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert so_instance.responsible_service() == canton_service
    assert so_instance.case.meta["dossier-number"].startswith(
        str(municipality_service.external_identifier)
    )

    bab_exam = so_instance.case.work_items.get(task_id="material-exam-bab")

    assert bab_exam.status == caluma_workflow_models.WorkItem.STATUS_READY
    assert bab_exam.addressed_groups == [str(canton_service.pk)]


@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize(
    "has_permission, expect_status",
    [
        (True, status.HTTP_204_NO_CONTENT),
        (False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_instance_delete_permissions_module(
    db,
    access_level_factory,
    admin_client,
    admin_user,
    applicant_factory,
    expect_status,
    has_permission,
    so_instance,
    so_permissions_settings,
):
    so_instance.involved_applicants.all().delete()
    role = ROLE_CHOICES.ADMIN.value if has_permission else ROLE_CHOICES.READ_ONLY.value
    applicant_factory(instance=so_instance, invitee=admin_user, role=role)

    permissions_api.grant(
        so_instance,
        grant_type=permissions_api.GRANT_CHOICES.USER.value,
        access_level=access_level_factory(pk="applicant"),
        user=admin_user,
    )

    url = reverse("instance-detail", args=[so_instance.pk])
    response = admin_client.delete(url)

    assert response.status_code == expect_status


@pytest.mark.parametrize(
    "has_permission,expected_status",
    [(True, status.HTTP_201_CREATED), (False, status.HTTP_403_FORBIDDEN)],
)
@pytest.mark.parametrize("instance_state__name", ["rejected"])
def test_copy_rejected_instance(
    db,
    admin_client,
    admin_user,
    applicant_factory,
    application_settings,
    disable_ech0211_settings,
    expected_status,
    has_permission,
    instance_state_factory,
    mock_generate_and_store_pdf,
    set_application_so,
    so_access_levels,
    so_instance,
    so_permissions_settings,
):
    """Make sure the permission 'instance-copy-after-rejection' is checked."""

    application_settings["NOTIFICATIONS"]["SUBMIT"] = []
    instance_state_factory(name="new")

    so_instance.involved_applicants.all().delete()
    role = ROLE_CHOICES.ADMIN.value if has_permission else ROLE_CHOICES.READ_ONLY.value
    applicant_factory(instance=so_instance, invitee=admin_user, role=role)

    permissions_api.grant(
        so_instance,
        grant_type=permissions_api.GRANT_CHOICES.USER.value,
        access_level="applicant",
        user=admin_user,
    )

    response = admin_client.post(
        reverse("instance-list"),
        {
            "data": {
                "type": "instances",
                "attributes": {
                    "copy-source": str(so_instance.pk),
                },
            }
        },
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "has_permission,expected_status",
    [(True, status.HTTP_201_CREATED), (False, status.HTTP_403_FORBIDDEN)],
)
def test_copy_instance_modification(
    db,
    admin_client,
    admin_user,
    applicant_factory,
    application_settings,
    disable_ech0211_settings,
    expected_status,
    has_permission,
    instance_state_factory,
    mock_generate_and_store_pdf,
    set_application_gr,
    gr_access_levels,
    gr_instance,
    gr_permissions_settings,
    gr_project_modification_settings,
):
    """Make sure the permission 'instance-create-modification' is checked."""

    gr_project_modification_settings["ALLOW_FORMS"] = ["main-form"]
    gr_permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    gr_permissions_settings["ACCESS_LEVELS"]["applicant"] = [
        (
            "instance-create-modification",
            HasApplicantRole(["ADMIN"]),
        ),
    ]
    application_settings["NOTIFICATIONS"]["SUBMIT"] = []
    instance_state_factory(name="new")

    gr_instance.involved_applicants.all().delete()
    role = ROLE_CHOICES.ADMIN.value if has_permission else ROLE_CHOICES.READ_ONLY.value
    applicant_factory(instance=gr_instance, invitee=admin_user, role=role)

    permissions_api.grant(
        gr_instance,
        grant_type=permissions_api.GRANT_CHOICES.USER.value,
        access_level="applicant",
        user=admin_user,
    )

    response = admin_client.post(
        reverse("instance-list"),
        {
            "data": {
                "type": "instances",
                "attributes": {
                    "copy-source": str(gr_instance.pk),
                    "is-modification": True,
                },
            }
        },
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize("allow_notification", [True, False])
def test_send_notifications(
    db,
    application_settings,
    instance,
    case_factory,
    answer_factory,
    document_factory,
    notification_template,
    mocker,
    allow_notification,
):
    send_notification_mock = mocker.patch(
        "camac.instance.serializers.CalumaInstanceSubmitSerializer._send_notification",
        return_value=None,
    )
    config_1 = [
        {"template_slug": notification_template.slug, "recipient_types": ["test_a"]}
    ]
    config_2 = [
        {"template_slug": notification_template.slug, "recipient_types": ["test_b"]}
    ]
    application_settings["NOTIFICATIONS"]["SUBMIT_HEAT_GENERATOR_IMMISSIONSSCHUTZ"] = (
        config_1
    )
    application_settings["NOTIFICATIONS"]["SUBMIT_HEAT_GENERATOR"] = config_2
    case_factory(
        instance=instance, document=document_factory(form__slug="heat-generator-v2")
    )

    if allow_notification:
        answer_factory(
            question__slug="heat-generator-combustion-database-v2",
            value="heat-generator-combustion-database-v2-ja",
            document=instance.case.document,
        )

    serializers = CalumaInstanceSubmitSerializer(instance)
    serializers._send_notifications(instance.case)

    calls = [call(**config_2[0])]
    if allow_notification:
        calls = [call(**config_1[0])] + calls
    send_notification_mock.assert_has_calls(calls)
