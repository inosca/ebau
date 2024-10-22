from io import StringIO

import pytest
from rest_framework.exceptions import ParseError
from wsgidav.xml_tools import etree as wsgi_dav_etree

from camac.ech0211.parsers import ECHXMLParser
from camac.ech0211.tests.utils import xml_data


def test_malicious_xml_pyxb():
    xml = xml_data("test_malicious_xxe_external")

    with pytest.raises(ParseError) as e:
        ECHXMLParser().parse(StringIO(xml))
    assert "malicious" in str(e.value)


def test_malicious_xml_wsgidav():
    xml = xml_data("test_malicious_xxe")

    with pytest.raises(RuntimeError) as e:
        wsgi_dav_etree.fromstring(xml)
    assert "xxe" in str(e.value)
