import logging
import os.path

import pytest
import xmlschema
from caluma.caluma_workflow.api import (
    cancel_work_item,
    complete_work_item,
    skip_work_item,
)
from django.core.management import call_command
from pyxb import IncompleteElementContentError, UnprocessedElementContentError

from camac.constants.kt_bern import ECH_BASE_DELIVERY
from camac.document.models import Attachment
from camac.ech0211 import formatters
from camac.ech0211.formatters import determine_decision_state

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "form",
    ["baugesuch", "einfache vorabklaerung", "vollstaendige vorabklaerung"],
)
def test_base_delivery(
    form,
    ech_mandatory_answers_baugesuch,
    ech_mandatory_answers_einfache_vorabklaerung,
    ech_mandatory_answers_vollstaendige_vorabklaerung,
    set_application_be,
    ech_instance_be,
    multilang,
):

    ech_mandatory_answers = ech_mandatory_answers_baugesuch
    if form == "baugesuch":
        ech_mandatory_answers_baugesuch["baukosten-in-chf"] = 999  # too cheap
        ech_mandatory_answers_baugesuch["parzelle"][0][
            "lagekoordinaten-nord"
        ] = 1070500.0001  # too many decimal places
        ech_mandatory_answers_baugesuch["parzelle"][0][
            "lagekoordinaten-ost"
        ] = 2480034.0
    elif form == "einfache vorabklaerung":
        ech_mandatory_answers = ech_mandatory_answers_einfache_vorabklaerung
        ech_mandatory_answers[
            "ort-grundstueck"
        ] = ""  # implicitly test filling up strings to min_length
        # implicitly test empty coordinates
        ech_mandatory_answers["parzelle"][0]["lagekoordinaten-nord"] = None
        ech_mandatory_answers["parzelle"][0]["lagekoordinaten-ost"] = None

    elif form == "vollstaendige vorabklaerung":
        ech_mandatory_answers = ech_mandatory_answers_vollstaendige_vorabklaerung

    configured_base_delivery_formatter = formatters.BaseDeliveryFormatter(
        config="kt_bern"
    )

    xml = formatters.delivery(
        ech_instance_be,
        ech_mandatory_answers,
        ECH_BASE_DELIVERY,
        eventBaseDelivery=configured_base_delivery_formatter.format_base_delivery(
            ech_instance_be, answers=ech_mandatory_answers
        ),
    )

    assert xml

    my_dir = os.path.dirname(__file__)
    my_schema = xmlschema.XMLSchema(my_dir + "/../xsd/ech_0211_2_0.xsd")
    try:
        xml_data = xml.toxml()
    except (
        IncompleteElementContentError,
        UnprocessedElementContentError,
    ) as e:  # pragma: no cover
        logger.error(e.details())
        raise

    my_schema.validate(xml_data)


def test_office(ech_instance_be, ech_snapshot, multilang):
    off = formatters.office(
        ech_instance_be.responsible_service(filter_type="municipality"),
        organization_category="ebaube",
        canton="BE",
    )
    ech_snapshot(off.toxml(element_name="office"))


@pytest.mark.parametrize("amount", [0, 1, 2])
@pytest.mark.parametrize("with_display_name", [True, False])
def test_get_documents(db, attachment_factory, amount, with_display_name, ech_snapshot):
    context = {}
    if with_display_name:
        context = {"displayName": "baz"}
    uuids = [
        "7604864d-fada-4431-b63b-fc9f4915233d",
        "23daf554-c2f5-4aa2-b5f2-734a96ed84d8",
    ]
    for count in range(1, amount + 1):
        attachment_factory(
            name="foo.bar",
            context=context,
            attachment_id=count,
            uuid=uuids[count - 1],
            mime_type="application/pdf",
        )

    xml = formatters.get_documents(Attachment.objects.filter(uuid__in=uuids))

    assert xml

    for doc in xml:
        try:
            ech_snapshot(doc.toxml(element_name="doc"))
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


@pytest.mark.freeze_time("2022-01-01")
@pytest.mark.parametrize(
    "skip,task_id,work_item_action,expected_decision,expected_state",
    [
        (
            ["submit", "complete-check", "skip-circulation"],
            "make-decision",
            cancel_work_item,
            4,  # negative
            "denied",
        ),
        (
            ["submit", "complete-check", "skip-circulation"],
            "make-decision",
            complete_work_item,
            1,  # positive
            "accepted",
        ),
        (["submit"], "reject-form", complete_work_item, 3, "negative"),
    ],
)
def test_decision_formatter(
    ech_instance_sz,
    instance_state_factory,
    caluma_config_sz,
    set_application_sz,
    skip,
    task_id,
    work_item_action,
    expected_decision,
    expected_state,
    caluma_admin_user,
):
    call_command("loaddata", "/app/kt_schwyz/config/instance.json")

    instance_state_factory(name=expected_state)
    for task in skip:
        t = ech_instance_sz.case.work_items.get(task_id=task)
        skip_work_item(t, caluma_admin_user)
    work_item_action(
        ech_instance_sz.case.work_items.get(task_id=task_id),
        caluma_admin_user,
        {"no-notification": True},
    )
    decision, decision_date = determine_decision_state(ech_instance_sz)
    assert decision == expected_decision
