from rest_framework_xml.parsers import XMLParser

from .schema.ech_0211_2_0 import CreateFromDocument


class ECHXMLParser(XMLParser):
    """XML parser."""

    media_type = "application/xml"

    def parse(self, stream, media_type=None, parser_context=None):
        """Parse the incoming bytestream as XML and return the resulting data."""
        data = CreateFromDocument(stream.read())
        return data
