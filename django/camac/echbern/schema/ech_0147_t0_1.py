# ../../camac/echbern/schema/ech_0147_t0_1.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:bad86dca18ccfe646d0ff5f8e36af6e7d4b05834
# Generated 2019-09-26 17:57:08.875990 by PyXB version 1.2.6 using Python 3.6.8.final.0
# Namespace http://www.ech.ch/xmlns/eCH-0147/T0/1 [xmlns:eCH-0147T0]

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
import camac.echbern.schema.ech_0046_1_0 as _ImportedBinding_camac_echbern_schema_ech_0046_1_0
import camac.echbern.schema.ech_0058_3_0 as _ImportedBinding_camac_echbern_schema_ech_0058_3_0

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.ech.ch/xmlns/eCH-0147/T0/1', create_if_missing=True)
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


# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0147/T0/1}errorKindType
class errorKindType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """Fehlermeldung für negative Antwortmeldungen."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'errorKindType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 168, 1)
    _Documentation = 'Fehlermeldung für negative Antwortmeldungen.'
errorKindType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=errorKindType, enum_prefix=None)
errorKindType.notValid = errorKindType._CF_enumeration.addEnumeration(unicode_value='notValid', tag='notValid')
errorKindType.fileWithoutReference = errorKindType._CF_enumeration.addEnumeration(unicode_value='fileWithoutReference', tag='fileWithoutReference')
errorKindType.referenceWithoutFile = errorKindType._CF_enumeration.addEnumeration(unicode_value='referenceWithoutFile', tag='referenceWithoutFile')
errorKindType.unknownRecipient = errorKindType._CF_enumeration.addEnumeration(unicode_value='unknownRecipient', tag='unknownRecipient')
errorKindType._InitializeFacetMap(errorKindType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'errorKindType', errorKindType)
_module_typeBindings.errorKindType = errorKindType

# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}addressType with content type ELEMENT_ONLY
class addressType (pyxb.binding.basis.complexTypeDefinition):
    """Adresse: Basiskomponente zur Abbildung von Kontaktinformationen. Basiert auf eCH-0046 Datenstandard Kontakt."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'addressType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpwww_ech_chxmlnseCH_0147T01_addressType_httpwww_ech_chxmlnseCH_0147T01uuid', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 13, 3), )

    
    uuid = property(__uuid.value, __uuid.set, None, 'UUID: Universally Unique Identifier der Adresse. Referenz des Objekts, nicht der Nachricht.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}transactionRole uses Python identifier transactionRole
    __transactionRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'transactionRole'), 'transactionRole', '__httpwww_ech_chxmlnseCH_0147T01_addressType_httpwww_ech_chxmlnseCH_0147T01transactionRole', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 18, 3), )

    
    transactionRole = property(__transactionRole.value, __transactionRole.set, None, 'Transaktionsrolle: Angabe, ob es sich bei der Rolle um einen Absender, Emfpänger oder Beteiligten (Kopie an) handelt.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}position uses Python identifier position
    __position = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'position'), 'position', '__httpwww_ech_chxmlnseCH_0147T01_addressType_httpwww_ech_chxmlnseCH_0147T01position', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 23, 3), )

    
    position = property(__position.value, __position.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}contact uses Python identifier contact
    __contact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'contact'), 'contact', '__httpwww_ech_chxmlnseCH_0147T01_addressType_httpwww_ech_chxmlnseCH_0147T01contact', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 24, 3), )

    
    contact = property(__contact.value, __contact.set, None, 'Kontaktinformatione: Implementiert eCH-0046 Datenstandard Kontakt.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}applicationCustom uses Python identifier applicationCustom
    __applicationCustom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), 'applicationCustom', '__httpwww_ech_chxmlnseCH_0147T01_addressType_httpwww_ech_chxmlnseCH_0147T01applicationCustom', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 29, 3), )

    
    applicationCustom = property(__applicationCustom.value, __applicationCustom.set, None, None)

    _ElementMap.update({
        __uuid.name() : __uuid,
        __transactionRole.name() : __transactionRole,
        __position.name() : __position,
        __contact.name() : __contact,
        __applicationCustom.name() : __applicationCustom
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.addressType = addressType
Namespace.addCategoryObject('typeBinding', 'addressType', addressType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}addressesType with content type ELEMENT_ONLY
class addressesType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}addressesType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'addressesType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 32, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}address uses Python identifier address
    __address = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'address'), 'address', '__httpwww_ech_chxmlnseCH_0147T01_addressesType_httpwww_ech_chxmlnseCH_0147T01address', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 34, 3), )

    
    address = property(__address.value, __address.set, None, None)

    _ElementMap.update({
        __address.name() : __address
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.addressesType = addressesType
Namespace.addCategoryObject('typeBinding', 'addressesType', addressesType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}applicationCustomType with content type MIXED
class applicationCustomType (pyxb.binding.basis.complexTypeDefinition):
    """Anwendungsspezifische Erweiterung: Zusätzliche Anwendungsspezifsiche Metadaten für den Austausch.Information supplémentaire pour l'échange entre applications"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'applicationCustomType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 37, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.applicationCustomType = applicationCustomType
Namespace.addCategoryObject('typeBinding', 'applicationCustomType', applicationCustomType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}documentType with content type ELEMENT_ONLY
class documentType (pyxb.binding.basis.complexTypeDefinition):
    """Dokument (Unterlage) zur Abbildung der Metadaten von Dokumenten und Unterlagen."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'documentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 46, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01uuid', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 51, 3), )

    
    uuid = property(__uuid.value, __uuid.set, None, 'UUID: Universally Unique Identifier des Dokuments. Referenz des Objekts, nicht der Nachricht.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}titles uses Python identifier titles
    __titles = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'titles'), 'titles', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01titles', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 56, 3), )

    
    titles = property(__titles.value, __titles.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}status uses Python identifier status
    __status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'status'), 'status', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01status', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 57, 3), )

    
    status = property(__status.value, __status.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}files uses Python identifier files
    __files = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'files'), 'files', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01files', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 58, 3), )

    
    files = property(__files.value, __files.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}classification uses Python identifier classification
    __classification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'classification'), 'classification', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01classification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 59, 3), )

    
    classification = property(__classification.value, __classification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}openToThePublic uses Python identifier openToThePublic
    __openToThePublic = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'openToThePublic'), 'openToThePublic', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01openToThePublic', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 60, 3), )

    
    openToThePublic = property(__openToThePublic.value, __openToThePublic.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}hasPrivacyProtection uses Python identifier hasPrivacyProtection
    __hasPrivacyProtection = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection'), 'hasPrivacyProtection', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01hasPrivacyProtection', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 61, 3), )

    
    hasPrivacyProtection = property(__hasPrivacyProtection.value, __hasPrivacyProtection.set, None, 'Datenschutzstufe: Markierung, die angibt, ob das Dokument besonders Schützenswerte Personendaten oder Persönlichkeitsprofile gemäss Datenschutzrecht enthält.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}openingDate uses Python identifier openingDate
    __openingDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'openingDate'), 'openingDate', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01openingDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 66, 3), )

    
    openingDate = property(__openingDate.value, __openingDate.set, None, 'Eröffnungsdatum: Tag, an dem das Dokument im GEVER-System einem Dossier zugeordnet worden ist.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}owner uses Python identifier owner
    __owner = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'owner'), 'owner', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01owner', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 71, 3), )

    
    owner = property(__owner.value, __owner.set, None, 'Eigentümer: Name des Eigentümers des Dokuments.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}signer uses Python identifier signer
    __signer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'signer'), 'signer', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01signer', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 76, 3), )

    
    signer = property(__signer.value, __signer.set, None, 'Unterzeichner: Person, welche das Dokument unterzeichnet hat oder die Verantwortung dafür übernimmt.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}ourRecordReference uses Python identifier ourRecordReference
    __ourRecordReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ourRecordReference'), 'ourRecordReference', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01ourRecordReference', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 81, 3), )

    
    ourRecordReference = property(__ourRecordReference.value, __ourRecordReference.set, None, 'Unser Aktenzeichen: Referenz auf das entsprechende Dossier des Absenders.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}comments uses Python identifier comments
    __comments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comments'), 'comments', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01comments', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 86, 3), )

    
    comments = property(__comments.value, __comments.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}keywords uses Python identifier keywords
    __keywords = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'keywords'), 'keywords', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01keywords', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 87, 3), )

    
    keywords = property(__keywords.value, __keywords.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}isLeadingDocument uses Python identifier isLeadingDocument
    __isLeadingDocument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'isLeadingDocument'), 'isLeadingDocument', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01isLeadingDocument', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 88, 3), )

    
    isLeadingDocument = property(__isLeadingDocument.value, __isLeadingDocument.set, None, 'Hauptdokument: Angabe, ob es sich um das Hauptdokument (führendes Dokument) handelt.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}sortOrder uses Python identifier sortOrder
    __sortOrder = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sortOrder'), 'sortOrder', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01sortOrder', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 93, 3), )

    
    sortOrder = property(__sortOrder.value, __sortOrder.set, None, 'Sortierfolge: Angabe zur Reihenfolge der Sortierung von Dokumenten.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}documentKind uses Python identifier documentKind
    __documentKind = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'documentKind'), 'documentKind', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01documentKind', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 98, 3), )

    
    documentKind = property(__documentKind.value, __documentKind.set, None, 'Dokumenttyp: Fachliche Beschreibung des Dokuments (z.B. Vertrag, Antrag, Antwort. u.a).')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}applicationCustom uses Python identifier applicationCustom
    __applicationCustom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), 'applicationCustom', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_0147T01applicationCustom', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 103, 3), )

    
    applicationCustom = property(__applicationCustom.value, __applicationCustom.set, None, None)

    
    # Attribute {http://www.ech.ch/xmlns/eCH-0039/2}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_eCH_0039, 'lang'), 'lang', '__httpwww_ech_chxmlnseCH_0147T01_documentType_httpwww_ech_chxmlnseCH_00392lang', pyxb.binding.datatypes.language)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 546, 1)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 105, 2)
    
    lang = property(__lang.value, __lang.set, None, 'Sprache: Attribut zur Angabe des Sprachcodes nach ISO 639-1 (zweistelliger Sprachcode). Ursprünglich RFC 1766.')

    _ElementMap.update({
        __uuid.name() : __uuid,
        __titles.name() : __titles,
        __status.name() : __status,
        __files.name() : __files,
        __classification.name() : __classification,
        __openToThePublic.name() : __openToThePublic,
        __hasPrivacyProtection.name() : __hasPrivacyProtection,
        __openingDate.name() : __openingDate,
        __owner.name() : __owner,
        __signer.name() : __signer,
        __ourRecordReference.name() : __ourRecordReference,
        __comments.name() : __comments,
        __keywords.name() : __keywords,
        __isLeadingDocument.name() : __isLeadingDocument,
        __sortOrder.name() : __sortOrder,
        __documentKind.name() : __documentKind,
        __applicationCustom.name() : __applicationCustom
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.documentType = documentType
Namespace.addCategoryObject('typeBinding', 'documentType', documentType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}documentsType with content type ELEMENT_ONLY
class documentsType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}documentsType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'documentsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 107, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}document uses Python identifier document
    __document = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'document'), 'document', '__httpwww_ech_chxmlnseCH_0147T01_documentsType_httpwww_ech_chxmlnseCH_0147T01document', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 109, 3), )

    
    document = property(__document.value, __document.set, None, None)

    _ElementMap.update({
        __document.name() : __document
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.documentsType = documentsType
Namespace.addCategoryObject('typeBinding', 'documentsType', documentsType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}dossierType with content type ELEMENT_ONLY
class dossierType (pyxb.binding.basis.complexTypeDefinition):
    """Dossier: Basiskomponente zur Abbildung von Dossiers und Subdossiers."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dossierType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 112, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01uuid', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 117, 3), )

    
    uuid = property(__uuid.value, __uuid.set, None, 'UUID: Universally Unique Identifier des Dossiers. Referenz des Objekts, nicht der Nachricht.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}status uses Python identifier status
    __status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'status'), 'status', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01status', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 122, 3), )

    
    status = property(__status.value, __status.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}titles uses Python identifier titles
    __titles = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'titles'), 'titles', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01titles', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 123, 3), )

    
    titles = property(__titles.value, __titles.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}classification uses Python identifier classification
    __classification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'classification'), 'classification', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01classification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 124, 3), )

    
    classification = property(__classification.value, __classification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}hasPrivacyProtection uses Python identifier hasPrivacyProtection
    __hasPrivacyProtection = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection'), 'hasPrivacyProtection', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01hasPrivacyProtection', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 125, 3), )

    
    hasPrivacyProtection = property(__hasPrivacyProtection.value, __hasPrivacyProtection.set, None, 'Datenschutzstufe: Markierung, die angibt, ob das Dokument besonders Schützenswerte Personendaten oder Persönlichkeitsprofile gemäss Datenschutzrecht enthält.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}openToThePublicType uses Python identifier openToThePublicType
    __openToThePublicType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'openToThePublicType'), 'openToThePublicType', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01openToThePublicType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 130, 3), )

    
    openToThePublicType = property(__openToThePublicType.value, __openToThePublicType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}caseReferenceLocalId uses Python identifier caseReferenceLocalId
    __caseReferenceLocalId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'caseReferenceLocalId'), 'caseReferenceLocalId', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01caseReferenceLocalId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 131, 3), )

    
    caseReferenceLocalId = property(__caseReferenceLocalId.value, __caseReferenceLocalId.set, None, 'Ordnungsmerkmal: Ordnungsmerkmal des Dossiers, welches durch den Absender vergeben wird.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}openingDate uses Python identifier openingDate
    __openingDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'openingDate'), 'openingDate', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01openingDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 136, 3), )

    
    openingDate = property(__openingDate.value, __openingDate.set, None, 'Datum: Datum, an welchem das Dossier eröffnet / registriert wurde. ')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}keywords uses Python identifier keywords
    __keywords = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'keywords'), 'keywords', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01keywords', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 141, 3), )

    
    keywords = property(__keywords.value, __keywords.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}comments uses Python identifier comments
    __comments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comments'), 'comments', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01comments', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 142, 3), )

    
    comments = property(__comments.value, __comments.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}links uses Python identifier links
    __links = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'links'), 'links', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01links', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 143, 3), )

    
    links = property(__links.value, __links.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}addresses uses Python identifier addresses
    __addresses = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'addresses'), 'addresses', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01addresses', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 144, 3), )

    
    addresses = property(__addresses.value, __addresses.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}dossiers uses Python identifier dossiers
    __dossiers = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dossiers'), 'dossiers', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01dossiers', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 145, 3), )

    
    dossiers = property(__dossiers.value, __dossiers.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}documents uses Python identifier documents
    __documents = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'documents'), 'documents', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01documents', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 146, 3), )

    
    documents = property(__documents.value, __documents.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}folders uses Python identifier folders
    __folders = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'folders'), 'folders', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01folders', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 147, 3), )

    
    folders = property(__folders.value, __folders.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}applicationCustom uses Python identifier applicationCustom
    __applicationCustom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), 'applicationCustom', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_0147T01applicationCustom', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 148, 3), )

    
    applicationCustom = property(__applicationCustom.value, __applicationCustom.set, None, None)

    
    # Attribute {http://www.ech.ch/xmlns/eCH-0039/2}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_eCH_0039, 'lang'), 'lang', '__httpwww_ech_chxmlnseCH_0147T01_dossierType_httpwww_ech_chxmlnseCH_00392lang', pyxb.binding.datatypes.language)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 546, 1)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 150, 2)
    
    lang = property(__lang.value, __lang.set, None, 'Sprache: Attribut zur Angabe des Sprachcodes nach ISO 639-1 (zweistelliger Sprachcode). Ursprünglich RFC 1766.')

    _ElementMap.update({
        __uuid.name() : __uuid,
        __status.name() : __status,
        __titles.name() : __titles,
        __classification.name() : __classification,
        __hasPrivacyProtection.name() : __hasPrivacyProtection,
        __openToThePublicType.name() : __openToThePublicType,
        __caseReferenceLocalId.name() : __caseReferenceLocalId,
        __openingDate.name() : __openingDate,
        __keywords.name() : __keywords,
        __comments.name() : __comments,
        __links.name() : __links,
        __addresses.name() : __addresses,
        __dossiers.name() : __dossiers,
        __documents.name() : __documents,
        __folders.name() : __folders,
        __applicationCustom.name() : __applicationCustom
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.dossierType = dossierType
Namespace.addCategoryObject('typeBinding', 'dossierType', dossierType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}dossiersType with content type ELEMENT_ONLY
class dossiersType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}dossiersType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dossiersType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 152, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}dossier uses Python identifier dossier
    __dossier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dossier'), 'dossier', '__httpwww_ech_chxmlnseCH_0147T01_dossiersType_httpwww_ech_chxmlnseCH_0147T01dossier', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 154, 3), )

    
    dossier = property(__dossier.value, __dossier.set, None, None)

    _ElementMap.update({
        __dossier.name() : __dossier
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.dossiersType = dossiersType
Namespace.addCategoryObject('typeBinding', 'dossiersType', dossiersType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}errorsType with content type ELEMENT_ONLY
class errorsType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}errorsType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'errorsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 157, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}error uses Python identifier error
    __error = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'error'), 'error', '__httpwww_ech_chxmlnseCH_0147T01_errorsType_httpwww_ech_chxmlnseCH_0147T01error', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 159, 3), )

    
    error = property(__error.value, __error.set, None, None)

    _ElementMap.update({
        __error.name() : __error
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.errorsType = errorsType
Namespace.addCategoryObject('typeBinding', 'errorsType', errorsType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}errorType with content type ELEMENT_ONLY
class errorType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}errorType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'errorType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 162, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}errorKind uses Python identifier errorKind
    __errorKind = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'errorKind'), 'errorKind', '__httpwww_ech_chxmlnseCH_0147T01_errorType_httpwww_ech_chxmlnseCH_0147T01errorKind', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 164, 3), )

    
    errorKind = property(__errorKind.value, __errorKind.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}comments uses Python identifier comments
    __comments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comments'), 'comments', '__httpwww_ech_chxmlnseCH_0147T01_errorType_httpwww_ech_chxmlnseCH_0147T01comments', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 165, 3), )

    
    comments = property(__comments.value, __comments.set, None, None)

    _ElementMap.update({
        __errorKind.name() : __errorKind,
        __comments.name() : __comments
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.errorType = errorType
Namespace.addCategoryObject('typeBinding', 'errorType', errorType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}eventReportType with content type ELEMENT_ONLY
class eventReportType (pyxb.binding.basis.complexTypeDefinition):
    """Definiert das Root-Element für message.xml einer Antwortmeldung."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventReportType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 179, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}reportHeader uses Python identifier reportHeader
    __reportHeader = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'reportHeader'), 'reportHeader', '__httpwww_ech_chxmlnseCH_0147T01_eventReportType_httpwww_ech_chxmlnseCH_0147T01reportHeader', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 184, 3), )

    
    reportHeader = property(__reportHeader.value, __reportHeader.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}report uses Python identifier report
    __report = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'report'), 'report', '__httpwww_ech_chxmlnseCH_0147T01_eventReportType_httpwww_ech_chxmlnseCH_0147T01report', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 185, 3), )

    
    report = property(__report.value, __report.set, None, None)

    _ElementMap.update({
        __reportHeader.name() : __reportHeader,
        __report.name() : __report
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventReportType = eventReportType
Namespace.addCategoryObject('typeBinding', 'eventReportType', eventReportType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}fileType with content type ELEMENT_ONLY
class fileType (pyxb.binding.basis.complexTypeDefinition):
    """Datei: Metadaten der angehängten oder referenzierten
				Datei."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'fileType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 188, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}pathFileName uses Python identifier pathFileName
    __pathFileName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'pathFileName'), 'pathFileName', '__httpwww_ech_chxmlnseCH_0147T01_fileType_httpwww_ech_chxmlnseCH_0147T01pathFileName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 194, 3), )

    
    pathFileName = property(__pathFileName.value, __pathFileName.set, None, 'Pfad: Pfad zur Datei. Dabei kann es sich um einen lokalen Pfad oder eine URL handeln. Der Pfad bildet sich aus Pfad + Name + Extension (Dateiendung). Handelt es sich um eine lokale Referenz innehalb der ZIP-Datei, so beginnt der Pfad mit files/dateiname.extension')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}mimeType uses Python identifier mimeType
    __mimeType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'mimeType'), 'mimeType', '__httpwww_ech_chxmlnseCH_0147T01_fileType_httpwww_ech_chxmlnseCH_0147T01mimeType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 199, 3), )

    
    mimeType = property(__mimeType.value, __mimeType.set, None, 'MIME-Type der Datei.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}internalSortOrder uses Python identifier internalSortOrder
    __internalSortOrder = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'internalSortOrder'), 'internalSortOrder', '__httpwww_ech_chxmlnseCH_0147T01_fileType_httpwww_ech_chxmlnseCH_0147T01internalSortOrder', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 204, 3), )

    
    internalSortOrder = property(__internalSortOrder.value, __internalSortOrder.set, None, 'Sortierfolge: Angabe zur Reihenfolge der Sortierung bei Dokumenten, welche aus mehreren Dateien bestehen.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}version uses Python identifier version
    __version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'version'), 'version', '__httpwww_ech_chxmlnseCH_0147T01_fileType_httpwww_ech_chxmlnseCH_0147T01version', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 209, 3), )

    
    version = property(__version.value, __version.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}hashCode uses Python identifier hashCode
    __hashCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'hashCode'), 'hashCode', '__httpwww_ech_chxmlnseCH_0147T01_fileType_httpwww_ech_chxmlnseCH_0147T01hashCode', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 210, 3), )

    
    hashCode = property(__hashCode.value, __hashCode.set, None, 'Hashwert: Hashwert der Datei.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}hashCodeAlgorithm uses Python identifier hashCodeAlgorithm
    __hashCodeAlgorithm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'hashCodeAlgorithm'), 'hashCodeAlgorithm', '__httpwww_ech_chxmlnseCH_0147T01_fileType_httpwww_ech_chxmlnseCH_0147T01hashCodeAlgorithm', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 215, 3), )

    
    hashCodeAlgorithm = property(__hashCodeAlgorithm.value, __hashCodeAlgorithm.set, None, 'Hashalgorithmus: Abkürzung des Algorithmus welcher zur Bildung des Hashwerts verwendet wurde.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}applicationCustom uses Python identifier applicationCustom
    __applicationCustom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), 'applicationCustom', '__httpwww_ech_chxmlnseCH_0147T01_fileType_httpwww_ech_chxmlnseCH_0147T01applicationCustom', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 220, 3), )

    
    applicationCustom = property(__applicationCustom.value, __applicationCustom.set, None, None)

    
    # Attribute {http://www.ech.ch/xmlns/eCH-0039/2}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_eCH_0039, 'lang'), 'lang', '__httpwww_ech_chxmlnseCH_0147T01_fileType_httpwww_ech_chxmlnseCH_00392lang', pyxb.binding.datatypes.language)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 546, 1)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 222, 2)
    
    lang = property(__lang.value, __lang.set, None, 'Sprache: Attribut zur Angabe des Sprachcodes nach ISO 639-1 (zweistelliger Sprachcode). Ursprünglich RFC 1766.')

    _ElementMap.update({
        __pathFileName.name() : __pathFileName,
        __mimeType.name() : __mimeType,
        __internalSortOrder.name() : __internalSortOrder,
        __version.name() : __version,
        __hashCode.name() : __hashCode,
        __hashCodeAlgorithm.name() : __hashCodeAlgorithm,
        __applicationCustom.name() : __applicationCustom
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.fileType = fileType
Namespace.addCategoryObject('typeBinding', 'fileType', fileType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}filesType with content type ELEMENT_ONLY
class filesType (pyxb.binding.basis.complexTypeDefinition):
    """Dateien: Enthält eine oder mehrere übergebene oder referenzierte Dateien."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'filesType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 224, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}file uses Python identifier file
    __file = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'file'), 'file', '__httpwww_ech_chxmlnseCH_0147T01_filesType_httpwww_ech_chxmlnseCH_0147T01file', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 229, 3), )

    
    file = property(__file.value, __file.set, None, None)

    _ElementMap.update({
        __file.name() : __file
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.filesType = filesType
Namespace.addCategoryObject('typeBinding', 'filesType', filesType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}folderType with content type ELEMENT_ONLY
class folderType (pyxb.binding.basis.complexTypeDefinition):
    """Folder: Ordner, welcher zum Gruppieren von Dokumenten innerhalb eines Dossiers / Subdossiers dient (ein Ordner wird vor der Aussonderung an ein Archiv aufgelöst)."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'folderType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 232, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}folderTitles uses Python identifier folderTitles
    __folderTitles = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'folderTitles'), 'folderTitles', '__httpwww_ech_chxmlnseCH_0147T01_folderType_httpwww_ech_chxmlnseCH_0147T01folderTitles', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 237, 3), )

    
    folderTitles = property(__folderTitles.value, __folderTitles.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}documents uses Python identifier documents
    __documents = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'documents'), 'documents', '__httpwww_ech_chxmlnseCH_0147T01_folderType_httpwww_ech_chxmlnseCH_0147T01documents', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 238, 3), )

    
    documents = property(__documents.value, __documents.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}applicationCustom uses Python identifier applicationCustom
    __applicationCustom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), 'applicationCustom', '__httpwww_ech_chxmlnseCH_0147T01_folderType_httpwww_ech_chxmlnseCH_0147T01applicationCustom', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 239, 3), )

    
    applicationCustom = property(__applicationCustom.value, __applicationCustom.set, None, None)

    _ElementMap.update({
        __folderTitles.name() : __folderTitles,
        __documents.name() : __documents,
        __applicationCustom.name() : __applicationCustom
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.folderType = folderType
Namespace.addCategoryObject('typeBinding', 'folderType', folderType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}foldersType with content type ELEMENT_ONLY
class foldersType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}foldersType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'foldersType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 242, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}folder uses Python identifier folder
    __folder = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'folder'), 'folder', '__httpwww_ech_chxmlnseCH_0147T01_foldersType_httpwww_ech_chxmlnseCH_0147T01folder', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 244, 3), )

    
    folder = property(__folder.value, __folder.set, None, None)

    _ElementMap.update({
        __folder.name() : __folder
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.foldersType = foldersType
Namespace.addCategoryObject('typeBinding', 'foldersType', foldersType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}folderTitlesType with content type ELEMENT_ONLY
class folderTitlesType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}folderTitlesType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'folderTitlesType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 247, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}folderTitle uses Python identifier folderTitle
    __folderTitle = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'folderTitle'), 'folderTitle', '__httpwww_ech_chxmlnseCH_0147T01_folderTitlesType_httpwww_ech_chxmlnseCH_0147T01folderTitle', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 249, 3), )

    
    folderTitle = property(__folderTitle.value, __folderTitle.set, None, None)

    _ElementMap.update({
        __folderTitle.name() : __folderTitle
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.folderTitlesType = folderTitlesType
Namespace.addCategoryObject('typeBinding', 'folderTitlesType', folderTitlesType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}folderTitleType with content type SIMPLE
class folderTitleType (pyxb.binding.basis.complexTypeDefinition):
    """Titel des Ordners: Enthält ein Titel. Die Sprache kann im Attribut angegeben werden."""
    _TypeDefinition = pyxb.binding.datatypes.token
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'folderTitleType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 252, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.token
    
    # Attribute {http://www.ech.ch/xmlns/eCH-0039/2}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_eCH_0039, 'lang'), 'lang', '__httpwww_ech_chxmlnseCH_0147T01_folderTitleType_httpwww_ech_chxmlnseCH_00392lang', pyxb.binding.datatypes.language)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 546, 1)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 258, 4)
    
    lang = property(__lang.value, __lang.set, None, 'Sprache: Attribut zur Angabe des Sprachcodes nach ISO 639-1 (zweistelliger Sprachcode). Ursprünglich RFC 1766.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.folderTitleType = folderTitleType
Namespace.addCategoryObject('typeBinding', 'folderTitleType', folderTitleType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}headerType with content type ELEMENT_ONLY
class headerType (pyxb.binding.basis.complexTypeDefinition):
    """Header: Enthält die Headerinformationen für
				Erstmeldungen und implementiert eCH-0058 Meldungsrahmen."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'headerType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 262, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}senderId uses Python identifier senderId
    __senderId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'senderId'), 'senderId', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01senderId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 268, 3), )

    
    senderId = property(__senderId.value, __senderId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}recipientId uses Python identifier recipientId
    __recipientId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'recipientId'), 'recipientId', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01recipientId', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 269, 3), )

    
    recipientId = property(__recipientId.value, __recipientId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}originalSenderId uses Python identifier originalSenderId
    __originalSenderId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'originalSenderId'), 'originalSenderId', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01originalSenderId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 270, 3), )

    
    originalSenderId = property(__originalSenderId.value, __originalSenderId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}declarationLocalReference uses Python identifier declarationLocalReference
    __declarationLocalReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'declarationLocalReference'), 'declarationLocalReference', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01declarationLocalReference', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 271, 3), )

    
    declarationLocalReference = property(__declarationLocalReference.value, __declarationLocalReference.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}messageId uses Python identifier messageId
    __messageId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageId'), 'messageId', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01messageId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 272, 3), )

    
    messageId = property(__messageId.value, __messageId.set, None, 'Nachrichten-ID: Empfehlung des Einsatzes von\n\t\t\t\t\t\tUUID für die eindeutige Referenz von übermittelten\n\t\t\t\t\t\tNachrichten.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}referenceMessageId uses Python identifier referenceMessageId
    __referenceMessageId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId'), 'referenceMessageId', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01referenceMessageId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 279, 3), )

    
    referenceMessageId = property(__referenceMessageId.value, __referenceMessageId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}uniqueBusinessTransactionId uses Python identifier uniqueBusinessTransactionId
    __uniqueBusinessTransactionId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uniqueBusinessTransactionId'), 'uniqueBusinessTransactionId', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01uniqueBusinessTransactionId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 280, 3), )

    
    uniqueBusinessTransactionId = property(__uniqueBusinessTransactionId.value, __uniqueBusinessTransactionId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}ourBusinessReferenceId uses Python identifier ourBusinessReferenceId
    __ourBusinessReferenceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId'), 'ourBusinessReferenceId', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01ourBusinessReferenceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 281, 3), )

    
    ourBusinessReferenceId = property(__ourBusinessReferenceId.value, __ourBusinessReferenceId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}yourBusinessReferenceId uses Python identifier yourBusinessReferenceId
    __yourBusinessReferenceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId'), 'yourBusinessReferenceId', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01yourBusinessReferenceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 282, 3), )

    
    yourBusinessReferenceId = property(__yourBusinessReferenceId.value, __yourBusinessReferenceId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}messageType uses Python identifier messageType
    __messageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageType'), 'messageType', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01messageType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 283, 3), )

    
    messageType = property(__messageType.value, __messageType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}subMessageType uses Python identifier subMessageType
    __subMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subMessageType'), 'subMessageType', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01subMessageType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 284, 3), )

    
    subMessageType = property(__subMessageType.value, __subMessageType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}messageGroup uses Python identifier messageGroup
    __messageGroup = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageGroup'), 'messageGroup', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01messageGroup', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 285, 3), )

    
    messageGroup = property(__messageGroup.value, __messageGroup.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}sendingApplication uses Python identifier sendingApplication
    __sendingApplication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication'), 'sendingApplication', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01sendingApplication', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 286, 3), )

    
    sendingApplication = property(__sendingApplication.value, __sendingApplication.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}subjects uses Python identifier subjects
    __subjects = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subjects'), 'subjects', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01subjects', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 287, 3), )

    
    subjects = property(__subjects.value, __subjects.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}object uses Python identifier object
    __object = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'object'), 'object', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01object', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 288, 3), )

    
    object = property(__object.value, __object.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}comments uses Python identifier comments
    __comments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comments'), 'comments', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01comments', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 289, 3), )

    
    comments = property(__comments.value, __comments.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}messageDate uses Python identifier messageDate
    __messageDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageDate'), 'messageDate', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01messageDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 290, 3), )

    
    messageDate = property(__messageDate.value, __messageDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}initialMessageDate uses Python identifier initialMessageDate
    __initialMessageDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate'), 'initialMessageDate', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01initialMessageDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 291, 3), )

    
    initialMessageDate = property(__initialMessageDate.value, __initialMessageDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}eventDate uses Python identifier eventDate
    __eventDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventDate'), 'eventDate', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01eventDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 292, 3), )

    
    eventDate = property(__eventDate.value, __eventDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}eventPeriod uses Python identifier eventPeriod
    __eventPeriod = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventPeriod'), 'eventPeriod', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01eventPeriod', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 293, 3), )

    
    eventPeriod = property(__eventPeriod.value, __eventPeriod.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}modificationDate uses Python identifier modificationDate
    __modificationDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'modificationDate'), 'modificationDate', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01modificationDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 294, 3), )

    
    modificationDate = property(__modificationDate.value, __modificationDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}action uses Python identifier action
    __action = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'action'), 'action', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01action', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 295, 3), )

    
    action = property(__action.value, __action.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}testDeliveryFlag uses Python identifier testDeliveryFlag
    __testDeliveryFlag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag'), 'testDeliveryFlag', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01testDeliveryFlag', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 296, 3), )

    
    testDeliveryFlag = property(__testDeliveryFlag.value, __testDeliveryFlag.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}reference uses Python identifier reference
    __reference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'reference'), 'reference', '__httpwww_ech_chxmlnseCH_0147T01_headerType_httpwww_ech_chxmlnseCH_0147T01reference', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 297, 3), )

    
    reference = property(__reference.value, __reference.set, None, None)

    _ElementMap.update({
        __senderId.name() : __senderId,
        __recipientId.name() : __recipientId,
        __originalSenderId.name() : __originalSenderId,
        __declarationLocalReference.name() : __declarationLocalReference,
        __messageId.name() : __messageId,
        __referenceMessageId.name() : __referenceMessageId,
        __uniqueBusinessTransactionId.name() : __uniqueBusinessTransactionId,
        __ourBusinessReferenceId.name() : __ourBusinessReferenceId,
        __yourBusinessReferenceId.name() : __yourBusinessReferenceId,
        __messageType.name() : __messageType,
        __subMessageType.name() : __subMessageType,
        __messageGroup.name() : __messageGroup,
        __sendingApplication.name() : __sendingApplication,
        __subjects.name() : __subjects,
        __object.name() : __object,
        __comments.name() : __comments,
        __messageDate.name() : __messageDate,
        __initialMessageDate.name() : __initialMessageDate,
        __eventDate.name() : __eventDate,
        __eventPeriod.name() : __eventPeriod,
        __modificationDate.name() : __modificationDate,
        __action.name() : __action,
        __testDeliveryFlag.name() : __testDeliveryFlag,
        __reference.name() : __reference
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.headerType = headerType
Namespace.addCategoryObject('typeBinding', 'headerType', headerType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}objectType with content type ELEMENT_ONLY
class objectType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}objectType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'objectType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 300, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}applicationCustom uses Python identifier applicationCustom
    __applicationCustom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), 'applicationCustom', '__httpwww_ech_chxmlnseCH_0147T01_objectType_httpwww_ech_chxmlnseCH_0147T01applicationCustom', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 302, 3), )

    
    applicationCustom = property(__applicationCustom.value, __applicationCustom.set, None, None)

    _ElementMap.update({
        __applicationCustom.name() : __applicationCustom
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.objectType = objectType
Namespace.addCategoryObject('typeBinding', 'objectType', objectType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}negativeReportType with content type ELEMENT_ONLY
class negativeReportType (pyxb.binding.basis.complexTypeDefinition):
    """Negativer Bericht: Bericht, welcher einer negativen Antwortmeldung angehängt werden kann (Gebrauch ist zu spezifizieren)."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'negativeReportType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 305, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}errors uses Python identifier errors
    __errors = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'errors'), 'errors', '__httpwww_ech_chxmlnseCH_0147T01_negativeReportType_httpwww_ech_chxmlnseCH_0147T01errors', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 310, 3), )

    
    errors = property(__errors.value, __errors.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}comments uses Python identifier comments
    __comments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comments'), 'comments', '__httpwww_ech_chxmlnseCH_0147T01_negativeReportType_httpwww_ech_chxmlnseCH_0147T01comments', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 311, 3), )

    
    comments = property(__comments.value, __comments.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}applicationCustom uses Python identifier applicationCustom
    __applicationCustom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), 'applicationCustom', '__httpwww_ech_chxmlnseCH_0147T01_negativeReportType_httpwww_ech_chxmlnseCH_0147T01applicationCustom', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 312, 3), )

    
    applicationCustom = property(__applicationCustom.value, __applicationCustom.set, None, None)

    _ElementMap.update({
        __errors.name() : __errors,
        __comments.name() : __comments,
        __applicationCustom.name() : __applicationCustom
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.negativeReportType = negativeReportType
Namespace.addCategoryObject('typeBinding', 'negativeReportType', negativeReportType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}positiveReportType with content type ELEMENT_ONLY
class positiveReportType (pyxb.binding.basis.complexTypeDefinition):
    """Positiver Bericht: Bericht, welcher einer positiven Antwortmeldung angehängt werden kann."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'positiveReportType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 315, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}comments uses Python identifier comments
    __comments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comments'), 'comments', '__httpwww_ech_chxmlnseCH_0147T01_positiveReportType_httpwww_ech_chxmlnseCH_0147T01comments', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 320, 3), )

    
    comments = property(__comments.value, __comments.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}applicationCustom uses Python identifier applicationCustom
    __applicationCustom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), 'applicationCustom', '__httpwww_ech_chxmlnseCH_0147T01_positiveReportType_httpwww_ech_chxmlnseCH_0147T01applicationCustom', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 321, 3), )

    
    applicationCustom = property(__applicationCustom.value, __applicationCustom.set, None, None)

    _ElementMap.update({
        __comments.name() : __comments,
        __applicationCustom.name() : __applicationCustom
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.positiveReportType = positiveReportType
Namespace.addCategoryObject('typeBinding', 'positiveReportType', positiveReportType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}reportHeaderType with content type ELEMENT_ONLY
class reportHeaderType (pyxb.binding.basis.complexTypeDefinition):
    """Implementiert den Meldungsrahmen (Header) nach eCH-0058 für Antwortmeldungen."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'reportHeaderType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 324, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}senderId uses Python identifier senderId
    __senderId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'senderId'), 'senderId', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01senderId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 329, 3), )

    
    senderId = property(__senderId.value, __senderId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}recipientId uses Python identifier recipientId
    __recipientId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'recipientId'), 'recipientId', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01recipientId', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 330, 3), )

    
    recipientId = property(__recipientId.value, __recipientId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}messageId uses Python identifier messageId
    __messageId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageId'), 'messageId', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01messageId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 331, 3), )

    
    messageId = property(__messageId.value, __messageId.set, None, 'Nachrichten-ID: Empfehlung des Einsatzes von\n\t\t\t\t\t\t\tUUID für die eindeutige Referenz von übermittelten\n\t\t\t\t\t\t\tNachrichten.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}referenceMessageId uses Python identifier referenceMessageId
    __referenceMessageId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId'), 'referenceMessageId', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01referenceMessageId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 338, 3), )

    
    referenceMessageId = property(__referenceMessageId.value, __referenceMessageId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}uniqueBusinessTransactionId uses Python identifier uniqueBusinessTransactionId
    __uniqueBusinessTransactionId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uniqueBusinessTransactionId'), 'uniqueBusinessTransactionId', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01uniqueBusinessTransactionId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 339, 3), )

    
    uniqueBusinessTransactionId = property(__uniqueBusinessTransactionId.value, __uniqueBusinessTransactionId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}ourBusinessReferenceId uses Python identifier ourBusinessReferenceId
    __ourBusinessReferenceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId'), 'ourBusinessReferenceId', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01ourBusinessReferenceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 340, 3), )

    
    ourBusinessReferenceId = property(__ourBusinessReferenceId.value, __ourBusinessReferenceId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}yourBusinessReferenceId uses Python identifier yourBusinessReferenceId
    __yourBusinessReferenceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId'), 'yourBusinessReferenceId', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01yourBusinessReferenceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 341, 3), )

    
    yourBusinessReferenceId = property(__yourBusinessReferenceId.value, __yourBusinessReferenceId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}messageType uses Python identifier messageType
    __messageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageType'), 'messageType', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01messageType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 342, 3), )

    
    messageType = property(__messageType.value, __messageType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}subMessageType uses Python identifier subMessageType
    __subMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subMessageType'), 'subMessageType', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01subMessageType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 343, 3), )

    
    subMessageType = property(__subMessageType.value, __subMessageType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}messageGroup uses Python identifier messageGroup
    __messageGroup = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageGroup'), 'messageGroup', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01messageGroup', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 344, 3), )

    
    messageGroup = property(__messageGroup.value, __messageGroup.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}sendingApplication uses Python identifier sendingApplication
    __sendingApplication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication'), 'sendingApplication', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01sendingApplication', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 345, 3), )

    
    sendingApplication = property(__sendingApplication.value, __sendingApplication.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}object uses Python identifier object
    __object = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'object'), 'object', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01object', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 346, 3), )

    
    object = property(__object.value, __object.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}initialMessageDate uses Python identifier initialMessageDate
    __initialMessageDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate'), 'initialMessageDate', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01initialMessageDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 347, 3), )

    
    initialMessageDate = property(__initialMessageDate.value, __initialMessageDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}action uses Python identifier action
    __action = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'action'), 'action', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01action', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 348, 3), )

    
    action = property(__action.value, __action.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}testDeliveryFlag uses Python identifier testDeliveryFlag
    __testDeliveryFlag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag'), 'testDeliveryFlag', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01testDeliveryFlag', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 349, 3), )

    
    testDeliveryFlag = property(__testDeliveryFlag.value, __testDeliveryFlag.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}reference uses Python identifier reference
    __reference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'reference'), 'reference', '__httpwww_ech_chxmlnseCH_0147T01_reportHeaderType_httpwww_ech_chxmlnseCH_0147T01reference', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 350, 3), )

    
    reference = property(__reference.value, __reference.set, None, None)

    _ElementMap.update({
        __senderId.name() : __senderId,
        __recipientId.name() : __recipientId,
        __messageId.name() : __messageId,
        __referenceMessageId.name() : __referenceMessageId,
        __uniqueBusinessTransactionId.name() : __uniqueBusinessTransactionId,
        __ourBusinessReferenceId.name() : __ourBusinessReferenceId,
        __yourBusinessReferenceId.name() : __yourBusinessReferenceId,
        __messageType.name() : __messageType,
        __subMessageType.name() : __subMessageType,
        __messageGroup.name() : __messageGroup,
        __sendingApplication.name() : __sendingApplication,
        __object.name() : __object,
        __initialMessageDate.name() : __initialMessageDate,
        __action.name() : __action,
        __testDeliveryFlag.name() : __testDeliveryFlag,
        __reference.name() : __reference
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.reportHeaderType = reportHeaderType
Namespace.addCategoryObject('typeBinding', 'reportHeaderType', reportHeaderType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T0/1}reportType with content type ELEMENT_ONLY
class reportType (pyxb.binding.basis.complexTypeDefinition):
    """Bericht: Enthält einen Bericht, welcher einer Antwortmeldung angehängt werden kann."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'reportType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 353, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}positiveReport uses Python identifier positiveReport
    __positiveReport = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'positiveReport'), 'positiveReport', '__httpwww_ech_chxmlnseCH_0147T01_reportType_httpwww_ech_chxmlnseCH_0147T01positiveReport', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 358, 3), )

    
    positiveReport = property(__positiveReport.value, __positiveReport.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0147/T0/1}negativeReport uses Python identifier negativeReport
    __negativeReport = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'negativeReport'), 'negativeReport', '__httpwww_ech_chxmlnseCH_0147T01_reportType_httpwww_ech_chxmlnseCH_0147T01negativeReport', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 359, 3), )

    
    negativeReport = property(__negativeReport.value, __negativeReport.set, None, None)

    _ElementMap.update({
        __positiveReport.name() : __positiveReport,
        __negativeReport.name() : __negativeReport
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.reportType = reportType
Namespace.addCategoryObject('typeBinding', 'reportType', reportType)




addressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.token, scope=addressType, documentation='UUID: Universally Unique Identifier der Adresse. Referenz des Objekts, nicht der Nachricht.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 13, 3)))

addressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'transactionRole'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.transactionRoleType, scope=addressType, documentation='Transaktionsrolle: Angabe, ob es sich bei der Rolle um einen Absender, Emfpänger oder Beteiligten (Kopie an) handelt.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 18, 3)))

addressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'position'), pyxb.binding.datatypes.token, scope=addressType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 23, 3)))

addressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contact'), _ImportedBinding_camac_echbern_schema_ech_0046_1_0.contactType, scope=addressType, documentation='Kontaktinformatione: Implementiert eCH-0046 Datenstandard Kontakt.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 24, 3)))

addressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), applicationCustomType, scope=addressType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 29, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 18, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 23, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 24, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 29, 3))
    counters.add(cc_3)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(addressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 13, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(addressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'transactionRole')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 18, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(addressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'position')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 23, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(addressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'contact')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 24, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(addressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 29, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
addressType._Automaton = _BuildAutomaton()




addressesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'address'), addressType, scope=addressesType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 34, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(addressesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'address')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 34, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
addressesType._Automaton = _BuildAutomaton_()




def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
applicationCustomType._Automaton = _BuildAutomaton_2()




documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.token, scope=documentType, documentation='UUID: Universally Unique Identifier des Dokuments. Referenz des Objekts, nicht der Nachricht.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 51, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'titles'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.titlesType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 56, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'status'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.documentStatusType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 57, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'files'), filesType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 58, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'classification'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.classificationType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 59, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'openToThePublic'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.openToThePublicType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 60, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection'), pyxb.binding.datatypes.boolean, scope=documentType, documentation='Datenschutzstufe: Markierung, die angibt, ob das Dokument besonders Schützenswerte Personendaten oder Persönlichkeitsprofile gemäss Datenschutzrecht enthält.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 61, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'openingDate'), pyxb.binding.datatypes.date, scope=documentType, documentation='Eröffnungsdatum: Tag, an dem das Dokument im GEVER-System einem Dossier zugeordnet worden ist.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 66, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'owner'), pyxb.binding.datatypes.token, scope=documentType, documentation='Eigentümer: Name des Eigentümers des Dokuments.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 71, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signer'), pyxb.binding.datatypes.token, scope=documentType, documentation='Unterzeichner: Person, welche das Dokument unterzeichnet hat oder die Verantwortung dafür übernimmt.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 76, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ourRecordReference'), pyxb.binding.datatypes.token, scope=documentType, documentation='Unser Aktenzeichen: Referenz auf das entsprechende Dossier des Absenders.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 81, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comments'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.commentsType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 86, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'keywords'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.keywordsType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 87, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'isLeadingDocument'), pyxb.binding.datatypes.boolean, scope=documentType, documentation='Hauptdokument: Angabe, ob es sich um das Hauptdokument (führendes Dokument) handelt.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 88, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sortOrder'), pyxb.binding.datatypes.nonNegativeInteger, scope=documentType, documentation='Sortierfolge: Angabe zur Reihenfolge der Sortierung von Dokumenten.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 93, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'documentKind'), pyxb.binding.datatypes.token, scope=documentType, documentation='Dokumenttyp: Fachliche Beschreibung des Dokuments (z.B. Vertrag, Antrag, Antwort. u.a).', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 98, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), applicationCustomType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 103, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 59, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 60, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 61, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 66, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 71, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 76, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 81, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 86, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 87, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 88, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 93, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 98, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 103, 3))
    counters.add(cc_12)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 51, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'titles')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 56, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'status')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 57, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'files')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 58, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'classification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 59, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'openToThePublic')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 60, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 61, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'openingDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 66, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'owner')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 71, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'signer')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 76, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ourRecordReference')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 81, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comments')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 86, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'keywords')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 87, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'isLeadingDocument')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 88, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sortOrder')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 93, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'documentKind')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 98, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 103, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
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
    st_2._set_transitionSet(transitions)
    transitions = []
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
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True) ]))
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, True) ]))
    st_16._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
documentType._Automaton = _BuildAutomaton_3()




documentsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'document'), documentType, scope=documentsType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 109, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(documentsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'document')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 109, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
documentsType._Automaton = _BuildAutomaton_4()




dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.token, scope=dossierType, documentation='UUID: Universally Unique Identifier des Dossiers. Referenz des Objekts, nicht der Nachricht.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 117, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'status'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.dossierStatusType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 122, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'titles'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.titlesType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 123, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'classification'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.classificationType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 124, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection'), pyxb.binding.datatypes.boolean, scope=dossierType, documentation='Datenschutzstufe: Markierung, die angibt, ob das Dokument besonders Schützenswerte Personendaten oder Persönlichkeitsprofile gemäss Datenschutzrecht enthält.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 125, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'openToThePublicType'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.openToThePublicType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 130, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'caseReferenceLocalId'), pyxb.binding.datatypes.token, scope=dossierType, documentation='Ordnungsmerkmal: Ordnungsmerkmal des Dossiers, welches durch den Absender vergeben wird.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 131, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'openingDate'), pyxb.binding.datatypes.date, scope=dossierType, documentation='Datum: Datum, an welchem das Dossier eröffnet / registriert wurde. ', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 136, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'keywords'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.keywordsType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 141, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comments'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.commentsType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 142, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'links'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.linksType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 143, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'addresses'), addressesType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 144, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dossiers'), dossiersType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 145, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'documents'), documentsType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 146, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'folders'), foldersType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 147, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), applicationCustomType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 148, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 124, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 125, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 130, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 131, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 136, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 141, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 142, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 143, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 144, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 145, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 146, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 147, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 148, 3))
    counters.add(cc_12)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 117, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'status')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 122, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'titles')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 123, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'classification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 124, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 125, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'openToThePublicType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 130, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'caseReferenceLocalId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 131, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'openingDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 136, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'keywords')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 141, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comments')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 142, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'links')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 143, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'addresses')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 144, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dossiers')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 145, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'documents')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 146, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'folders')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 147, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 148, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
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
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_15, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_15, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_15, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_15, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_15, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_15, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, True) ]))
    st_15._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
dossierType._Automaton = _BuildAutomaton_5()




dossiersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dossier'), dossierType, scope=dossiersType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 154, 3)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(dossiersType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dossier')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 154, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
dossiersType._Automaton = _BuildAutomaton_6()




errorsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'error'), errorType, scope=errorsType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 159, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(errorsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'error')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 159, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
errorsType._Automaton = _BuildAutomaton_7()




errorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'errorKind'), errorKindType, scope=errorType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 164, 3)))

errorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comments'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.commentsType, scope=errorType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 165, 3)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 165, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(errorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'errorKind')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 164, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(errorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comments')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 165, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
errorType._Automaton = _BuildAutomaton_8()




eventReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reportHeader'), reportHeaderType, scope=eventReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 184, 3)))

eventReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'report'), reportType, scope=eventReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 185, 3)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'reportHeader')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 184, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'report')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 185, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventReportType._Automaton = _BuildAutomaton_9()




fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'pathFileName'), pyxb.binding.datatypes.token, scope=fileType, documentation='Pfad: Pfad zur Datei. Dabei kann es sich um einen lokalen Pfad oder eine URL handeln. Der Pfad bildet sich aus Pfad + Name + Extension (Dateiendung). Handelt es sich um eine lokale Referenz innehalb der ZIP-Datei, so beginnt der Pfad mit files/dateiname.extension', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 194, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mimeType'), pyxb.binding.datatypes.token, scope=fileType, documentation='MIME-Type der Datei.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 199, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'internalSortOrder'), pyxb.binding.datatypes.nonNegativeInteger, scope=fileType, documentation='Sortierfolge: Angabe zur Reihenfolge der Sortierung bei Dokumenten, welche aus mehreren Dateien bestehen.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 204, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'version'), pyxb.binding.datatypes.token, scope=fileType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 209, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'hashCode'), pyxb.binding.datatypes.token, scope=fileType, documentation='Hashwert: Hashwert der Datei.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 210, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'hashCodeAlgorithm'), pyxb.binding.datatypes.token, scope=fileType, documentation='Hashalgorithmus: Abkürzung des Algorithmus welcher zur Bildung des Hashwerts verwendet wurde.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 215, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), applicationCustomType, scope=fileType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 220, 3)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 204, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 209, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 210, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 215, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 220, 3))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'pathFileName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 194, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'mimeType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 199, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'internalSortOrder')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 204, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'version')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 209, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'hashCode')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 210, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'hashCodeAlgorithm')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 215, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 220, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
fileType._Automaton = _BuildAutomaton_10()




filesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'file'), fileType, scope=filesType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 229, 3)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(filesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'file')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 229, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
filesType._Automaton = _BuildAutomaton_11()




folderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'folderTitles'), folderTitlesType, scope=folderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 237, 3)))

folderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'documents'), documentsType, scope=folderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 238, 3)))

folderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), applicationCustomType, scope=folderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 239, 3)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 238, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 239, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(folderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'folderTitles')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 237, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(folderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'documents')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 238, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(folderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 239, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
folderType._Automaton = _BuildAutomaton_12()




foldersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'folder'), folderType, scope=foldersType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 244, 3)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(foldersType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'folder')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 244, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
foldersType._Automaton = _BuildAutomaton_13()




folderTitlesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'folderTitle'), folderTitleType, scope=folderTitlesType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 249, 3)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(folderTitlesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'folderTitle')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 249, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
folderTitlesType._Automaton = _BuildAutomaton_14()




headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'senderId'), pyxb.binding.datatypes.token, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 268, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'recipientId'), pyxb.binding.datatypes.token, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 269, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'originalSenderId'), pyxb.binding.datatypes.token, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 270, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'declarationLocalReference'), pyxb.binding.datatypes.token, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 271, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageId'), pyxb.binding.datatypes.token, scope=headerType, documentation='Nachrichten-ID: Empfehlung des Einsatzes von\n\t\t\t\t\t\tUUID für die eindeutige Referenz von übermittelten\n\t\t\t\t\t\tNachrichten.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 272, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId'), pyxb.binding.datatypes.token, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 279, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uniqueBusinessTransactionId'), pyxb.binding.datatypes.token, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 280, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId'), pyxb.binding.datatypes.token, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 281, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId'), pyxb.binding.datatypes.token, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 282, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageType'), pyxb.binding.datatypes.int, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 283, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subMessageType'), pyxb.binding.datatypes.token, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 284, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageGroup'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.messageGroupType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 285, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.sendingApplicationType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 286, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subjects'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.subjectsType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 287, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'object'), objectType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 288, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comments'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.commentsType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 289, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageDate'), pyxb.binding.datatypes.dateTime, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 290, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate'), pyxb.binding.datatypes.dateTime, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 291, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventDate'), pyxb.binding.datatypes.dateTime, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 292, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventPeriod'), pyxb.binding.datatypes.token, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 293, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'modificationDate'), pyxb.binding.datatypes.dateTime, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 294, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'action'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.actionType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 295, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag'), pyxb.binding.datatypes.boolean, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 296, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reference'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.referenceType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 297, 3)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 269, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 270, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 271, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 279, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 280, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 281, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 282, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 284, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 287, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 288, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 289, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 291, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 292, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 293, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 294, 3))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 297, 3))
    counters.add(cc_15)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'senderId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 268, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'recipientId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 269, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'originalSenderId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 270, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'declarationLocalReference')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 271, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 272, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 279, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uniqueBusinessTransactionId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 280, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 281, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 282, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 283, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subMessageType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 284, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageGroup')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 285, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 286, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subjects')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 287, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'object')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 288, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comments')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 289, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 290, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 291, 3))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 292, 3))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventPeriod')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 293, 3))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'modificationDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 294, 3))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'action')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 295, 3))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 296, 3))
    st_22 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'reference')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 297, 3))
    st_23 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_23)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
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
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
         ]))
    transitions.append(fac.Transition(st_18, [
         ]))
    transitions.append(fac.Transition(st_19, [
         ]))
    transitions.append(fac.Transition(st_20, [
         ]))
    transitions.append(fac.Transition(st_21, [
         ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_22, [
         ]))
    st_21._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
         ]))
    st_22._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_15, True) ]))
    st_23._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
headerType._Automaton = _BuildAutomaton_15()




objectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), applicationCustomType, scope=objectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 302, 3)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(objectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 302, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
objectType._Automaton = _BuildAutomaton_16()




negativeReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'errors'), errorsType, scope=negativeReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 310, 3)))

negativeReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comments'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.commentsType, scope=negativeReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 311, 3)))

negativeReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), applicationCustomType, scope=negativeReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 312, 3)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 311, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 312, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(negativeReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'errors')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 310, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(negativeReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comments')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 311, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(negativeReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 312, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
negativeReportType._Automaton = _BuildAutomaton_17()




positiveReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comments'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.commentsType, scope=positiveReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 320, 3)))

positiveReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom'), applicationCustomType, scope=positiveReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 321, 3)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 320, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 321, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(positiveReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comments')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 320, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(positiveReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'applicationCustom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 321, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
positiveReportType._Automaton = _BuildAutomaton_18()




reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'senderId'), pyxb.binding.datatypes.token, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 329, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'recipientId'), pyxb.binding.datatypes.token, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 330, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageId'), pyxb.binding.datatypes.token, scope=reportHeaderType, documentation='Nachrichten-ID: Empfehlung des Einsatzes von\n\t\t\t\t\t\t\tUUID für die eindeutige Referenz von übermittelten\n\t\t\t\t\t\t\tNachrichten.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 331, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId'), pyxb.binding.datatypes.token, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 338, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uniqueBusinessTransactionId'), pyxb.binding.datatypes.token, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 339, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId'), pyxb.binding.datatypes.token, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 340, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId'), pyxb.binding.datatypes.token, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 341, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageType'), pyxb.binding.datatypes.int, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 342, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subMessageType'), pyxb.binding.datatypes.token, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 343, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageGroup'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.messageGroupType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 344, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.sendingApplicationType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 345, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'object'), objectType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 346, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate'), pyxb.binding.datatypes.dateTime, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 347, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'action'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.reportActionType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 348, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag'), pyxb.binding.datatypes.boolean, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 349, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reference'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.referenceType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 350, 3)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 330, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 338, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 339, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 340, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 341, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 343, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 346, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 347, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 350, 3))
    counters.add(cc_8)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'senderId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 329, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'recipientId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 330, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 331, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 338, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uniqueBusinessTransactionId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 339, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 340, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 341, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 342, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subMessageType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 343, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageGroup')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 344, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 345, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'object')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 346, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 347, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'action')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 348, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 349, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'reference')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 350, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
         ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
         ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, True) ]))
    st_15._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
reportHeaderType._Automaton = _BuildAutomaton_19()




reportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'positiveReport'), positiveReportType, scope=reportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 358, 3)))

reportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'negativeReport'), negativeReportType, scope=reportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 359, 3)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 358, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 359, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(reportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'positiveReport')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 358, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(reportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'negativeReport')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t0_1.xsd', 359, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
reportType._Automaton = _BuildAutomaton_20()

