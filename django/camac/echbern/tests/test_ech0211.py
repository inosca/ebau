import os.path

import xmlschema

from camac.constants.kt_bern import ECH_BASE_DELIVERY
from camac.echbern import formatters


def test_generate_delivery(
    ech_mandatory_answers_einfache_vorabklaerung, ech_instance, multilang
):
    xml_data = formatters.delivery(
        ech_instance,
        ech_mandatory_answers_einfache_vorabklaerung,
        ECH_BASE_DELIVERY,
        eventBaseDelivery=formatters.base_delivery(
            ech_instance, ech_mandatory_answers_einfache_vorabklaerung
        ),
    ).toxml()

    my_dir = os.path.dirname(__file__)
    my_schema = xmlschema.XMLSchema(my_dir + "/../xsd/ech_0211_2_0.xsd")
    my_schema.validate(xml_data)
