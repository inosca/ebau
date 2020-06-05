import logging
import os.path
import xml.dom.minidom as minidom

import pytest
import xmlschema
from pyxb import IncompleteElementContentError, UnprocessedElementContentError

from camac.constants.kt_bern import ECH_BASE_DELIVERY
from camac.echbern import formatters

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "form", ["baugesuch", "einfache vorabklaerung", "vollstaendige vorabklaerung"]
)
def test_base_delivery(
    form,
    ech_mandatory_answers_baugesuch,
    ech_mandatory_answers_einfache_vorabklaerung,
    ech_mandatory_answers_vollstaendige_vorabklaerung,
    ech_instance,
    multilang,
):
    ech_mandatory_answers = ech_mandatory_answers_baugesuch
    if form == "baugesuch":
        ech_mandatory_answers_baugesuch["baukosten-in-chf"] = 999  # too cheap
    elif form == "einfache vorabklaerung":
        ech_mandatory_answers = ech_mandatory_answers_einfache_vorabklaerung
        ech_mandatory_answers[
            "ort-gesuchstellerin"
        ] = ""  # implicitly test filling up strings to min_length
        # implicitly test empty coordinates
        ech_mandatory_answers["lagekoordinaten-nord-einfache-vorabklaerung"] = None
        ech_mandatory_answers["lagekoordinaten-ost-einfache-vorabklaerung"] = None

    elif form == "vollstaendige vorabklaerung":
        ech_mandatory_answers = ech_mandatory_answers_vollstaendige_vorabklaerung

    xml = formatters.delivery(
        ech_instance,
        ech_mandatory_answers,
        ECH_BASE_DELIVERY,
        eventBaseDelivery=formatters.base_delivery(ech_instance, ech_mandatory_answers),
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


def test_office(ech_instance, snapshot, multilang):
    off = formatters.office(ech_instance.active_service())
    snapshot.assert_match(off.toxml(element_name="office"))


@pytest.mark.parametrize("amount", [0, 1, 2])
@pytest.mark.parametrize("with_display_name", [True, False])
def test_get_documents(db, attachment_factory, amount, with_display_name, snapshot):
    context = {}
    if with_display_name:
        context = {"displayName": "baz"}
    uuids = [
        "7604864d-fada-4431-b63b-fc9f4915233d",
        "23daf554-c2f5-4aa2-b5f2-734a96ed84d8",
    ]
    attachments = [
        attachment_factory(
            name="foo.bar",
            context=context,
            attachment_id=count,
            uuid=uuids[count - 1],
            mime_type="application/pdf",
        )
        for count in range(1, amount + 1)
    ]
    xml = formatters.get_documents(attachments)

    assert xml

    xml_documents = []

    for doc in xml:
        try:
            xml_data = doc.toxml(element_name="doc")
            pretty = minidom.parseString(xml_data).toprettyxml()
            xml_documents.append(pretty)
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise
    snapshot.assert_match(xml_documents)
