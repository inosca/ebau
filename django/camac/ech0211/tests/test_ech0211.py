import os.path

import pytest
import xmlschema
from pytest_lazyfixture import lazy_fixture

from camac.constants.kt_bern import ECH_BASE_DELIVERY
from camac.ech0211 import formatters


@pytest.mark.freeze_time("2022-06-03")
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
    camac_instance,
    config,
    appconf,
    multilang,
    ech_snapshot,
    master_data_is_visible_mock,
):
    base_delivery_formatter = formatters.BaseDeliveryFormatter()

    if config == "kt_schwyz":
        camac_instance.fields.create(name="verfahrensart", value="baubewilligung")
    else:
        camac_instance.case.document.form.name = "Einfache Vorabklärung"
        camac_instance.case.document.form.save()

    delivery = formatters.delivery(
        camac_instance,
        subject="Einfache Vorabklärung",
        message_type=ECH_BASE_DELIVERY,
        eventBaseDelivery=base_delivery_formatter.format_base_delivery(camac_instance),
    )
    xml_data = delivery.toxml()
    my_dir = os.path.dirname(__file__)
    my_schema = xmlschema.XMLSchema(my_dir + "/../xsd/ech_0211_2_0.xsd")
    my_schema.validate(xml_data)

    ech_snapshot(xml_data)
