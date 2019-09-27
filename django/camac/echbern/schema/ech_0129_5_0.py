# ../../camac/echbern/schema/ech_0129_5_0.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:8aa2a70b6dec836410fe085a0be6dafa39fa1a96
# Generated 2019-09-26 17:57:08.877275 by PyXB version 1.2.6 using Python 3.6.8.final.0
# Namespace http://www.ech.ch/xmlns/eCH-0129/5 [xmlns:eCH-0129]

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
import camac.echbern.schema.ech_0044_4_1 as _ImportedBinding_camac_echbern_schema_ech_0044_4_1
import camac.echbern.schema.ech_0097_2_0 as _ImportedBinding_camac_echbern_schema_ech_0097_2_0
import camac.echbern.schema.ech_0007_6_0 as _ImportedBinding_camac_echbern_schema_ech_0007_6_0
import camac.echbern.schema.ech_0008_3_0 as _ImportedBinding_camac_echbern_schema_ech_0008_3_0
import camac.echbern.schema.ech_0010_6_0 as _ImportedBinding_camac_echbern_schema_ech_0010_6_0

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.ech.ch/xmlns/eCH-0129/5', create_if_missing=True)
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


# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}longDescriptionType
class longDescriptionType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'longDescriptionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 10, 1)
    _Documentation = None
longDescriptionType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
longDescriptionType._InitializeFacetMap(longDescriptionType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'longDescriptionType', longDescriptionType)
_module_typeBindings.longDescriptionType = longDescriptionType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}shortDescriptionType
class shortDescriptionType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'shortDescriptionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 15, 1)
    _Documentation = None
shortDescriptionType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(40))
shortDescriptionType._InitializeFacetMap(shortDescriptionType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'shortDescriptionType', shortDescriptionType)
_module_typeBindings.shortDescriptionType = shortDescriptionType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}freeTextType
class freeTextType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'freeTextType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 20, 1)
    _Documentation = None
freeTextType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
freeTextType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(32))
freeTextType._InitializeFacetMap(freeTextType._CF_minLength,
   freeTextType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'freeTextType', freeTextType)
_module_typeBindings.freeTextType = freeTextType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}phoneNumberType
class phoneNumberType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'phoneNumberType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 26, 1)
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

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}emailAddressType
class emailAddressType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'emailAddressType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 33, 1)
    _Documentation = None
emailAddressType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
emailAddressType._CF_pattern = pyxb.binding.facets.CF_pattern()
emailAddressType._CF_pattern.addPattern(pattern="[A-Za-zäöüÄÖÜàáâãåæçèéêëìíîïðñòóôõøùúûýþÿ0-9!#-'\\*\\+\\-/=\\?\\^_`\\{-~]+(\\.[A-Za-zäöüÄÖÜàáâãåæçèéêëìíîïðñòóôõøùúûýþÿ0-9!#-'\\*\\+\\-/=\\?\\^_`\\{-~]+)*@[A-Za-zäöüÄÖÜàáâãåæçèéêëìíîïðñòóôõøùúûýþÿ0-9!#-'\\*\\+\\-/=\\?\\^_`\\{-~]+(\\.[A-Za-zäöüÄÖÜàáâãåæçèéêëìíîïðñòóôõøùúûýþÿ0-9!#-'\\*\\+\\-/=\\?\\^_`\\{-~]+)*")
emailAddressType._CF_whiteSpace = pyxb.binding.facets.CF_whiteSpace(value=pyxb.binding.facets._WhiteSpace_enum.collapse)
emailAddressType._InitializeFacetMap(emailAddressType._CF_maxLength,
   emailAddressType._CF_pattern,
   emailAddressType._CF_whiteSpace)
Namespace.addCategoryObject('typeBinding', 'emailAddressType', emailAddressType)
_module_typeBindings.emailAddressType = emailAddressType

# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 43, 4)
    _Documentation = None
STD_ANON._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
STD_ANON._InitializeFacetMap(STD_ANON._CF_minLength,
   STD_ANON._CF_maxLength)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 51, 4)
    _Documentation = None
STD_ANON_._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_minLength)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}iDCategoryType
class iDCategoryType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'iDCategoryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 59, 1)
    _Documentation = None
iDCategoryType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
iDCategoryType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
iDCategoryType._InitializeFacetMap(iDCategoryType._CF_minLength,
   iDCategoryType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'iDCategoryType', iDCategoryType)
_module_typeBindings.iDCategoryType = iDCategoryType

# Atomic simple type: [anonymous]
class STD_ANON_2 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 75, 4)
    _Documentation = None
STD_ANON_2._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON_2._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_minLength,
   STD_ANON_2._CF_maxLength)
_module_typeBindings.STD_ANON_2 = STD_ANON_2

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}withdrawalDateType
class withdrawalDateType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'withdrawalDateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 91, 1)
    _Documentation = None
withdrawalDateType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=withdrawalDateType, value=pyxb.binding.datatypes.date('2000-01-01'))
withdrawalDateType._InitializeFacetMap(withdrawalDateType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'withdrawalDateType', withdrawalDateType)
_module_typeBindings.withdrawalDateType = withdrawalDateType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}originOfCoordinatesType
class originOfCoordinatesType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'originOfCoordinatesType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 96, 1)
    _Documentation = None
originOfCoordinatesType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=originOfCoordinatesType, enum_prefix=None)
originOfCoordinatesType._CF_enumeration.addEnumeration(unicode_value='901', tag=None)
originOfCoordinatesType._CF_enumeration.addEnumeration(unicode_value='902', tag=None)
originOfCoordinatesType._CF_enumeration.addEnumeration(unicode_value='903', tag=None)
originOfCoordinatesType._CF_enumeration.addEnumeration(unicode_value='904', tag=None)
originOfCoordinatesType._CF_enumeration.addEnumeration(unicode_value='905', tag=None)
originOfCoordinatesType._CF_enumeration.addEnumeration(unicode_value='906', tag=None)
originOfCoordinatesType._CF_enumeration.addEnumeration(unicode_value='909', tag=None)
originOfCoordinatesType._InitializeFacetMap(originOfCoordinatesType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'originOfCoordinatesType', originOfCoordinatesType)
_module_typeBindings.originOfCoordinatesType = originOfCoordinatesType

# Atomic simple type: [anonymous]
class STD_ANON_3 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 113, 7)
    _Documentation = None
STD_ANON_3._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_3, value=pyxb.binding.datatypes.decimal('2480000.0'))
STD_ANON_3._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON_3, value=pyxb.binding.datatypes.decimal('2840000.999'))
STD_ANON_3._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(10))
STD_ANON_3._CF_fractionDigits = pyxb.binding.facets.CF_fractionDigits(value=pyxb.binding.datatypes.nonNegativeInteger(3))
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_minInclusive,
   STD_ANON_3._CF_maxInclusive,
   STD_ANON_3._CF_totalDigits,
   STD_ANON_3._CF_fractionDigits)
_module_typeBindings.STD_ANON_3 = STD_ANON_3

# Atomic simple type: [anonymous]
class STD_ANON_4 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 123, 7)
    _Documentation = None
STD_ANON_4._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_4, value=pyxb.binding.datatypes.decimal('1070000.0'))
STD_ANON_4._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON_4, value=pyxb.binding.datatypes.decimal('1300000.999'))
STD_ANON_4._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(10))
STD_ANON_4._CF_fractionDigits = pyxb.binding.facets.CF_fractionDigits(value=pyxb.binding.datatypes.nonNegativeInteger(3))
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_minInclusive,
   STD_ANON_4._CF_maxInclusive,
   STD_ANON_4._CF_totalDigits,
   STD_ANON_4._CF_fractionDigits)
_module_typeBindings.STD_ANON_4 = STD_ANON_4

# Atomic simple type: [anonymous]
class STD_ANON_5 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 140, 7)
    _Documentation = None
STD_ANON_5._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_5, value=pyxb.binding.datatypes.decimal('480000.0'))
STD_ANON_5._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON_5, value=pyxb.binding.datatypes.decimal('840000.999'))
STD_ANON_5._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(9))
STD_ANON_5._CF_fractionDigits = pyxb.binding.facets.CF_fractionDigits(value=pyxb.binding.datatypes.nonNegativeInteger(3))
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_minInclusive,
   STD_ANON_5._CF_maxInclusive,
   STD_ANON_5._CF_totalDigits,
   STD_ANON_5._CF_fractionDigits)
_module_typeBindings.STD_ANON_5 = STD_ANON_5

# Atomic simple type: [anonymous]
class STD_ANON_6 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 150, 7)
    _Documentation = None
STD_ANON_6._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_6, value=pyxb.binding.datatypes.decimal('70000.0'))
STD_ANON_6._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON_6, value=pyxb.binding.datatypes.decimal('300000.999'))
STD_ANON_6._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(9))
STD_ANON_6._CF_fractionDigits = pyxb.binding.facets.CF_fractionDigits(value=pyxb.binding.datatypes.nonNegativeInteger(3))
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_minInclusive,
   STD_ANON_6._CF_maxInclusive,
   STD_ANON_6._CF_totalDigits,
   STD_ANON_6._CF_fractionDigits)
_module_typeBindings.STD_ANON_6 = STD_ANON_6

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}officialConstructionProjectFileNoType
class officialConstructionProjectFileNoType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'officialConstructionProjectFileNoType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 165, 1)
    _Documentation = None
officialConstructionProjectFileNoType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
officialConstructionProjectFileNoType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(15))
officialConstructionProjectFileNoType._InitializeFacetMap(officialConstructionProjectFileNoType._CF_minLength,
   officialConstructionProjectFileNoType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'officialConstructionProjectFileNoType', officialConstructionProjectFileNoType)
_module_typeBindings.officialConstructionProjectFileNoType = officialConstructionProjectFileNoType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}extensionOfOfficialConstructionProjectFileNoType
class extensionOfOfficialConstructionProjectFileNoType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'extensionOfOfficialConstructionProjectFileNoType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 171, 1)
    _Documentation = None
extensionOfOfficialConstructionProjectFileNoType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=extensionOfOfficialConstructionProjectFileNoType, value=pyxb.binding.datatypes.nonNegativeInteger(0))
extensionOfOfficialConstructionProjectFileNoType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=extensionOfOfficialConstructionProjectFileNoType, value=pyxb.binding.datatypes.nonNegativeInteger(99))
extensionOfOfficialConstructionProjectFileNoType._InitializeFacetMap(extensionOfOfficialConstructionProjectFileNoType._CF_minInclusive,
   extensionOfOfficialConstructionProjectFileNoType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'extensionOfOfficialConstructionProjectFileNoType', extensionOfOfficialConstructionProjectFileNoType)
_module_typeBindings.extensionOfOfficialConstructionProjectFileNoType = extensionOfOfficialConstructionProjectFileNoType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}typeOfConstructionProjectType
class typeOfConstructionProjectType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeOfConstructionProjectType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 177, 1)
    _Documentation = None
typeOfConstructionProjectType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=typeOfConstructionProjectType, enum_prefix=None)
typeOfConstructionProjectType._CF_enumeration.addEnumeration(unicode_value='6010', tag=None)
typeOfConstructionProjectType._CF_enumeration.addEnumeration(unicode_value='6011', tag=None)
typeOfConstructionProjectType._InitializeFacetMap(typeOfConstructionProjectType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'typeOfConstructionProjectType', typeOfConstructionProjectType)
_module_typeBindings.typeOfConstructionProjectType = typeOfConstructionProjectType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}typeOfPermitType
class typeOfPermitType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeOfPermitType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 190, 1)
    _Documentation = None
typeOfPermitType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=typeOfPermitType, enum_prefix=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5000', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5001', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5002', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5003', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5004', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5005', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5006', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5007', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5008', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5009', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5011', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5012', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5015', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5021', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5022', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5023', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5031', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5041', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5043', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5044', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5051', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5061', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5062', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5063', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5064', tag=None)
typeOfPermitType._CF_enumeration.addEnumeration(unicode_value='5071', tag=None)
typeOfPermitType._InitializeFacetMap(typeOfPermitType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'typeOfPermitType', typeOfPermitType)
_module_typeBindings.typeOfPermitType = typeOfPermitType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}projectStartDateType
class projectStartDateType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'projectStartDateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 220, 1)
    _Documentation = None
projectStartDateType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=projectStartDateType, value=pyxb.binding.datatypes.date('2000-01-01'))
projectStartDateType._InitializeFacetMap(projectStartDateType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'projectStartDateType', projectStartDateType)
_module_typeBindings.projectStartDateType = projectStartDateType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}projectCancellationDateType
class projectCancellationDateType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'projectCancellationDateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 225, 1)
    _Documentation = None
projectCancellationDateType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'projectCancellationDateType', projectCancellationDateType)
_module_typeBindings.projectCancellationDateType = projectCancellationDateType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}constructionAuthorisationDeniedDateType
class constructionAuthorisationDeniedDateType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'constructionAuthorisationDeniedDateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 228, 1)
    _Documentation = None
constructionAuthorisationDeniedDateType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=constructionAuthorisationDeniedDateType, value=pyxb.binding.datatypes.date('2000-01-01'))
constructionAuthorisationDeniedDateType._InitializeFacetMap(constructionAuthorisationDeniedDateType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'constructionAuthorisationDeniedDateType', constructionAuthorisationDeniedDateType)
_module_typeBindings.constructionAuthorisationDeniedDateType = constructionAuthorisationDeniedDateType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}buildingPermitIssueDateType
class buildingPermitIssueDateType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingPermitIssueDateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 233, 1)
    _Documentation = None
buildingPermitIssueDateType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=buildingPermitIssueDateType, value=pyxb.binding.datatypes.date('2000-01-01'))
buildingPermitIssueDateType._InitializeFacetMap(buildingPermitIssueDateType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'buildingPermitIssueDateType', buildingPermitIssueDateType)
_module_typeBindings.buildingPermitIssueDateType = buildingPermitIssueDateType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}projectAnnouncementDateType
class projectAnnouncementDateType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'projectAnnouncementDateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 238, 1)
    _Documentation = None
projectAnnouncementDateType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=projectAnnouncementDateType, value=pyxb.binding.datatypes.date('2000-01-01'))
projectAnnouncementDateType._InitializeFacetMap(projectAnnouncementDateType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'projectAnnouncementDateType', projectAnnouncementDateType)
_module_typeBindings.projectAnnouncementDateType = projectAnnouncementDateType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}projectCompletionDateType
class projectCompletionDateType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'projectCompletionDateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 243, 1)
    _Documentation = None
projectCompletionDateType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=projectCompletionDateType, value=pyxb.binding.datatypes.date('2000-01-01'))
projectCompletionDateType._InitializeFacetMap(projectCompletionDateType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'projectCompletionDateType', projectCompletionDateType)
_module_typeBindings.projectCompletionDateType = projectCompletionDateType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}projectSuspensionDateType
class projectSuspensionDateType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'projectSuspensionDateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 248, 1)
    _Documentation = None
projectSuspensionDateType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=projectSuspensionDateType, value=pyxb.binding.datatypes.date('2000-01-01'))
projectSuspensionDateType._InitializeFacetMap(projectSuspensionDateType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'projectSuspensionDateType', projectSuspensionDateType)
_module_typeBindings.projectSuspensionDateType = projectSuspensionDateType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}nonRealisationDateType
class nonRealisationDateType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'nonRealisationDateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 253, 1)
    _Documentation = None
nonRealisationDateType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=nonRealisationDateType, value=pyxb.binding.datatypes.date('2000-01-01'))
nonRealisationDateType._InitializeFacetMap(nonRealisationDateType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'nonRealisationDateType', nonRealisationDateType)
_module_typeBindings.nonRealisationDateType = nonRealisationDateType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}durationOfConstructionPhaseType
class durationOfConstructionPhaseType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'durationOfConstructionPhaseType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 258, 1)
    _Documentation = None
durationOfConstructionPhaseType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=durationOfConstructionPhaseType, value=pyxb.binding.datatypes.nonNegativeInteger(1))
durationOfConstructionPhaseType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=durationOfConstructionPhaseType, value=pyxb.binding.datatypes.nonNegativeInteger(999))
durationOfConstructionPhaseType._InitializeFacetMap(durationOfConstructionPhaseType._CF_minInclusive,
   durationOfConstructionPhaseType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'durationOfConstructionPhaseType', durationOfConstructionPhaseType)
_module_typeBindings.durationOfConstructionPhaseType = durationOfConstructionPhaseType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}EPROIDType
class EPROIDType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EPROIDType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 264, 1)
    _Documentation = None
EPROIDType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=EPROIDType, value=pyxb.binding.datatypes.nonNegativeInteger(1))
EPROIDType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=EPROIDType, value=pyxb.binding.datatypes.nonNegativeInteger(900000000))
EPROIDType._InitializeFacetMap(EPROIDType._CF_minInclusive,
   EPROIDType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'EPROIDType', EPROIDType)
_module_typeBindings.EPROIDType = EPROIDType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}totalCostsOfProjectType
class totalCostsOfProjectType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'totalCostsOfProjectType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 270, 1)
    _Documentation = None
totalCostsOfProjectType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=totalCostsOfProjectType, value=pyxb.binding.datatypes.nonNegativeInteger(1000))
totalCostsOfProjectType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=totalCostsOfProjectType, value=pyxb.binding.datatypes.nonNegativeInteger(999999999000))
totalCostsOfProjectType._InitializeFacetMap(totalCostsOfProjectType._CF_minInclusive,
   totalCostsOfProjectType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'totalCostsOfProjectType', totalCostsOfProjectType)
_module_typeBindings.totalCostsOfProjectType = totalCostsOfProjectType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}projectStatusType
class projectStatusType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'projectStatusType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 276, 1)
    _Documentation = None
projectStatusType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=projectStatusType, enum_prefix=None)
projectStatusType._CF_enumeration.addEnumeration(unicode_value='6701', tag=None)
projectStatusType._CF_enumeration.addEnumeration(unicode_value='6702', tag=None)
projectStatusType._CF_enumeration.addEnumeration(unicode_value='6703', tag=None)
projectStatusType._CF_enumeration.addEnumeration(unicode_value='6704', tag=None)
projectStatusType._CF_enumeration.addEnumeration(unicode_value='6706', tag=None)
projectStatusType._CF_enumeration.addEnumeration(unicode_value='6707', tag=None)
projectStatusType._CF_enumeration.addEnumeration(unicode_value='6708', tag=None)
projectStatusType._CF_enumeration.addEnumeration(unicode_value='6709', tag=None)
projectStatusType._InitializeFacetMap(projectStatusType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'projectStatusType', projectStatusType)
_module_typeBindings.projectStatusType = projectStatusType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}typeOfClientType
class typeOfClientType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeOfClientType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 288, 1)
    _Documentation = None
typeOfClientType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=typeOfClientType, enum_prefix=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6101', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6103', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6104', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6107', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6108', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6110', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6111', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6115', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6116', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6121', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6122', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6123', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6124', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6131', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6132', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6133', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6141', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6142', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6143', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6161', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6151', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6152', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6162', tag=None)
typeOfClientType._CF_enumeration.addEnumeration(unicode_value='6163', tag=None)
typeOfClientType._InitializeFacetMap(typeOfClientType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'typeOfClientType', typeOfClientType)
_module_typeBindings.typeOfClientType = typeOfClientType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}typeOfConstructionType
class typeOfConstructionType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeOfConstructionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 316, 1)
    _Documentation = None
typeOfConstructionType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=typeOfConstructionType, enum_prefix=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6211', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6212', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6213', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6214', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6219', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6221', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6222', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6223', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6231', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6232', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6233', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6234', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6235', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6241', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6242', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6243', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6244', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6245', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6249', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6251', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6252', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6253', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6254', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6255', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6256', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6257', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6258', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6259', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6261', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6262', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6269', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6271', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6272', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6273', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6274', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6276', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6278', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6279', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6281', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6282', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6283', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6291', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6292', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6293', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6294', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6295', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6296', tag=None)
typeOfConstructionType._CF_enumeration.addEnumeration(unicode_value='6299', tag=None)
typeOfConstructionType._InitializeFacetMap(typeOfConstructionType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'typeOfConstructionType', typeOfConstructionType)
_module_typeBindings.typeOfConstructionType = typeOfConstructionType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}constructionProjectDescriptionType
class constructionProjectDescriptionType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'constructionProjectDescriptionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 368, 1)
    _Documentation = None
constructionProjectDescriptionType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(3))
constructionProjectDescriptionType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(1000))
constructionProjectDescriptionType._InitializeFacetMap(constructionProjectDescriptionType._CF_minLength,
   constructionProjectDescriptionType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'constructionProjectDescriptionType', constructionProjectDescriptionType)
_module_typeBindings.constructionProjectDescriptionType = constructionProjectDescriptionType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}numberOfConcernedBuildingsType
class numberOfConcernedBuildingsType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'numberOfConcernedBuildingsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 374, 1)
    _Documentation = None
numberOfConcernedBuildingsType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=numberOfConcernedBuildingsType, value=pyxb.binding.datatypes.nonNegativeInteger(1))
numberOfConcernedBuildingsType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=numberOfConcernedBuildingsType, value=pyxb.binding.datatypes.nonNegativeInteger(999))
numberOfConcernedBuildingsType._InitializeFacetMap(numberOfConcernedBuildingsType._CF_minInclusive,
   numberOfConcernedBuildingsType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'numberOfConcernedBuildingsType', numberOfConcernedBuildingsType)
_module_typeBindings.numberOfConcernedBuildingsType = numberOfConcernedBuildingsType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}numberOfConcernedDwellingsType
class numberOfConcernedDwellingsType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'numberOfConcernedDwellingsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 380, 1)
    _Documentation = None
numberOfConcernedDwellingsType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=numberOfConcernedDwellingsType, value=pyxb.binding.datatypes.nonNegativeInteger(1))
numberOfConcernedDwellingsType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=numberOfConcernedDwellingsType, value=pyxb.binding.datatypes.nonNegativeInteger(999))
numberOfConcernedDwellingsType._InitializeFacetMap(numberOfConcernedDwellingsType._CF_minInclusive,
   numberOfConcernedDwellingsType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'numberOfConcernedDwellingsType', numberOfConcernedDwellingsType)
_module_typeBindings.numberOfConcernedDwellingsType = numberOfConcernedDwellingsType

# Atomic simple type: [anonymous]
class STD_ANON_7 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 437, 8)
    _Documentation = None
STD_ANON_7._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON_7._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
STD_ANON_7._InitializeFacetMap(STD_ANON_7._CF_minLength,
   STD_ANON_7._CF_maxLength)
_module_typeBindings.STD_ANON_7 = STD_ANON_7

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}periodOfConstructionType
class periodOfConstructionType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'periodOfConstructionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 454, 1)
    _Documentation = None
periodOfConstructionType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=periodOfConstructionType, enum_prefix=None)
periodOfConstructionType._CF_enumeration.addEnumeration(unicode_value='8011', tag=None)
periodOfConstructionType._CF_enumeration.addEnumeration(unicode_value='8012', tag=None)
periodOfConstructionType._CF_enumeration.addEnumeration(unicode_value='8013', tag=None)
periodOfConstructionType._CF_enumeration.addEnumeration(unicode_value='8014', tag=None)
periodOfConstructionType._CF_enumeration.addEnumeration(unicode_value='8015', tag=None)
periodOfConstructionType._CF_enumeration.addEnumeration(unicode_value='8016', tag=None)
periodOfConstructionType._CF_enumeration.addEnumeration(unicode_value='8017', tag=None)
periodOfConstructionType._CF_enumeration.addEnumeration(unicode_value='8018', tag=None)
periodOfConstructionType._CF_enumeration.addEnumeration(unicode_value='8019', tag=None)
periodOfConstructionType._CF_enumeration.addEnumeration(unicode_value='8020', tag=None)
periodOfConstructionType._CF_enumeration.addEnumeration(unicode_value='8021', tag=None)
periodOfConstructionType._CF_enumeration.addEnumeration(unicode_value='8022', tag=None)
periodOfConstructionType._CF_enumeration.addEnumeration(unicode_value='8023', tag=None)
periodOfConstructionType._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(4))
periodOfConstructionType._InitializeFacetMap(periodOfConstructionType._CF_enumeration,
   periodOfConstructionType._CF_totalDigits)
Namespace.addCategoryObject('typeBinding', 'periodOfConstructionType', periodOfConstructionType)
_module_typeBindings.periodOfConstructionType = periodOfConstructionType

# Atomic simple type: [anonymous]
class STD_ANON_8 (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 475, 4)
    _Documentation = None
STD_ANON_8._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_8, value=pyxb.binding.datatypes.date('1000-01-01'))
STD_ANON_8._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON_8, value=pyxb.binding.datatypes.date('2099-12-31'))
STD_ANON_8._InitializeFacetMap(STD_ANON_8._CF_minInclusive,
   STD_ANON_8._CF_maxInclusive)
_module_typeBindings.STD_ANON_8 = STD_ANON_8

# Atomic simple type: [anonymous]
class STD_ANON_9 (pyxb.binding.datatypes.gYearMonth):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 483, 4)
    _Documentation = None
STD_ANON_9._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_9, value=pyxb.binding.datatypes.gYearMonth('1000-01'))
STD_ANON_9._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON_9, value=pyxb.binding.datatypes.gYearMonth('2099-12'))
STD_ANON_9._InitializeFacetMap(STD_ANON_9._CF_minInclusive,
   STD_ANON_9._CF_maxInclusive)
_module_typeBindings.STD_ANON_9 = STD_ANON_9

# Atomic simple type: [anonymous]
class STD_ANON_10 (pyxb.binding.datatypes.gYear):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 491, 4)
    _Documentation = None
STD_ANON_10._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_10, value=pyxb.binding.datatypes.gYear('1000'))
STD_ANON_10._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON_10, value=pyxb.binding.datatypes.gYear('2099'))
STD_ANON_10._InitializeFacetMap(STD_ANON_10._CF_minInclusive,
   STD_ANON_10._CF_maxInclusive)
_module_typeBindings.STD_ANON_10 = STD_ANON_10

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}localCodeType
class localCodeType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'localCodeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 501, 1)
    _Documentation = None
localCodeType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
localCodeType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(8))
localCodeType._InitializeFacetMap(localCodeType._CF_minLength,
   localCodeType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'localCodeType', localCodeType)
_module_typeBindings.localCodeType = localCodeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}officialBuildingNoType
class officialBuildingNoType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'officialBuildingNoType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 507, 1)
    _Documentation = None
officialBuildingNoType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
officialBuildingNoType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
officialBuildingNoType._InitializeFacetMap(officialBuildingNoType._CF_minLength,
   officialBuildingNoType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'officialBuildingNoType', officialBuildingNoType)
_module_typeBindings.officialBuildingNoType = officialBuildingNoType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}numberOfFloorsType
class numberOfFloorsType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'numberOfFloorsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 513, 1)
    _Documentation = None
numberOfFloorsType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=numberOfFloorsType, value=pyxb.binding.datatypes.nonNegativeInteger(1))
numberOfFloorsType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=numberOfFloorsType, value=pyxb.binding.datatypes.nonNegativeInteger(99))
numberOfFloorsType._InitializeFacetMap(numberOfFloorsType._CF_minInclusive,
   numberOfFloorsType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'numberOfFloorsType', numberOfFloorsType)
_module_typeBindings.numberOfFloorsType = numberOfFloorsType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}numberOfSeparateHabitableRoomsType
class numberOfSeparateHabitableRoomsType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'numberOfSeparateHabitableRoomsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 519, 1)
    _Documentation = None
numberOfSeparateHabitableRoomsType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=numberOfSeparateHabitableRoomsType, value=pyxb.binding.datatypes.nonNegativeInteger(0))
numberOfSeparateHabitableRoomsType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=numberOfSeparateHabitableRoomsType, value=pyxb.binding.datatypes.nonNegativeInteger(999))
numberOfSeparateHabitableRoomsType._InitializeFacetMap(numberOfSeparateHabitableRoomsType._CF_minInclusive,
   numberOfSeparateHabitableRoomsType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'numberOfSeparateHabitableRoomsType', numberOfSeparateHabitableRoomsType)
_module_typeBindings.numberOfSeparateHabitableRoomsType = numberOfSeparateHabitableRoomsType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}EGIDType
class EGIDType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EGIDType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 525, 1)
    _Documentation = None
EGIDType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=EGIDType, value=pyxb.binding.datatypes.nonNegativeInteger(1))
EGIDType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=EGIDType, value=pyxb.binding.datatypes.nonNegativeInteger(900000000))
EGIDType._InitializeFacetMap(EGIDType._CF_minInclusive,
   EGIDType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'EGIDType', EGIDType)
_module_typeBindings.EGIDType = EGIDType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}nameOfBuildingType
class nameOfBuildingType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'nameOfBuildingType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 531, 1)
    _Documentation = None
nameOfBuildingType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(3))
nameOfBuildingType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(40))
nameOfBuildingType._InitializeFacetMap(nameOfBuildingType._CF_minLength,
   nameOfBuildingType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'nameOfBuildingType', nameOfBuildingType)
_module_typeBindings.nameOfBuildingType = nameOfBuildingType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}surfaceAreaOfBuildingType
class surfaceAreaOfBuildingType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfBuildingType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 537, 1)
    _Documentation = None
surfaceAreaOfBuildingType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=surfaceAreaOfBuildingType, value=pyxb.binding.datatypes.nonNegativeInteger(1))
surfaceAreaOfBuildingType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=surfaceAreaOfBuildingType, value=pyxb.binding.datatypes.nonNegativeInteger(99999))
surfaceAreaOfBuildingType._InitializeFacetMap(surfaceAreaOfBuildingType._CF_minInclusive,
   surfaceAreaOfBuildingType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'surfaceAreaOfBuildingType', surfaceAreaOfBuildingType)
_module_typeBindings.surfaceAreaOfBuildingType = surfaceAreaOfBuildingType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}surfaceAreaOfBuildingSingleObjectType
class surfaceAreaOfBuildingSingleObjectType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfBuildingSingleObjectType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 543, 1)
    _Documentation = None
surfaceAreaOfBuildingSingleObjectType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=surfaceAreaOfBuildingSingleObjectType, value=pyxb.binding.datatypes.nonNegativeInteger(1))
surfaceAreaOfBuildingSingleObjectType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=surfaceAreaOfBuildingSingleObjectType, value=pyxb.binding.datatypes.nonNegativeInteger(99999))
surfaceAreaOfBuildingSingleObjectType._InitializeFacetMap(surfaceAreaOfBuildingSingleObjectType._CF_minInclusive,
   surfaceAreaOfBuildingSingleObjectType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'surfaceAreaOfBuildingSingleObjectType', surfaceAreaOfBuildingSingleObjectType)
_module_typeBindings.surfaceAreaOfBuildingSingleObjectType = surfaceAreaOfBuildingSingleObjectType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}buildingCategoryType
class buildingCategoryType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingCategoryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 549, 1)
    _Documentation = None
buildingCategoryType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=buildingCategoryType, enum_prefix=None)
buildingCategoryType._CF_enumeration.addEnumeration(unicode_value='1010', tag=None)
buildingCategoryType._CF_enumeration.addEnumeration(unicode_value='1020', tag=None)
buildingCategoryType._CF_enumeration.addEnumeration(unicode_value='1030', tag=None)
buildingCategoryType._CF_enumeration.addEnumeration(unicode_value='1040', tag=None)
buildingCategoryType._CF_enumeration.addEnumeration(unicode_value='1060', tag=None)
buildingCategoryType._CF_enumeration.addEnumeration(unicode_value='1080', tag=None)
buildingCategoryType._InitializeFacetMap(buildingCategoryType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'buildingCategoryType', buildingCategoryType)
_module_typeBindings.buildingCategoryType = buildingCategoryType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}buildingClassType
class buildingClassType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingClassType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 559, 1)
    _Documentation = None
buildingClassType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=buildingClassType, value=pyxb.binding.datatypes.nonNegativeInteger(1110))
buildingClassType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=buildingClassType, value=pyxb.binding.datatypes.nonNegativeInteger(1278))
buildingClassType._InitializeFacetMap(buildingClassType._CF_minInclusive,
   buildingClassType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'buildingClassType', buildingClassType)
_module_typeBindings.buildingClassType = buildingClassType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}buildingStatusType
class buildingStatusType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingStatusType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 565, 1)
    _Documentation = None
buildingStatusType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=buildingStatusType, enum_prefix=None)
buildingStatusType._CF_enumeration.addEnumeration(unicode_value='1001', tag=None)
buildingStatusType._CF_enumeration.addEnumeration(unicode_value='1002', tag=None)
buildingStatusType._CF_enumeration.addEnumeration(unicode_value='1003', tag=None)
buildingStatusType._CF_enumeration.addEnumeration(unicode_value='1004', tag=None)
buildingStatusType._CF_enumeration.addEnumeration(unicode_value='1005', tag=None)
buildingStatusType._CF_enumeration.addEnumeration(unicode_value='1007', tag=None)
buildingStatusType._CF_enumeration.addEnumeration(unicode_value='1008', tag=None)
buildingStatusType._CF_enumeration.addEnumeration(unicode_value='1009', tag=None)
buildingStatusType._InitializeFacetMap(buildingStatusType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'buildingStatusType', buildingStatusType)
_module_typeBindings.buildingStatusType = buildingStatusType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}buildingInsuranceNumberType
class buildingInsuranceNumberType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingInsuranceNumberType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 577, 1)
    _Documentation = None
buildingInsuranceNumberType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'buildingInsuranceNumberType', buildingInsuranceNumberType)
_module_typeBindings.buildingInsuranceNumberType = buildingInsuranceNumberType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}neighbourhoodType
class neighbourhoodType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'neighbourhoodType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 580, 1)
    _Documentation = None
neighbourhoodType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=neighbourhoodType, value=pyxb.binding.datatypes.nonNegativeInteger(1000))
neighbourhoodType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=neighbourhoodType, value=pyxb.binding.datatypes.nonNegativeInteger(9999999))
neighbourhoodType._InitializeFacetMap(neighbourhoodType._CF_minInclusive,
   neighbourhoodType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'neighbourhoodType', neighbourhoodType)
_module_typeBindings.neighbourhoodType = neighbourhoodType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}energyRelevantSurfaceType
class energyRelevantSurfaceType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'energyRelevantSurfaceType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 586, 1)
    _Documentation = None
energyRelevantSurfaceType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=energyRelevantSurfaceType, value=pyxb.binding.datatypes.nonNegativeInteger(5))
energyRelevantSurfaceType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=energyRelevantSurfaceType, value=pyxb.binding.datatypes.nonNegativeInteger(900000))
energyRelevantSurfaceType._InitializeFacetMap(energyRelevantSurfaceType._CF_minInclusive,
   energyRelevantSurfaceType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'energyRelevantSurfaceType', energyRelevantSurfaceType)
_module_typeBindings.energyRelevantSurfaceType = energyRelevantSurfaceType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}buildingVolumeInformationSourceType
class buildingVolumeInformationSourceType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingVolumeInformationSourceType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 592, 1)
    _Documentation = None
buildingVolumeInformationSourceType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=buildingVolumeInformationSourceType, enum_prefix=None)
buildingVolumeInformationSourceType._CF_enumeration.addEnumeration(unicode_value='869', tag=None)
buildingVolumeInformationSourceType._CF_enumeration.addEnumeration(unicode_value='858', tag=None)
buildingVolumeInformationSourceType._CF_enumeration.addEnumeration(unicode_value='853', tag=None)
buildingVolumeInformationSourceType._CF_enumeration.addEnumeration(unicode_value='852', tag=None)
buildingVolumeInformationSourceType._CF_enumeration.addEnumeration(unicode_value='857', tag=None)
buildingVolumeInformationSourceType._CF_enumeration.addEnumeration(unicode_value='851', tag=None)
buildingVolumeInformationSourceType._CF_enumeration.addEnumeration(unicode_value='870', tag=None)
buildingVolumeInformationSourceType._CF_enumeration.addEnumeration(unicode_value='878', tag=None)
buildingVolumeInformationSourceType._CF_enumeration.addEnumeration(unicode_value='859', tag=None)
buildingVolumeInformationSourceType._InitializeFacetMap(buildingVolumeInformationSourceType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'buildingVolumeInformationSourceType', buildingVolumeInformationSourceType)
_module_typeBindings.buildingVolumeInformationSourceType = buildingVolumeInformationSourceType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}buildingVolumeNormType
class buildingVolumeNormType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingVolumeNormType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 605, 1)
    _Documentation = None
buildingVolumeNormType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=buildingVolumeNormType, enum_prefix=None)
buildingVolumeNormType._CF_enumeration.addEnumeration(unicode_value='961', tag=None)
buildingVolumeNormType._CF_enumeration.addEnumeration(unicode_value='962', tag=None)
buildingVolumeNormType._CF_enumeration.addEnumeration(unicode_value='969', tag=None)
buildingVolumeNormType._InitializeFacetMap(buildingVolumeNormType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'buildingVolumeNormType', buildingVolumeNormType)
_module_typeBindings.buildingVolumeNormType = buildingVolumeNormType

# Atomic simple type: [anonymous]
class STD_ANON_11 (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 615, 4)
    _Documentation = None
STD_ANON_11._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_11, value=pyxb.binding.datatypes.nonNegativeInteger(5))
STD_ANON_11._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON_11, value=pyxb.binding.datatypes.nonNegativeInteger(9999999))
STD_ANON_11._InitializeFacetMap(STD_ANON_11._CF_minInclusive,
   STD_ANON_11._CF_maxInclusive)
_module_typeBindings.STD_ANON_11 = STD_ANON_11

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}heatGeneratorHeatingType
class heatGeneratorHeatingType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'heatGeneratorHeatingType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 626, 1)
    _Documentation = None
heatGeneratorHeatingType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=heatGeneratorHeatingType, enum_prefix=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7400', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7410', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7411', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7420', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7421', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7430', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7431', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7432', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7433', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7434', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7435', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7436', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7440', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7441', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7450', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7451', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7452', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7460', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7461', tag=None)
heatGeneratorHeatingType._CF_enumeration.addEnumeration(unicode_value='7499', tag=None)
heatGeneratorHeatingType._InitializeFacetMap(heatGeneratorHeatingType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'heatGeneratorHeatingType', heatGeneratorHeatingType)
_module_typeBindings.heatGeneratorHeatingType = heatGeneratorHeatingType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}heatGeneratorHotWaterType
class heatGeneratorHotWaterType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'heatGeneratorHotWaterType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 650, 1)
    _Documentation = None
heatGeneratorHotWaterType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=heatGeneratorHotWaterType, enum_prefix=None)
heatGeneratorHotWaterType._CF_enumeration.addEnumeration(unicode_value='7600', tag=None)
heatGeneratorHotWaterType._CF_enumeration.addEnumeration(unicode_value='7610', tag=None)
heatGeneratorHotWaterType._CF_enumeration.addEnumeration(unicode_value='7620', tag=None)
heatGeneratorHotWaterType._CF_enumeration.addEnumeration(unicode_value='7630', tag=None)
heatGeneratorHotWaterType._CF_enumeration.addEnumeration(unicode_value='7632', tag=None)
heatGeneratorHotWaterType._CF_enumeration.addEnumeration(unicode_value='7634', tag=None)
heatGeneratorHotWaterType._CF_enumeration.addEnumeration(unicode_value='7640', tag=None)
heatGeneratorHotWaterType._CF_enumeration.addEnumeration(unicode_value='7650', tag=None)
heatGeneratorHotWaterType._CF_enumeration.addEnumeration(unicode_value='7651', tag=None)
heatGeneratorHotWaterType._CF_enumeration.addEnumeration(unicode_value='7660', tag=None)
heatGeneratorHotWaterType._CF_enumeration.addEnumeration(unicode_value='7699', tag=None)
heatGeneratorHotWaterType._InitializeFacetMap(heatGeneratorHotWaterType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'heatGeneratorHotWaterType', heatGeneratorHotWaterType)
_module_typeBindings.heatGeneratorHotWaterType = heatGeneratorHotWaterType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}thermotechnicalDeviceHeatingTypeType
class thermotechnicalDeviceHeatingTypeType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'thermotechnicalDeviceHeatingTypeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 665, 1)
    _Documentation = None
thermotechnicalDeviceHeatingTypeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=thermotechnicalDeviceHeatingTypeType, enum_prefix=None)
thermotechnicalDeviceHeatingTypeType._CF_enumeration.addEnumeration(unicode_value='7701', tag=None)
thermotechnicalDeviceHeatingTypeType._CF_enumeration.addEnumeration(unicode_value='7702', tag=None)
thermotechnicalDeviceHeatingTypeType._CF_enumeration.addEnumeration(unicode_value='7703', tag=None)
thermotechnicalDeviceHeatingTypeType._InitializeFacetMap(thermotechnicalDeviceHeatingTypeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'thermotechnicalDeviceHeatingTypeType', thermotechnicalDeviceHeatingTypeType)
_module_typeBindings.thermotechnicalDeviceHeatingTypeType = thermotechnicalDeviceHeatingTypeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}informationSourceType
class informationSourceType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'informationSourceType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 672, 1)
    _Documentation = None
informationSourceType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=informationSourceType, enum_prefix=None)
informationSourceType._CF_enumeration.addEnumeration(unicode_value='852', tag=None)
informationSourceType._CF_enumeration.addEnumeration(unicode_value='853', tag=None)
informationSourceType._CF_enumeration.addEnumeration(unicode_value='855', tag=None)
informationSourceType._CF_enumeration.addEnumeration(unicode_value='857', tag=None)
informationSourceType._CF_enumeration.addEnumeration(unicode_value='858', tag=None)
informationSourceType._CF_enumeration.addEnumeration(unicode_value='859', tag=None)
informationSourceType._CF_enumeration.addEnumeration(unicode_value='860', tag=None)
informationSourceType._CF_enumeration.addEnumeration(unicode_value='864', tag=None)
informationSourceType._CF_enumeration.addEnumeration(unicode_value='865', tag=None)
informationSourceType._CF_enumeration.addEnumeration(unicode_value='869', tag=None)
informationSourceType._CF_enumeration.addEnumeration(unicode_value='870', tag=None)
informationSourceType._CF_enumeration.addEnumeration(unicode_value='871', tag=None)
informationSourceType._InitializeFacetMap(informationSourceType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'informationSourceType', informationSourceType)
_module_typeBindings.informationSourceType = informationSourceType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}energySourceType
class energySourceType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'energySourceType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 688, 1)
    _Documentation = None
energySourceType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=energySourceType, enum_prefix=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7500', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7501', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7510', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7511', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7512', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7513', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7520', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7530', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7540', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7541', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7542', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7543', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7550', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7560', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7570', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7580', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7581', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7582', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7598', tag=None)
energySourceType._CF_enumeration.addEnumeration(unicode_value='7599', tag=None)
energySourceType._InitializeFacetMap(energySourceType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'energySourceType', energySourceType)
_module_typeBindings.energySourceType = energySourceType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}EDIDType
class EDIDType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EDIDType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 795, 1)
    _Documentation = None
EDIDType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=EDIDType, value=pyxb.binding.datatypes.nonNegativeInteger(0))
EDIDType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=EDIDType, value=pyxb.binding.datatypes.nonNegativeInteger(90))
EDIDType._InitializeFacetMap(EDIDType._CF_minInclusive,
   EDIDType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'EDIDType', EDIDType)
_module_typeBindings.EDIDType = EDIDType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}EGAIDType
class EGAIDType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EGAIDType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 801, 1)
    _Documentation = None
EGAIDType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=EGAIDType, value=pyxb.binding.datatypes.nonNegativeInteger(100000000))
EGAIDType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=EGAIDType, value=pyxb.binding.datatypes.nonNegativeInteger(900000000))
EGAIDType._InitializeFacetMap(EGAIDType._CF_minInclusive,
   EGAIDType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'EGAIDType', EGAIDType)
_module_typeBindings.EGAIDType = EGAIDType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}buildingEntranceNoType
class buildingEntranceNoType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingEntranceNoType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 807, 1)
    _Documentation = None
buildingEntranceNoType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
buildingEntranceNoType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
buildingEntranceNoType._InitializeFacetMap(buildingEntranceNoType._CF_minLength,
   buildingEntranceNoType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'buildingEntranceNoType', buildingEntranceNoType)
_module_typeBindings.buildingEntranceNoType = buildingEntranceNoType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}administrativeDwellingNoType
class administrativeDwellingNoType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'administrativeDwellingNoType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 844, 1)
    _Documentation = None
administrativeDwellingNoType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
administrativeDwellingNoType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
administrativeDwellingNoType._InitializeFacetMap(administrativeDwellingNoType._CF_minLength,
   administrativeDwellingNoType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'administrativeDwellingNoType', administrativeDwellingNoType)
_module_typeBindings.administrativeDwellingNoType = administrativeDwellingNoType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}EWIDType
class EWIDType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EWIDType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 850, 1)
    _Documentation = None
EWIDType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=EWIDType, value=pyxb.binding.datatypes.nonNegativeInteger(1))
EWIDType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=EWIDType, value=pyxb.binding.datatypes.nonNegativeInteger(900))
EWIDType._InitializeFacetMap(EWIDType._CF_minInclusive,
   EWIDType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'EWIDType', EWIDType)
_module_typeBindings.EWIDType = EWIDType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}kitchenType
class kitchenType (pyxb.binding.datatypes.boolean):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'kitchenType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 856, 1)
    _Documentation = None
kitchenType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'kitchenType', kitchenType)
_module_typeBindings.kitchenType = kitchenType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}locationOfDwellingOnFloorType
class locationOfDwellingOnFloorType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'locationOfDwellingOnFloorType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 859, 1)
    _Documentation = None
locationOfDwellingOnFloorType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(3))
locationOfDwellingOnFloorType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(40))
locationOfDwellingOnFloorType._InitializeFacetMap(locationOfDwellingOnFloorType._CF_minLength,
   locationOfDwellingOnFloorType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'locationOfDwellingOnFloorType', locationOfDwellingOnFloorType)
_module_typeBindings.locationOfDwellingOnFloorType = locationOfDwellingOnFloorType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}physicalDwellingNoType
class physicalDwellingNoType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'physicalDwellingNoType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 865, 1)
    _Documentation = None
physicalDwellingNoType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
physicalDwellingNoType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
physicalDwellingNoType._InitializeFacetMap(physicalDwellingNoType._CF_minLength,
   physicalDwellingNoType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'physicalDwellingNoType', physicalDwellingNoType)
_module_typeBindings.physicalDwellingNoType = physicalDwellingNoType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}floorType
class floorType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'floorType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 871, 1)
    _Documentation = None
floorType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=floorType, value=pyxb.binding.datatypes.nonNegativeInteger(3100))
floorType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=floorType, value=pyxb.binding.datatypes.nonNegativeInteger(3419))
floorType._InitializeFacetMap(floorType._CF_minInclusive,
   floorType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'floorType', floorType)
_module_typeBindings.floorType = floorType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}surfaceAreaOfDwellingType
class surfaceAreaOfDwellingType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfDwellingType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 877, 1)
    _Documentation = None
surfaceAreaOfDwellingType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=surfaceAreaOfDwellingType, value=pyxb.binding.datatypes.nonNegativeInteger(1))
surfaceAreaOfDwellingType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=surfaceAreaOfDwellingType, value=pyxb.binding.datatypes.nonNegativeInteger(9999))
surfaceAreaOfDwellingType._InitializeFacetMap(surfaceAreaOfDwellingType._CF_minInclusive,
   surfaceAreaOfDwellingType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'surfaceAreaOfDwellingType', surfaceAreaOfDwellingType)
_module_typeBindings.surfaceAreaOfDwellingType = surfaceAreaOfDwellingType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}dwellingStatusType
class dwellingStatusType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dwellingStatusType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 883, 1)
    _Documentation = None
dwellingStatusType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=dwellingStatusType, enum_prefix=None)
dwellingStatusType._CF_enumeration.addEnumeration(unicode_value='3001', tag=None)
dwellingStatusType._CF_enumeration.addEnumeration(unicode_value='3002', tag=None)
dwellingStatusType._CF_enumeration.addEnumeration(unicode_value='3003', tag=None)
dwellingStatusType._CF_enumeration.addEnumeration(unicode_value='3004', tag=None)
dwellingStatusType._CF_enumeration.addEnumeration(unicode_value='3005', tag=None)
dwellingStatusType._CF_enumeration.addEnumeration(unicode_value='3007', tag=None)
dwellingStatusType._CF_enumeration.addEnumeration(unicode_value='3008', tag=None)
dwellingStatusType._CF_enumeration.addEnumeration(unicode_value='3009', tag=None)
dwellingStatusType._InitializeFacetMap(dwellingStatusType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'dwellingStatusType', dwellingStatusType)
_module_typeBindings.dwellingStatusType = dwellingStatusType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}noOfHabitableRoomsType
class noOfHabitableRoomsType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'noOfHabitableRoomsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 895, 1)
    _Documentation = None
noOfHabitableRoomsType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=noOfHabitableRoomsType, value=pyxb.binding.datatypes.nonNegativeInteger(1))
noOfHabitableRoomsType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=noOfHabitableRoomsType, value=pyxb.binding.datatypes.nonNegativeInteger(99))
noOfHabitableRoomsType._InitializeFacetMap(noOfHabitableRoomsType._CF_minInclusive,
   noOfHabitableRoomsType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'noOfHabitableRoomsType', noOfHabitableRoomsType)
_module_typeBindings.noOfHabitableRoomsType = noOfHabitableRoomsType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}multipleFloorType
class multipleFloorType (pyxb.binding.datatypes.boolean):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'multipleFloorType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 901, 1)
    _Documentation = None
multipleFloorType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'multipleFloorType', multipleFloorType)
_module_typeBindings.multipleFloorType = multipleFloorType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}usageLimitationType
class usageLimitationType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'usageLimitationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 904, 1)
    _Documentation = None
usageLimitationType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=usageLimitationType, enum_prefix=None)
usageLimitationType._CF_enumeration.addEnumeration(unicode_value='3401', tag=None)
usageLimitationType._CF_enumeration.addEnumeration(unicode_value='3402', tag=None)
usageLimitationType._CF_enumeration.addEnumeration(unicode_value='3403', tag=None)
usageLimitationType._CF_enumeration.addEnumeration(unicode_value='3404', tag=None)
usageLimitationType._InitializeFacetMap(usageLimitationType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'usageLimitationType', usageLimitationType)
_module_typeBindings.usageLimitationType = usageLimitationType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}dwellingUsageCodeType
class dwellingUsageCodeType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dwellingUsageCodeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 912, 1)
    _Documentation = None
dwellingUsageCodeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=dwellingUsageCodeType, enum_prefix=None)
dwellingUsageCodeType._CF_enumeration.addEnumeration(unicode_value='3010', tag=None)
dwellingUsageCodeType._CF_enumeration.addEnumeration(unicode_value='3020', tag=None)
dwellingUsageCodeType._CF_enumeration.addEnumeration(unicode_value='3030', tag=None)
dwellingUsageCodeType._CF_enumeration.addEnumeration(unicode_value='3031', tag=None)
dwellingUsageCodeType._CF_enumeration.addEnumeration(unicode_value='3032', tag=None)
dwellingUsageCodeType._CF_enumeration.addEnumeration(unicode_value='3033', tag=None)
dwellingUsageCodeType._CF_enumeration.addEnumeration(unicode_value='3034', tag=None)
dwellingUsageCodeType._CF_enumeration.addEnumeration(unicode_value='3035', tag=None)
dwellingUsageCodeType._CF_enumeration.addEnumeration(unicode_value='3036', tag=None)
dwellingUsageCodeType._CF_enumeration.addEnumeration(unicode_value='3037', tag=None)
dwellingUsageCodeType._CF_enumeration.addEnumeration(unicode_value='3038', tag=None)
dwellingUsageCodeType._CF_enumeration.addEnumeration(unicode_value='3070', tag=None)
dwellingUsageCodeType._InitializeFacetMap(dwellingUsageCodeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'dwellingUsageCodeType', dwellingUsageCodeType)
_module_typeBindings.dwellingUsageCodeType = dwellingUsageCodeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}dwellingInformationSourceType
class dwellingInformationSourceType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dwellingInformationSourceType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 928, 1)
    _Documentation = None
dwellingInformationSourceType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=dwellingInformationSourceType, enum_prefix=None)
dwellingInformationSourceType._CF_enumeration.addEnumeration(unicode_value='3090', tag=None)
dwellingInformationSourceType._CF_enumeration.addEnumeration(unicode_value='3091', tag=None)
dwellingInformationSourceType._CF_enumeration.addEnumeration(unicode_value='3092', tag=None)
dwellingInformationSourceType._CF_enumeration.addEnumeration(unicode_value='3093', tag=None)
dwellingInformationSourceType._InitializeFacetMap(dwellingInformationSourceType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'dwellingInformationSourceType', dwellingInformationSourceType)
_module_typeBindings.dwellingInformationSourceType = dwellingInformationSourceType

# Atomic simple type: [anonymous]
class STD_ANON_12 (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 949, 4)
    _Documentation = None
STD_ANON_12._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_12, value=pyxb.binding.datatypes.date('2012-12-31'))
STD_ANON_12._InitializeFacetMap(STD_ANON_12._CF_minInclusive)
_module_typeBindings.STD_ANON_12 = STD_ANON_12

# Atomic simple type: [anonymous]
class STD_ANON_13 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 956, 4)
    _Documentation = None
STD_ANON_13._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON_13._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(2000))
STD_ANON_13._InitializeFacetMap(STD_ANON_13._CF_minLength,
   STD_ANON_13._CF_maxLength)
_module_typeBindings.STD_ANON_13 = STD_ANON_13

# Atomic simple type: [anonymous]
class STD_ANON_14 (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 966, 4)
    _Documentation = None
STD_ANON_14._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_14, value=pyxb.binding.datatypes.date('2012-12-31'))
STD_ANON_14._InitializeFacetMap(STD_ANON_14._CF_minInclusive)
_module_typeBindings.STD_ANON_14 = STD_ANON_14

# Atomic simple type: [anonymous]
class STD_ANON_15 (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 973, 4)
    _Documentation = None
STD_ANON_15._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_15, value=pyxb.binding.datatypes.date('2012-12-31'))
STD_ANON_15._InitializeFacetMap(STD_ANON_15._CF_minInclusive)
_module_typeBindings.STD_ANON_15 = STD_ANON_15

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}validFromType
class validFromType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'validFromType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1002, 1)
    _Documentation = None
validFromType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'validFromType', validFromType)
_module_typeBindings.validFromType = validFromType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}validTillType
class validTillType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'validTillType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1005, 1)
    _Documentation = None
validTillType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'validTillType', validTillType)
_module_typeBindings.validTillType = validTillType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}geometryType
class geometryType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'geometryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1008, 1)
    _Documentation = None
geometryType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=geometryType, enum_prefix=None)
geometryType._CF_enumeration.addEnumeration(unicode_value='9801', tag=None)
geometryType._CF_enumeration.addEnumeration(unicode_value='9802', tag=None)
geometryType._CF_enumeration.addEnumeration(unicode_value='9803', tag=None)
geometryType._CF_enumeration.addEnumeration(unicode_value='9809', tag=None)
geometryType._InitializeFacetMap(geometryType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'geometryType', geometryType)
_module_typeBindings.geometryType = geometryType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}EGRIDType
class EGRIDType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EGRIDType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1016, 1)
    _Documentation = None
EGRIDType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(14))
EGRIDType._InitializeFacetMap(EGRIDType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'EGRIDType', EGRIDType)
_module_typeBindings.EGRIDType = EGRIDType

# Atomic simple type: [anonymous]
class STD_ANON_16 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1029, 4)
    _Documentation = None
STD_ANON_16._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON_16._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
STD_ANON_16._InitializeFacetMap(STD_ANON_16._CF_minLength,
   STD_ANON_16._CF_maxLength)
_module_typeBindings.STD_ANON_16 = STD_ANON_16

# Atomic simple type: [anonymous]
class STD_ANON_17 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1037, 4)
    _Documentation = None
STD_ANON_17._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON_17._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
STD_ANON_17._InitializeFacetMap(STD_ANON_17._CF_minLength,
   STD_ANON_17._CF_maxLength)
_module_typeBindings.STD_ANON_17 = STD_ANON_17

# Atomic simple type: [anonymous]
class STD_ANON_18 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1045, 4)
    _Documentation = None
STD_ANON_18._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON_18._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(15))
STD_ANON_18._InitializeFacetMap(STD_ANON_18._CF_minLength,
   STD_ANON_18._CF_maxLength)
_module_typeBindings.STD_ANON_18 = STD_ANON_18

# Atomic simple type: [anonymous]
class STD_ANON_19 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1053, 4)
    _Documentation = None
STD_ANON_19._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON_19._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(15))
STD_ANON_19._InitializeFacetMap(STD_ANON_19._CF_minLength,
   STD_ANON_19._CF_maxLength)
_module_typeBindings.STD_ANON_19 = STD_ANON_19

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}cadasterAreaNumberType
class cadasterAreaNumberType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'cadasterAreaNumberType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1062, 1)
    _Documentation = None
cadasterAreaNumberType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'cadasterAreaNumberType', cadasterAreaNumberType)
_module_typeBindings.cadasterAreaNumberType = cadasterAreaNumberType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}realestateTypeType
class realestateTypeType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'realestateTypeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1065, 1)
    _Documentation = None
realestateTypeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=realestateTypeType, enum_prefix=None)
realestateTypeType._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
realestateTypeType._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
realestateTypeType._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
realestateTypeType._CF_enumeration.addEnumeration(unicode_value='4', tag=None)
realestateTypeType._CF_enumeration.addEnumeration(unicode_value='5', tag=None)
realestateTypeType._CF_enumeration.addEnumeration(unicode_value='6', tag=None)
realestateTypeType._CF_enumeration.addEnumeration(unicode_value='7', tag=None)
realestateTypeType._CF_enumeration.addEnumeration(unicode_value='8', tag=None)
realestateTypeType._InitializeFacetMap(realestateTypeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'realestateTypeType', realestateTypeType)
_module_typeBindings.realestateTypeType = realestateTypeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}authorityType
class authorityType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'authorityType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1077, 1)
    _Documentation = None
authorityType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
authorityType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
authorityType._InitializeFacetMap(authorityType._CF_minLength,
   authorityType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'authorityType', authorityType)
_module_typeBindings.authorityType = authorityType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}squareMeasureType
class squareMeasureType (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'squareMeasureType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1083, 1)
    _Documentation = None
squareMeasureType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=squareMeasureType, value=pyxb.binding.datatypes.decimal('0.0'))
squareMeasureType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=squareMeasureType, value=pyxb.binding.datatypes.decimal('1000000000.0'))
squareMeasureType._InitializeFacetMap(squareMeasureType._CF_minInclusive,
   squareMeasureType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'squareMeasureType', squareMeasureType)
_module_typeBindings.squareMeasureType = squareMeasureType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}realestateStatusType
class realestateStatusType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'realestateStatusType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1089, 1)
    _Documentation = None
realestateStatusType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=realestateStatusType, enum_prefix=None)
realestateStatusType._CF_enumeration.addEnumeration(unicode_value='0', tag=None)
realestateStatusType._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
realestateStatusType._InitializeFacetMap(realestateStatusType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'realestateStatusType', realestateStatusType)
_module_typeBindings.realestateStatusType = realestateStatusType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}realestateMutnumberType
class realestateMutnumberType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'realestateMutnumberType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1095, 1)
    _Documentation = None
realestateMutnumberType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
realestateMutnumberType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
realestateMutnumberType._InitializeFacetMap(realestateMutnumberType._CF_minLength,
   realestateMutnumberType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'realestateMutnumberType', realestateMutnumberType)
_module_typeBindings.realestateMutnumberType = realestateMutnumberType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}realestateDateType
class realestateDateType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'realestateDateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1101, 1)
    _Documentation = None
realestateDateType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'realestateDateType', realestateDateType)
_module_typeBindings.realestateDateType = realestateDateType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}realestateIncompleteType
class realestateIncompleteType (pyxb.binding.datatypes.boolean):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'realestateIncompleteType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1104, 1)
    _Documentation = None
realestateIncompleteType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'realestateIncompleteType', realestateIncompleteType)
_module_typeBindings.realestateIncompleteType = realestateIncompleteType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}cantonalSubKindType
class cantonalSubKindType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'cantonalSubKindType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1107, 1)
    _Documentation = None
cantonalSubKindType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
cantonalSubKindType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(60))
cantonalSubKindType._InitializeFacetMap(cantonalSubKindType._CF_minLength,
   cantonalSubKindType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'cantonalSubKindType', cantonalSubKindType)
_module_typeBindings.cantonalSubKindType = cantonalSubKindType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}identDNType
class identDNType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'identDNType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1113, 1)
    _Documentation = None
identDNType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
identDNType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
identDNType._InitializeFacetMap(identDNType._CF_minLength,
   identDNType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'identDNType', identDNType)
_module_typeBindings.identDNType = identDNType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}zipcode6Type
class zipcode6Type (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'zipcode6Type')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1136, 1)
    _Documentation = None
zipcode6Type._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=zipcode6Type, value=pyxb.binding.datatypes.nonNegativeInteger(6))
zipcode6Type._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=zipcode6Type, value=pyxb.binding.datatypes.nonNegativeInteger(6))
zipcode6Type._InitializeFacetMap(zipcode6Type._CF_minInclusive,
   zipcode6Type._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'zipcode6Type', zipcode6Type)
_module_typeBindings.zipcode6Type = zipcode6Type

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}indentureNumberPostType
class indentureNumberPostType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'indentureNumberPostType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1142, 1)
    _Documentation = None
indentureNumberPostType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=indentureNumberPostType, value=pyxb.binding.datatypes.nonNegativeInteger(0))
indentureNumberPostType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=indentureNumberPostType, value=pyxb.binding.datatypes.nonNegativeInteger(99999))
indentureNumberPostType._InitializeFacetMap(indentureNumberPostType._CF_minInclusive,
   indentureNumberPostType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'indentureNumberPostType', indentureNumberPostType)
_module_typeBindings.indentureNumberPostType = indentureNumberPostType

# Atomic simple type: [anonymous]
class STD_ANON_20 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1152, 4)
    _Documentation = None
STD_ANON_20._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(2))
STD_ANON_20._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(40))
STD_ANON_20._InitializeFacetMap(STD_ANON_20._CF_minLength,
   STD_ANON_20._CF_maxLength)
_module_typeBindings.STD_ANON_20 = STD_ANON_20

# Atomic simple type: [anonymous]
class STD_ANON_21 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1160, 4)
    _Documentation = None
STD_ANON_21._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(2))
STD_ANON_21._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(18))
STD_ANON_21._InitializeFacetMap(STD_ANON_21._CF_minLength,
   STD_ANON_21._CF_maxLength)
_module_typeBindings.STD_ANON_21 = STD_ANON_21

# Atomic simple type: [anonymous]
class STD_ANON_22 (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1181, 4)
    _Documentation = None
STD_ANON_22._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_22, enum_prefix=None)
STD_ANON_22._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
STD_ANON_22._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
STD_ANON_22._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
STD_ANON_22._InitializeFacetMap(STD_ANON_22._CF_enumeration)
_module_typeBindings.STD_ANON_22 = STD_ANON_22

# Atomic simple type: [anonymous]
class STD_ANON_23 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1192, 4)
    _Documentation = None
STD_ANON_23._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_23, value=pyxb.binding.datatypes.decimal('0.001'))
STD_ANON_23._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON_23, value=pyxb.binding.datatypes.decimal('100.0'))
STD_ANON_23._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(7))
STD_ANON_23._CF_fractionDigits = pyxb.binding.facets.CF_fractionDigits(value=pyxb.binding.datatypes.nonNegativeInteger(3))
STD_ANON_23._InitializeFacetMap(STD_ANON_23._CF_minInclusive,
   STD_ANON_23._CF_maxInclusive,
   STD_ANON_23._CF_totalDigits,
   STD_ANON_23._CF_fractionDigits)
_module_typeBindings.STD_ANON_23 = STD_ANON_23

# Atomic simple type: [anonymous]
class STD_ANON_24 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1202, 4)
    _Documentation = None
STD_ANON_24._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_24, value=pyxb.binding.datatypes.decimal('0.001'))
STD_ANON_24._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON_24, value=pyxb.binding.datatypes.decimal('100.0'))
STD_ANON_24._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(7))
STD_ANON_24._CF_fractionDigits = pyxb.binding.facets.CF_fractionDigits(value=pyxb.binding.datatypes.nonNegativeInteger(3))
STD_ANON_24._InitializeFacetMap(STD_ANON_24._CF_minInclusive,
   STD_ANON_24._CF_maxInclusive,
   STD_ANON_24._CF_totalDigits,
   STD_ANON_24._CF_fractionDigits)
_module_typeBindings.STD_ANON_24 = STD_ANON_24

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}areaTypeType
class areaTypeType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'areaTypeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1214, 1)
    _Documentation = None
areaTypeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=areaTypeType, enum_prefix=None)
areaTypeType._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
areaTypeType._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
areaTypeType._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
areaTypeType._InitializeFacetMap(areaTypeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'areaTypeType', areaTypeType)
_module_typeBindings.areaTypeType = areaTypeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}areaDescriptionCodeType
class areaDescriptionCodeType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'areaDescriptionCodeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1221, 1)
    _Documentation = None
areaDescriptionCodeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=areaDescriptionCodeType, enum_prefix=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='0', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='4', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='5', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='6', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='7', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='8', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='9', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='10', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='11', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='12', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='13', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='14', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='15', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='16', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='17', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='18', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='19', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='20', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='21', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='22', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='23', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='24', tag=None)
areaDescriptionCodeType._CF_enumeration.addEnumeration(unicode_value='25', tag=None)
areaDescriptionCodeType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=areaDescriptionCodeType, value=pyxb.binding.datatypes.nonNegativeInteger(0))
areaDescriptionCodeType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=areaDescriptionCodeType, value=pyxb.binding.datatypes.nonNegativeInteger(25))
areaDescriptionCodeType._InitializeFacetMap(areaDescriptionCodeType._CF_enumeration,
   areaDescriptionCodeType._CF_minInclusive,
   areaDescriptionCodeType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'areaDescriptionCodeType', areaDescriptionCodeType)
_module_typeBindings.areaDescriptionCodeType = areaDescriptionCodeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}areaDescriptionType
class areaDescriptionType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'areaDescriptionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1253, 1)
    _Documentation = None
areaDescriptionType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
areaDescriptionType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
areaDescriptionType._InitializeFacetMap(areaDescriptionType._CF_minLength,
   areaDescriptionType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'areaDescriptionType', areaDescriptionType)
_module_typeBindings.areaDescriptionType = areaDescriptionType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}areaValueType
class areaValueType (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'areaValueType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1259, 1)
    _Documentation = None
areaValueType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=areaValueType, value=pyxb.binding.datatypes.decimal('0.0'))
areaValueType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=areaValueType, value=pyxb.binding.datatypes.decimal('1000000000.0'))
areaValueType._InitializeFacetMap(areaValueType._CF_minInclusive,
   areaValueType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'areaValueType', areaValueType)
_module_typeBindings.areaValueType = areaValueType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}usageCodeType
class usageCodeType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'usageCodeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1274, 1)
    _Documentation = None
usageCodeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=usageCodeType, enum_prefix=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1199', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1219', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1220', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1230', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1241', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1242', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1252', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1259', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1263', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1264', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1265', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1269', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1271', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1272', tag=None)
usageCodeType._CF_enumeration.addEnumeration(unicode_value='1274', tag=None)
usageCodeType._InitializeFacetMap(usageCodeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'usageCodeType', usageCodeType)
_module_typeBindings.usageCodeType = usageCodeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}usageDescriptionType
class usageDescriptionType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'usageDescriptionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1293, 1)
    _Documentation = None
usageDescriptionType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'usageDescriptionType', usageDescriptionType)
_module_typeBindings.usageDescriptionType = usageDescriptionType

# Atomic simple type: [anonymous]
class STD_ANON_25 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1299, 4)
    _Documentation = None
STD_ANON_25._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(12))
STD_ANON_25._CF_fractionDigits = pyxb.binding.facets.CF_fractionDigits(value=pyxb.binding.datatypes.nonNegativeInteger(2))
STD_ANON_25._InitializeFacetMap(STD_ANON_25._CF_totalDigits,
   STD_ANON_25._CF_fractionDigits)
_module_typeBindings.STD_ANON_25 = STD_ANON_25

# Atomic simple type: [anonymous]
class STD_ANON_26 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1307, 4)
    _Documentation = None
STD_ANON_26._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(5))
STD_ANON_26._CF_fractionDigits = pyxb.binding.facets.CF_fractionDigits(value=pyxb.binding.datatypes.nonNegativeInteger(2))
STD_ANON_26._InitializeFacetMap(STD_ANON_26._CF_totalDigits,
   STD_ANON_26._CF_fractionDigits)
_module_typeBindings.STD_ANON_26 = STD_ANON_26

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}changeReasonType
class changeReasonType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'changeReasonType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1316, 1)
    _Documentation = None
changeReasonType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=changeReasonType, enum_prefix=None)
changeReasonType._CF_enumeration.addEnumeration(unicode_value='1001', tag=None)
changeReasonType._CF_enumeration.addEnumeration(unicode_value='1002', tag=None)
changeReasonType._CF_enumeration.addEnumeration(unicode_value='1003', tag=None)
changeReasonType._CF_enumeration.addEnumeration(unicode_value='1004', tag=None)
changeReasonType._CF_enumeration.addEnumeration(unicode_value='1005', tag=None)
changeReasonType._CF_enumeration.addEnumeration(unicode_value='1006', tag=None)
changeReasonType._InitializeFacetMap(changeReasonType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'changeReasonType', changeReasonType)
_module_typeBindings.changeReasonType = changeReasonType

# Atomic simple type: [anonymous]
class STD_ANON_27 (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1337, 4)
    _Documentation = None
STD_ANON_27._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_27, value=pyxb.binding.datatypes.nonNegativeInteger(5))
STD_ANON_27._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON_27, value=pyxb.binding.datatypes.nonNegativeInteger(9999999))
STD_ANON_27._InitializeFacetMap(STD_ANON_27._CF_minInclusive,
   STD_ANON_27._CF_maxInclusive)
_module_typeBindings.STD_ANON_27 = STD_ANON_27

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}ESIDType
class ESIDType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ESIDType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1375, 1)
    _Documentation = None
ESIDType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=ESIDType, value=pyxb.binding.datatypes.nonNegativeInteger(10000000))
ESIDType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=ESIDType, value=pyxb.binding.datatypes.nonNegativeInteger(90000000))
ESIDType._InitializeFacetMap(ESIDType._CF_minInclusive,
   ESIDType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'ESIDType', ESIDType)
_module_typeBindings.ESIDType = ESIDType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}officialStreetNumberType
class officialStreetNumberType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'officialStreetNumberType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1381, 1)
    _Documentation = None
officialStreetNumberType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=officialStreetNumberType, value=pyxb.binding.datatypes.nonNegativeInteger(1))
officialStreetNumberType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=officialStreetNumberType, value=pyxb.binding.datatypes.nonNegativeInteger(999999999999))
officialStreetNumberType._InitializeFacetMap(officialStreetNumberType._CF_minInclusive,
   officialStreetNumberType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'officialStreetNumberType', officialStreetNumberType)
_module_typeBindings.officialStreetNumberType = officialStreetNumberType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}streetKindType
class streetKindType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'streetKindType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1387, 1)
    _Documentation = None
streetKindType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=streetKindType, enum_prefix=None)
streetKindType._CF_enumeration.addEnumeration(unicode_value='9801', tag=None)
streetKindType._CF_enumeration.addEnumeration(unicode_value='9802', tag=None)
streetKindType._CF_enumeration.addEnumeration(unicode_value='9803', tag=None)
streetKindType._CF_enumeration.addEnumeration(unicode_value='9809', tag=None)
streetKindType._InitializeFacetMap(streetKindType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'streetKindType', streetKindType)
_module_typeBindings.streetKindType = streetKindType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}isOfficialDescriptionType
class isOfficialDescriptionType (pyxb.binding.datatypes.boolean):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'isOfficialDescriptionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1395, 1)
    _Documentation = None
isOfficialDescriptionType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'isOfficialDescriptionType', isOfficialDescriptionType)
_module_typeBindings.isOfficialDescriptionType = isOfficialDescriptionType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}streetStatusType
class streetStatusType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'streetStatusType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1398, 1)
    _Documentation = None
streetStatusType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=streetStatusType, enum_prefix=None)
streetStatusType._CF_enumeration.addEnumeration(unicode_value='9811', tag=None)
streetStatusType._CF_enumeration.addEnumeration(unicode_value='9812', tag=None)
streetStatusType._CF_enumeration.addEnumeration(unicode_value='9813', tag=None)
streetStatusType._CF_enumeration.addEnumeration(unicode_value='9814', tag=None)
streetStatusType._InitializeFacetMap(streetStatusType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'streetStatusType', streetStatusType)
_module_typeBindings.streetStatusType = streetStatusType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}streetDescriptionLongType
class streetDescriptionLongType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'streetDescriptionLongType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1406, 1)
    _Documentation = None
streetDescriptionLongType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
streetDescriptionLongType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(60))
streetDescriptionLongType._InitializeFacetMap(streetDescriptionLongType._CF_minLength,
   streetDescriptionLongType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'streetDescriptionLongType', streetDescriptionLongType)
_module_typeBindings.streetDescriptionLongType = streetDescriptionLongType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}streetDescriptionShortType
class streetDescriptionShortType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'streetDescriptionShortType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1412, 1)
    _Documentation = None
streetDescriptionShortType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
streetDescriptionShortType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(24))
streetDescriptionShortType._InitializeFacetMap(streetDescriptionShortType._CF_minLength,
   streetDescriptionShortType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'streetDescriptionShortType', streetDescriptionShortType)
_module_typeBindings.streetDescriptionShortType = streetDescriptionShortType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}streetIndexNameType
class streetIndexNameType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'streetIndexNameType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1418, 1)
    _Documentation = None
streetIndexNameType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
streetIndexNameType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(3))
streetIndexNameType._InitializeFacetMap(streetIndexNameType._CF_minLength,
   streetIndexNameType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'streetIndexNameType', streetIndexNameType)
_module_typeBindings.streetIndexNameType = streetIndexNameType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}numberingType
class numberingType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'numberingType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1424, 1)
    _Documentation = None
numberingType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=numberingType, enum_prefix=None)
numberingType._CF_enumeration.addEnumeration(unicode_value='9830', tag=None)
numberingType._CF_enumeration.addEnumeration(unicode_value='9832', tag=None)
numberingType._CF_enumeration.addEnumeration(unicode_value='9835', tag=None)
numberingType._CF_enumeration.addEnumeration(unicode_value='9836', tag=None)
numberingType._CF_enumeration.addEnumeration(unicode_value='9837', tag=None)
numberingType._CF_enumeration.addEnumeration(unicode_value='9839', tag=None)
numberingType._InitializeFacetMap(numberingType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'numberingType', numberingType)
_module_typeBindings.numberingType = numberingType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}streetLanguageType
class streetLanguageType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'streetLanguageType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1454, 1)
    _Documentation = None
streetLanguageType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=streetLanguageType, enum_prefix=None)
streetLanguageType._CF_enumeration.addEnumeration(unicode_value='9901', tag=None)
streetLanguageType._CF_enumeration.addEnumeration(unicode_value='9902', tag=None)
streetLanguageType._CF_enumeration.addEnumeration(unicode_value='9903', tag=None)
streetLanguageType._CF_enumeration.addEnumeration(unicode_value='9904', tag=None)
streetLanguageType._InitializeFacetMap(streetLanguageType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'streetLanguageType', streetLanguageType)
_module_typeBindings.streetLanguageType = streetLanguageType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}EREIDType
class EREIDType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EREIDType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1470, 1)
    _Documentation = None
EREIDType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'EREIDType', EREIDType)
_module_typeBindings.EREIDType = EREIDType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}mapNumberType
class mapNumberType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'mapNumberType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1479, 1)
    _Documentation = None
mapNumberType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
mapNumberType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
mapNumberType._InitializeFacetMap(mapNumberType._CF_minLength,
   mapNumberType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'mapNumberType', mapNumberType)
_module_typeBindings.mapNumberType = mapNumberType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}remarkTypeType
class remarkTypeType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'remarkTypeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1492, 1)
    _Documentation = None
remarkTypeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=remarkTypeType, enum_prefix=None)
remarkTypeType._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
remarkTypeType._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
remarkTypeType._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
remarkTypeType._CF_enumeration.addEnumeration(unicode_value='4', tag=None)
remarkTypeType._CF_enumeration.addEnumeration(unicode_value='5', tag=None)
remarkTypeType._CF_enumeration.addEnumeration(unicode_value='6', tag=None)
remarkTypeType._InitializeFacetMap(remarkTypeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'remarkTypeType', remarkTypeType)
_module_typeBindings.remarkTypeType = remarkTypeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}remarkOtherTypeType
class remarkOtherTypeType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'remarkOtherTypeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1502, 1)
    _Documentation = None
remarkOtherTypeType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'remarkOtherTypeType', remarkOtherTypeType)
_module_typeBindings.remarkOtherTypeType = remarkOtherTypeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}remarkTextType
class remarkTextType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'remarkTextType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1505, 1)
    _Documentation = None
remarkTextType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'remarkTextType', remarkTextType)
_module_typeBindings.remarkTextType = remarkTextType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}objectIDType
class objectIDType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'objectIDType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1508, 1)
    _Documentation = None
objectIDType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'objectIDType', objectIDType)
_module_typeBindings.objectIDType = objectIDType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}placeNameTypeType
class placeNameTypeType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'placeNameTypeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1520, 1)
    _Documentation = None
placeNameTypeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=placeNameTypeType, enum_prefix=None)
placeNameTypeType._CF_enumeration.addEnumeration(unicode_value='0', tag=None)
placeNameTypeType._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
placeNameTypeType._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
placeNameTypeType._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
placeNameTypeType._InitializeFacetMap(placeNameTypeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'placeNameTypeType', placeNameTypeType)
_module_typeBindings.placeNameTypeType = placeNameTypeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}localGeographicalNameType
class localGeographicalNameType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'localGeographicalNameType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1528, 1)
    _Documentation = None
localGeographicalNameType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'localGeographicalNameType', localGeographicalNameType)
_module_typeBindings.localGeographicalNameType = localGeographicalNameType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}kindOfWorkType
class kindOfWorkType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'kindOfWorkType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1551, 1)
    _Documentation = None
kindOfWorkType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=kindOfWorkType, enum_prefix=None)
kindOfWorkType._CF_enumeration.addEnumeration(unicode_value='6001', tag=None)
kindOfWorkType._CF_enumeration.addEnumeration(unicode_value='6002', tag=None)
kindOfWorkType._CF_enumeration.addEnumeration(unicode_value='6007', tag=None)
kindOfWorkType._InitializeFacetMap(kindOfWorkType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'kindOfWorkType', kindOfWorkType)
_module_typeBindings.kindOfWorkType = kindOfWorkType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}typeOfvalueType
class typeOfvalueType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'typeOfvalueType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1573, 1)
    _Documentation = None
typeOfvalueType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=typeOfvalueType, enum_prefix=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='1007', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2001', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2002', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2003', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2004', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2005', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2006', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2007', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2008', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2009', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2010', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2011', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2012', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2013', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2014', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2015', tag=None)
typeOfvalueType._CF_enumeration.addEnumeration(unicode_value='2016', tag=None)
typeOfvalueType._InitializeFacetMap(typeOfvalueType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'typeOfvalueType', typeOfvalueType)
_module_typeBindings.typeOfvalueType = typeOfvalueType

# Atomic simple type: [anonymous]
class STD_ANON_28 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1597, 4)
    _Documentation = None
STD_ANON_28._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(12))
STD_ANON_28._CF_fractionDigits = pyxb.binding.facets.CF_fractionDigits(value=pyxb.binding.datatypes.nonNegativeInteger(2))
STD_ANON_28._InitializeFacetMap(STD_ANON_28._CF_totalDigits,
   STD_ANON_28._CF_fractionDigits)
_module_typeBindings.STD_ANON_28 = STD_ANON_28

# Atomic simple type: [anonymous]
class STD_ANON_29 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1605, 4)
    _Documentation = None
STD_ANON_29._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(5))
STD_ANON_29._CF_fractionDigits = pyxb.binding.facets.CF_fractionDigits(value=pyxb.binding.datatypes.nonNegativeInteger(2))
STD_ANON_29._InitializeFacetMap(STD_ANON_29._CF_totalDigits,
   STD_ANON_29._CF_fractionDigits)
_module_typeBindings.STD_ANON_29 = STD_ANON_29

# Atomic simple type: [anonymous]
class STD_ANON_30 (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1618, 4)
    _Documentation = None
STD_ANON_30._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_30, value=pyxb.binding.datatypes.nonNegativeInteger(1000))
STD_ANON_30._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON_30, value=pyxb.binding.datatypes.nonNegativeInteger(2999))
STD_ANON_30._InitializeFacetMap(STD_ANON_30._CF_minInclusive,
   STD_ANON_30._CF_maxInclusive)
_module_typeBindings.STD_ANON_30 = STD_ANON_30

# Atomic simple type: [anonymous]
class STD_ANON_31 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1627, 4)
    _Documentation = None
STD_ANON_31._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON_31, value=pyxb.binding.datatypes.decimal('0.0'))
STD_ANON_31._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON_31, value=pyxb.binding.datatypes.decimal('999.99'))
STD_ANON_31._InitializeFacetMap(STD_ANON_31._CF_minInclusive,
   STD_ANON_31._CF_maxInclusive)
_module_typeBindings.STD_ANON_31 = STD_ANON_31

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}estimationVolumeType
class estimationVolumeType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'estimationVolumeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1638, 1)
    _Documentation = None
estimationVolumeType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=estimationVolumeType, value=pyxb.binding.datatypes.nonNegativeInteger(5))
estimationVolumeType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=estimationVolumeType, value=pyxb.binding.datatypes.nonNegativeInteger(2000000))
estimationVolumeType._InitializeFacetMap(estimationVolumeType._CF_minInclusive,
   estimationVolumeType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'estimationVolumeType', estimationVolumeType)
_module_typeBindings.estimationVolumeType = estimationVolumeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}estimationYearOfConstructionType
class estimationYearOfConstructionType (pyxb.binding.datatypes.gYear):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'estimationYearOfConstructionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1644, 1)
    _Documentation = None
estimationYearOfConstructionType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=estimationYearOfConstructionType, value=pyxb.binding.datatypes.gYear('1000'))
estimationYearOfConstructionType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=estimationYearOfConstructionType, value=pyxb.binding.datatypes.gYear('2099'))
estimationYearOfConstructionType._InitializeFacetMap(estimationYearOfConstructionType._CF_minInclusive,
   estimationYearOfConstructionType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'estimationYearOfConstructionType', estimationYearOfConstructionType)
_module_typeBindings.estimationYearOfConstructionType = estimationYearOfConstructionType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}estimationDescriptionType
class estimationDescriptionType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'estimationDescriptionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1650, 1)
    _Documentation = None
estimationDescriptionType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(3))
estimationDescriptionType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(1000))
estimationDescriptionType._InitializeFacetMap(estimationDescriptionType._CF_minLength,
   estimationDescriptionType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'estimationDescriptionType', estimationDescriptionType)
_module_typeBindings.estimationDescriptionType = estimationDescriptionType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0129/5}estimationReasonTextType
class estimationReasonTextType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'estimationReasonTextType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1656, 1)
    _Documentation = None
estimationReasonTextType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
estimationReasonTextType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(30))
estimationReasonTextType._InitializeFacetMap(estimationReasonTextType._CF_minLength,
   estimationReasonTextType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'estimationReasonTextType', estimationReasonTextType)
_module_typeBindings.estimationReasonTextType = estimationReasonTextType

# Atomic simple type: [anonymous]
class STD_ANON_32 (EGRIDType):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1024, 4)
    _Documentation = None
STD_ANON_32._InitializeFacetMap()
_module_typeBindings.STD_ANON_32 = STD_ANON_32

# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}namedMetaDataType with content type ELEMENT_ONLY
class namedMetaDataType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}namedMetaDataType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'namedMetaDataType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 40, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}metaDataName uses Python identifier metaDataName
    __metaDataName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'metaDataName'), 'metaDataName', '__httpwww_ech_chxmlnseCH_01295_namedMetaDataType_httpwww_ech_chxmlnseCH_01295metaDataName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 42, 3), )

    
    metaDataName = property(__metaDataName.value, __metaDataName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}metaDataValue uses Python identifier metaDataValue
    __metaDataValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'metaDataValue'), 'metaDataValue', '__httpwww_ech_chxmlnseCH_01295_namedMetaDataType_httpwww_ech_chxmlnseCH_01295metaDataValue', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 50, 3), )

    
    metaDataValue = property(__metaDataValue.value, __metaDataValue.set, None, None)

    _ElementMap.update({
        __metaDataName.name() : __metaDataName,
        __metaDataValue.name() : __metaDataValue
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.namedMetaDataType = namedMetaDataType
Namespace.addCategoryObject('typeBinding', 'namedMetaDataType', namedMetaDataType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}personIdentificationType with content type ELEMENT_ONLY
class personIdentificationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}personIdentificationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'personIdentificationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 65, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}individual uses Python identifier individual
    __individual = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'individual'), 'individual', '__httpwww_ech_chxmlnseCH_01295_personIdentificationType_httpwww_ech_chxmlnseCH_01295individual', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 67, 3), )

    
    individual = property(__individual.value, __individual.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}organisation uses Python identifier organisation
    __organisation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'organisation'), 'organisation', '__httpwww_ech_chxmlnseCH_01295_personIdentificationType_httpwww_ech_chxmlnseCH_01295organisation', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 68, 3), )

    
    organisation = property(__organisation.value, __organisation.set, None, None)

    _ElementMap.update({
        __individual.name() : __individual,
        __organisation.name() : __organisation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.personIdentificationType = personIdentificationType
Namespace.addCategoryObject('typeBinding', 'personIdentificationType', personIdentificationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}namedIdType with content type ELEMENT_ONLY
class namedIdType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}namedIdType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'namedIdType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 71, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}IdCategory uses Python identifier IdCategory
    __IdCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdCategory'), 'IdCategory', '__httpwww_ech_chxmlnseCH_01295_namedIdType_httpwww_ech_chxmlnseCH_01295IdCategory', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 73, 3), )

    
    IdCategory = property(__IdCategory.value, __IdCategory.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}Id uses Python identifier Id
    __Id = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Id'), 'Id', '__httpwww_ech_chxmlnseCH_01295_namedIdType_httpwww_ech_chxmlnseCH_01295Id', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 74, 3), )

    
    Id = property(__Id.value, __Id.set, None, None)

    _ElementMap.update({
        __IdCategory.name() : __IdCategory,
        __Id.name() : __Id
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.namedIdType = namedIdType
Namespace.addCategoryObject('typeBinding', 'namedIdType', namedIdType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}datePartiallyKnownType with content type ELEMENT_ONLY
class datePartiallyKnownType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}datePartiallyKnownType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'datePartiallyKnownType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 84, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}yearMonthDay uses Python identifier yearMonthDay
    __yearMonthDay = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yearMonthDay'), 'yearMonthDay', '__httpwww_ech_chxmlnseCH_01295_datePartiallyKnownType_httpwww_ech_chxmlnseCH_01295yearMonthDay', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 86, 3), )

    
    yearMonthDay = property(__yearMonthDay.value, __yearMonthDay.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}yearMonth uses Python identifier yearMonth
    __yearMonth = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yearMonth'), 'yearMonth', '__httpwww_ech_chxmlnseCH_01295_datePartiallyKnownType_httpwww_ech_chxmlnseCH_01295yearMonth', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 87, 3), )

    
    yearMonth = property(__yearMonth.value, __yearMonth.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}year uses Python identifier year
    __year = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'year'), 'year', '__httpwww_ech_chxmlnseCH_01295_datePartiallyKnownType_httpwww_ech_chxmlnseCH_01295year', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 88, 3), )

    
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


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}coordinatesType with content type ELEMENT_ONLY
class coordinatesType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}coordinatesType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'coordinatesType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 107, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}LV95 uses Python identifier LV95
    __LV95 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LV95'), 'LV95', '__httpwww_ech_chxmlnseCH_01295_coordinatesType_httpwww_ech_chxmlnseCH_01295LV95', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 109, 3), )

    
    LV95 = property(__LV95.value, __LV95.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}LV03 uses Python identifier LV03
    __LV03 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LV03'), 'LV03', '__httpwww_ech_chxmlnseCH_01295_coordinatesType_httpwww_ech_chxmlnseCH_01295LV03', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 136, 3), )

    
    LV03 = property(__LV03.value, __LV03.set, None, None)

    _ElementMap.update({
        __LV95.name() : __LV95,
        __LV03.name() : __LV03
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.coordinatesType = coordinatesType
Namespace.addCategoryObject('typeBinding', 'coordinatesType', coordinatesType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 110, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}east uses Python identifier east
    __east = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'east'), 'east', '__httpwww_ech_chxmlnseCH_01295_CTD_ANON_httpwww_ech_chxmlnseCH_01295east', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 112, 6), )

    
    east = property(__east.value, __east.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}north uses Python identifier north
    __north = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'north'), 'north', '__httpwww_ech_chxmlnseCH_01295_CTD_ANON_httpwww_ech_chxmlnseCH_01295north', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 122, 6), )

    
    north = property(__north.value, __north.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}originOfCoordinates uses Python identifier originOfCoordinates
    __originOfCoordinates = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'originOfCoordinates'), 'originOfCoordinates', '__httpwww_ech_chxmlnseCH_01295_CTD_ANON_httpwww_ech_chxmlnseCH_01295originOfCoordinates', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 132, 6), )

    
    originOfCoordinates = property(__originOfCoordinates.value, __originOfCoordinates.set, None, None)

    _ElementMap.update({
        __east.name() : __east,
        __north.name() : __north,
        __originOfCoordinates.name() : __originOfCoordinates
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 137, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}Y uses Python identifier Y
    __Y = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Y'), 'Y', '__httpwww_ech_chxmlnseCH_01295_CTD_ANON__httpwww_ech_chxmlnseCH_01295Y', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 139, 6), )

    
    Y = property(__Y.value, __Y.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}X uses Python identifier X
    __X = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'X'), 'X', '__httpwww_ech_chxmlnseCH_01295_CTD_ANON__httpwww_ech_chxmlnseCH_01295X', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 149, 6), )

    
    X = property(__X.value, __X.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}originOfCoordinates uses Python identifier originOfCoordinates
    __originOfCoordinates = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'originOfCoordinates'), 'originOfCoordinates', '__httpwww_ech_chxmlnseCH_01295_CTD_ANON__httpwww_ech_chxmlnseCH_01295originOfCoordinates', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 159, 6), )

    
    originOfCoordinates = property(__originOfCoordinates.value, __originOfCoordinates.set, None, None)

    _ElementMap.update({
        __Y.name() : __Y,
        __X.name() : __X,
        __originOfCoordinates.name() : __originOfCoordinates
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}constructionLocalisationType with content type ELEMENT_ONLY
class constructionLocalisationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}constructionLocalisationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'constructionLocalisationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 183, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}municipality uses Python identifier municipality
    __municipality = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'municipality'), 'municipality', '__httpwww_ech_chxmlnseCH_01295_constructionLocalisationType_httpwww_ech_chxmlnseCH_01295municipality', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 185, 3), )

    
    municipality = property(__municipality.value, __municipality.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}canton uses Python identifier canton
    __canton = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'canton'), 'canton', '__httpwww_ech_chxmlnseCH_01295_constructionLocalisationType_httpwww_ech_chxmlnseCH_01295canton', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 186, 3), )

    
    canton = property(__canton.value, __canton.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}country uses Python identifier country
    __country = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'country'), 'country', '__httpwww_ech_chxmlnseCH_01295_constructionLocalisationType_httpwww_ech_chxmlnseCH_01295country', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 187, 3), )

    
    country = property(__country.value, __country.set, None, None)

    _ElementMap.update({
        __municipality.name() : __municipality,
        __canton.name() : __canton,
        __country.name() : __country
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.constructionLocalisationType = constructionLocalisationType
Namespace.addCategoryObject('typeBinding', 'constructionLocalisationType', constructionLocalisationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}constructionProjectIdentificationType with content type ELEMENT_ONLY
class constructionProjectIdentificationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}constructionProjectIdentificationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'constructionProjectIdentificationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 386, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_01295_constructionProjectIdentificationType_httpwww_ech_chxmlnseCH_01295localID', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 388, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EPROID uses Python identifier EPROID
    __EPROID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EPROID'), 'EPROID', '__httpwww_ech_chxmlnseCH_01295_constructionProjectIdentificationType_httpwww_ech_chxmlnseCH_01295EPROID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 389, 3), )

    
    EPROID = property(__EPROID.value, __EPROID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}officialConstructionProjectFileNo uses Python identifier officialConstructionProjectFileNo
    __officialConstructionProjectFileNo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'officialConstructionProjectFileNo'), 'officialConstructionProjectFileNo', '__httpwww_ech_chxmlnseCH_01295_constructionProjectIdentificationType_httpwww_ech_chxmlnseCH_01295officialConstructionProjectFileNo', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 390, 3), )

    
    officialConstructionProjectFileNo = property(__officialConstructionProjectFileNo.value, __officialConstructionProjectFileNo.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}extensionOfOfficialConstructionProjectFileNo uses Python identifier extensionOfOfficialConstructionProjectFileNo
    __extensionOfOfficialConstructionProjectFileNo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extensionOfOfficialConstructionProjectFileNo'), 'extensionOfOfficialConstructionProjectFileNo', '__httpwww_ech_chxmlnseCH_01295_constructionProjectIdentificationType_httpwww_ech_chxmlnseCH_01295extensionOfOfficialConstructionProjectFileNo', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 391, 3), )

    
    extensionOfOfficialConstructionProjectFileNo = property(__extensionOfOfficialConstructionProjectFileNo.value, __extensionOfOfficialConstructionProjectFileNo.set, None, None)

    _ElementMap.update({
        __localID.name() : __localID,
        __EPROID.name() : __EPROID,
        __officialConstructionProjectFileNo.name() : __officialConstructionProjectFileNo,
        __extensionOfOfficialConstructionProjectFileNo.name() : __extensionOfOfficialConstructionProjectFileNo
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.constructionProjectIdentificationType = constructionProjectIdentificationType
Namespace.addCategoryObject('typeBinding', 'constructionProjectIdentificationType', constructionProjectIdentificationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}constructionProjectType with content type ELEMENT_ONLY
class constructionProjectType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}constructionProjectType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'constructionProjectType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 394, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}constructionProjectIdentification uses Python identifier constructionProjectIdentification
    __constructionProjectIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'constructionProjectIdentification'), 'constructionProjectIdentification', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295constructionProjectIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 396, 3), )

    
    constructionProjectIdentification = property(__constructionProjectIdentification.value, __constructionProjectIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}typeOfConstructionProject uses Python identifier typeOfConstructionProject
    __typeOfConstructionProject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'typeOfConstructionProject'), 'typeOfConstructionProject', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295typeOfConstructionProject', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 397, 3), )

    
    typeOfConstructionProject = property(__typeOfConstructionProject.value, __typeOfConstructionProject.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}constructionLocalisation uses Python identifier constructionLocalisation
    __constructionLocalisation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'constructionLocalisation'), 'constructionLocalisation', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295constructionLocalisation', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 398, 3), )

    
    constructionLocalisation = property(__constructionLocalisation.value, __constructionLocalisation.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}typeOfPermit uses Python identifier typeOfPermit
    __typeOfPermit = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'typeOfPermit'), 'typeOfPermit', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295typeOfPermit', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 399, 3), )

    
    typeOfPermit = property(__typeOfPermit.value, __typeOfPermit.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}buildingPermitIssueDate uses Python identifier buildingPermitIssueDate
    __buildingPermitIssueDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'buildingPermitIssueDate'), 'buildingPermitIssueDate', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295buildingPermitIssueDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 400, 3), )

    
    buildingPermitIssueDate = property(__buildingPermitIssueDate.value, __buildingPermitIssueDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}projectAnnouncementDate uses Python identifier projectAnnouncementDate
    __projectAnnouncementDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'projectAnnouncementDate'), 'projectAnnouncementDate', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295projectAnnouncementDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 401, 3), )

    
    projectAnnouncementDate = property(__projectAnnouncementDate.value, __projectAnnouncementDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}constructionAuthorisationDeniedDate uses Python identifier constructionAuthorisationDeniedDate
    __constructionAuthorisationDeniedDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'constructionAuthorisationDeniedDate'), 'constructionAuthorisationDeniedDate', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295constructionAuthorisationDeniedDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 402, 3), )

    
    constructionAuthorisationDeniedDate = property(__constructionAuthorisationDeniedDate.value, __constructionAuthorisationDeniedDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}projectStartDate uses Python identifier projectStartDate
    __projectStartDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'projectStartDate'), 'projectStartDate', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295projectStartDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 403, 3), )

    
    projectStartDate = property(__projectStartDate.value, __projectStartDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}projectCompletionDate uses Python identifier projectCompletionDate
    __projectCompletionDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'projectCompletionDate'), 'projectCompletionDate', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295projectCompletionDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 404, 3), )

    
    projectCompletionDate = property(__projectCompletionDate.value, __projectCompletionDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}projectSuspensionDate uses Python identifier projectSuspensionDate
    __projectSuspensionDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'projectSuspensionDate'), 'projectSuspensionDate', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295projectSuspensionDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 405, 3), )

    
    projectSuspensionDate = property(__projectSuspensionDate.value, __projectSuspensionDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}withdrawalDate uses Python identifier withdrawalDate
    __withdrawalDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'withdrawalDate'), 'withdrawalDate', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295withdrawalDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 406, 3), )

    
    withdrawalDate = property(__withdrawalDate.value, __withdrawalDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}nonRealisationDate uses Python identifier nonRealisationDate
    __nonRealisationDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'nonRealisationDate'), 'nonRealisationDate', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295nonRealisationDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 407, 3), )

    
    nonRealisationDate = property(__nonRealisationDate.value, __nonRealisationDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}totalCostsOfProject uses Python identifier totalCostsOfProject
    __totalCostsOfProject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'totalCostsOfProject'), 'totalCostsOfProject', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295totalCostsOfProject', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 408, 3), )

    
    totalCostsOfProject = property(__totalCostsOfProject.value, __totalCostsOfProject.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}status uses Python identifier status
    __status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'status'), 'status', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295status', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 409, 3), )

    
    status = property(__status.value, __status.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}typeOfClient uses Python identifier typeOfClient
    __typeOfClient = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'typeOfClient'), 'typeOfClient', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295typeOfClient', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 410, 3), )

    
    typeOfClient = property(__typeOfClient.value, __typeOfClient.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}typeOfConstruction uses Python identifier typeOfConstruction
    __typeOfConstruction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'typeOfConstruction'), 'typeOfConstruction', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295typeOfConstruction', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 411, 3), )

    
    typeOfConstruction = property(__typeOfConstruction.value, __typeOfConstruction.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295description', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 412, 3), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}durationOfConstructionPhase uses Python identifier durationOfConstructionPhase
    __durationOfConstructionPhase = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'durationOfConstructionPhase'), 'durationOfConstructionPhase', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295durationOfConstructionPhase', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 413, 3), )

    
    durationOfConstructionPhase = property(__durationOfConstructionPhase.value, __durationOfConstructionPhase.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}numberOfConcernedBuildings uses Python identifier numberOfConcernedBuildings
    __numberOfConcernedBuildings = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'numberOfConcernedBuildings'), 'numberOfConcernedBuildings', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295numberOfConcernedBuildings', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 414, 3), )

    
    numberOfConcernedBuildings = property(__numberOfConcernedBuildings.value, __numberOfConcernedBuildings.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}numberOfConcernedDwellings uses Python identifier numberOfConcernedDwellings
    __numberOfConcernedDwellings = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'numberOfConcernedDwellings'), 'numberOfConcernedDwellings', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295numberOfConcernedDwellings', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 415, 3), )

    
    numberOfConcernedDwellings = property(__numberOfConcernedDwellings.value, __numberOfConcernedDwellings.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}projectFreeText uses Python identifier projectFreeText
    __projectFreeText = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'projectFreeText'), 'projectFreeText', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295projectFreeText', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 416, 3), )

    
    projectFreeText = property(__projectFreeText.value, __projectFreeText.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}municipality uses Python identifier municipality
    __municipality = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'municipality'), 'municipality', '__httpwww_ech_chxmlnseCH_01295_constructionProjectType_httpwww_ech_chxmlnseCH_01295municipality', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 417, 3), )

    
    municipality = property(__municipality.value, __municipality.set, None, None)

    _ElementMap.update({
        __constructionProjectIdentification.name() : __constructionProjectIdentification,
        __typeOfConstructionProject.name() : __typeOfConstructionProject,
        __constructionLocalisation.name() : __constructionLocalisation,
        __typeOfPermit.name() : __typeOfPermit,
        __buildingPermitIssueDate.name() : __buildingPermitIssueDate,
        __projectAnnouncementDate.name() : __projectAnnouncementDate,
        __constructionAuthorisationDeniedDate.name() : __constructionAuthorisationDeniedDate,
        __projectStartDate.name() : __projectStartDate,
        __projectCompletionDate.name() : __projectCompletionDate,
        __projectSuspensionDate.name() : __projectSuspensionDate,
        __withdrawalDate.name() : __withdrawalDate,
        __nonRealisationDate.name() : __nonRealisationDate,
        __totalCostsOfProject.name() : __totalCostsOfProject,
        __status.name() : __status,
        __typeOfClient.name() : __typeOfClient,
        __typeOfConstruction.name() : __typeOfConstruction,
        __description.name() : __description,
        __durationOfConstructionPhase.name() : __durationOfConstructionPhase,
        __numberOfConcernedBuildings.name() : __numberOfConcernedBuildings,
        __numberOfConcernedDwellings.name() : __numberOfConcernedDwellings,
        __projectFreeText.name() : __projectFreeText,
        __municipality.name() : __municipality
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.constructionProjectType = constructionProjectType
Namespace.addCategoryObject('typeBinding', 'constructionProjectType', constructionProjectType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingIdentificationType with content type ELEMENT_ONLY
class buildingIdentificationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingIdentificationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingIdentificationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 421, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EGID uses Python identifier EGID
    __EGID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EGID'), 'EGID', '__httpwww_ech_chxmlnseCH_01295_buildingIdentificationType_httpwww_ech_chxmlnseCH_01295EGID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 424, 4), )

    
    EGID = property(__EGID.value, __EGID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}street uses Python identifier street
    __street = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'street'), 'street', '__httpwww_ech_chxmlnseCH_01295_buildingIdentificationType_httpwww_ech_chxmlnseCH_01295street', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 426, 5), )

    
    street = property(__street.value, __street.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}houseNumber uses Python identifier houseNumber
    __houseNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'houseNumber'), 'houseNumber', '__httpwww_ech_chxmlnseCH_01295_buildingIdentificationType_httpwww_ech_chxmlnseCH_01295houseNumber', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 427, 5), )

    
    houseNumber = property(__houseNumber.value, __houseNumber.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}zipCode uses Python identifier zipCode
    __zipCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'zipCode'), 'zipCode', '__httpwww_ech_chxmlnseCH_01295_buildingIdentificationType_httpwww_ech_chxmlnseCH_01295zipCode', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 428, 5), )

    
    zipCode = property(__zipCode.value, __zipCode.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}nameOfBuilding uses Python identifier nameOfBuilding
    __nameOfBuilding = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'nameOfBuilding'), 'nameOfBuilding', '__httpwww_ech_chxmlnseCH_01295_buildingIdentificationType_httpwww_ech_chxmlnseCH_01295nameOfBuilding', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 429, 5), )

    
    nameOfBuilding = property(__nameOfBuilding.value, __nameOfBuilding.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EGRID uses Python identifier EGRID
    __EGRID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EGRID'), 'EGRID', '__httpwww_ech_chxmlnseCH_01295_buildingIdentificationType_httpwww_ech_chxmlnseCH_01295EGRID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 433, 6), )

    
    EGRID = property(__EGRID.value, __EGRID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}cadasterAreaNumber uses Python identifier cadasterAreaNumber
    __cadasterAreaNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'cadasterAreaNumber'), 'cadasterAreaNumber', '__httpwww_ech_chxmlnseCH_01295_buildingIdentificationType_httpwww_ech_chxmlnseCH_01295cadasterAreaNumber', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 435, 7), )

    
    cadasterAreaNumber = property(__cadasterAreaNumber.value, __cadasterAreaNumber.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}number uses Python identifier number
    __number = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'number'), 'number', '__httpwww_ech_chxmlnseCH_01295_buildingIdentificationType_httpwww_ech_chxmlnseCH_01295number', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 436, 7), )

    
    number = property(__number.value, __number.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}realestateType uses Python identifier realestateType
    __realestateType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'realestateType'), 'realestateType', '__httpwww_ech_chxmlnseCH_01295_buildingIdentificationType_httpwww_ech_chxmlnseCH_01295realestateType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 444, 7), )

    
    realestateType = property(__realestateType.value, __realestateType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}officialBuildingNo uses Python identifier officialBuildingNo
    __officialBuildingNo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'officialBuildingNo'), 'officialBuildingNo', '__httpwww_ech_chxmlnseCH_01295_buildingIdentificationType_httpwww_ech_chxmlnseCH_01295officialBuildingNo', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 447, 5), )

    
    officialBuildingNo = property(__officialBuildingNo.value, __officialBuildingNo.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_01295_buildingIdentificationType_httpwww_ech_chxmlnseCH_01295localID', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 450, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}municipality uses Python identifier municipality
    __municipality = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'municipality'), 'municipality', '__httpwww_ech_chxmlnseCH_01295_buildingIdentificationType_httpwww_ech_chxmlnseCH_01295municipality', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 451, 3), )

    
    municipality = property(__municipality.value, __municipality.set, None, None)

    _ElementMap.update({
        __EGID.name() : __EGID,
        __street.name() : __street,
        __houseNumber.name() : __houseNumber,
        __zipCode.name() : __zipCode,
        __nameOfBuilding.name() : __nameOfBuilding,
        __EGRID.name() : __EGRID,
        __cadasterAreaNumber.name() : __cadasterAreaNumber,
        __number.name() : __number,
        __realestateType.name() : __realestateType,
        __officialBuildingNo.name() : __officialBuildingNo,
        __localID.name() : __localID,
        __municipality.name() : __municipality
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.buildingIdentificationType = buildingIdentificationType
Namespace.addCategoryObject('typeBinding', 'buildingIdentificationType', buildingIdentificationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingDateType with content type ELEMENT_ONLY
class buildingDateType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingDateType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingDateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 472, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}yearMonthDay uses Python identifier yearMonthDay
    __yearMonthDay = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yearMonthDay'), 'yearMonthDay', '__httpwww_ech_chxmlnseCH_01295_buildingDateType_httpwww_ech_chxmlnseCH_01295yearMonthDay', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 474, 3), )

    
    yearMonthDay = property(__yearMonthDay.value, __yearMonthDay.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}yearMonth uses Python identifier yearMonth
    __yearMonth = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yearMonth'), 'yearMonth', '__httpwww_ech_chxmlnseCH_01295_buildingDateType_httpwww_ech_chxmlnseCH_01295yearMonth', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 482, 3), )

    
    yearMonth = property(__yearMonth.value, __yearMonth.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}year uses Python identifier year
    __year = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'year'), 'year', '__httpwww_ech_chxmlnseCH_01295_buildingDateType_httpwww_ech_chxmlnseCH_01295year', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 490, 3), )

    
    year = property(__year.value, __year.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}periodOfConstruction uses Python identifier periodOfConstruction
    __periodOfConstruction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'periodOfConstruction'), 'periodOfConstruction', '__httpwww_ech_chxmlnseCH_01295_buildingDateType_httpwww_ech_chxmlnseCH_01295periodOfConstruction', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 498, 3), )

    
    periodOfConstruction = property(__periodOfConstruction.value, __periodOfConstruction.set, None, None)

    _ElementMap.update({
        __yearMonthDay.name() : __yearMonthDay,
        __yearMonth.name() : __yearMonth,
        __year.name() : __year,
        __periodOfConstruction.name() : __periodOfConstruction
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.buildingDateType = buildingDateType
Namespace.addCategoryObject('typeBinding', 'buildingDateType', buildingDateType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingVolumeType with content type ELEMENT_ONLY
class buildingVolumeType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingVolumeType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingVolumeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 612, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}volume uses Python identifier volume
    __volume = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'volume'), 'volume', '__httpwww_ech_chxmlnseCH_01295_buildingVolumeType_httpwww_ech_chxmlnseCH_01295volume', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 614, 3), )

    
    volume = property(__volume.value, __volume.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}informationSource uses Python identifier informationSource
    __informationSource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'informationSource'), 'informationSource', '__httpwww_ech_chxmlnseCH_01295_buildingVolumeType_httpwww_ech_chxmlnseCH_01295informationSource', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 622, 3), )

    
    informationSource = property(__informationSource.value, __informationSource.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}norm uses Python identifier norm
    __norm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'norm'), 'norm', '__httpwww_ech_chxmlnseCH_01295_buildingVolumeType_httpwww_ech_chxmlnseCH_01295norm', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 623, 3), )

    
    norm = property(__norm.value, __norm.set, None, None)

    _ElementMap.update({
        __volume.name() : __volume,
        __informationSource.name() : __informationSource,
        __norm.name() : __norm
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.buildingVolumeType = buildingVolumeType
Namespace.addCategoryObject('typeBinding', 'buildingVolumeType', buildingVolumeType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}heatingType with content type ELEMENT_ONLY
class heatingType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}heatingType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'heatingType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 712, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}heatGeneratorHeating uses Python identifier heatGeneratorHeating
    __heatGeneratorHeating = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'heatGeneratorHeating'), 'heatGeneratorHeating', '__httpwww_ech_chxmlnseCH_01295_heatingType_httpwww_ech_chxmlnseCH_01295heatGeneratorHeating', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 714, 3), )

    
    heatGeneratorHeating = property(__heatGeneratorHeating.value, __heatGeneratorHeating.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}energySourceHeating uses Python identifier energySourceHeating
    __energySourceHeating = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'energySourceHeating'), 'energySourceHeating', '__httpwww_ech_chxmlnseCH_01295_heatingType_httpwww_ech_chxmlnseCH_01295energySourceHeating', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 715, 3), )

    
    energySourceHeating = property(__energySourceHeating.value, __energySourceHeating.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}informationSourceHeating uses Python identifier informationSourceHeating
    __informationSourceHeating = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'informationSourceHeating'), 'informationSourceHeating', '__httpwww_ech_chxmlnseCH_01295_heatingType_httpwww_ech_chxmlnseCH_01295informationSourceHeating', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 716, 3), )

    
    informationSourceHeating = property(__informationSourceHeating.value, __informationSourceHeating.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}revisionDate uses Python identifier revisionDate
    __revisionDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'revisionDate'), 'revisionDate', '__httpwww_ech_chxmlnseCH_01295_heatingType_httpwww_ech_chxmlnseCH_01295revisionDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 717, 3), )

    
    revisionDate = property(__revisionDate.value, __revisionDate.set, None, None)

    _ElementMap.update({
        __heatGeneratorHeating.name() : __heatGeneratorHeating,
        __energySourceHeating.name() : __energySourceHeating,
        __informationSourceHeating.name() : __informationSourceHeating,
        __revisionDate.name() : __revisionDate
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.heatingType = heatingType
Namespace.addCategoryObject('typeBinding', 'heatingType', heatingType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}hotWaterType with content type ELEMENT_ONLY
class hotWaterType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}hotWaterType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'hotWaterType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 720, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}heatGeneratorHotWater uses Python identifier heatGeneratorHotWater
    __heatGeneratorHotWater = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'heatGeneratorHotWater'), 'heatGeneratorHotWater', '__httpwww_ech_chxmlnseCH_01295_hotWaterType_httpwww_ech_chxmlnseCH_01295heatGeneratorHotWater', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 722, 3), )

    
    heatGeneratorHotWater = property(__heatGeneratorHotWater.value, __heatGeneratorHotWater.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}energySourceHeating uses Python identifier energySourceHeating
    __energySourceHeating = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'energySourceHeating'), 'energySourceHeating', '__httpwww_ech_chxmlnseCH_01295_hotWaterType_httpwww_ech_chxmlnseCH_01295energySourceHeating', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 723, 3), )

    
    energySourceHeating = property(__energySourceHeating.value, __energySourceHeating.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}informationSourceHeating uses Python identifier informationSourceHeating
    __informationSourceHeating = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'informationSourceHeating'), 'informationSourceHeating', '__httpwww_ech_chxmlnseCH_01295_hotWaterType_httpwww_ech_chxmlnseCH_01295informationSourceHeating', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 724, 3), )

    
    informationSourceHeating = property(__informationSourceHeating.value, __informationSourceHeating.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}revisionDate uses Python identifier revisionDate
    __revisionDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'revisionDate'), 'revisionDate', '__httpwww_ech_chxmlnseCH_01295_hotWaterType_httpwww_ech_chxmlnseCH_01295revisionDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 725, 3), )

    
    revisionDate = property(__revisionDate.value, __revisionDate.set, None, None)

    _ElementMap.update({
        __heatGeneratorHotWater.name() : __heatGeneratorHotWater,
        __energySourceHeating.name() : __energySourceHeating,
        __informationSourceHeating.name() : __informationSourceHeating,
        __revisionDate.name() : __revisionDate
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.hotWaterType = hotWaterType
Namespace.addCategoryObject('typeBinding', 'hotWaterType', hotWaterType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingType with content type ELEMENT_ONLY
class buildingType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 728, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}buildingIdentification uses Python identifier buildingIdentification
    __buildingIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'buildingIdentification'), 'buildingIdentification', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295buildingIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 730, 3), )

    
    buildingIdentification = property(__buildingIdentification.value, __buildingIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EGID uses Python identifier EGID
    __EGID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EGID'), 'EGID', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295EGID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 731, 3), )

    
    EGID = property(__EGID.value, __EGID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}officialBuildingNo uses Python identifier officialBuildingNo
    __officialBuildingNo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'officialBuildingNo'), 'officialBuildingNo', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295officialBuildingNo', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 732, 3), )

    
    officialBuildingNo = property(__officialBuildingNo.value, __officialBuildingNo.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'name'), 'name', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295name', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 733, 3), )

    
    name = property(__name.value, __name.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}dateOfConstruction uses Python identifier dateOfConstruction
    __dateOfConstruction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateOfConstruction'), 'dateOfConstruction', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295dateOfConstruction', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 734, 3), )

    
    dateOfConstruction = property(__dateOfConstruction.value, __dateOfConstruction.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}dateOfRenovation uses Python identifier dateOfRenovation
    __dateOfRenovation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateOfRenovation'), 'dateOfRenovation', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295dateOfRenovation', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 735, 3), )

    
    dateOfRenovation = property(__dateOfRenovation.value, __dateOfRenovation.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}dateOfDemolition uses Python identifier dateOfDemolition
    __dateOfDemolition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateOfDemolition'), 'dateOfDemolition', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295dateOfDemolition', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 736, 3), )

    
    dateOfDemolition = property(__dateOfDemolition.value, __dateOfDemolition.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}numberOfFloors uses Python identifier numberOfFloors
    __numberOfFloors = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'numberOfFloors'), 'numberOfFloors', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295numberOfFloors', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 737, 3), )

    
    numberOfFloors = property(__numberOfFloors.value, __numberOfFloors.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}numberOfSeparateHabitableRooms uses Python identifier numberOfSeparateHabitableRooms
    __numberOfSeparateHabitableRooms = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'numberOfSeparateHabitableRooms'), 'numberOfSeparateHabitableRooms', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295numberOfSeparateHabitableRooms', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 738, 3), )

    
    numberOfSeparateHabitableRooms = property(__numberOfSeparateHabitableRooms.value, __numberOfSeparateHabitableRooms.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}surfaceAreaOfBuilding uses Python identifier surfaceAreaOfBuilding
    __surfaceAreaOfBuilding = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfBuilding'), 'surfaceAreaOfBuilding', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295surfaceAreaOfBuilding', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 739, 3), )

    
    surfaceAreaOfBuilding = property(__surfaceAreaOfBuilding.value, __surfaceAreaOfBuilding.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}subSurfaceAreaOfBuilding uses Python identifier subSurfaceAreaOfBuilding
    __subSurfaceAreaOfBuilding = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subSurfaceAreaOfBuilding'), 'subSurfaceAreaOfBuilding', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295subSurfaceAreaOfBuilding', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 740, 3), )

    
    subSurfaceAreaOfBuilding = property(__subSurfaceAreaOfBuilding.value, __subSurfaceAreaOfBuilding.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}surfaceAreaOfBuildingSignaleObject uses Python identifier surfaceAreaOfBuildingSignaleObject
    __surfaceAreaOfBuildingSignaleObject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfBuildingSignaleObject'), 'surfaceAreaOfBuildingSignaleObject', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295surfaceAreaOfBuildingSignaleObject', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 741, 3), )

    
    surfaceAreaOfBuildingSignaleObject = property(__surfaceAreaOfBuildingSignaleObject.value, __surfaceAreaOfBuildingSignaleObject.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}buildingCategory uses Python identifier buildingCategory
    __buildingCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'buildingCategory'), 'buildingCategory', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295buildingCategory', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 742, 3), )

    
    buildingCategory = property(__buildingCategory.value, __buildingCategory.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}buildingClass uses Python identifier buildingClass
    __buildingClass = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'buildingClass'), 'buildingClass', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295buildingClass', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 743, 3), )

    
    buildingClass = property(__buildingClass.value, __buildingClass.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}status uses Python identifier status
    __status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'status'), 'status', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295status', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 744, 3), )

    
    status = property(__status.value, __status.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}coordinates uses Python identifier coordinates
    __coordinates = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'coordinates'), 'coordinates', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295coordinates', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 745, 3), )

    
    coordinates = property(__coordinates.value, __coordinates.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}otherID uses Python identifier otherID
    __otherID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherID'), 'otherID', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295otherID', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 746, 3), )

    
    otherID = property(__otherID.value, __otherID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}civilDefenseShelter uses Python identifier civilDefenseShelter
    __civilDefenseShelter = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'civilDefenseShelter'), 'civilDefenseShelter', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295civilDefenseShelter', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 747, 3), )

    
    civilDefenseShelter = property(__civilDefenseShelter.value, __civilDefenseShelter.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}neighbourhood uses Python identifier neighbourhood
    __neighbourhood = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'neighbourhood'), 'neighbourhood', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295neighbourhood', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 748, 3), )

    
    neighbourhood = property(__neighbourhood.value, __neighbourhood.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localCode uses Python identifier localCode
    __localCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localCode'), 'localCode', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295localCode', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 749, 3), )

    
    localCode = property(__localCode.value, __localCode.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}energyRelevantSurface uses Python identifier energyRelevantSurface
    __energyRelevantSurface = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'energyRelevantSurface'), 'energyRelevantSurface', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295energyRelevantSurface', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 750, 3), )

    
    energyRelevantSurface = property(__energyRelevantSurface.value, __energyRelevantSurface.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}volume uses Python identifier volume
    __volume = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'volume'), 'volume', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295volume', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 751, 3), )

    
    volume = property(__volume.value, __volume.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}heating uses Python identifier heating
    __heating = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'heating'), 'heating', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295heating', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 752, 3), )

    
    heating = property(__heating.value, __heating.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}hotWater uses Python identifier hotWater
    __hotWater = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'hotWater'), 'hotWater', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295hotWater', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 753, 3), )

    
    hotWater = property(__hotWater.value, __hotWater.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}buildingEntrance uses Python identifier buildingEntrance
    __buildingEntrance = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'buildingEntrance'), 'buildingEntrance', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295buildingEntrance', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 754, 3), )

    
    buildingEntrance = property(__buildingEntrance.value, __buildingEntrance.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}namedMetaData uses Python identifier namedMetaData
    __namedMetaData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'namedMetaData'), 'namedMetaData', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295namedMetaData', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 755, 3), )

    
    namedMetaData = property(__namedMetaData.value, __namedMetaData.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}buildingFreeText uses Python identifier buildingFreeText
    __buildingFreeText = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'buildingFreeText'), 'buildingFreeText', '__httpwww_ech_chxmlnseCH_01295_buildingType_httpwww_ech_chxmlnseCH_01295buildingFreeText', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 756, 3), )

    
    buildingFreeText = property(__buildingFreeText.value, __buildingFreeText.set, None, None)

    _ElementMap.update({
        __buildingIdentification.name() : __buildingIdentification,
        __EGID.name() : __EGID,
        __officialBuildingNo.name() : __officialBuildingNo,
        __name.name() : __name,
        __dateOfConstruction.name() : __dateOfConstruction,
        __dateOfRenovation.name() : __dateOfRenovation,
        __dateOfDemolition.name() : __dateOfDemolition,
        __numberOfFloors.name() : __numberOfFloors,
        __numberOfSeparateHabitableRooms.name() : __numberOfSeparateHabitableRooms,
        __surfaceAreaOfBuilding.name() : __surfaceAreaOfBuilding,
        __subSurfaceAreaOfBuilding.name() : __subSurfaceAreaOfBuilding,
        __surfaceAreaOfBuildingSignaleObject.name() : __surfaceAreaOfBuildingSignaleObject,
        __buildingCategory.name() : __buildingCategory,
        __buildingClass.name() : __buildingClass,
        __status.name() : __status,
        __coordinates.name() : __coordinates,
        __otherID.name() : __otherID,
        __civilDefenseShelter.name() : __civilDefenseShelter,
        __neighbourhood.name() : __neighbourhood,
        __localCode.name() : __localCode,
        __energyRelevantSurface.name() : __energyRelevantSurface,
        __volume.name() : __volume,
        __heating.name() : __heating,
        __hotWater.name() : __hotWater,
        __buildingEntrance.name() : __buildingEntrance,
        __namedMetaData.name() : __namedMetaData,
        __buildingFreeText.name() : __buildingFreeText
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.buildingType = buildingType
Namespace.addCategoryObject('typeBinding', 'buildingType', buildingType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingEntranceIdentificationType with content type ELEMENT_ONLY
class buildingEntranceIdentificationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingEntranceIdentificationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingEntranceIdentificationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 813, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EGID uses Python identifier EGID
    __EGID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EGID'), 'EGID', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceIdentificationType_httpwww_ech_chxmlnseCH_01295EGID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 815, 3), )

    
    EGID = property(__EGID.value, __EGID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EGAID uses Python identifier EGAID
    __EGAID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EGAID'), 'EGAID', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceIdentificationType_httpwww_ech_chxmlnseCH_01295EGAID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 816, 3), )

    
    EGAID = property(__EGAID.value, __EGAID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EDID uses Python identifier EDID
    __EDID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EDID'), 'EDID', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceIdentificationType_httpwww_ech_chxmlnseCH_01295EDID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 817, 3), )

    
    EDID = property(__EDID.value, __EDID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceIdentificationType_httpwww_ech_chxmlnseCH_01295localID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 818, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    _ElementMap.update({
        __EGID.name() : __EGID,
        __EGAID.name() : __EGAID,
        __EDID.name() : __EDID,
        __localID.name() : __localID
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.buildingEntranceIdentificationType = buildingEntranceIdentificationType
Namespace.addCategoryObject('typeBinding', 'buildingEntranceIdentificationType', buildingEntranceIdentificationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingEntranceType with content type ELEMENT_ONLY
class buildingEntranceType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingEntranceType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingEntranceType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 821, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EGAID uses Python identifier EGAID
    __EGAID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EGAID'), 'EGAID', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceType_httpwww_ech_chxmlnseCH_01295EGAID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 823, 3), )

    
    EGAID = property(__EGAID.value, __EGAID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EDID uses Python identifier EDID
    __EDID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EDID'), 'EDID', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceType_httpwww_ech_chxmlnseCH_01295EDID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 824, 3), )

    
    EDID = property(__EDID.value, __EDID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}buildingEntranceNo uses Python identifier buildingEntranceNo
    __buildingEntranceNo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'buildingEntranceNo'), 'buildingEntranceNo', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceType_httpwww_ech_chxmlnseCH_01295buildingEntranceNo', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 825, 3), )

    
    buildingEntranceNo = property(__buildingEntranceNo.value, __buildingEntranceNo.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}coordinates uses Python identifier coordinates
    __coordinates = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'coordinates'), 'coordinates', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceType_httpwww_ech_chxmlnseCH_01295coordinates', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 826, 3), )

    
    coordinates = property(__coordinates.value, __coordinates.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceType_httpwww_ech_chxmlnseCH_01295localID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 827, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}isOfficialAddress uses Python identifier isOfficialAddress
    __isOfficialAddress = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'isOfficialAddress'), 'isOfficialAddress', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceType_httpwww_ech_chxmlnseCH_01295isOfficialAddress', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 828, 3), )

    
    isOfficialAddress = property(__isOfficialAddress.value, __isOfficialAddress.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}steetSection uses Python identifier steetSection
    __steetSection = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'steetSection'), 'steetSection', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceType_httpwww_ech_chxmlnseCH_01295steetSection', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 829, 3), )

    
    steetSection = property(__steetSection.value, __steetSection.set, None, None)

    _ElementMap.update({
        __EGAID.name() : __EGAID,
        __EDID.name() : __EDID,
        __buildingEntranceNo.name() : __buildingEntranceNo,
        __coordinates.name() : __coordinates,
        __localID.name() : __localID,
        __isOfficialAddress.name() : __isOfficialAddress,
        __steetSection.name() : __steetSection
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.buildingEntranceType = buildingEntranceType
Namespace.addCategoryObject('typeBinding', 'buildingEntranceType', buildingEntranceType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingEntranceOnlyType with content type ELEMENT_ONLY
class buildingEntranceOnlyType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingEntranceOnlyType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingEntranceOnlyType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 832, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EGAID uses Python identifier EGAID
    __EGAID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EGAID'), 'EGAID', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceOnlyType_httpwww_ech_chxmlnseCH_01295EGAID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 834, 3), )

    
    EGAID = property(__EGAID.value, __EGAID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EDID uses Python identifier EDID
    __EDID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EDID'), 'EDID', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceOnlyType_httpwww_ech_chxmlnseCH_01295EDID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 835, 3), )

    
    EDID = property(__EDID.value, __EDID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}buildingEntranceNo uses Python identifier buildingEntranceNo
    __buildingEntranceNo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'buildingEntranceNo'), 'buildingEntranceNo', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceOnlyType_httpwww_ech_chxmlnseCH_01295buildingEntranceNo', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 836, 3), )

    
    buildingEntranceNo = property(__buildingEntranceNo.value, __buildingEntranceNo.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}coordinates uses Python identifier coordinates
    __coordinates = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'coordinates'), 'coordinates', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceOnlyType_httpwww_ech_chxmlnseCH_01295coordinates', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 837, 3), )

    
    coordinates = property(__coordinates.value, __coordinates.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceOnlyType_httpwww_ech_chxmlnseCH_01295localID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 838, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}isOfficialAddress uses Python identifier isOfficialAddress
    __isOfficialAddress = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'isOfficialAddress'), 'isOfficialAddress', '__httpwww_ech_chxmlnseCH_01295_buildingEntranceOnlyType_httpwww_ech_chxmlnseCH_01295isOfficialAddress', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 839, 3), )

    
    isOfficialAddress = property(__isOfficialAddress.value, __isOfficialAddress.set, None, None)

    _ElementMap.update({
        __EGAID.name() : __EGAID,
        __EDID.name() : __EDID,
        __buildingEntranceNo.name() : __buildingEntranceNo,
        __coordinates.name() : __coordinates,
        __localID.name() : __localID,
        __isOfficialAddress.name() : __isOfficialAddress
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.buildingEntranceOnlyType = buildingEntranceOnlyType
Namespace.addCategoryObject('typeBinding', 'buildingEntranceOnlyType', buildingEntranceOnlyType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}dwellingIdentificationType with content type ELEMENT_ONLY
class dwellingIdentificationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}dwellingIdentificationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dwellingIdentificationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 936, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EGID uses Python identifier EGID
    __EGID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EGID'), 'EGID', '__httpwww_ech_chxmlnseCH_01295_dwellingIdentificationType_httpwww_ech_chxmlnseCH_01295EGID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 938, 3), )

    
    EGID = property(__EGID.value, __EGID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EDID uses Python identifier EDID
    __EDID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EDID'), 'EDID', '__httpwww_ech_chxmlnseCH_01295_dwellingIdentificationType_httpwww_ech_chxmlnseCH_01295EDID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 939, 3), )

    
    EDID = property(__EDID.value, __EDID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EWID uses Python identifier EWID
    __EWID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EWID'), 'EWID', '__httpwww_ech_chxmlnseCH_01295_dwellingIdentificationType_httpwww_ech_chxmlnseCH_01295EWID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 940, 3), )

    
    EWID = property(__EWID.value, __EWID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_01295_dwellingIdentificationType_httpwww_ech_chxmlnseCH_01295localID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 941, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    _ElementMap.update({
        __EGID.name() : __EGID,
        __EDID.name() : __EDID,
        __EWID.name() : __EWID,
        __localID.name() : __localID
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.dwellingIdentificationType = dwellingIdentificationType
Namespace.addCategoryObject('typeBinding', 'dwellingIdentificationType', dwellingIdentificationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}dwellingUsageType with content type ELEMENT_ONLY
class dwellingUsageType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}dwellingUsageType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dwellingUsageType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 944, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}usageCode uses Python identifier usageCode
    __usageCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'usageCode'), 'usageCode', '__httpwww_ech_chxmlnseCH_01295_dwellingUsageType_httpwww_ech_chxmlnseCH_01295usageCode', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 946, 3), )

    
    usageCode = property(__usageCode.value, __usageCode.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}informationSource uses Python identifier informationSource
    __informationSource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'informationSource'), 'informationSource', '__httpwww_ech_chxmlnseCH_01295_dwellingUsageType_httpwww_ech_chxmlnseCH_01295informationSource', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 947, 3), )

    
    informationSource = property(__informationSource.value, __informationSource.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}revisionDate uses Python identifier revisionDate
    __revisionDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'revisionDate'), 'revisionDate', '__httpwww_ech_chxmlnseCH_01295_dwellingUsageType_httpwww_ech_chxmlnseCH_01295revisionDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 948, 3), )

    
    revisionDate = property(__revisionDate.value, __revisionDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}remark uses Python identifier remark
    __remark = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remark'), 'remark', '__httpwww_ech_chxmlnseCH_01295_dwellingUsageType_httpwww_ech_chxmlnseCH_01295remark', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 955, 3), )

    
    remark = property(__remark.value, __remark.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}personWithMainResidence uses Python identifier personWithMainResidence
    __personWithMainResidence = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'personWithMainResidence'), 'personWithMainResidence', '__httpwww_ech_chxmlnseCH_01295_dwellingUsageType_httpwww_ech_chxmlnseCH_01295personWithMainResidence', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 963, 3), )

    
    personWithMainResidence = property(__personWithMainResidence.value, __personWithMainResidence.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}personWithSecondaryResidence uses Python identifier personWithSecondaryResidence
    __personWithSecondaryResidence = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'personWithSecondaryResidence'), 'personWithSecondaryResidence', '__httpwww_ech_chxmlnseCH_01295_dwellingUsageType_httpwww_ech_chxmlnseCH_01295personWithSecondaryResidence', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 964, 3), )

    
    personWithSecondaryResidence = property(__personWithSecondaryResidence.value, __personWithSecondaryResidence.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}dateFirstOccupancy uses Python identifier dateFirstOccupancy
    __dateFirstOccupancy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateFirstOccupancy'), 'dateFirstOccupancy', '__httpwww_ech_chxmlnseCH_01295_dwellingUsageType_httpwww_ech_chxmlnseCH_01295dateFirstOccupancy', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 965, 3), )

    
    dateFirstOccupancy = property(__dateFirstOccupancy.value, __dateFirstOccupancy.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}dateLastOccupancy uses Python identifier dateLastOccupancy
    __dateLastOccupancy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateLastOccupancy'), 'dateLastOccupancy', '__httpwww_ech_chxmlnseCH_01295_dwellingUsageType_httpwww_ech_chxmlnseCH_01295dateLastOccupancy', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 972, 3), )

    
    dateLastOccupancy = property(__dateLastOccupancy.value, __dateLastOccupancy.set, None, None)

    _ElementMap.update({
        __usageCode.name() : __usageCode,
        __informationSource.name() : __informationSource,
        __revisionDate.name() : __revisionDate,
        __remark.name() : __remark,
        __personWithMainResidence.name() : __personWithMainResidence,
        __personWithSecondaryResidence.name() : __personWithSecondaryResidence,
        __dateFirstOccupancy.name() : __dateFirstOccupancy,
        __dateLastOccupancy.name() : __dateLastOccupancy
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.dwellingUsageType = dwellingUsageType
Namespace.addCategoryObject('typeBinding', 'dwellingUsageType', dwellingUsageType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}dwellingType with content type ELEMENT_ONLY
class dwellingType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}dwellingType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dwellingType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 981, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295localID', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 983, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}administrativeDwellingNo uses Python identifier administrativeDwellingNo
    __administrativeDwellingNo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'administrativeDwellingNo'), 'administrativeDwellingNo', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295administrativeDwellingNo', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 984, 3), )

    
    administrativeDwellingNo = property(__administrativeDwellingNo.value, __administrativeDwellingNo.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EWID uses Python identifier EWID
    __EWID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EWID'), 'EWID', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295EWID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 985, 3), )

    
    EWID = property(__EWID.value, __EWID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}physicalDwellingNo uses Python identifier physicalDwellingNo
    __physicalDwellingNo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'physicalDwellingNo'), 'physicalDwellingNo', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295physicalDwellingNo', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 986, 3), )

    
    physicalDwellingNo = property(__physicalDwellingNo.value, __physicalDwellingNo.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}dateOfConstruction uses Python identifier dateOfConstruction
    __dateOfConstruction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateOfConstruction'), 'dateOfConstruction', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295dateOfConstruction', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 987, 3), )

    
    dateOfConstruction = property(__dateOfConstruction.value, __dateOfConstruction.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}dateOfDemolition uses Python identifier dateOfDemolition
    __dateOfDemolition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateOfDemolition'), 'dateOfDemolition', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295dateOfDemolition', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 988, 3), )

    
    dateOfDemolition = property(__dateOfDemolition.value, __dateOfDemolition.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}noOfHabitableRooms uses Python identifier noOfHabitableRooms
    __noOfHabitableRooms = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'noOfHabitableRooms'), 'noOfHabitableRooms', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295noOfHabitableRooms', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 989, 3), )

    
    noOfHabitableRooms = property(__noOfHabitableRooms.value, __noOfHabitableRooms.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}floor uses Python identifier floor
    __floor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'floor'), 'floor', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295floor', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 990, 3), )

    
    floor = property(__floor.value, __floor.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}locationOfDwellingOnFloor uses Python identifier locationOfDwellingOnFloor
    __locationOfDwellingOnFloor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'locationOfDwellingOnFloor'), 'locationOfDwellingOnFloor', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295locationOfDwellingOnFloor', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 991, 3), )

    
    locationOfDwellingOnFloor = property(__locationOfDwellingOnFloor.value, __locationOfDwellingOnFloor.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}multipleFloor uses Python identifier multipleFloor
    __multipleFloor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'multipleFloor'), 'multipleFloor', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295multipleFloor', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 992, 3), )

    
    multipleFloor = property(__multipleFloor.value, __multipleFloor.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}usageLimitation uses Python identifier usageLimitation
    __usageLimitation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'usageLimitation'), 'usageLimitation', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295usageLimitation', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 993, 3), )

    
    usageLimitation = property(__usageLimitation.value, __usageLimitation.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}kitchen uses Python identifier kitchen
    __kitchen = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'kitchen'), 'kitchen', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295kitchen', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 994, 3), )

    
    kitchen = property(__kitchen.value, __kitchen.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}surfaceAreaOfDwelling uses Python identifier surfaceAreaOfDwelling
    __surfaceAreaOfDwelling = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfDwelling'), 'surfaceAreaOfDwelling', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295surfaceAreaOfDwelling', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 995, 3), )

    
    surfaceAreaOfDwelling = property(__surfaceAreaOfDwelling.value, __surfaceAreaOfDwelling.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}status uses Python identifier status
    __status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'status'), 'status', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295status', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 996, 3), )

    
    status = property(__status.value, __status.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}dwellingUsage uses Python identifier dwellingUsage
    __dwellingUsage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dwellingUsage'), 'dwellingUsage', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295dwellingUsage', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 997, 3), )

    
    dwellingUsage = property(__dwellingUsage.value, __dwellingUsage.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}dwellingFreeText uses Python identifier dwellingFreeText
    __dwellingFreeText = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dwellingFreeText'), 'dwellingFreeText', '__httpwww_ech_chxmlnseCH_01295_dwellingType_httpwww_ech_chxmlnseCH_01295dwellingFreeText', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 998, 3), )

    
    dwellingFreeText = property(__dwellingFreeText.value, __dwellingFreeText.set, None, None)

    _ElementMap.update({
        __localID.name() : __localID,
        __administrativeDwellingNo.name() : __administrativeDwellingNo,
        __EWID.name() : __EWID,
        __physicalDwellingNo.name() : __physicalDwellingNo,
        __dateOfConstruction.name() : __dateOfConstruction,
        __dateOfDemolition.name() : __dateOfDemolition,
        __noOfHabitableRooms.name() : __noOfHabitableRooms,
        __floor.name() : __floor,
        __locationOfDwellingOnFloor.name() : __locationOfDwellingOnFloor,
        __multipleFloor.name() : __multipleFloor,
        __usageLimitation.name() : __usageLimitation,
        __kitchen.name() : __kitchen,
        __surfaceAreaOfDwelling.name() : __surfaceAreaOfDwelling,
        __status.name() : __status,
        __dwellingUsage.name() : __dwellingUsage,
        __dwellingFreeText.name() : __dwellingFreeText
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.dwellingType = dwellingType
Namespace.addCategoryObject('typeBinding', 'dwellingType', dwellingType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}realestateIdentificationType with content type ELEMENT_ONLY
class realestateIdentificationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}realestateIdentificationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'realestateIdentificationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1021, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EGRID uses Python identifier EGRID
    __EGRID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EGRID'), 'EGRID', '__httpwww_ech_chxmlnseCH_01295_realestateIdentificationType_httpwww_ech_chxmlnseCH_01295EGRID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1023, 3), )

    
    EGRID = property(__EGRID.value, __EGRID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}number uses Python identifier number
    __number = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'number'), 'number', '__httpwww_ech_chxmlnseCH_01295_realestateIdentificationType_httpwww_ech_chxmlnseCH_01295number', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1028, 3), )

    
    number = property(__number.value, __number.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}numberSuffix uses Python identifier numberSuffix
    __numberSuffix = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'numberSuffix'), 'numberSuffix', '__httpwww_ech_chxmlnseCH_01295_realestateIdentificationType_httpwww_ech_chxmlnseCH_01295numberSuffix', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1036, 3), )

    
    numberSuffix = property(__numberSuffix.value, __numberSuffix.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}subDistrict uses Python identifier subDistrict
    __subDistrict = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subDistrict'), 'subDistrict', '__httpwww_ech_chxmlnseCH_01295_realestateIdentificationType_httpwww_ech_chxmlnseCH_01295subDistrict', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1044, 3), )

    
    subDistrict = property(__subDistrict.value, __subDistrict.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}lot uses Python identifier lot
    __lot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'lot'), 'lot', '__httpwww_ech_chxmlnseCH_01295_realestateIdentificationType_httpwww_ech_chxmlnseCH_01295lot', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1052, 3), )

    
    lot = property(__lot.value, __lot.set, None, None)

    _ElementMap.update({
        __EGRID.name() : __EGRID,
        __number.name() : __number,
        __numberSuffix.name() : __numberSuffix,
        __subDistrict.name() : __subDistrict,
        __lot.name() : __lot
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.realestateIdentificationType = realestateIdentificationType
Namespace.addCategoryObject('typeBinding', 'realestateIdentificationType', realestateIdentificationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}realestateType with content type ELEMENT_ONLY
class realestateType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}realestateType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'realestateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1119, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}realestateIdentification uses Python identifier realestateIdentification
    __realestateIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'realestateIdentification'), 'realestateIdentification', '__httpwww_ech_chxmlnseCH_01295_realestateType_httpwww_ech_chxmlnseCH_01295realestateIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1121, 3), )

    
    realestateIdentification = property(__realestateIdentification.value, __realestateIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}authority uses Python identifier authority
    __authority = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'authority'), 'authority', '__httpwww_ech_chxmlnseCH_01295_realestateType_httpwww_ech_chxmlnseCH_01295authority', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1122, 3), )

    
    authority = property(__authority.value, __authority.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}date uses Python identifier date
    __date = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'date'), 'date', '__httpwww_ech_chxmlnseCH_01295_realestateType_httpwww_ech_chxmlnseCH_01295date', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1123, 3), )

    
    date = property(__date.value, __date.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}realestateType uses Python identifier realestateType
    __realestateType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'realestateType'), 'realestateType', '__httpwww_ech_chxmlnseCH_01295_realestateType_httpwww_ech_chxmlnseCH_01295realestateType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1124, 3), )

    
    realestateType = property(__realestateType.value, __realestateType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}cantonalSubKind uses Python identifier cantonalSubKind
    __cantonalSubKind = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'cantonalSubKind'), 'cantonalSubKind', '__httpwww_ech_chxmlnseCH_01295_realestateType_httpwww_ech_chxmlnseCH_01295cantonalSubKind', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1125, 3), )

    
    cantonalSubKind = property(__cantonalSubKind.value, __cantonalSubKind.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}status uses Python identifier status
    __status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'status'), 'status', '__httpwww_ech_chxmlnseCH_01295_realestateType_httpwww_ech_chxmlnseCH_01295status', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1126, 3), )

    
    status = property(__status.value, __status.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}mutnumber uses Python identifier mutnumber
    __mutnumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'mutnumber'), 'mutnumber', '__httpwww_ech_chxmlnseCH_01295_realestateType_httpwww_ech_chxmlnseCH_01295mutnumber', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1127, 3), )

    
    mutnumber = property(__mutnumber.value, __mutnumber.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}identDN uses Python identifier identDN
    __identDN = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'identDN'), 'identDN', '__httpwww_ech_chxmlnseCH_01295_realestateType_httpwww_ech_chxmlnseCH_01295identDN', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1128, 3), )

    
    identDN = property(__identDN.value, __identDN.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}squareMeasure uses Python identifier squareMeasure
    __squareMeasure = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'squareMeasure'), 'squareMeasure', '__httpwww_ech_chxmlnseCH_01295_realestateType_httpwww_ech_chxmlnseCH_01295squareMeasure', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1129, 3), )

    
    squareMeasure = property(__squareMeasure.value, __squareMeasure.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}realestateIncomplete uses Python identifier realestateIncomplete
    __realestateIncomplete = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'realestateIncomplete'), 'realestateIncomplete', '__httpwww_ech_chxmlnseCH_01295_realestateType_httpwww_ech_chxmlnseCH_01295realestateIncomplete', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1130, 3), )

    
    realestateIncomplete = property(__realestateIncomplete.value, __realestateIncomplete.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}coordinates uses Python identifier coordinates
    __coordinates = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'coordinates'), 'coordinates', '__httpwww_ech_chxmlnseCH_01295_realestateType_httpwww_ech_chxmlnseCH_01295coordinates', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1131, 3), )

    
    coordinates = property(__coordinates.value, __coordinates.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}namedMetaData uses Python identifier namedMetaData
    __namedMetaData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'namedMetaData'), 'namedMetaData', '__httpwww_ech_chxmlnseCH_01295_realestateType_httpwww_ech_chxmlnseCH_01295namedMetaData', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1132, 3), )

    
    namedMetaData = property(__namedMetaData.value, __namedMetaData.set, None, None)

    _ElementMap.update({
        __realestateIdentification.name() : __realestateIdentification,
        __authority.name() : __authority,
        __date.name() : __date,
        __realestateType.name() : __realestateType,
        __cantonalSubKind.name() : __cantonalSubKind,
        __status.name() : __status,
        __mutnumber.name() : __mutnumber,
        __identDN.name() : __identDN,
        __squareMeasure.name() : __squareMeasure,
        __realestateIncomplete.name() : __realestateIncomplete,
        __coordinates.name() : __coordinates,
        __namedMetaData.name() : __namedMetaData
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.realestateType = realestateType
Namespace.addCategoryObject('typeBinding', 'realestateType', realestateType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}localityNameType with content type ELEMENT_ONLY
class localityNameType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}localityNameType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'localityNameType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1148, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}language uses Python identifier language
    __language = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'language'), 'language', '__httpwww_ech_chxmlnseCH_01295_localityNameType_httpwww_ech_chxmlnseCH_01295language', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1150, 3), )

    
    language = property(__language.value, __language.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}nameLong uses Python identifier nameLong
    __nameLong = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'nameLong'), 'nameLong', '__httpwww_ech_chxmlnseCH_01295_localityNameType_httpwww_ech_chxmlnseCH_01295nameLong', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1151, 3), )

    
    nameLong = property(__nameLong.value, __nameLong.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}nameShort uses Python identifier nameShort
    __nameShort = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'nameShort'), 'nameShort', '__httpwww_ech_chxmlnseCH_01295_localityNameType_httpwww_ech_chxmlnseCH_01295nameShort', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1159, 3), )

    
    nameShort = property(__nameShort.value, __nameShort.set, None, None)

    _ElementMap.update({
        __language.name() : __language,
        __nameLong.name() : __nameLong,
        __nameShort.name() : __nameShort
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.localityNameType = localityNameType
Namespace.addCategoryObject('typeBinding', 'localityNameType', localityNameType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}localityType with content type ELEMENT_ONLY
class localityType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}localityType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'localityType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1169, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}swissZipCode uses Python identifier swissZipCode
    __swissZipCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'swissZipCode'), 'swissZipCode', '__httpwww_ech_chxmlnseCH_01295_localityType_httpwww_ech_chxmlnseCH_01295swissZipCode', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1171, 3), )

    
    swissZipCode = property(__swissZipCode.value, __swissZipCode.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}swissZipCodeAddOn uses Python identifier swissZipCodeAddOn
    __swissZipCodeAddOn = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'swissZipCodeAddOn'), 'swissZipCodeAddOn', '__httpwww_ech_chxmlnseCH_01295_localityType_httpwww_ech_chxmlnseCH_01295swissZipCodeAddOn', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1172, 3), )

    
    swissZipCodeAddOn = property(__swissZipCodeAddOn.value, __swissZipCodeAddOn.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'name'), 'name', '__httpwww_ech_chxmlnseCH_01295_localityType_httpwww_ech_chxmlnseCH_01295name', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1173, 3), )

    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        __swissZipCode.name() : __swissZipCode,
        __swissZipCodeAddOn.name() : __swissZipCodeAddOn,
        __name.name() : __name
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.localityType = localityType
Namespace.addCategoryObject('typeBinding', 'localityType', localityType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}fiscalOwnershipType with content type ELEMENT_ONLY
class fiscalOwnershipType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}fiscalOwnershipType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'fiscalOwnershipType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1177, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}accessionDate uses Python identifier accessionDate
    __accessionDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'accessionDate'), 'accessionDate', '__httpwww_ech_chxmlnseCH_01295_fiscalOwnershipType_httpwww_ech_chxmlnseCH_01295accessionDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1179, 3), )

    
    accessionDate = property(__accessionDate.value, __accessionDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}fiscalRelationship uses Python identifier fiscalRelationship
    __fiscalRelationship = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'fiscalRelationship'), 'fiscalRelationship', '__httpwww_ech_chxmlnseCH_01295_fiscalOwnershipType_httpwww_ech_chxmlnseCH_01295fiscalRelationship', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1180, 3), )

    
    fiscalRelationship = property(__fiscalRelationship.value, __fiscalRelationship.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}validFrom uses Python identifier validFrom
    __validFrom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'validFrom'), 'validFrom', '__httpwww_ech_chxmlnseCH_01295_fiscalOwnershipType_httpwww_ech_chxmlnseCH_01295validFrom', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1189, 3), )

    
    validFrom = property(__validFrom.value, __validFrom.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}validTill uses Python identifier validTill
    __validTill = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'validTill'), 'validTill', '__httpwww_ech_chxmlnseCH_01295_fiscalOwnershipType_httpwww_ech_chxmlnseCH_01295validTill', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1190, 3), )

    
    validTill = property(__validTill.value, __validTill.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}denominator uses Python identifier denominator
    __denominator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'denominator'), 'denominator', '__httpwww_ech_chxmlnseCH_01295_fiscalOwnershipType_httpwww_ech_chxmlnseCH_01295denominator', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1191, 3), )

    
    denominator = property(__denominator.value, __denominator.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}tally uses Python identifier tally
    __tally = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'tally'), 'tally', '__httpwww_ech_chxmlnseCH_01295_fiscalOwnershipType_httpwww_ech_chxmlnseCH_01295tally', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1201, 3), )

    
    tally = property(__tally.value, __tally.set, None, None)

    _ElementMap.update({
        __accessionDate.name() : __accessionDate,
        __fiscalRelationship.name() : __fiscalRelationship,
        __validFrom.name() : __validFrom,
        __validTill.name() : __validTill,
        __denominator.name() : __denominator,
        __tally.name() : __tally
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.fiscalOwnershipType = fiscalOwnershipType
Namespace.addCategoryObject('typeBinding', 'fiscalOwnershipType', fiscalOwnershipType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}areaType with content type ELEMENT_ONLY
class areaType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}areaType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'areaType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1265, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}areaType uses Python identifier areaType
    __areaType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'areaType'), 'areaType', '__httpwww_ech_chxmlnseCH_01295_areaType_httpwww_ech_chxmlnseCH_01295areaType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1267, 3), )

    
    areaType = property(__areaType.value, __areaType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}areaDescriptionCode uses Python identifier areaDescriptionCode
    __areaDescriptionCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'areaDescriptionCode'), 'areaDescriptionCode', '__httpwww_ech_chxmlnseCH_01295_areaType_httpwww_ech_chxmlnseCH_01295areaDescriptionCode', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1268, 3), )

    
    areaDescriptionCode = property(__areaDescriptionCode.value, __areaDescriptionCode.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}areaDescription uses Python identifier areaDescription
    __areaDescription = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'areaDescription'), 'areaDescription', '__httpwww_ech_chxmlnseCH_01295_areaType_httpwww_ech_chxmlnseCH_01295areaDescription', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1269, 3), )

    
    areaDescription = property(__areaDescription.value, __areaDescription.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}areaValue uses Python identifier areaValue
    __areaValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'areaValue'), 'areaValue', '__httpwww_ech_chxmlnseCH_01295_areaType_httpwww_ech_chxmlnseCH_01295areaValue', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1270, 3), )

    
    areaValue = property(__areaValue.value, __areaValue.set, None, None)

    _ElementMap.update({
        __areaType.name() : __areaType,
        __areaDescriptionCode.name() : __areaDescriptionCode,
        __areaDescription.name() : __areaDescription,
        __areaValue.name() : __areaValue
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.areaType = areaType
Namespace.addCategoryObject('typeBinding', 'areaType', areaType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}insuranceSumType with content type ELEMENT_ONLY
class insuranceSumType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}insuranceSumType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'insuranceSumType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1296, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}amount uses Python identifier amount
    __amount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'amount'), 'amount', '__httpwww_ech_chxmlnseCH_01295_insuranceSumType_httpwww_ech_chxmlnseCH_01295amount', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1298, 3), )

    
    amount = property(__amount.value, __amount.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}percentage uses Python identifier percentage
    __percentage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'percentage'), 'percentage', '__httpwww_ech_chxmlnseCH_01295_insuranceSumType_httpwww_ech_chxmlnseCH_01295percentage', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1306, 3), )

    
    percentage = property(__percentage.value, __percentage.set, None, None)

    _ElementMap.update({
        __amount.name() : __amount,
        __percentage.name() : __percentage
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.insuranceSumType = insuranceSumType
Namespace.addCategoryObject('typeBinding', 'insuranceSumType', insuranceSumType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}insuranceValueType with content type ELEMENT_ONLY
class insuranceValueType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}insuranceValueType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'insuranceValueType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1326, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_01295_insuranceValueType_httpwww_ech_chxmlnseCH_01295localID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1328, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}validFrom uses Python identifier validFrom
    __validFrom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'validFrom'), 'validFrom', '__httpwww_ech_chxmlnseCH_01295_insuranceValueType_httpwww_ech_chxmlnseCH_01295validFrom', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1329, 3), )

    
    validFrom = property(__validFrom.value, __validFrom.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}changeReason uses Python identifier changeReason
    __changeReason = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'changeReason'), 'changeReason', '__httpwww_ech_chxmlnseCH_01295_insuranceValueType_httpwww_ech_chxmlnseCH_01295changeReason', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1330, 3), )

    
    changeReason = property(__changeReason.value, __changeReason.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}insuranceSum uses Python identifier insuranceSum
    __insuranceSum = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'insuranceSum'), 'insuranceSum', '__httpwww_ech_chxmlnseCH_01295_insuranceValueType_httpwww_ech_chxmlnseCH_01295insuranceSum', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1331, 3), )

    
    insuranceSum = property(__insuranceSum.value, __insuranceSum.set, None, None)

    _ElementMap.update({
        __localID.name() : __localID,
        __validFrom.name() : __validFrom,
        __changeReason.name() : __changeReason,
        __insuranceSum.name() : __insuranceSum
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.insuranceValueType = insuranceValueType
Namespace.addCategoryObject('typeBinding', 'insuranceValueType', insuranceValueType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}insuranceVolumeType with content type ELEMENT_ONLY
class insuranceVolumeType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}insuranceVolumeType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'insuranceVolumeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1334, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}volume uses Python identifier volume
    __volume = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'volume'), 'volume', '__httpwww_ech_chxmlnseCH_01295_insuranceVolumeType_httpwww_ech_chxmlnseCH_01295volume', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1336, 3), )

    
    volume = property(__volume.value, __volume.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}norm uses Python identifier norm
    __norm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'norm'), 'norm', '__httpwww_ech_chxmlnseCH_01295_insuranceVolumeType_httpwww_ech_chxmlnseCH_01295norm', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1344, 3), )

    
    norm = property(__norm.value, __norm.set, None, None)

    _ElementMap.update({
        __volume.name() : __volume,
        __norm.name() : __norm
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.insuranceVolumeType = insuranceVolumeType
Namespace.addCategoryObject('typeBinding', 'insuranceVolumeType', insuranceVolumeType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}insuranceObjectType with content type ELEMENT_ONLY
class insuranceObjectType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}insuranceObjectType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'insuranceObjectType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1347, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_01295_insuranceObjectType_httpwww_ech_chxmlnseCH_01295localID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1349, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}startDate uses Python identifier startDate
    __startDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'startDate'), 'startDate', '__httpwww_ech_chxmlnseCH_01295_insuranceObjectType_httpwww_ech_chxmlnseCH_01295startDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1350, 3), )

    
    startDate = property(__startDate.value, __startDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}endDate uses Python identifier endDate
    __endDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'endDate'), 'endDate', '__httpwww_ech_chxmlnseCH_01295_insuranceObjectType_httpwww_ech_chxmlnseCH_01295endDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1351, 3), )

    
    endDate = property(__endDate.value, __endDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}insuranceNumber uses Python identifier insuranceNumber
    __insuranceNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'insuranceNumber'), 'insuranceNumber', '__httpwww_ech_chxmlnseCH_01295_insuranceObjectType_httpwww_ech_chxmlnseCH_01295insuranceNumber', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1352, 3), )

    
    insuranceNumber = property(__insuranceNumber.value, __insuranceNumber.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}usageCode uses Python identifier usageCode
    __usageCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'usageCode'), 'usageCode', '__httpwww_ech_chxmlnseCH_01295_insuranceObjectType_httpwww_ech_chxmlnseCH_01295usageCode', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1353, 3), )

    
    usageCode = property(__usageCode.value, __usageCode.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}usageDescription uses Python identifier usageDescription
    __usageDescription = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'usageDescription'), 'usageDescription', '__httpwww_ech_chxmlnseCH_01295_insuranceObjectType_httpwww_ech_chxmlnseCH_01295usageDescription', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1354, 3), )

    
    usageDescription = property(__usageDescription.value, __usageDescription.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}insuranceValue uses Python identifier insuranceValue
    __insuranceValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'insuranceValue'), 'insuranceValue', '__httpwww_ech_chxmlnseCH_01295_insuranceObjectType_httpwww_ech_chxmlnseCH_01295insuranceValue', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1355, 3), )

    
    insuranceValue = property(__insuranceValue.value, __insuranceValue.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}volume uses Python identifier volume
    __volume = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'volume'), 'volume', '__httpwww_ech_chxmlnseCH_01295_insuranceObjectType_httpwww_ech_chxmlnseCH_01295volume', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1356, 3), )

    
    volume = property(__volume.value, __volume.set, None, None)

    _ElementMap.update({
        __localID.name() : __localID,
        __startDate.name() : __startDate,
        __endDate.name() : __endDate,
        __insuranceNumber.name() : __insuranceNumber,
        __usageCode.name() : __usageCode,
        __usageDescription.name() : __usageDescription,
        __insuranceValue.name() : __insuranceValue,
        __volume.name() : __volume
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.insuranceObjectType = insuranceObjectType
Namespace.addCategoryObject('typeBinding', 'insuranceObjectType', insuranceObjectType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}streetType with content type ELEMENT_ONLY
class streetType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}streetType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'streetType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1434, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}ESID uses Python identifier ESID
    __ESID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ESID'), 'ESID', '__httpwww_ech_chxmlnseCH_01295_streetType_httpwww_ech_chxmlnseCH_01295ESID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1436, 3), )

    
    ESID = property(__ESID.value, __ESID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}isOfficialDescription uses Python identifier isOfficialDescription
    __isOfficialDescription = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'isOfficialDescription'), 'isOfficialDescription', '__httpwww_ech_chxmlnseCH_01295_streetType_httpwww_ech_chxmlnseCH_01295isOfficialDescription', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1437, 3), )

    
    isOfficialDescription = property(__isOfficialDescription.value, __isOfficialDescription.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}officialStreetNumber uses Python identifier officialStreetNumber
    __officialStreetNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'officialStreetNumber'), 'officialStreetNumber', '__httpwww_ech_chxmlnseCH_01295_streetType_httpwww_ech_chxmlnseCH_01295officialStreetNumber', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1438, 3), )

    
    officialStreetNumber = property(__officialStreetNumber.value, __officialStreetNumber.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_01295_streetType_httpwww_ech_chxmlnseCH_01295localID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1439, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}streetKind uses Python identifier streetKind
    __streetKind = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'streetKind'), 'streetKind', '__httpwww_ech_chxmlnseCH_01295_streetType_httpwww_ech_chxmlnseCH_01295streetKind', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1440, 3), )

    
    streetKind = property(__streetKind.value, __streetKind.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpwww_ech_chxmlnseCH_01295_streetType_httpwww_ech_chxmlnseCH_01295description', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1441, 3), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}streetStatus uses Python identifier streetStatus
    __streetStatus = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'streetStatus'), 'streetStatus', '__httpwww_ech_chxmlnseCH_01295_streetType_httpwww_ech_chxmlnseCH_01295streetStatus', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1442, 3), )

    
    streetStatus = property(__streetStatus.value, __streetStatus.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}streetGeometry uses Python identifier streetGeometry
    __streetGeometry = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'streetGeometry'), 'streetGeometry', '__httpwww_ech_chxmlnseCH_01295_streetType_httpwww_ech_chxmlnseCH_01295streetGeometry', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1443, 3), )

    
    streetGeometry = property(__streetGeometry.value, __streetGeometry.set, None, None)

    _ElementMap.update({
        __ESID.name() : __ESID,
        __isOfficialDescription.name() : __isOfficialDescription,
        __officialStreetNumber.name() : __officialStreetNumber,
        __localID.name() : __localID,
        __streetKind.name() : __streetKind,
        __description.name() : __description,
        __streetStatus.name() : __streetStatus,
        __streetGeometry.name() : __streetGeometry
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.streetType = streetType
Namespace.addCategoryObject('typeBinding', 'streetType', streetType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}streetSectionType with content type ELEMENT_ONLY
class streetSectionType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}streetSectionType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'streetSectionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1446, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}ESID uses Python identifier ESID
    __ESID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ESID'), 'ESID', '__httpwww_ech_chxmlnseCH_01295_streetSectionType_httpwww_ech_chxmlnseCH_01295ESID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1448, 3), )

    
    ESID = property(__ESID.value, __ESID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}swissZipCode uses Python identifier swissZipCode
    __swissZipCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'swissZipCode'), 'swissZipCode', '__httpwww_ech_chxmlnseCH_01295_streetSectionType_httpwww_ech_chxmlnseCH_01295swissZipCode', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1449, 3), )

    
    swissZipCode = property(__swissZipCode.value, __swissZipCode.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}swissZipCodeAddOn uses Python identifier swissZipCodeAddOn
    __swissZipCodeAddOn = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'swissZipCodeAddOn'), 'swissZipCodeAddOn', '__httpwww_ech_chxmlnseCH_01295_streetSectionType_httpwww_ech_chxmlnseCH_01295swissZipCodeAddOn', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1450, 3), )

    
    swissZipCodeAddOn = property(__swissZipCodeAddOn.value, __swissZipCodeAddOn.set, None, None)

    _ElementMap.update({
        __ESID.name() : __ESID,
        __swissZipCode.name() : __swissZipCode,
        __swissZipCodeAddOn.name() : __swissZipCodeAddOn
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.streetSectionType = streetSectionType
Namespace.addCategoryObject('typeBinding', 'streetSectionType', streetSectionType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}streetDescriptionType with content type ELEMENT_ONLY
class streetDescriptionType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}streetDescriptionType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'streetDescriptionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1462, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}language uses Python identifier language
    __language = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'language'), 'language', '__httpwww_ech_chxmlnseCH_01295_streetDescriptionType_httpwww_ech_chxmlnseCH_01295language', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1464, 3), )

    
    language = property(__language.value, __language.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}descriptionLong uses Python identifier descriptionLong
    __descriptionLong = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'descriptionLong'), 'descriptionLong', '__httpwww_ech_chxmlnseCH_01295_streetDescriptionType_httpwww_ech_chxmlnseCH_01295descriptionLong', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1465, 3), )

    
    descriptionLong = property(__descriptionLong.value, __descriptionLong.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}descriptionShort uses Python identifier descriptionShort
    __descriptionShort = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'descriptionShort'), 'descriptionShort', '__httpwww_ech_chxmlnseCH_01295_streetDescriptionType_httpwww_ech_chxmlnseCH_01295descriptionShort', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1466, 3), )

    
    descriptionShort = property(__descriptionShort.value, __descriptionShort.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}descriptionIndex uses Python identifier descriptionIndex
    __descriptionIndex = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'descriptionIndex'), 'descriptionIndex', '__httpwww_ech_chxmlnseCH_01295_streetDescriptionType_httpwww_ech_chxmlnseCH_01295descriptionIndex', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1467, 3), )

    
    descriptionIndex = property(__descriptionIndex.value, __descriptionIndex.set, None, None)

    _ElementMap.update({
        __language.name() : __language,
        __descriptionLong.name() : __descriptionLong,
        __descriptionShort.name() : __descriptionShort,
        __descriptionIndex.name() : __descriptionIndex
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.streetDescriptionType = streetDescriptionType
Namespace.addCategoryObject('typeBinding', 'streetDescriptionType', streetDescriptionType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}rightType with content type ELEMENT_ONLY
class rightType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}rightType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'rightType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1473, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}EREID uses Python identifier EREID
    __EREID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EREID'), 'EREID', '__httpwww_ech_chxmlnseCH_01295_rightType_httpwww_ech_chxmlnseCH_01295EREID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1475, 3), )

    
    EREID = property(__EREID.value, __EREID.set, None, None)

    _ElementMap.update({
        __EREID.name() : __EREID
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.rightType = rightType
Namespace.addCategoryObject('typeBinding', 'rightType', rightType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}cadastralMapType with content type ELEMENT_ONLY
class cadastralMapType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}cadastralMapType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'cadastralMapType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1485, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}mapNumber uses Python identifier mapNumber
    __mapNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'mapNumber'), 'mapNumber', '__httpwww_ech_chxmlnseCH_01295_cadastralMapType_httpwww_ech_chxmlnseCH_01295mapNumber', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1487, 3), )

    
    mapNumber = property(__mapNumber.value, __mapNumber.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}identDN uses Python identifier identDN
    __identDN = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'identDN'), 'identDN', '__httpwww_ech_chxmlnseCH_01295_cadastralMapType_httpwww_ech_chxmlnseCH_01295identDN', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1488, 3), )

    
    identDN = property(__identDN.value, __identDN.set, None, None)

    _ElementMap.update({
        __mapNumber.name() : __mapNumber,
        __identDN.name() : __identDN
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.cadastralMapType = cadastralMapType
Namespace.addCategoryObject('typeBinding', 'cadastralMapType', cadastralMapType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}cadastralSurveyorRemarkType with content type ELEMENT_ONLY
class cadastralSurveyorRemarkType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}cadastralSurveyorRemarkType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'cadastralSurveyorRemarkType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1511, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}remarkType uses Python identifier remarkType
    __remarkType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remarkType'), 'remarkType', '__httpwww_ech_chxmlnseCH_01295_cadastralSurveyorRemarkType_httpwww_ech_chxmlnseCH_01295remarkType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1513, 3), )

    
    remarkType = property(__remarkType.value, __remarkType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}remarkOtherType uses Python identifier remarkOtherType
    __remarkOtherType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remarkOtherType'), 'remarkOtherType', '__httpwww_ech_chxmlnseCH_01295_cadastralSurveyorRemarkType_httpwww_ech_chxmlnseCH_01295remarkOtherType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1514, 3), )

    
    remarkOtherType = property(__remarkOtherType.value, __remarkOtherType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}remarkText uses Python identifier remarkText
    __remarkText = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remarkText'), 'remarkText', '__httpwww_ech_chxmlnseCH_01295_cadastralSurveyorRemarkType_httpwww_ech_chxmlnseCH_01295remarkText', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1515, 3), )

    
    remarkText = property(__remarkText.value, __remarkText.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}objectID uses Python identifier objectID
    __objectID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'objectID'), 'objectID', '__httpwww_ech_chxmlnseCH_01295_cadastralSurveyorRemarkType_httpwww_ech_chxmlnseCH_01295objectID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1516, 3), )

    
    objectID = property(__objectID.value, __objectID.set, None, None)

    _ElementMap.update({
        __remarkType.name() : __remarkType,
        __remarkOtherType.name() : __remarkOtherType,
        __remarkText.name() : __remarkText,
        __objectID.name() : __objectID
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.cadastralSurveyorRemarkType = cadastralSurveyorRemarkType
Namespace.addCategoryObject('typeBinding', 'cadastralSurveyorRemarkType', cadastralSurveyorRemarkType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}placeNameType with content type ELEMENT_ONLY
class placeNameType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}placeNameType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'placeNameType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1531, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}placeNameType uses Python identifier placeNameType
    __placeNameType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'placeNameType'), 'placeNameType', '__httpwww_ech_chxmlnseCH_01295_placeNameType_httpwww_ech_chxmlnseCH_01295placeNameType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1533, 3), )

    
    placeNameType = property(__placeNameType.value, __placeNameType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localGeographicalName uses Python identifier localGeographicalName
    __localGeographicalName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localGeographicalName'), 'localGeographicalName', '__httpwww_ech_chxmlnseCH_01295_placeNameType_httpwww_ech_chxmlnseCH_01295localGeographicalName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1534, 3), )

    
    localGeographicalName = property(__localGeographicalName.value, __localGeographicalName.set, None, None)

    _ElementMap.update({
        __placeNameType.name() : __placeNameType,
        __localGeographicalName.name() : __localGeographicalName
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.placeNameType = placeNameType
Namespace.addCategoryObject('typeBinding', 'placeNameType', placeNameType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}coveringAreaOfSDRType with content type ELEMENT_ONLY
class coveringAreaOfSDRType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}coveringAreaOfSDRType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'coveringAreaOfSDRType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1538, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}squareMeasure uses Python identifier squareMeasure
    __squareMeasure = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'squareMeasure'), 'squareMeasure', '__httpwww_ech_chxmlnseCH_01295_coveringAreaOfSDRType_httpwww_ech_chxmlnseCH_01295squareMeasure', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1540, 3), )

    
    squareMeasure = property(__squareMeasure.value, __squareMeasure.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}realestateIdentification uses Python identifier realestateIdentification
    __realestateIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'realestateIdentification'), 'realestateIdentification', '__httpwww_ech_chxmlnseCH_01295_coveringAreaOfSDRType_httpwww_ech_chxmlnseCH_01295realestateIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1541, 3), )

    
    realestateIdentification = property(__realestateIdentification.value, __realestateIdentification.set, None, None)

    _ElementMap.update({
        __squareMeasure.name() : __squareMeasure,
        __realestateIdentification.name() : __realestateIdentification
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.coveringAreaOfSDRType = coveringAreaOfSDRType
Namespace.addCategoryObject('typeBinding', 'coveringAreaOfSDRType', coveringAreaOfSDRType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}partialAreaOfBuildingType with content type ELEMENT_ONLY
class partialAreaOfBuildingType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}partialAreaOfBuildingType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'partialAreaOfBuildingType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1545, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}squareMeasure uses Python identifier squareMeasure
    __squareMeasure = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'squareMeasure'), 'squareMeasure', '__httpwww_ech_chxmlnseCH_01295_partialAreaOfBuildingType_httpwww_ech_chxmlnseCH_01295squareMeasure', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1547, 3), )

    
    squareMeasure = property(__squareMeasure.value, __squareMeasure.set, None, None)

    _ElementMap.update({
        __squareMeasure.name() : __squareMeasure
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.partialAreaOfBuildingType = partialAreaOfBuildingType
Namespace.addCategoryObject('typeBinding', 'partialAreaOfBuildingType', partialAreaOfBuildingType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}kindOfConstructionWorkType with content type ELEMENT_ONLY
class kindOfConstructionWorkType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}kindOfConstructionWorkType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'kindOfConstructionWorkType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1558, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}kindOfWork uses Python identifier kindOfWork
    __kindOfWork = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'kindOfWork'), 'kindOfWork', '__httpwww_ech_chxmlnseCH_01295_kindOfConstructionWorkType_httpwww_ech_chxmlnseCH_01295kindOfWork', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1560, 3), )

    
    kindOfWork = property(__kindOfWork.value, __kindOfWork.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}energeticRestauration uses Python identifier energeticRestauration
    __energeticRestauration = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'energeticRestauration'), 'energeticRestauration', '__httpwww_ech_chxmlnseCH_01295_kindOfConstructionWorkType_httpwww_ech_chxmlnseCH_01295energeticRestauration', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1561, 3), )

    
    energeticRestauration = property(__energeticRestauration.value, __energeticRestauration.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}renovationHeatingsystem uses Python identifier renovationHeatingsystem
    __renovationHeatingsystem = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'renovationHeatingsystem'), 'renovationHeatingsystem', '__httpwww_ech_chxmlnseCH_01295_kindOfConstructionWorkType_httpwww_ech_chxmlnseCH_01295renovationHeatingsystem', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1562, 3), )

    
    renovationHeatingsystem = property(__renovationHeatingsystem.value, __renovationHeatingsystem.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}innerConversionRenovation uses Python identifier innerConversionRenovation
    __innerConversionRenovation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'innerConversionRenovation'), 'innerConversionRenovation', '__httpwww_ech_chxmlnseCH_01295_kindOfConstructionWorkType_httpwww_ech_chxmlnseCH_01295innerConversionRenovation', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1563, 3), )

    
    innerConversionRenovation = property(__innerConversionRenovation.value, __innerConversionRenovation.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}conversion uses Python identifier conversion
    __conversion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'conversion'), 'conversion', '__httpwww_ech_chxmlnseCH_01295_kindOfConstructionWorkType_httpwww_ech_chxmlnseCH_01295conversion', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1564, 3), )

    
    conversion = property(__conversion.value, __conversion.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}extensionHeighteningHeated uses Python identifier extensionHeighteningHeated
    __extensionHeighteningHeated = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extensionHeighteningHeated'), 'extensionHeighteningHeated', '__httpwww_ech_chxmlnseCH_01295_kindOfConstructionWorkType_httpwww_ech_chxmlnseCH_01295extensionHeighteningHeated', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1565, 3), )

    
    extensionHeighteningHeated = property(__extensionHeighteningHeated.value, __extensionHeighteningHeated.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}extensionHeighteningNotHeated uses Python identifier extensionHeighteningNotHeated
    __extensionHeighteningNotHeated = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extensionHeighteningNotHeated'), 'extensionHeighteningNotHeated', '__httpwww_ech_chxmlnseCH_01295_kindOfConstructionWorkType_httpwww_ech_chxmlnseCH_01295extensionHeighteningNotHeated', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1566, 3), )

    
    extensionHeighteningNotHeated = property(__extensionHeighteningNotHeated.value, __extensionHeighteningNotHeated.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}thermicSolarFacility uses Python identifier thermicSolarFacility
    __thermicSolarFacility = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'thermicSolarFacility'), 'thermicSolarFacility', '__httpwww_ech_chxmlnseCH_01295_kindOfConstructionWorkType_httpwww_ech_chxmlnseCH_01295thermicSolarFacility', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1567, 3), )

    
    thermicSolarFacility = property(__thermicSolarFacility.value, __thermicSolarFacility.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}photovoltaicSolarFacility uses Python identifier photovoltaicSolarFacility
    __photovoltaicSolarFacility = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'photovoltaicSolarFacility'), 'photovoltaicSolarFacility', '__httpwww_ech_chxmlnseCH_01295_kindOfConstructionWorkType_httpwww_ech_chxmlnseCH_01295photovoltaicSolarFacility', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1568, 3), )

    
    photovoltaicSolarFacility = property(__photovoltaicSolarFacility.value, __photovoltaicSolarFacility.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}otherWorks uses Python identifier otherWorks
    __otherWorks = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherWorks'), 'otherWorks', '__httpwww_ech_chxmlnseCH_01295_kindOfConstructionWorkType_httpwww_ech_chxmlnseCH_01295otherWorks', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1569, 3), )

    
    otherWorks = property(__otherWorks.value, __otherWorks.set, None, None)

    _ElementMap.update({
        __kindOfWork.name() : __kindOfWork,
        __energeticRestauration.name() : __energeticRestauration,
        __renovationHeatingsystem.name() : __renovationHeatingsystem,
        __innerConversionRenovation.name() : __innerConversionRenovation,
        __conversion.name() : __conversion,
        __extensionHeighteningHeated.name() : __extensionHeighteningHeated,
        __extensionHeighteningNotHeated.name() : __extensionHeighteningNotHeated,
        __thermicSolarFacility.name() : __thermicSolarFacility,
        __photovoltaicSolarFacility.name() : __photovoltaicSolarFacility,
        __otherWorks.name() : __otherWorks
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.kindOfConstructionWorkType = kindOfConstructionWorkType
Namespace.addCategoryObject('typeBinding', 'kindOfConstructionWorkType', kindOfConstructionWorkType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}valueType with content type ELEMENT_ONLY
class valueType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}valueType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'valueType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1594, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}amount uses Python identifier amount
    __amount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'amount'), 'amount', '__httpwww_ech_chxmlnseCH_01295_valueType_httpwww_ech_chxmlnseCH_01295amount', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1596, 3), )

    
    amount = property(__amount.value, __amount.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}percentage uses Python identifier percentage
    __percentage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'percentage'), 'percentage', '__httpwww_ech_chxmlnseCH_01295_valueType_httpwww_ech_chxmlnseCH_01295percentage', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1604, 3), )

    
    percentage = property(__percentage.value, __percentage.set, None, None)

    _ElementMap.update({
        __amount.name() : __amount,
        __percentage.name() : __percentage
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.valueType = valueType
Namespace.addCategoryObject('typeBinding', 'valueType', valueType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}estimationValueType with content type ELEMENT_ONLY
class estimationValueType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}estimationValueType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'estimationValueType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1614, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_01295_estimationValueType_httpwww_ech_chxmlnseCH_01295localID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1616, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}baseYear uses Python identifier baseYear
    __baseYear = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'baseYear'), 'baseYear', '__httpwww_ech_chxmlnseCH_01295_estimationValueType_httpwww_ech_chxmlnseCH_01295baseYear', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1617, 3), )

    
    baseYear = property(__baseYear.value, __baseYear.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}validFrom uses Python identifier validFrom
    __validFrom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'validFrom'), 'validFrom', '__httpwww_ech_chxmlnseCH_01295_estimationValueType_httpwww_ech_chxmlnseCH_01295validFrom', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1625, 3), )

    
    validFrom = property(__validFrom.value, __validFrom.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}indexValue uses Python identifier indexValue
    __indexValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'indexValue'), 'indexValue', '__httpwww_ech_chxmlnseCH_01295_estimationValueType_httpwww_ech_chxmlnseCH_01295indexValue', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1626, 3), )

    
    indexValue = property(__indexValue.value, __indexValue.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}value uses Python identifier value_
    __value = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'value'), 'value_', '__httpwww_ech_chxmlnseCH_01295_estimationValueType_httpwww_ech_chxmlnseCH_01295value', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1634, 3), )

    
    value_ = property(__value.value, __value.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}typeOfvalue uses Python identifier typeOfvalue
    __typeOfvalue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'typeOfvalue'), 'typeOfvalue', '__httpwww_ech_chxmlnseCH_01295_estimationValueType_httpwww_ech_chxmlnseCH_01295typeOfvalue', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1635, 3), )

    
    typeOfvalue = property(__typeOfvalue.value, __typeOfvalue.set, None, None)

    _ElementMap.update({
        __localID.name() : __localID,
        __baseYear.name() : __baseYear,
        __validFrom.name() : __validFrom,
        __indexValue.name() : __indexValue,
        __value.name() : __value,
        __typeOfvalue.name() : __typeOfvalue
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.estimationValueType = estimationValueType
Namespace.addCategoryObject('typeBinding', 'estimationValueType', estimationValueType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}estimationObjectType with content type ELEMENT_ONLY
class estimationObjectType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}estimationObjectType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'estimationObjectType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1662, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_01295_estimationObjectType_httpwww_ech_chxmlnseCH_01295localID', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1664, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}volume uses Python identifier volume
    __volume = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'volume'), 'volume', '__httpwww_ech_chxmlnseCH_01295_estimationObjectType_httpwww_ech_chxmlnseCH_01295volume', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1665, 3), )

    
    volume = property(__volume.value, __volume.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}yearOfConstruction uses Python identifier yearOfConstruction
    __yearOfConstruction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'yearOfConstruction'), 'yearOfConstruction', '__httpwww_ech_chxmlnseCH_01295_estimationObjectType_httpwww_ech_chxmlnseCH_01295yearOfConstruction', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1666, 3), )

    
    yearOfConstruction = property(__yearOfConstruction.value, __yearOfConstruction.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpwww_ech_chxmlnseCH_01295_estimationObjectType_httpwww_ech_chxmlnseCH_01295description', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1667, 3), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}validFrom uses Python identifier validFrom
    __validFrom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'validFrom'), 'validFrom', '__httpwww_ech_chxmlnseCH_01295_estimationObjectType_httpwww_ech_chxmlnseCH_01295validFrom', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1668, 3), )

    
    validFrom = property(__validFrom.value, __validFrom.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}estimationReason uses Python identifier estimationReason
    __estimationReason = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'estimationReason'), 'estimationReason', '__httpwww_ech_chxmlnseCH_01295_estimationObjectType_httpwww_ech_chxmlnseCH_01295estimationReason', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1669, 3), )

    
    estimationReason = property(__estimationReason.value, __estimationReason.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}estimationValue uses Python identifier estimationValue
    __estimationValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'estimationValue'), 'estimationValue', '__httpwww_ech_chxmlnseCH_01295_estimationObjectType_httpwww_ech_chxmlnseCH_01295estimationValue', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1670, 3), )

    
    estimationValue = property(__estimationValue.value, __estimationValue.set, None, None)

    _ElementMap.update({
        __localID.name() : __localID,
        __volume.name() : __volume,
        __yearOfConstruction.name() : __yearOfConstruction,
        __description.name() : __description,
        __validFrom.name() : __validFrom,
        __estimationReason.name() : __estimationReason,
        __estimationValue.name() : __estimationValue
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.estimationObjectType = estimationObjectType
Namespace.addCategoryObject('typeBinding', 'estimationObjectType', estimationObjectType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingAuthorityType with content type ELEMENT_ONLY
class buildingAuthorityType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingAuthorityType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingAuthorityType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1688, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}buildingAuthorityIdentificationType uses Python identifier buildingAuthorityIdentificationType
    __buildingAuthorityIdentificationType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'buildingAuthorityIdentificationType'), 'buildingAuthorityIdentificationType', '__httpwww_ech_chxmlnseCH_01295_buildingAuthorityType_httpwww_ech_chxmlnseCH_01295buildingAuthorityIdentificationType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1690, 3), )

    
    buildingAuthorityIdentificationType = property(__buildingAuthorityIdentificationType.value, __buildingAuthorityIdentificationType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpwww_ech_chxmlnseCH_01295_buildingAuthorityType_httpwww_ech_chxmlnseCH_01295description', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1691, 3), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}shortDescription uses Python identifier shortDescription
    __shortDescription = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'shortDescription'), 'shortDescription', '__httpwww_ech_chxmlnseCH_01295_buildingAuthorityType_httpwww_ech_chxmlnseCH_01295shortDescription', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1692, 3), )

    
    shortDescription = property(__shortDescription.value, __shortDescription.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}contactPerson uses Python identifier contactPerson
    __contactPerson = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'contactPerson'), 'contactPerson', '__httpwww_ech_chxmlnseCH_01295_buildingAuthorityType_httpwww_ech_chxmlnseCH_01295contactPerson', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1693, 3), )

    
    contactPerson = property(__contactPerson.value, __contactPerson.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}contact uses Python identifier contact
    __contact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'contact'), 'contact', '__httpwww_ech_chxmlnseCH_01295_buildingAuthorityType_httpwww_ech_chxmlnseCH_01295contact', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1701, 3), )

    
    contact = property(__contact.value, __contact.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}address uses Python identifier address
    __address = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'address'), 'address', '__httpwww_ech_chxmlnseCH_01295_buildingAuthorityType_httpwww_ech_chxmlnseCH_01295address', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1702, 3), )

    
    address = property(__address.value, __address.set, None, None)

    _ElementMap.update({
        __buildingAuthorityIdentificationType.name() : __buildingAuthorityIdentificationType,
        __description.name() : __description,
        __shortDescription.name() : __shortDescription,
        __contactPerson.name() : __contactPerson,
        __contact.name() : __contact,
        __address.name() : __address
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.buildingAuthorityType = buildingAuthorityType
Namespace.addCategoryObject('typeBinding', 'buildingAuthorityType', buildingAuthorityType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1694, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}personIdentification uses Python identifier personIdentification
    __personIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'personIdentification'), 'personIdentification', '__httpwww_ech_chxmlnseCH_01295_CTD_ANON_2_httpwww_ech_chxmlnseCH_01295personIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1696, 6), )

    
    personIdentification = property(__personIdentification.value, __personIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}organisationIdentification uses Python identifier organisationIdentification
    __organisationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification'), 'organisationIdentification', '__httpwww_ech_chxmlnseCH_01295_CTD_ANON_2_httpwww_ech_chxmlnseCH_01295organisationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1697, 6), )

    
    organisationIdentification = property(__organisationIdentification.value, __organisationIdentification.set, None, None)

    _ElementMap.update({
        __personIdentification.name() : __personIdentification,
        __organisationIdentification.name() : __organisationIdentification
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}contactType with content type ELEMENT_ONLY
class contactType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}contactType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'contactType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1716, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}emailAddress uses Python identifier emailAddress
    __emailAddress = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'emailAddress'), 'emailAddress', '__httpwww_ech_chxmlnseCH_01295_contactType_httpwww_ech_chxmlnseCH_01295emailAddress', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1718, 3), )

    
    emailAddress = property(__emailAddress.value, __emailAddress.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}phoneNumber uses Python identifier phoneNumber
    __phoneNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'phoneNumber'), 'phoneNumber', '__httpwww_ech_chxmlnseCH_01295_contactType_httpwww_ech_chxmlnseCH_01295phoneNumber', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1719, 3), )

    
    phoneNumber = property(__phoneNumber.value, __phoneNumber.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}faxNumber uses Python identifier faxNumber
    __faxNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'faxNumber'), 'faxNumber', '__httpwww_ech_chxmlnseCH_01295_contactType_httpwww_ech_chxmlnseCH_01295faxNumber', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1720, 3), )

    
    faxNumber = property(__faxNumber.value, __faxNumber.set, None, None)

    _ElementMap.update({
        __emailAddress.name() : __emailAddress,
        __phoneNumber.name() : __phoneNumber,
        __faxNumber.name() : __faxNumber
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.contactType = contactType
Namespace.addCategoryObject('typeBinding', 'contactType', contactType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}personType with content type ELEMENT_ONLY
class personType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}personType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'personType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1723, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}identification uses Python identifier identification
    __identification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'identification'), 'identification', '__httpwww_ech_chxmlnseCH_01295_personType_httpwww_ech_chxmlnseCH_01295identification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1725, 3), )

    
    identification = property(__identification.value, __identification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}address uses Python identifier address
    __address = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'address'), 'address', '__httpwww_ech_chxmlnseCH_01295_personType_httpwww_ech_chxmlnseCH_01295address', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1733, 3), )

    
    address = property(__address.value, __address.set, None, None)

    _ElementMap.update({
        __identification.name() : __identification,
        __address.name() : __address
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.personType = personType
Namespace.addCategoryObject('typeBinding', 'personType', personType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1726, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}personIdentification uses Python identifier personIdentification
    __personIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'personIdentification'), 'personIdentification', '__httpwww_ech_chxmlnseCH_01295_CTD_ANON_3_httpwww_ech_chxmlnseCH_01295personIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1728, 6), )

    
    personIdentification = property(__personIdentification.value, __personIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}organisationIdentification uses Python identifier organisationIdentification
    __organisationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification'), 'organisationIdentification', '__httpwww_ech_chxmlnseCH_01295_CTD_ANON_3_httpwww_ech_chxmlnseCH_01295organisationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1729, 6), )

    
    organisationIdentification = property(__organisationIdentification.value, __organisationIdentification.set, None, None)

    _ElementMap.update({
        __personIdentification.name() : __personIdentification,
        __organisationIdentification.name() : __organisationIdentification
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}personOnlyType with content type ELEMENT_ONLY
class personOnlyType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}personOnlyType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'personOnlyType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1736, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}identification uses Python identifier identification
    __identification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'identification'), 'identification', '__httpwww_ech_chxmlnseCH_01295_personOnlyType_httpwww_ech_chxmlnseCH_01295identification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1738, 3), )

    
    identification = property(__identification.value, __identification.set, None, None)

    _ElementMap.update({
        __identification.name() : __identification
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.personOnlyType = personOnlyType
Namespace.addCategoryObject('typeBinding', 'personOnlyType', personOnlyType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1739, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}personIdentification uses Python identifier personIdentification
    __personIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'personIdentification'), 'personIdentification', '__httpwww_ech_chxmlnseCH_01295_CTD_ANON_4_httpwww_ech_chxmlnseCH_01295personIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1741, 6), )

    
    personIdentification = property(__personIdentification.value, __personIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0129/5}organisationIdentification uses Python identifier organisationIdentification
    __organisationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification'), 'organisationIdentification', '__httpwww_ech_chxmlnseCH_01295_CTD_ANON_4_httpwww_ech_chxmlnseCH_01295organisationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1742, 6), )

    
    organisationIdentification = property(__organisationIdentification.value, __organisationIdentification.set, None, None)

    _ElementMap.update({
        __personIdentification.name() : __personIdentification,
        __organisationIdentification.name() : __organisationIdentification
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_4 = CTD_ANON_4


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingOnlyType with content type ELEMENT_ONLY
class buildingOnlyType (buildingType):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingOnlyType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingOnlyType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 760, 1)
    _ElementMap = buildingType._ElementMap.copy()
    _AttributeMap = buildingType._AttributeMap.copy()
    # Base type is buildingType
    
    # Element buildingIdentification ({http://www.ech.ch/xmlns/eCH-0129/5}buildingIdentification) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element EGID ({http://www.ech.ch/xmlns/eCH-0129/5}EGID) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element officialBuildingNo ({http://www.ech.ch/xmlns/eCH-0129/5}officialBuildingNo) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element name ({http://www.ech.ch/xmlns/eCH-0129/5}name) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element dateOfConstruction ({http://www.ech.ch/xmlns/eCH-0129/5}dateOfConstruction) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element dateOfRenovation ({http://www.ech.ch/xmlns/eCH-0129/5}dateOfRenovation) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element dateOfDemolition ({http://www.ech.ch/xmlns/eCH-0129/5}dateOfDemolition) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element numberOfFloors ({http://www.ech.ch/xmlns/eCH-0129/5}numberOfFloors) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element numberOfSeparateHabitableRooms ({http://www.ech.ch/xmlns/eCH-0129/5}numberOfSeparateHabitableRooms) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element surfaceAreaOfBuilding ({http://www.ech.ch/xmlns/eCH-0129/5}surfaceAreaOfBuilding) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element subSurfaceAreaOfBuilding ({http://www.ech.ch/xmlns/eCH-0129/5}subSurfaceAreaOfBuilding) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element surfaceAreaOfBuildingSignaleObject ({http://www.ech.ch/xmlns/eCH-0129/5}surfaceAreaOfBuildingSignaleObject) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element buildingCategory ({http://www.ech.ch/xmlns/eCH-0129/5}buildingCategory) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element buildingClass ({http://www.ech.ch/xmlns/eCH-0129/5}buildingClass) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element status ({http://www.ech.ch/xmlns/eCH-0129/5}status) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element coordinates ({http://www.ech.ch/xmlns/eCH-0129/5}coordinates) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element otherID ({http://www.ech.ch/xmlns/eCH-0129/5}otherID) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element civilDefenseShelter ({http://www.ech.ch/xmlns/eCH-0129/5}civilDefenseShelter) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element neighbourhood ({http://www.ech.ch/xmlns/eCH-0129/5}neighbourhood) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element localCode ({http://www.ech.ch/xmlns/eCH-0129/5}localCode) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element energyRelevantSurface ({http://www.ech.ch/xmlns/eCH-0129/5}energyRelevantSurface) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element volume ({http://www.ech.ch/xmlns/eCH-0129/5}volume) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element heating ({http://www.ech.ch/xmlns/eCH-0129/5}heating) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element hotWater ({http://www.ech.ch/xmlns/eCH-0129/5}hotWater) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element namedMetaData ({http://www.ech.ch/xmlns/eCH-0129/5}namedMetaData) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    
    # Element buildingFreeText ({http://www.ech.ch/xmlns/eCH-0129/5}buildingFreeText) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.buildingOnlyType = buildingOnlyType
Namespace.addCategoryObject('typeBinding', 'buildingOnlyType', buildingOnlyType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}insuranceObjectOnlyType with content type ELEMENT_ONLY
class insuranceObjectOnlyType (insuranceObjectType):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}insuranceObjectOnlyType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'insuranceObjectOnlyType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1359, 1)
    _ElementMap = insuranceObjectType._ElementMap.copy()
    _AttributeMap = insuranceObjectType._AttributeMap.copy()
    # Base type is insuranceObjectType
    
    # Element localID ({http://www.ech.ch/xmlns/eCH-0129/5}localID) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}insuranceObjectType
    
    # Element startDate ({http://www.ech.ch/xmlns/eCH-0129/5}startDate) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}insuranceObjectType
    
    # Element endDate ({http://www.ech.ch/xmlns/eCH-0129/5}endDate) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}insuranceObjectType
    
    # Element insuranceNumber ({http://www.ech.ch/xmlns/eCH-0129/5}insuranceNumber) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}insuranceObjectType
    
    # Element usageCode ({http://www.ech.ch/xmlns/eCH-0129/5}usageCode) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}insuranceObjectType
    
    # Element usageDescription ({http://www.ech.ch/xmlns/eCH-0129/5}usageDescription) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}insuranceObjectType
    
    # Element volume ({http://www.ech.ch/xmlns/eCH-0129/5}volume) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}insuranceObjectType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.insuranceObjectOnlyType = insuranceObjectOnlyType
Namespace.addCategoryObject('typeBinding', 'insuranceObjectOnlyType', insuranceObjectOnlyType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}estimationObjectOnlyType with content type ELEMENT_ONLY
class estimationObjectOnlyType (estimationObjectType):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}estimationObjectOnlyType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'estimationObjectOnlyType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1673, 1)
    _ElementMap = estimationObjectType._ElementMap.copy()
    _AttributeMap = estimationObjectType._AttributeMap.copy()
    # Base type is estimationObjectType
    
    # Element localID ({http://www.ech.ch/xmlns/eCH-0129/5}localID) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}estimationObjectType
    
    # Element volume ({http://www.ech.ch/xmlns/eCH-0129/5}volume) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}estimationObjectType
    
    # Element yearOfConstruction ({http://www.ech.ch/xmlns/eCH-0129/5}yearOfConstruction) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}estimationObjectType
    
    # Element description ({http://www.ech.ch/xmlns/eCH-0129/5}description) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}estimationObjectType
    
    # Element validFrom ({http://www.ech.ch/xmlns/eCH-0129/5}validFrom) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}estimationObjectType
    
    # Element estimationReason ({http://www.ech.ch/xmlns/eCH-0129/5}estimationReason) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}estimationObjectType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.estimationObjectOnlyType = estimationObjectOnlyType
Namespace.addCategoryObject('typeBinding', 'estimationObjectOnlyType', estimationObjectOnlyType)


# Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingAuthorityOnlyType with content type ELEMENT_ONLY
class buildingAuthorityOnlyType (buildingAuthorityType):
    """Complex type {http://www.ech.ch/xmlns/eCH-0129/5}buildingAuthorityOnlyType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingAuthorityOnlyType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1705, 1)
    _ElementMap = buildingAuthorityType._ElementMap.copy()
    _AttributeMap = buildingAuthorityType._AttributeMap.copy()
    # Base type is buildingAuthorityType
    
    # Element buildingAuthorityIdentificationType ({http://www.ech.ch/xmlns/eCH-0129/5}buildingAuthorityIdentificationType) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingAuthorityType
    
    # Element description ({http://www.ech.ch/xmlns/eCH-0129/5}description) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingAuthorityType
    
    # Element shortDescription ({http://www.ech.ch/xmlns/eCH-0129/5}shortDescription) inherited from {http://www.ech.ch/xmlns/eCH-0129/5}buildingAuthorityType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.buildingAuthorityOnlyType = buildingAuthorityOnlyType
Namespace.addCategoryObject('typeBinding', 'buildingAuthorityOnlyType', buildingAuthorityOnlyType)


constructionProject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'constructionProject'), constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 420, 1))
Namespace.addCategoryObject('elementBinding', constructionProject.name().localName(), constructionProject)

building = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'building'), buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 759, 1))
Namespace.addCategoryObject('elementBinding', building.name().localName(), building)

buildingEntrance = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'buildingEntrance'), buildingEntranceType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 842, 1))
Namespace.addCategoryObject('elementBinding', buildingEntrance.name().localName(), buildingEntrance)

buildingEntranceOnly = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'buildingEntranceOnly'), buildingEntranceOnlyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 843, 1))
Namespace.addCategoryObject('elementBinding', buildingEntranceOnly.name().localName(), buildingEntranceOnly)

dwelling = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dwelling'), dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1001, 1))
Namespace.addCategoryObject('elementBinding', dwelling.name().localName(), dwelling)

realestate = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'realestate'), realestateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1135, 1))
Namespace.addCategoryObject('elementBinding', realestate.name().localName(), realestate)

locality = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'locality'), localityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1176, 1))
Namespace.addCategoryObject('elementBinding', locality.name().localName(), locality)

fiscalOwnership = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'fiscalOwnership'), fiscalOwnershipType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1213, 1))
Namespace.addCategoryObject('elementBinding', fiscalOwnership.name().localName(), fiscalOwnership)

area = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'area'), areaType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1273, 1))
Namespace.addCategoryObject('elementBinding', area.name().localName(), area)

insuranceObject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'insuranceObject'), insuranceObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1374, 1))
Namespace.addCategoryObject('elementBinding', insuranceObject.name().localName(), insuranceObject)

street = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'street'), streetType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1453, 1))
Namespace.addCategoryObject('elementBinding', street.name().localName(), street)

right = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'right'), rightType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1478, 1))
Namespace.addCategoryObject('elementBinding', right.name().localName(), right)

cadastralMap = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'cadastralMap'), cadastralMapType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1491, 1))
Namespace.addCategoryObject('elementBinding', cadastralMap.name().localName(), cadastralMap)

cadastralSurveyorRemark = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'cadastralSurveyorRemark'), cadastralSurveyorRemarkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1519, 1))
Namespace.addCategoryObject('elementBinding', cadastralSurveyorRemark.name().localName(), cadastralSurveyorRemark)

placeName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'placeName'), placeNameType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1537, 1))
Namespace.addCategoryObject('elementBinding', placeName.name().localName(), placeName)

coveringAreaOfSDR = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'coveringAreaOfSDR'), coveringAreaOfSDRType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1544, 1))
Namespace.addCategoryObject('elementBinding', coveringAreaOfSDR.name().localName(), coveringAreaOfSDR)

partialAreaOfBuilding = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'partialAreaOfBuilding'), partialAreaOfBuildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1550, 1))
Namespace.addCategoryObject('elementBinding', partialAreaOfBuilding.name().localName(), partialAreaOfBuilding)

kindOfConstructionWork = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'kindOfConstructionWork'), kindOfConstructionWorkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1572, 1))
Namespace.addCategoryObject('elementBinding', kindOfConstructionWork.name().localName(), kindOfConstructionWork)

estimationObject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'estimationObject'), estimationObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1687, 1))
Namespace.addCategoryObject('elementBinding', estimationObject.name().localName(), estimationObject)

buildingOnly = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'buildingOnly'), buildingOnlyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 794, 1))
Namespace.addCategoryObject('elementBinding', buildingOnly.name().localName(), buildingOnly)



namedMetaDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'metaDataName'), STD_ANON, scope=namedMetaDataType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 42, 3)))

namedMetaDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'metaDataValue'), STD_ANON_, scope=namedMetaDataType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 50, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(namedMetaDataType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'metaDataName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 42, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(namedMetaDataType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'metaDataValue')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 50, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
namedMetaDataType._Automaton = _BuildAutomaton()




personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'individual'), _ImportedBinding_camac_echbern_schema_ech_0044_4_1.personIdentificationLightType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 67, 3)))

personIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'organisation'), _ImportedBinding_camac_echbern_schema_ech_0097_2_0.organisationIdentificationType, scope=personIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 68, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'individual')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 67, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(personIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'organisation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 68, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
personIdentificationType._Automaton = _BuildAutomaton_()




namedIdType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdCategory'), iDCategoryType, scope=namedIdType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 73, 3)))

namedIdType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Id'), STD_ANON_2, scope=namedIdType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 74, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(namedIdType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 73, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(namedIdType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Id')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 74, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
namedIdType._Automaton = _BuildAutomaton_2()




datePartiallyKnownType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yearMonthDay'), pyxb.binding.datatypes.date, scope=datePartiallyKnownType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 86, 3)))

datePartiallyKnownType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yearMonth'), pyxb.binding.datatypes.gYearMonth, scope=datePartiallyKnownType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 87, 3)))

datePartiallyKnownType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'year'), pyxb.binding.datatypes.gYear, scope=datePartiallyKnownType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 88, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(datePartiallyKnownType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yearMonthDay')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 86, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(datePartiallyKnownType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yearMonth')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 87, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(datePartiallyKnownType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'year')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 88, 3))
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




coordinatesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LV95'), CTD_ANON, scope=coordinatesType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 109, 3)))

coordinatesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LV03'), CTD_ANON_, scope=coordinatesType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 136, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(coordinatesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LV95')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 109, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(coordinatesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LV03')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 136, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
coordinatesType._Automaton = _BuildAutomaton_4()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'east'), STD_ANON_3, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 112, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'north'), STD_ANON_4, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 122, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'originOfCoordinates'), originOfCoordinatesType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 132, 6)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'east')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 112, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'north')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 122, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'originOfCoordinates')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 132, 6))
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
CTD_ANON._Automaton = _BuildAutomaton_5()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Y'), STD_ANON_5, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 139, 6)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'X'), STD_ANON_6, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 149, 6)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'originOfCoordinates'), originOfCoordinatesType, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 159, 6)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Y')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 139, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'X')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 149, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'originOfCoordinates')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 159, 6))
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
CTD_ANON_._Automaton = _BuildAutomaton_6()




constructionLocalisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'municipality'), _ImportedBinding_camac_echbern_schema_ech_0007_6_0.swissMunicipalityType, scope=constructionLocalisationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 185, 3)))

constructionLocalisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'canton'), _ImportedBinding_camac_echbern_schema_ech_0007_6_0.cantonAbbreviationType, scope=constructionLocalisationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 186, 3)))

constructionLocalisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'country'), _ImportedBinding_camac_echbern_schema_ech_0008_3_0.countryType, scope=constructionLocalisationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 187, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(constructionLocalisationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'municipality')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 185, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(constructionLocalisationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'canton')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 186, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(constructionLocalisationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'country')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 187, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
constructionLocalisationType._Automaton = _BuildAutomaton_7()




constructionProjectIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), namedIdType, scope=constructionProjectIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 388, 3)))

constructionProjectIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EPROID'), EPROIDType, scope=constructionProjectIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 389, 3)))

constructionProjectIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'officialConstructionProjectFileNo'), officialConstructionProjectFileNoType, scope=constructionProjectIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 390, 3)))

constructionProjectIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensionOfOfficialConstructionProjectFileNo'), extensionOfOfficialConstructionProjectFileNoType, scope=constructionProjectIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 391, 3)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 389, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 390, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 391, 3))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(constructionProjectIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 388, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(constructionProjectIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EPROID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 389, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(constructionProjectIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'officialConstructionProjectFileNo')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 390, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(constructionProjectIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensionOfOfficialConstructionProjectFileNo')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 391, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
constructionProjectIdentificationType._Automaton = _BuildAutomaton_8()




constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'constructionProjectIdentification'), constructionProjectIdentificationType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 396, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'typeOfConstructionProject'), typeOfConstructionProjectType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 397, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'constructionLocalisation'), constructionLocalisationType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 398, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'typeOfPermit'), typeOfPermitType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 399, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'buildingPermitIssueDate'), buildingPermitIssueDateType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 400, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'projectAnnouncementDate'), projectAnnouncementDateType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 401, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'constructionAuthorisationDeniedDate'), constructionAuthorisationDeniedDateType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 402, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'projectStartDate'), projectStartDateType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 403, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'projectCompletionDate'), projectCompletionDateType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 404, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'projectSuspensionDate'), projectSuspensionDateType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 405, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'withdrawalDate'), withdrawalDateType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 406, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'nonRealisationDate'), nonRealisationDateType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 407, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'totalCostsOfProject'), totalCostsOfProjectType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 408, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'status'), projectStatusType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 409, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'typeOfClient'), typeOfClientType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 410, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'typeOfConstruction'), typeOfConstructionType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 411, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), constructionProjectDescriptionType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 412, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'durationOfConstructionPhase'), durationOfConstructionPhaseType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 413, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'numberOfConcernedBuildings'), numberOfConcernedBuildingsType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 414, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'numberOfConcernedDwellings'), numberOfConcernedDwellingsType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 415, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'projectFreeText'), freeTextType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 416, 3)))

constructionProjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'municipality'), _ImportedBinding_camac_echbern_schema_ech_0007_6_0.swissAndFlMunicipalityType, scope=constructionProjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 417, 3)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 396, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 397, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 398, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 399, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 400, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 401, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 402, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 403, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 404, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 405, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 406, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 407, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 408, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 410, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 411, 3))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 413, 3))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 414, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 415, 3))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=2, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 416, 3))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 417, 3))
    counters.add(cc_19)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'constructionProjectIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 396, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'typeOfConstructionProject')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 397, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'constructionLocalisation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 398, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'typeOfPermit')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 399, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingPermitIssueDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 400, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'projectAnnouncementDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 401, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'constructionAuthorisationDeniedDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 402, 3))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'projectStartDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 403, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'projectCompletionDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 404, 3))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'projectSuspensionDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 405, 3))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'withdrawalDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 406, 3))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'nonRealisationDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 407, 3))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'totalCostsOfProject')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 408, 3))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'status')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 409, 3))
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'typeOfClient')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 410, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'typeOfConstruction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 411, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 412, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'durationOfConstructionPhase')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 413, 3))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'numberOfConcernedBuildings')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 414, 3))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'numberOfConcernedDwellings')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 415, 3))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'projectFreeText')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 416, 3))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(constructionProjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'municipality')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 417, 3))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
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
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
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
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_14, False) ]))
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
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_15, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_16, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_18, True) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_18, False) ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_19, True) ]))
    st_21._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
constructionProjectType._Automaton = _BuildAutomaton_9()




buildingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EGID'), EGIDType, scope=buildingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 424, 4)))

buildingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'street'), _ImportedBinding_camac_echbern_schema_ech_0010_6_0.streetType, scope=buildingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 426, 5)))

buildingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'houseNumber'), _ImportedBinding_camac_echbern_schema_ech_0010_6_0.houseNumberType, scope=buildingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 427, 5)))

buildingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'zipCode'), _ImportedBinding_camac_echbern_schema_ech_0010_6_0.swissZipCodeType, scope=buildingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 428, 5)))

buildingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'nameOfBuilding'), nameOfBuildingType, scope=buildingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 429, 5)))

buildingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EGRID'), EGRIDType, scope=buildingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 433, 6)))

buildingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'cadasterAreaNumber'), cadasterAreaNumberType, scope=buildingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 435, 7)))

buildingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'number'), STD_ANON_7, scope=buildingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 436, 7)))

buildingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'realestateType'), realestateTypeType, scope=buildingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 444, 7)))

buildingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'officialBuildingNo'), officialBuildingNoType, scope=buildingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 447, 5)))

buildingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), namedIdType, scope=buildingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 450, 3)))

buildingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'municipality'), _ImportedBinding_camac_echbern_schema_ech_0007_6_0.municipalityIdType, scope=buildingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 451, 3)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 429, 5))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 444, 7))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EGID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 424, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'street')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 426, 5))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'houseNumber')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 427, 5))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'zipCode')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 428, 5))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'nameOfBuilding')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 429, 5))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EGRID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 433, 6))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'cadasterAreaNumber')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 435, 7))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'number')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 436, 7))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'realestateType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 444, 7))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'officialBuildingNo')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 447, 5))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 450, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'municipality')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 451, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    transitions = []
    transitions.append(fac.Transition(st_10, [
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
    transitions.append(fac.Transition(st_10, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
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
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    st_11._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
buildingIdentificationType._Automaton = _BuildAutomaton_10()




buildingDateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yearMonthDay'), STD_ANON_8, scope=buildingDateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 474, 3)))

buildingDateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yearMonth'), STD_ANON_9, scope=buildingDateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 482, 3)))

buildingDateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'year'), STD_ANON_10, scope=buildingDateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 490, 3)))

buildingDateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'periodOfConstruction'), periodOfConstructionType, scope=buildingDateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 498, 3)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingDateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yearMonthDay')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 474, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingDateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yearMonth')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 482, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingDateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'year')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 490, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingDateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'periodOfConstruction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 498, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
buildingDateType._Automaton = _BuildAutomaton_11()




buildingVolumeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'volume'), STD_ANON_11, scope=buildingVolumeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 614, 3)))

buildingVolumeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'informationSource'), buildingVolumeInformationSourceType, scope=buildingVolumeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 622, 3)))

buildingVolumeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'norm'), buildingVolumeNormType, scope=buildingVolumeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 623, 3)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 622, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingVolumeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'volume')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 614, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingVolumeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'informationSource')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 622, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingVolumeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'norm')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 623, 3))
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
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
buildingVolumeType._Automaton = _BuildAutomaton_12()




heatingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'heatGeneratorHeating'), heatGeneratorHeatingType, scope=heatingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 714, 3)))

heatingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'energySourceHeating'), energySourceType, scope=heatingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 715, 3)))

heatingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'informationSourceHeating'), informationSourceType, scope=heatingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 716, 3)))

heatingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'revisionDate'), pyxb.binding.datatypes.date, scope=heatingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 717, 3)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 715, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 716, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 717, 3))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(heatingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'heatGeneratorHeating')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 714, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(heatingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'energySourceHeating')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 715, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(heatingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'informationSourceHeating')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 716, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(heatingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'revisionDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 717, 3))
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
heatingType._Automaton = _BuildAutomaton_13()




hotWaterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'heatGeneratorHotWater'), heatGeneratorHotWaterType, scope=hotWaterType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 722, 3)))

hotWaterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'energySourceHeating'), energySourceType, scope=hotWaterType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 723, 3)))

hotWaterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'informationSourceHeating'), informationSourceType, scope=hotWaterType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 724, 3)))

hotWaterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'revisionDate'), pyxb.binding.datatypes.date, scope=hotWaterType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 725, 3)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 723, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 724, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 725, 3))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(hotWaterType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'heatGeneratorHotWater')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 722, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(hotWaterType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'energySourceHeating')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 723, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(hotWaterType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'informationSourceHeating')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 724, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(hotWaterType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'revisionDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 725, 3))
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
hotWaterType._Automaton = _BuildAutomaton_14()




buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'buildingIdentification'), buildingIdentificationType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 730, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EGID'), EGIDType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 731, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'officialBuildingNo'), officialBuildingNoType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 732, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'name'), nameOfBuildingType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 733, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateOfConstruction'), buildingDateType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 734, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateOfRenovation'), buildingDateType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 735, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateOfDemolition'), datePartiallyKnownType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 736, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'numberOfFloors'), numberOfFloorsType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 737, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'numberOfSeparateHabitableRooms'), numberOfSeparateHabitableRoomsType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 738, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfBuilding'), surfaceAreaOfBuildingType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 739, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subSurfaceAreaOfBuilding'), surfaceAreaOfBuildingType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 740, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfBuildingSignaleObject'), surfaceAreaOfBuildingSingleObjectType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 741, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'buildingCategory'), buildingCategoryType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 742, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'buildingClass'), buildingClassType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 743, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'status'), buildingStatusType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 744, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'coordinates'), coordinatesType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 745, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherID'), namedIdType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 746, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'civilDefenseShelter'), pyxb.binding.datatypes.boolean, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 747, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'neighbourhood'), neighbourhoodType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 748, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localCode'), localCodeType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 749, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'energyRelevantSurface'), energyRelevantSurfaceType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 750, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'volume'), buildingVolumeType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 751, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'heating'), heatingType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 752, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'hotWater'), hotWaterType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 753, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'buildingEntrance'), buildingEntranceType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 754, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'namedMetaData'), namedMetaDataType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 755, 3)))

buildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'buildingFreeText'), freeTextType, scope=buildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 756, 3)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 730, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 731, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 732, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 733, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 734, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 735, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 736, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 737, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 738, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 739, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 740, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 741, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 743, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 744, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 745, 3))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 746, 3))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 747, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 748, 3))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=4, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 749, 3))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 750, 3))
    counters.add(cc_19)
    cc_20 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 751, 3))
    counters.add(cc_20)
    cc_21 = fac.CounterCondition(min=0, max=2, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 752, 3))
    counters.add(cc_21)
    cc_22 = fac.CounterCondition(min=0, max=2, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 753, 3))
    counters.add(cc_22)
    cc_23 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 754, 3))
    counters.add(cc_23)
    cc_24 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 755, 3))
    counters.add(cc_24)
    cc_25 = fac.CounterCondition(min=0, max=2, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 756, 3))
    counters.add(cc_25)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 730, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EGID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 731, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'officialBuildingNo')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 732, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'name')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 733, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateOfConstruction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 734, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateOfRenovation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 735, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateOfDemolition')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 736, 3))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'numberOfFloors')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 737, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'numberOfSeparateHabitableRooms')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 738, 3))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfBuilding')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 739, 3))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subSurfaceAreaOfBuilding')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 740, 3))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfBuildingSignaleObject')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 741, 3))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 742, 3))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingClass')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 743, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'status')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 744, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'coordinates')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 745, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 746, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'civilDefenseShelter')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 747, 3))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'neighbourhood')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 748, 3))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localCode')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 749, 3))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'energyRelevantSurface')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 750, 3))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_20, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'volume')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 751, 3))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_21, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'heating')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 752, 3))
    st_22 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_22, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'hotWater')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 753, 3))
    st_23 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_23)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_23, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingEntrance')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 754, 3))
    st_24 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_24)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_24, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'namedMetaData')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 755, 3))
    st_25 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_25)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_25, False))
    symbol = pyxb.binding.content.ElementUse(buildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingFreeText')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 756, 3))
    st_26 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_26)
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
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
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, False) ]))
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
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_12, False) ]))
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
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_13, False) ]))
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
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_15, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_16, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_18, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_18, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_19, True) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_19, False) ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_20, True) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_20, False) ]))
    st_21._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_21, True) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_21, False) ]))
    st_22._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_22, True) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_22, False) ]))
    st_23._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_23, True) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_23, False) ]))
    st_24._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_24, True) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_24, False) ]))
    st_25._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_25, True) ]))
    st_26._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
buildingType._Automaton = _BuildAutomaton_15()




buildingEntranceIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EGID'), EGIDType, scope=buildingEntranceIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 815, 3)))

buildingEntranceIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EGAID'), EGAIDType, scope=buildingEntranceIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 816, 3)))

buildingEntranceIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EDID'), EDIDType, scope=buildingEntranceIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 817, 3)))

buildingEntranceIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), namedIdType, scope=buildingEntranceIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 818, 3)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 816, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 817, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingEntranceIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EGID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 815, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingEntranceIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EGAID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 816, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingEntranceIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EDID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 817, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingEntranceIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 818, 3))
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
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
buildingEntranceIdentificationType._Automaton = _BuildAutomaton_16()




buildingEntranceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EGAID'), EGAIDType, scope=buildingEntranceType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 823, 3)))

buildingEntranceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EDID'), EDIDType, scope=buildingEntranceType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 824, 3)))

buildingEntranceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'buildingEntranceNo'), buildingEntranceNoType, scope=buildingEntranceType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 825, 3)))

buildingEntranceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'coordinates'), coordinatesType, scope=buildingEntranceType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 826, 3)))

buildingEntranceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), namedIdType, scope=buildingEntranceType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 827, 3)))

buildingEntranceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'isOfficialAddress'), pyxb.binding.datatypes.boolean, scope=buildingEntranceType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 828, 3)))

buildingEntranceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'steetSection'), streetSectionType, scope=buildingEntranceType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 829, 3)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 823, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 824, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 825, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 826, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 828, 3))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingEntranceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EGAID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 823, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingEntranceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EDID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 824, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingEntranceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingEntranceNo')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 825, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingEntranceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'coordinates')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 826, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingEntranceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 827, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingEntranceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'isOfficialAddress')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 828, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingEntranceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'steetSection')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 829, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
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
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
buildingEntranceType._Automaton = _BuildAutomaton_17()




buildingEntranceOnlyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EGAID'), EGAIDType, scope=buildingEntranceOnlyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 834, 3)))

buildingEntranceOnlyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EDID'), EDIDType, scope=buildingEntranceOnlyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 835, 3)))

buildingEntranceOnlyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'buildingEntranceNo'), buildingEntranceNoType, scope=buildingEntranceOnlyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 836, 3)))

buildingEntranceOnlyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'coordinates'), coordinatesType, scope=buildingEntranceOnlyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 837, 3)))

buildingEntranceOnlyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), namedIdType, scope=buildingEntranceOnlyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 838, 3)))

buildingEntranceOnlyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'isOfficialAddress'), pyxb.binding.datatypes.boolean, scope=buildingEntranceOnlyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 839, 3)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 834, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 835, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 836, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 837, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 839, 3))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingEntranceOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EGAID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 834, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingEntranceOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EDID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 835, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingEntranceOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingEntranceNo')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 836, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingEntranceOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'coordinates')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 837, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingEntranceOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 838, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(buildingEntranceOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'isOfficialAddress')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 839, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
buildingEntranceOnlyType._Automaton = _BuildAutomaton_18()




dwellingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EGID'), EGIDType, scope=dwellingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 938, 3)))

dwellingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EDID'), EDIDType, scope=dwellingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 939, 3)))

dwellingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EWID'), EWIDType, scope=dwellingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 940, 3)))

dwellingIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), namedIdType, scope=dwellingIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 941, 3)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(dwellingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EGID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 938, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(dwellingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EDID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 939, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(dwellingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EWID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 940, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(dwellingIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 941, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
dwellingIdentificationType._Automaton = _BuildAutomaton_19()




dwellingUsageType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'usageCode'), dwellingUsageCodeType, scope=dwellingUsageType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 946, 3)))

dwellingUsageType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'informationSource'), dwellingInformationSourceType, scope=dwellingUsageType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 947, 3)))

dwellingUsageType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'revisionDate'), STD_ANON_12, scope=dwellingUsageType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 948, 3)))

dwellingUsageType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remark'), STD_ANON_13, scope=dwellingUsageType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 955, 3)))

dwellingUsageType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personWithMainResidence'), pyxb.binding.datatypes.boolean, scope=dwellingUsageType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 963, 3)))

dwellingUsageType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personWithSecondaryResidence'), pyxb.binding.datatypes.boolean, scope=dwellingUsageType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 964, 3)))

dwellingUsageType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateFirstOccupancy'), STD_ANON_14, scope=dwellingUsageType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 965, 3)))

dwellingUsageType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateLastOccupancy'), STD_ANON_15, scope=dwellingUsageType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 972, 3)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 946, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 947, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 948, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 955, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 963, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 964, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 965, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 972, 3))
    counters.add(cc_7)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(dwellingUsageType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'usageCode')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 946, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(dwellingUsageType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'informationSource')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 947, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(dwellingUsageType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'revisionDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 948, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(dwellingUsageType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remark')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 955, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(dwellingUsageType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personWithMainResidence')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 963, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(dwellingUsageType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personWithSecondaryResidence')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 964, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(dwellingUsageType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateFirstOccupancy')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 965, 3))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(dwellingUsageType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateLastOccupancy')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 972, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
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
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
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
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
dwellingUsageType._Automaton = _BuildAutomaton_20()




dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), namedIdType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 983, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'administrativeDwellingNo'), administrativeDwellingNoType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 984, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EWID'), EWIDType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 985, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'physicalDwellingNo'), physicalDwellingNoType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 986, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateOfConstruction'), datePartiallyKnownType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 987, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateOfDemolition'), datePartiallyKnownType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 988, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'noOfHabitableRooms'), noOfHabitableRoomsType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 989, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'floor'), floorType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 990, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'locationOfDwellingOnFloor'), locationOfDwellingOnFloorType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 991, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'multipleFloor'), multipleFloorType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 992, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'usageLimitation'), usageLimitationType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 993, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'kitchen'), kitchenType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 994, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfDwelling'), surfaceAreaOfDwellingType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 995, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'status'), dwellingStatusType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 996, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dwellingUsage'), dwellingUsageType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 997, 3)))

dwellingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dwellingFreeText'), freeTextType, scope=dwellingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 998, 3)))

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 984, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 985, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 986, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 987, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 988, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 989, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 990, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 991, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 992, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 993, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 994, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 995, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 996, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 997, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=2, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 998, 3))
    counters.add(cc_14)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 983, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'administrativeDwellingNo')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 984, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EWID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 985, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'physicalDwellingNo')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 986, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateOfConstruction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 987, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateOfDemolition')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 988, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'noOfHabitableRooms')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 989, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'floor')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 990, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'locationOfDwellingOnFloor')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 991, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'multipleFloor')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 992, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'usageLimitation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 993, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'kitchen')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 994, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfDwelling')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 995, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'status')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 996, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dwellingUsage')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 997, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(dwellingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dwellingFreeText')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 998, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
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
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
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
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
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
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
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
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_14, True) ]))
    st_15._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
dwellingType._Automaton = _BuildAutomaton_21()




realestateIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EGRID'), STD_ANON_32, scope=realestateIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1023, 3)))

realestateIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'number'), STD_ANON_16, scope=realestateIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1028, 3)))

realestateIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'numberSuffix'), STD_ANON_17, scope=realestateIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1036, 3)))

realestateIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subDistrict'), STD_ANON_18, scope=realestateIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1044, 3)))

realestateIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'lot'), STD_ANON_19, scope=realestateIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1052, 3)))

def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1023, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1036, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1044, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1052, 3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(realestateIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EGRID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1023, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(realestateIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'number')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1028, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(realestateIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'numberSuffix')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1036, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(realestateIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subDistrict')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1044, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(realestateIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'lot')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1052, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
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
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
realestateIdentificationType._Automaton = _BuildAutomaton_22()




realestateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'realestateIdentification'), realestateIdentificationType, scope=realestateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1121, 3)))

realestateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'authority'), authorityType, scope=realestateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1122, 3)))

realestateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'date'), realestateDateType, scope=realestateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1123, 3)))

realestateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'realestateType'), realestateTypeType, scope=realestateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1124, 3)))

realestateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'cantonalSubKind'), cantonalSubKindType, scope=realestateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1125, 3)))

realestateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'status'), realestateStatusType, scope=realestateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1126, 3)))

realestateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mutnumber'), realestateMutnumberType, scope=realestateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1127, 3)))

realestateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'identDN'), identDNType, scope=realestateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1128, 3)))

realestateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'squareMeasure'), squareMeasureType, scope=realestateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1129, 3)))

realestateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'realestateIncomplete'), realestateIncompleteType, scope=realestateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1130, 3)))

realestateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'coordinates'), coordinatesType, scope=realestateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1131, 3)))

realestateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'namedMetaData'), namedMetaDataType, scope=realestateType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1132, 3)))

def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1122, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1123, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1125, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1126, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1127, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1128, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1129, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1130, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1131, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1132, 3))
    counters.add(cc_9)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(realestateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'realestateIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1121, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(realestateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'authority')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1122, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(realestateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'date')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1123, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(realestateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'realestateType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1124, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(realestateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'cantonalSubKind')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1125, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(realestateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'status')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1126, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(realestateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'mutnumber')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1127, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(realestateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'identDN')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1128, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(realestateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'squareMeasure')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1129, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(realestateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'realestateIncomplete')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1130, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(realestateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'coordinates')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1131, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(realestateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'namedMetaData')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1132, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
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
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
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
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
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
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, True) ]))
    st_11._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
realestateType._Automaton = _BuildAutomaton_23()




localityNameType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'language'), streetLanguageType, scope=localityNameType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1150, 3)))

localityNameType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'nameLong'), STD_ANON_20, scope=localityNameType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1151, 3)))

localityNameType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'nameShort'), STD_ANON_21, scope=localityNameType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1159, 3)))

def _BuildAutomaton_24 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1159, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(localityNameType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'language')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1150, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(localityNameType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'nameLong')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1151, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(localityNameType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'nameShort')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1159, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
localityNameType._Automaton = _BuildAutomaton_24()




localityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'swissZipCode'), _ImportedBinding_camac_echbern_schema_ech_0010_6_0.swissZipCodeType, scope=localityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1171, 3)))

localityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'swissZipCodeAddOn'), _ImportedBinding_camac_echbern_schema_ech_0010_6_0.swissZipCodeAddOnType, scope=localityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1172, 3)))

localityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'name'), localityNameType, scope=localityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1173, 3)))

def _BuildAutomaton_25 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1171, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1172, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(localityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'swissZipCode')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1171, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(localityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'swissZipCodeAddOn')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1172, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(localityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'name')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1173, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
localityType._Automaton = _BuildAutomaton_25()




fiscalOwnershipType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'accessionDate'), pyxb.binding.datatypes.date, scope=fiscalOwnershipType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1179, 3)))

fiscalOwnershipType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'fiscalRelationship'), STD_ANON_22, scope=fiscalOwnershipType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1180, 3)))

fiscalOwnershipType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'validFrom'), pyxb.binding.datatypes.date, scope=fiscalOwnershipType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1189, 3)))

fiscalOwnershipType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'validTill'), pyxb.binding.datatypes.date, scope=fiscalOwnershipType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1190, 3)))

fiscalOwnershipType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'denominator'), STD_ANON_23, scope=fiscalOwnershipType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1191, 3)))

fiscalOwnershipType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'tally'), STD_ANON_24, scope=fiscalOwnershipType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1201, 3)))

def _BuildAutomaton_26 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_26
    del _BuildAutomaton_26
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1189, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1190, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1191, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1201, 3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(fiscalOwnershipType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'accessionDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1179, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(fiscalOwnershipType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'fiscalRelationship')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1180, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(fiscalOwnershipType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'validFrom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1189, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(fiscalOwnershipType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'validTill')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1190, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(fiscalOwnershipType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'denominator')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1191, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(fiscalOwnershipType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'tally')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1201, 3))
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
fiscalOwnershipType._Automaton = _BuildAutomaton_26()




areaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'areaType'), areaTypeType, scope=areaType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1267, 3)))

areaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'areaDescriptionCode'), areaDescriptionCodeType, scope=areaType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1268, 3)))

areaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'areaDescription'), areaDescriptionType, scope=areaType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1269, 3)))

areaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'areaValue'), areaValueType, scope=areaType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1270, 3)))

def _BuildAutomaton_27 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_27
    del _BuildAutomaton_27
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(areaType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'areaType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1267, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(areaType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'areaDescriptionCode')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1268, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(areaType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'areaDescription')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1269, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(areaType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'areaValue')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1270, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
areaType._Automaton = _BuildAutomaton_27()




insuranceSumType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'amount'), STD_ANON_25, scope=insuranceSumType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1298, 3)))

insuranceSumType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'percentage'), STD_ANON_26, scope=insuranceSumType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1306, 3)))

def _BuildAutomaton_28 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_28
    del _BuildAutomaton_28
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(insuranceSumType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'amount')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1298, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(insuranceSumType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'percentage')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1306, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
insuranceSumType._Automaton = _BuildAutomaton_28()




insuranceValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), namedIdType, scope=insuranceValueType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1328, 3)))

insuranceValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'validFrom'), pyxb.binding.datatypes.date, scope=insuranceValueType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1329, 3)))

insuranceValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'changeReason'), changeReasonType, scope=insuranceValueType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1330, 3)))

insuranceValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'insuranceSum'), insuranceSumType, scope=insuranceValueType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1331, 3)))

def _BuildAutomaton_29 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_29
    del _BuildAutomaton_29
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(insuranceValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1328, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(insuranceValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'validFrom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1329, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(insuranceValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'changeReason')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1330, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(insuranceValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'insuranceSum')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1331, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
insuranceValueType._Automaton = _BuildAutomaton_29()




insuranceVolumeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'volume'), STD_ANON_27, scope=insuranceVolumeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1336, 3)))

insuranceVolumeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'norm'), buildingVolumeNormType, scope=insuranceVolumeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1344, 3)))

def _BuildAutomaton_30 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_30
    del _BuildAutomaton_30
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(insuranceVolumeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'volume')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1336, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(insuranceVolumeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'norm')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1344, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
insuranceVolumeType._Automaton = _BuildAutomaton_30()




insuranceObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), namedIdType, scope=insuranceObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1349, 3)))

insuranceObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'startDate'), pyxb.binding.datatypes.date, scope=insuranceObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1350, 3)))

insuranceObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'endDate'), pyxb.binding.datatypes.date, scope=insuranceObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1351, 3)))

insuranceObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'insuranceNumber'), buildingInsuranceNumberType, scope=insuranceObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1352, 3)))

insuranceObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'usageCode'), usageCodeType, scope=insuranceObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1353, 3)))

insuranceObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'usageDescription'), usageDescriptionType, scope=insuranceObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1354, 3)))

insuranceObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'insuranceValue'), insuranceValueType, scope=insuranceObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1355, 3)))

insuranceObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'volume'), insuranceVolumeType, scope=insuranceObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1356, 3)))

def _BuildAutomaton_31 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_31
    del _BuildAutomaton_31
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1350, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1351, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1353, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1354, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1355, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1356, 3))
    counters.add(cc_5)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(insuranceObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1349, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(insuranceObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'startDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1350, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(insuranceObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'endDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1351, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(insuranceObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'insuranceNumber')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1352, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(insuranceObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'usageCode')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1353, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(insuranceObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'usageDescription')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1354, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(insuranceObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'insuranceValue')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1355, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(insuranceObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'volume')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1356, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
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
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
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
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
insuranceObjectType._Automaton = _BuildAutomaton_31()




streetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ESID'), ESIDType, scope=streetType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1436, 3)))

streetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'isOfficialDescription'), isOfficialDescriptionType, scope=streetType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1437, 3)))

streetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'officialStreetNumber'), officialStreetNumberType, scope=streetType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1438, 3)))

streetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), namedIdType, scope=streetType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1439, 3)))

streetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'streetKind'), streetKindType, scope=streetType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1440, 3)))

streetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), streetDescriptionType, scope=streetType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1441, 3)))

streetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'streetStatus'), streetStatusType, scope=streetType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1442, 3)))

streetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'streetGeometry'), pyxb.binding.datatypes.anyType, scope=streetType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1443, 3)))

def _BuildAutomaton_32 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_32
    del _BuildAutomaton_32
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1436, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1437, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1438, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1439, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1440, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1442, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1443, 3))
    counters.add(cc_6)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(streetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ESID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1436, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(streetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'isOfficialDescription')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1437, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(streetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'officialStreetNumber')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1438, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(streetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1439, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(streetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'streetKind')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1440, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(streetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1441, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(streetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'streetStatus')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1442, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(streetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'streetGeometry')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1443, 3))
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
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
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
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
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
streetType._Automaton = _BuildAutomaton_32()




streetSectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ESID'), ESIDType, scope=streetSectionType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1448, 3)))

streetSectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'swissZipCode'), _ImportedBinding_camac_echbern_schema_ech_0010_6_0.swissZipCodeType, scope=streetSectionType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1449, 3)))

streetSectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'swissZipCodeAddOn'), _ImportedBinding_camac_echbern_schema_ech_0010_6_0.swissZipCodeAddOnType, scope=streetSectionType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1450, 3)))

def _BuildAutomaton_33 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_33
    del _BuildAutomaton_33
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(streetSectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ESID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1448, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(streetSectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'swissZipCode')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1449, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(streetSectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'swissZipCodeAddOn')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1450, 3))
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
streetSectionType._Automaton = _BuildAutomaton_33()




streetDescriptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'language'), streetLanguageType, scope=streetDescriptionType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1464, 3)))

streetDescriptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'descriptionLong'), streetDescriptionLongType, scope=streetDescriptionType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1465, 3)))

streetDescriptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'descriptionShort'), streetDescriptionShortType, scope=streetDescriptionType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1466, 3)))

streetDescriptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'descriptionIndex'), streetIndexNameType, scope=streetDescriptionType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1467, 3)))

def _BuildAutomaton_34 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_34
    del _BuildAutomaton_34
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1466, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1467, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(streetDescriptionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'language')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1464, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(streetDescriptionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'descriptionLong')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1465, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(streetDescriptionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'descriptionShort')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1466, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(streetDescriptionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'descriptionIndex')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1467, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
streetDescriptionType._Automaton = _BuildAutomaton_34()




rightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EREID'), EREIDType, scope=rightType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1475, 3)))

def _BuildAutomaton_35 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_35
    del _BuildAutomaton_35
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(rightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EREID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1475, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
rightType._Automaton = _BuildAutomaton_35()




cadastralMapType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mapNumber'), mapNumberType, scope=cadastralMapType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1487, 3)))

cadastralMapType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'identDN'), identDNType, scope=cadastralMapType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1488, 3)))

def _BuildAutomaton_36 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_36
    del _BuildAutomaton_36
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(cadastralMapType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'mapNumber')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1487, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(cadastralMapType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'identDN')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1488, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
cadastralMapType._Automaton = _BuildAutomaton_36()




cadastralSurveyorRemarkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remarkType'), remarkTypeType, scope=cadastralSurveyorRemarkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1513, 3)))

cadastralSurveyorRemarkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remarkOtherType'), remarkOtherTypeType, scope=cadastralSurveyorRemarkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1514, 3)))

cadastralSurveyorRemarkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remarkText'), remarkTextType, scope=cadastralSurveyorRemarkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1515, 3)))

cadastralSurveyorRemarkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectID'), objectIDType, scope=cadastralSurveyorRemarkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1516, 3)))

def _BuildAutomaton_37 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_37
    del _BuildAutomaton_37
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1514, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(cadastralSurveyorRemarkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remarkType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1513, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(cadastralSurveyorRemarkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remarkOtherType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1514, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(cadastralSurveyorRemarkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remarkText')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1515, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(cadastralSurveyorRemarkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'objectID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1516, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
cadastralSurveyorRemarkType._Automaton = _BuildAutomaton_37()




placeNameType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'placeNameType'), placeNameTypeType, scope=placeNameType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1533, 3)))

placeNameType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localGeographicalName'), localGeographicalNameType, scope=placeNameType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1534, 3)))

def _BuildAutomaton_38 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_38
    del _BuildAutomaton_38
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(placeNameType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'placeNameType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1533, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(placeNameType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localGeographicalName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1534, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
placeNameType._Automaton = _BuildAutomaton_38()




coveringAreaOfSDRType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'squareMeasure'), squareMeasureType, scope=coveringAreaOfSDRType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1540, 3)))

coveringAreaOfSDRType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'realestateIdentification'), realestateIdentificationType, scope=coveringAreaOfSDRType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1541, 3)))

def _BuildAutomaton_39 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_39
    del _BuildAutomaton_39
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(coveringAreaOfSDRType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'squareMeasure')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1540, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(coveringAreaOfSDRType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'realestateIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1541, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
coveringAreaOfSDRType._Automaton = _BuildAutomaton_39()




partialAreaOfBuildingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'squareMeasure'), squareMeasureType, scope=partialAreaOfBuildingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1547, 3)))

def _BuildAutomaton_40 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_40
    del _BuildAutomaton_40
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1547, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(partialAreaOfBuildingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'squareMeasure')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1547, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
partialAreaOfBuildingType._Automaton = _BuildAutomaton_40()




kindOfConstructionWorkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'kindOfWork'), kindOfWorkType, scope=kindOfConstructionWorkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1560, 3)))

kindOfConstructionWorkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'energeticRestauration'), pyxb.binding.datatypes.boolean, scope=kindOfConstructionWorkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1561, 3)))

kindOfConstructionWorkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'renovationHeatingsystem'), pyxb.binding.datatypes.boolean, scope=kindOfConstructionWorkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1562, 3)))

kindOfConstructionWorkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'innerConversionRenovation'), pyxb.binding.datatypes.boolean, scope=kindOfConstructionWorkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1563, 3)))

kindOfConstructionWorkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'conversion'), pyxb.binding.datatypes.boolean, scope=kindOfConstructionWorkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1564, 3)))

kindOfConstructionWorkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensionHeighteningHeated'), pyxb.binding.datatypes.boolean, scope=kindOfConstructionWorkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1565, 3)))

kindOfConstructionWorkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensionHeighteningNotHeated'), pyxb.binding.datatypes.boolean, scope=kindOfConstructionWorkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1566, 3)))

kindOfConstructionWorkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'thermicSolarFacility'), pyxb.binding.datatypes.boolean, scope=kindOfConstructionWorkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1567, 3)))

kindOfConstructionWorkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'photovoltaicSolarFacility'), pyxb.binding.datatypes.boolean, scope=kindOfConstructionWorkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1568, 3)))

kindOfConstructionWorkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherWorks'), pyxb.binding.datatypes.boolean, scope=kindOfConstructionWorkType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1569, 3)))

def _BuildAutomaton_41 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_41
    del _BuildAutomaton_41
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1561, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1562, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1563, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1564, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1565, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1566, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1567, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1568, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1569, 3))
    counters.add(cc_8)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(kindOfConstructionWorkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'kindOfWork')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1560, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(kindOfConstructionWorkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'energeticRestauration')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1561, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(kindOfConstructionWorkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'renovationHeatingsystem')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1562, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(kindOfConstructionWorkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'innerConversionRenovation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1563, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(kindOfConstructionWorkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'conversion')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1564, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(kindOfConstructionWorkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensionHeighteningHeated')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1565, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(kindOfConstructionWorkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensionHeighteningNotHeated')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1566, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(kindOfConstructionWorkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'thermicSolarFacility')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1567, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(kindOfConstructionWorkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'photovoltaicSolarFacility')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1568, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(kindOfConstructionWorkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherWorks')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1569, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
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
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
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
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
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
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
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
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
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
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, True) ]))
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
kindOfConstructionWorkType._Automaton = _BuildAutomaton_41()




valueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'amount'), STD_ANON_28, scope=valueType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1596, 3)))

valueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'percentage'), STD_ANON_29, scope=valueType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1604, 3)))

def _BuildAutomaton_42 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_42
    del _BuildAutomaton_42
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(valueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'amount')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1596, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(valueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'percentage')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1604, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
valueType._Automaton = _BuildAutomaton_42()




estimationValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), namedIdType, scope=estimationValueType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1616, 3)))

estimationValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'baseYear'), STD_ANON_30, scope=estimationValueType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1617, 3)))

estimationValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'validFrom'), validFromType, scope=estimationValueType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1625, 3)))

estimationValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'indexValue'), STD_ANON_31, scope=estimationValueType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1626, 3)))

estimationValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'value'), valueType, scope=estimationValueType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1634, 3)))

estimationValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'typeOfvalue'), typeOfvalueType, scope=estimationValueType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1635, 3)))

def _BuildAutomaton_43 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_43
    del _BuildAutomaton_43
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1617, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1625, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1626, 3))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(estimationValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1616, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(estimationValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'baseYear')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1617, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(estimationValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'validFrom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1625, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(estimationValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'indexValue')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1626, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(estimationValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'value')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1634, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(estimationValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'typeOfvalue')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1635, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_4._set_transitionSet(transitions)
    transitions = []
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
estimationValueType._Automaton = _BuildAutomaton_43()




estimationObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), namedIdType, scope=estimationObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1664, 3)))

estimationObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'volume'), estimationVolumeType, scope=estimationObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1665, 3)))

estimationObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'yearOfConstruction'), estimationYearOfConstructionType, scope=estimationObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1666, 3)))

estimationObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), estimationDescriptionType, scope=estimationObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1667, 3)))

estimationObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'validFrom'), pyxb.binding.datatypes.date, scope=estimationObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1668, 3)))

estimationObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'estimationReason'), estimationReasonTextType, scope=estimationObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1669, 3)))

estimationObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'estimationValue'), estimationValueType, scope=estimationObjectType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1670, 3)))

def _BuildAutomaton_44 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_44
    del _BuildAutomaton_44
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1665, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1666, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1667, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1668, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1669, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1670, 3))
    counters.add(cc_5)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(estimationObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1664, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(estimationObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'volume')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1665, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(estimationObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yearOfConstruction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1666, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(estimationObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1667, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(estimationObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'validFrom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1668, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(estimationObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'estimationReason')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1669, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(estimationObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'estimationValue')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1670, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
estimationObjectType._Automaton = _BuildAutomaton_44()




buildingAuthorityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'buildingAuthorityIdentificationType'), _ImportedBinding_camac_echbern_schema_ech_0097_2_0.organisationIdentificationType, scope=buildingAuthorityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1690, 3)))

buildingAuthorityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), longDescriptionType, scope=buildingAuthorityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1691, 3)))

buildingAuthorityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'shortDescription'), shortDescriptionType, scope=buildingAuthorityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1692, 3)))

buildingAuthorityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contactPerson'), CTD_ANON_2, scope=buildingAuthorityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1693, 3)))

buildingAuthorityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contact'), contactType, scope=buildingAuthorityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1701, 3)))

buildingAuthorityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'address'), _ImportedBinding_camac_echbern_schema_ech_0010_6_0.addressInformationType, scope=buildingAuthorityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1702, 3)))

def _BuildAutomaton_45 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_45
    del _BuildAutomaton_45
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1691, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1692, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1693, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1701, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1702, 3))
    counters.add(cc_4)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingAuthorityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingAuthorityIdentificationType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1690, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(buildingAuthorityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1691, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(buildingAuthorityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'shortDescription')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1692, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(buildingAuthorityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'contactPerson')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1693, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(buildingAuthorityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'contact')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1701, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(buildingAuthorityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'address')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1702, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
buildingAuthorityType._Automaton = _BuildAutomaton_45()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personIdentification'), _ImportedBinding_camac_echbern_schema_ech_0044_4_1.personIdentificationLightType, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1696, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification'), _ImportedBinding_camac_echbern_schema_ech_0097_2_0.organisationIdentificationType, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1697, 6)))

def _BuildAutomaton_46 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_46
    del _BuildAutomaton_46
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1696, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1697, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_46()




contactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'emailAddress'), emailAddressType, scope=contactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1718, 3)))

contactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'phoneNumber'), phoneNumberType, scope=contactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1719, 3)))

contactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'faxNumber'), phoneNumberType, scope=contactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1720, 3)))

def _BuildAutomaton_47 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_47
    del _BuildAutomaton_47
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1718, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1719, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1720, 3))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(contactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'emailAddress')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1718, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(contactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'phoneNumber')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1719, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(contactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'faxNumber')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1720, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
contactType._Automaton = _BuildAutomaton_47()




personType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'identification'), CTD_ANON_3, scope=personType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1725, 3)))

personType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'address'), _ImportedBinding_camac_echbern_schema_ech_0010_6_0.addressInformationType, scope=personType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1733, 3)))

def _BuildAutomaton_48 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_48
    del _BuildAutomaton_48
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1733, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(personType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'identification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1725, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(personType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'address')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1733, 3))
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
personType._Automaton = _BuildAutomaton_48()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personIdentification'), _ImportedBinding_camac_echbern_schema_ech_0044_4_1.personIdentificationLightType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1728, 6)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification'), _ImportedBinding_camac_echbern_schema_ech_0097_2_0.organisationIdentificationType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1729, 6)))

def _BuildAutomaton_49 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_49
    del _BuildAutomaton_49
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1728, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1729, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_49()




personOnlyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'identification'), CTD_ANON_4, scope=personOnlyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1738, 3)))

def _BuildAutomaton_50 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_50
    del _BuildAutomaton_50
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(personOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'identification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1738, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
personOnlyType._Automaton = _BuildAutomaton_50()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personIdentification'), _ImportedBinding_camac_echbern_schema_ech_0044_4_1.personIdentificationLightType, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1741, 6)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification'), _ImportedBinding_camac_echbern_schema_ech_0097_2_0.organisationIdentificationType, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1742, 6)))

def _BuildAutomaton_51 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_51
    del _BuildAutomaton_51
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1741, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1742, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_4._Automaton = _BuildAutomaton_51()




def _BuildAutomaton_52 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_52
    del _BuildAutomaton_52
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 764, 5))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 765, 5))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 766, 5))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 767, 5))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 768, 5))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 769, 5))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 770, 5))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 771, 5))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 772, 5))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 773, 5))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 774, 5))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 775, 5))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 777, 5))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 778, 5))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 779, 5))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 780, 5))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 781, 5))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 782, 5))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=4, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 783, 5))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 784, 5))
    counters.add(cc_19)
    cc_20 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 785, 5))
    counters.add(cc_20)
    cc_21 = fac.CounterCondition(min=0, max=2, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 786, 5))
    counters.add(cc_21)
    cc_22 = fac.CounterCondition(min=0, max=2, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 787, 5))
    counters.add(cc_22)
    cc_23 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 788, 5))
    counters.add(cc_23)
    cc_24 = fac.CounterCondition(min=0, max=2, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 789, 5))
    counters.add(cc_24)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 764, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EGID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 765, 5))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'officialBuildingNo')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 766, 5))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'name')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 767, 5))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateOfConstruction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 768, 5))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateOfRenovation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 769, 5))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateOfDemolition')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 770, 5))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'numberOfFloors')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 771, 5))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'numberOfSeparateHabitableRooms')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 772, 5))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfBuilding')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 773, 5))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subSurfaceAreaOfBuilding')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 774, 5))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'surfaceAreaOfBuildingSignaleObject')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 775, 5))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingCategory')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 776, 5))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingClass')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 777, 5))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'status')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 778, 5))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'coordinates')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 779, 5))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 780, 5))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'civilDefenseShelter')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 781, 5))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'neighbourhood')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 782, 5))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localCode')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 783, 5))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'energyRelevantSurface')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 784, 5))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_20, False))
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'volume')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 785, 5))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_21, False))
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'heating')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 786, 5))
    st_22 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_22, False))
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'hotWater')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 787, 5))
    st_23 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_23)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_23, False))
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'namedMetaData')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 788, 5))
    st_24 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_24)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_24, False))
    symbol = pyxb.binding.content.ElementUse(buildingOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingFreeText')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 789, 5))
    st_25 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_25)
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
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
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, False) ]))
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
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_12, False) ]))
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
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_15, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_16, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_18, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_18, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_19, True) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_19, False) ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_20, True) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_20, False) ]))
    st_21._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_21, True) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_21, False) ]))
    st_22._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_22, True) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_22, False) ]))
    st_23._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_23, True) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_23, False) ]))
    st_24._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_24, True) ]))
    st_25._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
buildingOnlyType._Automaton = _BuildAutomaton_52()




def _BuildAutomaton_53 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_53
    del _BuildAutomaton_53
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1364, 5))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1365, 5))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1367, 5))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1368, 5))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1369, 5))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(insuranceObjectOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1363, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(insuranceObjectOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'startDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1364, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(insuranceObjectOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'endDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1365, 5))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(insuranceObjectOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'insuranceNumber')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1366, 5))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(insuranceObjectOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'usageCode')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1367, 5))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(insuranceObjectOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'usageDescription')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1368, 5))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(insuranceObjectOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'volume')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1369, 5))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
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
insuranceObjectOnlyType._Automaton = _BuildAutomaton_53()




def _BuildAutomaton_54 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_54
    del _BuildAutomaton_54
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1678, 5))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1679, 5))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1680, 5))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1681, 5))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1682, 5))
    counters.add(cc_4)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(estimationObjectOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1677, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(estimationObjectOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'volume')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1678, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(estimationObjectOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'yearOfConstruction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1679, 5))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(estimationObjectOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1680, 5))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(estimationObjectOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'validFrom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1681, 5))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(estimationObjectOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'estimationReason')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1682, 5))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
estimationObjectOnlyType._Automaton = _BuildAutomaton_54()




def _BuildAutomaton_55 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_55
    del _BuildAutomaton_55
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1710, 5))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1711, 5))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingAuthorityOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingAuthorityIdentificationType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1709, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(buildingAuthorityOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1710, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(buildingAuthorityOnlyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'shortDescription')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0129_5_0.xsd', 1711, 5))
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
buildingAuthorityOnlyType._Automaton = _BuildAutomaton_55()

