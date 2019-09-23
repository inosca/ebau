# ../../camac/echbern/schema/ech_0046_1_0.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:f795e2507397ec14d8cbe32eec815c17b8d61511
# Generated 2019-09-26 17:57:08.875004 by PyXB version 1.2.6 using Python 3.6.8.final.0
# Namespace http://www.ech.ch/xmlns/eCH-0046/1 [xmlns:eCH-0046]

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
import camac.echbern.schema.ech_0044_1_0 as _ImportedBinding_camac_echbern_schema_ech_0044_1_0
import camac.echbern.schema.ech_0010_3_0 as _ImportedBinding_camac_echbern_schema_ech_0010_3_0

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.ech.ch/xmlns/eCH-0046/1', create_if_missing=True)
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


# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0046/1}emailCategoryType
class emailCategoryType (pyxb.binding.datatypes.integer, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'emailCategoryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 56, 1)
    _Documentation = None
emailCategoryType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=emailCategoryType, enum_prefix=None)
emailCategoryType._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
emailCategoryType._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
emailCategoryType._InitializeFacetMap(emailCategoryType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'emailCategoryType', emailCategoryType)
_module_typeBindings.emailCategoryType = emailCategoryType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0046/1}emailAddressType
class emailAddressType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'emailAddressType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 62, 1)
    _Documentation = None
emailAddressType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
emailAddressType._CF_pattern = pyxb.binding.facets.CF_pattern()
emailAddressType._CF_pattern.addPattern(pattern="[A-Za-z0-9!#-'\\*\\+\\-/=\\?\\^_`\\{-~]+(\\.[A-Za-z0-9!#-'\\*\\+\\-/=\\?\\^_`\\{-~]+)*@[A-Za-z0-9!#-'\\*\\+\\-/=\\?\\^_`\\{-~]+(\\.[A-Za-z0-9!#-'\\*\\+\\-/=\\?\\^_`\\{-~]+)*")
emailAddressType._CF_whiteSpace = pyxb.binding.facets.CF_whiteSpace(value=pyxb.binding.facets._WhiteSpace_enum.collapse)
emailAddressType._InitializeFacetMap(emailAddressType._CF_maxLength,
   emailAddressType._CF_pattern,
   emailAddressType._CF_whiteSpace)
Namespace.addCategoryObject('typeBinding', 'emailAddressType', emailAddressType)
_module_typeBindings.emailAddressType = emailAddressType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0046/1}addressCategoryType
class addressCategoryType (pyxb.binding.datatypes.integer, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'addressCategoryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 69, 1)
    _Documentation = None
addressCategoryType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=addressCategoryType, enum_prefix=None)
addressCategoryType._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
addressCategoryType._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
addressCategoryType._InitializeFacetMap(addressCategoryType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'addressCategoryType', addressCategoryType)
_module_typeBindings.addressCategoryType = addressCategoryType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0046/1}phoneCategoryType
class phoneCategoryType (pyxb.binding.datatypes.integer, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'phoneCategoryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 75, 1)
    _Documentation = None
phoneCategoryType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=phoneCategoryType, enum_prefix=None)
phoneCategoryType._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
phoneCategoryType._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
phoneCategoryType._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
phoneCategoryType._CF_enumeration.addEnumeration(unicode_value='4', tag=None)
phoneCategoryType._CF_enumeration.addEnumeration(unicode_value='5', tag=None)
phoneCategoryType._CF_enumeration.addEnumeration(unicode_value='6', tag=None)
phoneCategoryType._CF_enumeration.addEnumeration(unicode_value='7', tag=None)
phoneCategoryType._CF_enumeration.addEnumeration(unicode_value='8', tag=None)
phoneCategoryType._CF_enumeration.addEnumeration(unicode_value='9', tag=None)
phoneCategoryType._CF_enumeration.addEnumeration(unicode_value='10', tag=None)
phoneCategoryType._InitializeFacetMap(phoneCategoryType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'phoneCategoryType', phoneCategoryType)
_module_typeBindings.phoneCategoryType = phoneCategoryType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0046/1}phoneNumberType
class phoneNumberType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'phoneNumberType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 89, 1)
    _Documentation = None
phoneNumberType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
phoneNumberType._CF_pattern = pyxb.binding.facets.CF_pattern()
phoneNumberType._CF_pattern.addPattern(pattern='\\d{10,20}')
phoneNumberType._CF_whiteSpace = pyxb.binding.facets.CF_whiteSpace(value=pyxb.binding.facets._WhiteSpace_enum.collapse)
phoneNumberType._InitializeFacetMap(phoneNumberType._CF_maxLength,
   phoneNumberType._CF_pattern,
   phoneNumberType._CF_whiteSpace)
Namespace.addCategoryObject('typeBinding', 'phoneNumberType', phoneNumberType)
_module_typeBindings.phoneNumberType = phoneNumberType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0046/1}internetCategoryType
class internetCategoryType (pyxb.binding.datatypes.integer, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'internetCategoryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 96, 1)
    _Documentation = None
internetCategoryType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=internetCategoryType, enum_prefix=None)
internetCategoryType._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
internetCategoryType._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
internetCategoryType._InitializeFacetMap(internetCategoryType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'internetCategoryType', internetCategoryType)
_module_typeBindings.internetCategoryType = internetCategoryType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0046/1}internetAddressType
class internetAddressType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'internetAddressType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 102, 1)
    _Documentation = None
internetAddressType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
internetAddressType._CF_pattern = pyxb.binding.facets.CF_pattern()
internetAddressType._CF_pattern.addPattern(pattern='http://.*')
internetAddressType._CF_whiteSpace = pyxb.binding.facets.CF_whiteSpace(value=pyxb.binding.facets._WhiteSpace_enum.collapse)
internetAddressType._InitializeFacetMap(internetAddressType._CF_maxLength,
   internetAddressType._CF_pattern,
   internetAddressType._CF_whiteSpace)
Namespace.addCategoryObject('typeBinding', 'internetAddressType', internetAddressType)
_module_typeBindings.internetAddressType = internetAddressType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0046/1}freeKategoryTextType
class freeKategoryTextType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'freeKategoryTextType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 109, 1)
    _Documentation = None
freeKategoryTextType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
freeKategoryTextType._CF_whiteSpace = pyxb.binding.facets.CF_whiteSpace(value=pyxb.binding.facets._WhiteSpace_enum.collapse)
freeKategoryTextType._InitializeFacetMap(freeKategoryTextType._CF_maxLength,
   freeKategoryTextType._CF_whiteSpace)
Namespace.addCategoryObject('typeBinding', 'freeKategoryTextType', freeKategoryTextType)
_module_typeBindings.freeKategoryTextType = freeKategoryTextType

# Complex type {http://www.ech.ch/xmlns/eCH-0046/1}contactType with content type ELEMENT_ONLY
class contactType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0046/1}contactType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'contactType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 7, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_00461_contactType_httpwww_ech_chxmlnseCH_00461localID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 9, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}address uses Python identifier address
    __address = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'address'), 'address', '__httpwww_ech_chxmlnseCH_00461_contactType_httpwww_ech_chxmlnseCH_00461address', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 10, 3), )

    
    address = property(__address.value, __address.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}email uses Python identifier email
    __email = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'email'), 'email', '__httpwww_ech_chxmlnseCH_00461_contactType_httpwww_ech_chxmlnseCH_00461email', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 11, 3), )

    
    email = property(__email.value, __email.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}phone uses Python identifier phone
    __phone = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'phone'), 'phone', '__httpwww_ech_chxmlnseCH_00461_contactType_httpwww_ech_chxmlnseCH_00461phone', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 12, 3), )

    
    phone = property(__phone.value, __phone.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}internet uses Python identifier internet
    __internet = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'internet'), 'internet', '__httpwww_ech_chxmlnseCH_00461_contactType_httpwww_ech_chxmlnseCH_00461internet', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 13, 3), )

    
    internet = property(__internet.value, __internet.set, None, None)

    _ElementMap.update({
        __localID.name() : __localID,
        __address.name() : __address,
        __email.name() : __email,
        __phone.name() : __phone,
        __internet.name() : __internet
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.contactType = contactType
Namespace.addCategoryObject('typeBinding', 'contactType', contactType)


# Complex type {http://www.ech.ch/xmlns/eCH-0046/1}addressType with content type ELEMENT_ONLY
class addressType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0046/1}addressType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'addressType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 16, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}addressCategory uses Python identifier addressCategory
    __addressCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'addressCategory'), 'addressCategory', '__httpwww_ech_chxmlnseCH_00461_addressType_httpwww_ech_chxmlnseCH_00461addressCategory', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 19, 4), )

    
    addressCategory = property(__addressCategory.value, __addressCategory.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}otherAddressCategory uses Python identifier otherAddressCategory
    __otherAddressCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherAddressCategory'), 'otherAddressCategory', '__httpwww_ech_chxmlnseCH_00461_addressType_httpwww_ech_chxmlnseCH_00461otherAddressCategory', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 20, 4), )

    
    otherAddressCategory = property(__otherAddressCategory.value, __otherAddressCategory.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}postalAddress uses Python identifier postalAddress
    __postalAddress = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'postalAddress'), 'postalAddress', '__httpwww_ech_chxmlnseCH_00461_addressType_httpwww_ech_chxmlnseCH_00461postalAddress', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 22, 3), )

    
    postalAddress = property(__postalAddress.value, __postalAddress.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}validity uses Python identifier validity
    __validity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'validity'), 'validity', '__httpwww_ech_chxmlnseCH_00461_addressType_httpwww_ech_chxmlnseCH_00461validity', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 23, 3), )

    
    validity = property(__validity.value, __validity.set, None, None)

    _ElementMap.update({
        __addressCategory.name() : __addressCategory,
        __otherAddressCategory.name() : __otherAddressCategory,
        __postalAddress.name() : __postalAddress,
        __validity.name() : __validity
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.addressType = addressType
Namespace.addCategoryObject('typeBinding', 'addressType', addressType)


# Complex type {http://www.ech.ch/xmlns/eCH-0046/1}emailType with content type ELEMENT_ONLY
class emailType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0046/1}emailType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'emailType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 26, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}emailCategory uses Python identifier emailCategory
    __emailCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'emailCategory'), 'emailCategory', '__httpwww_ech_chxmlnseCH_00461_emailType_httpwww_ech_chxmlnseCH_00461emailCategory', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 29, 4), )

    
    emailCategory = property(__emailCategory.value, __emailCategory.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}otherEmailCategory uses Python identifier otherEmailCategory
    __otherEmailCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherEmailCategory'), 'otherEmailCategory', '__httpwww_ech_chxmlnseCH_00461_emailType_httpwww_ech_chxmlnseCH_00461otherEmailCategory', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 30, 4), )

    
    otherEmailCategory = property(__otherEmailCategory.value, __otherEmailCategory.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}emailAddress uses Python identifier emailAddress
    __emailAddress = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'emailAddress'), 'emailAddress', '__httpwww_ech_chxmlnseCH_00461_emailType_httpwww_ech_chxmlnseCH_00461emailAddress', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 32, 3), )

    
    emailAddress = property(__emailAddress.value, __emailAddress.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}validity uses Python identifier validity
    __validity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'validity'), 'validity', '__httpwww_ech_chxmlnseCH_00461_emailType_httpwww_ech_chxmlnseCH_00461validity', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 33, 3), )

    
    validity = property(__validity.value, __validity.set, None, None)

    _ElementMap.update({
        __emailCategory.name() : __emailCategory,
        __otherEmailCategory.name() : __otherEmailCategory,
        __emailAddress.name() : __emailAddress,
        __validity.name() : __validity
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.emailType = emailType
Namespace.addCategoryObject('typeBinding', 'emailType', emailType)


# Complex type {http://www.ech.ch/xmlns/eCH-0046/1}phoneType with content type ELEMENT_ONLY
class phoneType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0046/1}phoneType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'phoneType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 36, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}phoneCategory uses Python identifier phoneCategory
    __phoneCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'phoneCategory'), 'phoneCategory', '__httpwww_ech_chxmlnseCH_00461_phoneType_httpwww_ech_chxmlnseCH_00461phoneCategory', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 39, 4), )

    
    phoneCategory = property(__phoneCategory.value, __phoneCategory.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}otherPhoneCategory uses Python identifier otherPhoneCategory
    __otherPhoneCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherPhoneCategory'), 'otherPhoneCategory', '__httpwww_ech_chxmlnseCH_00461_phoneType_httpwww_ech_chxmlnseCH_00461otherPhoneCategory', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 40, 4), )

    
    otherPhoneCategory = property(__otherPhoneCategory.value, __otherPhoneCategory.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}phoneNumber uses Python identifier phoneNumber
    __phoneNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'phoneNumber'), 'phoneNumber', '__httpwww_ech_chxmlnseCH_00461_phoneType_httpwww_ech_chxmlnseCH_00461phoneNumber', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 42, 3), )

    
    phoneNumber = property(__phoneNumber.value, __phoneNumber.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}validity uses Python identifier validity
    __validity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'validity'), 'validity', '__httpwww_ech_chxmlnseCH_00461_phoneType_httpwww_ech_chxmlnseCH_00461validity', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 43, 3), )

    
    validity = property(__validity.value, __validity.set, None, None)

    _ElementMap.update({
        __phoneCategory.name() : __phoneCategory,
        __otherPhoneCategory.name() : __otherPhoneCategory,
        __phoneNumber.name() : __phoneNumber,
        __validity.name() : __validity
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.phoneType = phoneType
Namespace.addCategoryObject('typeBinding', 'phoneType', phoneType)


# Complex type {http://www.ech.ch/xmlns/eCH-0046/1}internetType with content type ELEMENT_ONLY
class internetType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0046/1}internetType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'internetType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 46, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}internetCategory uses Python identifier internetCategory
    __internetCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'internetCategory'), 'internetCategory', '__httpwww_ech_chxmlnseCH_00461_internetType_httpwww_ech_chxmlnseCH_00461internetCategory', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 49, 4), )

    
    internetCategory = property(__internetCategory.value, __internetCategory.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}otherInternetCategory uses Python identifier otherInternetCategory
    __otherInternetCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherInternetCategory'), 'otherInternetCategory', '__httpwww_ech_chxmlnseCH_00461_internetType_httpwww_ech_chxmlnseCH_00461otherInternetCategory', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 50, 4), )

    
    otherInternetCategory = property(__otherInternetCategory.value, __otherInternetCategory.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}internetAddress uses Python identifier internetAddress
    __internetAddress = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'internetAddress'), 'internetAddress', '__httpwww_ech_chxmlnseCH_00461_internetType_httpwww_ech_chxmlnseCH_00461internetAddress', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 52, 3), )

    
    internetAddress = property(__internetAddress.value, __internetAddress.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}validity uses Python identifier validity
    __validity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'validity'), 'validity', '__httpwww_ech_chxmlnseCH_00461_internetType_httpwww_ech_chxmlnseCH_00461validity', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 53, 3), )

    
    validity = property(__validity.value, __validity.set, None, None)

    _ElementMap.update({
        __internetCategory.name() : __internetCategory,
        __otherInternetCategory.name() : __otherInternetCategory,
        __internetAddress.name() : __internetAddress,
        __validity.name() : __validity
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.internetType = internetType
Namespace.addCategoryObject('typeBinding', 'internetType', internetType)


# Complex type {http://www.ech.ch/xmlns/eCH-0046/1}dateRangeType with content type ELEMENT_ONLY
class dateRangeType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0046/1}dateRangeType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dateRangeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 115, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}dateFrom uses Python identifier dateFrom
    __dateFrom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateFrom'), 'dateFrom', '__httpwww_ech_chxmlnseCH_00461_dateRangeType_httpwww_ech_chxmlnseCH_00461dateFrom', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 117, 3), )

    
    dateFrom = property(__dateFrom.value, __dateFrom.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}dateTo uses Python identifier dateTo
    __dateTo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateTo'), 'dateTo', '__httpwww_ech_chxmlnseCH_00461_dateRangeType_httpwww_ech_chxmlnseCH_00461dateTo', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 118, 3), )

    
    dateTo = property(__dateTo.value, __dateTo.set, None, None)

    _ElementMap.update({
        __dateFrom.name() : __dateFrom,
        __dateTo.name() : __dateTo
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.dateRangeType = dateRangeType
Namespace.addCategoryObject('typeBinding', 'dateRangeType', dateRangeType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 122, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0046/1}contact uses Python identifier contact
    __contact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'contact'), 'contact', '__httpwww_ech_chxmlnseCH_00461_CTD_ANON_httpwww_ech_chxmlnseCH_00461contact', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 124, 4), )

    
    contact = property(__contact.value, __contact.set, None, None)

    _ElementMap.update({
        __contact.name() : __contact
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


contactRoot = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contactRoot'), CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 121, 1))
Namespace.addCategoryObject('elementBinding', contactRoot.name().localName(), contactRoot)



contactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), _ImportedBinding_camac_echbern_schema_ech_0044_1_0.namedPersonIdType, scope=contactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 9, 3)))

contactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'address'), addressType, scope=contactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 10, 3)))

contactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'email'), emailType, scope=contactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 11, 3)))

contactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'phone'), phoneType, scope=contactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 12, 3)))

contactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'internet'), internetType, scope=contactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 13, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 9, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 10, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 11, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 12, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 13, 3))
    counters.add(cc_4)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(contactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 9, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(contactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'address')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 10, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(contactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'email')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 11, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(contactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'phone')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 12, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(contactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'internet')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 13, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
contactType._Automaton = _BuildAutomaton()




addressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'addressCategory'), addressCategoryType, scope=addressType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 19, 4)))

addressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherAddressCategory'), freeKategoryTextType, scope=addressType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 20, 4)))

addressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'postalAddress'), _ImportedBinding_camac_echbern_schema_ech_0010_3_0.mailAddressType, scope=addressType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 22, 3)))

addressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'validity'), dateRangeType, scope=addressType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 23, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 18, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 23, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(addressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'addressCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 19, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(addressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherAddressCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 20, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(addressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'postalAddress')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 22, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(addressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'validity')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 23, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
addressType._Automaton = _BuildAutomaton_()




emailType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'emailCategory'), emailCategoryType, scope=emailType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 29, 4)))

emailType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherEmailCategory'), freeKategoryTextType, scope=emailType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 30, 4)))

emailType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'emailAddress'), emailAddressType, scope=emailType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 32, 3)))

emailType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'validity'), dateRangeType, scope=emailType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 33, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 28, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 33, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(emailType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'emailCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 29, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(emailType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherEmailCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 30, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(emailType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'emailAddress')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 32, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(emailType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'validity')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 33, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
emailType._Automaton = _BuildAutomaton_2()




phoneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'phoneCategory'), phoneCategoryType, scope=phoneType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 39, 4)))

phoneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherPhoneCategory'), freeKategoryTextType, scope=phoneType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 40, 4)))

phoneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'phoneNumber'), phoneNumberType, scope=phoneType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 42, 3)))

phoneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'validity'), dateRangeType, scope=phoneType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 43, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 38, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 43, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(phoneType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'phoneCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 39, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(phoneType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherPhoneCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 40, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(phoneType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'phoneNumber')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 42, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(phoneType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'validity')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 43, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
phoneType._Automaton = _BuildAutomaton_3()




internetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'internetCategory'), internetCategoryType, scope=internetType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 49, 4)))

internetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherInternetCategory'), freeKategoryTextType, scope=internetType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 50, 4)))

internetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'internetAddress'), internetAddressType, scope=internetType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 52, 3)))

internetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'validity'), dateRangeType, scope=internetType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 53, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 48, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 53, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(internetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'internetCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 49, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(internetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherInternetCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 50, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(internetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'internetAddress')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 52, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(internetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'validity')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 53, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
internetType._Automaton = _BuildAutomaton_4()




dateRangeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateFrom'), pyxb.binding.datatypes.date, scope=dateRangeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 117, 3)))

dateRangeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateTo'), pyxb.binding.datatypes.date, scope=dateRangeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 118, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 117, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 118, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(dateRangeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateFrom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 117, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(dateRangeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateTo')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 118, 3))
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
dateRangeType._Automaton = _BuildAutomaton_5()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contact'), contactType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 124, 4)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'contact')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0046_1_0.xsd', 124, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_6()

