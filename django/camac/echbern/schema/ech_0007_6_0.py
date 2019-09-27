# ../../camac/echbern/schema/ech_0007_6_0.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:16f67f23faf89ba4c924048d1e0b954b58272b13
# Generated 2019-09-26 17:57:08.876873 by PyXB version 1.2.6 using Python 3.6.8.final.0
# Namespace http://www.ech.ch/xmlns/eCH-0007/6 [xmlns:eCH-0007]

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
Namespace = pyxb.namespace.NamespaceForURI('http://www.ech.ch/xmlns/eCH-0007/6', create_if_missing=True)
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


# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0007/6}municipalityIdType
class municipalityIdType (pyxb.binding.datatypes.int):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'municipalityIdType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 5, 1)
    _Documentation = None
municipalityIdType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=municipalityIdType, value=pyxb.binding.datatypes.int(1))
municipalityIdType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=municipalityIdType, value=pyxb.binding.datatypes.int(9999))
municipalityIdType._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(4))
municipalityIdType._InitializeFacetMap(municipalityIdType._CF_minInclusive,
   municipalityIdType._CF_maxInclusive,
   municipalityIdType._CF_totalDigits)
Namespace.addCategoryObject('typeBinding', 'municipalityIdType', municipalityIdType)
_module_typeBindings.municipalityIdType = municipalityIdType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0007/6}municipalityNameType
class municipalityNameType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'municipalityNameType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 12, 1)
    _Documentation = None
municipalityNameType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(40))
municipalityNameType._InitializeFacetMap(municipalityNameType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'municipalityNameType', municipalityNameType)
_module_typeBindings.municipalityNameType = municipalityNameType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0007/6}cantonFlAbbreviationType
class cantonFlAbbreviationType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'cantonFlAbbreviationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 17, 1)
    _Documentation = None
cantonFlAbbreviationType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(2))
cantonFlAbbreviationType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=cantonFlAbbreviationType, enum_prefix=None)
cantonFlAbbreviationType.ZH = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='ZH', tag='ZH')
cantonFlAbbreviationType.BE = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='BE', tag='BE')
cantonFlAbbreviationType.LU = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='LU', tag='LU')
cantonFlAbbreviationType.UR = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='UR', tag='UR')
cantonFlAbbreviationType.SZ = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='SZ', tag='SZ')
cantonFlAbbreviationType.OW = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='OW', tag='OW')
cantonFlAbbreviationType.NW = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='NW', tag='NW')
cantonFlAbbreviationType.GL = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='GL', tag='GL')
cantonFlAbbreviationType.ZG = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='ZG', tag='ZG')
cantonFlAbbreviationType.FR = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='FR', tag='FR')
cantonFlAbbreviationType.SO = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='SO', tag='SO')
cantonFlAbbreviationType.BS = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='BS', tag='BS')
cantonFlAbbreviationType.BL = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='BL', tag='BL')
cantonFlAbbreviationType.SH = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='SH', tag='SH')
cantonFlAbbreviationType.AR = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='AR', tag='AR')
cantonFlAbbreviationType.AI = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='AI', tag='AI')
cantonFlAbbreviationType.SG = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='SG', tag='SG')
cantonFlAbbreviationType.GR = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='GR', tag='GR')
cantonFlAbbreviationType.AG = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='AG', tag='AG')
cantonFlAbbreviationType.TG = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='TG', tag='TG')
cantonFlAbbreviationType.TI = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='TI', tag='TI')
cantonFlAbbreviationType.VD = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='VD', tag='VD')
cantonFlAbbreviationType.VS = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='VS', tag='VS')
cantonFlAbbreviationType.NE = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='NE', tag='NE')
cantonFlAbbreviationType.GE = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='GE', tag='GE')
cantonFlAbbreviationType.JU = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='JU', tag='JU')
cantonFlAbbreviationType.FL = cantonFlAbbreviationType._CF_enumeration.addEnumeration(unicode_value='FL', tag='FL')
cantonFlAbbreviationType._InitializeFacetMap(cantonFlAbbreviationType._CF_maxLength,
   cantonFlAbbreviationType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'cantonFlAbbreviationType', cantonFlAbbreviationType)
_module_typeBindings.cantonFlAbbreviationType = cantonFlAbbreviationType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0007/6}cantonAbbreviationType
class cantonAbbreviationType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'cantonAbbreviationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 49, 1)
    _Documentation = None
cantonAbbreviationType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(2))
cantonAbbreviationType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=cantonAbbreviationType, enum_prefix=None)
cantonAbbreviationType.ZH = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='ZH', tag='ZH')
cantonAbbreviationType.BE = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='BE', tag='BE')
cantonAbbreviationType.LU = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='LU', tag='LU')
cantonAbbreviationType.UR = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='UR', tag='UR')
cantonAbbreviationType.SZ = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='SZ', tag='SZ')
cantonAbbreviationType.OW = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='OW', tag='OW')
cantonAbbreviationType.NW = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='NW', tag='NW')
cantonAbbreviationType.GL = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='GL', tag='GL')
cantonAbbreviationType.ZG = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='ZG', tag='ZG')
cantonAbbreviationType.FR = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='FR', tag='FR')
cantonAbbreviationType.SO = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='SO', tag='SO')
cantonAbbreviationType.BS = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='BS', tag='BS')
cantonAbbreviationType.BL = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='BL', tag='BL')
cantonAbbreviationType.SH = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='SH', tag='SH')
cantonAbbreviationType.AR = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='AR', tag='AR')
cantonAbbreviationType.AI = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='AI', tag='AI')
cantonAbbreviationType.SG = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='SG', tag='SG')
cantonAbbreviationType.GR = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='GR', tag='GR')
cantonAbbreviationType.AG = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='AG', tag='AG')
cantonAbbreviationType.TG = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='TG', tag='TG')
cantonAbbreviationType.TI = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='TI', tag='TI')
cantonAbbreviationType.VD = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='VD', tag='VD')
cantonAbbreviationType.VS = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='VS', tag='VS')
cantonAbbreviationType.NE = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='NE', tag='NE')
cantonAbbreviationType.GE = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='GE', tag='GE')
cantonAbbreviationType.JU = cantonAbbreviationType._CF_enumeration.addEnumeration(unicode_value='JU', tag='JU')
cantonAbbreviationType._InitializeFacetMap(cantonAbbreviationType._CF_maxLength,
   cantonAbbreviationType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'cantonAbbreviationType', cantonAbbreviationType)
_module_typeBindings.cantonAbbreviationType = cantonAbbreviationType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0007/6}historyMunicipalityId
class historyMunicipalityId (pyxb.binding.datatypes.int):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'historyMunicipalityId')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 80, 1)
    _Documentation = None
historyMunicipalityId._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=historyMunicipalityId, value=pyxb.binding.datatypes.int(10001))
historyMunicipalityId._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=historyMunicipalityId, value=pyxb.binding.datatypes.int(99999))
historyMunicipalityId._InitializeFacetMap(historyMunicipalityId._CF_minInclusive,
   historyMunicipalityId._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'historyMunicipalityId', historyMunicipalityId)
_module_typeBindings.historyMunicipalityId = historyMunicipalityId

# Complex type {http://www.ech.ch/xmlns/eCH-0007/6}swissMunicipalityType with content type ELEMENT_ONLY
class swissMunicipalityType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0007/6}swissMunicipalityType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'swissMunicipalityType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 86, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0007/6}municipalityId uses Python identifier municipalityId
    __municipalityId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'municipalityId'), 'municipalityId', '__httpwww_ech_chxmlnseCH_00076_swissMunicipalityType_httpwww_ech_chxmlnseCH_00076municipalityId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 88, 3), )

    
    municipalityId = property(__municipalityId.value, __municipalityId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0007/6}municipalityName uses Python identifier municipalityName
    __municipalityName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'municipalityName'), 'municipalityName', '__httpwww_ech_chxmlnseCH_00076_swissMunicipalityType_httpwww_ech_chxmlnseCH_00076municipalityName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 89, 3), )

    
    municipalityName = property(__municipalityName.value, __municipalityName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0007/6}cantonAbbreviation uses Python identifier cantonAbbreviation
    __cantonAbbreviation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'cantonAbbreviation'), 'cantonAbbreviation', '__httpwww_ech_chxmlnseCH_00076_swissMunicipalityType_httpwww_ech_chxmlnseCH_00076cantonAbbreviation', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 90, 3), )

    
    cantonAbbreviation = property(__cantonAbbreviation.value, __cantonAbbreviation.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0007/6}historyMunicipalityId uses Python identifier historyMunicipalityId
    __historyMunicipalityId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'historyMunicipalityId'), 'historyMunicipalityId', '__httpwww_ech_chxmlnseCH_00076_swissMunicipalityType_httpwww_ech_chxmlnseCH_00076historyMunicipalityId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 91, 3), )

    
    historyMunicipalityId = property(__historyMunicipalityId.value, __historyMunicipalityId.set, None, None)

    _ElementMap.update({
        __municipalityId.name() : __municipalityId,
        __municipalityName.name() : __municipalityName,
        __cantonAbbreviation.name() : __cantonAbbreviation,
        __historyMunicipalityId.name() : __historyMunicipalityId
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.swissMunicipalityType = swissMunicipalityType
Namespace.addCategoryObject('typeBinding', 'swissMunicipalityType', swissMunicipalityType)


# Complex type {http://www.ech.ch/xmlns/eCH-0007/6}swissAndFlMunicipalityType with content type ELEMENT_ONLY
class swissAndFlMunicipalityType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0007/6}swissAndFlMunicipalityType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'swissAndFlMunicipalityType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 94, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0007/6}municipalityId uses Python identifier municipalityId
    __municipalityId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'municipalityId'), 'municipalityId', '__httpwww_ech_chxmlnseCH_00076_swissAndFlMunicipalityType_httpwww_ech_chxmlnseCH_00076municipalityId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 96, 3), )

    
    municipalityId = property(__municipalityId.value, __municipalityId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0007/6}municipalityName uses Python identifier municipalityName
    __municipalityName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'municipalityName'), 'municipalityName', '__httpwww_ech_chxmlnseCH_00076_swissAndFlMunicipalityType_httpwww_ech_chxmlnseCH_00076municipalityName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 97, 3), )

    
    municipalityName = property(__municipalityName.value, __municipalityName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0007/6}cantonFlAbbreviation uses Python identifier cantonFlAbbreviation
    __cantonFlAbbreviation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'cantonFlAbbreviation'), 'cantonFlAbbreviation', '__httpwww_ech_chxmlnseCH_00076_swissAndFlMunicipalityType_httpwww_ech_chxmlnseCH_00076cantonFlAbbreviation', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 98, 3), )

    
    cantonFlAbbreviation = property(__cantonFlAbbreviation.value, __cantonFlAbbreviation.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0007/6}historyMunicipalityId uses Python identifier historyMunicipalityId
    __historyMunicipalityId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'historyMunicipalityId'), 'historyMunicipalityId', '__httpwww_ech_chxmlnseCH_00076_swissAndFlMunicipalityType_httpwww_ech_chxmlnseCH_00076historyMunicipalityId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 99, 3), )

    
    historyMunicipalityId = property(__historyMunicipalityId.value, __historyMunicipalityId.set, None, None)

    _ElementMap.update({
        __municipalityId.name() : __municipalityId,
        __municipalityName.name() : __municipalityName,
        __cantonFlAbbreviation.name() : __cantonFlAbbreviation,
        __historyMunicipalityId.name() : __historyMunicipalityId
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.swissAndFlMunicipalityType = swissAndFlMunicipalityType
Namespace.addCategoryObject('typeBinding', 'swissAndFlMunicipalityType', swissAndFlMunicipalityType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 103, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0007/6}swissMunicipality uses Python identifier swissMunicipality
    __swissMunicipality = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'swissMunicipality'), 'swissMunicipality', '__httpwww_ech_chxmlnseCH_00076_CTD_ANON_httpwww_ech_chxmlnseCH_00076swissMunicipality', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 105, 4), )

    
    swissMunicipality = property(__swissMunicipality.value, __swissMunicipality.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0007/6}swissAndFlMunicipality uses Python identifier swissAndFlMunicipality
    __swissAndFlMunicipality = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'swissAndFlMunicipality'), 'swissAndFlMunicipality', '__httpwww_ech_chxmlnseCH_00076_CTD_ANON_httpwww_ech_chxmlnseCH_00076swissAndFlMunicipality', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 106, 4), )

    
    swissAndFlMunicipality = property(__swissAndFlMunicipality.value, __swissAndFlMunicipality.set, None, None)

    _ElementMap.update({
        __swissMunicipality.name() : __swissMunicipality,
        __swissAndFlMunicipality.name() : __swissAndFlMunicipality
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


municipalityRoot = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'municipalityRoot'), CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 102, 1))
Namespace.addCategoryObject('elementBinding', municipalityRoot.name().localName(), municipalityRoot)



swissMunicipalityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'municipalityId'), municipalityIdType, scope=swissMunicipalityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 88, 3)))

swissMunicipalityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'municipalityName'), municipalityNameType, scope=swissMunicipalityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 89, 3)))

swissMunicipalityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'cantonAbbreviation'), cantonAbbreviationType, scope=swissMunicipalityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 90, 3)))

swissMunicipalityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'historyMunicipalityId'), historyMunicipalityId, scope=swissMunicipalityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 91, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 88, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 90, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 91, 3))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(swissMunicipalityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'municipalityId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 88, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(swissMunicipalityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'municipalityName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 89, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(swissMunicipalityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'cantonAbbreviation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 90, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(swissMunicipalityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'historyMunicipalityId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 91, 3))
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
swissMunicipalityType._Automaton = _BuildAutomaton()




swissAndFlMunicipalityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'municipalityId'), municipalityIdType, scope=swissAndFlMunicipalityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 96, 3)))

swissAndFlMunicipalityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'municipalityName'), municipalityNameType, scope=swissAndFlMunicipalityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 97, 3)))

swissAndFlMunicipalityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'cantonFlAbbreviation'), cantonFlAbbreviationType, scope=swissAndFlMunicipalityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 98, 3)))

swissAndFlMunicipalityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'historyMunicipalityId'), historyMunicipalityId, scope=swissAndFlMunicipalityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 99, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 99, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(swissAndFlMunicipalityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'municipalityId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 96, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(swissAndFlMunicipalityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'municipalityName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 97, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(swissAndFlMunicipalityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'cantonFlAbbreviation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 98, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(swissAndFlMunicipalityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'historyMunicipalityId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 99, 3))
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
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
swissAndFlMunicipalityType._Automaton = _BuildAutomaton_()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'swissMunicipality'), swissMunicipalityType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 105, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'swissAndFlMunicipality'), swissAndFlMunicipalityType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 106, 4)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'swissMunicipality')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 105, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'swissAndFlMunicipality')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0007_6_0.xsd', 106, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_2()

