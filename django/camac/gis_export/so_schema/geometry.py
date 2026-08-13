# ../../../camac/gis_export/so_schema/geometry.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:a3802a31954231a649773462036b3bb221bf1d6a
# Generated 2026-08-13 13:25:16.304329 by PyXB version 1.2.6 using Python 3.13.3.final.0
# Namespace http://www.interlis.ch/geometry/1.0 [xmlns:geom]

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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:a2f54d30-8bc1-475c-b11b-e75cb31730ec')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.interlis.ch/geometry/1.0', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

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


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """any vendor specifics"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 10, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.interlis.ch/geometry/1.0}GeometryType with content type ELEMENT_ONLY
class GeometryType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/geometry/1.0}GeometryType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GeometryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 20, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}extensions uses Python identifier extensions
    __extensions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extensions'), 'extensions', '__httpwww_interlis_chgeometry1_0_GeometryType_httpwww_interlis_chgeometry1_0extensions', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 6, 2), )

    
    extensions = property(__extensions.value, __extensions.set, None, 'any vendor specifics')

    
    # Attribute {http://www.interlis.ch/geometry/1.0}epsg uses Python identifier epsg
    __epsg = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'epsg'), 'epsg', '__httpwww_interlis_chgeometry1_0_GeometryType_httpwww_interlis_chgeometry1_0epsg', pyxb.binding.datatypes.string)
    __epsg._DeclarationLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 17, 2)
    __epsg._UseLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 24, 4)
    
    epsg = property(__epsg.value, __epsg.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __extensions.name() : __extensions
    })
    _AttributeMap.update({
        __epsg.name() : __epsg
    })
_module_typeBindings.GeometryType = GeometryType
Namespace.addCategoryObject('typeBinding', 'GeometryType', GeometryType)


# Complex type {http://www.interlis.ch/geometry/1.0}MultiCoordType with content type ELEMENT_ONLY
class MultiCoordType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/geometry/1.0}MultiCoordType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MultiCoordType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 42, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}coord uses Python identifier coord
    __coord = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'coord'), 'coord', '__httpwww_interlis_chgeometry1_0_MultiCoordType_httpwww_interlis_chgeometry1_0coord', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 28, 2), )

    
    coord = property(__coord.value, __coord.set, None, None)

    _ElementMap.update({
        __coord.name() : __coord
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MultiCoordType = MultiCoordType
Namespace.addCategoryObject('typeBinding', 'MultiCoordType', MultiCoordType)


# Complex type {http://www.interlis.ch/geometry/1.0}LineSegmentType with content type ELEMENT_ONLY
class LineSegmentType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/geometry/1.0}LineSegmentType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LineSegmentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 49, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}extensions uses Python identifier extensions
    __extensions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extensions'), 'extensions', '__httpwww_interlis_chgeometry1_0_LineSegmentType_httpwww_interlis_chgeometry1_0extensions', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 6, 2), )

    
    extensions = property(__extensions.value, __extensions.set, None, 'any vendor specifics')

    
    # Element {http://www.interlis.ch/geometry/1.0}c1 uses Python identifier c1
    __c1 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'c1'), 'c1', '__httpwww_interlis_chgeometry1_0_LineSegmentType_httpwww_interlis_chgeometry1_0c1', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 52, 6), )

    
    c1 = property(__c1.value, __c1.set, None, None)

    
    # Element {http://www.interlis.ch/geometry/1.0}c2 uses Python identifier c2
    __c2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'c2'), 'c2', '__httpwww_interlis_chgeometry1_0_LineSegmentType_httpwww_interlis_chgeometry1_0c2', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 53, 6), )

    
    c2 = property(__c2.value, __c2.set, None, None)

    
    # Element {http://www.interlis.ch/geometry/1.0}c3 uses Python identifier c3
    __c3 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'c3'), 'c3', '__httpwww_interlis_chgeometry1_0_LineSegmentType_httpwww_interlis_chgeometry1_0c3', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 54, 6), )

    
    c3 = property(__c3.value, __c3.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __extensions.name() : __extensions,
        __c1.name() : __c1,
        __c2.name() : __c2,
        __c3.name() : __c3
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.LineSegmentType = LineSegmentType
Namespace.addCategoryObject('typeBinding', 'LineSegmentType', LineSegmentType)


# Complex type {http://www.interlis.ch/geometry/1.0}MultiPolylineType with content type ELEMENT_ONLY
class MultiPolylineType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/geometry/1.0}MultiPolylineType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MultiPolylineType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 104, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}polyline uses Python identifier polyline
    __polyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'polyline'), 'polyline', '__httpwww_interlis_chgeometry1_0_MultiPolylineType_httpwww_interlis_chgeometry1_0polyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2), )

    
    polyline = property(__polyline.value, __polyline.set, None, None)

    _ElementMap.update({
        __polyline.name() : __polyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MultiPolylineType = MultiPolylineType
Namespace.addCategoryObject('typeBinding', 'MultiPolylineType', MultiPolylineType)


# Complex type {http://www.interlis.ch/geometry/1.0}BoundaryType with content type ELEMENT_ONLY
class BoundaryType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/geometry/1.0}BoundaryType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BoundaryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 110, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}polyline uses Python identifier polyline
    __polyline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'polyline'), 'polyline', '__httpwww_interlis_chgeometry1_0_BoundaryType_httpwww_interlis_chgeometry1_0polyline', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2), )

    
    polyline = property(__polyline.value, __polyline.set, None, None)

    _ElementMap.update({
        __polyline.name() : __polyline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.BoundaryType = BoundaryType
Namespace.addCategoryObject('typeBinding', 'BoundaryType', BoundaryType)


# Complex type {http://www.interlis.ch/geometry/1.0}MultiSurfaceType with content type ELEMENT_ONLY
class MultiSurfaceType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/geometry/1.0}MultiSurfaceType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MultiSurfaceType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 129, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/geometry/1.0}surface uses Python identifier surface
    __surface = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'surface'), 'surface', '__httpwww_interlis_chgeometry1_0_MultiSurfaceType_httpwww_interlis_chgeometry1_0surface', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 116, 2), )

    
    surface = property(__surface.value, __surface.set, None, None)

    _ElementMap.update({
        __surface.name() : __surface
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MultiSurfaceType = MultiSurfaceType
Namespace.addCategoryObject('typeBinding', 'MultiSurfaceType', MultiSurfaceType)


# Complex type {http://www.interlis.ch/geometry/1.0}CoordType with content type ELEMENT_ONLY
class CoordType (GeometryType):
    """Complex type {http://www.interlis.ch/geometry/1.0}CoordType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CoordType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 29, 2)
    _ElementMap = GeometryType._ElementMap.copy()
    _AttributeMap = GeometryType._AttributeMap.copy()
    # Base type is GeometryType
    
    # Element extensions ({http://www.interlis.ch/geometry/1.0}extensions) inherited from {http://www.interlis.ch/geometry/1.0}GeometryType
    
    # Element {http://www.interlis.ch/geometry/1.0}c1 uses Python identifier c1
    __c1 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'c1'), 'c1', '__httpwww_interlis_chgeometry1_0_CoordType_httpwww_interlis_chgeometry1_0c1', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 33, 10), )

    
    c1 = property(__c1.value, __c1.set, None, None)

    
    # Element {http://www.interlis.ch/geometry/1.0}c2 uses Python identifier c2
    __c2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'c2'), 'c2', '__httpwww_interlis_chgeometry1_0_CoordType_httpwww_interlis_chgeometry1_0c2', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 34, 10), )

    
    c2 = property(__c2.value, __c2.set, None, None)

    
    # Element {http://www.interlis.ch/geometry/1.0}c3 uses Python identifier c3
    __c3 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'c3'), 'c3', '__httpwww_interlis_chgeometry1_0_CoordType_httpwww_interlis_chgeometry1_0c3', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 35, 10), )

    
    c3 = property(__c3.value, __c3.set, None, None)

    
    # Attribute epsg inherited from {http://www.interlis.ch/geometry/1.0}GeometryType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __c1.name() : __c1,
        __c2.name() : __c2,
        __c3.name() : __c3
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CoordType = CoordType
Namespace.addCategoryObject('typeBinding', 'CoordType', CoordType)


# Complex type {http://www.interlis.ch/geometry/1.0}StartSegmentType with content type ELEMENT_ONLY
class StartSegmentType (LineSegmentType):
    """Complex type {http://www.interlis.ch/geometry/1.0}StartSegmentType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'StartSegmentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 59, 2)
    _ElementMap = LineSegmentType._ElementMap.copy()
    _AttributeMap = LineSegmentType._AttributeMap.copy()
    # Base type is LineSegmentType
    
    # Element extensions ({http://www.interlis.ch/geometry/1.0}extensions) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    
    # Element c1 ({http://www.interlis.ch/geometry/1.0}c1) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    
    # Element c2 ({http://www.interlis.ch/geometry/1.0}c2) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    
    # Element c3 ({http://www.interlis.ch/geometry/1.0}c3) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.StartSegmentType = StartSegmentType
Namespace.addCategoryObject('typeBinding', 'StartSegmentType', StartSegmentType)


# Complex type {http://www.interlis.ch/geometry/1.0}StraightSegmentType with content type ELEMENT_ONLY
class StraightSegmentType (LineSegmentType):
    """Complex type {http://www.interlis.ch/geometry/1.0}StraightSegmentType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'StraightSegmentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 67, 2)
    _ElementMap = LineSegmentType._ElementMap.copy()
    _AttributeMap = LineSegmentType._AttributeMap.copy()
    # Base type is LineSegmentType
    
    # Element extensions ({http://www.interlis.ch/geometry/1.0}extensions) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    
    # Element c1 ({http://www.interlis.ch/geometry/1.0}c1) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    
    # Element c2 ({http://www.interlis.ch/geometry/1.0}c2) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    
    # Element c3 ({http://www.interlis.ch/geometry/1.0}c3) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.StraightSegmentType = StraightSegmentType
Namespace.addCategoryObject('typeBinding', 'StraightSegmentType', StraightSegmentType)


# Complex type {http://www.interlis.ch/geometry/1.0}ArcSegmentType with content type ELEMENT_ONLY
class ArcSegmentType (LineSegmentType):
    """Complex type {http://www.interlis.ch/geometry/1.0}ArcSegmentType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ArcSegmentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 75, 2)
    _ElementMap = LineSegmentType._ElementMap.copy()
    _AttributeMap = LineSegmentType._AttributeMap.copy()
    # Base type is LineSegmentType
    
    # Element extensions ({http://www.interlis.ch/geometry/1.0}extensions) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    
    # Element c1 ({http://www.interlis.ch/geometry/1.0}c1) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    
    # Element c2 ({http://www.interlis.ch/geometry/1.0}c2) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    
    # Element c3 ({http://www.interlis.ch/geometry/1.0}c3) inherited from {http://www.interlis.ch/geometry/1.0}LineSegmentType
    
    # Element {http://www.interlis.ch/geometry/1.0}a1 uses Python identifier a1
    __a1 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'a1'), 'a1', '__httpwww_interlis_chgeometry1_0_ArcSegmentType_httpwww_interlis_chgeometry1_0a1', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 79, 10), )

    
    a1 = property(__a1.value, __a1.set, None, None)

    
    # Element {http://www.interlis.ch/geometry/1.0}a2 uses Python identifier a2
    __a2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'a2'), 'a2', '__httpwww_interlis_chgeometry1_0_ArcSegmentType_httpwww_interlis_chgeometry1_0a2', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 80, 10), )

    
    a2 = property(__a2.value, __a2.set, None, None)

    
    # Element {http://www.interlis.ch/geometry/1.0}r uses Python identifier r
    __r = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'r'), 'r', '__httpwww_interlis_chgeometry1_0_ArcSegmentType_httpwww_interlis_chgeometry1_0r', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 81, 10), )

    
    r = property(__r.value, __r.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __a1.name() : __a1,
        __a2.name() : __a2,
        __r.name() : __r
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ArcSegmentType = ArcSegmentType
Namespace.addCategoryObject('typeBinding', 'ArcSegmentType', ArcSegmentType)


# Complex type {http://www.interlis.ch/geometry/1.0}PolylineType with content type ELEMENT_ONLY
class PolylineType (GeometryType):
    """Complex type {http://www.interlis.ch/geometry/1.0}PolylineType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PolylineType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 88, 2)
    _ElementMap = GeometryType._ElementMap.copy()
    _AttributeMap = GeometryType._AttributeMap.copy()
    # Base type is GeometryType
    
    # Element extensions ({http://www.interlis.ch/geometry/1.0}extensions) inherited from {http://www.interlis.ch/geometry/1.0}GeometryType
    
    # Element {http://www.interlis.ch/geometry/1.0}coord uses Python identifier coord
    __coord = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'coord'), 'coord', '__httpwww_interlis_chgeometry1_0_PolylineType_httpwww_interlis_chgeometry1_0coord', True, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 28, 2), )

    
    coord = property(__coord.value, __coord.set, None, None)

    
    # Element {http://www.interlis.ch/geometry/1.0}customLineSegment uses Python identifier customLineSegment
    __customLineSegment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'customLineSegment'), 'customLineSegment', '__httpwww_interlis_chgeometry1_0_PolylineType_httpwww_interlis_chgeometry1_0customLineSegment', True, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 48, 2), )

    
    customLineSegment = property(__customLineSegment.value, __customLineSegment.set, None, None)

    
    # Element {http://www.interlis.ch/geometry/1.0}arc uses Python identifier arc
    __arc = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'arc'), 'arc', '__httpwww_interlis_chgeometry1_0_PolylineType_httpwww_interlis_chgeometry1_0arc', True, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 95, 12), )

    
    arc = property(__arc.value, __arc.set, None, None)

    
    # Attribute epsg inherited from {http://www.interlis.ch/geometry/1.0}GeometryType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __coord.name() : __coord,
        __customLineSegment.name() : __customLineSegment,
        __arc.name() : __arc
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.PolylineType = PolylineType
Namespace.addCategoryObject('typeBinding', 'PolylineType', PolylineType)


# Complex type {http://www.interlis.ch/geometry/1.0}SurfaceType with content type ELEMENT_ONLY
class SurfaceType (GeometryType):
    """Complex type {http://www.interlis.ch/geometry/1.0}SurfaceType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SurfaceType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 117, 2)
    _ElementMap = GeometryType._ElementMap.copy()
    _AttributeMap = GeometryType._AttributeMap.copy()
    # Base type is GeometryType
    
    # Element extensions ({http://www.interlis.ch/geometry/1.0}extensions) inherited from {http://www.interlis.ch/geometry/1.0}GeometryType
    
    # Element {http://www.interlis.ch/geometry/1.0}exterior uses Python identifier exterior
    __exterior = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'exterior'), 'exterior', '__httpwww_interlis_chgeometry1_0_SurfaceType_httpwww_interlis_chgeometry1_0exterior', True, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 121, 10), )

    
    exterior = property(__exterior.value, __exterior.set, None, None)

    
    # Element {http://www.interlis.ch/geometry/1.0}interior uses Python identifier interior
    __interior = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'interior'), 'interior', '__httpwww_interlis_chgeometry1_0_SurfaceType_httpwww_interlis_chgeometry1_0interior', True, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 122, 10), )

    
    interior = property(__interior.value, __interior.set, None, None)

    
    # Attribute epsg inherited from {http://www.interlis.ch/geometry/1.0}GeometryType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _ElementMap.update({
        __exterior.name() : __exterior,
        __interior.name() : __interior
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.SurfaceType = SurfaceType
Namespace.addCategoryObject('typeBinding', 'SurfaceType', SurfaceType)


extensions = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensions'), CTD_ANON, documentation='any vendor specifics', location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 6, 2))
Namespace.addCategoryObject('elementBinding', extensions.name().localName(), extensions)

geometry = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'geometry'), GeometryType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 19, 2))
Namespace.addCategoryObject('elementBinding', geometry.name().localName(), geometry)

multicoord = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'multicoord'), MultiCoordType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 41, 2))
Namespace.addCategoryObject('elementBinding', multicoord.name().localName(), multicoord)

customLineSegment = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'customLineSegment'), LineSegmentType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 48, 2))
Namespace.addCategoryObject('elementBinding', customLineSegment.name().localName(), customLineSegment)

multipolyline = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'multipolyline'), MultiPolylineType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 103, 2))
Namespace.addCategoryObject('elementBinding', multipolyline.name().localName(), multipolyline)

multisurface = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'multisurface'), MultiSurfaceType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 128, 2))
Namespace.addCategoryObject('elementBinding', multisurface.name().localName(), multisurface)

coord = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'coord'), CoordType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 28, 2))
Namespace.addCategoryObject('elementBinding', coord.name().localName(), coord)

polyline = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'polyline'), PolylineType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2))
Namespace.addCategoryObject('elementBinding', polyline.name().localName(), polyline)

surface = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'surface'), SurfaceType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 116, 2))
Namespace.addCategoryObject('elementBinding', surface.name().localName(), surface)



def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 12, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 12, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




GeometryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensions'), CTD_ANON, scope=GeometryType, documentation='any vendor specifics', location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 6, 2)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 22, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(GeometryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 22, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
GeometryType._Automaton = _BuildAutomaton_()




MultiCoordType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'coord'), CoordType, scope=MultiCoordType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 28, 2)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 44, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MultiCoordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'coord')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 44, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MultiCoordType._Automaton = _BuildAutomaton_2()




LineSegmentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extensions'), CTD_ANON, scope=LineSegmentType, documentation='any vendor specifics', location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 6, 2)))

LineSegmentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'c1'), pyxb.binding.datatypes.double, scope=LineSegmentType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 52, 6)))

LineSegmentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'c2'), pyxb.binding.datatypes.double, scope=LineSegmentType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 53, 6)))

LineSegmentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'c3'), pyxb.binding.datatypes.double, scope=LineSegmentType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 54, 6)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 51, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 54, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LineSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 51, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LineSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c1')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 52, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(LineSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c2')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 53, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(LineSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c3')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 54, 6))
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
LineSegmentType._Automaton = _BuildAutomaton_3()




MultiPolylineType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'polyline'), PolylineType, scope=MultiPolylineType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 106, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MultiPolylineType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'polyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 106, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MultiPolylineType._Automaton = _BuildAutomaton_4()




BoundaryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'polyline'), PolylineType, scope=BoundaryType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 87, 2)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BoundaryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'polyline')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 112, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
BoundaryType._Automaton = _BuildAutomaton_5()




MultiSurfaceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'surface'), SurfaceType, scope=MultiSurfaceType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 116, 2)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 131, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MultiSurfaceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'surface')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 131, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MultiSurfaceType._Automaton = _BuildAutomaton_6()




CoordType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'c1'), pyxb.binding.datatypes.double, scope=CoordType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 33, 10)))

CoordType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'c2'), pyxb.binding.datatypes.double, scope=CoordType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 34, 10)))

CoordType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'c3'), pyxb.binding.datatypes.double, scope=CoordType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 35, 10)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 22, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 35, 10))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CoordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 22, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CoordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c1')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 33, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CoordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c2')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 34, 10))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CoordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c3')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 35, 10))
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
CoordType._Automaton = _BuildAutomaton_7()




def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 51, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 54, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(StartSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 51, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(StartSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c1')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 52, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(StartSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c2')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 53, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(StartSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c3')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 54, 6))
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
StartSegmentType._Automaton = _BuildAutomaton_8()




def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 51, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 54, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(StraightSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 51, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(StraightSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c1')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 52, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(StraightSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c2')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 53, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(StraightSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c3')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 54, 6))
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
StraightSegmentType._Automaton = _BuildAutomaton_9()




ArcSegmentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'a1'), pyxb.binding.datatypes.double, scope=ArcSegmentType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 79, 10)))

ArcSegmentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'a2'), pyxb.binding.datatypes.double, scope=ArcSegmentType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 80, 10)))

ArcSegmentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'r'), pyxb.binding.datatypes.double, scope=ArcSegmentType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 81, 10)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 51, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 54, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 81, 10))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ArcSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 51, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ArcSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c1')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 52, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ArcSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c2')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 53, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ArcSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'c3')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 54, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ArcSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'a1')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 79, 10))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ArcSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'a2')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 80, 10))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(ArcSegmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'r')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 81, 10))
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
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
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ArcSegmentType._Automaton = _BuildAutomaton_10()




PolylineType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'coord'), CoordType, scope=PolylineType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 28, 2)))

PolylineType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'customLineSegment'), LineSegmentType, scope=PolylineType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 48, 2)))

PolylineType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'arc'), ArcSegmentType, scope=PolylineType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 95, 12)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 22, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(PolylineType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 22, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(PolylineType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'coord')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 92, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(PolylineType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'coord')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 94, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(PolylineType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'arc')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 95, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(PolylineType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'customLineSegment')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 96, 12))
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
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
PolylineType._Automaton = _BuildAutomaton_11()




SurfaceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'exterior'), BoundaryType, scope=SurfaceType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 121, 10)))

SurfaceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'interior'), BoundaryType, scope=SurfaceType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 122, 10)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 22, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 122, 10))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SurfaceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extensions')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 22, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SurfaceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'exterior')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 121, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(SurfaceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'interior')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/geometry.xsd', 122, 10))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SurfaceType._Automaton = _BuildAutomaton_12()


coord._setSubstitutionGroup(geometry)

polyline._setSubstitutionGroup(geometry)

surface._setSubstitutionGroup(geometry)
