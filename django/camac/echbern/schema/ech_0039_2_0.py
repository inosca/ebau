# ../../camac/echbern/schema/ech_0039_2_0.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:cba342e2f4db239b912a83ae929d430d24003c9e
# Generated 2019-09-26 17:57:08.875293 by PyXB version 1.2.6 using Python 3.6.8.final.0
# Namespace http://www.ech.ch/xmlns/eCH-0039/2 [xmlns:eCH-0039]

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
import camac.echbern.schema.ech_0046_1_0 as _ImportedBinding_camac_echbern_schema_ech_0046_1_0
import camac.echbern.schema.ech_0058_3_0 as _ImportedBinding_camac_echbern_schema_ech_0058_3_0

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.ech.ch/xmlns/eCH-0039/2', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

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


# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0039/2}actionType
class actionType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """Aktion für Erstmeldungen: Fachliche Austauschanweisung für den Empfänger."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'actionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 32, 1)
    _Documentation = 'Aktion für Erstmeldungen: Fachliche Austauschanweisung für den Empfänger.'
actionType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=actionType, enum_prefix=None)
actionType._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
actionType._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
actionType._CF_enumeration.addEnumeration(unicode_value='4', tag=None)
actionType._CF_enumeration.addEnumeration(unicode_value='5', tag=None)
actionType._CF_enumeration.addEnumeration(unicode_value='6', tag=None)
actionType._CF_enumeration.addEnumeration(unicode_value='7', tag=None)
actionType._CF_enumeration.addEnumeration(unicode_value='10', tag=None)
actionType._CF_enumeration.addEnumeration(unicode_value='12', tag=None)
actionType._InitializeFacetMap(actionType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'actionType', actionType)
_module_typeBindings.actionType = actionType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0039/2}classificationType
class classificationType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """Klassifizierungskategorie: Grad, indem das Dossier und die enthaltenen Unterlagen vor unberechtigter Einsicht geschützt werden müssen."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'classificationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 47, 1)
    _Documentation = 'Klassifizierungskategorie: Grad, indem das Dossier und die enthaltenen Unterlagen vor unberechtigter Einsicht geschützt werden müssen.'
classificationType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=classificationType, enum_prefix=None)
classificationType.unclassified = classificationType._CF_enumeration.addEnumeration(unicode_value='unclassified', tag='unclassified')
classificationType.confidential = classificationType._CF_enumeration.addEnumeration(unicode_value='confidential', tag='confidential')
classificationType.secret = classificationType._CF_enumeration.addEnumeration(unicode_value='secret', tag='secret')
classificationType.in_house = classificationType._CF_enumeration.addEnumeration(unicode_value='in_house', tag='in_house')
classificationType._InitializeFacetMap(classificationType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'classificationType', classificationType)
_module_typeBindings.classificationType = classificationType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0039/2}directiveInstructionType
class directiveInstructionType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """Instruktion: Bearbeitungsanweisung einer Anweisung."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'directiveInstructionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 107, 1)
    _Documentation = 'Instruktion: Bearbeitungsanweisung einer Anweisung.'
directiveInstructionType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=directiveInstructionType, enum_prefix=None)
directiveInstructionType.process = directiveInstructionType._CF_enumeration.addEnumeration(unicode_value='process', tag='process')
directiveInstructionType.external_process = directiveInstructionType._CF_enumeration.addEnumeration(unicode_value='external_process', tag='external_process')
directiveInstructionType.information = directiveInstructionType._CF_enumeration.addEnumeration(unicode_value='information', tag='information')
directiveInstructionType.comment = directiveInstructionType._CF_enumeration.addEnumeration(unicode_value='comment', tag='comment')
directiveInstructionType.approve = directiveInstructionType._CF_enumeration.addEnumeration(unicode_value='approve', tag='approve')
directiveInstructionType.sign = directiveInstructionType._CF_enumeration.addEnumeration(unicode_value='sign', tag='sign')
directiveInstructionType.send = directiveInstructionType._CF_enumeration.addEnumeration(unicode_value='send', tag='send')
directiveInstructionType.complete = directiveInstructionType._CF_enumeration.addEnumeration(unicode_value='complete', tag='complete')
directiveInstructionType._InitializeFacetMap(directiveInstructionType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'directiveInstructionType', directiveInstructionType)
_module_typeBindings.directiveInstructionType = directiveInstructionType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0039/2}documentStatusType
class documentStatusType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """Status: Zustand des Dokuments in Bezug auf Veränderbarkeit und Gültigkeit."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'documentStatusType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 122, 1)
    _Documentation = 'Status: Zustand des Dokuments in Bezug auf Veränderbarkeit und Gültigkeit.'
documentStatusType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=documentStatusType, enum_prefix=None)
documentStatusType.undefined = documentStatusType._CF_enumeration.addEnumeration(unicode_value='undefined', tag='undefined')
documentStatusType.created = documentStatusType._CF_enumeration.addEnumeration(unicode_value='created', tag='created')
documentStatusType.in_process = documentStatusType._CF_enumeration.addEnumeration(unicode_value='in_process', tag='in_process')
documentStatusType.signed = documentStatusType._CF_enumeration.addEnumeration(unicode_value='signed', tag='signed')
documentStatusType.approved = documentStatusType._CF_enumeration.addEnumeration(unicode_value='approved', tag='approved')
documentStatusType.sent = documentStatusType._CF_enumeration.addEnumeration(unicode_value='sent', tag='sent')
documentStatusType.canceled = documentStatusType._CF_enumeration.addEnumeration(unicode_value='canceled', tag='canceled')
documentStatusType.invalidated = documentStatusType._CF_enumeration.addEnumeration(unicode_value='invalidated', tag='invalidated')
documentStatusType.archived = documentStatusType._CF_enumeration.addEnumeration(unicode_value='archived', tag='archived')
documentStatusType.preserved = documentStatusType._CF_enumeration.addEnumeration(unicode_value='preserved', tag='preserved')
documentStatusType._InitializeFacetMap(documentStatusType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'documentStatusType', documentStatusType)
_module_typeBindings.documentStatusType = documentStatusType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0039/2}dossierStatusType
class dossierStatusType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """Status: Zustand in Bezug auf den Lebenszyklus des Dossiers."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dossierStatusType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 199, 1)
    _Documentation = 'Status: Zustand in Bezug auf den Lebenszyklus des Dossiers.'
dossierStatusType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=dossierStatusType, enum_prefix=None)
dossierStatusType.undefined = dossierStatusType._CF_enumeration.addEnumeration(unicode_value='undefined', tag='undefined')
dossierStatusType.created = dossierStatusType._CF_enumeration.addEnumeration(unicode_value='created', tag='created')
dossierStatusType.in_process = dossierStatusType._CF_enumeration.addEnumeration(unicode_value='in_process', tag='in_process')
dossierStatusType.moved = dossierStatusType._CF_enumeration.addEnumeration(unicode_value='moved', tag='moved')
dossierStatusType.canceled = dossierStatusType._CF_enumeration.addEnumeration(unicode_value='canceled', tag='canceled')
dossierStatusType.closed = dossierStatusType._CF_enumeration.addEnumeration(unicode_value='closed', tag='closed')
dossierStatusType.archived = dossierStatusType._CF_enumeration.addEnumeration(unicode_value='archived', tag='archived')
dossierStatusType.invalidated = dossierStatusType._CF_enumeration.addEnumeration(unicode_value='invalidated', tag='invalidated')
dossierStatusType.in_selection = dossierStatusType._CF_enumeration.addEnumeration(unicode_value='in_selection', tag='in_selection')
dossierStatusType.preserved = dossierStatusType._CF_enumeration.addEnumeration(unicode_value='preserved', tag='preserved')
dossierStatusType._InitializeFacetMap(dossierStatusType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'dossierStatusType', dossierStatusType)
_module_typeBindings.dossierStatusType = dossierStatusType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0039/2}openToThePublicType
class openToThePublicType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """Öffentlichkeitsstatus: Angabe, ob das Dossier / Dokument gemäss BGÖ schützenswerte Informationen enthält oder nicht."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'openToThePublicType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 385, 1)
    _Documentation = 'Öffentlichkeitsstatus: Angabe, ob das Dossier / Dokument gemäss BGÖ schützenswerte Informationen enthält oder nicht.'
openToThePublicType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=openToThePublicType, enum_prefix=None)
openToThePublicType.undefined = openToThePublicType._CF_enumeration.addEnumeration(unicode_value='undefined', tag='undefined')
openToThePublicType.public = openToThePublicType._CF_enumeration.addEnumeration(unicode_value='public', tag='public')
openToThePublicType.not_public = openToThePublicType._CF_enumeration.addEnumeration(unicode_value='not_public', tag='not_public')
openToThePublicType._InitializeFacetMap(openToThePublicType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'openToThePublicType', openToThePublicType)
_module_typeBindings.openToThePublicType = openToThePublicType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0039/2}priorityType
class priorityType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """Priorität: Angabe zur Dringlichkeit der Anweisung."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'priorityType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 395, 1)
    _Documentation = 'Priorität: Angabe zur Dringlichkeit der Anweisung.'
priorityType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=priorityType, enum_prefix=None)
priorityType.undefined = priorityType._CF_enumeration.addEnumeration(unicode_value='undefined', tag='undefined')
priorityType.medium = priorityType._CF_enumeration.addEnumeration(unicode_value='medium', tag='medium')
priorityType.high = priorityType._CF_enumeration.addEnumeration(unicode_value='high', tag='high')
priorityType._InitializeFacetMap(priorityType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'priorityType', priorityType)
_module_typeBindings.priorityType = priorityType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0039/2}reportActionType
class reportActionType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """Aktion für Antwortmeldungen: Fachliche Austauschanweisung für den Empfänger."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'reportActionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 452, 1)
    _Documentation = 'Aktion für Antwortmeldungen: Fachliche Austauschanweisung für den Empfänger.'
reportActionType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=reportActionType, enum_prefix=None)
reportActionType._CF_enumeration.addEnumeration(unicode_value='8', tag=None)
reportActionType._CF_enumeration.addEnumeration(unicode_value='9', tag=None)
reportActionType._CF_enumeration.addEnumeration(unicode_value='11', tag=None)
reportActionType._InitializeFacetMap(reportActionType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'reportActionType', reportActionType)
_module_typeBindings.reportActionType = reportActionType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0039/2}transactionRoleType
class transactionRoleType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """Transaktionsrolle: Angabe, ob es sich bei der Rolle um einen Absender, Emfpänger oder Beteiligten (Kopie an) handelt."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'transactionRoleType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 536, 1)
    _Documentation = 'Transaktionsrolle: Angabe, ob es sich bei der Rolle um einen Absender, Emfpänger oder Beteiligten (Kopie an) handelt.'
transactionRoleType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=transactionRoleType, enum_prefix=None)
transactionRoleType.sender = transactionRoleType._CF_enumeration.addEnumeration(unicode_value='sender', tag='sender')
transactionRoleType.addressee = transactionRoleType._CF_enumeration.addEnumeration(unicode_value='addressee', tag='addressee')
transactionRoleType.participant = transactionRoleType._CF_enumeration.addEnumeration(unicode_value='participant', tag='participant')
transactionRoleType._InitializeFacetMap(transactionRoleType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'transactionRoleType', transactionRoleType)
_module_typeBindings.transactionRoleType = transactionRoleType

# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}addressType with content type ELEMENT_ONLY
class addressType (pyxb.binding.basis.complexTypeDefinition):
    """Adresse: Basiskomponente zur Abbildung von Kontaktinformationen. Basiert auf eCH-0046 Datenstandard Kontakt."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'addressType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 9, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpwww_ech_chxmlnseCH_00392_addressType_httpwww_ech_chxmlnseCH_00392uuid', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 14, 3), )

    
    uuid = property(__uuid.value, __uuid.set, None, 'UUID: Universally Unique Identifier der Adresse. Referenz des Objekts, nicht der Nachricht.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}transactionRole uses Python identifier transactionRole
    __transactionRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'transactionRole'), 'transactionRole', '__httpwww_ech_chxmlnseCH_00392_addressType_httpwww_ech_chxmlnseCH_00392transactionRole', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 19, 3), )

    
    transactionRole = property(__transactionRole.value, __transactionRole.set, None, 'Transaktionsrolle: Angabe, ob es sich bei der Rolle um einen Absender, Emfpänger oder Beteiligten (Kopie an) handelt.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}position uses Python identifier position
    __position = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'position'), 'position', '__httpwww_ech_chxmlnseCH_00392_addressType_httpwww_ech_chxmlnseCH_00392position', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 24, 3), )

    
    position = property(__position.value, __position.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}contact uses Python identifier contact
    __contact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'contact'), 'contact', '__httpwww_ech_chxmlnseCH_00392_addressType_httpwww_ech_chxmlnseCH_00392contact', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 25, 3), )

    
    contact = property(__contact.value, __contact.set, None, 'Kontaktinformatione: Implementiert eCH-0046 Datenstandard Kontakt.')

    _ElementMap.update({
        __uuid.name() : __uuid,
        __transactionRole.name() : __transactionRole,
        __position.name() : __position,
        __contact.name() : __contact
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.addressType = addressType
Namespace.addCategoryObject('typeBinding', 'addressType', addressType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}commentType with content type SIMPLE
class commentType (pyxb.binding.basis.complexTypeDefinition):
    """Kommentar: Enthält einen Kommentar. Die Sprache kann im Attribut angegeben werden."""
    _TypeDefinition = pyxb.binding.datatypes.token
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'commentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 58, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.token
    
    # Attribute {http://www.ech.ch/xmlns/eCH-0039/2}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'lang'), 'lang', '__httpwww_ech_chxmlnseCH_00392_commentType_httpwww_ech_chxmlnseCH_00392lang', pyxb.binding.datatypes.language)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 546, 1)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 64, 4)
    
    lang = property(__lang.value, __lang.set, None, 'Sprache: Attribut zur Angabe des Sprachcodes nach ISO 639-1 (zweistelliger Sprachcode). Ursprünglich RFC 1766.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.commentType = commentType
Namespace.addCategoryObject('typeBinding', 'commentType', commentType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}commentsType with content type ELEMENT_ONLY
class commentsType (pyxb.binding.basis.complexTypeDefinition):
    """Kommentare: Enthält einen oder mehrere
				Kommentare."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'commentsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 68, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}comment uses Python identifier comment
    __comment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comment'), 'comment', '__httpwww_ech_chxmlnseCH_00392_commentsType_httpwww_ech_chxmlnseCH_00392comment', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 74, 3), )

    
    comment = property(__comment.value, __comment.set, None, None)

    _ElementMap.update({
        __comment.name() : __comment
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.commentsType = commentsType
Namespace.addCategoryObject('typeBinding', 'commentsType', commentsType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}directiveType with content type ELEMENT_ONLY
class directiveType (pyxb.binding.basis.complexTypeDefinition):
    """Anweisung: Basiskomponente zur Abbildung von Bearbeitungsanweisungen an den Empfänger."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'directiveType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 77, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpwww_ech_chxmlnseCH_00392_directiveType_httpwww_ech_chxmlnseCH_00392uuid', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 82, 3), )

    
    uuid = property(__uuid.value, __uuid.set, None, 'UUID: Universally Unique Identifier der Anweisung. Referenz des Objekts, nicht der Nachricht.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}instruction uses Python identifier instruction
    __instruction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'instruction'), 'instruction', '__httpwww_ech_chxmlnseCH_00392_directiveType_httpwww_ech_chxmlnseCH_00392instruction', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 87, 3), )

    
    instruction = property(__instruction.value, __instruction.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}priority uses Python identifier priority
    __priority = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'priority'), 'priority', '__httpwww_ech_chxmlnseCH_00392_directiveType_httpwww_ech_chxmlnseCH_00392priority', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 88, 3), )

    
    priority = property(__priority.value, __priority.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}titles uses Python identifier titles
    __titles = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'titles'), 'titles', '__httpwww_ech_chxmlnseCH_00392_directiveType_httpwww_ech_chxmlnseCH_00392titles', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 89, 3), )

    
    titles = property(__titles.value, __titles.set, None, 'Titel: Benennung von Tätigkeit und Gegenstand des Geschäftsvorfalls.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}deadline uses Python identifier deadline
    __deadline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'deadline'), 'deadline', '__httpwww_ech_chxmlnseCH_00392_directiveType_httpwww_ech_chxmlnseCH_00392deadline', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 94, 3), )

    
    deadline = property(__deadline.value, __deadline.set, None, 'Bearbeitungsfrist: Tag, an dem die Aktivität erledigt sein soll.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}serviceId uses Python identifier serviceId
    __serviceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'serviceId'), 'serviceId', '__httpwww_ech_chxmlnseCH_00392_directiveType_httpwww_ech_chxmlnseCH_00392serviceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 99, 3), )

    
    serviceId = property(__serviceId.value, __serviceId.set, None, 'Leistungsidentifikation: Identifikation der Leistung gemäss eCH-0070 Leistungsinventar eGov CH.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}comments uses Python identifier comments
    __comments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comments'), 'comments', '__httpwww_ech_chxmlnseCH_00392_directiveType_httpwww_ech_chxmlnseCH_00392comments', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 104, 3), )

    
    comments = property(__comments.value, __comments.set, None, None)

    _ElementMap.update({
        __uuid.name() : __uuid,
        __instruction.name() : __instruction,
        __priority.name() : __priority,
        __titles.name() : __titles,
        __deadline.name() : __deadline,
        __serviceId.name() : __serviceId,
        __comments.name() : __comments
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.directiveType = directiveType
Namespace.addCategoryObject('typeBinding', 'directiveType', directiveType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}documentType with content type ELEMENT_ONLY
class documentType (pyxb.binding.basis.complexTypeDefinition):
    """Dokument (Unterlage): Basiskomponente zur Abbildung der Metadaten von Dokumenten und Unterlagen."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'documentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 139, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392uuid', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 144, 3), )

    
    uuid = property(__uuid.value, __uuid.set, None, 'UUID: Universally Unique Identifier des Dokuments. Referenz des Objekts, nicht der Nachricht.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}titles uses Python identifier titles
    __titles = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'titles'), 'titles', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392titles', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 149, 3), )

    
    titles = property(__titles.value, __titles.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}status uses Python identifier status
    __status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'status'), 'status', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392status', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 150, 3), )

    
    status = property(__status.value, __status.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}files uses Python identifier files
    __files = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'files'), 'files', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392files', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 151, 3), )

    
    files = property(__files.value, __files.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}classification uses Python identifier classification
    __classification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'classification'), 'classification', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392classification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 152, 3), )

    
    classification = property(__classification.value, __classification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}openToThePublic uses Python identifier openToThePublic
    __openToThePublic = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'openToThePublic'), 'openToThePublic', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392openToThePublic', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 153, 3), )

    
    openToThePublic = property(__openToThePublic.value, __openToThePublic.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}hasPrivacyProtection uses Python identifier hasPrivacyProtection
    __hasPrivacyProtection = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection'), 'hasPrivacyProtection', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392hasPrivacyProtection', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 154, 3), )

    
    hasPrivacyProtection = property(__hasPrivacyProtection.value, __hasPrivacyProtection.set, None, 'Datenschutzstufe: Markierung, die angibt, ob das Dokument besonders Schützenswerte Personendaten oder Persönlichkeitsprofile gemäss Datenschutzrecht enthält.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}openingDate uses Python identifier openingDate
    __openingDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'openingDate'), 'openingDate', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392openingDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 159, 3), )

    
    openingDate = property(__openingDate.value, __openingDate.set, None, 'Eröffnungsdatum: Tag, an dem das Dokument im GEVER-System einem Dossier zugeordnet worden ist.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}owner uses Python identifier owner
    __owner = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'owner'), 'owner', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392owner', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 164, 3), )

    
    owner = property(__owner.value, __owner.set, None, 'Eigentümer: Name des Eigentümers des Dokuments.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}signer uses Python identifier signer
    __signer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'signer'), 'signer', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392signer', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 169, 3), )

    
    signer = property(__signer.value, __signer.set, None, 'Unterzeichner: Person, welche das Dokument unterzeichnet hat oder die Verantwortung dafür übernimmt.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}ourRecordReference uses Python identifier ourRecordReference
    __ourRecordReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ourRecordReference'), 'ourRecordReference', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392ourRecordReference', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 174, 3), )

    
    ourRecordReference = property(__ourRecordReference.value, __ourRecordReference.set, None, 'Unser Aktenzeichen: Referenz auf das entsprechende Dossier des Absenders.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}comments uses Python identifier comments
    __comments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comments'), 'comments', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392comments', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 179, 3), )

    
    comments = property(__comments.value, __comments.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}keywords uses Python identifier keywords
    __keywords = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'keywords'), 'keywords', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392keywords', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 180, 3), )

    
    keywords = property(__keywords.value, __keywords.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}isLeadingDocument uses Python identifier isLeadingDocument
    __isLeadingDocument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'isLeadingDocument'), 'isLeadingDocument', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392isLeadingDocument', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 181, 3), )

    
    isLeadingDocument = property(__isLeadingDocument.value, __isLeadingDocument.set, None, 'Hauptdokument: Angabe, ob es sich um das Hauptdokument (führendes Dokument) handelt.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}sortOrder uses Python identifier sortOrder
    __sortOrder = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sortOrder'), 'sortOrder', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392sortOrder', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 186, 3), )

    
    sortOrder = property(__sortOrder.value, __sortOrder.set, None, 'Sortierfolge: Angabe zur Reihenfolge der Sortierung von Dokumenten.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}documentKind uses Python identifier documentKind
    __documentKind = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'documentKind'), 'documentKind', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392documentKind', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 191, 3), )

    
    documentKind = property(__documentKind.value, __documentKind.set, None, 'Dokumenttyp: Fachliche Beschreibung des Dokuments (z.B. Vertrag, Antrag, Antwort. u.a).')

    
    # Attribute {http://www.ech.ch/xmlns/eCH-0039/2}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'lang'), 'lang', '__httpwww_ech_chxmlnseCH_00392_documentType_httpwww_ech_chxmlnseCH_00392lang', pyxb.binding.datatypes.language)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 546, 1)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 197, 2)
    
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
        __documentKind.name() : __documentKind
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.documentType = documentType
Namespace.addCategoryObject('typeBinding', 'documentType', documentType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}dossierType with content type ELEMENT_ONLY
class dossierType (pyxb.binding.basis.complexTypeDefinition):
    """Dossier: Basiskomponente zur Abbildung von Dossiers und Subdossiers."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dossierType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 216, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpwww_ech_chxmlnseCH_00392_dossierType_httpwww_ech_chxmlnseCH_00392uuid', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 221, 3), )

    
    uuid = property(__uuid.value, __uuid.set, None, 'UUID: Universally Unique Identifier des Dossiers. Referenz des Objekts, nicht der Nachricht.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}status uses Python identifier status
    __status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'status'), 'status', '__httpwww_ech_chxmlnseCH_00392_dossierType_httpwww_ech_chxmlnseCH_00392status', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 226, 3), )

    
    status = property(__status.value, __status.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}titles uses Python identifier titles
    __titles = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'titles'), 'titles', '__httpwww_ech_chxmlnseCH_00392_dossierType_httpwww_ech_chxmlnseCH_00392titles', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 227, 3), )

    
    titles = property(__titles.value, __titles.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}classification uses Python identifier classification
    __classification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'classification'), 'classification', '__httpwww_ech_chxmlnseCH_00392_dossierType_httpwww_ech_chxmlnseCH_00392classification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 228, 3), )

    
    classification = property(__classification.value, __classification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}hasPrivacyProtection uses Python identifier hasPrivacyProtection
    __hasPrivacyProtection = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection'), 'hasPrivacyProtection', '__httpwww_ech_chxmlnseCH_00392_dossierType_httpwww_ech_chxmlnseCH_00392hasPrivacyProtection', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 229, 3), )

    
    hasPrivacyProtection = property(__hasPrivacyProtection.value, __hasPrivacyProtection.set, None, 'Datenschutzstufe: Markierung, die angibt, ob das Dokument besonders Schützenswerte Personendaten oder Persönlichkeitsprofile gemäss Datenschutzrecht enthält.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}openToThePublicType uses Python identifier openToThePublicType
    __openToThePublicType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'openToThePublicType'), 'openToThePublicType', '__httpwww_ech_chxmlnseCH_00392_dossierType_httpwww_ech_chxmlnseCH_00392openToThePublicType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 234, 3), )

    
    openToThePublicType = property(__openToThePublicType.value, __openToThePublicType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}caseReferenceLocalId uses Python identifier caseReferenceLocalId
    __caseReferenceLocalId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'caseReferenceLocalId'), 'caseReferenceLocalId', '__httpwww_ech_chxmlnseCH_00392_dossierType_httpwww_ech_chxmlnseCH_00392caseReferenceLocalId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 235, 3), )

    
    caseReferenceLocalId = property(__caseReferenceLocalId.value, __caseReferenceLocalId.set, None, 'Ordnungsmerkmal: Ordnungsmerkmal des Dossiers, welches durch den Absender vergeben wird.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}openingDate uses Python identifier openingDate
    __openingDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'openingDate'), 'openingDate', '__httpwww_ech_chxmlnseCH_00392_dossierType_httpwww_ech_chxmlnseCH_00392openingDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 240, 3), )

    
    openingDate = property(__openingDate.value, __openingDate.set, None, 'Datum: Datum, an welchem das Dossier eröffnet / registriert wurde. ')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}keywords uses Python identifier keywords
    __keywords = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'keywords'), 'keywords', '__httpwww_ech_chxmlnseCH_00392_dossierType_httpwww_ech_chxmlnseCH_00392keywords', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 245, 3), )

    
    keywords = property(__keywords.value, __keywords.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}comments uses Python identifier comments
    __comments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comments'), 'comments', '__httpwww_ech_chxmlnseCH_00392_dossierType_httpwww_ech_chxmlnseCH_00392comments', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 246, 3), )

    
    comments = property(__comments.value, __comments.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}links uses Python identifier links
    __links = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'links'), 'links', '__httpwww_ech_chxmlnseCH_00392_dossierType_httpwww_ech_chxmlnseCH_00392links', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 247, 3), )

    
    links = property(__links.value, __links.set, None, None)

    
    # Attribute {http://www.ech.ch/xmlns/eCH-0039/2}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'lang'), 'lang', '__httpwww_ech_chxmlnseCH_00392_dossierType_httpwww_ech_chxmlnseCH_00392lang', pyxb.binding.datatypes.language)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 546, 1)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 249, 2)
    
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
        __links.name() : __links
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.dossierType = dossierType
Namespace.addCategoryObject('typeBinding', 'dossierType', dossierType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}fileType with content type ELEMENT_ONLY
class fileType (pyxb.binding.basis.complexTypeDefinition):
    """Datei: Metadaten der angehängten oder referenzierten
				Datei."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'fileType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 251, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}pathFileName uses Python identifier pathFileName
    __pathFileName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'pathFileName'), 'pathFileName', '__httpwww_ech_chxmlnseCH_00392_fileType_httpwww_ech_chxmlnseCH_00392pathFileName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 257, 3), )

    
    pathFileName = property(__pathFileName.value, __pathFileName.set, None, 'Pfad: Pfad zur Datei. Dabei kann es sich um einen lokalen Pfad oder eine URL handeln. Der Pfad bildet sich aus Pfad + Name + Extension (Dateiendung). Handelt es sich um eine lokale Referenz innehalb der ZIP-Datei, so beginnt der Pfad mit files/dateiname.extension')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}mimeType uses Python identifier mimeType
    __mimeType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'mimeType'), 'mimeType', '__httpwww_ech_chxmlnseCH_00392_fileType_httpwww_ech_chxmlnseCH_00392mimeType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 262, 3), )

    
    mimeType = property(__mimeType.value, __mimeType.set, None, 'MIME-Type der Datei.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}internalSortOrder uses Python identifier internalSortOrder
    __internalSortOrder = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'internalSortOrder'), 'internalSortOrder', '__httpwww_ech_chxmlnseCH_00392_fileType_httpwww_ech_chxmlnseCH_00392internalSortOrder', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 267, 3), )

    
    internalSortOrder = property(__internalSortOrder.value, __internalSortOrder.set, None, 'Sortierfolge: Angabe zur Reihenfolge der Sortierung bei Dokumenten, welche aus mehreren Dateien bestehen.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}version uses Python identifier version
    __version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'version'), 'version', '__httpwww_ech_chxmlnseCH_00392_fileType_httpwww_ech_chxmlnseCH_00392version', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 272, 3), )

    
    version = property(__version.value, __version.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}hashCode uses Python identifier hashCode
    __hashCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'hashCode'), 'hashCode', '__httpwww_ech_chxmlnseCH_00392_fileType_httpwww_ech_chxmlnseCH_00392hashCode', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 273, 3), )

    
    hashCode = property(__hashCode.value, __hashCode.set, None, 'Hashwert: Hashwert der Datei.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}hashCodeAlgorithm uses Python identifier hashCodeAlgorithm
    __hashCodeAlgorithm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'hashCodeAlgorithm'), 'hashCodeAlgorithm', '__httpwww_ech_chxmlnseCH_00392_fileType_httpwww_ech_chxmlnseCH_00392hashCodeAlgorithm', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 278, 3), )

    
    hashCodeAlgorithm = property(__hashCodeAlgorithm.value, __hashCodeAlgorithm.set, None, 'Hashalgorithmus: Abkürzung des Algorithmus welcher zur Bildung des Hashwerts verwendet wurde.')

    
    # Attribute {http://www.ech.ch/xmlns/eCH-0039/2}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'lang'), 'lang', '__httpwww_ech_chxmlnseCH_00392_fileType_httpwww_ech_chxmlnseCH_00392lang', pyxb.binding.datatypes.language)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 546, 1)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 284, 2)
    
    lang = property(__lang.value, __lang.set, None, 'Sprache: Attribut zur Angabe des Sprachcodes nach ISO 639-1 (zweistelliger Sprachcode). Ursprünglich RFC 1766.')

    _ElementMap.update({
        __pathFileName.name() : __pathFileName,
        __mimeType.name() : __mimeType,
        __internalSortOrder.name() : __internalSortOrder,
        __version.name() : __version,
        __hashCode.name() : __hashCode,
        __hashCodeAlgorithm.name() : __hashCodeAlgorithm
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.fileType = fileType
Namespace.addCategoryObject('typeBinding', 'fileType', fileType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}filesType with content type ELEMENT_ONLY
class filesType (pyxb.binding.basis.complexTypeDefinition):
    """Dateien: Enthält eine oder mehrere übergebene oder referenzierte Dateien."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'filesType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 286, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}file uses Python identifier file
    __file = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'file'), 'file', '__httpwww_ech_chxmlnseCH_00392_filesType_httpwww_ech_chxmlnseCH_00392file', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 291, 3), )

    
    file = property(__file.value, __file.set, None, None)

    _ElementMap.update({
        __file.name() : __file
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.filesType = filesType
Namespace.addCategoryObject('typeBinding', 'filesType', filesType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}headerType with content type ELEMENT_ONLY
class headerType (pyxb.binding.basis.complexTypeDefinition):
    """Header: Enthält die Headerinformationen für Erstmeldungen und implementiert eCH-0058 (Version 3.0) Meldungsrahmen."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'headerType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 294, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}senderId uses Python identifier senderId
    __senderId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'senderId'), 'senderId', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392senderId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 299, 3), )

    
    senderId = property(__senderId.value, __senderId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}messageId uses Python identifier messageId
    __messageId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageId'), 'messageId', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392messageId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 300, 3), )

    
    messageId = property(__messageId.value, __messageId.set, None, 'Nachrichten-ID: Empfehlung des Einsatzes von UUID für die eindeutige Referenz von übermittelten Nachrichten.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}messageGroup uses Python identifier messageGroup
    __messageGroup = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageGroup'), 'messageGroup', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392messageGroup', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 305, 3), )

    
    messageGroup = property(__messageGroup.value, __messageGroup.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}messageType uses Python identifier messageType
    __messageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageType'), 'messageType', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392messageType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 306, 3), )

    
    messageType = property(__messageType.value, __messageType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}sendingApplication uses Python identifier sendingApplication
    __sendingApplication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication'), 'sendingApplication', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392sendingApplication', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 307, 3), )

    
    sendingApplication = property(__sendingApplication.value, __sendingApplication.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}messageDate uses Python identifier messageDate
    __messageDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageDate'), 'messageDate', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392messageDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 308, 3), )

    
    messageDate = property(__messageDate.value, __messageDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}action uses Python identifier action
    __action = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'action'), 'action', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392action', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 309, 3), )

    
    action = property(__action.value, __action.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}testDeliveryFlag uses Python identifier testDeliveryFlag
    __testDeliveryFlag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag'), 'testDeliveryFlag', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392testDeliveryFlag', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 310, 3), )

    
    testDeliveryFlag = property(__testDeliveryFlag.value, __testDeliveryFlag.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}recipientId uses Python identifier recipientId
    __recipientId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'recipientId'), 'recipientId', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392recipientId', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 311, 3), )

    
    recipientId = property(__recipientId.value, __recipientId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}originalSenderId uses Python identifier originalSenderId
    __originalSenderId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'originalSenderId'), 'originalSenderId', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392originalSenderId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 312, 3), )

    
    originalSenderId = property(__originalSenderId.value, __originalSenderId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}declarationLocalReference uses Python identifier declarationLocalReference
    __declarationLocalReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'declarationLocalReference'), 'declarationLocalReference', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392declarationLocalReference', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 313, 3), )

    
    declarationLocalReference = property(__declarationLocalReference.value, __declarationLocalReference.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}referenceMessageId uses Python identifier referenceMessageId
    __referenceMessageId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId'), 'referenceMessageId', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392referenceMessageId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 314, 3), )

    
    referenceMessageId = property(__referenceMessageId.value, __referenceMessageId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}uniqueIdBusinessTransaction uses Python identifier uniqueIdBusinessTransaction
    __uniqueIdBusinessTransaction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessTransaction'), 'uniqueIdBusinessTransaction', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392uniqueIdBusinessTransaction', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 315, 3), )

    
    uniqueIdBusinessTransaction = property(__uniqueIdBusinessTransaction.value, __uniqueIdBusinessTransaction.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}ourBusinessReferenceId uses Python identifier ourBusinessReferenceId
    __ourBusinessReferenceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId'), 'ourBusinessReferenceId', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392ourBusinessReferenceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 316, 3), )

    
    ourBusinessReferenceId = property(__ourBusinessReferenceId.value, __ourBusinessReferenceId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}yourBusinessReferenceId uses Python identifier yourBusinessReferenceId
    __yourBusinessReferenceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId'), 'yourBusinessReferenceId', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392yourBusinessReferenceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 317, 3), )

    
    yourBusinessReferenceId = property(__yourBusinessReferenceId.value, __yourBusinessReferenceId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}subMessageType uses Python identifier subMessageType
    __subMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subMessageType'), 'subMessageType', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392subMessageType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 318, 3), )

    
    subMessageType = property(__subMessageType.value, __subMessageType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}partialDelivery uses Python identifier partialDelivery
    __partialDelivery = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'partialDelivery'), 'partialDelivery', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392partialDelivery', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 319, 3), )

    
    partialDelivery = property(__partialDelivery.value, __partialDelivery.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}subjects uses Python identifier subjects
    __subjects = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subjects'), 'subjects', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392subjects', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 328, 3), )

    
    subjects = property(__subjects.value, __subjects.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}object uses Python identifier object
    __object = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'object'), 'object', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392object', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 329, 3), )

    
    object = property(__object.value, __object.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}comments uses Python identifier comments
    __comments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comments'), 'comments', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392comments', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 330, 3), )

    
    comments = property(__comments.value, __comments.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}initialMessageDate uses Python identifier initialMessageDate
    __initialMessageDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate'), 'initialMessageDate', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392initialMessageDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 331, 3), )

    
    initialMessageDate = property(__initialMessageDate.value, __initialMessageDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}eventDate uses Python identifier eventDate
    __eventDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventDate'), 'eventDate', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392eventDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 332, 3), )

    
    eventDate = property(__eventDate.value, __eventDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}eventPeriod uses Python identifier eventPeriod
    __eventPeriod = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventPeriod'), 'eventPeriod', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392eventPeriod', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 333, 3), )

    
    eventPeriod = property(__eventPeriod.value, __eventPeriod.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}modificationDate uses Python identifier modificationDate
    __modificationDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'modificationDate'), 'modificationDate', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392modificationDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 334, 3), )

    
    modificationDate = property(__modificationDate.value, __modificationDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}testData uses Python identifier testData
    __testData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'testData'), 'testData', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392testData', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 335, 3), )

    
    testData = property(__testData.value, __testData.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}reference uses Python identifier reference
    __reference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'reference'), 'reference', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392reference', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 336, 3), )

    
    reference = property(__reference.value, __reference.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_00392_headerType_httpwww_ech_chxmlnseCH_00392extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 337, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __senderId.name() : __senderId,
        __messageId.name() : __messageId,
        __messageGroup.name() : __messageGroup,
        __messageType.name() : __messageType,
        __sendingApplication.name() : __sendingApplication,
        __messageDate.name() : __messageDate,
        __action.name() : __action,
        __testDeliveryFlag.name() : __testDeliveryFlag,
        __recipientId.name() : __recipientId,
        __originalSenderId.name() : __originalSenderId,
        __declarationLocalReference.name() : __declarationLocalReference,
        __referenceMessageId.name() : __referenceMessageId,
        __uniqueIdBusinessTransaction.name() : __uniqueIdBusinessTransaction,
        __ourBusinessReferenceId.name() : __ourBusinessReferenceId,
        __yourBusinessReferenceId.name() : __yourBusinessReferenceId,
        __subMessageType.name() : __subMessageType,
        __partialDelivery.name() : __partialDelivery,
        __subjects.name() : __subjects,
        __object.name() : __object,
        __comments.name() : __comments,
        __initialMessageDate.name() : __initialMessageDate,
        __eventDate.name() : __eventDate,
        __eventPeriod.name() : __eventPeriod,
        __modificationDate.name() : __modificationDate,
        __testData.name() : __testData,
        __reference.name() : __reference,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.headerType = headerType
Namespace.addCategoryObject('typeBinding', 'headerType', headerType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 320, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}uniqueIdBusinessCase uses Python identifier uniqueIdBusinessCase
    __uniqueIdBusinessCase = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessCase'), 'uniqueIdBusinessCase', '__httpwww_ech_chxmlnseCH_00392_CTD_ANON_httpwww_ech_chxmlnseCH_00392uniqueIdBusinessCase', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 322, 6), )

    
    uniqueIdBusinessCase = property(__uniqueIdBusinessCase.value, __uniqueIdBusinessCase.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}totalNumberOfPackages uses Python identifier totalNumberOfPackages
    __totalNumberOfPackages = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'totalNumberOfPackages'), 'totalNumberOfPackages', '__httpwww_ech_chxmlnseCH_00392_CTD_ANON_httpwww_ech_chxmlnseCH_00392totalNumberOfPackages', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 323, 6), )

    
    totalNumberOfPackages = property(__totalNumberOfPackages.value, __totalNumberOfPackages.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}numberOfActualPackage uses Python identifier numberOfActualPackage
    __numberOfActualPackage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'numberOfActualPackage'), 'numberOfActualPackage', '__httpwww_ech_chxmlnseCH_00392_CTD_ANON_httpwww_ech_chxmlnseCH_00392numberOfActualPackage', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 324, 6), )

    
    numberOfActualPackage = property(__numberOfActualPackage.value, __numberOfActualPackage.set, None, None)

    _ElementMap.update({
        __uniqueIdBusinessCase.name() : __uniqueIdBusinessCase,
        __totalNumberOfPackages.name() : __totalNumberOfPackages,
        __numberOfActualPackage.name() : __numberOfActualPackage
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}keywordType with content type SIMPLE
class keywordType (pyxb.binding.basis.complexTypeDefinition):
    """Schlagwort: Enthält ein Schlagwort. Die Sprache kann im Attribut angegeben werden."""
    _TypeDefinition = pyxb.binding.datatypes.token
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'keywordType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 340, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.token
    
    # Attribute {http://www.ech.ch/xmlns/eCH-0039/2}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'lang'), 'lang', '__httpwww_ech_chxmlnseCH_00392_keywordType_httpwww_ech_chxmlnseCH_00392lang', pyxb.binding.datatypes.language)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 546, 1)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 346, 4)
    
    lang = property(__lang.value, __lang.set, None, 'Sprache: Attribut zur Angabe des Sprachcodes nach ISO 639-1 (zweistelliger Sprachcode). Ursprünglich RFC 1766.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.keywordType = keywordType
Namespace.addCategoryObject('typeBinding', 'keywordType', keywordType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}keywordsType with content type ELEMENT_ONLY
class keywordsType (pyxb.binding.basis.complexTypeDefinition):
    """Schlagwörter: Enthält ein oder mehrere Schlagwörter."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'keywordsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 350, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}keyword uses Python identifier keyword
    __keyword = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'keyword'), 'keyword', '__httpwww_ech_chxmlnseCH_00392_keywordsType_httpwww_ech_chxmlnseCH_00392keyword', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 355, 3), )

    
    keyword = property(__keyword.value, __keyword.set, None, None)

    _ElementMap.update({
        __keyword.name() : __keyword
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.keywordsType = keywordsType
Namespace.addCategoryObject('typeBinding', 'keywordsType', keywordsType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}linkType with content type SIMPLE
class linkType (pyxb.binding.basis.complexTypeDefinition):
    """Verweis: Referenz auf eine Ordnungssystemposition oder ein Dossier, welches in enger Beziehung mit dem Dossier steht ohne in direkter hierarchischer Linie mit ihm verknüpft zu sein."""
    _TypeDefinition = pyxb.binding.datatypes.token
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'linkType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 358, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.token
    
    # Attribute {http://www.ech.ch/xmlns/eCH-0039/2}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'lang'), 'lang', '__httpwww_ech_chxmlnseCH_00392_linkType_httpwww_ech_chxmlnseCH_00392lang', pyxb.binding.datatypes.language)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 546, 1)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 364, 4)
    
    lang = property(__lang.value, __lang.set, None, 'Sprache: Attribut zur Angabe des Sprachcodes nach ISO 639-1 (zweistelliger Sprachcode). Ursprünglich RFC 1766.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.linkType = linkType
Namespace.addCategoryObject('typeBinding', 'linkType', linkType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}linksType with content type ELEMENT_ONLY
class linksType (pyxb.binding.basis.complexTypeDefinition):
    """Links: Enthält ein oder mehrere Referenzen / Verweise. """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'linksType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 368, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}link uses Python identifier link
    __link = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'link'), 'link', '__httpwww_ech_chxmlnseCH_00392_linksType_httpwww_ech_chxmlnseCH_00392link', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 373, 3), )

    
    link = property(__link.value, __link.set, None, None)

    _ElementMap.update({
        __link.name() : __link
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.linksType = linksType
Namespace.addCategoryObject('typeBinding', 'linksType', linksType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}messageGroupType with content type ELEMENT_ONLY
class messageGroupType (pyxb.binding.basis.complexTypeDefinition):
    """Nachrichtengruppe: Identifiziert die Nachrichtengruppe und den Nachrichtentyp nach eCH-0039."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'messageGroupType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 376, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}messageGroupId uses Python identifier messageGroupId
    __messageGroupId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageGroupId'), 'messageGroupId', '__httpwww_ech_chxmlnseCH_00392_messageGroupType_httpwww_ech_chxmlnseCH_00392messageGroupId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 381, 3), )

    
    messageGroupId = property(__messageGroupId.value, __messageGroupId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}messageTypeId uses Python identifier messageTypeId
    __messageTypeId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageTypeId'), 'messageTypeId', '__httpwww_ech_chxmlnseCH_00392_messageGroupType_httpwww_ech_chxmlnseCH_00392messageTypeId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 382, 3), )

    
    messageTypeId = property(__messageTypeId.value, __messageTypeId.set, None, None)

    _ElementMap.update({
        __messageGroupId.name() : __messageGroupId,
        __messageTypeId.name() : __messageTypeId
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.messageGroupType = messageGroupType
Namespace.addCategoryObject('typeBinding', 'messageGroupType', messageGroupType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}referenceType with content type ELEMENT_ONLY
class referenceType (pyxb.binding.basis.complexTypeDefinition):
    """Referenz: Basiskomponente welche die Referenz auf übergeordnete Leistungen und Geschäftsprozesse enthält."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'referenceType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 405, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpwww_ech_chxmlnseCH_00392_referenceType_httpwww_ech_chxmlnseCH_00392uuid', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 410, 3), )

    
    uuid = property(__uuid.value, __uuid.set, None, 'UUID: Universally Unique Identifier der Referenz. ')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}serviceInventoryId uses Python identifier serviceInventoryId
    __serviceInventoryId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'serviceInventoryId'), 'serviceInventoryId', '__httpwww_ech_chxmlnseCH_00392_referenceType_httpwww_ech_chxmlnseCH_00392serviceInventoryId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 415, 3), )

    
    serviceInventoryId = property(__serviceInventoryId.value, __serviceInventoryId.set, None, 'Leistungsinventar: Identifikationsnummer des referenzierten Leistungsinventars (gemäss eCH-0070 Leistungsinventar eGov CH) Leistungen sind immer eindeutig entweder einem lokalen, re¬gionalen oder globalen Inventar zugeordnet.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}serviceId uses Python identifier serviceId
    __serviceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'serviceId'), 'serviceId', '__httpwww_ech_chxmlnseCH_00392_referenceType_httpwww_ech_chxmlnseCH_00392serviceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 420, 3), )

    
    serviceId = property(__serviceId.value, __serviceId.set, None, 'Identifikationsnummer: Eindeutige Identifikationsnummer einer Leistung (gemäss eCH-0070 Leistungsinventar eGov CH).')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}serviceTitle uses Python identifier serviceTitle
    __serviceTitle = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'serviceTitle'), 'serviceTitle', '__httpwww_ech_chxmlnseCH_00392_referenceType_httpwww_ech_chxmlnseCH_00392serviceTitle', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 425, 3), )

    
    serviceTitle = property(__serviceTitle.value, __serviceTitle.set, None, 'Titel: Bezeichnung der Leistung (gemäss eCH-0070 Leistungsinventar eGov CH).')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}serviceProvider uses Python identifier serviceProvider
    __serviceProvider = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'serviceProvider'), 'serviceProvider', '__httpwww_ech_chxmlnseCH_00392_referenceType_httpwww_ech_chxmlnseCH_00392serviceProvider', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 430, 3), )

    
    serviceProvider = property(__serviceProvider.value, __serviceProvider.set, None, 'Leistungserbringer: Identifikation des Leistungserbringers (federführende Behörde oder Stelle) gemäss Schweizerischem Behördenverzeichnis.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}caseId uses Python identifier caseId
    __caseId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'caseId'), 'caseId', '__httpwww_ech_chxmlnseCH_00392_referenceType_httpwww_ech_chxmlnseCH_00392caseId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 435, 3), )

    
    caseId = property(__caseId.value, __caseId.set, None, 'Geschäftsfall: Identifikation des Geschäftsfalls (wird von der federführenden Stelle vergeben).')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}caseTitle uses Python identifier caseTitle
    __caseTitle = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'caseTitle'), 'caseTitle', '__httpwww_ech_chxmlnseCH_00392_referenceType_httpwww_ech_chxmlnseCH_00392caseTitle', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 440, 3), )

    
    caseTitle = property(__caseTitle.value, __caseTitle.set, None, 'Titel: Benennung des Geschäftsvorfalls.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}caseAnnotation uses Python identifier caseAnnotation
    __caseAnnotation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'caseAnnotation'), 'caseAnnotation', '__httpwww_ech_chxmlnseCH_00392_referenceType_httpwww_ech_chxmlnseCH_00392caseAnnotation', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 445, 3), )

    
    caseAnnotation = property(__caseAnnotation.value, __caseAnnotation.set, None, 'Bemerkung: Informationen zum Geschäftsvorfall.')

    _ElementMap.update({
        __uuid.name() : __uuid,
        __serviceInventoryId.name() : __serviceInventoryId,
        __serviceId.name() : __serviceId,
        __serviceTitle.name() : __serviceTitle,
        __serviceProvider.name() : __serviceProvider,
        __caseId.name() : __caseId,
        __caseTitle.name() : __caseTitle,
        __caseAnnotation.name() : __caseAnnotation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.referenceType = referenceType
Namespace.addCategoryObject('typeBinding', 'referenceType', referenceType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}reportHeaderType with content type ELEMENT_ONLY
class reportHeaderType (pyxb.binding.basis.complexTypeDefinition):
    """Report Header: Enthält die Headerinformationen einer Antwortmeldungen und implementiert eCH-0058 Meldungsrahmen."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'reportHeaderType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 462, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}senderId uses Python identifier senderId
    __senderId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'senderId'), 'senderId', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392senderId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 467, 3), )

    
    senderId = property(__senderId.value, __senderId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}messageId uses Python identifier messageId
    __messageId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageId'), 'messageId', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392messageId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 468, 3), )

    
    messageId = property(__messageId.value, __messageId.set, None, 'Nachrichten-ID: Empfehlung des Einsatzes von UUID für die eindeutige Referenz von übermittelten Nachrichten.')

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}messageGroup uses Python identifier messageGroup
    __messageGroup = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageGroup'), 'messageGroup', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392messageGroup', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 473, 3), )

    
    messageGroup = property(__messageGroup.value, __messageGroup.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}messageType uses Python identifier messageType
    __messageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageType'), 'messageType', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392messageType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 474, 3), )

    
    messageType = property(__messageType.value, __messageType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}sendingApplication uses Python identifier sendingApplication
    __sendingApplication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication'), 'sendingApplication', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392sendingApplication', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 475, 3), )

    
    sendingApplication = property(__sendingApplication.value, __sendingApplication.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}action uses Python identifier action
    __action = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'action'), 'action', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392action', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 476, 3), )

    
    action = property(__action.value, __action.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}testDeliveryFlag uses Python identifier testDeliveryFlag
    __testDeliveryFlag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag'), 'testDeliveryFlag', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392testDeliveryFlag', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 477, 3), )

    
    testDeliveryFlag = property(__testDeliveryFlag.value, __testDeliveryFlag.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}recipientId uses Python identifier recipientId
    __recipientId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'recipientId'), 'recipientId', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392recipientId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 478, 3), )

    
    recipientId = property(__recipientId.value, __recipientId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}referenceMessageId uses Python identifier referenceMessageId
    __referenceMessageId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId'), 'referenceMessageId', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392referenceMessageId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 479, 3), )

    
    referenceMessageId = property(__referenceMessageId.value, __referenceMessageId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}ourBusinessReferenceId uses Python identifier ourBusinessReferenceId
    __ourBusinessReferenceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId'), 'ourBusinessReferenceId', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392ourBusinessReferenceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 480, 3), )

    
    ourBusinessReferenceId = property(__ourBusinessReferenceId.value, __ourBusinessReferenceId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}yourBusinessReferenceId uses Python identifier yourBusinessReferenceId
    __yourBusinessReferenceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId'), 'yourBusinessReferenceId', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392yourBusinessReferenceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 481, 3), )

    
    yourBusinessReferenceId = property(__yourBusinessReferenceId.value, __yourBusinessReferenceId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}uniqueIdBusinessTransaction uses Python identifier uniqueIdBusinessTransaction
    __uniqueIdBusinessTransaction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessTransaction'), 'uniqueIdBusinessTransaction', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392uniqueIdBusinessTransaction', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 482, 3), )

    
    uniqueIdBusinessTransaction = property(__uniqueIdBusinessTransaction.value, __uniqueIdBusinessTransaction.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}subMessageType uses Python identifier subMessageType
    __subMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subMessageType'), 'subMessageType', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392subMessageType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 483, 3), )

    
    subMessageType = property(__subMessageType.value, __subMessageType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}object uses Python identifier object
    __object = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'object'), 'object', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392object', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 484, 3), )

    
    object = property(__object.value, __object.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}initialMessageDate uses Python identifier initialMessageDate
    __initialMessageDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate'), 'initialMessageDate', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392initialMessageDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 485, 3), )

    
    initialMessageDate = property(__initialMessageDate.value, __initialMessageDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}testData uses Python identifier testData
    __testData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'testData'), 'testData', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392testData', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 486, 3), )

    
    testData = property(__testData.value, __testData.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}reference uses Python identifier reference
    __reference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'reference'), 'reference', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392reference', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 487, 3), )

    
    reference = property(__reference.value, __reference.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_00392_reportHeaderType_httpwww_ech_chxmlnseCH_00392extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 488, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __senderId.name() : __senderId,
        __messageId.name() : __messageId,
        __messageGroup.name() : __messageGroup,
        __messageType.name() : __messageType,
        __sendingApplication.name() : __sendingApplication,
        __action.name() : __action,
        __testDeliveryFlag.name() : __testDeliveryFlag,
        __recipientId.name() : __recipientId,
        __referenceMessageId.name() : __referenceMessageId,
        __ourBusinessReferenceId.name() : __ourBusinessReferenceId,
        __yourBusinessReferenceId.name() : __yourBusinessReferenceId,
        __uniqueIdBusinessTransaction.name() : __uniqueIdBusinessTransaction,
        __subMessageType.name() : __subMessageType,
        __object.name() : __object,
        __initialMessageDate.name() : __initialMessageDate,
        __testData.name() : __testData,
        __reference.name() : __reference,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.reportHeaderType = reportHeaderType
Namespace.addCategoryObject('typeBinding', 'reportHeaderType', reportHeaderType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}reportType with content type ELEMENT_ONLY
class reportType (pyxb.binding.basis.complexTypeDefinition):
    """Report Typ: Definiert die bei der Antwort möglichen Reporttypen (positiver und negativer Report)."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'reportType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 491, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}positiveReport uses Python identifier positiveReport
    __positiveReport = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'positiveReport'), 'positiveReport', '__httpwww_ech_chxmlnseCH_00392_reportType_httpwww_ech_chxmlnseCH_00392positiveReport', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 496, 3), )

    
    positiveReport = property(__positiveReport.value, __positiveReport.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}negativeReport uses Python identifier negativeReport
    __negativeReport = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'negativeReport'), 'negativeReport', '__httpwww_ech_chxmlnseCH_00392_reportType_httpwww_ech_chxmlnseCH_00392negativeReport', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 497, 3), )

    
    negativeReport = property(__negativeReport.value, __negativeReport.set, None, None)

    _ElementMap.update({
        __positiveReport.name() : __positiveReport,
        __negativeReport.name() : __negativeReport
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.reportType = reportType
Namespace.addCategoryObject('typeBinding', 'reportType', reportType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}subjectType with content type SIMPLE
class subjectType (pyxb.binding.basis.complexTypeDefinition):
    """Betreff: Die Sprache kann im Attribut angegeben werden."""
    _TypeDefinition = pyxb.binding.datatypes.token
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'subjectType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 500, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.token
    
    # Attribute {http://www.ech.ch/xmlns/eCH-0039/2}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'lang'), 'lang', '__httpwww_ech_chxmlnseCH_00392_subjectType_httpwww_ech_chxmlnseCH_00392lang', pyxb.binding.datatypes.language)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 546, 1)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 506, 4)
    
    lang = property(__lang.value, __lang.set, None, 'Sprache: Attribut zur Angabe des Sprachcodes nach ISO 639-1 (zweistelliger Sprachcode). Ursprünglich RFC 1766.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.subjectType = subjectType
Namespace.addCategoryObject('typeBinding', 'subjectType', subjectType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}subjectsType with content type ELEMENT_ONLY
class subjectsType (pyxb.binding.basis.complexTypeDefinition):
    """Betreff: Enthält eine oder mehrere Betreff."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'subjectsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 510, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subject'), 'subject', '__httpwww_ech_chxmlnseCH_00392_subjectsType_httpwww_ech_chxmlnseCH_00392subject', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 515, 3), )

    
    subject = property(__subject.value, __subject.set, None, None)

    _ElementMap.update({
        __subject.name() : __subject
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.subjectsType = subjectsType
Namespace.addCategoryObject('typeBinding', 'subjectsType', subjectsType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}titleType with content type SIMPLE
class titleType (pyxb.binding.basis.complexTypeDefinition):
    """Titel: Enthält einen Titel. Die Sprache kann im Attribut angegeben werden."""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'titleType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 518, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute {http://www.ech.ch/xmlns/eCH-0039/2}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'lang'), 'lang', '__httpwww_ech_chxmlnseCH_00392_titleType_httpwww_ech_chxmlnseCH_00392lang', pyxb.binding.datatypes.language)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 546, 1)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 524, 4)
    
    lang = property(__lang.value, __lang.set, None, 'Sprache: Attribut zur Angabe des Sprachcodes nach ISO 639-1 (zweistelliger Sprachcode). Ursprünglich RFC 1766.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.titleType = titleType
Namespace.addCategoryObject('typeBinding', 'titleType', titleType)


# Complex type {http://www.ech.ch/xmlns/eCH-0039/2}titlesType with content type ELEMENT_ONLY
class titlesType (pyxb.binding.basis.complexTypeDefinition):
    """Titel: Enthält ein oder mehrere Titel."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'titlesType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 528, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0039/2}title uses Python identifier title
    __title = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'title'), 'title', '__httpwww_ech_chxmlnseCH_00392_titlesType_httpwww_ech_chxmlnseCH_00392title', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 533, 3), )

    
    title = property(__title.value, __title.set, None, None)

    _ElementMap.update({
        __title.name() : __title
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.titlesType = titlesType
Namespace.addCategoryObject('typeBinding', 'titlesType', titlesType)




addressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.token, scope=addressType, documentation='UUID: Universally Unique Identifier der Adresse. Referenz des Objekts, nicht der Nachricht.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 14, 3)))

addressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'transactionRole'), transactionRoleType, scope=addressType, documentation='Transaktionsrolle: Angabe, ob es sich bei der Rolle um einen Absender, Emfpänger oder Beteiligten (Kopie an) handelt.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 19, 3)))

addressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'position'), pyxb.binding.datatypes.token, scope=addressType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 24, 3)))

addressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contact'), _ImportedBinding_camac_echbern_schema_ech_0046_1_0.contactType, scope=addressType, documentation='Kontaktinformatione: Implementiert eCH-0046 Datenstandard Kontakt.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 25, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 19, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 24, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 25, 3))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(addressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 14, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(addressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'transactionRole')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 19, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(addressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'position')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 24, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(addressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'contact')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 25, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
addressType._Automaton = _BuildAutomaton()




commentsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comment'), commentType, scope=commentsType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 74, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(commentsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comment')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 74, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
commentsType._Automaton = _BuildAutomaton_()




directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.token, scope=directiveType, documentation='UUID: Universally Unique Identifier der Anweisung. Referenz des Objekts, nicht der Nachricht.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 82, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'instruction'), directiveInstructionType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 87, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'priority'), priorityType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 88, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'titles'), titlesType, scope=directiveType, documentation='Titel: Benennung von Tätigkeit und Gegenstand des Geschäftsvorfalls.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 89, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'deadline'), pyxb.binding.datatypes.date, scope=directiveType, documentation='Bearbeitungsfrist: Tag, an dem die Aktivität erledigt sein soll.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 94, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'serviceId'), pyxb.binding.datatypes.token, scope=directiveType, documentation='Leistungsidentifikation: Identifikation der Leistung gemäss eCH-0070 Leistungsinventar eGov CH.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 99, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comments'), commentsType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 104, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 89, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 94, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 99, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 104, 3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 82, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'instruction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 87, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'priority')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 88, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'titles')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 89, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'deadline')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 94, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'serviceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 99, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comments')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 104, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
directiveType._Automaton = _BuildAutomaton_2()




documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.token, scope=documentType, documentation='UUID: Universally Unique Identifier des Dokuments. Referenz des Objekts, nicht der Nachricht.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 144, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'titles'), titlesType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 149, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'status'), documentStatusType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 150, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'files'), filesType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 151, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'classification'), classificationType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 152, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'openToThePublic'), openToThePublicType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 153, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection'), pyxb.binding.datatypes.boolean, scope=documentType, documentation='Datenschutzstufe: Markierung, die angibt, ob das Dokument besonders Schützenswerte Personendaten oder Persönlichkeitsprofile gemäss Datenschutzrecht enthält.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 154, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'openingDate'), pyxb.binding.datatypes.date, scope=documentType, documentation='Eröffnungsdatum: Tag, an dem das Dokument im GEVER-System einem Dossier zugeordnet worden ist.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 159, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'owner'), pyxb.binding.datatypes.token, scope=documentType, documentation='Eigentümer: Name des Eigentümers des Dokuments.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 164, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signer'), pyxb.binding.datatypes.token, scope=documentType, documentation='Unterzeichner: Person, welche das Dokument unterzeichnet hat oder die Verantwortung dafür übernimmt.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 169, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ourRecordReference'), pyxb.binding.datatypes.token, scope=documentType, documentation='Unser Aktenzeichen: Referenz auf das entsprechende Dossier des Absenders.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 174, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comments'), commentsType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 179, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'keywords'), keywordsType, scope=documentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 180, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'isLeadingDocument'), pyxb.binding.datatypes.boolean, scope=documentType, documentation='Hauptdokument: Angabe, ob es sich um das Hauptdokument (führendes Dokument) handelt.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 181, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sortOrder'), pyxb.binding.datatypes.nonNegativeInteger, scope=documentType, documentation='Sortierfolge: Angabe zur Reihenfolge der Sortierung von Dokumenten.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 186, 3)))

documentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'documentKind'), pyxb.binding.datatypes.token, scope=documentType, documentation='Dokumenttyp: Fachliche Beschreibung des Dokuments (z.B. Vertrag, Antrag, Antwort. u.a).', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 191, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 152, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 153, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 154, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 159, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 164, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 169, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 174, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 179, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 180, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 181, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 186, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 191, 3))
    counters.add(cc_11)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 144, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'titles')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 149, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'status')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 150, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'files')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 151, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'classification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 152, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'openToThePublic')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 153, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 154, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'openingDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 159, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'owner')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 164, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'signer')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 169, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ourRecordReference')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 174, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comments')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 179, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'keywords')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 180, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'isLeadingDocument')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 181, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sortOrder')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 186, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(documentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'documentKind')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 191, 3))
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
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, True) ]))
    st_15._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
documentType._Automaton = _BuildAutomaton_3()




dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.token, scope=dossierType, documentation='UUID: Universally Unique Identifier des Dossiers. Referenz des Objekts, nicht der Nachricht.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 221, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'status'), dossierStatusType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 226, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'titles'), titlesType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 227, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'classification'), classificationType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 228, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection'), pyxb.binding.datatypes.boolean, scope=dossierType, documentation='Datenschutzstufe: Markierung, die angibt, ob das Dokument besonders Schützenswerte Personendaten oder Persönlichkeitsprofile gemäss Datenschutzrecht enthält.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 229, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'openToThePublicType'), openToThePublicType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 234, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'caseReferenceLocalId'), pyxb.binding.datatypes.token, scope=dossierType, documentation='Ordnungsmerkmal: Ordnungsmerkmal des Dossiers, welches durch den Absender vergeben wird.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 235, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'openingDate'), pyxb.binding.datatypes.date, scope=dossierType, documentation='Datum: Datum, an welchem das Dossier eröffnet / registriert wurde. ', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 240, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'keywords'), keywordsType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 245, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comments'), commentsType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 246, 3)))

dossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'links'), linksType, scope=dossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 247, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 228, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 229, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 234, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 235, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 240, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 245, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 246, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 247, 3))
    counters.add(cc_7)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 221, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'status')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 226, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'titles')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 227, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'classification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 228, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'hasPrivacyProtection')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 229, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'openToThePublicType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 234, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'caseReferenceLocalId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 235, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'openingDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 240, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'keywords')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 245, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comments')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 246, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(dossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'links')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 247, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
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
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_10._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
dossierType._Automaton = _BuildAutomaton_4()




fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'pathFileName'), pyxb.binding.datatypes.token, scope=fileType, documentation='Pfad: Pfad zur Datei. Dabei kann es sich um einen lokalen Pfad oder eine URL handeln. Der Pfad bildet sich aus Pfad + Name + Extension (Dateiendung). Handelt es sich um eine lokale Referenz innehalb der ZIP-Datei, so beginnt der Pfad mit files/dateiname.extension', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 257, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mimeType'), pyxb.binding.datatypes.token, scope=fileType, documentation='MIME-Type der Datei.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 262, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'internalSortOrder'), pyxb.binding.datatypes.nonNegativeInteger, scope=fileType, documentation='Sortierfolge: Angabe zur Reihenfolge der Sortierung bei Dokumenten, welche aus mehreren Dateien bestehen.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 267, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'version'), pyxb.binding.datatypes.token, scope=fileType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 272, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'hashCode'), pyxb.binding.datatypes.token, scope=fileType, documentation='Hashwert: Hashwert der Datei.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 273, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'hashCodeAlgorithm'), pyxb.binding.datatypes.token, scope=fileType, documentation='Hashalgorithmus: Abkürzung des Algorithmus welcher zur Bildung des Hashwerts verwendet wurde.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 278, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 267, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 272, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 273, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 278, 3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'pathFileName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 257, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'mimeType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 262, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'internalSortOrder')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 267, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'version')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 272, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'hashCode')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 273, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'hashCodeAlgorithm')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 278, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
fileType._Automaton = _BuildAutomaton_5()




filesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'file'), fileType, scope=filesType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 291, 3)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(filesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'file')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 291, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
filesType._Automaton = _BuildAutomaton_6()




headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'senderId'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.participantIdType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 299, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageId'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.messageIdType, scope=headerType, documentation='Nachrichten-ID: Empfehlung des Einsatzes von UUID für die eindeutige Referenz von übermittelten Nachrichten.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 300, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageGroup'), messageGroupType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 305, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageType'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.messageTypeType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 306, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.sendingApplicationType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 307, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageDate'), pyxb.binding.datatypes.dateTime, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 308, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'action'), actionType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 309, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.testDeliveryFlagType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 310, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'recipientId'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.participantIdType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 311, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'originalSenderId'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.participantIdType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 312, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'declarationLocalReference'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.declarationLocalReferenceType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 313, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.messageIdType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 314, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessTransaction'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.uniqueIdBusinessTransactionType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 315, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.businessReferenceIdType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 316, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.businessReferenceIdType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 317, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subMessageType'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.subMessageTypeType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 318, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'partialDelivery'), CTD_ANON, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 319, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subjects'), subjectsType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 328, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'object'), pyxb.binding.datatypes.anyType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 329, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comments'), commentsType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 330, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate'), pyxb.binding.datatypes.dateTime, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 331, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventDate'), pyxb.binding.datatypes.dateTime, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 332, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventPeriod'), pyxb.binding.datatypes.token, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 333, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'modificationDate'), pyxb.binding.datatypes.dateTime, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 334, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'testData'), pyxb.binding.datatypes.anyType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 335, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reference'), referenceType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 336, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 337, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 311, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 312, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 313, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 314, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 315, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 316, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 317, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 318, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 319, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 328, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 329, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 330, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 331, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 332, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 333, 3))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 334, 3))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 335, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 336, 3))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 337, 3))
    counters.add(cc_18)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'senderId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 299, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 300, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageGroup')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 305, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 306, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 307, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 308, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'action')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 309, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 310, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'recipientId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 311, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'originalSenderId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 312, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'declarationLocalReference')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 313, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 314, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessTransaction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 315, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 316, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 317, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subMessageType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 318, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'partialDelivery')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 319, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subjects')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 328, 3))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'object')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 329, 3))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comments')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 330, 3))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 331, 3))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 332, 3))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventPeriod')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 333, 3))
    st_22 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'modificationDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 334, 3))
    st_23 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_23)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'testData')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 335, 3))
    st_24 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_24)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'reference')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 336, 3))
    st_25 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_25)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 337, 3))
    st_26 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_26)
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
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
    transitions.append(fac.Transition(st_22, [
         ]))
    transitions.append(fac.Transition(st_23, [
         ]))
    transitions.append(fac.Transition(st_24, [
         ]))
    transitions.append(fac.Transition(st_25, [
         ]))
    transitions.append(fac.Transition(st_26, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
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
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, True) ]))
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
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, True) ]))
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
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, True) ]))
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
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_21._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_22._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_15, False) ]))
    st_23._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_16, False) ]))
    st_24._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_25._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_18, True) ]))
    st_26._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
headerType._Automaton = _BuildAutomaton_7()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessCase'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.uniqueIdBusinessCaseType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 322, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'totalNumberOfPackages'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.totalNumberOfPackagesType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 323, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'numberOfActualPackage'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.numberOfActualPackageType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 324, 6)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessCase')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 322, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'totalNumberOfPackages')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 323, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'numberOfActualPackage')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 324, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_8()




keywordsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'keyword'), keywordType, scope=keywordsType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 355, 3)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(keywordsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'keyword')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 355, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
keywordsType._Automaton = _BuildAutomaton_9()




linksType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'link'), linkType, scope=linksType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 373, 3)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(linksType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'link')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 373, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
linksType._Automaton = _BuildAutomaton_10()




messageGroupType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageGroupId'), pyxb.binding.datatypes.nonNegativeInteger, scope=messageGroupType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 381, 3)))

messageGroupType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageTypeId'), pyxb.binding.datatypes.nonNegativeInteger, scope=messageGroupType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 382, 3)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(messageGroupType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageGroupId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 381, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(messageGroupType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageTypeId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 382, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
messageGroupType._Automaton = _BuildAutomaton_11()




referenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.token, scope=referenceType, documentation='UUID: Universally Unique Identifier der Referenz. ', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 410, 3)))

referenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'serviceInventoryId'), pyxb.binding.datatypes.token, scope=referenceType, documentation='Leistungsinventar: Identifikationsnummer des referenzierten Leistungsinventars (gemäss eCH-0070 Leistungsinventar eGov CH) Leistungen sind immer eindeutig entweder einem lokalen, re¬gionalen oder globalen Inventar zugeordnet.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 415, 3)))

referenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'serviceId'), pyxb.binding.datatypes.token, scope=referenceType, documentation='Identifikationsnummer: Eindeutige Identifikationsnummer einer Leistung (gemäss eCH-0070 Leistungsinventar eGov CH).', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 420, 3)))

referenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'serviceTitle'), pyxb.binding.datatypes.token, scope=referenceType, documentation='Titel: Bezeichnung der Leistung (gemäss eCH-0070 Leistungsinventar eGov CH).', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 425, 3)))

referenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'serviceProvider'), pyxb.binding.datatypes.token, scope=referenceType, documentation='Leistungserbringer: Identifikation des Leistungserbringers (federführende Behörde oder Stelle) gemäss Schweizerischem Behördenverzeichnis.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 430, 3)))

referenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'caseId'), pyxb.binding.datatypes.token, scope=referenceType, documentation='Geschäftsfall: Identifikation des Geschäftsfalls (wird von der federführenden Stelle vergeben).', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 435, 3)))

referenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'caseTitle'), pyxb.binding.datatypes.token, scope=referenceType, documentation='Titel: Benennung des Geschäftsvorfalls.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 440, 3)))

referenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'caseAnnotation'), pyxb.binding.datatypes.token, scope=referenceType, documentation='Bemerkung: Informationen zum Geschäftsvorfall.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 445, 3)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 415, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 420, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 425, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 430, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 435, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 440, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 445, 3))
    counters.add(cc_6)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(referenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 410, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(referenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'serviceInventoryId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 415, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(referenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'serviceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 420, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(referenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'serviceTitle')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 425, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(referenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'serviceProvider')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 430, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(referenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'caseId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 435, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(referenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'caseTitle')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 440, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(referenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'caseAnnotation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 445, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
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
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
referenceType._Automaton = _BuildAutomaton_12()




reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'senderId'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.participantIdType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 467, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageId'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.messageIdType, scope=reportHeaderType, documentation='Nachrichten-ID: Empfehlung des Einsatzes von UUID für die eindeutige Referenz von übermittelten Nachrichten.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 468, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageGroup'), messageGroupType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 473, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageType'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.messageTypeType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 474, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.sendingApplicationType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 475, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'action'), reportActionType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 476, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.testDeliveryFlagType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 477, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'recipientId'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.participantIdType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 478, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.messageIdType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 479, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.businessReferenceIdType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 480, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.businessReferenceIdType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 481, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessTransaction'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.uniqueIdBusinessTransactionType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 482, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subMessageType'), _ImportedBinding_camac_echbern_schema_ech_0058_3_0.subMessageTypeType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 483, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'object'), pyxb.binding.datatypes.anyType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 484, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate'), pyxb.binding.datatypes.dateTime, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 485, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'testData'), pyxb.binding.datatypes.anyType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 486, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reference'), referenceType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 487, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 488, 3)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 478, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 479, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 480, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 481, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 482, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 483, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 484, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 485, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 486, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 487, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 488, 3))
    counters.add(cc_10)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'senderId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 467, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 468, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageGroup')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 473, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 474, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 475, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'action')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 476, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 477, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'recipientId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 478, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 479, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 480, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 481, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessTransaction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 482, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subMessageType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 483, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'object')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 484, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 485, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'testData')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 486, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'reference')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 487, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 488, 3))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
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
    transitions.append(fac.Transition(st_17, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
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
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, True) ]))
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
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, True) ]))
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
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, True) ]))
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
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, True) ]))
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
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_10, True) ]))
    st_17._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
reportHeaderType._Automaton = _BuildAutomaton_13()




reportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'positiveReport'), pyxb.binding.datatypes.anyType, scope=reportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 496, 3)))

reportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'negativeReport'), pyxb.binding.datatypes.anyType, scope=reportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 497, 3)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 495, 2))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 496, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 497, 3))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(reportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'positiveReport')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 496, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(reportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'negativeReport')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 497, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
reportType._Automaton = _BuildAutomaton_14()




subjectsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subject'), subjectType, scope=subjectsType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 515, 3)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(subjectsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subject')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 515, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
subjectsType._Automaton = _BuildAutomaton_15()




titlesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'title'), titleType, scope=titlesType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 533, 3)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(titlesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'title')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0039_2_0.xsd', 533, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
titlesType._Automaton = _BuildAutomaton_16()

