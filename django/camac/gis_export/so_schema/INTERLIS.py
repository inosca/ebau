# ../../../camac/gis_export/so_schema/INTERLIS.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:263202c1148d18e1a11c6e8a67dcc77ff5c628b7
# Generated 2026-07-15 11:48:20.603136 by PyXB version 1.2.6 using Python 3.12.13.final.0
# Namespace http://www.interlis.ch/xtf/2.4/INTERLIS [xmlns:INTERLIS]

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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:32adce28-9fd4-4cfa-a367-c8f7873f934c')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import camac.gis_export.so_schema.geometry as _ImportedBinding_camac_gis_export_so_schema_geometry
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.interlis.ch/xtf/2.4/INTERLIS', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])
_Namespace_geom = _ImportedBinding_camac_gis_export_so_schema_geometry.Namespace
_Namespace_geom.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, fallback_namespace=None, location_base=None, default_namespace=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword fallback_namespace An absent L{pyxb.Namespace} instance
    to use for unqualified names when there is no default namespace in
    scope.  If unspecified or C{None}, the namespace of the module
    containing this function will be used, if it is an absent
    namespace.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.

    @keyword default_namespace An alias for @c fallback_namespace used
    in PyXB 1.1.4 through 1.2.6.  It behaved like a default namespace
    only for absent namespaces.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    if fallback_namespace is None:
        fallback_namespace = default_namespace
    if fallback_namespace is None:
        fallback_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=fallback_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, fallback_namespace=None, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if fallback_namespace is None:
        fallback_namespace = default_namespace
    if fallback_namespace is None:
        fallback_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, fallback_namespace)


# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}tidType
class tidType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'tidType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 28, 2)
    _Documentation = None
tidType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'tidType', tidType)
_module_typeBindings.tidType = tidType

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}refType
class refType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'refType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 31, 2)
    _Documentation = None
refType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'refType', refType)
_module_typeBindings.refType = refType

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}orderposType
class orderposType (pyxb.binding.datatypes.positiveInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'orderposType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 34, 2)
    _Documentation = None
orderposType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'orderposType', orderposType)
_module_typeBindings.orderposType = orderposType

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}bidType
class bidType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'bidType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 37, 2)
    _Documentation = None
bidType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'bidType', bidType)
_module_typeBindings.bidType = bidType

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}consistencyType
class consistencyType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'consistencyType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 40, 2)
    _Documentation = None
consistencyType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=consistencyType)
consistencyType.COMPLETE = consistencyType._CF_enumeration.addEnumeration(unicode_value='COMPLETE', tag='COMPLETE')
consistencyType.INCOMPLETE = consistencyType._CF_enumeration.addEnumeration(unicode_value='INCOMPLETE', tag='INCOMPLETE')
consistencyType._InitializeFacetMap(consistencyType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'consistencyType', consistencyType)
_module_typeBindings.consistencyType = consistencyType

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}domainsType
class domainsType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'domainsType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 46, 2)
    _Documentation = None
domainsType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'domainsType', domainsType)
_module_typeBindings.domainsType = domainsType

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}transferKindType
class transferKindType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'transferKindType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 49, 2)
    _Documentation = None
transferKindType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=transferKindType)
transferKindType.FULL = transferKindType._CF_enumeration.addEnumeration(unicode_value='FULL', tag='FULL')
transferKindType.UPDATE = transferKindType._CF_enumeration.addEnumeration(unicode_value='UPDATE', tag='UPDATE')
transferKindType.INITIAL = transferKindType._CF_enumeration.addEnumeration(unicode_value='INITIAL', tag='INITIAL')
transferKindType._InitializeFacetMap(transferKindType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'transferKindType', transferKindType)
_module_typeBindings.transferKindType = transferKindType

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}operationType
class operationType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'operationType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 57, 2)
    _Documentation = None
operationType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=operationType)
operationType.INSERT = operationType._CF_enumeration.addEnumeration(unicode_value='INSERT', tag='INSERT')
operationType.UPDATE = operationType._CF_enumeration.addEnumeration(unicode_value='UPDATE', tag='UPDATE')
operationType.DELETE = operationType._CF_enumeration.addEnumeration(unicode_value='DELETE', tag='DELETE')
operationType._InitializeFacetMap(operationType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'operationType', operationType)
_module_typeBindings.operationType = operationType

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}basketStateType
class basketStateType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'basketStateType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 64, 2)
    _Documentation = None
basketStateType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'basketStateType', basketStateType)
_module_typeBindings.basketStateType = basketStateType

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}HALIGNMENT
class HALIGNMENT (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'HALIGNMENT')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 97, 2)
    _Documentation = None
HALIGNMENT._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=HALIGNMENT)
HALIGNMENT.Left = HALIGNMENT._CF_enumeration.addEnumeration(unicode_value='Left', tag='Left')
HALIGNMENT.Center = HALIGNMENT._CF_enumeration.addEnumeration(unicode_value='Center', tag='Center')
HALIGNMENT.Right = HALIGNMENT._CF_enumeration.addEnumeration(unicode_value='Right', tag='Right')
HALIGNMENT._InitializeFacetMap(HALIGNMENT._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'HALIGNMENT', HALIGNMENT)
_module_typeBindings.HALIGNMENT = HALIGNMENT

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}VALIGNMENT
class VALIGNMENT (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VALIGNMENT')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 104, 2)
    _Documentation = None
VALIGNMENT._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=VALIGNMENT)
VALIGNMENT.Top = VALIGNMENT._CF_enumeration.addEnumeration(unicode_value='Top', tag='Top')
VALIGNMENT.Cap = VALIGNMENT._CF_enumeration.addEnumeration(unicode_value='Cap', tag='Cap')
VALIGNMENT.Half = VALIGNMENT._CF_enumeration.addEnumeration(unicode_value='Half', tag='Half')
VALIGNMENT.Base = VALIGNMENT._CF_enumeration.addEnumeration(unicode_value='Base', tag='Base')
VALIGNMENT.Bottom = VALIGNMENT._CF_enumeration.addEnumeration(unicode_value='Bottom', tag='Bottom')
VALIGNMENT._InitializeFacetMap(VALIGNMENT._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'VALIGNMENT', VALIGNMENT)
_module_typeBindings.VALIGNMENT = VALIGNMENT

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}I32OID
class I32OID (pyxb.binding.datatypes.int):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'I32OID')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 114, 2)
    _Documentation = None
I32OID._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.int(0), value_datatype=I32OID)
I32OID._InitializeFacetMap(I32OID._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'I32OID', I32OID)
_module_typeBindings.I32OID = I32OID

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}STANDARDOID
class STANDARDOID (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'STANDARDOID')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 120, 2)
    _Documentation = None
STANDARDOID._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(16))
STANDARDOID._CF_pattern = pyxb.binding.facets.CF_pattern()
STANDARDOID._CF_pattern.addPattern(pattern='[a-zA-Z][a-zA-Z0-9]*')
STANDARDOID._InitializeFacetMap(STANDARDOID._CF_length,
   STANDARDOID._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'STANDARDOID', STANDARDOID)
_module_typeBindings.STANDARDOID = STANDARDOID

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/INTERLIS}UUIDOID
class UUIDOID (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'UUIDOID')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 127, 2)
    _Documentation = None
UUIDOID._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(36))
UUIDOID._CF_pattern = pyxb.binding.facets.CF_pattern()
UUIDOID._CF_pattern.addPattern(pattern='[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}')
UUIDOID._InitializeFacetMap(UUIDOID._CF_length,
   UUIDOID._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'UUIDOID', UUIDOID)
_module_typeBindings.UUIDOID = UUIDOID

# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 139, 8)
    _Documentation = None
STD_ANON._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(255))
STD_ANON._CF_pattern = pyxb.binding.facets.CF_pattern()
STD_ANON._CF_pattern.addPattern(pattern='[a-zA-Z][a-zA-Z0-9_]*')
STD_ANON._InitializeFacetMap(STD_ANON._CF_maxLength,
   STD_ANON._CF_pattern)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 155, 8)
    _Documentation = None
STD_ANON_._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(255))
STD_ANON_._CF_pattern = pyxb.binding.facets.CF_pattern()
STD_ANON_._CF_pattern.addPattern(pattern='[a-zA-Z][a-zA-Z0-9_]*')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_maxLength,
   STD_ANON_._CF_pattern)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Atomic simple type: [anonymous]
class STD_ANON_2 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 163, 8)
    _Documentation = None
STD_ANON_2._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(255))
STD_ANON_2._CF_pattern = pyxb.binding.facets.CF_pattern()
STD_ANON_2._CF_pattern.addPattern(pattern='[a-zA-Z][a-zA-Z0-9_]*')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_maxLength,
   STD_ANON_2._CF_pattern)
_module_typeBindings.STD_ANON_2 = STD_ANON_2

# Atomic simple type: [anonymous]
class STD_ANON_3 (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 248, 8)
    _Documentation = None
STD_ANON_3._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(23), value_datatype=STD_ANON_3)
STD_ANON_3._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(0), value_datatype=STD_ANON_3)
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_maxInclusive,
   STD_ANON_3._CF_minInclusive)
_module_typeBindings.STD_ANON_3 = STD_ANON_3

# Atomic simple type: [anonymous]
class STD_ANON_4 (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 256, 8)
    _Documentation = None
STD_ANON_4._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(59), value_datatype=STD_ANON_4)
STD_ANON_4._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(0), value_datatype=STD_ANON_4)
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_maxInclusive,
   STD_ANON_4._CF_minInclusive)
_module_typeBindings.STD_ANON_4 = STD_ANON_4

# Atomic simple type: [anonymous]
class STD_ANON_5 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 264, 8)
    _Documentation = None
STD_ANON_5._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.decimal('59.999'), value_datatype=STD_ANON_5)
STD_ANON_5._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.decimal('0.0'), value_datatype=STD_ANON_5)
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_maxInclusive,
   STD_ANON_5._CF_minInclusive)
_module_typeBindings.STD_ANON_5 = STD_ANON_5

# Atomic simple type: [anonymous]
class STD_ANON_6 (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 288, 8)
    _Documentation = None
STD_ANON_6._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(12), value_datatype=STD_ANON_6)
STD_ANON_6._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(1), value_datatype=STD_ANON_6)
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_maxInclusive,
   STD_ANON_6._CF_minInclusive)
_module_typeBindings.STD_ANON_6 = STD_ANON_6

# Atomic simple type: [anonymous]
class STD_ANON_7 (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 296, 8)
    _Documentation = None
STD_ANON_7._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(31), value_datatype=STD_ANON_7)
STD_ANON_7._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(1), value_datatype=STD_ANON_7)
STD_ANON_7._InitializeFacetMap(STD_ANON_7._CF_maxInclusive,
   STD_ANON_7._CF_minInclusive)
_module_typeBindings.STD_ANON_7 = STD_ANON_7

# Atomic simple type: [anonymous]
class STD_ANON_8 (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 312, 12)
    _Documentation = None
STD_ANON_8._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(23), value_datatype=STD_ANON_8)
STD_ANON_8._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(0), value_datatype=STD_ANON_8)
STD_ANON_8._InitializeFacetMap(STD_ANON_8._CF_maxInclusive,
   STD_ANON_8._CF_minInclusive)
_module_typeBindings.STD_ANON_8 = STD_ANON_8

# Atomic simple type: [anonymous]
class STD_ANON_9 (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 320, 12)
    _Documentation = None
STD_ANON_9._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(59), value_datatype=STD_ANON_9)
STD_ANON_9._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(0), value_datatype=STD_ANON_9)
STD_ANON_9._InitializeFacetMap(STD_ANON_9._CF_maxInclusive,
   STD_ANON_9._CF_minInclusive)
_module_typeBindings.STD_ANON_9 = STD_ANON_9

# Atomic simple type: [anonymous]
class STD_ANON_10 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 328, 12)
    _Documentation = None
STD_ANON_10._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.decimal('59.999'), value_datatype=STD_ANON_10)
STD_ANON_10._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.decimal('0.0'), value_datatype=STD_ANON_10)
STD_ANON_10._InitializeFacetMap(STD_ANON_10._CF_maxInclusive,
   STD_ANON_10._CF_minInclusive)
_module_typeBindings.STD_ANON_10 = STD_ANON_10

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 10, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}TransferType with content type ELEMENT_ONLY
class TransferType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}TransferType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TransferType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 69, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}headersection uses Python identifier headersection
    __headersection = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'headersection'), 'headersection', '__httpwww_interlis_chxtf2_4INTERLIS_TransferType_httpwww_interlis_chxtf2_4INTERLISheadersection', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 71, 6), )

    
    headersection = property(__headersection.value, __headersection.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}datasection uses Python identifier datasection
    __datasection = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'datasection'), 'datasection', '__httpwww_interlis_chxtf2_4INTERLIS_TransferType_httpwww_interlis_chxtf2_4INTERLISdatasection', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 87, 6), )

    
    datasection = property(__datasection.value, __datasection.set, None, None)

    _ElementMap.update({
        __headersection.name() : __headersection,
        __datasection.name() : __datasection
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.TransferType = TransferType
Namespace.addCategoryObject('typeBinding', 'TransferType', TransferType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 72, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}extensions uses Python identifier extensions
    __extensions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extensions'), 'extensions', '__httpwww_interlis_chxtf2_4INTERLIS_CTD_ANON__httpwww_interlis_chxtf2_4INTERLISextensions', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2), )

    
    extensions = property(__extensions.value, __extensions.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}models uses Python identifier models
    __models = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'models'), 'models', '__httpwww_interlis_chxtf2_4INTERLIS_CTD_ANON__httpwww_interlis_chxtf2_4INTERLISmodels', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 74, 12), )

    
    models = property(__models.value, __models.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}sender uses Python identifier sender
    __sender = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sender'), 'sender', '__httpwww_interlis_chxtf2_4INTERLIS_CTD_ANON__httpwww_interlis_chxtf2_4INTERLISsender', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 81, 12), )

    
    sender = property(__sender.value, __sender.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}comment uses Python identifier comment
    __comment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comment'), 'comment', '__httpwww_interlis_chxtf2_4INTERLIS_CTD_ANON__httpwww_interlis_chxtf2_4INTERLIScomment', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 82, 12), )

    
    comment = property(__comment.value, __comment.set, None, None)

    _ElementMap.update({
        __extensions.name() : __extensions,
        __models.name() : __models,
        __sender.name() : __sender,
        __comment.name() : __comment
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 75, 14)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}model uses Python identifier model
    __model = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'model'), 'model', '__httpwww_interlis_chxtf2_4INTERLIS_CTD_ANON_2_httpwww_interlis_chxtf2_4INTERLISmodel', True, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 77, 18), )

    
    model = property(__model.value, __model.set, None, None)

    _ElementMap.update({
        __model.name() : __model
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 88, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}AXISType with content type EMPTY
class AXISType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}AXISType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AXISType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 175, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.AXISType = AXISType
Namespace.addCategoryObject('typeBinding', 'AXISType', AXISType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 192, 12)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}AXIS uses Python identifier AXIS
    __AXIS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AXIS'), 'AXIS', '__httpwww_interlis_chxtf2_4INTERLIS_CTD_ANON_4_httpwww_interlis_chxtf2_4INTERLISAXIS', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 174, 2), )

    
    AXIS = property(__AXIS.value, __AXIS.set, None, None)

    _ElementMap.update({
        __AXIS.name() : __AXIS
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_4 = CTD_ANON_4


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}TIMESYSTEMSType with content type ELEMENT_ONLY
class TIMESYSTEMSType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}TIMESYSTEMSType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TIMESYSTEMSType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 235, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}CALENDAR uses Python identifier CALENDAR
    __CALENDAR = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CALENDAR'), 'CALENDAR', '__httpwww_interlis_chxtf2_4INTERLIS_TIMESYSTEMSType_httpwww_interlis_chxtf2_4INTERLISCALENDAR', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 218, 2), )

    
    CALENDAR = property(__CALENDAR.value, __CALENDAR.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}TIMEOFDAYSYS uses Python identifier TIMEOFDAYSYS
    __TIMEOFDAYSYS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TIMEOFDAYSYS'), 'TIMEOFDAYSYS', '__httpwww_interlis_chxtf2_4INTERLIS_TIMESYSTEMSType_httpwww_interlis_chxtf2_4INTERLISTIMEOFDAYSYS', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 226, 2), )

    
    TIMEOFDAYSYS = property(__TIMEOFDAYSYS.value, __TIMEOFDAYSYS.set, None, None)

    _ElementMap.update({
        __CALENDAR.name() : __CALENDAR,
        __TIMEOFDAYSYS.name() : __TIMEOFDAYSYS
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.TIMESYSTEMSType = TIMESYSTEMSType
Namespace.addCategoryObject('typeBinding', 'TIMESYSTEMSType', TIMESYSTEMSType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}TimeOfDayType with content type ELEMENT_ONLY
class TimeOfDayType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}TimeOfDayType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TimeOfDayType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 244, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}extensions uses Python identifier extensions
    __extensions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extensions'), 'extensions', '__httpwww_interlis_chxtf2_4INTERLIS_TimeOfDayType_httpwww_interlis_chxtf2_4INTERLISextensions', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2), )

    
    extensions = property(__extensions.value, __extensions.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Hours uses Python identifier Hours
    __Hours = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Hours'), 'Hours', '__httpwww_interlis_chxtf2_4INTERLIS_TimeOfDayType_httpwww_interlis_chxtf2_4INTERLISHours', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 247, 6), )

    
    Hours = property(__Hours.value, __Hours.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Minutes uses Python identifier Minutes
    __Minutes = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Minutes'), 'Minutes', '__httpwww_interlis_chxtf2_4INTERLIS_TimeOfDayType_httpwww_interlis_chxtf2_4INTERLISMinutes', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 255, 6), )

    
    Minutes = property(__Minutes.value, __Minutes.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Seconds uses Python identifier Seconds
    __Seconds = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Seconds'), 'Seconds', '__httpwww_interlis_chxtf2_4INTERLIS_TimeOfDayType_httpwww_interlis_chxtf2_4INTERLISSeconds', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 263, 6), )

    
    Seconds = property(__Seconds.value, __Seconds.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __extensions.name() : __extensions,
        __Hours.name() : __Hours,
        __Minutes.name() : __Minutes,
        __Seconds.name() : __Seconds
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.TimeOfDayType = TimeOfDayType
Namespace.addCategoryObject('typeBinding', 'TimeOfDayType', TimeOfDayType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}GregorianDateType with content type ELEMENT_ONLY
class GregorianDateType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}GregorianDateType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GregorianDateType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 283, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}extensions uses Python identifier extensions
    __extensions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extensions'), 'extensions', '__httpwww_interlis_chxtf2_4INTERLIS_GregorianDateType_httpwww_interlis_chxtf2_4INTERLISextensions', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2), )

    
    extensions = property(__extensions.value, __extensions.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Year uses Python identifier Year
    __Year = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Year'), 'Year', '__httpwww_interlis_chxtf2_4INTERLIS_GregorianDateType_httpwww_interlis_chxtf2_4INTERLISYear', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 286, 6), )

    
    Year = property(__Year.value, __Year.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Month uses Python identifier Month
    __Month = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Month'), 'Month', '__httpwww_interlis_chxtf2_4INTERLIS_GregorianDateType_httpwww_interlis_chxtf2_4INTERLISMonth', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 287, 6), )

    
    Month = property(__Month.value, __Month.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Day uses Python identifier Day
    __Day = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Day'), 'Day', '__httpwww_interlis_chxtf2_4INTERLIS_GregorianDateType_httpwww_interlis_chxtf2_4INTERLISDay', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 295, 6), )

    
    Day = property(__Day.value, __Day.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __extensions.name() : __extensions,
        __Year.name() : __Year,
        __Month.name() : __Month,
        __Day.name() : __Day
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.GregorianDateType = GregorianDateType
Namespace.addCategoryObject('typeBinding', 'GregorianDateType', GregorianDateType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}SurfaceEdgeType with content type ELEMENT_ONLY
class SurfaceEdgeType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}SurfaceEdgeType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SurfaceEdgeType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 348, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}extensions uses Python identifier extensions
    __extensions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extensions'), 'extensions', '__httpwww_interlis_chxtf2_4INTERLIS_SurfaceEdgeType_httpwww_interlis_chxtf2_4INTERLISextensions', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2), )

    
    extensions = property(__extensions.value, __extensions.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Geometry uses Python identifier Geometry
    __Geometry = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Geometry'), 'Geometry', '__httpwww_interlis_chxtf2_4INTERLIS_SurfaceEdgeType_httpwww_interlis_chxtf2_4INTERLISGeometry', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 351, 6), )

    
    Geometry = property(__Geometry.value, __Geometry.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __extensions.name() : __extensions,
        __Geometry.name() : __Geometry
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.SurfaceEdgeType = SurfaceEdgeType
Namespace.addCategoryObject('typeBinding', 'SurfaceEdgeType', SurfaceEdgeType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}SurfaceBoundaryType with content type ELEMENT_ONLY
class SurfaceBoundaryType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}SurfaceBoundaryType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SurfaceBoundaryType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 356, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}extensions uses Python identifier extensions
    __extensions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extensions'), 'extensions', '__httpwww_interlis_chxtf2_4INTERLIS_SurfaceBoundaryType_httpwww_interlis_chxtf2_4INTERLISextensions', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2), )

    
    extensions = property(__extensions.value, __extensions.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Lines uses Python identifier Lines
    __Lines = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Lines'), 'Lines', '__httpwww_interlis_chxtf2_4INTERLIS_SurfaceBoundaryType_httpwww_interlis_chxtf2_4INTERLISLines', True, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 359, 6), )

    
    Lines = property(__Lines.value, __Lines.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __extensions.name() : __extensions,
        __Lines.name() : __Lines
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.SurfaceBoundaryType = SurfaceBoundaryType
Namespace.addCategoryObject('typeBinding', 'SurfaceBoundaryType', SurfaceBoundaryType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 360, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}SurfaceEdge uses Python identifier SurfaceEdge
    __SurfaceEdge = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SurfaceEdge'), 'SurfaceEdge', '__httpwww_interlis_chxtf2_4INTERLIS_CTD_ANON_5_httpwww_interlis_chxtf2_4INTERLISSurfaceEdge', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 347, 2), )

    
    SurfaceEdge = property(__SurfaceEdge.value, __SurfaceEdge.set, None, None)

    _ElementMap.update({
        __SurfaceEdge.name() : __SurfaceEdge
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_5 = CTD_ANON_5


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}LineGeometryType with content type ELEMENT_ONLY
class LineGeometryType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}LineGeometryType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LineGeometryType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 370, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}extensions uses Python identifier extensions
    __extensions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extensions'), 'extensions', '__httpwww_interlis_chxtf2_4INTERLIS_LineGeometryType_httpwww_interlis_chxtf2_4INTERLISextensions', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2), )

    
    extensions = property(__extensions.value, __extensions.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Segments uses Python identifier Segments
    __Segments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Segments'), 'Segments', '__httpwww_interlis_chxtf2_4INTERLIS_LineGeometryType_httpwww_interlis_chxtf2_4INTERLISSegments', True, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 373, 6), )

    
    Segments = property(__Segments.value, __Segments.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __extensions.name() : __extensions,
        __Segments.name() : __Segments
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.LineGeometryType = LineGeometryType
Namespace.addCategoryObject('typeBinding', 'LineGeometryType', LineGeometryType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType with content type ELEMENT_ONLY
class METAOBJECTType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'METAOBJECTType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 135, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}extensions uses Python identifier extensions
    __extensions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extensions'), 'extensions', '__httpwww_interlis_chxtf2_4INTERLIS_METAOBJECTType_httpwww_interlis_chxtf2_4INTERLISextensions', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2), )

    
    extensions = property(__extensions.value, __extensions.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Name'), 'Name', '__httpwww_interlis_chxtf2_4INTERLIS_METAOBJECTType_httpwww_interlis_chxtf2_4INTERLISName', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6), )

    
    Name = property(__Name.value, __Name.set, None, None)

    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}tid uses Python identifier tid
    __tid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'tid'), 'tid', '__httpwww_interlis_chxtf2_4INTERLIS_METAOBJECTType_httpwww_interlis_chxtf2_4INTERLIStid', _module_typeBindings.tidType, required=True)
    __tid._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 17, 2)
    __tid._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 147, 4)
    
    tid = property(__tid.value, __tid.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __extensions.name() : __extensions,
        __Name.name() : __Name
    })
    _AttributeMap.update({
        __tid.name() : __tid
    })
_module_typeBindings.METAOBJECTType = METAOBJECTType
Namespace.addCategoryObject('typeBinding', 'METAOBJECTType', METAOBJECTType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECT_TRANSLATIONType with content type ELEMENT_ONLY
class METAOBJECT_TRANSLATIONType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECT_TRANSLATIONType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'METAOBJECT_TRANSLATIONType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 151, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}extensions uses Python identifier extensions
    __extensions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extensions'), 'extensions', '__httpwww_interlis_chxtf2_4INTERLIS_METAOBJECT_TRANSLATIONType_httpwww_interlis_chxtf2_4INTERLISextensions', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2), )

    
    extensions = property(__extensions.value, __extensions.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Name'), 'Name', '__httpwww_interlis_chxtf2_4INTERLIS_METAOBJECT_TRANSLATIONType_httpwww_interlis_chxtf2_4INTERLISName', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 154, 6), )

    
    Name = property(__Name.value, __Name.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}NameInBaseLanguage uses Python identifier NameInBaseLanguage
    __NameInBaseLanguage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NameInBaseLanguage'), 'NameInBaseLanguage', '__httpwww_interlis_chxtf2_4INTERLIS_METAOBJECT_TRANSLATIONType_httpwww_interlis_chxtf2_4INTERLISNameInBaseLanguage', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 162, 6), )

    
    NameInBaseLanguage = property(__NameInBaseLanguage.value, __NameInBaseLanguage.set, None, None)

    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}tid uses Python identifier tid
    __tid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'tid'), 'tid', '__httpwww_interlis_chxtf2_4INTERLIS_METAOBJECT_TRANSLATIONType_httpwww_interlis_chxtf2_4INTERLIStid', _module_typeBindings.tidType, required=True)
    __tid._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 17, 2)
    __tid._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 171, 4)
    
    tid = property(__tid.value, __tid.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __extensions.name() : __extensions,
        __Name.name() : __Name,
        __NameInBaseLanguage.name() : __NameInBaseLanguage
    })
    _AttributeMap.update({
        __tid.name() : __tid
    })
_module_typeBindings.METAOBJECT_TRANSLATIONType = METAOBJECT_TRANSLATIONType
Namespace.addCategoryObject('typeBinding', 'METAOBJECT_TRANSLATIONType', METAOBJECT_TRANSLATIONType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}UTCType with content type ELEMENT_ONLY
class UTCType (TimeOfDayType):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}UTCType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'UTCType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 275, 2)
    _ElementMap = TimeOfDayType._ElementMap.copy()
    _AttributeMap = TimeOfDayType._AttributeMap.copy()
    # Base type is TimeOfDayType
    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}TimeOfDayType
    
    # Element Hours ({http://www.interlis.ch/xtf/2.4/INTERLIS}Hours) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}TimeOfDayType
    
    # Element Minutes ({http://www.interlis.ch/xtf/2.4/INTERLIS}Minutes) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}TimeOfDayType
    
    # Element Seconds ({http://www.interlis.ch/xtf/2.4/INTERLIS}Seconds) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}TimeOfDayType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.UTCType = UTCType
Namespace.addCategoryObject('typeBinding', 'UTCType', UTCType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}GregorianDateTimeType with content type ELEMENT_ONLY
class GregorianDateTimeType (GregorianDateType):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}GregorianDateTimeType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GregorianDateTimeType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 307, 2)
    _ElementMap = GregorianDateType._ElementMap.copy()
    _AttributeMap = GregorianDateType._AttributeMap.copy()
    # Base type is GregorianDateType
    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}GregorianDateType
    
    # Element Year ({http://www.interlis.ch/xtf/2.4/INTERLIS}Year) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}GregorianDateType
    
    # Element Month ({http://www.interlis.ch/xtf/2.4/INTERLIS}Month) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}GregorianDateType
    
    # Element Day ({http://www.interlis.ch/xtf/2.4/INTERLIS}Day) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}GregorianDateType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Hours uses Python identifier Hours
    __Hours = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Hours'), 'Hours', '__httpwww_interlis_chxtf2_4INTERLIS_GregorianDateTimeType_httpwww_interlis_chxtf2_4INTERLISHours', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 311, 10), )

    
    Hours = property(__Hours.value, __Hours.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Minutes uses Python identifier Minutes
    __Minutes = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Minutes'), 'Minutes', '__httpwww_interlis_chxtf2_4INTERLIS_GregorianDateTimeType_httpwww_interlis_chxtf2_4INTERLISMinutes', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 319, 10), )

    
    Minutes = property(__Minutes.value, __Minutes.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Seconds uses Python identifier Seconds
    __Seconds = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Seconds'), 'Seconds', '__httpwww_interlis_chxtf2_4INTERLIS_GregorianDateTimeType_httpwww_interlis_chxtf2_4INTERLISSeconds', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 327, 10), )

    
    Seconds = property(__Seconds.value, __Seconds.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __Hours.name() : __Hours,
        __Minutes.name() : __Minutes,
        __Seconds.name() : __Seconds
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.GregorianDateTimeType = GregorianDateTimeType
Namespace.addCategoryObject('typeBinding', 'GregorianDateTimeType', GregorianDateTimeType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}LineSegmentType with content type ELEMENT_ONLY
class LineSegmentType (_ImportedBinding_camac_gis_export_so_schema_geometry.LineSegmentType):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}LineSegmentType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LineSegmentType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 341, 2)
    _ElementMap = _ImportedBinding_camac_gis_export_so_schema_geometry.LineSegmentType._ElementMap.copy()
    _AttributeMap = _ImportedBinding_camac_gis_export_so_schema_geometry.LineSegmentType._AttributeMap.copy()
    # Base type is _ImportedBinding_camac_gis_export_so_schema_geometry.LineSegmentType
    
    # Element extensions ({http://www.interlis.ch/geometry/1.0}extensions) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    
    # Element c1 ({http://www.interlis.ch/geometry/1.0}c1) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    
    # Element c2 ({http://www.interlis.ch/geometry/1.0}c2) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    
    # Element c3 ({http://www.interlis.ch/geometry/1.0}c3) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.LineSegmentType = LineSegmentType
Namespace.addCategoryObject('typeBinding', 'LineSegmentType', LineSegmentType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}REFSYSTEMType with content type ELEMENT_ONLY
class REFSYSTEMType (METAOBJECTType):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}REFSYSTEMType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'REFSYSTEMType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 179, 2)
    _ElementMap = METAOBJECTType._ElementMap.copy()
    _AttributeMap = METAOBJECTType._AttributeMap.copy()
    # Base type is METAOBJECTType
    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.REFSYSTEMType = REFSYSTEMType
Namespace.addCategoryObject('typeBinding', 'REFSYSTEMType', REFSYSTEMType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}SIGNType with content type ELEMENT_ONLY
class SIGNType (METAOBJECTType):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}SIGNType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SIGNType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 211, 2)
    _ElementMap = METAOBJECTType._ElementMap.copy()
    _AttributeMap = METAOBJECTType._AttributeMap.copy()
    # Base type is METAOBJECTType
    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.SIGNType = SIGNType
Namespace.addCategoryObject('typeBinding', 'SIGNType', SIGNType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}COORDSYSTEMType with content type ELEMENT_ONLY
class COORDSYSTEMType (REFSYSTEMType):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}COORDSYSTEMType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'COORDSYSTEMType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 187, 2)
    _ElementMap = REFSYSTEMType._ElementMap.copy()
    _AttributeMap = REFSYSTEMType._AttributeMap.copy()
    # Base type is REFSYSTEMType
    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element {http://www.interlis.ch/xtf/2.4/INTERLIS}Axis uses Python identifier Axis
    __Axis = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Axis'), 'Axis', '__httpwww_interlis_chxtf2_4INTERLIS_COORDSYSTEMType_httpwww_interlis_chxtf2_4INTERLISAxis', True, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10), )

    
    Axis = property(__Axis.value, __Axis.set, None, None)

    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __Axis.name() : __Axis
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.COORDSYSTEMType = COORDSYSTEMType
Namespace.addCategoryObject('typeBinding', 'COORDSYSTEMType', COORDSYSTEMType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}SCALSYSTEMType with content type ELEMENT_ONLY
class SCALSYSTEMType (REFSYSTEMType):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}SCALSYSTEMType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SCALSYSTEMType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 203, 2)
    _ElementMap = REFSYSTEMType._ElementMap.copy()
    _AttributeMap = REFSYSTEMType._AttributeMap.copy()
    # Base type is REFSYSTEMType
    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.SCALSYSTEMType = SCALSYSTEMType
Namespace.addCategoryObject('typeBinding', 'SCALSYSTEMType', SCALSYSTEMType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}CALENDARType with content type ELEMENT_ONLY
class CALENDARType (SCALSYSTEMType):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}CALENDARType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CALENDARType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 219, 2)
    _ElementMap = SCALSYSTEMType._ElementMap.copy()
    _AttributeMap = SCALSYSTEMType._AttributeMap.copy()
    # Base type is SCALSYSTEMType
    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CALENDARType = CALENDARType
Namespace.addCategoryObject('typeBinding', 'CALENDARType', CALENDARType)


# Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}TIMEOFDAYSYSType with content type ELEMENT_ONLY
class TIMEOFDAYSYSType (SCALSYSTEMType):
    """Complex type {http://www.interlis.ch/xtf/2.4/INTERLIS}TIMEOFDAYSYSType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TIMEOFDAYSYSType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 227, 2)
    _ElementMap = SCALSYSTEMType._ElementMap.copy()
    _AttributeMap = SCALSYSTEMType._AttributeMap.copy()
    # Base type is SCALSYSTEMType
    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.TIMEOFDAYSYSType = TIMEOFDAYSYSType
Namespace.addCategoryObject('typeBinding', 'TIMEOFDAYSYSType', TIMEOFDAYSYSType)


extensions = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensions'), CTD_ANON, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2))
Namespace.addCategoryObject('elementBinding', extensions.name().localName(), extensions)

transfer = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'transfer'), TransferType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 68, 2))
Namespace.addCategoryObject('elementBinding', transfer.name().localName(), transfer)

AXIS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AXIS'), AXISType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 174, 2))
Namespace.addCategoryObject('elementBinding', AXIS.name().localName(), AXIS)

TIMESYSTEMS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TIMESYSTEMS'), TIMESYSTEMSType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 234, 2))
Namespace.addCategoryObject('elementBinding', TIMESYSTEMS.name().localName(), TIMESYSTEMS)

TimeOfDay = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TimeOfDay'), TimeOfDayType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 243, 2))
Namespace.addCategoryObject('elementBinding', TimeOfDay.name().localName(), TimeOfDay)

GregorianDate = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GregorianDate'), GregorianDateType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 282, 2))
Namespace.addCategoryObject('elementBinding', GregorianDate.name().localName(), GregorianDate)

SurfaceEdge = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SurfaceEdge'), SurfaceEdgeType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 347, 2))
Namespace.addCategoryObject('elementBinding', SurfaceEdge.name().localName(), SurfaceEdge)

SurfaceBoundary = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SurfaceBoundary'), SurfaceBoundaryType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 355, 2))
Namespace.addCategoryObject('elementBinding', SurfaceBoundary.name().localName(), SurfaceBoundary)

LineGeometry = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LineGeometry'), LineGeometryType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 369, 2))
Namespace.addCategoryObject('elementBinding', LineGeometry.name().localName(), LineGeometry)

METAOBJECT = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'METAOBJECT'), METAOBJECTType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 134, 2))
Namespace.addCategoryObject('elementBinding', METAOBJECT.name().localName(), METAOBJECT)

METAOBJECT_TRANSLATION = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'METAOBJECT_TRANSLATION'), METAOBJECT_TRANSLATIONType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 150, 2))
Namespace.addCategoryObject('elementBinding', METAOBJECT_TRANSLATION.name().localName(), METAOBJECT_TRANSLATION)

UTC = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UTC'), UTCType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 274, 2))
Namespace.addCategoryObject('elementBinding', UTC.name().localName(), UTC)

GregorianDateTime = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GregorianDateTime'), GregorianDateTimeType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 306, 2))
Namespace.addCategoryObject('elementBinding', GregorianDateTime.name().localName(), GregorianDateTime)

LineSegment = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LineSegment'), LineSegmentType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 340, 2))
Namespace.addCategoryObject('elementBinding', LineSegment.name().localName(), LineSegment)

REFSYSTEM = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'REFSYSTEM'), REFSYSTEMType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 178, 2))
Namespace.addCategoryObject('elementBinding', REFSYSTEM.name().localName(), REFSYSTEM)

SIGN = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SIGN'), SIGNType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 210, 2))
Namespace.addCategoryObject('elementBinding', SIGN.name().localName(), SIGN)

COORDSYSTEM = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'COORDSYSTEM'), COORDSYSTEMType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 186, 2))
Namespace.addCategoryObject('elementBinding', COORDSYSTEM.name().localName(), COORDSYSTEM)

SCALSYSTEM = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SCALSYSTEM'), SCALSYSTEMType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 202, 2))
Namespace.addCategoryObject('elementBinding', SCALSYSTEM.name().localName(), SCALSYSTEM)

CALENDAR = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CALENDAR'), CALENDARType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 218, 2))
Namespace.addCategoryObject('elementBinding', CALENDAR.name().localName(), CALENDAR)

TIMEOFDAYSYS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TIMEOFDAYSYS'), TIMEOFDAYSYSType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 226, 2))
Namespace.addCategoryObject('elementBinding', TIMEOFDAYSYS.name().localName(), TIMEOFDAYSYS)



def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 12, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 12, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




TransferType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'headersection'), CTD_ANON_, scope=TransferType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 71, 6)))

TransferType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'datasection'), CTD_ANON_3, scope=TransferType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 87, 6)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TransferType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'headersection')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 71, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TransferType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'datasection')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 87, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
TransferType._Automaton = _BuildAutomaton_()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensions'), CTD_ANON, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'models'), CTD_ANON_2, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 74, 12)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sender'), pyxb.binding.datatypes.string, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 81, 12)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comment'), pyxb.binding.datatypes.string, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 82, 12)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 81, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 82, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 83, 12))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'models')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 74, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sender')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 81, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comment')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 82, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 83, 12))
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
CTD_ANON_._Automaton = _BuildAutomaton_2()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'model'), pyxb.binding.datatypes.token, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 77, 18)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'model')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 77, 18))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_3()




def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 90, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_strict, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 90, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_4()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AXIS'), AXISType, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 174, 2)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AXIS')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 194, 16))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_4._Automaton = _BuildAutomaton_5()




TIMESYSTEMSType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CALENDAR'), CALENDARType, scope=TIMESYSTEMSType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 218, 2)))

TIMESYSTEMSType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TIMEOFDAYSYS'), TIMEOFDAYSYSType, scope=TIMESYSTEMSType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 226, 2)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TIMESYSTEMSType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CALENDAR')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 238, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TIMESYSTEMSType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TIMEOFDAYSYS')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 239, 8))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
TIMESYSTEMSType._Automaton = _BuildAutomaton_6()




TimeOfDayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensions'), CTD_ANON, scope=TimeOfDayType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2)))

TimeOfDayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Hours'), STD_ANON_3, scope=TimeOfDayType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 247, 6)))

TimeOfDayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Minutes'), STD_ANON_4, scope=TimeOfDayType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 255, 6)))

TimeOfDayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Seconds'), STD_ANON_5, scope=TimeOfDayType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 263, 6)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 246, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 247, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 255, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 263, 6))
    counters.add(cc_3)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TimeOfDayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 246, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TimeOfDayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Hours')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 247, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(TimeOfDayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Minutes')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 255, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(TimeOfDayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Seconds')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 263, 6))
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
TimeOfDayType._Automaton = _BuildAutomaton_7()




GregorianDateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensions'), CTD_ANON, scope=GregorianDateType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2)))

GregorianDateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Year'), pyxb.binding.datatypes.gYear, scope=GregorianDateType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 286, 6)))

GregorianDateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Month'), STD_ANON_6, scope=GregorianDateType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 287, 6)))

GregorianDateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Day'), STD_ANON_7, scope=GregorianDateType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 295, 6)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 285, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 286, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 287, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 295, 6))
    counters.add(cc_3)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(GregorianDateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 285, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(GregorianDateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Year')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 286, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(GregorianDateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Month')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 287, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(GregorianDateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Day')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 295, 6))
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
GregorianDateType._Automaton = _BuildAutomaton_8()




SurfaceEdgeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensions'), CTD_ANON, scope=SurfaceEdgeType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2)))

SurfaceEdgeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Geometry'), _ImportedBinding_camac_gis_export_so_schema_geometry.PolylineType, scope=SurfaceEdgeType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 351, 6)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 350, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 351, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SurfaceEdgeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 350, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(SurfaceEdgeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Geometry')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 351, 6))
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
SurfaceEdgeType._Automaton = _BuildAutomaton_9()




SurfaceBoundaryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensions'), CTD_ANON, scope=SurfaceBoundaryType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2)))

SurfaceBoundaryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Lines'), CTD_ANON_5, scope=SurfaceBoundaryType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 359, 6)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 358, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SurfaceBoundaryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 358, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SurfaceBoundaryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Lines')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 359, 6))
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
         ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SurfaceBoundaryType._Automaton = _BuildAutomaton_10()




CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SurfaceEdge'), SurfaceEdgeType, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 347, 2)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SurfaceEdge')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 362, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_5._Automaton = _BuildAutomaton_11()




LineGeometryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensions'), CTD_ANON, scope=LineGeometryType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2)))

LineGeometryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Segments'), _ImportedBinding_camac_gis_export_so_schema_geometry.LineSegmentType, scope=LineGeometryType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 373, 6)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 372, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LineGeometryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 372, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(LineGeometryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Segments')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 373, 6))
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
         ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
LineGeometryType._Automaton = _BuildAutomaton_12()




METAOBJECTType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensions'), CTD_ANON, scope=METAOBJECTType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2)))

METAOBJECTType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Name'), STD_ANON, scope=METAOBJECTType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(METAOBJECTType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(METAOBJECTType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
METAOBJECTType._Automaton = _BuildAutomaton_13()




METAOBJECT_TRANSLATIONType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensions'), CTD_ANON, scope=METAOBJECT_TRANSLATIONType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 9, 2)))

METAOBJECT_TRANSLATIONType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Name'), STD_ANON_, scope=METAOBJECT_TRANSLATIONType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 154, 6)))

METAOBJECT_TRANSLATIONType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NameInBaseLanguage'), STD_ANON_2, scope=METAOBJECT_TRANSLATIONType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 162, 6)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 153, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(METAOBJECT_TRANSLATIONType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 153, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(METAOBJECT_TRANSLATIONType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 154, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(METAOBJECT_TRANSLATIONType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NameInBaseLanguage')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 162, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
METAOBJECT_TRANSLATIONType._Automaton = _BuildAutomaton_14()




def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 246, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 247, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 255, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 263, 6))
    counters.add(cc_3)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(UTCType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 246, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(UTCType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Hours')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 247, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(UTCType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Minutes')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 255, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(UTCType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Seconds')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 263, 6))
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
UTCType._Automaton = _BuildAutomaton_15()




GregorianDateTimeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Hours'), STD_ANON_8, scope=GregorianDateTimeType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 311, 10)))

GregorianDateTimeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Minutes'), STD_ANON_9, scope=GregorianDateTimeType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 319, 10)))

GregorianDateTimeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Seconds'), STD_ANON_10, scope=GregorianDateTimeType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 327, 10)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 285, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 286, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 287, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 295, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 311, 10))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 319, 10))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 327, 10))
    counters.add(cc_6)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(GregorianDateTimeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 285, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(GregorianDateTimeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Year')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 286, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(GregorianDateTimeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Month')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 287, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(GregorianDateTimeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Day')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 295, 6))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(GregorianDateTimeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Hours')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 311, 10))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(GregorianDateTimeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Minutes')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 319, 10))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(GregorianDateTimeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Seconds')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 327, 10))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
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
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
GregorianDateTimeType._Automaton = _BuildAutomaton_16()




def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/geometry.xsd', 51, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/geometry.xsd', 54, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LineSegmentType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/geometry.xsd', 51, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LineSegmentType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'c1')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/geometry.xsd', 52, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(LineSegmentType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'c2')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/geometry.xsd', 53, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(LineSegmentType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'c3')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/geometry.xsd', 54, 6))
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
LineSegmentType._Automaton = _BuildAutomaton_17()




def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(REFSYSTEMType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(REFSYSTEMType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
REFSYSTEMType._Automaton = _BuildAutomaton_18()




def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SIGNType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SIGNType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SIGNType._Automaton = _BuildAutomaton_19()




COORDSYSTEMType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Axis'), CTD_ANON_4, scope=COORDSYSTEMType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=1, max=3, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(COORDSYSTEMType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(COORDSYSTEMType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(COORDSYSTEMType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Axis')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
COORDSYSTEMType._Automaton = _BuildAutomaton_20()




def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SCALSYSTEMType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SCALSYSTEMType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SCALSYSTEMType._Automaton = _BuildAutomaton_21()




def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CALENDARType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CALENDARType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CALENDARType._Automaton = _BuildAutomaton_22()




def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TIMEOFDAYSYSType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TIMEOFDAYSYSType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
TIMEOFDAYSYSType._Automaton = _BuildAutomaton_23()


UTC._setSubstitutionGroup(TimeOfDay)

GregorianDateTime._setSubstitutionGroup(GregorianDate)

LineSegment._setSubstitutionGroup(_ImportedBinding_camac_gis_export_so_schema_geometry.customLineSegment)

REFSYSTEM._setSubstitutionGroup(METAOBJECT)

SIGN._setSubstitutionGroup(METAOBJECT)

COORDSYSTEM._setSubstitutionGroup(REFSYSTEM)

SCALSYSTEM._setSubstitutionGroup(REFSYSTEM)

CALENDAR._setSubstitutionGroup(SCALSYSTEM)

TIMEOFDAYSYS._setSubstitutionGroup(SCALSYSTEM)
