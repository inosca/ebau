import os.path

import pytest
import xmlschema
from pytest_lazyfixture import lazy_fixture

from camac.constants.kt_bern import ECH_BASE_DELIVERY
from camac.ech0211 import formatters


@pytest.mark.parametrize(
    "config,appconf,camac_instance",
    [
        (
            "kt_bern",
            lazy_fixture("set_application_be"),
            lazy_fixture("ech_instance_be"),
        ),
        (
            "kt_schwyz",
            lazy_fixture("set_application_sz"),
            lazy_fixture("ech_instance_sz"),
        ),
    ],
)
def test_generate_delivery(
    ech_mandatory_answers_einfache_vorabklaerung,
    camac_instance,
    config,
    appconf,
    multilang,
    snapshot,
):
    base_delivery_formatter = formatters.BaseDeliveryFormatter(config)
    camac_instance.fields.create(name="verfahrensart", value="baubewilligung")
    # kt_bern's formatting requires data standardization in AnswersDict.
    # kt_schwyz relies on MasterData api
    additional_data = (
        {"answers": ech_mandatory_answers_einfache_vorabklaerung}
        if config == "kt_bern"
        else {}
    )
    delivery = formatters.delivery(
        camac_instance,
        ech_mandatory_answers_einfache_vorabklaerung,
        ECH_BASE_DELIVERY,
        eventBaseDelivery=base_delivery_formatter.format_base_delivery(
            camac_instance, **additional_data
        ),
    )
    xml_data = delivery.toxml()
    my_dir = os.path.dirname(__file__)
    my_schema = xmlschema.XMLSchema(my_dir + "/../xsd/ech_0211_2_0.xsd")
    my_schema.validate(xml_data)

    # from xml.dom import minidom
    # pretty_xml = minidom.parseString(xml_data).toprettyxml()
    # snapshot.update(pretty_xml)
