import os.path
from decimal import Decimal

import pytest
import xmlschema

from camac.echbern import formatters
from camac.echbern.schema import ech_0211_2_0 as ns_application


@pytest.mark.skip(
    "sample XML from ZH (https://test.portal.ebaugesuche.zh.ch/swagger-ui.html) is invalid"
)
def test_parse_sample():  # pragma: no cover (because test is skipped, duh!)
    my_path = os.path.dirname(__file__)
    with open(my_path + "/parse_test.xml", "r") as fh_xml:
        xml_data = fh_xml.read()
    result = ns_application.CreateFromDocument(xml_data)
    app_event = result.eventSubmitPlanningPermissionApplication
    app = app_event.planningPermissionApplication

    assert app.constructionCost == Decimal("99999999.25")


def test_generate_delivery(db, mandatory_answers, instance):
    xml_data = formatters.delivery(
        instance,
        mandatory_answers,
        eventBaseDelivery=formatters.base_delivery(instance, mandatory_answers),
    ).toxml()

    my_dir = os.path.dirname(__file__)
    my_schema = xmlschema.XMLSchema(my_dir + "/../xsd/ech_0211_2_0.xsd")
    my_schema.validate(xml_data)
