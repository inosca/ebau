# ../../camac/echbern/schema/ech_0097_2_0.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:c77de26c97dd629e89fd332613ef2b4ab3ec9785
# Generated 2019-09-26 17:57:08.875739 by PyXB version 1.2.6 using Python 3.6.8.final.0
# Namespace http://www.ech.ch/xmlns/eCH-0097/2 [xmlns:eCH-0097]

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
Namespace = pyxb.namespace.NamespaceForURI('http://www.ech.ch/xmlns/eCH-0097/2', create_if_missing=True)
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


# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0097/2}organisationIdCategoryType
class organisationIdCategoryType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'organisationIdCategoryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 5, 1)
    _Documentation = None
organisationIdCategoryType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
organisationIdCategoryType._InitializeFacetMap(organisationIdCategoryType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'organisationIdCategoryType', organisationIdCategoryType)
_module_typeBindings.organisationIdCategoryType = organisationIdCategoryType

# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 31, 4)
    _Documentation = None
STD_ANON._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
STD_ANON._InitializeFacetMap(STD_ANON._CF_minLength,
   STD_ANON._CF_maxLength)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0097/2}uidOrganisationIdCategorieType
class uidOrganisationIdCategorieType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'uidOrganisationIdCategorieType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 46, 1)
    _Documentation = None
uidOrganisationIdCategorieType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(3))
uidOrganisationIdCategorieType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(3))
uidOrganisationIdCategorieType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=uidOrganisationIdCategorieType, enum_prefix=None)
uidOrganisationIdCategorieType.CHE = uidOrganisationIdCategorieType._CF_enumeration.addEnumeration(unicode_value='CHE', tag='CHE')
uidOrganisationIdCategorieType.ADM = uidOrganisationIdCategorieType._CF_enumeration.addEnumeration(unicode_value='ADM', tag='ADM')
uidOrganisationIdCategorieType._InitializeFacetMap(uidOrganisationIdCategorieType._CF_minLength,
   uidOrganisationIdCategorieType._CF_maxLength,
   uidOrganisationIdCategorieType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'uidOrganisationIdCategorieType', uidOrganisationIdCategorieType)
_module_typeBindings.uidOrganisationIdCategorieType = uidOrganisationIdCategorieType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0097/2}uidOrganisationIdType
class uidOrganisationIdType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'uidOrganisationIdType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 54, 1)
    _Documentation = None
uidOrganisationIdType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=uidOrganisationIdType, value=pyxb.binding.datatypes.nonNegativeInteger(1))
uidOrganisationIdType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=uidOrganisationIdType, value=pyxb.binding.datatypes.nonNegativeInteger(999999999))
uidOrganisationIdType._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(9))
uidOrganisationIdType._CF_fractionDigits = pyxb.binding.facets.CF_fractionDigits(value=pyxb.binding.datatypes.nonNegativeInteger(0))
uidOrganisationIdType._InitializeFacetMap(uidOrganisationIdType._CF_minInclusive,
   uidOrganisationIdType._CF_maxInclusive,
   uidOrganisationIdType._CF_totalDigits,
   uidOrganisationIdType._CF_fractionDigits)
Namespace.addCategoryObject('typeBinding', 'uidOrganisationIdType', uidOrganisationIdType)
_module_typeBindings.uidOrganisationIdType = uidOrganisationIdType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0097/2}organisationNameType
class organisationNameType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'organisationNameType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 62, 1)
    _Documentation = None
organisationNameType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
organisationNameType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(255))
organisationNameType._InitializeFacetMap(organisationNameType._CF_minLength,
   organisationNameType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'organisationNameType', organisationNameType)
_module_typeBindings.organisationNameType = organisationNameType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0097/2}legalFormType
class legalFormType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'legalFormType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 68, 1)
    _Documentation = None
legalFormType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(2))
legalFormType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(4))
legalFormType._CF_pattern = pyxb.binding.facets.CF_pattern()
legalFormType._CF_pattern.addPattern(pattern='\\d{2,4}')
legalFormType._InitializeFacetMap(legalFormType._CF_minLength,
   legalFormType._CF_maxLength,
   legalFormType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'legalFormType', legalFormType)
_module_typeBindings.legalFormType = legalFormType

# Atomic simple type: [anonymous]
class STD_ANON_ (organisationIdCategoryType):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 24, 4)
    _Documentation = None
STD_ANON_._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_minLength)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Complex type {http://www.ech.ch/xmlns/eCH-0097/2}organisationIdentificationType with content type ELEMENT_ONLY
class organisationIdentificationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0097/2}organisationIdentificationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'organisationIdentificationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 10, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0097/2}uid uses Python identifier uid
    __uid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uid'), 'uid', '__httpwww_ech_chxmlnseCH_00972_organisationIdentificationType_httpwww_ech_chxmlnseCH_00972uid', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 12, 3), )

    
    uid = property(__uid.value, __uid.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0097/2}localOrganisationId uses Python identifier localOrganisationId
    __localOrganisationId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localOrganisationId'), 'localOrganisationId', '__httpwww_ech_chxmlnseCH_00972_organisationIdentificationType_httpwww_ech_chxmlnseCH_00972localOrganisationId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 13, 3), )

    
    localOrganisationId = property(__localOrganisationId.value, __localOrganisationId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0097/2}OtherOrganisationId uses Python identifier OtherOrganisationId
    __OtherOrganisationId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OtherOrganisationId'), 'OtherOrganisationId', '__httpwww_ech_chxmlnseCH_00972_organisationIdentificationType_httpwww_ech_chxmlnseCH_00972OtherOrganisationId', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 14, 3), )

    
    OtherOrganisationId = property(__OtherOrganisationId.value, __OtherOrganisationId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0097/2}organisationName uses Python identifier organisationName
    __organisationName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'organisationName'), 'organisationName', '__httpwww_ech_chxmlnseCH_00972_organisationIdentificationType_httpwww_ech_chxmlnseCH_00972organisationName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 15, 3), )

    
    organisationName = property(__organisationName.value, __organisationName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0097/2}organisationLegalName uses Python identifier organisationLegalName
    __organisationLegalName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'organisationLegalName'), 'organisationLegalName', '__httpwww_ech_chxmlnseCH_00972_organisationIdentificationType_httpwww_ech_chxmlnseCH_00972organisationLegalName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 16, 3), )

    
    organisationLegalName = property(__organisationLegalName.value, __organisationLegalName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0097/2}organisationAdditionalName uses Python identifier organisationAdditionalName
    __organisationAdditionalName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'organisationAdditionalName'), 'organisationAdditionalName', '__httpwww_ech_chxmlnseCH_00972_organisationIdentificationType_httpwww_ech_chxmlnseCH_00972organisationAdditionalName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 17, 3), )

    
    organisationAdditionalName = property(__organisationAdditionalName.value, __organisationAdditionalName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0097/2}legalForm uses Python identifier legalForm
    __legalForm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'legalForm'), 'legalForm', '__httpwww_ech_chxmlnseCH_00972_organisationIdentificationType_httpwww_ech_chxmlnseCH_00972legalForm', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 18, 3), )

    
    legalForm = property(__legalForm.value, __legalForm.set, None, None)

    _ElementMap.update({
        __uid.name() : __uid,
        __localOrganisationId.name() : __localOrganisationId,
        __OtherOrganisationId.name() : __OtherOrganisationId,
        __organisationName.name() : __organisationName,
        __organisationLegalName.name() : __organisationLegalName,
        __organisationAdditionalName.name() : __organisationAdditionalName,
        __legalForm.name() : __legalForm
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.organisationIdentificationType = organisationIdentificationType
Namespace.addCategoryObject('typeBinding', 'organisationIdentificationType', organisationIdentificationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0097/2}namedOrganisationIdType with content type ELEMENT_ONLY
class namedOrganisationIdType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0097/2}namedOrganisationIdType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'namedOrganisationIdType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0097/2}organisationIdCategory uses Python identifier organisationIdCategory
    __organisationIdCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'organisationIdCategory'), 'organisationIdCategory', '__httpwww_ech_chxmlnseCH_00972_namedOrganisationIdType_httpwww_ech_chxmlnseCH_00972organisationIdCategory', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 23, 3), )

    
    organisationIdCategory = property(__organisationIdCategory.value, __organisationIdCategory.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0097/2}organisationId uses Python identifier organisationId
    __organisationId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'organisationId'), 'organisationId', '__httpwww_ech_chxmlnseCH_00972_namedOrganisationIdType_httpwww_ech_chxmlnseCH_00972organisationId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 30, 3), )

    
    organisationId = property(__organisationId.value, __organisationId.set, None, None)

    _ElementMap.update({
        __organisationIdCategory.name() : __organisationIdCategory,
        __organisationId.name() : __organisationId
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.namedOrganisationIdType = namedOrganisationIdType
Namespace.addCategoryObject('typeBinding', 'namedOrganisationIdType', namedOrganisationIdType)


# Complex type {http://www.ech.ch/xmlns/eCH-0097/2}uidStructureType with content type ELEMENT_ONLY
class uidStructureType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0097/2}uidStructureType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'uidStructureType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 40, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0097/2}uidOrganisationIdCategorie uses Python identifier uidOrganisationIdCategorie
    __uidOrganisationIdCategorie = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uidOrganisationIdCategorie'), 'uidOrganisationIdCategorie', '__httpwww_ech_chxmlnseCH_00972_uidStructureType_httpwww_ech_chxmlnseCH_00972uidOrganisationIdCategorie', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 42, 3), )

    
    uidOrganisationIdCategorie = property(__uidOrganisationIdCategorie.value, __uidOrganisationIdCategorie.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0097/2}uidOrganisationId uses Python identifier uidOrganisationId
    __uidOrganisationId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uidOrganisationId'), 'uidOrganisationId', '__httpwww_ech_chxmlnseCH_00972_uidStructureType_httpwww_ech_chxmlnseCH_00972uidOrganisationId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 43, 3), )

    
    uidOrganisationId = property(__uidOrganisationId.value, __uidOrganisationId.set, None, None)

    _ElementMap.update({
        __uidOrganisationIdCategorie.name() : __uidOrganisationIdCategorie,
        __uidOrganisationId.name() : __uidOrganisationId
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.uidStructureType = uidStructureType
Namespace.addCategoryObject('typeBinding', 'uidStructureType', uidStructureType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 76, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0097/2}organisationIdentification uses Python identifier organisationIdentification
    __organisationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification'), 'organisationIdentification', '__httpwww_ech_chxmlnseCH_00972_CTD_ANON_httpwww_ech_chxmlnseCH_00972organisationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 78, 4), )

    
    organisationIdentification = property(__organisationIdentification.value, __organisationIdentification.set, None, None)

    _ElementMap.update({
        __organisationIdentification.name() : __organisationIdentification
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


organisationIdentificationRoot = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentificationRoot'), CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 75, 1))
Namespace.addCategoryObject('elementBinding', organisationIdentificationRoot.name().localName(), organisationIdentificationRoot)



organisationIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uid'), uidStructureType, scope=organisationIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 12, 3)))

organisationIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localOrganisationId'), namedOrganisationIdType, scope=organisationIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 13, 3)))

organisationIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OtherOrganisationId'), namedOrganisationIdType, scope=organisationIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 14, 3)))

organisationIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'organisationName'), organisationNameType, scope=organisationIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 15, 3)))

organisationIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'organisationLegalName'), organisationNameType, scope=organisationIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 16, 3)))

organisationIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'organisationAdditionalName'), organisationNameType, scope=organisationIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 17, 3)))

organisationIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'legalForm'), legalFormType, scope=organisationIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 18, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 12, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 14, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 16, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 17, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 18, 3))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(organisationIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uid')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 12, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(organisationIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localOrganisationId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 13, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(organisationIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OtherOrganisationId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 14, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(organisationIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'organisationName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 15, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(organisationIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'organisationLegalName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 16, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(organisationIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'organisationAdditionalName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 17, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(organisationIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'legalForm')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 18, 3))
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
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
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
organisationIdentificationType._Automaton = _BuildAutomaton()




namedOrganisationIdType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'organisationIdCategory'), STD_ANON_, scope=namedOrganisationIdType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 23, 3)))

namedOrganisationIdType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'organisationId'), STD_ANON, scope=namedOrganisationIdType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 30, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(namedOrganisationIdType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'organisationIdCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 23, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(namedOrganisationIdType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'organisationId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 30, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
namedOrganisationIdType._Automaton = _BuildAutomaton_()




uidStructureType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uidOrganisationIdCategorie'), uidOrganisationIdCategorieType, scope=uidStructureType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 42, 3)))

uidStructureType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uidOrganisationId'), uidOrganisationIdType, scope=uidStructureType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 43, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(uidStructureType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uidOrganisationIdCategorie')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 42, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(uidStructureType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uidOrganisationId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 43, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
uidStructureType._Automaton = _BuildAutomaton_2()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification'), organisationIdentificationType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 78, 4)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0097_2_0.xsd', 78, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_3()

