import re
import xml.dom.minidom as minidom
from datetime import datetime

import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_form.models import DynamicOption
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.core.management import call_command
from lxml import etree

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
    utils,
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
    ba_work_item = work_item_factory(
        task_id="building-authority", case=ech_instance.case
    )
    utils.add_table_answer(
        ba_work_item.document,
        "baukontrolle-realisierung-table",
        [{"baukontrolle-realisierung-baubeginn": datetime.now()}],
    )
    utils.add_answer(
        ba_work_item.document,
        "bewilligungsverfahren-gr-sitzung-bewilligungsdatum",
        datetime.now(),
    )
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
def ech_instance_be(ech_instance, instance_with_case, caluma_workflow_config_be, utils):
    ech_instance = instance_with_case(ech_instance)
    ech_instance.case.meta["ebau-number"] = "2020-1"

    municipality = ech_instance.instance_services.first().service
    municipality.name = "Testgemeinde"
    municipality.save()
    utils.add_answer(
        ech_instance.case.document,
        "gemeinde",
        str(municipality.pk),
    )
    ech_instance.case.document.dynamicoption_set.update(slug=str(municipality.pk))
    DynamicOption.objects.create(
        document=ech_instance.case.document,
        question_id="gemeinde",
        slug=str(municipality.pk),
        label=municipality.name,
    )

    utils.add_answer(
        ech_instance.case.document, "beschreibung-bauvorhaben", "Testvorhaben"
    )
    utils.add_table_answer(
        ech_instance.case.document,
        "parzelle",
        [
            {
                "parzellennummer": "1586",
                "lagekoordinaten-nord": 1070000.0001,  # too many decimal places
                "lagekoordinaten-ost": 2480000.0,
            }
        ],
    )
    utils.add_answer(ech_instance.case.document, "strasse-flurname", "Teststrasse")
    utils.add_answer(ech_instance.case.document, "nr", "23b")
    utils.add_table_answer(
        ech_instance.case.document,
        "personalien-gesuchstellerin",
        [
            {
                "vorname-gesuchstellerin": "Testvorname",
                "name-gesuchstellerin": "Testname",
                "ort-gesuchstellerin": "Testort",
                "plz-gesuchstellerin": 1234,
                "strasse-gesuchstellerin": "Teststrasse",
                "juristische-person-gesuchstellerin": "Nein",
                "telefon-oder-mobile-gesuchstellerin": int("0311234567"),
                "e-mail-gesuchstellerin": "a@b.ch",
            }
        ],
    )
    utils.add_table_answer(
        ech_instance.case.document,
        "beschreibung-der-prozessart-tabelle",
        [
            {
                "prozessart": {
                    "value": "felssturz",
                    "options": ["felssturz", "fliesslawine"],
                }
            }
        ],
    )
    utils.add_answer(ech_instance.case.document, "gwr-egid", "1738778")
    utils.add_answer(ech_instance.case.document, "effektive-geschosszahl", "2")
    utils.add_answer(
        ech_instance.case.document,
        "nutzungsart",
        ["wohnen"],
        options=["wohnen", "landwirtschaft"],
    )
    utils.add_answer(ech_instance.case.document, "sammelschutzraum", "Ja")
    utils.add_answer(ech_instance.case.document, "baukosten-in-chf", 42)
    utils.add_answer(ech_instance.case.document, "nutzungszone", "Testnutzungszone")
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
