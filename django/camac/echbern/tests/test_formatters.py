import os.path

import xmlschema

from camac.echbern import formatters


def test_base_delivery(db, mandatory_answers, instance):
    xml = formatters.delivery(
        instance,
        mandatory_answers,
        eventBaseDelivery=formatters.base_delivery(instance, mandatory_answers),
    )
    assert xml

    my_dir = os.path.dirname(__file__)
    my_schema = xmlschema.XMLSchema(my_dir + "/../xsd/ech_0211_2_0.xsd")

    xml_data = xml.toxml()
    my_schema.validate(xml_data)


def test_office(db, instance):
    off = formatters.office(instance)
    assert off.toxml(element_name="office") == (
        '<?xml version="1.0" ?><office xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" '
        'xmlns:ns2="http://www.ech.ch/xmlns/eCH-0097/2" '
        'xmlns:ns3="http://www.ech.ch/xmlns/eCH-0007/6"><ns1:entryOfficeIdentification>'
        "<ns2:localOrganisationId>"
        "<ns2:organisationIdCategory>blah</ns2:organisationIdCategory>"
        "<ns2:organisationId>1234</ns2:organisationId>"
        "</ns2:localOrganisationId><ns2:organisationName>asfdasdfasdf</ns2:organisationName>"
        "</ns1:entryOfficeIdentification><ns1:municipality>"
        "<ns3:municipalityName>Bern</ns3:municipalityName><ns3:cantonAbbreviation>BE"
        "</ns3:cantonAbbreviation></ns1:municipality></office>"
    )
