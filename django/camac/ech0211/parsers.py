import xml.sax

from defusedxml.common import DefusedXmlException
from pyxb.exceptions_ import PyXBException
from rest_framework.exceptions import ParseError
from rest_framework_xml.parsers import XMLParser

from camac.caluma.api import CalumaApi
from camac.core.utils import canton_aware

from .constants import ECH0211_NAMESPACES
from .schema.ech_0211_2_0 import CreateFromDocument


class ECHXMLParser(XMLParser):
    """XML parser."""

    media_type = "application/xml"

    def parse(self, stream, media_type=None, parser_context=None):
        """Parse the incoming bytestream as XML and return the resulting data."""

        try:
            return CreateFromDocument(stream.read())
        except PyXBException as exc:
            raise ParseError(f"eCH: XML parse error - {exc.details()}")
        except xml.sax.SAXParseException as exc:
            raise ParseError(f"eCH: invalid XML - {str(exc)}")
        except DefusedXmlException as exc:
            raise ParseError(f"eCH: malicious XML - {str(exc)}")


class ComplexSubmitMappings:
    """
    Implementation of complex mappings used in eventSubmitPlanningPermissionApplication send_handler.

    Specific mappings (e.g. combining two XML fields into one caluma answer) would complicate the
    config-driven approach too much, so we implement them in code.
    """

    @classmethod
    def _xml_value_or_default(cls, tree, xpath, default=""):
        value = tree.xpath(xpath, namespaces=ECH0211_NAMESPACES)
        return value[0].text if value else default

    @classmethod
    def _combine_street_and_housenumber(cls, tree, document, user):
        """Combine street and housenumber from XML into a single Caluma answer."""
        street = cls._xml_value_or_default(
            tree,
            "ech0211:planningPermissionApplication/ech0211:locationAddress/ech0010:street",
            "-",
        )
        number = cls._xml_value_or_default(
            tree,
            "ech0211:planningPermissionApplication/ech0211:locationAddress/ech0010:houseNumber",
        )

        CalumaApi().update_or_create_answer(
            document,
            "street-and-housenumber",
            " ".join([street, number]),
            user,
        )

    @classmethod
    @canton_aware
    def execute(cls, tree, document, user):  # pragma: no cover
        pass

    @classmethod
    def execute_gr(cls, tree, document, user):
        # combine street and housenumber
        cls._combine_street_and_housenumber(tree, document, user)

    @classmethod
    def execute_ag(cls, tree, document, user):
        # combine street and housenumber
        cls._combine_street_and_housenumber(tree, document, user)

        # set municipality for parcel table rows
        municipality = CalumaApi().get_answer_value(
            "gemeinde",
            document.case.instance,
        )

        plots = CalumaApi().get_table_answer(
            "parzelle",
            document.case.instance,
        )

        if plots:
            for row in plots:
                CalumaApi().update_or_create_answer(row, "gemeinde", municipality, user)
