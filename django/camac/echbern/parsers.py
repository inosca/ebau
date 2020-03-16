from xml.sax import SAXParseException

from pyxb.exceptions_ import PyXBException
from rest_framework.exceptions import ParseError
from rest_framework_xml.parsers import XMLParser

from .schema.ech_0211_2_0 import CreateFromDocument


class ECHXMLParser(XMLParser):
    """XML parser."""

    media_type = "application/xml"

    def parse(self, stream, media_type=None, parser_context=None):
        """Parse the incoming bytestream as XML and return the resulting data."""

        try:
            return CreateFromDocument(stream.read())
        except PyXBException as exc:
            raise ParseError(f"eCH XML parse error - {str(exc)}")
        except SAXParseException as exc:
            raise ParseError(f"eCH: invalid xml - {str(exc)}")
