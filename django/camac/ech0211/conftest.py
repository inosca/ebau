import re
import xml.dom.minidom as minidom

import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.core.management import call_command
from lxml import etree

from camac.ech0211.data_preparation import slugs_baugesuch, slugs_vorabklaerung_einfach
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.serializers import SUBMIT_DATE_FORMAT


@pytest.mark.freeze_time("2020-2-2")
@pytest.fixture
def ech_instance_sz(
    attachment_factory,
    caluma_workflow_config_sz,
    ech_instance,
    sz_person_factory,
    form_factory,
    instance_factory,
    instance_with_case,
    caluma_config_sz,
    work_item_factory,
    location,
):

    ech_instance = instance_with_case(ech_instance)

    for role in [
        "bauherrschaft",
        "vertreter-mit-vollmacht",
        "grundeigentumerschaft",
        "projektverfasser-planer",
    ]:
        title = None
        if role == "bauherrschaft":
            title = "Firma"
        sz_person_factory(ech_instance, role, title=title)

    ech_instance.identifier = CreateInstanceLogic.generate_identifier(
        ech_instance, prefix="TEST"
    )
    instance_with_case(instance_factory(identifier=ech_instance.identifier))
    ech_instance.form = form_factory(name="application_type")
    attachment_factory(instance=ech_instance)
    call_command("loaddata", "/app/kt_schwyz/config/buildingauthority.json")
    work_item_factory(task_id="building-authority", case=ech_instance.case)
    ech_instance.location = location
    ech_instance.save()
    return ech_instance


@pytest.fixture
def ech_instance(
    db,
    admin_user,
    instance_service_factory,
    service_t_factory,
    instance_with_case,
    instance_factory,
    applicant_factory,
):
    instance = instance_factory(pk=2323)
    inst_serv = instance_service_factory(
        instance__user=admin_user,
        instance=instance,
        service__name=None,
        service__city=None,
        service__zip="3400",
        service__address="Teststrasse 23",
        service__email="burgdorf@example.com",
        service__trans=None,
        service__service_group__name="municipality",
        active=1,
    )

    service_t_factory(
        service=inst_serv.service,
        language="de",
        name="Leitbehörde Burgdorf",
        city="Burgdorf",
    )

    applicant_factory(invitee=admin_user, instance=instance)

    return instance


@pytest.fixture
def ech_instance_be(ech_instance, instance_with_case, caluma_workflow_config_be):
    ech_instance = instance_with_case(ech_instance)
    ech_instance.case.meta["ebau-number"] = "2020-1"
    return ech_instance


@pytest.fixture
def ech_instance_case(ech_instance_be, caluma_admin_user):
    def wrapper(is_vorabklaerung=False):
        workflow_slug = (
            "preliminary-clarification" if is_vorabklaerung else "building-permit"
        )

        case = workflow_api.start_case(
            workflow=caluma_workflow_models.Workflow.objects.get(pk=workflow_slug),
            form=caluma_form_models.Form.objects.get(slug="main-form"),
            user=caluma_admin_user,
            meta={
                "submit-date": ech_instance_be.creation_date.strftime(
                    SUBMIT_DATE_FORMAT
                ),
                "paper-submit-date": ech_instance_be.creation_date.strftime(
                    SUBMIT_DATE_FORMAT
                ),
            },
        )

        ech_instance_be.case = case
        ech_instance_be.save()

        return case

    return wrapper


def fill_document_ech(document, data):
    for question_slug, value in data:
        question = caluma_form_models.Question.objects.get(slug=question_slug)
        if question.type == "dynamic_choice":
            caluma_form_models.DynamicOption.objects.create(
                document=document, question=question, slug=value, label=value
            )
        if question.type == "dynamic_multiple_choice":  # pragma: no cover
            for v in value:
                caluma_form_models.DynamicOption.objects.create(
                    document=document, question=question, slug=v, label=v
                )
        caluma_form_models.Answer.objects.create(
            document=document, value=value, question=question
        )


@pytest.fixture
def vorabklaerung_einfach_filled(
    caluma_config_bern, instance_with_case, instance_factory
):
    instance = instance_with_case(
        instance_factory(),
        workflow="preliminary-clarification",
        form="vorabklaerung-einfach",
    )

    document = instance.case.document
    fill_document_ech(document, slugs_vorabklaerung_einfach["top"])
    return document


@pytest.fixture
def baugesuch_filled(
    caluma_config_bern,
    answer_factory,
    answer_document_factory,
    instance_with_case,
    instance_factory,
):
    instance = instance_with_case(
        instance_factory(), workflow="building-permit", form="baugesuch-generell-v2"
    )

    document = instance.case.document

    for key, data in slugs_baugesuch.items():
        if key == "top":
            fill_document_ech(document, data)
            continue
        t_question = caluma_form_models.Question.objects.get(slug=key)
        t_answer = answer_factory(document=document, question=t_question)
        for row in data:
            row_answer_doc = answer_document_factory(answer=t_answer)
            fill_document_ech(row_answer_doc.document, row)

    return document


@pytest.fixture
def ech_snapshot(snapshot):
    def wrapper(raw_xml):
        pretty_xml = minidom.parseString(
            etree.tostring(
                etree.fromstring(raw_xml),
                method="c14n",  # c14n forces attributes to be sorted
            )
        ).toprettyxml()

        for search, replace in [
            (
                r"(<ns\d+:dossierIdentification>).+(</ns\d+:dossierIdentification>)",
                r"\1<!-- INSTANCE_ID -->\2",
            ),
            (
                r"(<ns\d+:organisationId>).+(</ns\d+:organisationId>)",
                r"\1<!-- ORGANISATION_ID -->\2",
            ),
            (
                r"(<ns\d+:messageId>).+(</ns\d+:messageId>)",
                r"\1<!-- MESSAGE_ID -->\2",
            ),
            (
                r"(<ns\d+:productVersion>).+(</ns\d+:productVersion>)",
                r"\1<!-- VERSION -->\2",
            ),
            (
                r"(<ns\d+:pathFileName>)(.*attachments=)\d+(</ns\d+:pathFileName>)",
                r"\1\2<!-- ATTACHMENT_ID -->\3",
            ),
        ]:

            pretty_xml = re.sub(
                search,
                replace,
                pretty_xml,
            )

        return snapshot.assert_match(pretty_xml)

    return wrapper
