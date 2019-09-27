# ../../camac/echbern/schema/ech_0044_1_0.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:74f799d93497653c948719b2a3ec36bcf58150b6
# Generated 2019-09-26 17:57:08.874731 by PyXB version 1.2.6 using Python 3.6.8.final.0
# Namespace http://www.ech.ch/xmlns/eCH-0044/1 [xmlns:eCH-0044]

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
Namespace = pyxb.namespace.NamespaceForURI('http://www.ech.ch/xmlns/eCH-0044/1', create_if_missing=True)
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


# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0044/1}personIdCategoryType
class personIdCategoryType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'personIdCategoryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 5, 1)
    _Documentation = None
personIdCategoryType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
personIdCategoryType._InitializeFacetMap(personIdCategoryType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'personIdCategoryType', personIdCategoryType)
_module_typeBindings.personIdCategoryType = personIdCategoryType

# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 14, 4)
    _Documentation = None
STD_ANON._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
STD_ANON._InitializeFacetMap(STD_ANON._CF_maxLength)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0044/1}baseNameType
class baseNameType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'baseNameType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 64, 1)
    _Documentation = None
baseNameType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
baseNameType._InitializeFacetMap(baseNameType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'baseNameType', baseNameType)
_module_typeBindings.baseNameType = baseNameType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0044/1}officialFirstNameType
class officialFirstNameType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'officialFirstNameType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 69, 1)
    _Documentation = None
officialFirstNameType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(50))
officialFirstNameType._CF_whiteSpace = pyxb.binding.facets.CF_whiteSpace(value=pyxb.binding.facets._WhiteSpace_enum.collapse)
officialFirstNameType._InitializeFacetMap(officialFirstNameType._CF_maxLength,
   officialFirstNameType._CF_whiteSpace)
Namespace.addCategoryObject('typeBinding', 'officialFirstNameType', officialFirstNameType)
_module_typeBindings.officialFirstNameType = officialFirstNameType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0044/1}sexType
class sexType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'sexType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 75, 1)
    _Documentation = None
sexType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=sexType, enum_prefix=None)
sexType.n1 = sexType._CF_enumeration.addEnumeration(unicode_value='1', tag='n1')
sexType.n2 = sexType._CF_enumeration.addEnumeration(unicode_value='2', tag='n2')
sexType._InitializeFacetMap(sexType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'sexType', sexType)
_module_typeBindings.sexType = sexType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0044/1}vnType
class vnType (pyxb.binding.datatypes.unsignedLong):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'vnType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 81, 1)
    _Documentation = None
vnType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=vnType, value=pyxb.binding.datatypes.unsignedLong(7560000000001))
vnType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=vnType, value=pyxb.binding.datatypes.unsignedLong(7569999999999))
vnType._InitializeFacetMap(vnType._CF_minInclusive,
   vnType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'vnType', vnType)
_module_typeBindings.vnType = vnType

# Complex type {http://www.ech.ch/xmlns/eCH-0044/1}namedPersonIdType with content type ELEMENT_ONLY
class namedPersonIdType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0044/1}namedPersonIdType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'namedPersonIdType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 10, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}personIdCategory uses Python identifier personIdCategory
    __personIdCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'personIdCategory'), 'personIdCategory', '__httpwww_ech_chxmlnseCH_00441_namedPersonIdType_httpwww_ech_chxmlnseCH_00441personIdCategory', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 12, 3), )

    
    personIdCategory = property(__personIdCategory.value, __personIdCategory.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}personId uses Python identifier personId
    __personId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'personId'), 'personId', '__httpwww_ech_chxmlnseCH_00441_namedPersonIdType_httpwww_ech_chxmlnseCH_00441personId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 13, 3), )

    
    personId = property(__personId.value, __personId.set, None, None)

    _ElementMap.update({
        __personIdCategory.name() : __personIdCategory,
        __personId.name() : __personId
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.namedPersonIdType = namedPersonIdType
Namespace.addCategoryObject('typeBinding', 'namedPersonIdType', namedPersonIdType)


# Complex type {http://www.ech.ch/xmlns/eCH-0044/1}personIdentificationType with content type ELEMENT_ONLY
class personIdentificationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0044/1}personIdentificationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'personIdentificationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 22, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}vn uses Python identifier vn
    __vn = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'vn'), 'vn', '__httpwww_ech_chxmlnseCH_00441_personIdentificationType_httpwww_ech_chxmlnseCH_00441vn', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 24, 3), )

    
    vn = property(__vn.value, __vn.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}localPersonId uses Python identifier localPersonId
    __localPersonId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localPersonId'), 'localPersonId', '__httpwww_ech_chxmlnseCH_00441_personIdentificationType_httpwww_ech_chxmlnseCH_00441localPersonId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 25, 3), )

    
    localPersonId = property(__localPersonId.value, __localPersonId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}OtherPersonId uses Python identifier OtherPersonId
    __OtherPersonId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OtherPersonId'), 'OtherPersonId', '__httpwww_ech_chxmlnseCH_00441_personIdentificationType_httpwww_ech_chxmlnseCH_00441OtherPersonId', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 26, 3), )

    
    OtherPersonId = property(__OtherPersonId.value, __OtherPersonId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}EuPersonId uses Python identifier EuPersonId
    __EuPersonId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EuPersonId'), 'EuPersonId', '__httpwww_ech_chxmlnseCH_00441_personIdentificationType_httpwww_ech_chxmlnseCH_00441EuPersonId', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 33, 3), )

    
    EuPersonId = property(__EuPersonId.value, __EuPersonId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}officialName uses Python identifier officialName
    __officialName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'officialName'), 'officialName', '__httpwww_ech_chxmlnseCH_00441_personIdentificationType_httpwww_ech_chxmlnseCH_00441officialName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 34, 3), )

    
    officialName = property(__officialName.value, __officialName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}firstName uses Python identifier firstName
    __firstName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'firstName'), 'firstName', '__httpwww_ech_chxmlnseCH_00441_personIdentificationType_httpwww_ech_chxmlnseCH_00441firstName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 35, 3), )

    
    firstName = property(__firstName.value, __firstName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}sex uses Python identifier sex
    __sex = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sex'), 'sex', '__httpwww_ech_chxmlnseCH_00441_personIdentificationType_httpwww_ech_chxmlnseCH_00441sex', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 36, 3), )

    
    sex = property(__sex.value, __sex.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}dateOfBirth uses Python identifier dateOfBirth
    __dateOfBirth = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateOfBirth'), 'dateOfBirth', '__httpwww_ech_chxmlnseCH_00441_personIdentificationType_httpwww_ech_chxmlnseCH_00441dateOfBirth', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 37, 3), )

    
    dateOfBirth = property(__dateOfBirth.value, __dateOfBirth.set, None, None)

    _ElementMap.update({
        __vn.name() : __vn,
        __localPersonId.name() : __localPersonId,
        __OtherPersonId.name() : __OtherPersonId,
        __EuPersonId.name() : __EuPersonId,
        __officialName.name() : __officialName,
        __firstName.name() : __firstName,
        __sex.name() : __sex,
        __dateOfBirth.name() : __dateOfBirth
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.personIdentificationType = personIdentificationType
Namespace.addCategoryObject('typeBinding', 'personIdentificationType', personIdentificationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0044/1}personIdentificationPartnerType with content type ELEMENT_ONLY
class personIdentificationPartnerType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0044/1}personIdentificationPartnerType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'personIdentificationPartnerType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 40, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}vn uses Python identifier vn
    __vn = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'vn'), 'vn', '__httpwww_ech_chxmlnseCH_00441_personIdentificationPartnerType_httpwww_ech_chxmlnseCH_00441vn', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 42, 3), )

    
    vn = property(__vn.value, __vn.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}localPersonId uses Python identifier localPersonId
    __localPersonId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localPersonId'), 'localPersonId', '__httpwww_ech_chxmlnseCH_00441_personIdentificationPartnerType_httpwww_ech_chxmlnseCH_00441localPersonId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 43, 3), )

    
    localPersonId = property(__localPersonId.value, __localPersonId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}OtherPersonId uses Python identifier OtherPersonId
    __OtherPersonId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OtherPersonId'), 'OtherPersonId', '__httpwww_ech_chxmlnseCH_00441_personIdentificationPartnerType_httpwww_ech_chxmlnseCH_00441OtherPersonId', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 44, 3), )

    
    OtherPersonId = property(__OtherPersonId.value, __OtherPersonId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}officialName uses Python identifier officialName
    __officialName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'officialName'), 'officialName', '__httpwww_ech_chxmlnseCH_00441_personIdentificationPartnerType_httpwww_ech_chxmlnseCH_00441officialName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 51, 3), )

    
    officialName = property(__officialName.value, __officialName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}firstName uses Python identifier firstName
    __firstName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'firstName'), 'firstName', '__httpwww_ech_chxmlnseCH_00441_personIdentificationPartnerType_httpwww_ech_chxmlnseCH_00441firstName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 52, 3), )

    
    firstName = property(__firstName.value, __firstName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}sex uses Python identifier sex
    __sex = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sex'), 'sex', '__httpwww_ech_chxmlnseCH_00441_personIdentificationPartnerType_httpwww_ech_chxmlnseCH_00441sex', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 53, 3), )

    
    sex = property(__sex.value, __sex.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}dateOfBirth uses Python identifier dateOfBirth
    __dateOfBirth = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateOfBirth'), 'dateOfBirth', '__httpwww_ech_chxmlnseCH_00441_personIdentificationPartnerType_httpwww_ech_chxmlnseCH_00441dateOfBirth', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 54, 3), )

    
    dateOfBirth = property(__dateOfBirth.value, __dateOfBirth.set, None, None)

    _ElementMap.update({
        __vn.name() : __vn,
        __localPersonId.name() : __localPersonId,
        __OtherPersonId.name() : __OtherPersonId,
        __officialName.name() : __officialName,
        __firstName.name() : __firstName,
        __sex.name() : __sex,
        __dateOfBirth.name() : __dateOfBirth
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.personIdentificationPartnerType = personIdentificationPartnerType
Namespace.addCategoryObject('typeBinding', 'personIdentificationPartnerType', personIdentificationPartnerType)


# Complex type {http://www.ech.ch/xmlns/eCH-0044/1}datePartiallyKnownType with content type ELEMENT_ONLY
class datePartiallyKnownType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0044/1}datePartiallyKnownType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'datePartiallyKnownType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 57, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}yearMonthDay uses Python identifier yearMonthDay
    __yearMonthDay = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yearMonthDay'), 'yearMonthDay', '__httpwww_ech_chxmlnseCH_00441_datePartiallyKnownType_httpwww_ech_chxmlnseCH_00441yearMonthDay', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 59, 3), )

    
    yearMonthDay = property(__yearMonthDay.value, __yearMonthDay.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}yearMonth uses Python identifier yearMonth
    __yearMonth = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yearMonth'), 'yearMonth', '__httpwww_ech_chxmlnseCH_00441_datePartiallyKnownType_httpwww_ech_chxmlnseCH_00441yearMonth', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 60, 3), )

    
    yearMonth = property(__yearMonth.value, __yearMonth.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}year uses Python identifier year
    __year = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'year'), 'year', '__httpwww_ech_chxmlnseCH_00441_datePartiallyKnownType_httpwww_ech_chxmlnseCH_00441year', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 61, 3), )

    
    year = property(__year.value, __year.set, None, None)

    _ElementMap.update({
        __yearMonthDay.name() : __yearMonthDay,
        __yearMonth.name() : __yearMonth,
        __year.name() : __year
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.datePartiallyKnownType = datePartiallyKnownType
Namespace.addCategoryObject('typeBinding', 'datePartiallyKnownType', datePartiallyKnownType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 88, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0044/1}personIdentification uses Python identifier personIdentification
    __personIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'personIdentification'), 'personIdentification', '__httpwww_ech_chxmlnseCH_00441_CTD_ANON_httpwww_ech_chxmlnseCH_00441personIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 90, 4), )

    
    personIdentification = property(__personIdentification.value, __personIdentification.set, None, None)

    _ElementMap.update({
        __personIdentification.name() : __personIdentification
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (namedPersonIdType):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 27, 4)
    _ElementMap = namedPersonIdType._ElementMap.copy()
    _AttributeMap = namedPersonIdType._AttributeMap.copy()
    # Base type is namedPersonIdType
    
    # Element personIdCategory ({http://www.ech.ch/xmlns/eCH-0044/1}personIdCategory) inherited from {http://www.ech.ch/xmlns/eCH-0044/1}namedPersonIdType
    
    # Element personId ({http://www.ech.ch/xmlns/eCH-0044/1}personId) inherited from {http://www.ech.ch/xmlns/eCH-0044/1}namedPersonIdType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (namedPersonIdType):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 45, 4)
    _ElementMap = namedPersonIdType._ElementMap.copy()
    _AttributeMap = namedPersonIdType._AttributeMap.copy()
    # Base type is namedPersonIdType
    
    # Element personIdCategory ({http://www.ech.ch/xmlns/eCH-0044/1}personIdCategory) inherited from {http://www.ech.ch/xmlns/eCH-0044/1}namedPersonIdType
    
    # Element personId ({http://www.ech.ch/xmlns/eCH-0044/1}personId) inherited from {http://www.ech.ch/xmlns/eCH-0044/1}namedPersonIdType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


personIdentificationRoot = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personIdentificationRoot'), CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 87, 1))
Namespace.addCategoryObject('elementBinding', personIdentificationRoot.name().localName(), personIdentificationRoot)



namedPersonIdType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personIdCategory'), personIdCategoryType, scope=namedPersonIdType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 12, 3)))

namedPersonIdType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personId'), STD_ANON, scope=namedPersonIdType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 13, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(namedPersonIdType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personIdCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 12, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(namedPersonIdType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 13, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
namedPersonIdType._Automaton = _BuildAutomaton()




personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'vn'), vnType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 24, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localPersonId'), namedPersonIdType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 25, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OtherPersonId'), CTD_ANON_, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 26, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EuPersonId'), namedPersonIdType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 33, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'officialName'), baseNameType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 34, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'firstName'), baseNameType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 35, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sex'), sexType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 36, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateOfBirth'), datePartiallyKnownType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 37, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 24, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 26, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 33, 3))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'vn')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 24, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localPersonId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 25, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OtherPersonId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 26, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EuPersonId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 33, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'officialName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 34, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'firstName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 35, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sex')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 36, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateOfBirth')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 37, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
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
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
personIdentificationType._Automaton = _BuildAutomaton_()




personIdentificationPartnerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'vn'), vnType, scope=personIdentificationPartnerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 42, 3)))

personIdentificationPartnerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localPersonId'), namedPersonIdType, scope=personIdentificationPartnerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 43, 3)))

personIdentificationPartnerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OtherPersonId'), CTD_ANON_2, scope=personIdentificationPartnerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 44, 3)))

personIdentificationPartnerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'officialName'), baseNameType, scope=personIdentificationPartnerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 51, 3)))

personIdentificationPartnerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'firstName'), baseNameType, scope=personIdentificationPartnerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 52, 3)))

personIdentificationPartnerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sex'), sexType, scope=personIdentificationPartnerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 53, 3)))

personIdentificationPartnerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateOfBirth'), datePartiallyKnownType, scope=personIdentificationPartnerType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 54, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 42, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 44, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 53, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 54, 3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationPartnerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'vn')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 42, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationPartnerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localPersonId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 43, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationPartnerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OtherPersonId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 44, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationPartnerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'officialName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 51, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(personIdentificationPartnerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'firstName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 52, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(personIdentificationPartnerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sex')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 53, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(personIdentificationPartnerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateOfBirth')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 54, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
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
personIdentificationPartnerType._Automaton = _BuildAutomaton_2()




datePartiallyKnownType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yearMonthDay'), pyxb.binding.datatypes.date, scope=datePartiallyKnownType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 59, 3)))

datePartiallyKnownType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yearMonth'), pyxb.binding.datatypes.gYearMonth, scope=datePartiallyKnownType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 60, 3)))

datePartiallyKnownType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'year'), pyxb.binding.datatypes.gYear, scope=datePartiallyKnownType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 61, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(datePartiallyKnownType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yearMonthDay')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 59, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(datePartiallyKnownType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yearMonth')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 60, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(datePartiallyKnownType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'year')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 61, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
datePartiallyKnownType._Automaton = _BuildAutomaton_3()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personIdentification'), personIdentificationType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 90, 4)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 90, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_4()




def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personIdCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 12, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 13, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_5()




def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personIdCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 12, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_1_0.xsd', 13, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_6()

