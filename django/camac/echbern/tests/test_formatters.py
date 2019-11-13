import logging
import os.path

import pytest
import xmlschema
from pyxb import IncompleteElementContentError, UnprocessedElementContentError

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
):
    ech_mandatory_answers = ech_mandatory_answers_baugesuch
    if form == "baugesuch":
        ech_mandatory_answers_baugesuch["baukosten-in-chf"] = 999  # too cheap
    elif form == "einfache vorabklaerung":
        ech_mandatory_answers = ech_mandatory_answers_einfache_vorabklaerung
    elif form == "vollstaendige vorabklaerung":
        ech_mandatory_answers = ech_mandatory_answers_vollstaendige_vorabklaerung

    xml = formatters.delivery(
        ech_instance,
        ech_mandatory_answers,
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


def test_office(ech_instance, snapshot):
    off = formatters.office(ech_instance.active_service)
    snapshot.assert_match(off.toxml(element_name="office"))
