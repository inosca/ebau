# ../../camac/echbern/schema/ech_0039g0t0_1_0.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:bcbc38fb8188c4bcf01edad60abf73611510bb1e
# Generated 2019-09-26 17:57:08.878072 by PyXB version 1.2.6 using Python 3.6.8.final.0
# Namespace http://www.ech.ch/xmlns/eCH-0039G0T0/1

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:4abb9ae0-e076-11e9-863f-6805ca3ced16')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import camac.echbern.schema.ech_0039_2_0 as _ImportedBinding_camac_echbern_schema_ech_0039_2_0

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.ech.ch/xmlns/eCH-0039G0T0/1', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])
_Namespace_eCH_0039 = _ImportedBinding_camac_echbern_schema_ech_0039_2_0.Namespace
_Namespace_eCH_0039.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Complex type {http://www.ech.ch/xmlns/eCH-0039G0T0/1}messageType with content type ELEMENT_ONLY
class messageType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0039G0T0/1}messageType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'messageType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 27, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}header uses Python identifier header
    __header = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'header'), 'header', '__httpwww_ech_chxmlnseCH_0039G0T01_messageType_httpwww_ech_chxmlnseCH_0039G0T01header', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 29, 3), )

    
    header = property(__header.value, __header.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}content uses Python identifier content_
    __content = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'content'), 'content_', '__httpwww_ech_chxmlnseCH_0039G0T01_messageType_httpwww_ech_chxmlnseCH_0039G0T01content', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 30, 3), )

    
    content_ = property(__content.value, __content.set, None, None)

    _ElementMap.update({
        __header.name() : __header,
        __content.name() : __content
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.messageType = messageType
Namespace.addCategoryObject('typeBinding', 'messageType', messageType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039G0T0/1}eventReport with content type ELEMENT_ONLY
class eventReport_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0039G0T0/1}eventReport with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventReport')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 33, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}reportHeader uses Python identifier reportHeader
    __reportHeader = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'reportHeader'), 'reportHeader', '__httpwww_ech_chxmlnseCH_0039G0T01_eventReport__httpwww_ech_chxmlnseCH_0039G0T01reportHeader', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 35, 3), )

    
    reportHeader = property(__reportHeader.value, __reportHeader.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}report uses Python identifier report
    __report = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'report'), 'report', '__httpwww_ech_chxmlnseCH_0039G0T01_eventReport__httpwww_ech_chxmlnseCH_0039G0T01report', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 36, 3), )

    
    report = property(__report.value, __report.set, None, None)

    _ElementMap.update({
        __reportHeader.name() : __reportHeader,
        __report.name() : __report
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventReport_ = eventReport_
Namespace.addCategoryObject('typeBinding', 'eventReport', eventReport_)


# Complex type {http://www.ech.ch/xmlns/eCH-0039G0T0/1}contentType with content type ELEMENT_ONLY
class contentType (pyxb.binding.basis.complexTypeDefinition):
    """Definiert den fachlichen Inhalt der Nachricht."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'contentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 39, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}directive uses Python identifier directive
    __directive = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'directive'), 'directive', '__httpwww_ech_chxmlnseCH_0039G0T01_contentType_httpwww_ech_chxmlnseCH_0039G0T01directive', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 44, 3), )

    
    directive = property(__directive.value, __directive.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}dossier uses Python identifier dossier
    __dossier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dossier'), 'dossier', '__httpwww_ech_chxmlnseCH_0039G0T01_contentType_httpwww_ech_chxmlnseCH_0039G0T01dossier', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 45, 3), )

    
    dossier = property(__dossier.value, __dossier.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}document uses Python identifier document
    __document = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'document'), 'document', '__httpwww_ech_chxmlnseCH_0039G0T01_contentType_httpwww_ech_chxmlnseCH_0039G0T01document', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 46, 3), )

    
    document = property(__document.value, __document.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}address uses Python identifier address
    __address = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'address'), 'address', '__httpwww_ech_chxmlnseCH_0039G0T01_contentType_httpwww_ech_chxmlnseCH_0039G0T01address', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 47, 3), )

    
    address = property(__address.value, __address.set, None, None)

    _ElementMap.update({
        __directive.name() : __directive,
        __dossier.name() : __dossier,
        __document.name() : __document,
        __address.name() : __address
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.contentType = contentType
Namespace.addCategoryObject('typeBinding', 'contentType', contentType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039G0T0/1}dossierType with content type ELEMENT_ONLY
class dossierType (pyxb.binding.basis.complexTypeDefinition):
    """Einem Dossier können alle anderen Basiskomponenten angehängt / Untergeordnet werden. Der Datentyp wird daher in der Nachrichtengruppe an dieser Stelle neu definiert."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dossierType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 50, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_0039G0T01uuid', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 55, 3), )

    
    uuid = property(__uuid.value, __uuid.set, None, 'UUID: Universally Unique Identifier des\n\t\t\t\t\t\tDossiers. Referenz des Objekts, nicht der Nachricht.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}status uses Python identifier status
    __status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'status'), 'status', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_0039G0T01status', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 61, 3), )

    
    status = property(__status.value, __status.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}titles uses Python identifier titles
    __titles = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'titles'), 'titles', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_0039G0T01titles', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 62, 3), )

    
    titles = property(__titles.value, __titles.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}classification uses Python identifier classification
    __classification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'classification'), 'classification', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_0039G0T01classification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 63, 3), )

    
    classification = property(__classification.value, __classification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}hasPrivacyProtection uses Python identifier hasPrivacyProtection
    __hasPrivacyProtection = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection'), 'hasPrivacyProtection', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_0039G0T01hasPrivacyProtection', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 64, 3), )

    
    hasPrivacyProtection = property(__hasPrivacyProtection.value, __hasPrivacyProtection.set, None, 'Datenschutzstufe: Markierung, die angibt, ob das\n\t\t\t\t\t\tDokument besonders Schützenswerte Personendaten oder Persönlichkeitsprofile\n\t\t\t\t\t\tgemäss Datenschutzrecht enthält.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}caseReferenceLocalId uses Python identifier caseReferenceLocalId
    __caseReferenceLocalId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'caseReferenceLocalId'), 'caseReferenceLocalId', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_0039G0T01caseReferenceLocalId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 71, 3), )

    
    caseReferenceLocalId = property(__caseReferenceLocalId.value, __caseReferenceLocalId.set, None, 'Ordnungsmerkmal: Ordnungsmerkmal des Dossiers,\n\t\t\t\t\t\twelches durch den Absender vergeben wird.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}openingDate uses Python identifier openingDate
    __openingDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'openingDate'), 'openingDate', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_0039G0T01openingDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 77, 3), )

    
    openingDate = property(__openingDate.value, __openingDate.set, None, 'Eröffnungsdatum: Tag, an welchem das Dossier im\n\t\t\t\t\t\tGEVER-System registriert wurde.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}keywords uses Python identifier keywords
    __keywords = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'keywords'), 'keywords', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_0039G0T01keywords', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 83, 3), )

    
    keywords = property(__keywords.value, __keywords.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}comments uses Python identifier comments
    __comments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comments'), 'comments', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_0039G0T01comments', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 84, 3), )

    
    comments = property(__comments.value, __comments.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}subdossier uses Python identifier subdossier
    __subdossier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subdossier'), 'subdossier', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_0039G0T01subdossier', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 85, 3), )

    
    subdossier = property(__subdossier.value, __subdossier.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}document uses Python identifier document
    __document = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'document'), 'document', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_0039G0T01document', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 86, 3), )

    
    document = property(__document.value, __document.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}directive uses Python identifier directive
    __directive = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'directive'), 'directive', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_0039G0T01directive', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 87, 3), )

    
    directive = property(__directive.value, __directive.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}address uses Python identifier address
    __address = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'address'), 'address', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_0039G0T01address', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 88, 3), )

    
    address = property(__address.value, __address.set, None, None)

    
    # Attribute {http://www.ech.ch/xmlns/eCH-0039/2}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_eCH_0039, 'lang'), 'lang', '__httpwww_ech_chxmlnseCH_0039G0T01_dossierType_httpwww_ech_chxmlnseCH_00392lang', pyxb.binding.datatypes.language)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 546, 1)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 90, 2)
    
    lang = property(__lang.value, __lang.set, None, 'Sprache: Attribut zur Angabe des Sprachcodes nach ISO 639-1 (zweistelliger Sprachcode). Ursprünglich RFC 1766.')

    _ElementMap.update({
        __uuid.name() : __uuid,
        __status.name() : __status,
        __titles.name() : __titles,
        __classification.name() : __classification,
        __hasPrivacyProtection.name() : __hasPrivacyProtection,
        __caseReferenceLocalId.name() : __caseReferenceLocalId,
        __openingDate.name() : __openingDate,
        __keywords.name() : __keywords,
        __comments.name() : __comments,
        __subdossier.name() : __subdossier,
        __document.name() : __document,
        __directive.name() : __directive,
        __address.name() : __address
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.dossierType = dossierType
Namespace.addCategoryObject('typeBinding', 'dossierType', dossierType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039G0T0/1}directiveType with content type ELEMENT_ONLY
class directiveType (pyxb.binding.basis.complexTypeDefinition):
    """Einer Anweisung können alle anderen Basiskomponenten angehängt / Untergeordnet werden. Der Datentyp wird daher in der Nachrichtengruppe an dieser Stelle neu definiert."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'directiveType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 92, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpwww_ech_chxmlnseCH_0039G0T01_directiveType_httpwww_ech_chxmlnseCH_0039G0T01uuid', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 97, 3), )

    
    uuid = property(__uuid.value, __uuid.set, None, 'UUID: Universally Unique Identifier der\n\t\t\t\t\t\tAnweisung. Referenz des Objekts, nicht der Nachricht.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}instruction uses Python identifier instruction
    __instruction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'instruction'), 'instruction', '__httpwww_ech_chxmlnseCH_0039G0T01_directiveType_httpwww_ech_chxmlnseCH_0039G0T01instruction', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 103, 3), )

    
    instruction = property(__instruction.value, __instruction.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}serviceId uses Python identifier serviceId
    __serviceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'serviceId'), 'serviceId', '__httpwww_ech_chxmlnseCH_0039G0T01_directiveType_httpwww_ech_chxmlnseCH_0039G0T01serviceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 104, 3), )

    
    serviceId = property(__serviceId.value, __serviceId.set, None, 'Leistungsidentifikation: Identifikation der\n\t\t\t\t\t\tLeistung gemäss eCH-0070 Leistungsinventar eGov CH.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}titles uses Python identifier titles
    __titles = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'titles'), 'titles', '__httpwww_ech_chxmlnseCH_0039G0T01_directiveType_httpwww_ech_chxmlnseCH_0039G0T01titles', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 110, 3), )

    
    titles = property(__titles.value, __titles.set, None, 'Titel: Benennung von Tätigkeit und Gegenstand\n\t\t\t\t\t\tdes Geschäftsvorfalls.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}priority uses Python identifier priority
    __priority = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'priority'), 'priority', '__httpwww_ech_chxmlnseCH_0039G0T01_directiveType_httpwww_ech_chxmlnseCH_0039G0T01priority', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 116, 3), )

    
    priority = property(__priority.value, __priority.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}deadline uses Python identifier deadline
    __deadline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'deadline'), 'deadline', '__httpwww_ech_chxmlnseCH_0039G0T01_directiveType_httpwww_ech_chxmlnseCH_0039G0T01deadline', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 117, 3), )

    
    deadline = property(__deadline.value, __deadline.set, None, 'Bearbeitungsfrist: Tag, an dem die Aktivität erledigt sein soll.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}comments uses Python identifier comments
    __comments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comments'), 'comments', '__httpwww_ech_chxmlnseCH_0039G0T01_directiveType_httpwww_ech_chxmlnseCH_0039G0T01comments', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 122, 3), )

    
    comments = property(__comments.value, __comments.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}dossier uses Python identifier dossier
    __dossier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dossier'), 'dossier', '__httpwww_ech_chxmlnseCH_0039G0T01_directiveType_httpwww_ech_chxmlnseCH_0039G0T01dossier', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 123, 3), )

    
    dossier = property(__dossier.value, __dossier.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}document uses Python identifier document
    __document = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'document'), 'document', '__httpwww_ech_chxmlnseCH_0039G0T01_directiveType_httpwww_ech_chxmlnseCH_0039G0T01document', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 124, 3), )

    
    document = property(__document.value, __document.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039G0T0/1}address uses Python identifier address
    __address = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'address'), 'address', '__httpwww_ech_chxmlnseCH_0039G0T01_directiveType_httpwww_ech_chxmlnseCH_0039G0T01address', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 125, 3), )

    
    address = property(__address.value, __address.set, None, None)

    _ElementMap.update({
        __uuid.name() : __uuid,
        __instruction.name() : __instruction,
        __serviceId.name() : __serviceId,
        __titles.name() : __titles,
        __priority.name() : __priority,
        __deadline.name() : __deadline,
        __comments.name() : __comments,
        __dossier.name() : __dossier,
        __document.name() : __document,
        __address.name() : __address
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.directiveType = directiveType
Namespace.addCategoryObject('typeBinding', 'directiveType', directiveType)


header = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'header'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.headerType, documentation='Definition des Root-Elements für header.xml einer Erstmeldung.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 7, 1))
Namespace.addCategoryObject('elementBinding', header.name().localName(), header)

message = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'message'), messageType, documentation='Definition des Root-Elements für message.xml einer Erstmeldung.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 12, 1))
Namespace.addCategoryObject('elementBinding', message.name().localName(), message)

reportHeader = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reportHeader'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.reportHeaderType, documentation='Definition des Root-Elements für header.xml einer Antwortmeldung.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 17, 1))
Namespace.addCategoryObject('elementBinding', reportHeader.name().localName(), reportHeader)

eventReport = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventReport'), eventReport_, documentation='Definition des Root-Elements für message.xml einer Antwortmeldung.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 22, 1))
Namespace.addCategoryObject('elementBinding', eventReport.name().localName(), eventReport)



messageType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'header'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.headerType, scope=messageType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 29, 3)))

messageType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'content'), contentType, scope=messageType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 30, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(messageType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'header')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 29, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(messageType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'content')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 30, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
messageType._Automaton = _BuildAutomaton()




eventReport_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reportHeader'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.reportHeaderType, scope=eventReport_, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 35, 3)))

eventReport_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'report'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.reportType, scope=eventReport_, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 36, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventReport_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'reportHeader')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 35, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventReport_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'report')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 36, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventReport_._Automaton = _BuildAutomaton_()




contentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'directive'), directiveType, scope=contentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 44, 3)))

contentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dossier'), dossierType, scope=contentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 45, 3)))

contentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'document'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.documentType, scope=contentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 46, 3)))

contentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'address'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.addressType, scope=contentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 47, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 44, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 45, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 46, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 47, 3))
    counters.add(cc_3)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(contentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'directive')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 44, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(contentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dossier')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 45, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(contentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'document')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 46, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(contentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'address')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 47, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
contentType._Automaton = _BuildAutomaton_2()




dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.token, scope=dossierType, documentation='UUID: Universally Unique Identifier des\n\t\t\t\t\t\tDossiers. Referenz des Objekts, nicht der Nachricht.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 55, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'status'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.dossierStatusType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 61, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'titles'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.titlesType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 62, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'classification'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.classificationType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 63, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection'), pyxb.binding.datatypes.boolean, scope=dossierType, documentation='Datenschutzstufe: Markierung, die angibt, ob das\n\t\t\t\t\t\tDokument besonders Schützenswerte Personendaten oder Persönlichkeitsprofile\n\t\t\t\t\t\tgemäss Datenschutzrecht enthält.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 64, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'caseReferenceLocalId'), pyxb.binding.datatypes.token, scope=dossierType, documentation='Ordnungsmerkmal: Ordnungsmerkmal des Dossiers,\n\t\t\t\t\t\twelches durch den Absender vergeben wird.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 71, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'openingDate'), pyxb.binding.datatypes.date, scope=dossierType, documentation='Eröffnungsdatum: Tag, an welchem das Dossier im\n\t\t\t\t\t\tGEVER-System registriert wurde.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 77, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'keywords'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.keywordsType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 83, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comments'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.commentsType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 84, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subdossier'), dossierType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 85, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'document'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.documentType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 86, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'directive'), directiveType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 87, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'address'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.addressType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 88, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 63, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 64, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 71, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 77, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 83, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 84, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 85, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 86, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 87, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 88, 3))
    counters.add(cc_9)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 55, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'status')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 61, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'titles')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 62, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'classification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 63, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 64, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'caseReferenceLocalId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 71, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'openingDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 77, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'keywords')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 83, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comments')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 84, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subdossier')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 85, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'document')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 86, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'directive')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 87, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'address')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 88, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, True) ]))
    st_12._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
dossierType._Automaton = _BuildAutomaton_3()




directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.token, scope=directiveType, documentation='UUID: Universally Unique Identifier der\n\t\t\t\t\t\tAnweisung. Referenz des Objekts, nicht der Nachricht.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 97, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'instruction'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.directiveInstructionType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 103, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'serviceId'), pyxb.binding.datatypes.token, scope=directiveType, documentation='Leistungsidentifikation: Identifikation der\n\t\t\t\t\t\tLeistung gemäss eCH-0070 Leistungsinventar eGov CH.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 104, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'titles'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.titlesType, scope=directiveType, documentation='Titel: Benennung von Tätigkeit und Gegenstand\n\t\t\t\t\t\tdes Geschäftsvorfalls.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 110, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'priority'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.priorityType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 116, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'deadline'), pyxb.binding.datatypes.date, scope=directiveType, documentation='Bearbeitungsfrist: Tag, an dem die Aktivität erledigt sein soll.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 117, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comments'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.commentsType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 122, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dossier'), dossierType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 123, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'document'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.documentType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 124, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'address'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.addressType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 125, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 104, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 110, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 116, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 117, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 122, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 123, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 124, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 125, 3))
    counters.add(cc_7)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 97, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'instruction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 103, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'serviceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 104, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'titles')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 110, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'priority')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 116, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'deadline')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 117, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comments')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 122, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dossier')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 123, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'document')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 124, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'address')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039g0t0_1_0.xsd', 125, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
directiveType._Automaton = _BuildAutomaton_4()

