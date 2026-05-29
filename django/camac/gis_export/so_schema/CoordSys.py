# ../../../camac/gis_export/so_schema/CoordSys.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:905db62da4e3209f4853aec3e646ec36d1fd4d52
# Generated 2026-07-15 11:48:20.603342 by PyXB version 1.2.6 using Python 3.12.13.final.0
# Namespace http://www.interlis.ch/xtf/2.4/CoordSys [xmlns:CoordSys]

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
import camac.gis_export.so_schema.INTERLIS as _ImportedBinding_camac_gis_export_so_schema_INTERLIS
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.interlis.ch/xtf/2.4/CoordSys', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])
_Namespace_INTERLIS = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.Namespace
_Namespace_INTERLIS.configureCategories(['typeBinding', 'elementBinding'])

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


# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 23, 6)
    _Documentation = None
STD_ANON._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(180), value_datatype=STD_ANON)
STD_ANON._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(-180), value_datatype=STD_ANON)
STD_ANON._InitializeFacetMap(STD_ANON._CF_maxInclusive,
   STD_ANON._CF_minInclusive)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 31, 6)
    _Documentation = None
STD_ANON_._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(59), value_datatype=STD_ANON_)
STD_ANON_._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(0), value_datatype=STD_ANON_)
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_maxInclusive,
   STD_ANON_._CF_minInclusive)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Atomic simple type: [anonymous]
class STD_ANON_2 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 39, 6)
    _Documentation = None
STD_ANON_2._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.decimal('59.999'), value_datatype=STD_ANON_2)
STD_ANON_2._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.decimal('0.0'), value_datatype=STD_ANON_2)
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_maxInclusive,
   STD_ANON_2._CF_minInclusive)
_module_typeBindings.STD_ANON_2 = STD_ANON_2

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/CoordSys}Angle_DMS
class Angle_DMS (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Angle_DMS')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 48, 0)
    _Documentation = None
Angle_DMS._CF_pattern = pyxb.binding.facets.CF_pattern()
Angle_DMS._CF_pattern.addPattern(pattern='([\\+\\-0-9\\.]+):([\\+\\-0-9\\.]+):([\\+\\-0-9\\.]+)')
Angle_DMS._InitializeFacetMap(Angle_DMS._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'Angle_DMS', Angle_DMS)
_module_typeBindings.Angle_DMS = Angle_DMS

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/CoordSys}Angle_DMS_90
class Angle_DMS_90 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Angle_DMS_90')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 53, 0)
    _Documentation = None
Angle_DMS_90._CF_pattern = pyxb.binding.facets.CF_pattern()
Angle_DMS_90._CF_pattern.addPattern(pattern='([\\+\\-0-9\\.]+):([\\+\\-0-9\\.]+):([\\+\\-0-9\\.]+)')
Angle_DMS_90._InitializeFacetMap(Angle_DMS_90._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'Angle_DMS_90', Angle_DMS_90)
_module_typeBindings.Angle_DMS_90 = Angle_DMS_90

# Atomic simple type: [anonymous]
class STD_ANON_3 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 64, 10)
    _Documentation = None
STD_ANON_3._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(70))
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_maxLength)
_module_typeBindings.STD_ANON_3 = STD_ANON_3

# Atomic simple type: [anonymous]
class STD_ANON_4 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 71, 10)
    _Documentation = None
STD_ANON_4._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.decimal('6390000.0'), value_datatype=STD_ANON_4)
STD_ANON_4._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.decimal('6360000.0'), value_datatype=STD_ANON_4)
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_maxInclusive,
   STD_ANON_4._CF_minInclusive)
_module_typeBindings.STD_ANON_4 = STD_ANON_4

# Atomic simple type: [anonymous]
class STD_ANON_5 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 79, 10)
    _Documentation = None
STD_ANON_5._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.decimal('350.0'), value_datatype=STD_ANON_5)
STD_ANON_5._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.decimal('0.0'), value_datatype=STD_ANON_5)
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_maxInclusive,
   STD_ANON_5._CF_minInclusive)
_module_typeBindings.STD_ANON_5 = STD_ANON_5

# Atomic simple type: [anonymous]
class STD_ANON_6 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 87, 10)
    _Documentation = None
STD_ANON_6._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(70))
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_maxLength)
_module_typeBindings.STD_ANON_6 = STD_ANON_6

# Atomic simple type: [anonymous]
class STD_ANON_7 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 103, 10)
    _Documentation = None
STD_ANON_7._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(70))
STD_ANON_7._InitializeFacetMap(STD_ANON_7._CF_maxLength)
_module_typeBindings.STD_ANON_7 = STD_ANON_7

# Atomic simple type: [anonymous]
class STD_ANON_8 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 110, 10)
    _Documentation = None
STD_ANON_8._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(70))
STD_ANON_8._InitializeFacetMap(STD_ANON_8._CF_maxLength)
_module_typeBindings.STD_ANON_8 = STD_ANON_8

# Atomic simple type: [anonymous]
class STD_ANON_9 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 126, 10)
    _Documentation = None
STD_ANON_9._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(70))
STD_ANON_9._InitializeFacetMap(STD_ANON_9._CF_maxLength)
_module_typeBindings.STD_ANON_9 = STD_ANON_9

# Atomic simple type: [anonymous]
class STD_ANON_10 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 133, 10)
    _Documentation = None
STD_ANON_10._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(70))
STD_ANON_10._InitializeFacetMap(STD_ANON_10._CF_maxLength)
_module_typeBindings.STD_ANON_10 = STD_ANON_10

# Atomic simple type: [anonymous]
class STD_ANON_11 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 149, 10)
    _Documentation = None
STD_ANON_11._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
STD_ANON_11._InitializeFacetMap(STD_ANON_11._CF_maxLength)
_module_typeBindings.STD_ANON_11 = STD_ANON_11

# Atomic simple type: [anonymous]
class STD_ANON_12 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 156, 10)
    _Documentation = None
STD_ANON_12._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(255))
STD_ANON_12._InitializeFacetMap(STD_ANON_12._CF_maxLength)
_module_typeBindings.STD_ANON_12 = STD_ANON_12

# Atomic simple type: [anonymous]
class STD_ANON_13 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 172, 10)
    _Documentation = None
STD_ANON_13._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(12))
STD_ANON_13._InitializeFacetMap(STD_ANON_13._CF_maxLength)
_module_typeBindings.STD_ANON_13 = STD_ANON_13

# Atomic simple type: [anonymous]
class STD_ANON_14 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 179, 10)
    _Documentation = None
STD_ANON_14._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(255))
STD_ANON_14._InitializeFacetMap(STD_ANON_14._CF_maxLength)
_module_typeBindings.STD_ANON_14 = STD_ANON_14

# Atomic simple type: [anonymous]
class STD_ANON_15 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 204, 10)
    _Documentation = None
STD_ANON_15._InitializeFacetMap()
_module_typeBindings.STD_ANON_15 = STD_ANON_15

# Atomic simple type: [anonymous]
class STD_ANON_16 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 210, 10)
    _Documentation = None
STD_ANON_16._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.decimal('10000.0'), value_datatype=STD_ANON_16)
STD_ANON_16._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.decimal('-10000.0'), value_datatype=STD_ANON_16)
STD_ANON_16._InitializeFacetMap(STD_ANON_16._CF_maxInclusive,
   STD_ANON_16._CF_minInclusive)
_module_typeBindings.STD_ANON_16 = STD_ANON_16

# Atomic simple type: [anonymous]
class STD_ANON_17 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 218, 10)
    _Documentation = None
STD_ANON_17._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(70))
STD_ANON_17._InitializeFacetMap(STD_ANON_17._CF_maxLength)
_module_typeBindings.STD_ANON_17 = STD_ANON_17

# Atomic simple type: [anonymous]
class STD_ANON_18 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 273, 10)
    _Documentation = None
STD_ANON_18._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(70))
STD_ANON_18._InitializeFacetMap(STD_ANON_18._CF_maxLength)
_module_typeBindings.STD_ANON_18 = STD_ANON_18

# Atomic simple type: [anonymous]
class STD_ANON_19 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 289, 10)
    _Documentation = None
STD_ANON_19._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(70))
STD_ANON_19._InitializeFacetMap(STD_ANON_19._CF_maxLength)
_module_typeBindings.STD_ANON_19 = STD_ANON_19

# Atomic simple type: [anonymous]
class STD_ANON_20 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 305, 10)
    _Documentation = None
STD_ANON_20._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(70))
STD_ANON_20._InitializeFacetMap(STD_ANON_20._CF_maxLength)
_module_typeBindings.STD_ANON_20 = STD_ANON_20

# Atomic simple type: [anonymous]
class STD_ANON_21 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 397, 6)
    _Documentation = None
STD_ANON_21._InitializeFacetMap()
_module_typeBindings.STD_ANON_21 = STD_ANON_21

# Atomic simple type: [anonymous]
class STD_ANON_22 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 403, 6)
    _Documentation = None
STD_ANON_22._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.decimal('10000.0'), value_datatype=STD_ANON_22)
STD_ANON_22._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.decimal('-10000.0'), value_datatype=STD_ANON_22)
STD_ANON_22._InitializeFacetMap(STD_ANON_22._CF_maxInclusive,
   STD_ANON_22._CF_minInclusive)
_module_typeBindings.STD_ANON_22 = STD_ANON_22

# Atomic simple type: [anonymous]
class STD_ANON_23 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 411, 6)
    _Documentation = None
STD_ANON_23._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.decimal('10000.0'), value_datatype=STD_ANON_23)
STD_ANON_23._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.decimal('-10000.0'), value_datatype=STD_ANON_23)
STD_ANON_23._InitializeFacetMap(STD_ANON_23._CF_maxInclusive,
   STD_ANON_23._CF_minInclusive)
_module_typeBindings.STD_ANON_23 = STD_ANON_23

# Atomic simple type: [anonymous]
class STD_ANON_24 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 419, 6)
    _Documentation = None
STD_ANON_24._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.decimal('10000.0'), value_datatype=STD_ANON_24)
STD_ANON_24._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.decimal('-10000.0'), value_datatype=STD_ANON_24)
STD_ANON_24._InitializeFacetMap(STD_ANON_24._CF_maxInclusive,
   STD_ANON_24._CF_minInclusive)
_module_typeBindings.STD_ANON_24 = STD_ANON_24

# Atomic simple type: [anonymous]
class STD_ANON_25 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 430, 6)
    _Documentation = None
STD_ANON_25._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.decimal('1000000.0'), value_datatype=STD_ANON_25)
STD_ANON_25._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.decimal('0.000001'), value_datatype=STD_ANON_25)
STD_ANON_25._InitializeFacetMap(STD_ANON_25._CF_maxInclusive,
   STD_ANON_25._CF_minInclusive)
_module_typeBindings.STD_ANON_25 = STD_ANON_25

# Atomic simple type: [anonymous]
class STD_ANON_26 (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 470, 6)
    _Documentation = None
STD_ANON_26._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(10000000), value_datatype=STD_ANON_26)
STD_ANON_26._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(-10000000), value_datatype=STD_ANON_26)
STD_ANON_26._InitializeFacetMap(STD_ANON_26._CF_maxInclusive,
   STD_ANON_26._CF_minInclusive)
_module_typeBindings.STD_ANON_26 = STD_ANON_26

# Atomic simple type: [anonymous]
class STD_ANON_27 (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 478, 6)
    _Documentation = None
STD_ANON_27._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(10000000), value_datatype=STD_ANON_27)
STD_ANON_27._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(-10000000), value_datatype=STD_ANON_27)
STD_ANON_27._InitializeFacetMap(STD_ANON_27._CF_maxInclusive,
   STD_ANON_27._CF_minInclusive)
_module_typeBindings.STD_ANON_27 = STD_ANON_27

# Atomic simple type: [anonymous]
class STD_ANON_28 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 584, 6)
    _Documentation = None
STD_ANON_28._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(70))
STD_ANON_28._InitializeFacetMap(STD_ANON_28._CF_maxLength)
_module_typeBindings.STD_ANON_28 = STD_ANON_28

# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}Angle_DMS_SType with content type ELEMENT_ONLY
class Angle_DMS_SType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}Angle_DMS_SType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Angle_DMS_SType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 20, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}Degrees uses Python identifier Degrees
    __Degrees = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Degrees'), 'Degrees', '__httpwww_interlis_chxtf2_4CoordSys_Angle_DMS_SType_httpwww_interlis_chxtf2_4CoordSysDegrees', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 22, 4), )

    
    Degrees = property(__Degrees.value, __Degrees.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}Minutes uses Python identifier Minutes
    __Minutes = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Minutes'), 'Minutes', '__httpwww_interlis_chxtf2_4CoordSys_Angle_DMS_SType_httpwww_interlis_chxtf2_4CoordSysMinutes', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 30, 4), )

    
    Minutes = property(__Minutes.value, __Minutes.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}Seconds uses Python identifier Seconds
    __Seconds = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Seconds'), 'Seconds', '__httpwww_interlis_chxtf2_4CoordSys_Angle_DMS_SType_httpwww_interlis_chxtf2_4CoordSysSeconds', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 38, 4), )

    
    Seconds = property(__Seconds.value, __Seconds.set, None, None)

    _ElementMap.update({
        __Degrees.name() : __Degrees,
        __Minutes.name() : __Minutes,
        __Seconds.name() : __Seconds
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Angle_DMS_SType = Angle_DMS_SType
Namespace.addCategoryObject('typeBinding', 'Angle_DMS_SType', Angle_DMS_SType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}HeightEllipsType with content type EMPTY
class HeightEllipsType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}HeightEllipsType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'HeightEllipsType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 253, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.HeightEllipsType = HeightEllipsType
Namespace.addCategoryObject('typeBinding', 'HeightEllipsType', HeightEllipsType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}HeightGravitType with content type EMPTY
class HeightGravitType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}HeightGravitType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'HeightGravitType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 258, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.HeightGravitType = HeightGravitType
Namespace.addCategoryObject('typeBinding', 'HeightGravitType', HeightGravitType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}HeightGeoidType with content type EMPTY
class HeightGeoidType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}HeightGeoidType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'HeightGeoidType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 263, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.HeightGeoidType = HeightGeoidType
Namespace.addCategoryObject('typeBinding', 'HeightGeoidType', HeightGeoidType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}EllCSEllipsType with content type EMPTY
class EllCSEllipsType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}EllCSEllipsType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EllCSEllipsType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 324, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.EllCSEllipsType = EllCSEllipsType
Namespace.addCategoryObject('typeBinding', 'EllCSEllipsType', EllCSEllipsType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}ToGeoEllipsoidalType with content type ELEMENT_ONLY
class ToGeoEllipsoidalType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}ToGeoEllipsoidalType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ToGeoEllipsoidalType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 329, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}From uses Python identifier From
    __From = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'From'), 'From', '__httpwww_interlis_chxtf2_4CoordSys_ToGeoEllipsoidalType_httpwww_interlis_chxtf2_4CoordSysFrom', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 331, 4), )

    
    From = property(__From.value, __From.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}To uses Python identifier To
    __To = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'To'), 'To', '__httpwww_interlis_chxtf2_4CoordSys_ToGeoEllipsoidalType_httpwww_interlis_chxtf2_4CoordSysTo', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 336, 4), )

    
    To = property(__To.value, __To.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}ToHeight uses Python identifier ToHeight
    __ToHeight = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ToHeight'), 'ToHeight', '__httpwww_interlis_chxtf2_4CoordSys_ToGeoEllipsoidalType_httpwww_interlis_chxtf2_4CoordSysToHeight', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 341, 4), )

    
    ToHeight = property(__ToHeight.value, __ToHeight.set, None, None)

    _ElementMap.update({
        __From.name() : __From,
        __To.name() : __To,
        __ToHeight.name() : __ToHeight
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ToGeoEllipsoidalType = ToGeoEllipsoidalType
Namespace.addCategoryObject('typeBinding', 'ToGeoEllipsoidalType', ToGeoEllipsoidalType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}ToGeoCartesian3DType with content type ELEMENT_ONLY
class ToGeoCartesian3DType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}ToGeoCartesian3DType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ToGeoCartesian3DType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 349, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}From2 uses Python identifier From2
    __From2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'From2'), 'From2', '__httpwww_interlis_chxtf2_4CoordSys_ToGeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysFrom2', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 351, 4), )

    
    From2 = property(__From2.value, __From2.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}FromHeight uses Python identifier FromHeight
    __FromHeight = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FromHeight'), 'FromHeight', '__httpwww_interlis_chxtf2_4CoordSys_ToGeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysFromHeight', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 356, 4), )

    
    FromHeight = property(__FromHeight.value, __FromHeight.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}To3 uses Python identifier To3
    __To3 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'To3'), 'To3', '__httpwww_interlis_chxtf2_4CoordSys_ToGeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysTo3', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 361, 4), )

    
    To3 = property(__To3.value, __To3.set, None, None)

    _ElementMap.update({
        __From2.name() : __From2,
        __FromHeight.name() : __FromHeight,
        __To3.name() : __To3
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ToGeoCartesian3DType = ToGeoCartesian3DType
Namespace.addCategoryObject('typeBinding', 'ToGeoCartesian3DType', ToGeoCartesian3DType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}BidirectGeoCartesian2DType with content type ELEMENT_ONLY
class BidirectGeoCartesian2DType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}BidirectGeoCartesian2DType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoCartesian2DType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 369, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}From uses Python identifier From
    __From = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'From'), 'From', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoCartesian2DType_httpwww_interlis_chxtf2_4CoordSysFrom', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 371, 4), )

    
    From = property(__From.value, __From.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}To uses Python identifier To
    __To = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'To'), 'To', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoCartesian2DType_httpwww_interlis_chxtf2_4CoordSysTo', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 376, 4), )

    
    To = property(__To.value, __To.set, None, None)

    _ElementMap.update({
        __From.name() : __From,
        __To.name() : __To
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.BidirectGeoCartesian2DType = BidirectGeoCartesian2DType
Namespace.addCategoryObject('typeBinding', 'BidirectGeoCartesian2DType', BidirectGeoCartesian2DType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}BidirectGeoCartesian3DType with content type ELEMENT_ONLY
class BidirectGeoCartesian3DType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}BidirectGeoCartesian3DType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoCartesian3DType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 384, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}From uses Python identifier From
    __From = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'From'), 'From', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysFrom', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 386, 4), )

    
    From = property(__From.value, __From.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}To2 uses Python identifier To2
    __To2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'To2'), 'To2', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysTo2', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 391, 4), )

    
    To2 = property(__To2.value, __To2.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}Precision uses Python identifier Precision
    __Precision = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Precision'), 'Precision', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysPrecision', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 396, 4), )

    
    Precision = property(__Precision.value, __Precision.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}ShiftAxis1 uses Python identifier ShiftAxis1
    __ShiftAxis1 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ShiftAxis1'), 'ShiftAxis1', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysShiftAxis1', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 402, 4), )

    
    ShiftAxis1 = property(__ShiftAxis1.value, __ShiftAxis1.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}ShiftAxis2 uses Python identifier ShiftAxis2
    __ShiftAxis2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ShiftAxis2'), 'ShiftAxis2', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysShiftAxis2', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 410, 4), )

    
    ShiftAxis2 = property(__ShiftAxis2.value, __ShiftAxis2.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}ShiftAxis3 uses Python identifier ShiftAxis3
    __ShiftAxis3 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ShiftAxis3'), 'ShiftAxis3', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysShiftAxis3', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 418, 4), )

    
    ShiftAxis3 = property(__ShiftAxis3.value, __ShiftAxis3.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}RotationAxis1 uses Python identifier RotationAxis1
    __RotationAxis1 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RotationAxis1'), 'RotationAxis1', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysRotationAxis1', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 426, 4), )

    
    RotationAxis1 = property(__RotationAxis1.value, __RotationAxis1.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}RotationAxis2 uses Python identifier RotationAxis2
    __RotationAxis2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RotationAxis2'), 'RotationAxis2', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysRotationAxis2', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 427, 4), )

    
    RotationAxis2 = property(__RotationAxis2.value, __RotationAxis2.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}RotationAxis3 uses Python identifier RotationAxis3
    __RotationAxis3 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RotationAxis3'), 'RotationAxis3', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysRotationAxis3', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 428, 4), )

    
    RotationAxis3 = property(__RotationAxis3.value, __RotationAxis3.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}NewScale uses Python identifier NewScale
    __NewScale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NewScale'), 'NewScale', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysNewScale', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 429, 4), )

    
    NewScale = property(__NewScale.value, __NewScale.set, None, None)

    _ElementMap.update({
        __From.name() : __From,
        __To2.name() : __To2,
        __Precision.name() : __Precision,
        __ShiftAxis1.name() : __ShiftAxis1,
        __ShiftAxis2.name() : __ShiftAxis2,
        __ShiftAxis3.name() : __ShiftAxis3,
        __RotationAxis1.name() : __RotationAxis1,
        __RotationAxis2.name() : __RotationAxis2,
        __RotationAxis3.name() : __RotationAxis3,
        __NewScale.name() : __NewScale
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.BidirectGeoCartesian3DType = BidirectGeoCartesian3DType
Namespace.addCategoryObject('typeBinding', 'BidirectGeoCartesian3DType', BidirectGeoCartesian3DType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}BidirectGeoEllipsoidalType with content type ELEMENT_ONLY
class BidirectGeoEllipsoidalType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}BidirectGeoEllipsoidalType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoEllipsoidalType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 440, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}From4 uses Python identifier From4
    __From4 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'From4'), 'From4', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoEllipsoidalType_httpwww_interlis_chxtf2_4CoordSysFrom4', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 442, 4), )

    
    From4 = property(__From4.value, __From4.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}To4 uses Python identifier To4
    __To4 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'To4'), 'To4', '__httpwww_interlis_chxtf2_4CoordSys_BidirectGeoEllipsoidalType_httpwww_interlis_chxtf2_4CoordSysTo4', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 447, 4), )

    
    To4 = property(__To4.value, __To4.set, None, None)

    _ElementMap.update({
        __From4.name() : __From4,
        __To4.name() : __To4
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.BidirectGeoEllipsoidalType = BidirectGeoEllipsoidalType
Namespace.addCategoryObject('typeBinding', 'BidirectGeoEllipsoidalType', BidirectGeoEllipsoidalType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType with content type ELEMENT_ONLY
class MapProjectionType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MapProjectionType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 455, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}From5 uses Python identifier From5
    __From5 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'From5'), 'From5', '__httpwww_interlis_chxtf2_4CoordSys_MapProjectionType_httpwww_interlis_chxtf2_4CoordSysFrom5', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 457, 4), )

    
    From5 = property(__From5.value, __From5.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}To5 uses Python identifier To5
    __To5 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'To5'), 'To5', '__httpwww_interlis_chxtf2_4CoordSys_MapProjectionType_httpwww_interlis_chxtf2_4CoordSysTo5', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 462, 4), )

    
    To5 = property(__To5.value, __To5.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}FromCo1_FundPt uses Python identifier FromCo1_FundPt
    __FromCo1_FundPt = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FromCo1_FundPt'), 'FromCo1_FundPt', '__httpwww_interlis_chxtf2_4CoordSys_MapProjectionType_httpwww_interlis_chxtf2_4CoordSysFromCo1_FundPt', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 467, 4), )

    
    FromCo1_FundPt = property(__FromCo1_FundPt.value, __FromCo1_FundPt.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}FromCo2_FundPt uses Python identifier FromCo2_FundPt
    __FromCo2_FundPt = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FromCo2_FundPt'), 'FromCo2_FundPt', '__httpwww_interlis_chxtf2_4CoordSys_MapProjectionType_httpwww_interlis_chxtf2_4CoordSysFromCo2_FundPt', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 468, 4), )

    
    FromCo2_FundPt = property(__FromCo2_FundPt.value, __FromCo2_FundPt.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord1_FundPt uses Python identifier ToCoord1_FundPt
    __ToCoord1_FundPt = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ToCoord1_FundPt'), 'ToCoord1_FundPt', '__httpwww_interlis_chxtf2_4CoordSys_MapProjectionType_httpwww_interlis_chxtf2_4CoordSysToCoord1_FundPt', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 469, 4), )

    
    ToCoord1_FundPt = property(__ToCoord1_FundPt.value, __ToCoord1_FundPt.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord2_FundPt uses Python identifier ToCoord2_FundPt
    __ToCoord2_FundPt = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ToCoord2_FundPt'), 'ToCoord2_FundPt', '__httpwww_interlis_chxtf2_4CoordSys_MapProjectionType_httpwww_interlis_chxtf2_4CoordSysToCoord2_FundPt', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 477, 4), )

    
    ToCoord2_FundPt = property(__ToCoord2_FundPt.value, __ToCoord2_FundPt.set, None, None)

    _ElementMap.update({
        __From5.name() : __From5,
        __To5.name() : __To5,
        __FromCo1_FundPt.name() : __FromCo1_FundPt,
        __FromCo2_FundPt.name() : __FromCo2_FundPt,
        __ToCoord1_FundPt.name() : __ToCoord1_FundPt,
        __ToCoord2_FundPt.name() : __ToCoord2_FundPt
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MapProjectionType = MapProjectionType
Namespace.addCategoryObject('typeBinding', 'MapProjectionType', MapProjectionType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}HeightConversionType with content type ELEMENT_ONLY
class HeightConversionType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}HeightConversionType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'HeightConversionType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 571, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}FromHeight uses Python identifier FromHeight
    __FromHeight = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FromHeight'), 'FromHeight', '__httpwww_interlis_chxtf2_4CoordSys_HeightConversionType_httpwww_interlis_chxtf2_4CoordSysFromHeight', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 573, 4), )

    
    FromHeight = property(__FromHeight.value, __FromHeight.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}ToHeight uses Python identifier ToHeight
    __ToHeight = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ToHeight'), 'ToHeight', '__httpwww_interlis_chxtf2_4CoordSys_HeightConversionType_httpwww_interlis_chxtf2_4CoordSysToHeight', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 578, 4), )

    
    ToHeight = property(__ToHeight.value, __ToHeight.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}Definition uses Python identifier Definition
    __Definition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Definition'), 'Definition', '__httpwww_interlis_chxtf2_4CoordSys_HeightConversionType_httpwww_interlis_chxtf2_4CoordSysDefinition', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 583, 4), )

    
    Definition = property(__Definition.value, __Definition.set, None, None)

    _ElementMap.update({
        __FromHeight.name() : __FromHeight,
        __ToHeight.name() : __ToHeight,
        __Definition.name() : __Definition
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.HeightConversionType = HeightConversionType
Namespace.addCategoryObject('typeBinding', 'HeightConversionType', HeightConversionType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}LengthAXISType with content type ELEMENT_ONLY
class LengthAXISType (_ImportedBinding_camac_gis_export_so_schema_INTERLIS.AXISType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}LengthAXISType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LengthAXISType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 144, 0)
    _ElementMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.AXISType._ElementMap.copy()
    _AttributeMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.AXISType._AttributeMap.copy()
    # Base type is _ImportedBinding_camac_gis_export_so_schema_INTERLIS.AXISType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}ShortName uses Python identifier ShortName
    __ShortName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ShortName'), 'ShortName', '__httpwww_interlis_chxtf2_4CoordSys_LengthAXISType_httpwww_interlis_chxtf2_4CoordSysShortName', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 148, 8), )

    
    ShortName = property(__ShortName.value, __ShortName.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Description'), 'Description', '__httpwww_interlis_chxtf2_4CoordSys_LengthAXISType_httpwww_interlis_chxtf2_4CoordSysDescription', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 155, 8), )

    
    Description = property(__Description.value, __Description.set, None, None)

    _ElementMap.update({
        __ShortName.name() : __ShortName,
        __Description.name() : __Description
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.LengthAXISType = LengthAXISType
Namespace.addCategoryObject('typeBinding', 'LengthAXISType', LengthAXISType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}AngleAXISType with content type ELEMENT_ONLY
class AngleAXISType (_ImportedBinding_camac_gis_export_so_schema_INTERLIS.AXISType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}AngleAXISType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AngleAXISType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 167, 0)
    _ElementMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.AXISType._ElementMap.copy()
    _AttributeMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.AXISType._AttributeMap.copy()
    # Base type is _ImportedBinding_camac_gis_export_so_schema_INTERLIS.AXISType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}ShortName uses Python identifier ShortName
    __ShortName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ShortName'), 'ShortName', '__httpwww_interlis_chxtf2_4CoordSys_AngleAXISType_httpwww_interlis_chxtf2_4CoordSysShortName', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 171, 8), )

    
    ShortName = property(__ShortName.value, __ShortName.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Description'), 'Description', '__httpwww_interlis_chxtf2_4CoordSys_AngleAXISType_httpwww_interlis_chxtf2_4CoordSysDescription', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 178, 8), )

    
    Description = property(__Description.value, __Description.set, None, None)

    _ElementMap.update({
        __ShortName.name() : __ShortName,
        __Description.name() : __Description
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.AngleAXISType = AngleAXISType
Namespace.addCategoryObject('typeBinding', 'AngleAXISType', AngleAXISType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 225, 10)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}HeightEllips uses Python identifier HeightEllips
    __HeightEllips = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HeightEllips'), 'HeightEllips', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_httpwww_interlis_chxtf2_4CoordSysHeightEllips', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 252, 0), )

    
    HeightEllips = property(__HeightEllips.value, __HeightEllips.set, None, None)

    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 229, 12)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        __HeightEllips.name() : __HeightEllips
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 233, 10)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}HeightGeoid uses Python identifier HeightGeoid
    __HeightGeoid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HeightGeoid'), 'HeightGeoid', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON__httpwww_interlis_chxtf2_4CoordSysHeightGeoid', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 262, 0), )

    
    HeightGeoid = property(__HeightGeoid.value, __HeightGeoid.set, None, None)

    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON__httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 237, 12)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        __HeightGeoid.name() : __HeightGeoid
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 241, 10)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}HeightGravit uses Python identifier HeightGravit
    __HeightGravit = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HeightGravit'), 'HeightGravit', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_2_httpwww_interlis_chxtf2_4CoordSysHeightGravit', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 257, 0), )

    
    HeightGravit = property(__HeightGravit.value, __HeightGravit.set, None, None)

    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_2_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 245, 12)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        __HeightGravit.name() : __HeightGravit
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 312, 10)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}EllCSEllips uses Python identifier EllCSEllips
    __EllCSEllips = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EllCSEllips'), 'EllCSEllips', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_3_httpwww_interlis_chxtf2_4CoordSysEllCSEllips', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 323, 0), )

    
    EllCSEllips = property(__EllCSEllips.value, __EllCSEllips.set, None, None)

    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_3_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 316, 12)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        __EllCSEllips.name() : __EllCSEllips
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 332, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_4_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 333, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_4 = CTD_ANON_4


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 337, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_5_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 338, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_5 = CTD_ANON_5


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 342, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_6_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 343, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_6 = CTD_ANON_6


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 352, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_7_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 353, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_7 = CTD_ANON_7


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 357, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_8_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 358, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_8 = CTD_ANON_8


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 362, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_9_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 363, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_9 = CTD_ANON_9


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 372, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_10_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 373, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_10 = CTD_ANON_10


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 377, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_11_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 378, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_11 = CTD_ANON_11


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 387, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_12_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 388, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_12 = CTD_ANON_12


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 392, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_13_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 393, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_13 = CTD_ANON_13


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_14 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 443, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_14_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 444, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_14 = CTD_ANON_14


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_15 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 448, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_15_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 449, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_15 = CTD_ANON_15


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_16 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 458, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_16_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 459, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_16 = CTD_ANON_16


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_17 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 463, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_17_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 464, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_17 = CTD_ANON_17


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}TransverseMercatorType with content type ELEMENT_ONLY
class TransverseMercatorType (MapProjectionType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}TransverseMercatorType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TransverseMercatorType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 488, 0)
    _ElementMap = MapProjectionType._ElementMap.copy()
    _AttributeMap = MapProjectionType._AttributeMap.copy()
    # Base type is MapProjectionType
    
    # Element From5 ({http://www.interlis.ch/xtf/2.4/CoordSys}From5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element To5 ({http://www.interlis.ch/xtf/2.4/CoordSys}To5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.TransverseMercatorType = TransverseMercatorType
Namespace.addCategoryObject('typeBinding', 'TransverseMercatorType', TransverseMercatorType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}SwissProjectionType with content type ELEMENT_ONLY
class SwissProjectionType (MapProjectionType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}SwissProjectionType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SwissProjectionType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 497, 0)
    _ElementMap = MapProjectionType._ElementMap.copy()
    _AttributeMap = MapProjectionType._AttributeMap.copy()
    # Base type is MapProjectionType
    
    # Element From5 ({http://www.interlis.ch/xtf/2.4/CoordSys}From5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element To5 ({http://www.interlis.ch/xtf/2.4/CoordSys}To5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}IntermFundP1 uses Python identifier IntermFundP1
    __IntermFundP1 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IntermFundP1'), 'IntermFundP1', '__httpwww_interlis_chxtf2_4CoordSys_SwissProjectionType_httpwww_interlis_chxtf2_4CoordSysIntermFundP1', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 501, 8), )

    
    IntermFundP1 = property(__IntermFundP1.value, __IntermFundP1.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}IntermFundP2 uses Python identifier IntermFundP2
    __IntermFundP2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IntermFundP2'), 'IntermFundP2', '__httpwww_interlis_chxtf2_4CoordSys_SwissProjectionType_httpwww_interlis_chxtf2_4CoordSysIntermFundP2', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 502, 8), )

    
    IntermFundP2 = property(__IntermFundP2.value, __IntermFundP2.set, None, None)

    _ElementMap.update({
        __IntermFundP1.name() : __IntermFundP1,
        __IntermFundP2.name() : __IntermFundP2
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.SwissProjectionType = SwissProjectionType
Namespace.addCategoryObject('typeBinding', 'SwissProjectionType', SwissProjectionType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}MercatorType with content type ELEMENT_ONLY
class MercatorType (MapProjectionType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}MercatorType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MercatorType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 508, 0)
    _ElementMap = MapProjectionType._ElementMap.copy()
    _AttributeMap = MapProjectionType._AttributeMap.copy()
    # Base type is MapProjectionType
    
    # Element From5 ({http://www.interlis.ch/xtf/2.4/CoordSys}From5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element To5 ({http://www.interlis.ch/xtf/2.4/CoordSys}To5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MercatorType = MercatorType
Namespace.addCategoryObject('typeBinding', 'MercatorType', MercatorType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}ObliqueMercatorType with content type ELEMENT_ONLY
class ObliqueMercatorType (MapProjectionType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}ObliqueMercatorType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ObliqueMercatorType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 517, 0)
    _ElementMap = MapProjectionType._ElementMap.copy()
    _AttributeMap = MapProjectionType._AttributeMap.copy()
    # Base type is MapProjectionType
    
    # Element From5 ({http://www.interlis.ch/xtf/2.4/CoordSys}From5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element To5 ({http://www.interlis.ch/xtf/2.4/CoordSys}To5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ObliqueMercatorType = ObliqueMercatorType
Namespace.addCategoryObject('typeBinding', 'ObliqueMercatorType', ObliqueMercatorType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}LambertType with content type ELEMENT_ONLY
class LambertType (MapProjectionType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}LambertType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LambertType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 526, 0)
    _ElementMap = MapProjectionType._ElementMap.copy()
    _AttributeMap = MapProjectionType._AttributeMap.copy()
    # Base type is MapProjectionType
    
    # Element From5 ({http://www.interlis.ch/xtf/2.4/CoordSys}From5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element To5 ({http://www.interlis.ch/xtf/2.4/CoordSys}To5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.LambertType = LambertType
Namespace.addCategoryObject('typeBinding', 'LambertType', LambertType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}PolyconicType with content type ELEMENT_ONLY
class PolyconicType (MapProjectionType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}PolyconicType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PolyconicType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 535, 0)
    _ElementMap = MapProjectionType._ElementMap.copy()
    _AttributeMap = MapProjectionType._AttributeMap.copy()
    # Base type is MapProjectionType
    
    # Element From5 ({http://www.interlis.ch/xtf/2.4/CoordSys}From5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element To5 ({http://www.interlis.ch/xtf/2.4/CoordSys}To5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.PolyconicType = PolyconicType
Namespace.addCategoryObject('typeBinding', 'PolyconicType', PolyconicType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}AlbusType with content type ELEMENT_ONLY
class AlbusType (MapProjectionType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}AlbusType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AlbusType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 544, 0)
    _ElementMap = MapProjectionType._ElementMap.copy()
    _AttributeMap = MapProjectionType._AttributeMap.copy()
    # Base type is MapProjectionType
    
    # Element From5 ({http://www.interlis.ch/xtf/2.4/CoordSys}From5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element To5 ({http://www.interlis.ch/xtf/2.4/CoordSys}To5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.AlbusType = AlbusType
Namespace.addCategoryObject('typeBinding', 'AlbusType', AlbusType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}AzimutalType with content type ELEMENT_ONLY
class AzimutalType (MapProjectionType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}AzimutalType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AzimutalType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 553, 0)
    _ElementMap = MapProjectionType._ElementMap.copy()
    _AttributeMap = MapProjectionType._AttributeMap.copy()
    # Base type is MapProjectionType
    
    # Element From5 ({http://www.interlis.ch/xtf/2.4/CoordSys}From5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element To5 ({http://www.interlis.ch/xtf/2.4/CoordSys}To5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.AzimutalType = AzimutalType
Namespace.addCategoryObject('typeBinding', 'AzimutalType', AzimutalType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}StereographicType with content type ELEMENT_ONLY
class StereographicType (MapProjectionType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}StereographicType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'StereographicType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 562, 0)
    _ElementMap = MapProjectionType._ElementMap.copy()
    _AttributeMap = MapProjectionType._AttributeMap.copy()
    # Base type is MapProjectionType
    
    # Element From5 ({http://www.interlis.ch/xtf/2.4/CoordSys}From5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element To5 ({http://www.interlis.ch/xtf/2.4/CoordSys}To5) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element FromCo2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}FromCo2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord1_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord1_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    
    # Element ToCoord2_FundPt ({http://www.interlis.ch/xtf/2.4/CoordSys}ToCoord2_FundPt) inherited from {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjectionType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.StereographicType = StereographicType
Namespace.addCategoryObject('typeBinding', 'StereographicType', StereographicType)


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_18 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 574, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_18_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 575, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_18 = CTD_ANON_18


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_19 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 579, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'ref'), 'ref', '__httpwww_interlis_chxtf2_4CoordSys_CTD_ANON_19_httpwww_interlis_chxtf2_4INTERLISref', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 18, 2)
    __ref._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 580, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_19 = CTD_ANON_19


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}CoordsysTopicType with content type ELEMENT_ONLY
class CoordsysTopicType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}CoordsysTopicType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CoordsysTopicType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 593, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}ToGeoEllipsoidal uses Python identifier ToGeoEllipsoidal
    __ToGeoEllipsoidal = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ToGeoEllipsoidal'), 'ToGeoEllipsoidal', '__httpwww_interlis_chxtf2_4CoordSys_CoordsysTopicType_httpwww_interlis_chxtf2_4CoordSysToGeoEllipsoidal', True, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 328, 0), )

    
    ToGeoEllipsoidal = property(__ToGeoEllipsoidal.value, __ToGeoEllipsoidal.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}ToGeoCartesian3D uses Python identifier ToGeoCartesian3D
    __ToGeoCartesian3D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ToGeoCartesian3D'), 'ToGeoCartesian3D', '__httpwww_interlis_chxtf2_4CoordSys_CoordsysTopicType_httpwww_interlis_chxtf2_4CoordSysToGeoCartesian3D', True, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 348, 0), )

    
    ToGeoCartesian3D = property(__ToGeoCartesian3D.value, __ToGeoCartesian3D.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}BidirectGeoCartesian2D uses Python identifier BidirectGeoCartesian2D
    __BidirectGeoCartesian2D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoCartesian2D'), 'BidirectGeoCartesian2D', '__httpwww_interlis_chxtf2_4CoordSys_CoordsysTopicType_httpwww_interlis_chxtf2_4CoordSysBidirectGeoCartesian2D', True, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 368, 0), )

    
    BidirectGeoCartesian2D = property(__BidirectGeoCartesian2D.value, __BidirectGeoCartesian2D.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}BidirectGeoCartesian3D uses Python identifier BidirectGeoCartesian3D
    __BidirectGeoCartesian3D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoCartesian3D'), 'BidirectGeoCartesian3D', '__httpwww_interlis_chxtf2_4CoordSys_CoordsysTopicType_httpwww_interlis_chxtf2_4CoordSysBidirectGeoCartesian3D', True, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 383, 0), )

    
    BidirectGeoCartesian3D = property(__BidirectGeoCartesian3D.value, __BidirectGeoCartesian3D.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}BidirectGeoEllipsoidal uses Python identifier BidirectGeoEllipsoidal
    __BidirectGeoEllipsoidal = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoEllipsoidal'), 'BidirectGeoEllipsoidal', '__httpwww_interlis_chxtf2_4CoordSys_CoordsysTopicType_httpwww_interlis_chxtf2_4CoordSysBidirectGeoEllipsoidal', True, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 439, 0), )

    
    BidirectGeoEllipsoidal = property(__BidirectGeoEllipsoidal.value, __BidirectGeoEllipsoidal.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}MapProjection uses Python identifier MapProjection
    __MapProjection = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MapProjection'), 'MapProjection', '__httpwww_interlis_chxtf2_4CoordSys_CoordsysTopicType_httpwww_interlis_chxtf2_4CoordSysMapProjection', True, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 454, 0), )

    
    MapProjection = property(__MapProjection.value, __MapProjection.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}HeightConversion uses Python identifier HeightConversion
    __HeightConversion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HeightConversion'), 'HeightConversion', '__httpwww_interlis_chxtf2_4CoordSys_CoordsysTopicType_httpwww_interlis_chxtf2_4CoordSysHeightConversion', True, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 570, 0), )

    
    HeightConversion = property(__HeightConversion.value, __HeightConversion.set, None, None)

    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}bid uses Python identifier bid
    __bid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'bid'), 'bid', '__httpwww_interlis_chxtf2_4CoordSys_CoordsysTopicType_httpwww_interlis_chxtf2_4INTERLISbid', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.bidType, required=True)
    __bid._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 21, 2)
    __bid._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 603, 2)
    
    bid = property(__bid.value, __bid.set, None, None)

    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}consistency uses Python identifier consistency
    __consistency = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'consistency'), 'consistency', '__httpwww_interlis_chxtf2_4CoordSys_CoordsysTopicType_httpwww_interlis_chxtf2_4INTERLISconsistency', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.consistencyType)
    __consistency._DeclarationLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 22, 2)
    __consistency._UseLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 604, 2)
    
    consistency = property(__consistency.value, __consistency.set, None, None)

    _ElementMap.update({
        __ToGeoEllipsoidal.name() : __ToGeoEllipsoidal,
        __ToGeoCartesian3D.name() : __ToGeoCartesian3D,
        __BidirectGeoCartesian2D.name() : __BidirectGeoCartesian2D,
        __BidirectGeoCartesian3D.name() : __BidirectGeoCartesian3D,
        __BidirectGeoEllipsoidal.name() : __BidirectGeoEllipsoidal,
        __MapProjection.name() : __MapProjection,
        __HeightConversion.name() : __HeightConversion
    })
    _AttributeMap.update({
        __bid.name() : __bid,
        __consistency.name() : __consistency
    })
_module_typeBindings.CoordsysTopicType = CoordsysTopicType
Namespace.addCategoryObject('typeBinding', 'CoordsysTopicType', CoordsysTopicType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}EllipsoidType with content type ELEMENT_ONLY
class EllipsoidType (_ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEMType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}EllipsoidType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EllipsoidType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 59, 0)
    _ElementMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEMType._ElementMap.copy()
    _AttributeMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEMType._AttributeMap.copy()
    # Base type is _ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEMType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}EllipsoidAlias uses Python identifier EllipsoidAlias
    __EllipsoidAlias = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EllipsoidAlias'), 'EllipsoidAlias', '__httpwww_interlis_chxtf2_4CoordSys_EllipsoidType_httpwww_interlis_chxtf2_4CoordSysEllipsoidAlias', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 63, 8), )

    
    EllipsoidAlias = property(__EllipsoidAlias.value, __EllipsoidAlias.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}SemiMajorAxis uses Python identifier SemiMajorAxis
    __SemiMajorAxis = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SemiMajorAxis'), 'SemiMajorAxis', '__httpwww_interlis_chxtf2_4CoordSys_EllipsoidType_httpwww_interlis_chxtf2_4CoordSysSemiMajorAxis', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 70, 8), )

    
    SemiMajorAxis = property(__SemiMajorAxis.value, __SemiMajorAxis.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}InverseFlattening uses Python identifier InverseFlattening
    __InverseFlattening = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'InverseFlattening'), 'InverseFlattening', '__httpwww_interlis_chxtf2_4CoordSys_EllipsoidType_httpwww_interlis_chxtf2_4CoordSysInverseFlattening', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 78, 8), )

    
    InverseFlattening = property(__InverseFlattening.value, __InverseFlattening.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}Remarks uses Python identifier Remarks
    __Remarks = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Remarks'), 'Remarks', '__httpwww_interlis_chxtf2_4CoordSys_EllipsoidType_httpwww_interlis_chxtf2_4CoordSysRemarks', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 86, 8), )

    
    Remarks = property(__Remarks.value, __Remarks.set, None, None)

    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __EllipsoidAlias.name() : __EllipsoidAlias,
        __SemiMajorAxis.name() : __SemiMajorAxis,
        __InverseFlattening.name() : __InverseFlattening,
        __Remarks.name() : __Remarks
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.EllipsoidType = EllipsoidType
Namespace.addCategoryObject('typeBinding', 'EllipsoidType', EllipsoidType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GravityModelType with content type ELEMENT_ONLY
class GravityModelType (_ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEMType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GravityModelType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GravityModelType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 98, 0)
    _ElementMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEMType._ElementMap.copy()
    _AttributeMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEMType._AttributeMap.copy()
    # Base type is _ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEMType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}GravityModAlias uses Python identifier GravityModAlias
    __GravityModAlias = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'GravityModAlias'), 'GravityModAlias', '__httpwww_interlis_chxtf2_4CoordSys_GravityModelType_httpwww_interlis_chxtf2_4CoordSysGravityModAlias', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 102, 8), )

    
    GravityModAlias = property(__GravityModAlias.value, __GravityModAlias.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}Definition uses Python identifier Definition
    __Definition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Definition'), 'Definition', '__httpwww_interlis_chxtf2_4CoordSys_GravityModelType_httpwww_interlis_chxtf2_4CoordSysDefinition', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 109, 8), )

    
    Definition = property(__Definition.value, __Definition.set, None, None)

    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __GravityModAlias.name() : __GravityModAlias,
        __Definition.name() : __Definition
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.GravityModelType = GravityModelType
Namespace.addCategoryObject('typeBinding', 'GravityModelType', GravityModelType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GeoidModelType with content type ELEMENT_ONLY
class GeoidModelType (_ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEMType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GeoidModelType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GeoidModelType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 121, 0)
    _ElementMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEMType._ElementMap.copy()
    _AttributeMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEMType._AttributeMap.copy()
    # Base type is _ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEMType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}GeoidModAlias uses Python identifier GeoidModAlias
    __GeoidModAlias = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'GeoidModAlias'), 'GeoidModAlias', '__httpwww_interlis_chxtf2_4CoordSys_GeoidModelType_httpwww_interlis_chxtf2_4CoordSysGeoidModAlias', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 125, 8), )

    
    GeoidModAlias = property(__GeoidModAlias.value, __GeoidModAlias.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}Definition uses Python identifier Definition
    __Definition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Definition'), 'Definition', '__httpwww_interlis_chxtf2_4CoordSys_GeoidModelType_httpwww_interlis_chxtf2_4CoordSysDefinition', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 132, 8), )

    
    Definition = property(__Definition.value, __Definition.set, None, None)

    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __GeoidModAlias.name() : __GeoidModAlias,
        __Definition.name() : __Definition
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.GeoidModelType = GeoidModelType
Namespace.addCategoryObject('typeBinding', 'GeoidModelType', GeoidModelType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GeoCartesian1DType with content type ELEMENT_ONLY
class GeoCartesian1DType (_ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GeoCartesian1DType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GeoCartesian1DType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 190, 0)
    _ElementMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType._ElementMap.copy()
    _AttributeMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType._AttributeMap.copy()
    # Base type is _ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType
    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Axis ({http://www.interlis.ch/xtf/2.4/INTERLIS}Axis) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}COORDSYSTEMType
    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.GeoCartesian1DType = GeoCartesian1DType
Namespace.addCategoryObject('typeBinding', 'GeoCartesian1DType', GeoCartesian1DType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GeoCartesian2DType with content type ELEMENT_ONLY
class GeoCartesian2DType (_ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GeoCartesian2DType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GeoCartesian2DType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 268, 0)
    _ElementMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType._ElementMap.copy()
    _AttributeMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType._AttributeMap.copy()
    # Base type is _ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}Definition uses Python identifier Definition
    __Definition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Definition'), 'Definition', '__httpwww_interlis_chxtf2_4CoordSys_GeoCartesian2DType_httpwww_interlis_chxtf2_4CoordSysDefinition', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 272, 8), )

    
    Definition = property(__Definition.value, __Definition.set, None, None)

    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Axis ({http://www.interlis.ch/xtf/2.4/INTERLIS}Axis) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}COORDSYSTEMType
    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __Definition.name() : __Definition
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.GeoCartesian2DType = GeoCartesian2DType
Namespace.addCategoryObject('typeBinding', 'GeoCartesian2DType', GeoCartesian2DType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GeoCartesian3DType with content type ELEMENT_ONLY
class GeoCartesian3DType (_ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GeoCartesian3DType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GeoCartesian3DType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 284, 0)
    _ElementMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType._ElementMap.copy()
    _AttributeMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType._AttributeMap.copy()
    # Base type is _ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}Definition uses Python identifier Definition
    __Definition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Definition'), 'Definition', '__httpwww_interlis_chxtf2_4CoordSys_GeoCartesian3DType_httpwww_interlis_chxtf2_4CoordSysDefinition', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 288, 8), )

    
    Definition = property(__Definition.value, __Definition.set, None, None)

    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Axis ({http://www.interlis.ch/xtf/2.4/INTERLIS}Axis) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}COORDSYSTEMType
    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __Definition.name() : __Definition
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.GeoCartesian3DType = GeoCartesian3DType
Namespace.addCategoryObject('typeBinding', 'GeoCartesian3DType', GeoCartesian3DType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GeoEllipsoidalType with content type ELEMENT_ONLY
class GeoEllipsoidalType (_ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GeoEllipsoidalType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GeoEllipsoidalType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 300, 0)
    _ElementMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType._ElementMap.copy()
    _AttributeMap = _ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType._AttributeMap.copy()
    # Base type is _ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEMType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}Definition uses Python identifier Definition
    __Definition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Definition'), 'Definition', '__httpwww_interlis_chxtf2_4CoordSys_GeoEllipsoidalType_httpwww_interlis_chxtf2_4CoordSysDefinition', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 304, 8), )

    
    Definition = property(__Definition.value, __Definition.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}EllipsoidRef uses Python identifier EllipsoidRef
    __EllipsoidRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EllipsoidRef'), 'EllipsoidRef', '__httpwww_interlis_chxtf2_4CoordSys_GeoEllipsoidalType_httpwww_interlis_chxtf2_4CoordSysEllipsoidRef', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 311, 8), )

    
    EllipsoidRef = property(__EllipsoidRef.value, __EllipsoidRef.set, None, None)

    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Axis ({http://www.interlis.ch/xtf/2.4/INTERLIS}Axis) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}COORDSYSTEMType
    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __Definition.name() : __Definition,
        __EllipsoidRef.name() : __EllipsoidRef
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.GeoEllipsoidalType = GeoEllipsoidalType
Namespace.addCategoryObject('typeBinding', 'GeoEllipsoidalType', GeoEllipsoidalType)


# Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GeoHeightType with content type ELEMENT_ONLY
class GeoHeightType (GeoCartesian1DType):
    """Complex type {http://www.interlis.ch/xtf/2.4/CoordSys}GeoHeightType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GeoHeightType')
    _XSDLocation = pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 199, 0)
    _ElementMap = GeoCartesian1DType._ElementMap.copy()
    _AttributeMap = GeoCartesian1DType._AttributeMap.copy()
    # Base type is GeoCartesian1DType
    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}System uses Python identifier System
    __System = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'System'), 'System', '__httpwww_interlis_chxtf2_4CoordSys_GeoHeightType_httpwww_interlis_chxtf2_4CoordSysSystem', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 203, 8), )

    
    System = property(__System.value, __System.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}ReferenceHeight uses Python identifier ReferenceHeight
    __ReferenceHeight = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReferenceHeight'), 'ReferenceHeight', '__httpwww_interlis_chxtf2_4CoordSys_GeoHeightType_httpwww_interlis_chxtf2_4CoordSysReferenceHeight', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 209, 8), )

    
    ReferenceHeight = property(__ReferenceHeight.value, __ReferenceHeight.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}ReferenceHeightDescr uses Python identifier ReferenceHeightDescr
    __ReferenceHeightDescr = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReferenceHeightDescr'), 'ReferenceHeightDescr', '__httpwww_interlis_chxtf2_4CoordSys_GeoHeightType_httpwww_interlis_chxtf2_4CoordSysReferenceHeightDescr', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 217, 8), )

    
    ReferenceHeightDescr = property(__ReferenceHeightDescr.value, __ReferenceHeightDescr.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}EllipsoidRef uses Python identifier EllipsoidRef
    __EllipsoidRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EllipsoidRef'), 'EllipsoidRef', '__httpwww_interlis_chxtf2_4CoordSys_GeoHeightType_httpwww_interlis_chxtf2_4CoordSysEllipsoidRef', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 224, 8), )

    
    EllipsoidRef = property(__EllipsoidRef.value, __EllipsoidRef.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}GeoidRef uses Python identifier GeoidRef
    __GeoidRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'GeoidRef'), 'GeoidRef', '__httpwww_interlis_chxtf2_4CoordSys_GeoHeightType_httpwww_interlis_chxtf2_4CoordSysGeoidRef', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 232, 8), )

    
    GeoidRef = property(__GeoidRef.value, __GeoidRef.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/CoordSys}GravityRef uses Python identifier GravityRef
    __GravityRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'GravityRef'), 'GravityRef', '__httpwww_interlis_chxtf2_4CoordSys_GeoHeightType_httpwww_interlis_chxtf2_4CoordSysGravityRef', False, pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 240, 8), )

    
    GravityRef = property(__GravityRef.value, __GravityRef.set, None, None)

    
    # Element extensions ({http://www.interlis.ch/xtf/2.4/INTERLIS}extensions) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Name ({http://www.interlis.ch/xtf/2.4/INTERLIS}Name) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    
    # Element Axis ({http://www.interlis.ch/xtf/2.4/INTERLIS}Axis) inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}COORDSYSTEMType
    
    # Attribute tid inherited from {http://www.interlis.ch/xtf/2.4/INTERLIS}METAOBJECTType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __System.name() : __System,
        __ReferenceHeight.name() : __ReferenceHeight,
        __ReferenceHeightDescr.name() : __ReferenceHeightDescr,
        __EllipsoidRef.name() : __EllipsoidRef,
        __GeoidRef.name() : __GeoidRef,
        __GravityRef.name() : __GravityRef
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.GeoHeightType = GeoHeightType
Namespace.addCategoryObject('typeBinding', 'GeoHeightType', GeoHeightType)


Angle_DMS_S = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Angle_DMS_S'), Angle_DMS_SType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 19, 0))
Namespace.addCategoryObject('elementBinding', Angle_DMS_S.name().localName(), Angle_DMS_S)

HeightEllips = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HeightEllips'), HeightEllipsType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 252, 0))
Namespace.addCategoryObject('elementBinding', HeightEllips.name().localName(), HeightEllips)

HeightGravit = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HeightGravit'), HeightGravitType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 257, 0))
Namespace.addCategoryObject('elementBinding', HeightGravit.name().localName(), HeightGravit)

HeightGeoid = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HeightGeoid'), HeightGeoidType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 262, 0))
Namespace.addCategoryObject('elementBinding', HeightGeoid.name().localName(), HeightGeoid)

EllCSEllips = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EllCSEllips'), EllCSEllipsType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 323, 0))
Namespace.addCategoryObject('elementBinding', EllCSEllips.name().localName(), EllCSEllips)

ToGeoEllipsoidal = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToGeoEllipsoidal'), ToGeoEllipsoidalType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 328, 0))
Namespace.addCategoryObject('elementBinding', ToGeoEllipsoidal.name().localName(), ToGeoEllipsoidal)

ToGeoCartesian3D = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToGeoCartesian3D'), ToGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 348, 0))
Namespace.addCategoryObject('elementBinding', ToGeoCartesian3D.name().localName(), ToGeoCartesian3D)

BidirectGeoCartesian2D = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoCartesian2D'), BidirectGeoCartesian2DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 368, 0))
Namespace.addCategoryObject('elementBinding', BidirectGeoCartesian2D.name().localName(), BidirectGeoCartesian2D)

BidirectGeoCartesian3D = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoCartesian3D'), BidirectGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 383, 0))
Namespace.addCategoryObject('elementBinding', BidirectGeoCartesian3D.name().localName(), BidirectGeoCartesian3D)

BidirectGeoEllipsoidal = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoEllipsoidal'), BidirectGeoEllipsoidalType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 439, 0))
Namespace.addCategoryObject('elementBinding', BidirectGeoEllipsoidal.name().localName(), BidirectGeoEllipsoidal)

MapProjection = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MapProjection'), MapProjectionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 454, 0))
Namespace.addCategoryObject('elementBinding', MapProjection.name().localName(), MapProjection)

HeightConversion = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HeightConversion'), HeightConversionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 570, 0))
Namespace.addCategoryObject('elementBinding', HeightConversion.name().localName(), HeightConversion)

LengthAXIS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LengthAXIS'), LengthAXISType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 143, 0))
Namespace.addCategoryObject('elementBinding', LengthAXIS.name().localName(), LengthAXIS)

AngleAXIS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AngleAXIS'), AngleAXISType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 166, 0))
Namespace.addCategoryObject('elementBinding', AngleAXIS.name().localName(), AngleAXIS)

TransverseMercator = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransverseMercator'), TransverseMercatorType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 487, 0))
Namespace.addCategoryObject('elementBinding', TransverseMercator.name().localName(), TransverseMercator)

SwissProjection = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SwissProjection'), SwissProjectionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 496, 0))
Namespace.addCategoryObject('elementBinding', SwissProjection.name().localName(), SwissProjection)

Mercator = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Mercator'), MercatorType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 507, 0))
Namespace.addCategoryObject('elementBinding', Mercator.name().localName(), Mercator)

ObliqueMercator = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ObliqueMercator'), ObliqueMercatorType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 516, 0))
Namespace.addCategoryObject('elementBinding', ObliqueMercator.name().localName(), ObliqueMercator)

Lambert = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Lambert'), LambertType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 525, 0))
Namespace.addCategoryObject('elementBinding', Lambert.name().localName(), Lambert)

Polyconic = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Polyconic'), PolyconicType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 534, 0))
Namespace.addCategoryObject('elementBinding', Polyconic.name().localName(), Polyconic)

Albus = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Albus'), AlbusType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 543, 0))
Namespace.addCategoryObject('elementBinding', Albus.name().localName(), Albus)

Azimutal = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Azimutal'), AzimutalType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 552, 0))
Namespace.addCategoryObject('elementBinding', Azimutal.name().localName(), Azimutal)

Stereographic = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Stereographic'), StereographicType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 561, 0))
Namespace.addCategoryObject('elementBinding', Stereographic.name().localName(), Stereographic)

CoordsysTopic = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CoordsysTopic'), CoordsysTopicType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 592, 0))
Namespace.addCategoryObject('elementBinding', CoordsysTopic.name().localName(), CoordsysTopic)

Ellipsoid = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Ellipsoid'), EllipsoidType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 58, 0))
Namespace.addCategoryObject('elementBinding', Ellipsoid.name().localName(), Ellipsoid)

GravityModel = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GravityModel'), GravityModelType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 97, 0))
Namespace.addCategoryObject('elementBinding', GravityModel.name().localName(), GravityModel)

GeoidModel = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GeoidModel'), GeoidModelType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 120, 0))
Namespace.addCategoryObject('elementBinding', GeoidModel.name().localName(), GeoidModel)

GeoCartesian1D = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GeoCartesian1D'), GeoCartesian1DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 189, 0))
Namespace.addCategoryObject('elementBinding', GeoCartesian1D.name().localName(), GeoCartesian1D)

GeoCartesian2D = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GeoCartesian2D'), GeoCartesian2DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 267, 0))
Namespace.addCategoryObject('elementBinding', GeoCartesian2D.name().localName(), GeoCartesian2D)

GeoCartesian3D = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GeoCartesian3D'), GeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 283, 0))
Namespace.addCategoryObject('elementBinding', GeoCartesian3D.name().localName(), GeoCartesian3D)

GeoEllipsoidal = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GeoEllipsoidal'), GeoEllipsoidalType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 299, 0))
Namespace.addCategoryObject('elementBinding', GeoEllipsoidal.name().localName(), GeoEllipsoidal)

GeoHeight = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GeoHeight'), GeoHeightType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 198, 0))
Namespace.addCategoryObject('elementBinding', GeoHeight.name().localName(), GeoHeight)



Angle_DMS_SType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Degrees'), STD_ANON, scope=Angle_DMS_SType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 22, 4)))

Angle_DMS_SType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Minutes'), STD_ANON_, scope=Angle_DMS_SType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 30, 4)))

Angle_DMS_SType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Seconds'), STD_ANON_2, scope=Angle_DMS_SType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 38, 4)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 22, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 30, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 38, 4))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Angle_DMS_SType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Degrees')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 22, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Angle_DMS_SType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Minutes')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 30, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(Angle_DMS_SType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Seconds')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 38, 4))
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
Angle_DMS_SType._Automaton = _BuildAutomaton()




ToGeoEllipsoidalType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'From'), CTD_ANON_4, scope=ToGeoEllipsoidalType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 331, 4)))

ToGeoEllipsoidalType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'To'), CTD_ANON_5, scope=ToGeoEllipsoidalType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 336, 4)))

ToGeoEllipsoidalType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToHeight'), CTD_ANON_6, scope=ToGeoEllipsoidalType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 341, 4)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ToGeoEllipsoidalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 331, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ToGeoEllipsoidalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 336, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ToGeoEllipsoidalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToHeight')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 341, 4))
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
ToGeoEllipsoidalType._Automaton = _BuildAutomaton_()




ToGeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'From2'), CTD_ANON_7, scope=ToGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 351, 4)))

ToGeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FromHeight'), CTD_ANON_8, scope=ToGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 356, 4)))

ToGeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'To3'), CTD_ANON_9, scope=ToGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 361, 4)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ToGeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From2')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 351, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ToGeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromHeight')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 356, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ToGeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To3')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 361, 4))
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
ToGeoCartesian3DType._Automaton = _BuildAutomaton_2()




BidirectGeoCartesian2DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'From'), CTD_ANON_10, scope=BidirectGeoCartesian2DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 371, 4)))

BidirectGeoCartesian2DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'To'), CTD_ANON_11, scope=BidirectGeoCartesian2DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 376, 4)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BidirectGeoCartesian2DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 371, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BidirectGeoCartesian2DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 376, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
BidirectGeoCartesian2DType._Automaton = _BuildAutomaton_3()




BidirectGeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'From'), CTD_ANON_12, scope=BidirectGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 386, 4)))

BidirectGeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'To2'), CTD_ANON_13, scope=BidirectGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 391, 4)))

BidirectGeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Precision'), STD_ANON_21, scope=BidirectGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 396, 4)))

BidirectGeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ShiftAxis1'), STD_ANON_22, scope=BidirectGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 402, 4)))

BidirectGeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ShiftAxis2'), STD_ANON_23, scope=BidirectGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 410, 4)))

BidirectGeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ShiftAxis3'), STD_ANON_24, scope=BidirectGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 418, 4)))

BidirectGeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RotationAxis1'), Angle_DMS_90, scope=BidirectGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 426, 4)))

BidirectGeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RotationAxis2'), Angle_DMS_90, scope=BidirectGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 427, 4)))

BidirectGeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RotationAxis3'), Angle_DMS_90, scope=BidirectGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 428, 4)))

BidirectGeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NewScale'), STD_ANON_25, scope=BidirectGeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 429, 4)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 426, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 427, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 428, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 429, 4))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BidirectGeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 386, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BidirectGeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To2')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 391, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BidirectGeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Precision')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 396, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BidirectGeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ShiftAxis1')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 402, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BidirectGeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ShiftAxis2')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 410, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BidirectGeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ShiftAxis3')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 418, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(BidirectGeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RotationAxis1')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 426, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(BidirectGeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RotationAxis2')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 427, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(BidirectGeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RotationAxis3')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 428, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(BidirectGeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NewScale')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 429, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
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
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
BidirectGeoCartesian3DType._Automaton = _BuildAutomaton_4()




BidirectGeoEllipsoidalType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'From4'), CTD_ANON_14, scope=BidirectGeoEllipsoidalType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 442, 4)))

BidirectGeoEllipsoidalType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'To4'), CTD_ANON_15, scope=BidirectGeoEllipsoidalType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 447, 4)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BidirectGeoEllipsoidalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From4')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 442, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BidirectGeoEllipsoidalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To4')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 447, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
BidirectGeoEllipsoidalType._Automaton = _BuildAutomaton_5()




MapProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'From5'), CTD_ANON_16, scope=MapProjectionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 457, 4)))

MapProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'To5'), CTD_ANON_17, scope=MapProjectionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 462, 4)))

MapProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FromCo1_FundPt'), Angle_DMS_90, scope=MapProjectionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 467, 4)))

MapProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FromCo2_FundPt'), Angle_DMS_90, scope=MapProjectionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 468, 4)))

MapProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToCoord1_FundPt'), STD_ANON_26, scope=MapProjectionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 469, 4)))

MapProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToCoord2_FundPt'), STD_ANON_27, scope=MapProjectionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 477, 4)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MapProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 457, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MapProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 462, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MapProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 467, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MapProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 468, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MapProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 469, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MapProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 477, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MapProjectionType._Automaton = _BuildAutomaton_6()




HeightConversionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FromHeight'), CTD_ANON_18, scope=HeightConversionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 573, 4)))

HeightConversionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToHeight'), CTD_ANON_19, scope=HeightConversionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 578, 4)))

HeightConversionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Definition'), STD_ANON_28, scope=HeightConversionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 583, 4)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 583, 4))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(HeightConversionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromHeight')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 573, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(HeightConversionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToHeight')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 578, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(HeightConversionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Definition')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 583, 4))
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
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
HeightConversionType._Automaton = _BuildAutomaton_7()




LengthAXISType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ShortName'), STD_ANON_11, scope=LengthAXISType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 148, 8)))

LengthAXISType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Description'), STD_ANON_12, scope=LengthAXISType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 155, 8)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 148, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 155, 8))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(LengthAXISType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ShortName')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 148, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(LengthAXISType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Description')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 155, 8))
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
LengthAXISType._Automaton = _BuildAutomaton_8()




AngleAXISType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ShortName'), STD_ANON_13, scope=AngleAXISType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 171, 8)))

AngleAXISType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Description'), STD_ANON_14, scope=AngleAXISType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 178, 8)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 171, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 178, 8))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AngleAXISType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ShortName')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 171, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(AngleAXISType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Description')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 178, 8))
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
AngleAXISType._Automaton = _BuildAutomaton_9()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HeightEllips'), HeightEllipsType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 252, 0)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 227, 14))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HeightEllips')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 227, 14))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_10()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HeightGeoid'), HeightGeoidType, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 262, 0)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 235, 14))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HeightGeoid')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 235, 14))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_11()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HeightGravit'), HeightGravitType, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 257, 0)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 243, 14))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HeightGravit')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 243, 14))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_12()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EllCSEllips'), EllCSEllipsType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 323, 0)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 314, 14))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EllCSEllips')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 314, 14))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_13()




def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TransverseMercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 457, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TransverseMercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 462, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TransverseMercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 467, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TransverseMercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 468, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TransverseMercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 469, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TransverseMercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 477, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
TransverseMercatorType._Automaton = _BuildAutomaton_14()




SwissProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntermFundP1'), Angle_DMS_90, scope=SwissProjectionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 501, 8)))

SwissProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntermFundP2'), Angle_DMS_90, scope=SwissProjectionType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 502, 8)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SwissProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 457, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SwissProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 462, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SwissProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 467, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SwissProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 468, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SwissProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 469, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SwissProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 477, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SwissProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IntermFundP1')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 501, 8))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SwissProjectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IntermFundP2')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 502, 8))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
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
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SwissProjectionType._Automaton = _BuildAutomaton_15()




def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 457, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 462, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 467, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 468, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 469, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 477, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MercatorType._Automaton = _BuildAutomaton_16()




def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObliqueMercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 457, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObliqueMercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 462, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObliqueMercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 467, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObliqueMercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 468, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObliqueMercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 469, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ObliqueMercatorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 477, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ObliqueMercatorType._Automaton = _BuildAutomaton_17()




def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LambertType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 457, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LambertType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 462, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LambertType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 467, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LambertType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 468, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LambertType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 469, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(LambertType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 477, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
LambertType._Automaton = _BuildAutomaton_18()




def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(PolyconicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 457, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(PolyconicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 462, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(PolyconicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 467, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(PolyconicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 468, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(PolyconicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 469, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(PolyconicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 477, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
PolyconicType._Automaton = _BuildAutomaton_19()




def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AlbusType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 457, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AlbusType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 462, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AlbusType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 467, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AlbusType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 468, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AlbusType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 469, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AlbusType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 477, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AlbusType._Automaton = _BuildAutomaton_20()




def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AzimutalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 457, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AzimutalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 462, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AzimutalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 467, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AzimutalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 468, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AzimutalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 469, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AzimutalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 477, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AzimutalType._Automaton = _BuildAutomaton_21()




def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(StereographicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'From5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 457, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(StereographicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'To5')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 462, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(StereographicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 467, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(StereographicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FromCo2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 468, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(StereographicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord1_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 469, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(StereographicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToCoord2_FundPt')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 477, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
StereographicType._Automaton = _BuildAutomaton_22()




CoordsysTopicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToGeoEllipsoidal'), ToGeoEllipsoidalType, scope=CoordsysTopicType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 328, 0)))

CoordsysTopicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToGeoCartesian3D'), ToGeoCartesian3DType, scope=CoordsysTopicType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 348, 0)))

CoordsysTopicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoCartesian2D'), BidirectGeoCartesian2DType, scope=CoordsysTopicType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 368, 0)))

CoordsysTopicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoCartesian3D'), BidirectGeoCartesian3DType, scope=CoordsysTopicType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 383, 0)))

CoordsysTopicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoEllipsoidal'), BidirectGeoEllipsoidalType, scope=CoordsysTopicType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 439, 0)))

CoordsysTopicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MapProjection'), MapProjectionType, scope=CoordsysTopicType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 454, 0)))

CoordsysTopicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HeightConversion'), HeightConversionType, scope=CoordsysTopicType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 570, 0)))

def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 594, 2))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CoordsysTopicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToGeoEllipsoidal')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 595, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CoordsysTopicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToGeoCartesian3D')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 596, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CoordsysTopicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoCartesian2D')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 597, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CoordsysTopicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoCartesian3D')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 598, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CoordsysTopicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BidirectGeoEllipsoidal')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 599, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CoordsysTopicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MapProjection')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 600, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CoordsysTopicType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HeightConversion')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 601, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CoordsysTopicType._Automaton = _BuildAutomaton_23()




EllipsoidType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EllipsoidAlias'), STD_ANON_3, scope=EllipsoidType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 63, 8)))

EllipsoidType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SemiMajorAxis'), STD_ANON_4, scope=EllipsoidType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 70, 8)))

EllipsoidType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'InverseFlattening'), STD_ANON_5, scope=EllipsoidType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 78, 8)))

EllipsoidType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Remarks'), STD_ANON_6, scope=EllipsoidType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 86, 8)))

def _BuildAutomaton_24 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 63, 8))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 86, 8))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(EllipsoidType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(EllipsoidType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(EllipsoidType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EllipsoidAlias')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 63, 8))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(EllipsoidType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SemiMajorAxis')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 70, 8))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(EllipsoidType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'InverseFlattening')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 78, 8))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(EllipsoidType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Remarks')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 86, 8))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
EllipsoidType._Automaton = _BuildAutomaton_24()




GravityModelType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GravityModAlias'), STD_ANON_7, scope=GravityModelType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 102, 8)))

GravityModelType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Definition'), STD_ANON_8, scope=GravityModelType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 109, 8)))

def _BuildAutomaton_25 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 102, 8))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 109, 8))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GravityModelType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(GravityModelType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(GravityModelType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'GravityModAlias')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 102, 8))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(GravityModelType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Definition')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 109, 8))
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
GravityModelType._Automaton = _BuildAutomaton_25()




GeoidModelType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GeoidModAlias'), STD_ANON_9, scope=GeoidModelType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 125, 8)))

GeoidModelType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Definition'), STD_ANON_10, scope=GeoidModelType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 132, 8)))

def _BuildAutomaton_26 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_26
    del _BuildAutomaton_26
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 125, 8))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 132, 8))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoidModelType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(GeoidModelType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(GeoidModelType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'GeoidModAlias')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 125, 8))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(GeoidModelType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Definition')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 132, 8))
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
GeoidModelType._Automaton = _BuildAutomaton_26()




def _BuildAutomaton_27 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_27
    del _BuildAutomaton_27
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=1, max=3, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoCartesian1DType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoCartesian1DType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(GeoCartesian1DType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'Axis')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10))
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
GeoCartesian1DType._Automaton = _BuildAutomaton_27()




GeoCartesian2DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Definition'), STD_ANON_18, scope=GeoCartesian2DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 272, 8)))

def _BuildAutomaton_28 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_28
    del _BuildAutomaton_28
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=1, max=3, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 272, 8))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoCartesian2DType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoCartesian2DType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(GeoCartesian2DType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'Axis')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(GeoCartesian2DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Definition')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 272, 8))
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
GeoCartesian2DType._Automaton = _BuildAutomaton_28()




GeoCartesian3DType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Definition'), STD_ANON_19, scope=GeoCartesian3DType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 288, 8)))

def _BuildAutomaton_29 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_29
    del _BuildAutomaton_29
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=1, max=3, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 288, 8))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(GeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'Axis')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(GeoCartesian3DType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Definition')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 288, 8))
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
GeoCartesian3DType._Automaton = _BuildAutomaton_29()




GeoEllipsoidalType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Definition'), STD_ANON_20, scope=GeoEllipsoidalType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 304, 8)))

GeoEllipsoidalType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EllipsoidRef'), CTD_ANON_3, scope=GeoEllipsoidalType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 311, 8)))

def _BuildAutomaton_30 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_30
    del _BuildAutomaton_30
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=1, max=3, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 304, 8))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoEllipsoidalType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoEllipsoidalType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoEllipsoidalType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'Axis')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoEllipsoidalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Definition')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 304, 8))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(GeoEllipsoidalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EllipsoidRef')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 311, 8))
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
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
GeoEllipsoidalType._Automaton = _BuildAutomaton_30()




GeoHeightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'System'), STD_ANON_15, scope=GeoHeightType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 203, 8)))

GeoHeightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReferenceHeight'), STD_ANON_16, scope=GeoHeightType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 209, 8)))

GeoHeightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReferenceHeightDescr'), STD_ANON_17, scope=GeoHeightType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 217, 8)))

GeoHeightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EllipsoidRef'), CTD_ANON, scope=GeoHeightType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 224, 8)))

GeoHeightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GeoidRef'), CTD_ANON_, scope=GeoHeightType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 232, 8)))

GeoHeightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GravityRef'), CTD_ANON_2, scope=GeoHeightType, location=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 240, 8)))

def _BuildAutomaton_31 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_31
    del _BuildAutomaton_31
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=1, max=3, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 217, 8))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoHeightType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'extensions')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 137, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoHeightType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'Name')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 138, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoHeightType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'Axis')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 191, 10))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoHeightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'System')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 203, 8))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoHeightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReferenceHeight')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 209, 8))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoHeightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReferenceHeightDescr')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 217, 8))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoHeightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EllipsoidRef')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 224, 8))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeoHeightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'GeoidRef')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 232, 8))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(GeoHeightType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'GravityRef')), pyxb.utils.utility.Location('/app/camac/gis_export/so_schema/xsd/CoordSys.xsd', 240, 8))
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
    transitions.append(fac.Transition(st_7, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
GeoHeightType._Automaton = _BuildAutomaton_31()


LengthAXIS._setSubstitutionGroup(_ImportedBinding_camac_gis_export_so_schema_INTERLIS.AXIS)

AngleAXIS._setSubstitutionGroup(_ImportedBinding_camac_gis_export_so_schema_INTERLIS.AXIS)

TransverseMercator._setSubstitutionGroup(MapProjection)

SwissProjection._setSubstitutionGroup(MapProjection)

Mercator._setSubstitutionGroup(MapProjection)

ObliqueMercator._setSubstitutionGroup(MapProjection)

Lambert._setSubstitutionGroup(MapProjection)

Polyconic._setSubstitutionGroup(MapProjection)

Albus._setSubstitutionGroup(MapProjection)

Azimutal._setSubstitutionGroup(MapProjection)

Stereographic._setSubstitutionGroup(MapProjection)

Ellipsoid._setSubstitutionGroup(_ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEM)

GravityModel._setSubstitutionGroup(_ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEM)

GeoidModel._setSubstitutionGroup(_ImportedBinding_camac_gis_export_so_schema_INTERLIS.REFSYSTEM)

GeoCartesian1D._setSubstitutionGroup(_ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEM)

GeoCartesian2D._setSubstitutionGroup(_ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEM)

GeoCartesian3D._setSubstitutionGroup(_ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEM)

GeoEllipsoidal._setSubstitutionGroup(_ImportedBinding_camac_gis_export_so_schema_INTERLIS.COORDSYSTEM)

GeoHeight._setSubstitutionGroup(GeoCartesian1D)
