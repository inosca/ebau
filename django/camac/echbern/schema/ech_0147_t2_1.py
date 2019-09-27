# ../../camac/echbern/schema/ech_0147_t2_1.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e77b27ecdd906e0a3541cc00d53e5306e1d65afd
# Generated 2019-09-26 17:57:08.877508 by PyXB version 1.2.6 using Python 3.6.8.final.0
# Namespace http://www.ech.ch/xmlns/eCH-0147/T2/1 [xmlns:eCH-0147T2]

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
import camac.echbern.schema.ech_0147_t0_1 as _ImportedBinding_camac_echbern_schema_ech_0147_t0_1
import camac.echbern.schema.ech_0039_2_0 as _ImportedBinding_camac_echbern_schema_ech_0039_2_0

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.ech.ch/xmlns/eCH-0147/T2/1', create_if_missing=True)
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


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T2/1}messageType with content type ELEMENT_ONLY
class messageType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0147/T2/1}messageType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'messageType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 29, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element header uses Python identifier header
    __header = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'header'), 'header', '__httpwww_ech_chxmlnseCH_0147T21_messageType_header', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 31, 3), )

    
    header = property(__header.value, __header.set, None, None)

    
    # Element content uses Python identifier content_
    __content = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'content'), 'content_', '__httpwww_ech_chxmlnseCH_0147T21_messageType_content', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 32, 3), )

    
    content_ = property(__content.value, __content.set, None, None)

    _ElementMap.update({
        __header.name() : __header,
        __content.name() : __content
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.messageType = messageType
Namespace.addCategoryObject('typeBinding', 'messageType', messageType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T2/1}contentType with content type ELEMENT_ONLY
class contentType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0147/T2/1}contentType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'contentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 35, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element directives uses Python identifier directives
    __directives = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'directives'), 'directives', '__httpwww_ech_chxmlnseCH_0147T21_contentType_directives', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 37, 3), )

    
    directives = property(__directives.value, __directives.set, None, None)

    _ElementMap.update({
        __directives.name() : __directives
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.contentType = contentType
Namespace.addCategoryObject('typeBinding', 'contentType', contentType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T2/1}directivesType with content type ELEMENT_ONLY
class directivesType (pyxb.binding.basis.complexTypeDefinition):
    """Anweisungen (mehrere): Eine Nachricht nach eCH-0147T2 enthält mindestens 2 Anweisungen. Enthält eine Nachricht nur eine oder keine Anweisung, so muss das Schema eCH-0039G1T1 benutzt werden. """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'directivesType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 40, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element directive uses Python identifier directive
    __directive = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'directive'), 'directive', '__httpwww_ech_chxmlnseCH_0147T21_directivesType_directive', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 45, 3), )

    
    directive = property(__directive.value, __directive.set, None, None)

    _ElementMap.update({
        __directive.name() : __directive
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.directivesType = directivesType
Namespace.addCategoryObject('typeBinding', 'directivesType', directivesType)


# Complex type {http://www.ech.ch/xmlns/eCH-0147/T2/1}directiveType with content type ELEMENT_ONLY
class directiveType (pyxb.binding.basis.complexTypeDefinition):
    """Anweisung: Basiskomponente zur Abbildung von Bearbeitungsanweisungen an den Empfänger muss an dieser Stelle definiert werden, da diese im Nachrichtentyp eCH-0147T2 um Dossiers, Dokumente und Adressen erweitert wird (Verschachtelung)"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'directiveType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 48, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'uuid'), 'uuid', '__httpwww_ech_chxmlnseCH_0147T21_directiveType_uuid', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 53, 3), )

    
    uuid = property(__uuid.value, __uuid.set, None, 'UUID: Universally Unique Identifier der Anweisung. Referenz des Objekts, nicht der Nachricht.')

    
    # Element instruction uses Python identifier instruction
    __instruction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'instruction'), 'instruction', '__httpwww_ech_chxmlnseCH_0147T21_directiveType_instruction', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 58, 3), )

    
    instruction = property(__instruction.value, __instruction.set, None, None)

    
    # Element priority uses Python identifier priority
    __priority = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'priority'), 'priority', '__httpwww_ech_chxmlnseCH_0147T21_directiveType_priority', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 59, 3), )

    
    priority = property(__priority.value, __priority.set, None, None)

    
    # Element titles uses Python identifier titles
    __titles = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'titles'), 'titles', '__httpwww_ech_chxmlnseCH_0147T21_directiveType_titles', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 60, 3), )

    
    titles = property(__titles.value, __titles.set, None, 'Titel: Benennung von Tätigkeit und Gegenstand des Geschäftsvorfalls.')

    
    # Element deadline uses Python identifier deadline
    __deadline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'deadline'), 'deadline', '__httpwww_ech_chxmlnseCH_0147T21_directiveType_deadline', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 65, 3), )

    
    deadline = property(__deadline.value, __deadline.set, None, 'Bearbeitungsfrist: Tag, an dem die Aktivität erledigt sein soll.')

    
    # Element serviceId uses Python identifier serviceId
    __serviceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'serviceId'), 'serviceId', '__httpwww_ech_chxmlnseCH_0147T21_directiveType_serviceId', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 70, 3), )

    
    serviceId = property(__serviceId.value, __serviceId.set, None, 'Leistungsidentifikation: Identifikation der Leistung gemäss eCH-0070 Leistungsinventar eGov CH.')

    
    # Element comments uses Python identifier comments
    __comments = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'comments'), 'comments', '__httpwww_ech_chxmlnseCH_0147T21_directiveType_comments', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 75, 3), )

    
    comments = property(__comments.value, __comments.set, None, None)

    
    # Element dossiers uses Python identifier dossiers
    __dossiers = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'dossiers'), 'dossiers', '__httpwww_ech_chxmlnseCH_0147T21_directiveType_dossiers', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 76, 3), )

    
    dossiers = property(__dossiers.value, __dossiers.set, None, None)

    
    # Element documents uses Python identifier documents
    __documents = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'documents'), 'documents', '__httpwww_ech_chxmlnseCH_0147T21_directiveType_documents', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 77, 3), )

    
    documents = property(__documents.value, __documents.set, None, None)

    
    # Element addresses uses Python identifier addresses
    __addresses = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'addresses'), 'addresses', '__httpwww_ech_chxmlnseCH_0147T21_directiveType_addresses', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 78, 3), )

    
    addresses = property(__addresses.value, __addresses.set, None, None)

    
    # Element applicationCustom uses Python identifier applicationCustom
    __applicationCustom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'applicationCustom'), 'applicationCustom', '__httpwww_ech_chxmlnseCH_0147T21_directiveType_applicationCustom', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 79, 3), )

    
    applicationCustom = property(__applicationCustom.value, __applicationCustom.set, None, None)

    _ElementMap.update({
        __uuid.name() : __uuid,
        __instruction.name() : __instruction,
        __priority.name() : __priority,
        __titles.name() : __titles,
        __deadline.name() : __deadline,
        __serviceId.name() : __serviceId,
        __comments.name() : __comments,
        __dossiers.name() : __dossiers,
        __documents.name() : __documents,
        __addresses.name() : __addresses,
        __applicationCustom.name() : __applicationCustom
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.directiveType = directiveType
Namespace.addCategoryObject('typeBinding', 'directiveType', directiveType)


header = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'header'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.headerType, documentation='Root-Element für header.xml einer Erstmeldung nach eCH-0147T2.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 9, 1))
Namespace.addCategoryObject('elementBinding', header.name().localName(), header)

message = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'message'), messageType, documentation='Root-Element für message.xml einer Erstmeldung nach eCH-0147T2.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 14, 1))
Namespace.addCategoryObject('elementBinding', message.name().localName(), message)

reportHeader = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reportHeader'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.reportHeaderType, documentation='Root-Element für header.xml einer Antwortmeldung nach eCH-0147T2.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 19, 1))
Namespace.addCategoryObject('elementBinding', reportHeader.name().localName(), reportHeader)

eventReport = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventReport'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.eventReportType, documentation='Root-Element für message.xml einer Antwortmeldung nach eCH-0147T2.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 24, 1))
Namespace.addCategoryObject('elementBinding', eventReport.name().localName(), eventReport)



messageType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'header'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.headerType, scope=messageType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 31, 3)))

messageType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'content'), contentType, scope=messageType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 32, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(messageType._UseForTag(pyxb.namespace.ExpandedName(None, 'header')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 31, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(messageType._UseForTag(pyxb.namespace.ExpandedName(None, 'content')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 32, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
messageType._Automaton = _BuildAutomaton()




contentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'directives'), directivesType, scope=contentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 37, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(contentType._UseForTag(pyxb.namespace.ExpandedName(None, 'directives')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 37, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
contentType._Automaton = _BuildAutomaton_()




directivesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'directive'), directiveType, scope=directivesType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 45, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=2, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 45, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(directivesType._UseForTag(pyxb.namespace.ExpandedName(None, 'directive')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 45, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
directivesType._Automaton = _BuildAutomaton_2()




directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'uuid'), pyxb.binding.datatypes.token, scope=directiveType, documentation='UUID: Universally Unique Identifier der Anweisung. Referenz des Objekts, nicht der Nachricht.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 53, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'instruction'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.directiveInstructionType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 58, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'priority'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.priorityType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 59, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'titles'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.titlesType, scope=directiveType, documentation='Titel: Benennung von Tätigkeit und Gegenstand des Geschäftsvorfalls.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 60, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'deadline'), pyxb.binding.datatypes.date, scope=directiveType, documentation='Bearbeitungsfrist: Tag, an dem die Aktivität erledigt sein soll.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 65, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'serviceId'), pyxb.binding.datatypes.token, scope=directiveType, documentation='Leistungsidentifikation: Identifikation der Leistung gemäss eCH-0070 Leistungsinventar eGov CH.', location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 70, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'comments'), _ImportedBinding_camac_echbern_schema_ech_0039_2_0.commentsType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 75, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'dossiers'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.dossiersType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 76, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'documents'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.documentsType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 77, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'addresses'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.addressesType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 78, 3)))

directiveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'applicationCustom'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.applicationCustomType, scope=directiveType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 79, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 60, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 65, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 70, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 75, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 76, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 77, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 78, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 79, 3))
    counters.add(cc_7)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(None, 'uuid')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 53, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(None, 'instruction')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 58, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(None, 'priority')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 59, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(None, 'titles')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 60, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(None, 'deadline')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 65, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(None, 'serviceId')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 70, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(None, 'comments')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 75, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(None, 'dossiers')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 76, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(None, 'documents')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 77, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(None, 'addresses')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 78, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(directiveType._UseForTag(pyxb.namespace.ExpandedName(None, 'applicationCustom')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0147_t2_1.xsd', 79, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
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
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
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
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_10, [
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
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
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
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_10._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
directiveType._Automaton = _BuildAutomaton_3()

