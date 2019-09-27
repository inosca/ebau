# ../../camac/echbern/schema/ech_0058_3_0.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:45a7005dbe5a596a2055c11cc5fb6e0ab60cb294
# Generated 2019-09-26 17:57:08.874060 by PyXB version 1.2.6 using Python 3.6.8.final.0
# Namespace http://www.ech.ch/xmlns/eCH-0058/3 [xmlns:eCH-0058]

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

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.ech.ch/xmlns/eCH-0058/3', create_if_missing=True)
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


# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 36, 4)
    _Documentation = None
STD_ANON._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(2))
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.n1 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='1', tag='n1')
STD_ANON.n3 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='3', tag='n3')
STD_ANON.n4 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='4', tag='n4')
STD_ANON.n5 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='5', tag='n5')
STD_ANON.n6 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='6', tag='n6')
STD_ANON.n7 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='7', tag='n7')
STD_ANON.n10 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='10', tag='n10')
STD_ANON.n12 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='12', tag='n12')
STD_ANON._InitializeFacetMap(STD_ANON._CF_maxLength,
   STD_ANON._CF_enumeration)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 71, 4)
    _Documentation = None
STD_ANON_._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(2))
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.n8 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='8', tag='n8')
STD_ANON_.n9 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='9', tag='n9')
STD_ANON_.n11 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='11', tag='n11')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_maxLength,
   STD_ANON_._CF_enumeration)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}messageIdType
class messageIdType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'messageIdType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 85, 1)
    _Documentation = None
messageIdType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'messageIdType', messageIdType)
_module_typeBindings.messageIdType = messageIdType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}subMessageTypeType
class subMessageTypeType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'subMessageTypeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 88, 1)
    _Documentation = None
subMessageTypeType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'subMessageTypeType', subMessageTypeType)
_module_typeBindings.subMessageTypeType = subMessageTypeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}messageTypeType
class messageTypeType (pyxb.binding.datatypes.int):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'messageTypeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 91, 1)
    _Documentation = None
messageTypeType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=messageTypeType, value=pyxb.binding.datatypes.int(0))
messageTypeType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=messageTypeType, value=pyxb.binding.datatypes.int(2699999))
messageTypeType._InitializeFacetMap(messageTypeType._CF_minInclusive,
   messageTypeType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'messageTypeType', messageTypeType)
_module_typeBindings.messageTypeType = messageTypeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}declarationLocalReferenceType
class declarationLocalReferenceType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'declarationLocalReferenceType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 97, 1)
    _Documentation = None
declarationLocalReferenceType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'declarationLocalReferenceType', declarationLocalReferenceType)
_module_typeBindings.declarationLocalReferenceType = declarationLocalReferenceType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}participantIdType
class participantIdType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'participantIdType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 100, 1)
    _Documentation = None
participantIdType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'participantIdType', participantIdType)
_module_typeBindings.participantIdType = participantIdType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}businessReferenceIdType
class businessReferenceIdType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'businessReferenceIdType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 103, 1)
    _Documentation = None
businessReferenceIdType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(50))
businessReferenceIdType._InitializeFacetMap(businessReferenceIdType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'businessReferenceIdType', businessReferenceIdType)
_module_typeBindings.businessReferenceIdType = businessReferenceIdType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}subjectType
class subjectType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'subjectType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 108, 1)
    _Documentation = None
subjectType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
subjectType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
subjectType._InitializeFacetMap(subjectType._CF_minLength,
   subjectType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'subjectType', subjectType)
_module_typeBindings.subjectType = subjectType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}commentType
class commentType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'commentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 114, 1)
    _Documentation = None
commentType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
commentType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(250))
commentType._InitializeFacetMap(commentType._CF_minLength,
   commentType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'commentType', commentType)
_module_typeBindings.commentType = commentType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}uniqueIdBusinessCaseType
class uniqueIdBusinessCaseType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessCaseType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 120, 1)
    _Documentation = None
uniqueIdBusinessCaseType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
uniqueIdBusinessCaseType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(50))
uniqueIdBusinessCaseType._InitializeFacetMap(uniqueIdBusinessCaseType._CF_minLength,
   uniqueIdBusinessCaseType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'uniqueIdBusinessCaseType', uniqueIdBusinessCaseType)
_module_typeBindings.uniqueIdBusinessCaseType = uniqueIdBusinessCaseType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}uniqueIdBusinessTransactionType
class uniqueIdBusinessTransactionType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessTransactionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 126, 1)
    _Documentation = None
uniqueIdBusinessTransactionType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
uniqueIdBusinessTransactionType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(50))
uniqueIdBusinessTransactionType._InitializeFacetMap(uniqueIdBusinessTransactionType._CF_minLength,
   uniqueIdBusinessTransactionType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'uniqueIdBusinessTransactionType', uniqueIdBusinessTransactionType)
_module_typeBindings.uniqueIdBusinessTransactionType = uniqueIdBusinessTransactionType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}totalNumberOfPackagesType
class totalNumberOfPackagesType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'totalNumberOfPackagesType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 132, 1)
    _Documentation = None
totalNumberOfPackagesType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'totalNumberOfPackagesType', totalNumberOfPackagesType)
_module_typeBindings.totalNumberOfPackagesType = totalNumberOfPackagesType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}numberOfActualPackageType
class numberOfActualPackageType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'numberOfActualPackageType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 135, 1)
    _Documentation = None
numberOfActualPackageType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'numberOfActualPackageType', numberOfActualPackageType)
_module_typeBindings.numberOfActualPackageType = numberOfActualPackageType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}testDeliveryFlagType
class testDeliveryFlagType (pyxb.binding.datatypes.boolean):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlagType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 138, 1)
    _Documentation = None
testDeliveryFlagType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'testDeliveryFlagType', testDeliveryFlagType)
_module_typeBindings.testDeliveryFlagType = testDeliveryFlagType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0058/3}initialMessageDateType
class initialMessageDateType (pyxb.binding.datatypes.dateTime):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'initialMessageDateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 141, 1)
    _Documentation = None
initialMessageDateType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'initialMessageDateType', initialMessageDateType)
_module_typeBindings.initialMessageDateType = initialMessageDateType

# Atomic simple type: [anonymous]
class STD_ANON_2 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 147, 4)
    _Documentation = None
STD_ANON_2._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(30))
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_maxLength)
_module_typeBindings.STD_ANON_2 = STD_ANON_2

# Atomic simple type: [anonymous]
class STD_ANON_3 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 154, 4)
    _Documentation = None
STD_ANON_3._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(30))
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_maxLength)
_module_typeBindings.STD_ANON_3 = STD_ANON_3

# Atomic simple type: [anonymous]
class STD_ANON_4 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 161, 4)
    _Documentation = None
STD_ANON_4._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(10))
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_maxLength)
_module_typeBindings.STD_ANON_4 = STD_ANON_4

# Complex type {http://www.ech.ch/xmlns/eCH-0058/3}headerType with content type ELEMENT_ONLY
class headerType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0058/3}headerType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'headerType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 5, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}senderId uses Python identifier senderId
    __senderId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'senderId'), 'senderId', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583senderId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 7, 3), )

    
    senderId = property(__senderId.value, __senderId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}originalSenderId uses Python identifier originalSenderId
    __originalSenderId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'originalSenderId'), 'originalSenderId', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583originalSenderId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 8, 3), )

    
    originalSenderId = property(__originalSenderId.value, __originalSenderId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}declarationLocalReference uses Python identifier declarationLocalReference
    __declarationLocalReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'declarationLocalReference'), 'declarationLocalReference', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583declarationLocalReference', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 9, 3), )

    
    declarationLocalReference = property(__declarationLocalReference.value, __declarationLocalReference.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}recipientId uses Python identifier recipientId
    __recipientId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'recipientId'), 'recipientId', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583recipientId', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 10, 3), )

    
    recipientId = property(__recipientId.value, __recipientId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}messageId uses Python identifier messageId
    __messageId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageId'), 'messageId', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583messageId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 11, 3), )

    
    messageId = property(__messageId.value, __messageId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}referenceMessageId uses Python identifier referenceMessageId
    __referenceMessageId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId'), 'referenceMessageId', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583referenceMessageId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 12, 3), )

    
    referenceMessageId = property(__referenceMessageId.value, __referenceMessageId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}ourBusinessReferenceId uses Python identifier ourBusinessReferenceId
    __ourBusinessReferenceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId'), 'ourBusinessReferenceId', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583ourBusinessReferenceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 13, 3), )

    
    ourBusinessReferenceId = property(__ourBusinessReferenceId.value, __ourBusinessReferenceId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}yourBusinessReferenceId uses Python identifier yourBusinessReferenceId
    __yourBusinessReferenceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId'), 'yourBusinessReferenceId', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583yourBusinessReferenceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 14, 3), )

    
    yourBusinessReferenceId = property(__yourBusinessReferenceId.value, __yourBusinessReferenceId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}uniqueIdBusinessTransaction uses Python identifier uniqueIdBusinessTransaction
    __uniqueIdBusinessTransaction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessTransaction'), 'uniqueIdBusinessTransaction', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583uniqueIdBusinessTransaction', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 15, 3), )

    
    uniqueIdBusinessTransaction = property(__uniqueIdBusinessTransaction.value, __uniqueIdBusinessTransaction.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}messageType uses Python identifier messageType
    __messageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageType'), 'messageType', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583messageType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 16, 3), )

    
    messageType = property(__messageType.value, __messageType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}subMessageType uses Python identifier subMessageType
    __subMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subMessageType'), 'subMessageType', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583subMessageType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 17, 3), )

    
    subMessageType = property(__subMessageType.value, __subMessageType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}sendingApplication uses Python identifier sendingApplication
    __sendingApplication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication'), 'sendingApplication', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583sendingApplication', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 18, 3), )

    
    sendingApplication = property(__sendingApplication.value, __sendingApplication.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}partialDelivery uses Python identifier partialDelivery
    __partialDelivery = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'partialDelivery'), 'partialDelivery', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583partialDelivery', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 19, 3), )

    
    partialDelivery = property(__partialDelivery.value, __partialDelivery.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subject'), 'subject', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583subject', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 28, 3), )

    
    subject = property(__subject.value, __subject.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}object uses Python identifier object
    __object = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'object'), 'object', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583object', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 29, 3), )

    
    object = property(__object.value, __object.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}comment uses Python identifier comment
    __comment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comment'), 'comment', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583comment', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 30, 3), )

    
    comment = property(__comment.value, __comment.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}messageDate uses Python identifier messageDate
    __messageDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageDate'), 'messageDate', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583messageDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 31, 3), )

    
    messageDate = property(__messageDate.value, __messageDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}initialMessageDate uses Python identifier initialMessageDate
    __initialMessageDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate'), 'initialMessageDate', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583initialMessageDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 32, 3), )

    
    initialMessageDate = property(__initialMessageDate.value, __initialMessageDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}eventDate uses Python identifier eventDate
    __eventDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventDate'), 'eventDate', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583eventDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 33, 3), )

    
    eventDate = property(__eventDate.value, __eventDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}modificationDate uses Python identifier modificationDate
    __modificationDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'modificationDate'), 'modificationDate', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583modificationDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 34, 3), )

    
    modificationDate = property(__modificationDate.value, __modificationDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}action uses Python identifier action
    __action = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'action'), 'action', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583action', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 35, 3), )

    
    action = property(__action.value, __action.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}attachment uses Python identifier attachment
    __attachment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'attachment'), 'attachment', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583attachment', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 50, 3), )

    
    attachment = property(__attachment.value, __attachment.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}testDeliveryFlag uses Python identifier testDeliveryFlag
    __testDeliveryFlag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag'), 'testDeliveryFlag', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583testDeliveryFlag', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 51, 3), )

    
    testDeliveryFlag = property(__testDeliveryFlag.value, __testDeliveryFlag.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}testData uses Python identifier testData
    __testData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'testData'), 'testData', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583testData', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 52, 3), )

    
    testData = property(__testData.value, __testData.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_00583_headerType_httpwww_ech_chxmlnseCH_00583extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 53, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __senderId.name() : __senderId,
        __originalSenderId.name() : __originalSenderId,
        __declarationLocalReference.name() : __declarationLocalReference,
        __recipientId.name() : __recipientId,
        __messageId.name() : __messageId,
        __referenceMessageId.name() : __referenceMessageId,
        __ourBusinessReferenceId.name() : __ourBusinessReferenceId,
        __yourBusinessReferenceId.name() : __yourBusinessReferenceId,
        __uniqueIdBusinessTransaction.name() : __uniqueIdBusinessTransaction,
        __messageType.name() : __messageType,
        __subMessageType.name() : __subMessageType,
        __sendingApplication.name() : __sendingApplication,
        __partialDelivery.name() : __partialDelivery,
        __subject.name() : __subject,
        __object.name() : __object,
        __comment.name() : __comment,
        __messageDate.name() : __messageDate,
        __initialMessageDate.name() : __initialMessageDate,
        __eventDate.name() : __eventDate,
        __modificationDate.name() : __modificationDate,
        __action.name() : __action,
        __attachment.name() : __attachment,
        __testDeliveryFlag.name() : __testDeliveryFlag,
        __testData.name() : __testData,
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
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 20, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}uniqueIdBusinessCase uses Python identifier uniqueIdBusinessCase
    __uniqueIdBusinessCase = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessCase'), 'uniqueIdBusinessCase', '__httpwww_ech_chxmlnseCH_00583_CTD_ANON_httpwww_ech_chxmlnseCH_00583uniqueIdBusinessCase', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 22, 6), )

    
    uniqueIdBusinessCase = property(__uniqueIdBusinessCase.value, __uniqueIdBusinessCase.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}totalNumberOfPackages uses Python identifier totalNumberOfPackages
    __totalNumberOfPackages = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'totalNumberOfPackages'), 'totalNumberOfPackages', '__httpwww_ech_chxmlnseCH_00583_CTD_ANON_httpwww_ech_chxmlnseCH_00583totalNumberOfPackages', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 23, 6), )

    
    totalNumberOfPackages = property(__totalNumberOfPackages.value, __totalNumberOfPackages.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}numberOfActualPackage uses Python identifier numberOfActualPackage
    __numberOfActualPackage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'numberOfActualPackage'), 'numberOfActualPackage', '__httpwww_ech_chxmlnseCH_00583_CTD_ANON_httpwww_ech_chxmlnseCH_00583numberOfActualPackage', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 24, 6), )

    
    numberOfActualPackage = property(__numberOfActualPackage.value, __numberOfActualPackage.set, None, None)

    _ElementMap.update({
        __uniqueIdBusinessCase.name() : __uniqueIdBusinessCase,
        __totalNumberOfPackages.name() : __totalNumberOfPackages,
        __numberOfActualPackage.name() : __numberOfActualPackage
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.ech.ch/xmlns/eCH-0058/3}reportHeaderType with content type ELEMENT_ONLY
class reportHeaderType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0058/3}reportHeaderType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'reportHeaderType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 56, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}senderId uses Python identifier senderId
    __senderId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'senderId'), 'senderId', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583senderId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 58, 3), )

    
    senderId = property(__senderId.value, __senderId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}recipientId uses Python identifier recipientId
    __recipientId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'recipientId'), 'recipientId', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583recipientId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 59, 3), )

    
    recipientId = property(__recipientId.value, __recipientId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}messageId uses Python identifier messageId
    __messageId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageId'), 'messageId', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583messageId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 60, 3), )

    
    messageId = property(__messageId.value, __messageId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}referenceMessageId uses Python identifier referenceMessageId
    __referenceMessageId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId'), 'referenceMessageId', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583referenceMessageId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 61, 3), )

    
    referenceMessageId = property(__referenceMessageId.value, __referenceMessageId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}ourBusinessReferenceId uses Python identifier ourBusinessReferenceId
    __ourBusinessReferenceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId'), 'ourBusinessReferenceId', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583ourBusinessReferenceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 62, 3), )

    
    ourBusinessReferenceId = property(__ourBusinessReferenceId.value, __ourBusinessReferenceId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}yourBusinessReferenceId uses Python identifier yourBusinessReferenceId
    __yourBusinessReferenceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId'), 'yourBusinessReferenceId', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583yourBusinessReferenceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 63, 3), )

    
    yourBusinessReferenceId = property(__yourBusinessReferenceId.value, __yourBusinessReferenceId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}uniqueIdBusinessTransaction uses Python identifier uniqueIdBusinessTransaction
    __uniqueIdBusinessTransaction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessTransaction'), 'uniqueIdBusinessTransaction', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583uniqueIdBusinessTransaction', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 64, 3), )

    
    uniqueIdBusinessTransaction = property(__uniqueIdBusinessTransaction.value, __uniqueIdBusinessTransaction.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}messageType uses Python identifier messageType
    __messageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageType'), 'messageType', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583messageType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 65, 3), )

    
    messageType = property(__messageType.value, __messageType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}subMessageType uses Python identifier subMessageType
    __subMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subMessageType'), 'subMessageType', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583subMessageType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 66, 3), )

    
    subMessageType = property(__subMessageType.value, __subMessageType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}sendingApplication uses Python identifier sendingApplication
    __sendingApplication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication'), 'sendingApplication', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583sendingApplication', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 67, 3), )

    
    sendingApplication = property(__sendingApplication.value, __sendingApplication.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}object uses Python identifier object
    __object = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'object'), 'object', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583object', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 68, 3), )

    
    object = property(__object.value, __object.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}initialMessageDate uses Python identifier initialMessageDate
    __initialMessageDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate'), 'initialMessageDate', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583initialMessageDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 69, 3), )

    
    initialMessageDate = property(__initialMessageDate.value, __initialMessageDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}action uses Python identifier action
    __action = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'action'), 'action', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583action', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 70, 3), )

    
    action = property(__action.value, __action.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}testDeliveryFlag uses Python identifier testDeliveryFlag
    __testDeliveryFlag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag'), 'testDeliveryFlag', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583testDeliveryFlag', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 80, 3), )

    
    testDeliveryFlag = property(__testDeliveryFlag.value, __testDeliveryFlag.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}testData uses Python identifier testData
    __testData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'testData'), 'testData', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583testData', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 81, 3), )

    
    testData = property(__testData.value, __testData.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_00583_reportHeaderType_httpwww_ech_chxmlnseCH_00583extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 82, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __senderId.name() : __senderId,
        __recipientId.name() : __recipientId,
        __messageId.name() : __messageId,
        __referenceMessageId.name() : __referenceMessageId,
        __ourBusinessReferenceId.name() : __ourBusinessReferenceId,
        __yourBusinessReferenceId.name() : __yourBusinessReferenceId,
        __uniqueIdBusinessTransaction.name() : __uniqueIdBusinessTransaction,
        __messageType.name() : __messageType,
        __subMessageType.name() : __subMessageType,
        __sendingApplication.name() : __sendingApplication,
        __object.name() : __object,
        __initialMessageDate.name() : __initialMessageDate,
        __action.name() : __action,
        __testDeliveryFlag.name() : __testDeliveryFlag,
        __testData.name() : __testData,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.reportHeaderType = reportHeaderType
Namespace.addCategoryObject('typeBinding', 'reportHeaderType', reportHeaderType)


# Complex type {http://www.ech.ch/xmlns/eCH-0058/3}sendingApplicationType with content type ELEMENT_ONLY
class sendingApplicationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0058/3}sendingApplicationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'sendingApplicationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 144, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}manufacturer uses Python identifier manufacturer
    __manufacturer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'manufacturer'), 'manufacturer', '__httpwww_ech_chxmlnseCH_00583_sendingApplicationType_httpwww_ech_chxmlnseCH_00583manufacturer', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 146, 3), )

    
    manufacturer = property(__manufacturer.value, __manufacturer.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}product uses Python identifier product
    __product = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'product'), 'product', '__httpwww_ech_chxmlnseCH_00583_sendingApplicationType_httpwww_ech_chxmlnseCH_00583product', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 153, 3), )

    
    product = property(__product.value, __product.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}productVersion uses Python identifier productVersion
    __productVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'productVersion'), 'productVersion', '__httpwww_ech_chxmlnseCH_00583_sendingApplicationType_httpwww_ech_chxmlnseCH_00583productVersion', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 160, 3), )

    
    productVersion = property(__productVersion.value, __productVersion.set, None, None)

    _ElementMap.update({
        __manufacturer.name() : __manufacturer,
        __product.name() : __product,
        __productVersion.name() : __productVersion
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.sendingApplicationType = sendingApplicationType
Namespace.addCategoryObject('typeBinding', 'sendingApplicationType', sendingApplicationType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 170, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}reportHeader uses Python identifier reportHeader
    __reportHeader = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'reportHeader'), 'reportHeader', '__httpwww_ech_chxmlnseCH_00583_CTD_ANON__httpwww_ech_chxmlnseCH_00583reportHeader', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 172, 4), )

    
    reportHeader = property(__reportHeader.value, __reportHeader.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}report uses Python identifier report
    __report = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'report'), 'report', '__httpwww_ech_chxmlnseCH_00583_CTD_ANON__httpwww_ech_chxmlnseCH_00583report', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 173, 4), )

    
    report = property(__report.value, __report.set, None, None)

    _ElementMap.update({
        __reportHeader.name() : __reportHeader,
        __report.name() : __report
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type {http://www.ech.ch/xmlns/eCH-0058/3}reportType with content type ELEMENT_ONLY
class reportType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0058/3}reportType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'reportType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 177, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}positiveReport uses Python identifier positiveReport
    __positiveReport = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'positiveReport'), 'positiveReport', '__httpwww_ech_chxmlnseCH_00583_reportType_httpwww_ech_chxmlnseCH_00583positiveReport', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 179, 3), )

    
    positiveReport = property(__positiveReport.value, __positiveReport.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0058/3}negativeReport uses Python identifier negativeReport
    __negativeReport = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'negativeReport'), 'negativeReport', '__httpwww_ech_chxmlnseCH_00583_reportType_httpwww_ech_chxmlnseCH_00583negativeReport', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 180, 3), )

    
    negativeReport = property(__negativeReport.value, __negativeReport.set, None, None)

    _ElementMap.update({
        __positiveReport.name() : __positiveReport,
        __negativeReport.name() : __negativeReport
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.reportType = reportType
Namespace.addCategoryObject('typeBinding', 'reportType', reportType)


eventReport = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventReport'), CTD_ANON_, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 169, 1))
Namespace.addCategoryObject('elementBinding', eventReport.name().localName(), eventReport)



headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'senderId'), participantIdType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 7, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'originalSenderId'), participantIdType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 8, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'declarationLocalReference'), declarationLocalReferenceType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 9, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'recipientId'), participantIdType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 10, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageId'), messageIdType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 11, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId'), messageIdType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 12, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId'), businessReferenceIdType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 13, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId'), businessReferenceIdType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 14, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessTransaction'), uniqueIdBusinessTransactionType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 15, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageType'), messageTypeType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 16, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subMessageType'), subMessageTypeType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 17, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication'), sendingApplicationType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 18, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'partialDelivery'), CTD_ANON, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 19, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subject'), subjectType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 28, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'object'), pyxb.binding.datatypes.anyType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 29, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comment'), commentType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 30, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageDate'), pyxb.binding.datatypes.dateTime, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 31, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate'), initialMessageDateType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 32, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventDate'), pyxb.binding.datatypes.dateTime, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 33, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'modificationDate'), pyxb.binding.datatypes.dateTime, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 34, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'action'), STD_ANON, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 35, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'attachment'), pyxb.binding.datatypes.anyType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 50, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag'), testDeliveryFlagType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 51, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'testData'), pyxb.binding.datatypes.anyType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 52, 3)))

headerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=headerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 53, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 8, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 9, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 10, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 12, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 13, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 14, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 15, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 17, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 19, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 28, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 29, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 30, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 32, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 34, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 50, 3))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 52, 3))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 53, 3))
    counters.add(cc_16)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'senderId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 7, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'originalSenderId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 8, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'declarationLocalReference')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 9, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'recipientId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 10, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 11, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 12, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 13, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 14, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessTransaction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 15, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 16, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subMessageType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 17, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 18, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'partialDelivery')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 19, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subject')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 28, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'object')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 29, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comment')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 30, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 31, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 32, 3))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 33, 3))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'modificationDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 34, 3))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'action')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 35, 3))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'attachment')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 50, 3))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 51, 3))
    st_22 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'testData')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 52, 3))
    st_23 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_23)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(headerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 53, 3))
    st_24 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_24)
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
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
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
    transitions.append(fac.Transition(st_17, [
         ]))
    transitions.append(fac.Transition(st_18, [
         ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
         ]))
    transitions.append(fac.Transition(st_20, [
         ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
         ]))
    transitions.append(fac.Transition(st_22, [
         ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_21._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
         ]))
    transitions.append(fac.Transition(st_24, [
         ]))
    st_22._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_15, False) ]))
    st_23._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_16, True) ]))
    st_24._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
headerType._Automaton = _BuildAutomaton()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessCase'), uniqueIdBusinessCaseType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 22, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'totalNumberOfPackages'), totalNumberOfPackagesType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 23, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'numberOfActualPackage'), numberOfActualPackageType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 24, 6)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessCase')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 22, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'totalNumberOfPackages')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 23, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'numberOfActualPackage')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 24, 6))
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
CTD_ANON._Automaton = _BuildAutomaton_()




reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'senderId'), participantIdType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 58, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'recipientId'), participantIdType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 59, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageId'), messageIdType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 60, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId'), messageIdType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 61, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId'), businessReferenceIdType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 62, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId'), businessReferenceIdType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 63, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessTransaction'), uniqueIdBusinessTransactionType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 64, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageType'), messageTypeType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 65, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subMessageType'), subMessageTypeType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 66, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication'), sendingApplicationType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 67, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'object'), pyxb.binding.datatypes.anyType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 68, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate'), initialMessageDateType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 69, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'action'), STD_ANON_, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 70, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag'), testDeliveryFlagType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 80, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'testData'), pyxb.binding.datatypes.anyType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 81, 3)))

reportHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=reportHeaderType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 82, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 59, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 61, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 62, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 63, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 64, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 66, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 68, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 69, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 81, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 82, 3))
    counters.add(cc_9)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'senderId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 58, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'recipientId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 59, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 60, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'referenceMessageId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 61, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ourBusinessReferenceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 62, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yourBusinessReferenceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 63, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uniqueIdBusinessTransaction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 64, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 65, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subMessageType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 66, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sendingApplication')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 67, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'object')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 68, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'initialMessageDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 69, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'action')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 70, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'testDeliveryFlag')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 80, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'testData')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 81, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(reportHeaderType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 82, 3))
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
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
         ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, True) ]))
    st_15._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
reportHeaderType._Automaton = _BuildAutomaton_2()




sendingApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'manufacturer'), STD_ANON_2, scope=sendingApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 146, 3)))

sendingApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'product'), STD_ANON_3, scope=sendingApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 153, 3)))

sendingApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'productVersion'), STD_ANON_4, scope=sendingApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 160, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(sendingApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'manufacturer')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 146, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(sendingApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'product')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 153, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(sendingApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'productVersion')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 160, 3))
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
sendingApplicationType._Automaton = _BuildAutomaton_3()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reportHeader'), reportHeaderType, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 172, 4)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'report'), reportType, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 173, 4)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'reportHeader')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 172, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'report')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 173, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_4()




reportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'positiveReport'), pyxb.binding.datatypes.anyType, scope=reportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 179, 3)))

reportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'negativeReport'), pyxb.binding.datatypes.anyType, scope=reportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 180, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(reportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'positiveReport')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 179, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(reportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'negativeReport')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0058_3_0.xsd', 180, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
reportType._Automaton = _BuildAutomaton_5()

