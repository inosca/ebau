# ../../../camac/gis_export/so_schema/GeometryCHLV95_V2.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:2182de60ee9ca86f75f5a00d2f0d3274f8dea653
# Generated 2026-08-18 17:22:41.115335 by PyXB version 1.2.6 using Python 3.13.3.final.0
# Namespace http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2 [xmlns:GeometryCHLV95_V2]

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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:664cf9e7-5e6f-473a-b35a-8fac28b73864')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import camac.gis_export.so_schema.geometry as _ImportedBinding_camac_gis_export_so_schema_geometry
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2', create_if_missing=True)
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


# Atomic simple type: {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}Orientation
class Orientation (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Orientation')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 135, 0)
    _Documentation = None
Orientation._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.decimal('359.99999'), value_datatype=Orientation)
Orientation._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.decimal('0.0'), value_datatype=Orientation)
Orientation._InitializeFacetMap(Orientation._CF_maxInclusive,
   Orientation._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'Orientation', Orientation)
_module_typeBindings.Orientation = Orientation

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}Accuracy
class Accuracy (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Accuracy')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 141, 0)
    _Documentation = None
Accuracy._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'Accuracy', Accuracy)
_module_typeBindings.Accuracy = Accuracy

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}Method
class Method (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Method')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 145, 0)
    _Documentation = None
Method._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'Method', Method)
_module_typeBindings.Method = Method

# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}Coord2 with content type ELEMENT_ONLY
class Coord2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}Coord2 with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Coord2')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 25, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}coord uses Python identifier coord
    __coord = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'coord'), 'coord', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_Coord2_httpwww_interlis_chgeometry1_0coord', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 28, 2), )

    
    coord = property(__coord.value, __coord.set, None, None)

    _ElementMap.update({
        __coord.name() : __coord
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Coord2 = Coord2
Namespace.addCategoryObject('typeBinding', 'Coord2', Coord2)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}Coord3 with content type ELEMENT_ONLY
class Coord3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}Coord3 with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Coord3')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 30, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}coord uses Python identifier coord
    __coord = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'coord'), 'coord', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_Coord3_httpwww_interlis_chgeometry1_0coord', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 28, 2), )

    
    coord = property(__coord.value, __coord.set, None, None)

    _ElementMap.update({
        __coord.name() : __coord
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Coord3 = Coord3
Namespace.addCategoryObject('typeBinding', 'Coord3', Coord3)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiPoint with content type ELEMENT_ONLY
class MultiPoint (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiPoint with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MultiPoint')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 35, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}multicoord uses Python identifier multicoord
    __multicoord = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'multicoord'), 'multicoord', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_MultiPoint_httpwww_interlis_chgeometry1_0multicoord', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 41, 2), )

    
    multicoord = property(__multicoord.value, __multicoord.set, None, None)

    _ElementMap.update({
        __multicoord.name() : __multicoord
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MultiPoint = MultiPoint
Namespace.addCategoryObject('typeBinding', 'MultiPoint', MultiPoint)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiPoint3D with content type ELEMENT_ONLY
class MultiPoint3D (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiPoint3D with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MultiPoint3D')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 40, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}multicoord uses Python identifier multicoord
    __multicoord = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'multicoord'), 'multicoord', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_MultiPoint3D_httpwww_interlis_chgeometry1_0multicoord', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 41, 2), )

    
    multicoord = property(__multicoord.value, __multicoord.set, None, None)

    _ElementMap.update({
        __multicoord.name() : __multicoord
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MultiPoint3D = MultiPoint3D
Namespace.addCategoryObject('typeBinding', 'MultiPoint3D', MultiPoint3D)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}Surface with content type ELEMENT_ONLY
class Surface (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}Surface with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Surface')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 45, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}surface uses Python identifier surface
    __surface = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'surface'), 'surface', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_Surface_httpwww_interlis_chgeometry1_0surface', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 116, 2), )

    
    surface = property(__surface.value, __surface.set, None, None)

    _ElementMap.update({
        __surface.name() : __surface
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Surface = Surface
Namespace.addCategoryObject('typeBinding', 'Surface', Surface)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}Area with content type ELEMENT_ONLY
class Area (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}Area with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Area')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 50, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}surface uses Python identifier surface
    __surface = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'surface'), 'surface', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_Area_httpwww_interlis_chgeometry1_0surface', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 116, 2), )

    
    surface = property(__surface.value, __surface.set, None, None)

    _ElementMap.update({
        __surface.name() : __surface
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Area = Area
Namespace.addCategoryObject('typeBinding', 'Area', Area)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}Line with content type ELEMENT_ONLY
class Line (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}Line with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Line')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 55, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}polyline uses Python identifier polyline
    __polyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), 'polyline', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_Line_httpwww_interlis_chgeometry1_0polyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2), )

    
    polyline = property(__polyline.value, __polyline.set, None, None)

    _ElementMap.update({
        __polyline.name() : __polyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Line = Line
Namespace.addCategoryObject('typeBinding', 'Line', Line)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}DirectedLine with content type ELEMENT_ONLY
class DirectedLine (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}DirectedLine with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DirectedLine')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 60, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}polyline uses Python identifier polyline
    __polyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), 'polyline', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_DirectedLine_httpwww_interlis_chgeometry1_0polyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2), )

    
    polyline = property(__polyline.value, __polyline.set, None, None)

    _ElementMap.update({
        __polyline.name() : __polyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.DirectedLine = DirectedLine
Namespace.addCategoryObject('typeBinding', 'DirectedLine', DirectedLine)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}LineWithAltitude with content type ELEMENT_ONLY
class LineWithAltitude (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}LineWithAltitude with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LineWithAltitude')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 65, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}polyline uses Python identifier polyline
    __polyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), 'polyline', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_LineWithAltitude_httpwww_interlis_chgeometry1_0polyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2), )

    
    polyline = property(__polyline.value, __polyline.set, None, None)

    _ElementMap.update({
        __polyline.name() : __polyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.LineWithAltitude = LineWithAltitude
Namespace.addCategoryObject('typeBinding', 'LineWithAltitude', LineWithAltitude)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}DirectedLineWithAltitude with content type ELEMENT_ONLY
class DirectedLineWithAltitude (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}DirectedLineWithAltitude with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DirectedLineWithAltitude')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 70, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}polyline uses Python identifier polyline
    __polyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), 'polyline', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_DirectedLineWithAltitude_httpwww_interlis_chgeometry1_0polyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2), )

    
    polyline = property(__polyline.value, __polyline.set, None, None)

    _ElementMap.update({
        __polyline.name() : __polyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.DirectedLineWithAltitude = DirectedLineWithAltitude
Namespace.addCategoryObject('typeBinding', 'DirectedLineWithAltitude', DirectedLineWithAltitude)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiLine with content type ELEMENT_ONLY
class MultiLine (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiLine with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MultiLine')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 75, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}multipolyline uses Python identifier multipolyline
    __multipolyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'multipolyline'), 'multipolyline', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_MultiLine_httpwww_interlis_chgeometry1_0multipolyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 103, 2), )

    
    multipolyline = property(__multipolyline.value, __multipolyline.set, None, None)

    _ElementMap.update({
        __multipolyline.name() : __multipolyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MultiLine = MultiLine
Namespace.addCategoryObject('typeBinding', 'MultiLine', MultiLine)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiDirectedLine with content type ELEMENT_ONLY
class MultiDirectedLine (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiDirectedLine with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MultiDirectedLine')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 80, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}multipolyline uses Python identifier multipolyline
    __multipolyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'multipolyline'), 'multipolyline', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_MultiDirectedLine_httpwww_interlis_chgeometry1_0multipolyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 103, 2), )

    
    multipolyline = property(__multipolyline.value, __multipolyline.set, None, None)

    _ElementMap.update({
        __multipolyline.name() : __multipolyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MultiDirectedLine = MultiDirectedLine
Namespace.addCategoryObject('typeBinding', 'MultiDirectedLine', MultiDirectedLine)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiSurface with content type ELEMENT_ONLY
class MultiSurface (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiSurface with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MultiSurface')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 85, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}multisurface uses Python identifier multisurface
    __multisurface = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'multisurface'), 'multisurface', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_MultiSurface_httpwww_interlis_chgeometry1_0multisurface', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 128, 2), )

    
    multisurface = property(__multisurface.value, __multisurface.set, None, None)

    _ElementMap.update({
        __multisurface.name() : __multisurface
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MultiSurface = MultiSurface
Namespace.addCategoryObject('typeBinding', 'MultiSurface', MultiSurface)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}SurfaceWithoutArcs with content type ELEMENT_ONLY
class SurfaceWithoutArcs (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}SurfaceWithoutArcs with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SurfaceWithoutArcs')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 90, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}surface uses Python identifier surface
    __surface = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'surface'), 'surface', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_SurfaceWithoutArcs_httpwww_interlis_chgeometry1_0surface', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 116, 2), )

    
    surface = property(__surface.value, __surface.set, None, None)

    _ElementMap.update({
        __surface.name() : __surface
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.SurfaceWithoutArcs = SurfaceWithoutArcs
Namespace.addCategoryObject('typeBinding', 'SurfaceWithoutArcs', SurfaceWithoutArcs)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}AreaWithoutArcs with content type ELEMENT_ONLY
class AreaWithoutArcs (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}AreaWithoutArcs with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AreaWithoutArcs')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 95, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}surface uses Python identifier surface
    __surface = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'surface'), 'surface', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_AreaWithoutArcs_httpwww_interlis_chgeometry1_0surface', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 116, 2), )

    
    surface = property(__surface.value, __surface.set, None, None)

    _ElementMap.update({
        __surface.name() : __surface
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.AreaWithoutArcs = AreaWithoutArcs
Namespace.addCategoryObject('typeBinding', 'AreaWithoutArcs', AreaWithoutArcs)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}LineWithoutArcs with content type ELEMENT_ONLY
class LineWithoutArcs (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}LineWithoutArcs with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LineWithoutArcs')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 100, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}polyline uses Python identifier polyline
    __polyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), 'polyline', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_LineWithoutArcs_httpwww_interlis_chgeometry1_0polyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2), )

    
    polyline = property(__polyline.value, __polyline.set, None, None)

    _ElementMap.update({
        __polyline.name() : __polyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.LineWithoutArcs = LineWithoutArcs
Namespace.addCategoryObject('typeBinding', 'LineWithoutArcs', LineWithoutArcs)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}DirectedLineWithoutArcs with content type ELEMENT_ONLY
class DirectedLineWithoutArcs (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}DirectedLineWithoutArcs with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DirectedLineWithoutArcs')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 105, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}polyline uses Python identifier polyline
    __polyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), 'polyline', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_DirectedLineWithoutArcs_httpwww_interlis_chgeometry1_0polyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2), )

    
    polyline = property(__polyline.value, __polyline.set, None, None)

    _ElementMap.update({
        __polyline.name() : __polyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.DirectedLineWithoutArcs = DirectedLineWithoutArcs
Namespace.addCategoryObject('typeBinding', 'DirectedLineWithoutArcs', DirectedLineWithoutArcs)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}LineWithAltitudeWithoutArcs with content type ELEMENT_ONLY
class LineWithAltitudeWithoutArcs (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}LineWithAltitudeWithoutArcs with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LineWithAltitudeWithoutArcs')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 110, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}polyline uses Python identifier polyline
    __polyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), 'polyline', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_LineWithAltitudeWithoutArcs_httpwww_interlis_chgeometry1_0polyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2), )

    
    polyline = property(__polyline.value, __polyline.set, None, None)

    _ElementMap.update({
        __polyline.name() : __polyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.LineWithAltitudeWithoutArcs = LineWithAltitudeWithoutArcs
Namespace.addCategoryObject('typeBinding', 'LineWithAltitudeWithoutArcs', LineWithAltitudeWithoutArcs)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}DirectedLineWithAltitudeWithoutArcs with content type ELEMENT_ONLY
class DirectedLineWithAltitudeWithoutArcs (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}DirectedLineWithAltitudeWithoutArcs with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DirectedLineWithAltitudeWithoutArcs')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 115, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}polyline uses Python identifier polyline
    __polyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), 'polyline', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_DirectedLineWithAltitudeWithoutArcs_httpwww_interlis_chgeometry1_0polyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2), )

    
    polyline = property(__polyline.value, __polyline.set, None, None)

    _ElementMap.update({
        __polyline.name() : __polyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.DirectedLineWithAltitudeWithoutArcs = DirectedLineWithAltitudeWithoutArcs
Namespace.addCategoryObject('typeBinding', 'DirectedLineWithAltitudeWithoutArcs', DirectedLineWithAltitudeWithoutArcs)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiLineWithoutArcs with content type ELEMENT_ONLY
class MultiLineWithoutArcs (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiLineWithoutArcs with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MultiLineWithoutArcs')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 120, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}multipolyline uses Python identifier multipolyline
    __multipolyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'multipolyline'), 'multipolyline', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_MultiLineWithoutArcs_httpwww_interlis_chgeometry1_0multipolyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 103, 2), )

    
    multipolyline = property(__multipolyline.value, __multipolyline.set, None, None)

    _ElementMap.update({
        __multipolyline.name() : __multipolyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MultiLineWithoutArcs = MultiLineWithoutArcs
Namespace.addCategoryObject('typeBinding', 'MultiLineWithoutArcs', MultiLineWithoutArcs)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiDirectedLineWithoutArcs with content type ELEMENT_ONLY
class MultiDirectedLineWithoutArcs (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiDirectedLineWithoutArcs with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MultiDirectedLineWithoutArcs')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 125, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}multipolyline uses Python identifier multipolyline
    __multipolyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'multipolyline'), 'multipolyline', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_MultiDirectedLineWithoutArcs_httpwww_interlis_chgeometry1_0multipolyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 103, 2), )

    
    multipolyline = property(__multipolyline.value, __multipolyline.set, None, None)

    _ElementMap.update({
        __multipolyline.name() : __multipolyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MultiDirectedLineWithoutArcs = MultiDirectedLineWithoutArcs
Namespace.addCategoryObject('typeBinding', 'MultiDirectedLineWithoutArcs', MultiDirectedLineWithoutArcs)


# Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiSurfaceWithoutArcs with content type ELEMENT_ONLY
class MultiSurfaceWithoutArcs (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/GeometryCHLV95_V2}MultiSurfaceWithoutArcs with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MultiSurfaceWithoutArcs')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 130, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}multisurface uses Python identifier multisurface
    __multisurface = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_geom, 'multisurface'), 'multisurface', '__httpwww_interlis_chxtf2_4GeometryCHLV95_V2_MultiSurfaceWithoutArcs_httpwww_interlis_chgeometry1_0multisurface', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 128, 2), )

    
    multisurface = property(__multisurface.value, __multisurface.set, None, None)

    _ElementMap.update({
        __multisurface.name() : __multisurface
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MultiSurfaceWithoutArcs = MultiSurfaceWithoutArcs
Namespace.addCategoryObject('typeBinding', 'MultiSurfaceWithoutArcs', MultiSurfaceWithoutArcs)




Coord2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'coord'), _ImportedBinding_camac_gis_export_so_schema_geometry.CoordType, scope=Coord2, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 28, 2)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Coord2._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'coord')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 27, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Coord2._Automaton = _BuildAutomaton()




Coord3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'coord'), _ImportedBinding_camac_gis_export_so_schema_geometry.CoordType, scope=Coord3, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 28, 2)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Coord3._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'coord')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 32, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Coord3._Automaton = _BuildAutomaton_()




MultiPoint._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'multicoord'), _ImportedBinding_camac_gis_export_so_schema_geometry.MultiCoordType, scope=MultiPoint, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 41, 2)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MultiPoint._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'multicoord')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 37, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MultiPoint._Automaton = _BuildAutomaton_2()




MultiPoint3D._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'multicoord'), _ImportedBinding_camac_gis_export_so_schema_geometry.MultiCoordType, scope=MultiPoint3D, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 41, 2)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MultiPoint3D._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'multicoord')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 42, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MultiPoint3D._Automaton = _BuildAutomaton_3()




Surface._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'surface'), _ImportedBinding_camac_gis_export_so_schema_geometry.SurfaceType, scope=Surface, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 116, 2)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Surface._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'surface')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 47, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Surface._Automaton = _BuildAutomaton_4()




Area._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'surface'), _ImportedBinding_camac_gis_export_so_schema_geometry.SurfaceType, scope=Area, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 116, 2)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Area._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'surface')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 52, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Area._Automaton = _BuildAutomaton_5()




Line._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), _ImportedBinding_camac_gis_export_so_schema_geometry.PolylineType, scope=Line, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Line._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 57, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Line._Automaton = _BuildAutomaton_6()




DirectedLine._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), _ImportedBinding_camac_gis_export_so_schema_geometry.PolylineType, scope=DirectedLine, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DirectedLine._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 62, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DirectedLine._Automaton = _BuildAutomaton_7()




LineWithAltitude._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), _ImportedBinding_camac_gis_export_so_schema_geometry.PolylineType, scope=LineWithAltitude, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(LineWithAltitude._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 67, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
LineWithAltitude._Automaton = _BuildAutomaton_8()




DirectedLineWithAltitude._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), _ImportedBinding_camac_gis_export_so_schema_geometry.PolylineType, scope=DirectedLineWithAltitude, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DirectedLineWithAltitude._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 72, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DirectedLineWithAltitude._Automaton = _BuildAutomaton_9()




MultiLine._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'multipolyline'), _ImportedBinding_camac_gis_export_so_schema_geometry.MultiPolylineType, scope=MultiLine, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 103, 2)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MultiLine._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'multipolyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 77, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MultiLine._Automaton = _BuildAutomaton_10()




MultiDirectedLine._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'multipolyline'), _ImportedBinding_camac_gis_export_so_schema_geometry.MultiPolylineType, scope=MultiDirectedLine, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 103, 2)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MultiDirectedLine._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'multipolyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 82, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MultiDirectedLine._Automaton = _BuildAutomaton_11()




MultiSurface._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'multisurface'), _ImportedBinding_camac_gis_export_so_schema_geometry.MultiSurfaceType, scope=MultiSurface, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 128, 2)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MultiSurface._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'multisurface')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 87, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MultiSurface._Automaton = _BuildAutomaton_12()




SurfaceWithoutArcs._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'surface'), _ImportedBinding_camac_gis_export_so_schema_geometry.SurfaceType, scope=SurfaceWithoutArcs, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 116, 2)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SurfaceWithoutArcs._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'surface')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 92, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SurfaceWithoutArcs._Automaton = _BuildAutomaton_13()




AreaWithoutArcs._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'surface'), _ImportedBinding_camac_gis_export_so_schema_geometry.SurfaceType, scope=AreaWithoutArcs, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 116, 2)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AreaWithoutArcs._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'surface')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 97, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AreaWithoutArcs._Automaton = _BuildAutomaton_14()




LineWithoutArcs._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), _ImportedBinding_camac_gis_export_so_schema_geometry.PolylineType, scope=LineWithoutArcs, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(LineWithoutArcs._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 102, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
LineWithoutArcs._Automaton = _BuildAutomaton_15()




DirectedLineWithoutArcs._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), _ImportedBinding_camac_gis_export_so_schema_geometry.PolylineType, scope=DirectedLineWithoutArcs, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DirectedLineWithoutArcs._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 107, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DirectedLineWithoutArcs._Automaton = _BuildAutomaton_16()




LineWithAltitudeWithoutArcs._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), _ImportedBinding_camac_gis_export_so_schema_geometry.PolylineType, scope=LineWithAltitudeWithoutArcs, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(LineWithAltitudeWithoutArcs._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 112, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
LineWithAltitudeWithoutArcs._Automaton = _BuildAutomaton_17()




DirectedLineWithAltitudeWithoutArcs._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline'), _ImportedBinding_camac_gis_export_so_schema_geometry.PolylineType, scope=DirectedLineWithAltitudeWithoutArcs, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DirectedLineWithAltitudeWithoutArcs._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'polyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 117, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DirectedLineWithAltitudeWithoutArcs._Automaton = _BuildAutomaton_18()




MultiLineWithoutArcs._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'multipolyline'), _ImportedBinding_camac_gis_export_so_schema_geometry.MultiPolylineType, scope=MultiLineWithoutArcs, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 103, 2)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MultiLineWithoutArcs._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'multipolyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 122, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MultiLineWithoutArcs._Automaton = _BuildAutomaton_19()




MultiDirectedLineWithoutArcs._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'multipolyline'), _ImportedBinding_camac_gis_export_so_schema_geometry.MultiPolylineType, scope=MultiDirectedLineWithoutArcs, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 103, 2)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MultiDirectedLineWithoutArcs._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'multipolyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 127, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MultiDirectedLineWithoutArcs._Automaton = _BuildAutomaton_20()




MultiSurfaceWithoutArcs._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_geom, 'multisurface'), _ImportedBinding_camac_gis_export_so_schema_geometry.MultiSurfaceType, scope=MultiSurfaceWithoutArcs, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 128, 2)))

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MultiSurfaceWithoutArcs._UseForTag(pyxb.namespace.ExpandedName(_Namespace_geom, 'multisurface')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/GeometryCHLV95_V2.xsd', 132, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MultiSurfaceWithoutArcs._Automaton = _BuildAutomaton_21()

