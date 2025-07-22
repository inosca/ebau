import xml.sax

import defusedxml
import defusedxml.expatreader
import defusedxml.sax
import lxml.etree
import pyxb.utils.saxutils
import wsgidav.xml_tools


def safe_xml_make_parser(**kwargs):
    """
    Patched pyxb.utils.saxutils.make_parser to prevent XML vulnerabilities.

    This uses the make_parser from defusedxml to check if any forbidden elements are in the XML.
    Thereby preventing XXE.
    """
    # simplified pyxb implementation
    content_handler_constructor = kwargs.pop(
        "content_handler_constructor", pyxb.utils.saxutils.BaseSAXHandler
    )
    content_handler = kwargs.pop("content_handler", None)
    if content_handler is None:  # pragma: no cover
        content_handler = content_handler_constructor(**kwargs)
    parser = defusedxml.expatreader.create_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, True)
    parser.setFeature(xml.sax.handler.feature_namespace_prefixes, False)
    parser.setContentHandler(content_handler)
    # defusedxml flags
    parser.setErrorHandler(xml.sax.ErrorHandler())
    parser.forbid_dtd = True
    parser.forbid_entities = True
    parser.forbid_external = True
    return parser


# Monkey patching is needed as the parser pyxb uses can not be replaced by the user.
pyxb.utils.saxutils.make_parser = safe_xml_make_parser

lxml_fromstring = lxml.etree.fromstring


def safe_lxml_fromstring(content: str, parser=None):
    """
    Patched lxml.etree.fromstring to prevent XML vulnerabilities.

    Checks parsed XML for forbidden entities.
    Parsing is safe in lxml by default, but forbidden entities can still exist.
    """
    root = lxml_fromstring(content, parser=parser)
    docinfo = root.getroottree().docinfo

    for dtd in (docinfo.internalDTD, docinfo.externalDTD):
        if dtd is None:
            continue
        for entity in dtd.iterentities():
            raise RuntimeError(
                "Forbidden entity in XML content: "
                f"Name: {entity.name} "
                f"Content: {entity.content}"
            )

    return root


# Monkey patching lxml directly is needed as the parser wsgiDAV uses can not be replaced by the user.
lxml.etree.fromstring = safe_lxml_fromstring
wsgidav.xml_tools.etree = lxml.etree
