import os.path

import pytest
import xmlschema
from pytest_lazyfixture import lazy_fixture

from camac.constants.kt_bern import ECH_BASE_DELIVERY
from camac.ech0211 import formatters


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize(
    "config,appconf,camac_instance,_master_data_settings",
    [
        (
            "kt_gr",
            lazy_fixture("set_application_gr"),
            lazy_fixture("ech_instance_gr"),
            lazy_fixture("gr_master_data_settings"),
        ),
        (
            "kt_bern",
            lazy_fixture("set_application_be"),
            lazy_fixture("ech_instance_be"),
            lazy_fixture("be_master_data_settings"),
        ),
        (
            "kt_schwyz",
            lazy_fixture("set_application_sz"),
            lazy_fixture("ech_instance_sz"),
            lazy_fixture("sz_master_data_settings"),
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
    _master_data_settings,
    reload_ech0211_urls,
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


@pytest.mark.parametrize(
    "input,expected",
    [
        ("Testweg 12a", ("Testweg", "12a")),
        ("Teststrasse", ("Teststrasse", None)),
        ("Test 12a, Beispiel 2b", ("Test 12a, Beispiel 2b", None)),
    ],
)
def test_split_street_and_housenumber(input, expected):
    assert formatters.split_street_and_housenumber(input) == expected
