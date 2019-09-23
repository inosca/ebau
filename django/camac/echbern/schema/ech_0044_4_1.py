# ../../camac/echbern/schema/ech_0044_4_1.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e20b38e7698de6077c79158dc47e0f1eeb700b22
# Generated 2019-09-26 17:57:08.876203 by PyXB version 1.2.6 using Python 3.6.8.final.0
# Namespace http://www.ech.ch/xmlns/eCH-0044/4 [xmlns:eCH-0044]

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
Namespace = pyxb.namespace.NamespaceForURI('http://www.ech.ch/xmlns/eCH-0044/4', create_if_missing=True)
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


# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0044/4}personIdCategoryType
class personIdCategoryType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'personIdCategoryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 5, 1)
    _Documentation = None
personIdCategoryType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
personIdCategoryType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
personIdCategoryType._InitializeFacetMap(personIdCategoryType._CF_minLength,
   personIdCategoryType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'personIdCategoryType', personIdCategoryType)
_module_typeBindings.personIdCategoryType = personIdCategoryType

# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 15, 4)
    _Documentation = None
STD_ANON._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(36))
STD_ANON._InitializeFacetMap(STD_ANON._CF_minLength,
   STD_ANON._CF_maxLength)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0044/4}baseNameType
class baseNameType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'baseNameType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 64, 1)
    _Documentation = None
baseNameType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
baseNameType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
baseNameType._InitializeFacetMap(baseNameType._CF_minLength,
   baseNameType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'baseNameType', baseNameType)
_module_typeBindings.baseNameType = baseNameType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0044/4}officialFirstNameType
class officialFirstNameType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'officialFirstNameType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 70, 1)
    _Documentation = None
officialFirstNameType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
officialFirstNameType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
officialFirstNameType._CF_whiteSpace = pyxb.binding.facets.CF_whiteSpace(value=pyxb.binding.facets._WhiteSpace_enum.collapse)
officialFirstNameType._InitializeFacetMap(officialFirstNameType._CF_minLength,
   officialFirstNameType._CF_maxLength,
   officialFirstNameType._CF_whiteSpace)
Namespace.addCategoryObject('typeBinding', 'officialFirstNameType', officialFirstNameType)
_module_typeBindings.officialFirstNameType = officialFirstNameType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0044/4}sexType
class sexType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'sexType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 77, 1)
    _Documentation = None
sexType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=sexType, enum_prefix=None)
sexType.n1 = sexType._CF_enumeration.addEnumeration(unicode_value='1', tag='n1')
sexType.n2 = sexType._CF_enumeration.addEnumeration(unicode_value='2', tag='n2')
sexType.n3 = sexType._CF_enumeration.addEnumeration(unicode_value='3', tag='n3')
sexType._InitializeFacetMap(sexType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'sexType', sexType)
_module_typeBindings.sexType = sexType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0044/4}vnType
class vnType (pyxb.binding.datatypes.unsignedLong):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'vnType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 84, 1)
    _Documentation = None
vnType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=vnType, value=pyxb.binding.datatypes.unsignedLong(7560000000001))
vnType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=vnType, value=pyxb.binding.datatypes.unsignedLong(7569999999999))
vnType._InitializeFacetMap(vnType._CF_minInclusive,
   vnType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'vnType', vnType)
_module_typeBindings.vnType = vnType

# Complex type {http://www.ech.ch/xmlns/eCH-0044/4}namedPersonIdType with content type ELEMENT_ONLY
class namedPersonIdType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0044/4}namedPersonIdType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'namedPersonIdType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 11, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}personIdCategory uses Python identifier personIdCategory
    __personIdCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'personIdCategory'), 'personIdCategory', '__httpwww_ech_chxmlnseCH_00444_namedPersonIdType_httpwww_ech_chxmlnseCH_00444personIdCategory', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 13, 3), )

    
    personIdCategory = property(__personIdCategory.value, __personIdCategory.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}personId uses Python identifier personId
    __personId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'personId'), 'personId', '__httpwww_ech_chxmlnseCH_00444_namedPersonIdType_httpwww_ech_chxmlnseCH_00444personId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 14, 3), )

    
    personId = property(__personId.value, __personId.set, None, None)

    _ElementMap.update({
        __personIdCategory.name() : __personIdCategory,
        __personId.name() : __personId
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.namedPersonIdType = namedPersonIdType
Namespace.addCategoryObject('typeBinding', 'namedPersonIdType', namedPersonIdType)


# Complex type {http://www.ech.ch/xmlns/eCH-0044/4}personIdentificationType with content type ELEMENT_ONLY
class personIdentificationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0044/4}personIdentificationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'personIdentificationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 24, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}vn uses Python identifier vn
    __vn = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'vn'), 'vn', '__httpwww_ech_chxmlnseCH_00444_personIdentificationType_httpwww_ech_chxmlnseCH_00444vn', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 26, 3), )

    
    vn = property(__vn.value, __vn.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}localPersonId uses Python identifier localPersonId
    __localPersonId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localPersonId'), 'localPersonId', '__httpwww_ech_chxmlnseCH_00444_personIdentificationType_httpwww_ech_chxmlnseCH_00444localPersonId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 27, 3), )

    
    localPersonId = property(__localPersonId.value, __localPersonId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}otherPersonId uses Python identifier otherPersonId
    __otherPersonId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherPersonId'), 'otherPersonId', '__httpwww_ech_chxmlnseCH_00444_personIdentificationType_httpwww_ech_chxmlnseCH_00444otherPersonId', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 28, 3), )

    
    otherPersonId = property(__otherPersonId.value, __otherPersonId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}euPersonId uses Python identifier euPersonId
    __euPersonId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'euPersonId'), 'euPersonId', '__httpwww_ech_chxmlnseCH_00444_personIdentificationType_httpwww_ech_chxmlnseCH_00444euPersonId', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 29, 3), )

    
    euPersonId = property(__euPersonId.value, __euPersonId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}officialName uses Python identifier officialName
    __officialName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'officialName'), 'officialName', '__httpwww_ech_chxmlnseCH_00444_personIdentificationType_httpwww_ech_chxmlnseCH_00444officialName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 30, 3), )

    
    officialName = property(__officialName.value, __officialName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}firstName uses Python identifier firstName
    __firstName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'firstName'), 'firstName', '__httpwww_ech_chxmlnseCH_00444_personIdentificationType_httpwww_ech_chxmlnseCH_00444firstName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 31, 3), )

    
    firstName = property(__firstName.value, __firstName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}originalName uses Python identifier originalName
    __originalName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'originalName'), 'originalName', '__httpwww_ech_chxmlnseCH_00444_personIdentificationType_httpwww_ech_chxmlnseCH_00444originalName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 32, 3), )

    
    originalName = property(__originalName.value, __originalName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}sex uses Python identifier sex
    __sex = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sex'), 'sex', '__httpwww_ech_chxmlnseCH_00444_personIdentificationType_httpwww_ech_chxmlnseCH_00444sex', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 33, 3), )

    
    sex = property(__sex.value, __sex.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}dateOfBirth uses Python identifier dateOfBirth
    __dateOfBirth = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateOfBirth'), 'dateOfBirth', '__httpwww_ech_chxmlnseCH_00444_personIdentificationType_httpwww_ech_chxmlnseCH_00444dateOfBirth', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 34, 3), )

    
    dateOfBirth = property(__dateOfBirth.value, __dateOfBirth.set, None, None)

    _ElementMap.update({
        __vn.name() : __vn,
        __localPersonId.name() : __localPersonId,
        __otherPersonId.name() : __otherPersonId,
        __euPersonId.name() : __euPersonId,
        __officialName.name() : __officialName,
        __firstName.name() : __firstName,
        __originalName.name() : __originalName,
        __sex.name() : __sex,
        __dateOfBirth.name() : __dateOfBirth
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.personIdentificationType = personIdentificationType
Namespace.addCategoryObject('typeBinding', 'personIdentificationType', personIdentificationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0044/4}personIdentificationKeyOnlyType with content type ELEMENT_ONLY
class personIdentificationKeyOnlyType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0044/4}personIdentificationKeyOnlyType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'personIdentificationKeyOnlyType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 37, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}vn uses Python identifier vn
    __vn = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'vn'), 'vn', '__httpwww_ech_chxmlnseCH_00444_personIdentificationKeyOnlyType_httpwww_ech_chxmlnseCH_00444vn', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 39, 3), )

    
    vn = property(__vn.value, __vn.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}localPersonId uses Python identifier localPersonId
    __localPersonId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localPersonId'), 'localPersonId', '__httpwww_ech_chxmlnseCH_00444_personIdentificationKeyOnlyType_httpwww_ech_chxmlnseCH_00444localPersonId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 40, 3), )

    
    localPersonId = property(__localPersonId.value, __localPersonId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}otherPersonId uses Python identifier otherPersonId
    __otherPersonId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherPersonId'), 'otherPersonId', '__httpwww_ech_chxmlnseCH_00444_personIdentificationKeyOnlyType_httpwww_ech_chxmlnseCH_00444otherPersonId', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 41, 3), )

    
    otherPersonId = property(__otherPersonId.value, __otherPersonId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}euPersonId uses Python identifier euPersonId
    __euPersonId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'euPersonId'), 'euPersonId', '__httpwww_ech_chxmlnseCH_00444_personIdentificationKeyOnlyType_httpwww_ech_chxmlnseCH_00444euPersonId', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 42, 3), )

    
    euPersonId = property(__euPersonId.value, __euPersonId.set, None, None)

    _ElementMap.update({
        __vn.name() : __vn,
        __localPersonId.name() : __localPersonId,
        __otherPersonId.name() : __otherPersonId,
        __euPersonId.name() : __euPersonId
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.personIdentificationKeyOnlyType = personIdentificationKeyOnlyType
Namespace.addCategoryObject('typeBinding', 'personIdentificationKeyOnlyType', personIdentificationKeyOnlyType)


# Complex type {http://www.ech.ch/xmlns/eCH-0044/4}personIdentificationLightType with content type ELEMENT_ONLY
class personIdentificationLightType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0044/4}personIdentificationLightType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'personIdentificationLightType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 45, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}vn uses Python identifier vn
    __vn = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'vn'), 'vn', '__httpwww_ech_chxmlnseCH_00444_personIdentificationLightType_httpwww_ech_chxmlnseCH_00444vn', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 47, 3), )

    
    vn = property(__vn.value, __vn.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}localPersonId uses Python identifier localPersonId
    __localPersonId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localPersonId'), 'localPersonId', '__httpwww_ech_chxmlnseCH_00444_personIdentificationLightType_httpwww_ech_chxmlnseCH_00444localPersonId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 48, 3), )

    
    localPersonId = property(__localPersonId.value, __localPersonId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}otherPersonId uses Python identifier otherPersonId
    __otherPersonId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherPersonId'), 'otherPersonId', '__httpwww_ech_chxmlnseCH_00444_personIdentificationLightType_httpwww_ech_chxmlnseCH_00444otherPersonId', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 49, 3), )

    
    otherPersonId = property(__otherPersonId.value, __otherPersonId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}officialName uses Python identifier officialName
    __officialName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'officialName'), 'officialName', '__httpwww_ech_chxmlnseCH_00444_personIdentificationLightType_httpwww_ech_chxmlnseCH_00444officialName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 50, 3), )

    
    officialName = property(__officialName.value, __officialName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}firstName uses Python identifier firstName
    __firstName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'firstName'), 'firstName', '__httpwww_ech_chxmlnseCH_00444_personIdentificationLightType_httpwww_ech_chxmlnseCH_00444firstName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 51, 3), )

    
    firstName = property(__firstName.value, __firstName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}originalName uses Python identifier originalName
    __originalName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'originalName'), 'originalName', '__httpwww_ech_chxmlnseCH_00444_personIdentificationLightType_httpwww_ech_chxmlnseCH_00444originalName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 52, 3), )

    
    originalName = property(__originalName.value, __originalName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}sex uses Python identifier sex
    __sex = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sex'), 'sex', '__httpwww_ech_chxmlnseCH_00444_personIdentificationLightType_httpwww_ech_chxmlnseCH_00444sex', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 53, 3), )

    
    sex = property(__sex.value, __sex.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}dateOfBirth uses Python identifier dateOfBirth
    __dateOfBirth = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateOfBirth'), 'dateOfBirth', '__httpwww_ech_chxmlnseCH_00444_personIdentificationLightType_httpwww_ech_chxmlnseCH_00444dateOfBirth', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 54, 3), )

    
    dateOfBirth = property(__dateOfBirth.value, __dateOfBirth.set, None, None)

    _ElementMap.update({
        __vn.name() : __vn,
        __localPersonId.name() : __localPersonId,
        __otherPersonId.name() : __otherPersonId,
        __officialName.name() : __officialName,
        __firstName.name() : __firstName,
        __originalName.name() : __originalName,
        __sex.name() : __sex,
        __dateOfBirth.name() : __dateOfBirth
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.personIdentificationLightType = personIdentificationLightType
Namespace.addCategoryObject('typeBinding', 'personIdentificationLightType', personIdentificationLightType)


# Complex type {http://www.ech.ch/xmlns/eCH-0044/4}datePartiallyKnownType with content type ELEMENT_ONLY
class datePartiallyKnownType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0044/4}datePartiallyKnownType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'datePartiallyKnownType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 57, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}yearMonthDay uses Python identifier yearMonthDay
    __yearMonthDay = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yearMonthDay'), 'yearMonthDay', '__httpwww_ech_chxmlnseCH_00444_datePartiallyKnownType_httpwww_ech_chxmlnseCH_00444yearMonthDay', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 59, 3), )

    
    yearMonthDay = property(__yearMonthDay.value, __yearMonthDay.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}yearMonth uses Python identifier yearMonth
    __yearMonth = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yearMonth'), 'yearMonth', '__httpwww_ech_chxmlnseCH_00444_datePartiallyKnownType_httpwww_ech_chxmlnseCH_00444yearMonth', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 60, 3), )

    
    yearMonth = property(__yearMonth.value, __yearMonth.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}year uses Python identifier year
    __year = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'year'), 'year', '__httpwww_ech_chxmlnseCH_00444_datePartiallyKnownType_httpwww_ech_chxmlnseCH_00444year', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 61, 3), )

    
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
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 91, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0044/4}personIdentification uses Python identifier personIdentification
    __personIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'personIdentification'), 'personIdentification', '__httpwww_ech_chxmlnseCH_00444_CTD_ANON_httpwww_ech_chxmlnseCH_00444personIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 93, 4), )

    
    personIdentification = property(__personIdentification.value, __personIdentification.set, None, None)

    _ElementMap.update({
        __personIdentification.name() : __personIdentification
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


personIdentificationRoot = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personIdentificationRoot'), CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 90, 1))
Namespace.addCategoryObject('elementBinding', personIdentificationRoot.name().localName(), personIdentificationRoot)



namedPersonIdType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personIdCategory'), personIdCategoryType, scope=namedPersonIdType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 13, 3)))

namedPersonIdType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personId'), STD_ANON, scope=namedPersonIdType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 14, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(namedPersonIdType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personIdCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 13, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(namedPersonIdType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 14, 3))
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




personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'vn'), vnType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 26, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localPersonId'), namedPersonIdType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 27, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherPersonId'), namedPersonIdType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 28, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'euPersonId'), namedPersonIdType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 29, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'officialName'), baseNameType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 30, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'firstName'), baseNameType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 31, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'originalName'), baseNameType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 32, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sex'), sexType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 33, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateOfBirth'), datePartiallyKnownType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 34, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 26, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 28, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 29, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 32, 3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'vn')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 26, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localPersonId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 27, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherPersonId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 28, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'euPersonId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 29, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'officialName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 30, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'firstName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 31, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'originalName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 32, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sex')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 33, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateOfBirth')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 34, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
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
    transitions.append(fac.Transition(st_7, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
personIdentificationType._Automaton = _BuildAutomaton_()




personIdentificationKeyOnlyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'vn'), vnType, scope=personIdentificationKeyOnlyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 39, 3)))

personIdentificationKeyOnlyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localPersonId'), namedPersonIdType, scope=personIdentificationKeyOnlyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 40, 3)))

personIdentificationKeyOnlyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherPersonId'), namedPersonIdType, scope=personIdentificationKeyOnlyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 41, 3)))

personIdentificationKeyOnlyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'euPersonId'), namedPersonIdType, scope=personIdentificationKeyOnlyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 42, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 39, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 41, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 42, 3))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationKeyOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'vn')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 39, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(personIdentificationKeyOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localPersonId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 40, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(personIdentificationKeyOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherPersonId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 41, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(personIdentificationKeyOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'euPersonId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 42, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
personIdentificationKeyOnlyType._Automaton = _BuildAutomaton_2()




personIdentificationLightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'vn'), vnType, scope=personIdentificationLightType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 47, 3)))

personIdentificationLightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localPersonId'), namedPersonIdType, scope=personIdentificationLightType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 48, 3)))

personIdentificationLightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherPersonId'), namedPersonIdType, scope=personIdentificationLightType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 49, 3)))

personIdentificationLightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'officialName'), baseNameType, scope=personIdentificationLightType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 50, 3)))

personIdentificationLightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'firstName'), baseNameType, scope=personIdentificationLightType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 51, 3)))

personIdentificationLightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'originalName'), baseNameType, scope=personIdentificationLightType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 52, 3)))

personIdentificationLightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sex'), sexType, scope=personIdentificationLightType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 53, 3)))

personIdentificationLightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateOfBirth'), datePartiallyKnownType, scope=personIdentificationLightType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 54, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 47, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 48, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 49, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 52, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 53, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 54, 3))
    counters.add(cc_5)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationLightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'vn')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 47, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationLightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localPersonId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 48, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationLightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherPersonId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 49, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(personIdentificationLightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'officialName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 50, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(personIdentificationLightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'firstName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 51, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(personIdentificationLightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'originalName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 52, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(personIdentificationLightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sex')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 53, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(personIdentificationLightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateOfBirth')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 54, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
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
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
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
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
personIdentificationLightType._Automaton = _BuildAutomaton_3()




datePartiallyKnownType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yearMonthDay'), pyxb.binding.datatypes.date, scope=datePartiallyKnownType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 59, 3)))

datePartiallyKnownType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yearMonth'), pyxb.binding.datatypes.gYearMonth, scope=datePartiallyKnownType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 60, 3)))

datePartiallyKnownType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'year'), pyxb.binding.datatypes.gYear, scope=datePartiallyKnownType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 61, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(datePartiallyKnownType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yearMonthDay')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 59, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(datePartiallyKnownType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yearMonth')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 60, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(datePartiallyKnownType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'year')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 61, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
datePartiallyKnownType._Automaton = _BuildAutomaton_4()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personIdentification'), personIdentificationType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 93, 4)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0044_4_1.xsd', 93, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_5()

