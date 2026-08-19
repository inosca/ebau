# ../../../camac/gis_export/so_schema/SO_DSBJD_eBauSO_Geschaefte_20250422.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:3da224dfcac20d1ee95f94a3b0ad73a86187cc9b
# Generated 2026-08-18 17:22:41.115414 by PyXB version 1.2.6 using Python 3.13.3.final.0
# Namespace http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422

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
import camac.gis_export.so_schema.GeometryCHLV95_V2 as _ImportedBinding_camac_gis_export_so_schema_GeometryCHLV95_V2
import camac.gis_export.so_schema.INTERLIS as _ImportedBinding_camac_gis_export_so_schema_INTERLIS
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422', create_if_missing=True)
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


# Atomic simple type: {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Status_Geschaeft
class Status_Geschaeft (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Status_Geschaeft')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 21, 0)
    _Documentation = None
Status_Geschaeft._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'Status_Geschaeft', Status_Geschaeft)
_module_typeBindings.Status_Geschaeft = Status_Geschaeft

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Entscheid
class Entscheid_ (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Entscheid')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 25, 0)
    _Documentation = None
Entscheid_._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'Entscheid', Entscheid_)
_module_typeBindings.Entscheid_ = Entscheid_

# Atomic simple type: {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Fachstellen
class Fachstellen (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Fachstellen')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 29, 0)
    _Documentation = None
Fachstellen._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'Fachstellen', Fachstellen)
_module_typeBindings.Fachstellen = Fachstellen

# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 38, 6)
    _Documentation = None
STD_ANON._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(500))
STD_ANON._InitializeFacetMap(STD_ANON._CF_maxLength)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 45, 6)
    _Documentation = None
STD_ANON_._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(500))
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_maxLength)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Atomic simple type: [anonymous]
class STD_ANON_2 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 57, 6)
    _Documentation = None
STD_ANON_2._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(200))
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_maxLength)
_module_typeBindings.STD_ANON_2 = STD_ANON_2

# Atomic simple type: [anonymous]
class STD_ANON_3 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 64, 6)
    _Documentation = None
STD_ANON_3._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(10))
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_maxLength)
_module_typeBindings.STD_ANON_3 = STD_ANON_3

# Atomic simple type: [anonymous]
class STD_ANON_4 (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 71, 6)
    _Documentation = None
STD_ANON_4._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(9999), value_datatype=STD_ANON_4)
STD_ANON_4._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(1000), value_datatype=STD_ANON_4)
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_maxInclusive,
   STD_ANON_4._CF_minInclusive)
_module_typeBindings.STD_ANON_4 = STD_ANON_4

# Atomic simple type: [anonymous]
class STD_ANON_5 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 79, 6)
    _Documentation = None
STD_ANON_5._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(200))
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_maxLength)
_module_typeBindings.STD_ANON_5 = STD_ANON_5

# Atomic simple type: [anonymous]
class STD_ANON_6 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 91, 6)
    _Documentation = None
STD_ANON_6._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_maxLength)
_module_typeBindings.STD_ANON_6 = STD_ANON_6

# Atomic simple type: [anonymous]
class STD_ANON_7 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 98, 6)
    _Documentation = None
STD_ANON_7._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_7._InitializeFacetMap(STD_ANON_7._CF_maxLength)
_module_typeBindings.STD_ANON_7 = STD_ANON_7

# Atomic simple type: [anonymous]
class STD_ANON_8 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 110, 6)
    _Documentation = None
STD_ANON_8._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(200))
STD_ANON_8._InitializeFacetMap(STD_ANON_8._CF_maxLength)
_module_typeBindings.STD_ANON_8 = STD_ANON_8

# Atomic simple type: [anonymous]
class STD_ANON_9 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 181, 6)
    _Documentation = None
STD_ANON_9._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(10))
STD_ANON_9._InitializeFacetMap(STD_ANON_9._CF_maxLength)
_module_typeBindings.STD_ANON_9 = STD_ANON_9

# Atomic simple type: [anonymous]
class STD_ANON_10 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 188, 6)
    _Documentation = None
STD_ANON_10._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(14))
STD_ANON_10._InitializeFacetMap(STD_ANON_10._CF_maxLength)
_module_typeBindings.STD_ANON_10 = STD_ANON_10

# Atomic simple type: [anonymous]
class STD_ANON_11 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 200, 6)
    _Documentation = None
STD_ANON_11._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(200))
STD_ANON_11._InitializeFacetMap(STD_ANON_11._CF_maxLength)
_module_typeBindings.STD_ANON_11 = STD_ANON_11

# Atomic simple type: [anonymous]
class STD_ANON_12 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 207, 6)
    _Documentation = None
STD_ANON_12._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(1000))
STD_ANON_12._InitializeFacetMap(STD_ANON_12._CF_maxLength)
_module_typeBindings.STD_ANON_12 = STD_ANON_12

# Atomic simple type: [anonymous]
class STD_ANON_13 (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 214, 6)
    _Documentation = None
STD_ANON_13._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(900000000), value_datatype=STD_ANON_13)
STD_ANON_13._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(1), value_datatype=STD_ANON_13)
STD_ANON_13._InitializeFacetMap(STD_ANON_13._CF_maxInclusive,
   STD_ANON_13._CF_minInclusive)
_module_typeBindings.STD_ANON_13 = STD_ANON_13

# Atomic simple type: [anonymous]
class STD_ANON_14 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 222, 6)
    _Documentation = None
STD_ANON_14._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
STD_ANON_14._InitializeFacetMap(STD_ANON_14._CF_maxLength)
_module_typeBindings.STD_ANON_14 = STD_ANON_14

# Atomic simple type: [anonymous]
class STD_ANON_15 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 229, 6)
    _Documentation = None
STD_ANON_15._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_15._InitializeFacetMap(STD_ANON_15._CF_maxLength)
_module_typeBindings.STD_ANON_15 = STD_ANON_15

# Atomic simple type: [anonymous]
class STD_ANON_16 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 241, 6)
    _Documentation = None
STD_ANON_16._InitializeFacetMap()
_module_typeBindings.STD_ANON_16 = STD_ANON_16

# Atomic simple type: [anonymous]
class STD_ANON_17 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 247, 6)
    _Documentation = None
STD_ANON_17._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
STD_ANON_17._InitializeFacetMap(STD_ANON_17._CF_maxLength)
_module_typeBindings.STD_ANON_17 = STD_ANON_17

# Atomic simple type: [anonymous]
class STD_ANON_18 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 254, 6)
    _Documentation = None
STD_ANON_18._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(200))
STD_ANON_18._InitializeFacetMap(STD_ANON_18._CF_maxLength)
_module_typeBindings.STD_ANON_18 = STD_ANON_18

# Atomic simple type: [anonymous]
class STD_ANON_19 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 273, 6)
    _Documentation = None
STD_ANON_19._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(72))
STD_ANON_19._InitializeFacetMap(STD_ANON_19._CF_maxLength)
_module_typeBindings.STD_ANON_19 = STD_ANON_19

# Atomic simple type: [anonymous]
class STD_ANON_20 (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 280, 6)
    _Documentation = None
STD_ANON_20._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(9999), value_datatype=STD_ANON_20)
STD_ANON_20._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(0), value_datatype=STD_ANON_20)
STD_ANON_20._InitializeFacetMap(STD_ANON_20._CF_maxInclusive,
   STD_ANON_20._CF_minInclusive)
_module_typeBindings.STD_ANON_20 = STD_ANON_20

# Atomic simple type: [anonymous]
class STD_ANON_21 (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 288, 6)
    _Documentation = None
STD_ANON_21._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(200))
STD_ANON_21._InitializeFacetMap(STD_ANON_21._CF_maxLength)
_module_typeBindings.STD_ANON_21 = STD_ANON_21

# Atomic simple type: [anonymous]
class STD_ANON_22 (pyxb.binding.datatypes.anyURI):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 377, 6)
    _Documentation = None
STD_ANON_22._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(1023))
STD_ANON_22._InitializeFacetMap(STD_ANON_22._CF_maxLength)
_module_typeBindings.STD_ANON_22 = STD_ANON_22

# Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}ZustaendigkeitType with content type ELEMENT_ONLY
class ZustaendigkeitType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}ZustaendigkeitType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ZustaendigkeitType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 34, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Fachstelle uses Python identifier Fachstelle
    __Fachstelle = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Fachstelle'), 'Fachstelle', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_ZustaendigkeitType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Fachstelle', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 36, 4), )

    
    Fachstelle = property(__Fachstelle.value, __Fachstelle.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Name'), 'Name', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_ZustaendigkeitType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Name', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 37, 4), )

    
    Name = property(__Name.value, __Name.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Abteilung uses Python identifier Abteilung
    __Abteilung = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Abteilung'), 'Abteilung', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_ZustaendigkeitType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Abteilung', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 44, 4), )

    
    Abteilung = property(__Abteilung.value, __Abteilung.set, None, None)

    _ElementMap.update({
        __Fachstelle.name() : __Fachstelle,
        __Name.name() : __Name,
        __Abteilung.name() : __Abteilung
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ZustaendigkeitType = ZustaendigkeitType
Namespace.addCategoryObject('typeBinding', 'ZustaendigkeitType', ZustaendigkeitType)


# Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Adresse_Type with content type ELEMENT_ONLY
class Adresse_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Adresse_Type with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Adresse_Type')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 54, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Strassenname uses Python identifier Strassenname
    __Strassenname = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Strassenname'), 'Strassenname', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Adresse_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Strassenname', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 56, 4), )

    
    Strassenname = property(__Strassenname.value, __Strassenname.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Hausnummer uses Python identifier Hausnummer
    __Hausnummer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Hausnummer'), 'Hausnummer', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Adresse_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Hausnummer', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 63, 4), )

    
    Hausnummer = property(__Hausnummer.value, __Hausnummer.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}PLZ uses Python identifier PLZ
    __PLZ = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PLZ'), 'PLZ', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Adresse_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422PLZ', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 70, 4), )

    
    PLZ = property(__PLZ.value, __PLZ.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Ortschaft uses Python identifier Ortschaft
    __Ortschaft = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Ortschaft'), 'Ortschaft', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Adresse_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Ortschaft', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 78, 4), )

    
    Ortschaft = property(__Ortschaft.value, __Ortschaft.set, None, None)

    _ElementMap.update({
        __Strassenname.name() : __Strassenname,
        __Hausnummer.name() : __Hausnummer,
        __PLZ.name() : __PLZ,
        __Ortschaft.name() : __Ortschaft
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Adresse_Type = Adresse_Type
Namespace.addCategoryObject('typeBinding', 'Adresse_Type', Adresse_Type)


# Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Natuerliche_PersonType with content type ELEMENT_ONLY
class Natuerliche_PersonType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Natuerliche_PersonType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Natuerliche_PersonType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 88, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Name'), 'Name', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Natuerliche_PersonType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Name', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 90, 4), )

    
    Name = property(__Name.value, __Name.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Vorname uses Python identifier Vorname
    __Vorname = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Vorname'), 'Vorname', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Natuerliche_PersonType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Vorname', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 97, 4), )

    
    Vorname = property(__Vorname.value, __Vorname.set, None, None)

    _ElementMap.update({
        __Name.name() : __Name,
        __Vorname.name() : __Vorname
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Natuerliche_PersonType = Natuerliche_PersonType
Namespace.addCategoryObject('typeBinding', 'Natuerliche_PersonType', Natuerliche_PersonType)


# Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Juristische_PersonType with content type ELEMENT_ONLY
class Juristische_PersonType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Juristische_PersonType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Juristische_PersonType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 107, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Name'), 'Name', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Juristische_PersonType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Name', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 109, 4), )

    
    Name = property(__Name.value, __Name.set, None, None)

    _ElementMap.update({
        __Name.name() : __Name
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Juristische_PersonType = Juristische_PersonType
Namespace.addCategoryObject('typeBinding', 'Juristische_PersonType', Juristische_PersonType)


# Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}PersonAdresseType with content type ELEMENT_ONLY
class PersonAdresseType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}PersonAdresseType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PersonAdresseType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 119, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Natuerliche_Person uses Python identifier Natuerliche_Person
    __Natuerliche_Person = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Natuerliche_Person'), 'Natuerliche_Person', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_PersonAdresseType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Natuerliche_Person', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 121, 4), )

    
    Natuerliche_Person = property(__Natuerliche_Person.value, __Natuerliche_Person.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Juristische_Person uses Python identifier Juristische_Person
    __Juristische_Person = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Juristische_Person'), 'Juristische_Person', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_PersonAdresseType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Juristische_Person', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 128, 4), )

    
    Juristische_Person = property(__Juristische_Person.value, __Juristische_Person.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Adresse uses Python identifier Adresse
    __Adresse = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Adresse'), 'Adresse', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_PersonAdresseType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Adresse', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 135, 4), )

    
    Adresse = property(__Adresse.value, __Adresse.set, None, None)

    _ElementMap.update({
        __Natuerliche_Person.name() : __Natuerliche_Person,
        __Juristische_Person.name() : __Juristische_Person,
        __Adresse.name() : __Adresse
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.PersonAdresseType = PersonAdresseType
Namespace.addCategoryObject('typeBinding', 'PersonAdresseType', PersonAdresseType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 122, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Natuerliche_Person uses Python identifier Natuerliche_Person
    __Natuerliche_Person = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Natuerliche_Person'), 'Natuerliche_Person', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Natuerliche_Person', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 87, 0), )

    
    Natuerliche_Person = property(__Natuerliche_Person.value, __Natuerliche_Person.set, None, None)

    _ElementMap.update({
        __Natuerliche_Person.name() : __Natuerliche_Person
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
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 129, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Juristische_Person uses Python identifier Juristische_Person
    __Juristische_Person = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Juristische_Person'), 'Juristische_Person', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Juristische_Person', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 106, 0), )

    
    Juristische_Person = property(__Juristische_Person.value, __Juristische_Person.set, None, None)

    _ElementMap.update({
        __Juristische_Person.name() : __Juristische_Person
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
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 136, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Adresse_ uses Python identifier Adresse
    __Adresse = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Adresse_'), 'Adresse', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_2_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Adresse', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 53, 0), )

    
    Adresse = property(__Adresse.value, __Adresse.set, None, None)

    _ElementMap.update({
        __Adresse.name() : __Adresse
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Gesuchsteller_Type with content type ELEMENT_ONLY
class Gesuchsteller_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Gesuchsteller_Type with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Gesuchsteller_Type')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 145, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Adresse uses Python identifier Adresse
    __Adresse = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Adresse'), 'Adresse', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Gesuchsteller_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Adresse', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 147, 4), )

    
    Adresse = property(__Adresse.value, __Adresse.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Vertretung uses Python identifier Vertretung
    __Vertretung = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Vertretung'), 'Vertretung', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Gesuchsteller_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Vertretung', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 154, 4), )

    
    Vertretung = property(__Vertretung.value, __Vertretung.set, None, None)

    _ElementMap.update({
        __Adresse.name() : __Adresse,
        __Vertretung.name() : __Vertretung
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Gesuchsteller_Type = Gesuchsteller_Type
Namespace.addCategoryObject('typeBinding', 'Gesuchsteller_Type', Gesuchsteller_Type)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 148, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}PersonAdresse uses Python identifier PersonAdresse
    __PersonAdresse = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse'), 'PersonAdresse', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_3_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422PersonAdresse', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 118, 0), )

    
    PersonAdresse = property(__PersonAdresse.value, __PersonAdresse.set, None, None)

    _ElementMap.update({
        __PersonAdresse.name() : __PersonAdresse
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 155, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}PersonAdresse uses Python identifier PersonAdresse
    __PersonAdresse = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse'), 'PersonAdresse', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_4_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422PersonAdresse', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 118, 0), )

    
    PersonAdresse = property(__PersonAdresse.value, __PersonAdresse.set, None, None)

    _ElementMap.update({
        __PersonAdresse.name() : __PersonAdresse
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_4 = CTD_ANON_4


# Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Entscheid_Type with content type ELEMENT_ONLY
class Entscheid_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Entscheid_Type with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Entscheid_Type')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 164, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Entscheid uses Python identifier Entscheid
    __Entscheid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Entscheid'), 'Entscheid', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Entscheid_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Entscheid', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 166, 4), )

    
    Entscheid = property(__Entscheid.value, __Entscheid.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Datum uses Python identifier Datum
    __Datum = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Datum'), 'Datum', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Entscheid_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Datum', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 167, 4), )

    
    Datum = property(__Datum.value, __Datum.set, None, None)

    _ElementMap.update({
        __Entscheid.name() : __Entscheid,
        __Datum.name() : __Datum
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Entscheid_Type = Entscheid_Type
Namespace.addCategoryObject('typeBinding', 'Entscheid_Type', Entscheid_Type)


# Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Auflage_Type with content type ELEMENT_ONLY
class Auflage_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Auflage_Type with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Auflage_Type')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 171, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Startdatum uses Python identifier Startdatum
    __Startdatum = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Startdatum'), 'Startdatum', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Auflage_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Startdatum', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 173, 4), )

    
    Startdatum = property(__Startdatum.value, __Startdatum.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Enddatum uses Python identifier Enddatum
    __Enddatum = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Enddatum'), 'Enddatum', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Auflage_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Enddatum', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 174, 4), )

    
    Enddatum = property(__Enddatum.value, __Enddatum.set, None, None)

    _ElementMap.update({
        __Startdatum.name() : __Startdatum,
        __Enddatum.name() : __Enddatum
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Auflage_Type = Auflage_Type
Namespace.addCategoryObject('typeBinding', 'Auflage_Type', Auflage_Type)


# Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}GrundstueckType with content type ELEMENT_ONLY
class GrundstueckType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}GrundstueckType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GrundstueckType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 178, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Nummer uses Python identifier Nummer
    __Nummer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Nummer'), 'Nummer', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GrundstueckType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Nummer', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 180, 4), )

    
    Nummer = property(__Nummer.value, __Nummer.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}EGRID uses Python identifier EGRID
    __EGRID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EGRID'), 'EGRID', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GrundstueckType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422EGRID', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 187, 4), )

    
    EGRID = property(__EGRID.value, __EGRID.set, None, None)

    _ElementMap.update({
        __Nummer.name() : __Nummer,
        __EGRID.name() : __EGRID
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.GrundstueckType = GrundstueckType
Namespace.addCategoryObject('typeBinding', 'GrundstueckType', GrundstueckType)


# Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}BauwerkType with content type ELEMENT_ONLY
class BauwerkType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}BauwerkType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BauwerkType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 197, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Bezeichnung uses Python identifier Bezeichnung
    __Bezeichnung = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Bezeichnung'), 'Bezeichnung', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_BauwerkType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Bezeichnung', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 199, 4), )

    
    Bezeichnung = property(__Bezeichnung.value, __Bezeichnung.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Bauwerk_Typ uses Python identifier Bauwerk_Typ
    __Bauwerk_Typ = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Bauwerk_Typ'), 'Bauwerk_Typ', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_BauwerkType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Bauwerk_Typ', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 206, 4), )

    
    Bauwerk_Typ = property(__Bauwerk_Typ.value, __Bauwerk_Typ.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}EGID uses Python identifier EGID
    __EGID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EGID'), 'EGID', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_BauwerkType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422EGID', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 213, 4), )

    
    EGID = property(__EGID.value, __EGID.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Arbeiten_Art uses Python identifier Arbeiten_Art
    __Arbeiten_Art = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Arbeiten_Art'), 'Arbeiten_Art', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_BauwerkType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Arbeiten_Art', True, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 221, 4), )

    
    Arbeiten_Art = property(__Arbeiten_Art.value, __Arbeiten_Art.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Gebaeudekategorie uses Python identifier Gebaeudekategorie
    __Gebaeudekategorie = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Gebaeudekategorie'), 'Gebaeudekategorie', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_BauwerkType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Gebaeudekategorie', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 228, 4), )

    
    Gebaeudekategorie = property(__Gebaeudekategorie.value, __Gebaeudekategorie.set, None, None)

    _ElementMap.update({
        __Bezeichnung.name() : __Bezeichnung,
        __Bauwerk_Typ.name() : __Bauwerk_Typ,
        __EGID.name() : __EGID,
        __Arbeiten_Art.name() : __Arbeiten_Art,
        __Gebaeudekategorie.name() : __Gebaeudekategorie
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.BauwerkType = BauwerkType
Namespace.addCategoryObject('typeBinding', 'BauwerkType', BauwerkType)


# Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Bauprojekt_Type with content type ELEMENT_ONLY
class Bauprojekt_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Bauprojekt_Type with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Bauprojekt_Type')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 238, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Beschreibung uses Python identifier Beschreibung
    __Beschreibung = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Beschreibung'), 'Beschreibung', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Bauprojekt_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Beschreibung', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 240, 4), )

    
    Beschreibung = property(__Beschreibung.value, __Beschreibung.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Bauwerk_Art uses Python identifier Bauwerk_Art
    __Bauwerk_Art = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Bauwerk_Art'), 'Bauwerk_Art', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Bauprojekt_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Bauwerk_Art', True, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 246, 4), )

    
    Bauwerk_Art = property(__Bauwerk_Art.value, __Bauwerk_Art.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Nutzungszweck uses Python identifier Nutzungszweck
    __Nutzungszweck = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Nutzungszweck'), 'Nutzungszweck', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Bauprojekt_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Nutzungszweck', True, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 253, 4), )

    
    Nutzungszweck = property(__Nutzungszweck.value, __Nutzungszweck.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Bauwerke uses Python identifier Bauwerke
    __Bauwerke = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Bauwerke'), 'Bauwerke', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_Bauprojekt_Type_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Bauwerke', True, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 260, 4), )

    
    Bauwerke = property(__Bauwerke.value, __Bauwerke.set, None, None)

    _ElementMap.update({
        __Beschreibung.name() : __Beschreibung,
        __Bauwerk_Art.name() : __Bauwerk_Art,
        __Nutzungszweck.name() : __Nutzungszweck,
        __Bauwerke.name() : __Bauwerke
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Bauprojekt_Type = Bauprojekt_Type
Namespace.addCategoryObject('typeBinding', 'Bauprojekt_Type', Bauprojekt_Type)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 261, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Bauwerk uses Python identifier Bauwerk
    __Bauwerk = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Bauwerk'), 'Bauwerk', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_5_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Bauwerk', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 196, 0), )

    
    Bauwerk = property(__Bauwerk.value, __Bauwerk.set, None, None)

    _ElementMap.update({
        __Bauwerk.name() : __Bauwerk
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_5 = CTD_ANON_5


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 298, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Adresse_ uses Python identifier Adresse
    __Adresse = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Adresse_'), 'Adresse', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_6_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Adresse', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 53, 0), )

    
    Adresse = property(__Adresse.value, __Adresse.set, None, None)

    _ElementMap.update({
        __Adresse.name() : __Adresse
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_6 = CTD_ANON_6


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 306, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Gesuchsteller_ uses Python identifier Gesuchsteller
    __Gesuchsteller = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Gesuchsteller_'), 'Gesuchsteller', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_7_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Gesuchsteller', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 144, 0), )

    
    Gesuchsteller = property(__Gesuchsteller.value, __Gesuchsteller.set, None, None)

    _ElementMap.update({
        __Gesuchsteller.name() : __Gesuchsteller
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_7 = CTD_ANON_7


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 313, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}PersonAdresse uses Python identifier PersonAdresse
    __PersonAdresse = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse'), 'PersonAdresse', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_8_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422PersonAdresse', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 118, 0), )

    
    PersonAdresse = property(__PersonAdresse.value, __PersonAdresse.set, None, None)

    _ElementMap.update({
        __PersonAdresse.name() : __PersonAdresse
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_8 = CTD_ANON_8


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 320, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}PersonAdresse uses Python identifier PersonAdresse
    __PersonAdresse = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse'), 'PersonAdresse', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_9_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422PersonAdresse', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 118, 0), )

    
    PersonAdresse = property(__PersonAdresse.value, __PersonAdresse.set, None, None)

    _ElementMap.update({
        __PersonAdresse.name() : __PersonAdresse
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_9 = CTD_ANON_9


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 327, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}PersonAdresse uses Python identifier PersonAdresse
    __PersonAdresse = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse'), 'PersonAdresse', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_10_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422PersonAdresse', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 118, 0), )

    
    PersonAdresse = property(__PersonAdresse.value, __PersonAdresse.set, None, None)

    _ElementMap.update({
        __PersonAdresse.name() : __PersonAdresse
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_10 = CTD_ANON_10


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 335, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Bauprojekt_ uses Python identifier Bauprojekt
    __Bauprojekt = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Bauprojekt_'), 'Bauprojekt', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_11_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Bauprojekt', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 237, 0), )

    
    Bauprojekt = property(__Bauprojekt.value, __Bauprojekt.set, None, None)

    _ElementMap.update({
        __Bauprojekt.name() : __Bauprojekt
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_11 = CTD_ANON_11


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 342, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Grundstueck uses Python identifier Grundstueck
    __Grundstueck = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Grundstueck'), 'Grundstueck', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_12_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Grundstueck', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 177, 0), )

    
    Grundstueck = property(__Grundstueck.value, __Grundstueck.set, None, None)

    _ElementMap.update({
        __Grundstueck.name() : __Grundstueck
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_12 = CTD_ANON_12


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 349, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Entscheid_ uses Python identifier Entscheid
    __Entscheid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Entscheid_'), 'Entscheid', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_13_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Entscheid', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 163, 0), )

    
    Entscheid = property(__Entscheid.value, __Entscheid.set, None, None)

    _ElementMap.update({
        __Entscheid.name() : __Entscheid
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_13 = CTD_ANON_13


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_14 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 356, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Auflage_ uses Python identifier Auflage
    __Auflage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Auflage_'), 'Auflage', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_14_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Auflage', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 170, 0), )

    
    Auflage = property(__Auflage.value, __Auflage.set, None, None)

    _ElementMap.update({
        __Auflage.name() : __Auflage
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_14 = CTD_ANON_14


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_15 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 363, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Zustaendigkeit uses Python identifier Zustaendigkeit
    __Zustaendigkeit = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Zustaendigkeit'), 'Zustaendigkeit', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_15_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Zustaendigkeit', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 33, 0), )

    
    Zustaendigkeit = property(__Zustaendigkeit.value, __Zustaendigkeit.set, None, None)

    _ElementMap.update({
        __Zustaendigkeit.name() : __Zustaendigkeit
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_15 = CTD_ANON_15


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_16 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 370, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Zustaendigkeit uses Python identifier Zustaendigkeit
    __Zustaendigkeit = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Zustaendigkeit'), 'Zustaendigkeit', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_CTD_ANON_16_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Zustaendigkeit', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 33, 0), )

    
    Zustaendigkeit = property(__Zustaendigkeit.value, __Zustaendigkeit.set, None, None)

    _ElementMap.update({
        __Zustaendigkeit.name() : __Zustaendigkeit
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_16 = CTD_ANON_16


# Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}GeschaeftType with content type ELEMENT_ONLY
class GeschaeftType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}GeschaeftType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GeschaeftType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 270, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Identifikator uses Python identifier Identifikator
    __Identifikator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Identifikator'), 'Identifikator', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Identifikator', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 272, 4), )

    
    Identifikator = property(__Identifikator.value, __Identifikator.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}BFSNr uses Python identifier BFSNr
    __BFSNr = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BFSNr'), 'BFSNr', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422BFSNr', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 279, 4), )

    
    BFSNr = property(__BFSNr.value, __BFSNr.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Verfahrensart uses Python identifier Verfahrensart
    __Verfahrensart = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Verfahrensart'), 'Verfahrensart', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Verfahrensart', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 287, 4), )

    
    Verfahrensart = property(__Verfahrensart.value, __Verfahrensart.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Geometrie_Punkt uses Python identifier Geometrie_Punkt
    __Geometrie_Punkt = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Geometrie_Punkt'), 'Geometrie_Punkt', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Geometrie_Punkt', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 294, 4), )

    
    Geometrie_Punkt = property(__Geometrie_Punkt.value, __Geometrie_Punkt.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Geometrie_Linie uses Python identifier Geometrie_Linie
    __Geometrie_Linie = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Geometrie_Linie'), 'Geometrie_Linie', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Geometrie_Linie', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 295, 4), )

    
    Geometrie_Linie = property(__Geometrie_Linie.value, __Geometrie_Linie.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Geometrie_Flaeche uses Python identifier Geometrie_Flaeche
    __Geometrie_Flaeche = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Geometrie_Flaeche'), 'Geometrie_Flaeche', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Geometrie_Flaeche', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 296, 4), )

    
    Geometrie_Flaeche = property(__Geometrie_Flaeche.value, __Geometrie_Flaeche.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Lokalisation uses Python identifier Lokalisation
    __Lokalisation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Lokalisation'), 'Lokalisation', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Lokalisation', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 297, 4), )

    
    Lokalisation = property(__Lokalisation.value, __Lokalisation.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Status uses Python identifier Status
    __Status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Status'), 'Status', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Status', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 304, 4), )

    
    Status = property(__Status.value, __Status.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Gesuchsteller uses Python identifier Gesuchsteller
    __Gesuchsteller = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Gesuchsteller'), 'Gesuchsteller', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Gesuchsteller', True, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 305, 4), )

    
    Gesuchsteller = property(__Gesuchsteller.value, __Gesuchsteller.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Projektverfasser uses Python identifier Projektverfasser
    __Projektverfasser = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Projektverfasser'), 'Projektverfasser', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Projektverfasser', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 312, 4), )

    
    Projektverfasser = property(__Projektverfasser.value, __Projektverfasser.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Rechnungsempfaenger uses Python identifier Rechnungsempfaenger
    __Rechnungsempfaenger = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Rechnungsempfaenger'), 'Rechnungsempfaenger', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Rechnungsempfaenger', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 319, 4), )

    
    Rechnungsempfaenger = property(__Rechnungsempfaenger.value, __Rechnungsempfaenger.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Grundeigentuemer uses Python identifier Grundeigentuemer
    __Grundeigentuemer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Grundeigentuemer'), 'Grundeigentuemer', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Grundeigentuemer', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 326, 4), )

    
    Grundeigentuemer = property(__Grundeigentuemer.value, __Grundeigentuemer.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}ausserhalb_Bauzone uses Python identifier ausserhalb_Bauzone
    __ausserhalb_Bauzone = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ausserhalb_Bauzone'), 'ausserhalb_Bauzone', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422ausserhalb_Bauzone', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 333, 4), )

    
    ausserhalb_Bauzone = property(__ausserhalb_Bauzone.value, __ausserhalb_Bauzone.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Bauprojekt uses Python identifier Bauprojekt
    __Bauprojekt = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Bauprojekt'), 'Bauprojekt', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Bauprojekt', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 334, 4), )

    
    Bauprojekt = property(__Bauprojekt.value, __Bauprojekt.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Grundstuecke uses Python identifier Grundstuecke
    __Grundstuecke = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Grundstuecke'), 'Grundstuecke', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Grundstuecke', True, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 341, 4), )

    
    Grundstuecke = property(__Grundstuecke.value, __Grundstuecke.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Entscheid_Leitbehoerde uses Python identifier Entscheid_Leitbehoerde
    __Entscheid_Leitbehoerde = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Entscheid_Leitbehoerde'), 'Entscheid_Leitbehoerde', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Entscheid_Leitbehoerde', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 348, 4), )

    
    Entscheid_Leitbehoerde = property(__Entscheid_Leitbehoerde.value, __Entscheid_Leitbehoerde.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Auflage uses Python identifier Auflage
    __Auflage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Auflage'), 'Auflage', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Auflage', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 355, 4), )

    
    Auflage = property(__Auflage.value, __Auflage.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Zirkulation uses Python identifier Zirkulation
    __Zirkulation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Zirkulation'), 'Zirkulation', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Zirkulation', True, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 362, 4), )

    
    Zirkulation = property(__Zirkulation.value, __Zirkulation.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Zustaendige_Personen uses Python identifier Zustaendige_Personen
    __Zustaendige_Personen = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Zustaendige_Personen'), 'Zustaendige_Personen', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Zustaendige_Personen', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 369, 4), )

    
    Zustaendige_Personen = property(__Zustaendige_Personen.value, __Zustaendige_Personen.set, None, None)

    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}eBau_Link uses Python identifier eBau_Link
    __eBau_Link = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eBau_Link'), 'eBau_Link', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422eBau_Link', False, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 376, 4), )

    
    eBau_Link = property(__eBau_Link.value, __eBau_Link.set, None, None)

    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}tid uses Python identifier tid
    __tid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'tid'), 'tid', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaeftType_httpwww_interlis_chxtf2_4INTERLIStid', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.tidType, required=True)
    __tid._DeclarationLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 17, 2)
    __tid._UseLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 384, 2)
    
    tid = property(__tid.value, __tid.set, None, None)

    _ElementMap.update({
        __Identifikator.name() : __Identifikator,
        __BFSNr.name() : __BFSNr,
        __Verfahrensart.name() : __Verfahrensart,
        __Geometrie_Punkt.name() : __Geometrie_Punkt,
        __Geometrie_Linie.name() : __Geometrie_Linie,
        __Geometrie_Flaeche.name() : __Geometrie_Flaeche,
        __Lokalisation.name() : __Lokalisation,
        __Status.name() : __Status,
        __Gesuchsteller.name() : __Gesuchsteller,
        __Projektverfasser.name() : __Projektverfasser,
        __Rechnungsempfaenger.name() : __Rechnungsempfaenger,
        __Grundeigentuemer.name() : __Grundeigentuemer,
        __ausserhalb_Bauzone.name() : __ausserhalb_Bauzone,
        __Bauprojekt.name() : __Bauprojekt,
        __Grundstuecke.name() : __Grundstuecke,
        __Entscheid_Leitbehoerde.name() : __Entscheid_Leitbehoerde,
        __Auflage.name() : __Auflage,
        __Zirkulation.name() : __Zirkulation,
        __Zustaendige_Personen.name() : __Zustaendige_Personen,
        __eBau_Link.name() : __eBau_Link
    })
    _AttributeMap.update({
        __tid.name() : __tid
    })
_module_typeBindings.GeschaeftType = GeschaeftType
Namespace.addCategoryObject('typeBinding', 'GeschaeftType', GeschaeftType)


# Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}GeschaefteType with content type ELEMENT_ONLY
class GeschaefteType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}GeschaefteType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GeschaefteType')
    _XSDLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 387, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.interlis.ch/xtf/2.4/SO_DSBJD_eBauSO_Geschaefte_20250422}Geschaeft uses Python identifier Geschaeft
    __Geschaeft = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Geschaeft'), 'Geschaeft', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaefteType_httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422Geschaeft', True, pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 269, 0), )

    
    Geschaeft = property(__Geschaeft.value, __Geschaeft.set, None, None)

    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}bid uses Python identifier bid
    __bid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'bid'), 'bid', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaefteType_httpwww_interlis_chxtf2_4INTERLISbid', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.bidType, required=True)
    __bid._DeclarationLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 21, 2)
    __bid._UseLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 391, 2)
    
    bid = property(__bid.value, __bid.set, None, None)

    
    # Attribute {http://www.interlis.ch/xtf/2.4/INTERLIS}consistency uses Python identifier consistency
    __consistency = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_INTERLIS, 'consistency'), 'consistency', '__httpwww_interlis_chxtf2_4SO_DSBJD_eBauSO_Geschaefte_20250422_GeschaefteType_httpwww_interlis_chxtf2_4INTERLISconsistency', _ImportedBinding_camac_gis_export_so_schema_INTERLIS.consistencyType)
    __consistency._DeclarationLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/INTERLIS.xsd', 22, 2)
    __consistency._UseLocation = pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 392, 2)
    
    consistency = property(__consistency.value, __consistency.set, None, None)

    _ElementMap.update({
        __Geschaeft.name() : __Geschaeft
    })
    _AttributeMap.update({
        __bid.name() : __bid,
        __consistency.name() : __consistency
    })
_module_typeBindings.GeschaefteType = GeschaefteType
Namespace.addCategoryObject('typeBinding', 'GeschaefteType', GeschaefteType)


Zustaendigkeit = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Zustaendigkeit'), ZustaendigkeitType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 33, 0))
Namespace.addCategoryObject('elementBinding', Zustaendigkeit.name().localName(), Zustaendigkeit)

Adresse = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Adresse_'), Adresse_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 53, 0))
Namespace.addCategoryObject('elementBinding', Adresse.name().localName(), Adresse)

Natuerliche_Person = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Natuerliche_Person'), Natuerliche_PersonType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 87, 0))
Namespace.addCategoryObject('elementBinding', Natuerliche_Person.name().localName(), Natuerliche_Person)

Juristische_Person = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Juristische_Person'), Juristische_PersonType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 106, 0))
Namespace.addCategoryObject('elementBinding', Juristische_Person.name().localName(), Juristische_Person)

PersonAdresse = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse'), PersonAdresseType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 118, 0))
Namespace.addCategoryObject('elementBinding', PersonAdresse.name().localName(), PersonAdresse)

Gesuchsteller = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Gesuchsteller_'), Gesuchsteller_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 144, 0))
Namespace.addCategoryObject('elementBinding', Gesuchsteller.name().localName(), Gesuchsteller)

Entscheid = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Entscheid_'), Entscheid_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 163, 0))
Namespace.addCategoryObject('elementBinding', Entscheid.name().localName(), Entscheid)

Auflage = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Auflage_'), Auflage_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 170, 0))
Namespace.addCategoryObject('elementBinding', Auflage.name().localName(), Auflage)

Grundstueck = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Grundstueck'), GrundstueckType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 177, 0))
Namespace.addCategoryObject('elementBinding', Grundstueck.name().localName(), Grundstueck)

Bauwerk = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Bauwerk'), BauwerkType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 196, 0))
Namespace.addCategoryObject('elementBinding', Bauwerk.name().localName(), Bauwerk)

Bauprojekt = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Bauprojekt_'), Bauprojekt_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 237, 0))
Namespace.addCategoryObject('elementBinding', Bauprojekt.name().localName(), Bauprojekt)

Geschaeft = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Geschaeft'), GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 269, 0))
Namespace.addCategoryObject('elementBinding', Geschaeft.name().localName(), Geschaeft)

Geschaefte = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Geschaefte'), GeschaefteType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 386, 0))
Namespace.addCategoryObject('elementBinding', Geschaefte.name().localName(), Geschaefte)



ZustaendigkeitType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Fachstelle'), Fachstellen, scope=ZustaendigkeitType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 36, 4)))

ZustaendigkeitType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Name'), STD_ANON, scope=ZustaendigkeitType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 37, 4)))

ZustaendigkeitType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Abteilung'), STD_ANON_, scope=ZustaendigkeitType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 44, 4)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 37, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 44, 4))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ZustaendigkeitType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Fachstelle')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 36, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ZustaendigkeitType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Name')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 37, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ZustaendigkeitType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Abteilung')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 44, 4))
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
ZustaendigkeitType._Automaton = _BuildAutomaton()




Adresse_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Strassenname'), STD_ANON_2, scope=Adresse_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 56, 4)))

Adresse_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Hausnummer'), STD_ANON_3, scope=Adresse_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 63, 4)))

Adresse_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PLZ'), STD_ANON_4, scope=Adresse_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 70, 4)))

Adresse_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Ortschaft'), STD_ANON_5, scope=Adresse_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 78, 4)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 56, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 63, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 70, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 78, 4))
    counters.add(cc_3)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Adresse_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Strassenname')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 56, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Adresse_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Hausnummer')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 63, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(Adresse_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PLZ')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 70, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(Adresse_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Ortschaft')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 78, 4))
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
Adresse_Type._Automaton = _BuildAutomaton_()




Natuerliche_PersonType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Name'), STD_ANON_6, scope=Natuerliche_PersonType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 90, 4)))

Natuerliche_PersonType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Vorname'), STD_ANON_7, scope=Natuerliche_PersonType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 97, 4)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 90, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 97, 4))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Natuerliche_PersonType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Name')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 90, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Natuerliche_PersonType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Vorname')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 97, 4))
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
Natuerliche_PersonType._Automaton = _BuildAutomaton_2()




Juristische_PersonType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Name'), STD_ANON_8, scope=Juristische_PersonType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 109, 4)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 109, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Juristische_PersonType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Name')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 109, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Juristische_PersonType._Automaton = _BuildAutomaton_3()




PersonAdresseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Natuerliche_Person'), CTD_ANON, scope=PersonAdresseType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 121, 4)))

PersonAdresseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Juristische_Person'), CTD_ANON_, scope=PersonAdresseType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 128, 4)))

PersonAdresseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Adresse'), CTD_ANON_2, scope=PersonAdresseType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 135, 4)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 128, 4))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(PersonAdresseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Natuerliche_Person')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 121, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(PersonAdresseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Juristische_Person')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 128, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(PersonAdresseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Adresse')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 135, 4))
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
PersonAdresseType._Automaton = _BuildAutomaton_4()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Natuerliche_Person'), Natuerliche_PersonType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 87, 0)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Natuerliche_Person')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 124, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_5()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Juristische_Person'), Juristische_PersonType, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 106, 0)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Juristische_Person')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 131, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_6()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Adresse_'), Adresse_Type, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 53, 0)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Adresse_')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 138, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_7()




Gesuchsteller_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Adresse'), CTD_ANON_3, scope=Gesuchsteller_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 147, 4)))

Gesuchsteller_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Vertretung'), CTD_ANON_4, scope=Gesuchsteller_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 154, 4)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 154, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Gesuchsteller_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Adresse')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 147, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Gesuchsteller_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Vertretung')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 154, 4))
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
Gesuchsteller_Type._Automaton = _BuildAutomaton_8()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse'), PersonAdresseType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 118, 0)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 150, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_9()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse'), PersonAdresseType, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 118, 0)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 157, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_4._Automaton = _BuildAutomaton_10()




Entscheid_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Entscheid'), Entscheid_, scope=Entscheid_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 166, 4)))

Entscheid_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Datum'), pyxb.binding.datatypes.date, scope=Entscheid_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 167, 4)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Entscheid_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Entscheid')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 166, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Entscheid_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Datum')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 167, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Entscheid_Type._Automaton = _BuildAutomaton_11()




Auflage_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Startdatum'), pyxb.binding.datatypes.date, scope=Auflage_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 173, 4)))

Auflage_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Enddatum'), pyxb.binding.datatypes.date, scope=Auflage_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 174, 4)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 173, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 174, 4))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Auflage_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Startdatum')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 173, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Auflage_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Enddatum')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 174, 4))
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
Auflage_Type._Automaton = _BuildAutomaton_12()




GrundstueckType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Nummer'), STD_ANON_9, scope=GrundstueckType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 180, 4)))

GrundstueckType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EGRID'), STD_ANON_10, scope=GrundstueckType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 187, 4)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GrundstueckType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Nummer')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 180, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(GrundstueckType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EGRID')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 187, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
GrundstueckType._Automaton = _BuildAutomaton_13()




BauwerkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Bezeichnung'), STD_ANON_11, scope=BauwerkType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 199, 4)))

BauwerkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Bauwerk_Typ'), STD_ANON_12, scope=BauwerkType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 206, 4)))

BauwerkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EGID'), STD_ANON_13, scope=BauwerkType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 213, 4)))

BauwerkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Arbeiten_Art'), STD_ANON_14, scope=BauwerkType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 221, 4)))

BauwerkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Gebaeudekategorie'), STD_ANON_15, scope=BauwerkType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 228, 4)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 213, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=1, max=3, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 221, 4))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BauwerkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Bezeichnung')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 199, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BauwerkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Bauwerk_Typ')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 206, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BauwerkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EGID')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 213, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BauwerkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Arbeiten_Art')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 221, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BauwerkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Gebaeudekategorie')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 228, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
BauwerkType._Automaton = _BuildAutomaton_14()




Bauprojekt_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Beschreibung'), STD_ANON_16, scope=Bauprojekt_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 240, 4)))

Bauprojekt_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Bauwerk_Art'), STD_ANON_17, scope=Bauprojekt_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 246, 4)))

Bauprojekt_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Nutzungszweck'), STD_ANON_18, scope=Bauprojekt_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 253, 4)))

Bauprojekt_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Bauwerke'), CTD_ANON_5, scope=Bauprojekt_Type, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 260, 4)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 240, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=2, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 246, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 253, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 260, 4))
    counters.add(cc_3)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Bauprojekt_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Beschreibung')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 240, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Bauprojekt_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Bauwerk_Art')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 246, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(Bauprojekt_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Nutzungszweck')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 253, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(Bauprojekt_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Bauwerke')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 260, 4))
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
Bauprojekt_Type._Automaton = _BuildAutomaton_15()




CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Bauwerk'), BauwerkType, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 196, 0)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Bauwerk')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 263, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_5._Automaton = _BuildAutomaton_16()




CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Adresse_'), Adresse_Type, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 53, 0)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Adresse_')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 300, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_6._Automaton = _BuildAutomaton_17()




CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Gesuchsteller_'), Gesuchsteller_Type, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 144, 0)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Gesuchsteller_')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 308, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_7._Automaton = _BuildAutomaton_18()




CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse'), PersonAdresseType, scope=CTD_ANON_8, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 118, 0)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 315, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_8._Automaton = _BuildAutomaton_19()




CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse'), PersonAdresseType, scope=CTD_ANON_9, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 118, 0)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 322, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_9._Automaton = _BuildAutomaton_20()




CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse'), PersonAdresseType, scope=CTD_ANON_10, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 118, 0)))

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PersonAdresse')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 329, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_10._Automaton = _BuildAutomaton_21()




CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Bauprojekt_'), Bauprojekt_Type, scope=CTD_ANON_11, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 237, 0)))

def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Bauprojekt_')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 337, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_11._Automaton = _BuildAutomaton_22()




CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Grundstueck'), GrundstueckType, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 177, 0)))

def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Grundstueck')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 344, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_12._Automaton = _BuildAutomaton_23()




CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Entscheid_'), Entscheid_Type, scope=CTD_ANON_13, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 163, 0)))

def _BuildAutomaton_24 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Entscheid_')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 351, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_13._Automaton = _BuildAutomaton_24()




CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Auflage_'), Auflage_Type, scope=CTD_ANON_14, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 170, 0)))

def _BuildAutomaton_25 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Auflage_')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 358, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_14._Automaton = _BuildAutomaton_25()




CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Zustaendigkeit'), ZustaendigkeitType, scope=CTD_ANON_15, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 33, 0)))

def _BuildAutomaton_26 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_26
    del _BuildAutomaton_26
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Zustaendigkeit')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 365, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_15._Automaton = _BuildAutomaton_26()




CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Zustaendigkeit'), ZustaendigkeitType, scope=CTD_ANON_16, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 33, 0)))

def _BuildAutomaton_27 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_27
    del _BuildAutomaton_27
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Zustaendigkeit')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 372, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_16._Automaton = _BuildAutomaton_27()




GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Identifikator'), STD_ANON_19, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 272, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BFSNr'), STD_ANON_20, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 279, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Verfahrensart'), STD_ANON_21, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 287, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Geometrie_Punkt'), _ImportedBinding_camac_gis_export_so_schema_GeometryCHLV95_V2.MultiPoint, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 294, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Geometrie_Linie'), _ImportedBinding_camac_gis_export_so_schema_GeometryCHLV95_V2.MultiLine, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 295, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Geometrie_Flaeche'), _ImportedBinding_camac_gis_export_so_schema_GeometryCHLV95_V2.MultiSurface, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 296, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Lokalisation'), CTD_ANON_6, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 297, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Status'), Status_Geschaeft, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 304, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Gesuchsteller'), CTD_ANON_7, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 305, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Projektverfasser'), CTD_ANON_8, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 312, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Rechnungsempfaenger'), CTD_ANON_9, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 319, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Grundeigentuemer'), CTD_ANON_10, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 326, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ausserhalb_Bauzone'), pyxb.binding.datatypes.boolean, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 333, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Bauprojekt'), CTD_ANON_11, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 334, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Grundstuecke'), CTD_ANON_12, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 341, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Entscheid_Leitbehoerde'), CTD_ANON_13, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 348, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Auflage'), CTD_ANON_14, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 355, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Zirkulation'), CTD_ANON_15, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 362, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Zustaendige_Personen'), CTD_ANON_16, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 369, 4)))

GeschaeftType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eBau_Link'), STD_ANON_22, scope=GeschaeftType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 376, 4)))

def _BuildAutomaton_28 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_28
    del _BuildAutomaton_28
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 294, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 295, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 296, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 297, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 312, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 319, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 326, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 333, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 334, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 348, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 355, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 362, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 369, 4))
    counters.add(cc_12)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Identifikator')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 272, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BFSNr')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 279, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Verfahrensart')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 287, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Geometrie_Punkt')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 294, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Geometrie_Linie')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 295, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Geometrie_Flaeche')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 296, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Lokalisation')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 297, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Status')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 304, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Gesuchsteller')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 305, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Projektverfasser')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 312, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Rechnungsempfaenger')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 319, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Grundeigentuemer')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 326, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ausserhalb_Bauzone')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 333, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Bauprojekt')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 334, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Grundstuecke')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 341, 4))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Entscheid_Leitbehoerde')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 348, 4))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Auflage')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 355, 4))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Zirkulation')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 362, 4))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Zustaendige_Personen')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 369, 4))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(GeschaeftType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eBau_Link')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 376, 4))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
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
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
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
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, True) ]))
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
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
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
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    st_19._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
GeschaeftType._Automaton = _BuildAutomaton_28()




GeschaefteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Geschaeft'), GeschaeftType, scope=GeschaefteType, location=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 269, 0)))

def _BuildAutomaton_29 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_29
    del _BuildAutomaton_29
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 388, 2))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(GeschaefteType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Geschaeft')), pyxb.utils.utility.Location('/home/susumo/projects/camac-ng/django/camac/gis_export/so_schema/xsd/SO_DSBJD_eBauSO_Geschaefte_20250422.xsd', 389, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
GeschaefteType._Automaton = _BuildAutomaton_29()

