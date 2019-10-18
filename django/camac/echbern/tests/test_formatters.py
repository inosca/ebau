import logging
import os.path

import xmlschema
from pyxb import IncompleteElementContentError, UnprocessedElementContentError

from camac.echbern import formatters

logger = logging.getLogger(__name__)


def test_base_delivery(mandatory_answers, ech_instance):
    xml = formatters.delivery(
        ech_instance,
        mandatory_answers,
        eventBaseDelivery=formatters.base_delivery(ech_instance, mandatory_answers),
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
    off = formatters.office(ech_instance, {"gemeinde": "Testgemeinde"})
    snapshot.assert_match(off.toxml(element_name="office"))
