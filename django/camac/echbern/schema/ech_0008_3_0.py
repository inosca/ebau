# ../../camac/echbern/schema/ech_0008_3_0.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:003955005781e1f27190a4b53818847e778e9a8c
# Generated 2019-09-26 17:57:08.876635 by PyXB version 1.2.6 using Python 3.6.8.final.0
# Namespace http://www.ech.ch/xmlns/eCH-0008/3 [xmlns:eCH-0008]

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
Namespace = pyxb.namespace.NamespaceForURI('http://www.ech.ch/xmlns/eCH-0008/3', create_if_missing=True)
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


# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0008/3}countryIdType
class countryIdType (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'countryIdType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 5, 1)
    _Documentation = None
countryIdType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=countryIdType, value=pyxb.binding.datatypes.integer(1000))
countryIdType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=countryIdType, value=pyxb.binding.datatypes.integer(9999))
countryIdType._InitializeFacetMap(countryIdType._CF_minInclusive,
   countryIdType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'countryIdType', countryIdType)
_module_typeBindings.countryIdType = countryIdType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0008/3}countryIdISO2Type
class countryIdISO2Type (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'countryIdISO2Type')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 11, 1)
    _Documentation = None
countryIdISO2Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(2))
countryIdISO2Type._InitializeFacetMap(countryIdISO2Type._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'countryIdISO2Type', countryIdISO2Type)
_module_typeBindings.countryIdISO2Type = countryIdISO2Type

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0008/3}countryNameShortType
class countryNameShortType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'countryNameShortType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 16, 1)
    _Documentation = None
countryNameShortType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(50))
countryNameShortType._InitializeFacetMap(countryNameShortType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'countryNameShortType', countryNameShortType)
_module_typeBindings.countryNameShortType = countryNameShortType

# Complex type {http://www.ech.ch/xmlns/eCH-0008/3}countryType with content type ELEMENT_ONLY
class countryType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0008/3}countryType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'countryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0008/3}countryId uses Python identifier countryId
    __countryId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'countryId'), 'countryId', '__httpwww_ech_chxmlnseCH_00083_countryType_httpwww_ech_chxmlnseCH_00083countryId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 23, 3), )

    
    countryId = property(__countryId.value, __countryId.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0008/3}countryIdISO2 uses Python identifier countryIdISO2
    __countryIdISO2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'countryIdISO2'), 'countryIdISO2', '__httpwww_ech_chxmlnseCH_00083_countryType_httpwww_ech_chxmlnseCH_00083countryIdISO2', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 24, 3), )

    
    countryIdISO2 = property(__countryIdISO2.value, __countryIdISO2.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0008/3}countryNameShort uses Python identifier countryNameShort
    __countryNameShort = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'countryNameShort'), 'countryNameShort', '__httpwww_ech_chxmlnseCH_00083_countryType_httpwww_ech_chxmlnseCH_00083countryNameShort', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 25, 3), )

    
    countryNameShort = property(__countryNameShort.value, __countryNameShort.set, None, None)

    _ElementMap.update({
        __countryId.name() : __countryId,
        __countryIdISO2.name() : __countryIdISO2,
        __countryNameShort.name() : __countryNameShort
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.countryType = countryType
Namespace.addCategoryObject('typeBinding', 'countryType', countryType)


# Complex type {http://www.ech.ch/xmlns/eCH-0008/3}countryShortType with content type ELEMENT_ONLY
class countryShortType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0008/3}countryShortType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'countryShortType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 28, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0008/3}countryNameShort uses Python identifier countryNameShort
    __countryNameShort = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'countryNameShort'), 'countryNameShort', '__httpwww_ech_chxmlnseCH_00083_countryShortType_httpwww_ech_chxmlnseCH_00083countryNameShort', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 30, 3), )

    
    countryNameShort = property(__countryNameShort.value, __countryNameShort.set, None, None)

    _ElementMap.update({
        __countryNameShort.name() : __countryNameShort
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.countryShortType = countryShortType
Namespace.addCategoryObject('typeBinding', 'countryShortType', countryShortType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 34, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0008/3}country uses Python identifier country
    __country = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'country'), 'country', '__httpwww_ech_chxmlnseCH_00083_CTD_ANON_httpwww_ech_chxmlnseCH_00083country', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 36, 4), )

    
    country = property(__country.value, __country.set, None, None)

    _ElementMap.update({
        __country.name() : __country
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


countryRoot = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'countryRoot'), CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 33, 1))
Namespace.addCategoryObject('elementBinding', countryRoot.name().localName(), countryRoot)



countryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'countryId'), countryIdType, scope=countryType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 23, 3)))

countryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'countryIdISO2'), countryIdISO2Type, scope=countryType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 24, 3)))

countryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'countryNameShort'), countryNameShortType, scope=countryType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 25, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 23, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 24, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(countryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'countryId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 23, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(countryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'countryIdISO2')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 24, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(countryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'countryNameShort')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 25, 3))
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
countryType._Automaton = _BuildAutomaton()




countryShortType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'countryNameShort'), countryNameShortType, scope=countryShortType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 30, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(countryShortType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'countryNameShort')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 30, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
countryShortType._Automaton = _BuildAutomaton_()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'country'), countryType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 36, 4)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'country')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0008_3_0.xsd', 36, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_2()

