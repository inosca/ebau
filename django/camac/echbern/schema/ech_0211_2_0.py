# ../../camac/echbern/schema/ech_0211_2_0.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:64ee96ae3a6e19fc9b6d39daaa681abcdeacea3d
# Generated 2019-09-26 17:57:08.877847 by PyXB version 1.2.6 using Python 3.6.8.final.0
# Namespace http://www.ech.ch/xmlns/eCH-0211/2

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
import camac.echbern.schema.ech_0129_5_0 as _ImportedBinding_camac_echbern_schema_ech_0129_5_0
import camac.echbern.schema.ech_0007_6_0 as _ImportedBinding_camac_echbern_schema_ech_0007_6_0
import camac.echbern.schema.ech_0010_6_0 as _ImportedBinding_camac_echbern_schema_ech_0010_6_0
import camac.echbern.schema.ech_0147_t2_1 as _ImportedBinding_camac_echbern_schema_ech_0147_t2_1
import camac.echbern.schema.ech_0147_t0_1 as _ImportedBinding_camac_echbern_schema_ech_0147_t0_1
import camac.echbern.schema.ech_0097_2_0 as _ImportedBinding_camac_echbern_schema_ech_0097_2_0
import camac.echbern.schema.ech_0044_4_1 as _ImportedBinding_camac_echbern_schema_ech_0044_4_1
import camac.echbern.schema.ech_0058_5_0 as _ImportedBinding_camac_echbern_schema_ech_0058_5_0

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.ech.ch/xmlns/eCH-0211/2', create_if_missing=True)
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


# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0211/2}eventTypeType
class eventTypeType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventTypeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 13, 1)
    _Documentation = None
eventTypeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=eventTypeType, enum_prefix=None)
eventTypeType.submit = eventTypeType._CF_enumeration.addEnumeration(unicode_value='submit', tag='submit')
eventTypeType.file_subsequently = eventTypeType._CF_enumeration.addEnumeration(unicode_value='file subsequently', tag='file_subsequently')
eventTypeType.applicant_request = eventTypeType._CF_enumeration.addEnumeration(unicode_value='applicant request', tag='applicant_request')
eventTypeType.withdraw_planning_permission_application = eventTypeType._CF_enumeration.addEnumeration(unicode_value='withdraw planning permission application', tag='withdraw_planning_permission_application')
eventTypeType.claim = eventTypeType._CF_enumeration.addEnumeration(unicode_value='claim', tag='claim')
eventTypeType.task = eventTypeType._CF_enumeration.addEnumeration(unicode_value='task', tag='task')
eventTypeType.notice_ruling = eventTypeType._CF_enumeration.addEnumeration(unicode_value='notice ruling', tag='notice_ruling')
eventTypeType.status_notification = eventTypeType._CF_enumeration.addEnumeration(unicode_value='status notification', tag='status_notification')
eventTypeType.close_dossier = eventTypeType._CF_enumeration.addEnumeration(unicode_value='close dossier', tag='close_dossier')
eventTypeType.archive_dossier = eventTypeType._CF_enumeration.addEnumeration(unicode_value='archive dossier', tag='archive_dossier')
eventTypeType.notice_involved_party = eventTypeType._CF_enumeration.addEnumeration(unicode_value='notice involved party', tag='notice_involved_party')
eventTypeType.notice_kind_of_proceedings = eventTypeType._CF_enumeration.addEnumeration(unicode_value='notice kind of proceedings', tag='notice_kind_of_proceedings')
eventTypeType.change_contact = eventTypeType._CF_enumeration.addEnumeration(unicode_value='change contact', tag='change_contact')
eventTypeType.accompanying_report = eventTypeType._CF_enumeration.addEnumeration(unicode_value='accompanying report', tag='accompanying_report')
eventTypeType.change_responsibility = eventTypeType._CF_enumeration.addEnumeration(unicode_value='change responsibility', tag='change_responsibility')
eventTypeType._InitializeFacetMap(eventTypeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'eventTypeType', eventTypeType)
_module_typeBindings.eventTypeType = eventTypeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0211/2}remarkType
class remarkType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'remarkType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 32, 1)
    _Documentation = None
remarkType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
remarkType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(1000))
remarkType._InitializeFacetMap(remarkType._CF_minLength,
   remarkType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'remarkType', remarkType)
_module_typeBindings.remarkType = remarkType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0211/2}descriptionType
class descriptionType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'descriptionType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 38, 1)
    _Documentation = None
descriptionType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
descriptionType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(1000))
descriptionType._InitializeFacetMap(descriptionType._CF_minLength,
   descriptionType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'descriptionType', descriptionType)
_module_typeBindings.descriptionType = descriptionType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0211/2}applicationTypeType
class applicationTypeType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'applicationTypeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 44, 1)
    _Documentation = None
applicationTypeType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
applicationTypeType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
applicationTypeType._InitializeFacetMap(applicationTypeType._CF_minLength,
   applicationTypeType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'applicationTypeType', applicationTypeType)
_module_typeBindings.applicationTypeType = applicationTypeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0211/2}proceedingTypeType
class proceedingTypeType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'proceedingTypeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 50, 1)
    _Documentation = None
proceedingTypeType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
proceedingTypeType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
proceedingTypeType._InitializeFacetMap(proceedingTypeType._CF_minLength,
   proceedingTypeType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'proceedingTypeType', proceedingTypeType)
_module_typeBindings.proceedingTypeType = proceedingTypeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0211/2}intendedPurposeType
class intendedPurposeType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'intendedPurposeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 56, 1)
    _Documentation = None
intendedPurposeType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
intendedPurposeType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(255))
intendedPurposeType._InitializeFacetMap(intendedPurposeType._CF_minLength,
   intendedPurposeType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'intendedPurposeType', intendedPurposeType)
_module_typeBindings.intendedPurposeType = intendedPurposeType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0211/2}dossierIdentificationType
class dossierIdentificationType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dossierIdentificationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 62, 1)
    _Documentation = None
dossierIdentificationType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
dossierIdentificationType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(255))
dossierIdentificationType._InitializeFacetMap(dossierIdentificationType._CF_minLength,
   dossierIdentificationType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'dossierIdentificationType', dossierIdentificationType)
_module_typeBindings.dossierIdentificationType = dossierIdentificationType

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0211/2}judgementType
class judgementType (pyxb.binding.datatypes.nonNegativeInteger, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'judgementType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 68, 1)
    _Documentation = None
judgementType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=judgementType, enum_prefix=None)
judgementType._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
judgementType._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
judgementType._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
judgementType._CF_enumeration.addEnumeration(unicode_value='4', tag=None)
judgementType._InitializeFacetMap(judgementType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'judgementType', judgementType)
_module_typeBindings.judgementType = judgementType

# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 79, 4)
    _Documentation = None
STD_ANON._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(255))
STD_ANON._InitializeFacetMap(STD_ANON._CF_minLength,
   STD_ANON._CF_maxLength)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 96, 5)
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.CH = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='CH', tag='CH')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationStatusType
class planningPermissionApplicationStatusType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationStatusType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 105, 1)
    _Documentation = None
planningPermissionApplicationStatusType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=planningPermissionApplicationStatusType, enum_prefix=None)
planningPermissionApplicationStatusType.submitted = planningPermissionApplicationStatusType._CF_enumeration.addEnumeration(unicode_value='submitted', tag='submitted')
planningPermissionApplicationStatusType.in_progress = planningPermissionApplicationStatusType._CF_enumeration.addEnumeration(unicode_value='in progress', tag='in_progress')
planningPermissionApplicationStatusType.withdrawn = planningPermissionApplicationStatusType._CF_enumeration.addEnumeration(unicode_value='withdrawn', tag='withdrawn')
planningPermissionApplicationStatusType.suspended = planningPermissionApplicationStatusType._CF_enumeration.addEnumeration(unicode_value='suspended', tag='suspended')
planningPermissionApplicationStatusType.appellant_process = planningPermissionApplicationStatusType._CF_enumeration.addEnumeration(unicode_value='appellant process', tag='appellant_process')
planningPermissionApplicationStatusType.objection_pending = planningPermissionApplicationStatusType._CF_enumeration.addEnumeration(unicode_value='objection pending', tag='objection_pending')
planningPermissionApplicationStatusType.decision_issued = planningPermissionApplicationStatusType._CF_enumeration.addEnumeration(unicode_value='decision issued', tag='decision_issued')
planningPermissionApplicationStatusType.decision_legally_binding = planningPermissionApplicationStatusType._CF_enumeration.addEnumeration(unicode_value='decision legally binding', tag='decision_legally_binding')
planningPermissionApplicationStatusType.building_freeze = planningPermissionApplicationStatusType._CF_enumeration.addEnumeration(unicode_value='building freeze', tag='building_freeze')
planningPermissionApplicationStatusType.under_construction = planningPermissionApplicationStatusType._CF_enumeration.addEnumeration(unicode_value='under construction', tag='under_construction')
planningPermissionApplicationStatusType.building_clearance = planningPermissionApplicationStatusType._CF_enumeration.addEnumeration(unicode_value='building clearance', tag='building_clearance')
planningPermissionApplicationStatusType.dossier_closed = planningPermissionApplicationStatusType._CF_enumeration.addEnumeration(unicode_value='dossier closed', tag='dossier_closed')
planningPermissionApplicationStatusType.dossier_archived = planningPermissionApplicationStatusType._CF_enumeration.addEnumeration(unicode_value='dossier archived', tag='dossier_archived')
planningPermissionApplicationStatusType._InitializeFacetMap(planningPermissionApplicationStatusType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'planningPermissionApplicationStatusType', planningPermissionApplicationStatusType)
_module_typeBindings.planningPermissionApplicationStatusType = planningPermissionApplicationStatusType

# Atomic simple type: [anonymous]
class STD_ANON_2 (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 142, 4)
    _Documentation = None
STD_ANON_2._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(12))
STD_ANON_2._CF_fractionDigits = pyxb.binding.facets.CF_fractionDigits(value=pyxb.binding.datatypes.nonNegativeInteger(2))
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_totalDigits,
   STD_ANON_2._CF_fractionDigits)
_module_typeBindings.STD_ANON_2 = STD_ANON_2

# Atomic simple type: [anonymous]
class STD_ANON_3 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 164, 4)
    _Documentation = None
STD_ANON_3._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON_3._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(255))
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_minLength,
   STD_ANON_3._CF_maxLength)
_module_typeBindings.STD_ANON_3 = STD_ANON_3

# Atomic simple type: [anonymous]
class STD_ANON_4 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 179, 4)
    _Documentation = None
STD_ANON_4._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON_4._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(25))
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_minLength,
   STD_ANON_4._CF_maxLength)
_module_typeBindings.STD_ANON_4 = STD_ANON_4

# Atomic simple type: [anonymous]
class STD_ANON_5 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 187, 4)
    _Documentation = None
STD_ANON_5._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON_5._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(255))
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_minLength,
   STD_ANON_5._CF_maxLength)
_module_typeBindings.STD_ANON_5 = STD_ANON_5

# Atomic simple type: [anonymous]
class STD_ANON_6 (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 195, 4)
    _Documentation = None
STD_ANON_6._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
STD_ANON_6._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(255))
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_minLength,
   STD_ANON_6._CF_maxLength)
_module_typeBindings.STD_ANON_6 = STD_ANON_6

# Atomic simple type: {http://www.ech.ch/xmlns/eCH-0211/2}roleType
class roleType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'roleType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 229, 1)
    _Documentation = None
roleType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
roleType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
roleType._InitializeFacetMap(roleType._CF_minLength,
   roleType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'roleType', roleType)
_module_typeBindings.roleType = roleType

# Atomic simple type: [anonymous]
class STD_ANON_7 (eventTypeType, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 291, 4)
    _Documentation = None
STD_ANON_7._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_7, enum_prefix=None)
STD_ANON_7.submit = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value='submit', tag='submit')
STD_ANON_7.file_subsequently = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value='file subsequently', tag='file_subsequently')
STD_ANON_7._InitializeFacetMap(STD_ANON_7._CF_enumeration)
_module_typeBindings.STD_ANON_7 = STD_ANON_7

# Atomic simple type: [anonymous]
class STD_ANON_8 (eventTypeType, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 306, 4)
    _Documentation = None
STD_ANON_8._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_8, enum_prefix=None)
STD_ANON_8.change_contact = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value='change contact', tag='change_contact')
STD_ANON_8._InitializeFacetMap(STD_ANON_8._CF_enumeration)
_module_typeBindings.STD_ANON_8 = STD_ANON_8

# Atomic simple type: [anonymous]
class STD_ANON_9 (eventTypeType, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 322, 4)
    _Documentation = None
STD_ANON_9._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_9, enum_prefix=None)
STD_ANON_9.applicant_request = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='applicant request', tag='applicant_request')
STD_ANON_9.withdraw_planning_permission_application = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='withdraw planning permission application', tag='withdraw_planning_permission_application')
STD_ANON_9.claim = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='claim', tag='claim')
STD_ANON_9.task = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='task', tag='task')
STD_ANON_9._InitializeFacetMap(STD_ANON_9._CF_enumeration)
_module_typeBindings.STD_ANON_9 = STD_ANON_9

# Atomic simple type: [anonymous]
class STD_ANON_10 (eventTypeType, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 341, 4)
    _Documentation = None
STD_ANON_10._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_10, enum_prefix=None)
STD_ANON_10.accompanying_report = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value='accompanying report', tag='accompanying_report')
STD_ANON_10._InitializeFacetMap(STD_ANON_10._CF_enumeration)
_module_typeBindings.STD_ANON_10 = STD_ANON_10

# Atomic simple type: [anonymous]
class STD_ANON_11 (eventTypeType, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 359, 4)
    _Documentation = None
STD_ANON_11._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_11, enum_prefix=None)
STD_ANON_11.close_dossier = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='close dossier', tag='close_dossier')
STD_ANON_11.archive_dossier = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='archive dossier', tag='archive_dossier')
STD_ANON_11._InitializeFacetMap(STD_ANON_11._CF_enumeration)
_module_typeBindings.STD_ANON_11 = STD_ANON_11

# Atomic simple type: [anonymous]
class STD_ANON_12 (eventTypeType, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 374, 4)
    _Documentation = None
STD_ANON_12._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_12, enum_prefix=None)
STD_ANON_12.notice_kind_of_proceedings = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value='notice kind of proceedings', tag='notice_kind_of_proceedings')
STD_ANON_12._InitializeFacetMap(STD_ANON_12._CF_enumeration)
_module_typeBindings.STD_ANON_12 = STD_ANON_12

# Atomic simple type: [anonymous]
class STD_ANON_13 (eventTypeType, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 389, 4)
    _Documentation = None
STD_ANON_13._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_13, enum_prefix=None)
STD_ANON_13.notice_involved_party = STD_ANON_13._CF_enumeration.addEnumeration(unicode_value='notice involved party', tag='notice_involved_party')
STD_ANON_13._InitializeFacetMap(STD_ANON_13._CF_enumeration)
_module_typeBindings.STD_ANON_13 = STD_ANON_13

# Atomic simple type: [anonymous]
class STD_ANON_14 (eventTypeType, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 407, 4)
    _Documentation = None
STD_ANON_14._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_14, enum_prefix=None)
STD_ANON_14.notice_ruling = STD_ANON_14._CF_enumeration.addEnumeration(unicode_value='notice ruling', tag='notice_ruling')
STD_ANON_14._InitializeFacetMap(STD_ANON_14._CF_enumeration)
_module_typeBindings.STD_ANON_14 = STD_ANON_14

# Atomic simple type: [anonymous]
class STD_ANON_15 (eventTypeType, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 423, 4)
    _Documentation = None
STD_ANON_15._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_15, enum_prefix=None)
STD_ANON_15.change_responsibility = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value='change responsibility', tag='change_responsibility')
STD_ANON_15._InitializeFacetMap(STD_ANON_15._CF_enumeration)
_module_typeBindings.STD_ANON_15 = STD_ANON_15

# Atomic simple type: [anonymous]
class STD_ANON_16 (eventTypeType, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 439, 4)
    _Documentation = None
STD_ANON_16._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_16, enum_prefix=None)
STD_ANON_16.status_notification = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value='status notification', tag='status_notification')
STD_ANON_16._InitializeFacetMap(STD_ANON_16._CF_enumeration)
_module_typeBindings.STD_ANON_16 = STD_ANON_16

# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}natureRiskType with content type ELEMENT_ONLY
class natureRiskType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}natureRiskType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'natureRiskType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 76, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}riskDesignation uses Python identifier riskDesignation
    __riskDesignation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'riskDesignation'), 'riskDesignation', '__httpwww_ech_chxmlnseCH_02112_natureRiskType_httpwww_ech_chxmlnseCH_02112riskDesignation', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 78, 3), )

    
    riskDesignation = property(__riskDesignation.value, __riskDesignation.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}riskExists uses Python identifier riskExists
    __riskExists = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'riskExists'), 'riskExists', '__httpwww_ech_chxmlnseCH_02112_natureRiskType_httpwww_ech_chxmlnseCH_02112riskExists', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 86, 3), )

    
    riskExists = property(__riskExists.value, __riskExists.set, None, None)

    _ElementMap.update({
        __riskDesignation.name() : __riskDesignation,
        __riskExists.name() : __riskExists
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.natureRiskType = natureRiskType
Namespace.addCategoryObject('typeBinding', 'natureRiskType', natureRiskType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}constructionProjectInformationType with content type ELEMENT_ONLY
class constructionProjectInformationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}constructionProjectInformationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'constructionProjectInformationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 89, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}constructionProject uses Python identifier constructionProject
    __constructionProject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'constructionProject'), 'constructionProject', '__httpwww_ech_chxmlnseCH_02112_constructionProjectInformationType_httpwww_ech_chxmlnseCH_02112constructionProject', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 91, 3), )

    
    constructionProject = property(__constructionProject.value, __constructionProject.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}municipality uses Python identifier municipality
    __municipality = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'municipality'), 'municipality', '__httpwww_ech_chxmlnseCH_02112_constructionProjectInformationType_httpwww_ech_chxmlnseCH_02112municipality', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 93, 4), )

    
    municipality = property(__municipality.value, __municipality.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}canton uses Python identifier canton
    __canton = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'canton'), 'canton', '__httpwww_ech_chxmlnseCH_02112_constructionProjectInformationType_httpwww_ech_chxmlnseCH_02112canton', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 94, 4), )

    
    canton = property(__canton.value, __canton.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}confederation uses Python identifier confederation
    __confederation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'confederation'), 'confederation', '__httpwww_ech_chxmlnseCH_02112_constructionProjectInformationType_httpwww_ech_chxmlnseCH_02112confederation', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 95, 4), )

    
    confederation = property(__confederation.value, __confederation.set, None, None)

    _ElementMap.update({
        __constructionProject.name() : __constructionProject,
        __municipality.name() : __municipality,
        __canton.name() : __canton,
        __confederation.name() : __confederation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.constructionProjectInformationType = constructionProjectInformationType
Namespace.addCategoryObject('typeBinding', 'constructionProjectInformationType', constructionProjectInformationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationIdentificationType with content type ELEMENT_ONLY
class planningPermissionApplicationIdentificationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationIdentificationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentificationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 122, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'localID'), 'localID', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationIdentificationType_httpwww_ech_chxmlnseCH_02112localID', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 124, 3), )

    
    localID = property(__localID.value, __localID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}otherID uses Python identifier otherID
    __otherID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherID'), 'otherID', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationIdentificationType_httpwww_ech_chxmlnseCH_02112otherID', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 125, 3), )

    
    otherID = property(__otherID.value, __otherID.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}dossierIdentification uses Python identifier dossierIdentification
    __dossierIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dossierIdentification'), 'dossierIdentification', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationIdentificationType_httpwww_ech_chxmlnseCH_02112dossierIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 126, 3), )

    
    dossierIdentification = property(__dossierIdentification.value, __dossierIdentification.set, None, None)

    _ElementMap.update({
        __localID.name() : __localID,
        __otherID.name() : __otherID,
        __dossierIdentification.name() : __dossierIdentification
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.planningPermissionApplicationIdentificationType = planningPermissionApplicationIdentificationType
Namespace.addCategoryObject('typeBinding', 'planningPermissionApplicationIdentificationType', planningPermissionApplicationIdentificationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationType with content type ELEMENT_ONLY
class planningPermissionApplicationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 129, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationIdentification uses Python identifier planningPermissionApplicationIdentification
    __planningPermissionApplicationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), 'planningPermissionApplicationIdentification', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112planningPermissionApplicationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 131, 3), )

    
    planningPermissionApplicationIdentification = property(__planningPermissionApplicationIdentification.value, __planningPermissionApplicationIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112description', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 132, 3), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}applicationType uses Python identifier applicationType
    __applicationType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'applicationType'), 'applicationType', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112applicationType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 133, 3), )

    
    applicationType = property(__applicationType.value, __applicationType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}remark uses Python identifier remark
    __remark = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remark'), 'remark', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112remark', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 134, 3), )

    
    remark = property(__remark.value, __remark.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}proceedingType uses Python identifier proceedingType
    __proceedingType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'proceedingType'), 'proceedingType', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112proceedingType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 135, 3), )

    
    proceedingType = property(__proceedingType.value, __proceedingType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}profilingYesNo uses Python identifier profilingYesNo
    __profilingYesNo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'profilingYesNo'), 'profilingYesNo', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112profilingYesNo', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 136, 3), )

    
    profilingYesNo = property(__profilingYesNo.value, __profilingYesNo.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}profilingDate uses Python identifier profilingDate
    __profilingDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'profilingDate'), 'profilingDate', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112profilingDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 137, 3), )

    
    profilingDate = property(__profilingDate.value, __profilingDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}intendedPurpose uses Python identifier intendedPurpose
    __intendedPurpose = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'intendedPurpose'), 'intendedPurpose', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112intendedPurpose', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 138, 3), )

    
    intendedPurpose = property(__intendedPurpose.value, __intendedPurpose.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}parkingLotsYesNo uses Python identifier parkingLotsYesNo
    __parkingLotsYesNo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'parkingLotsYesNo'), 'parkingLotsYesNo', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112parkingLotsYesNo', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 139, 3), )

    
    parkingLotsYesNo = property(__parkingLotsYesNo.value, __parkingLotsYesNo.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}natureRisk uses Python identifier natureRisk
    __natureRisk = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'natureRisk'), 'natureRisk', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112natureRisk', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 140, 3), )

    
    natureRisk = property(__natureRisk.value, __natureRisk.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}constructionCost uses Python identifier constructionCost
    __constructionCost = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'constructionCost'), 'constructionCost', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112constructionCost', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 141, 3), )

    
    constructionCost = property(__constructionCost.value, __constructionCost.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}publication uses Python identifier publication
    __publication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'publication'), 'publication', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112publication', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 149, 3), )

    
    publication = property(__publication.value, __publication.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}namedMetaData uses Python identifier namedMetaData
    __namedMetaData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'namedMetaData'), 'namedMetaData', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112namedMetaData', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 150, 3), )

    
    namedMetaData = property(__namedMetaData.value, __namedMetaData.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}locationAddress uses Python identifier locationAddress
    __locationAddress = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'locationAddress'), 'locationAddress', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112locationAddress', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 151, 3), )

    
    locationAddress = property(__locationAddress.value, __locationAddress.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}realestateInformation uses Python identifier realestateInformation
    __realestateInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'realestateInformation'), 'realestateInformation', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112realestateInformation', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 152, 3), )

    
    realestateInformation = property(__realestateInformation.value, __realestateInformation.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}zone uses Python identifier zone
    __zone = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'zone'), 'zone', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112zone', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 153, 3), )

    
    zone = property(__zone.value, __zone.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}constructionProjectInformation uses Python identifier constructionProjectInformation
    __constructionProjectInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'constructionProjectInformation'), 'constructionProjectInformation', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112constructionProjectInformation', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 154, 3), )

    
    constructionProjectInformation = property(__constructionProjectInformation.value, __constructionProjectInformation.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}directive uses Python identifier directive
    __directive = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'directive'), 'directive', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112directive', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 155, 3), )

    
    directive = property(__directive.value, __directive.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}decisionRuling uses Python identifier decisionRuling
    __decisionRuling = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'decisionRuling'), 'decisionRuling', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112decisionRuling', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 156, 3), )

    
    decisionRuling = property(__decisionRuling.value, __decisionRuling.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}document uses Python identifier document
    __document = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'document'), 'document', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112document', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 157, 3), )

    
    document = property(__document.value, __document.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}referencedPlanningPermissionApplication uses Python identifier referencedPlanningPermissionApplication
    __referencedPlanningPermissionApplication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'referencedPlanningPermissionApplication'), 'referencedPlanningPermissionApplication', '__httpwww_ech_chxmlnseCH_02112_planningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112referencedPlanningPermissionApplication', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 158, 3), )

    
    referencedPlanningPermissionApplication = property(__referencedPlanningPermissionApplication.value, __referencedPlanningPermissionApplication.set, None, None)

    _ElementMap.update({
        __planningPermissionApplicationIdentification.name() : __planningPermissionApplicationIdentification,
        __description.name() : __description,
        __applicationType.name() : __applicationType,
        __remark.name() : __remark,
        __proceedingType.name() : __proceedingType,
        __profilingYesNo.name() : __profilingYesNo,
        __profilingDate.name() : __profilingDate,
        __intendedPurpose.name() : __intendedPurpose,
        __parkingLotsYesNo.name() : __parkingLotsYesNo,
        __natureRisk.name() : __natureRisk,
        __constructionCost.name() : __constructionCost,
        __publication.name() : __publication,
        __namedMetaData.name() : __namedMetaData,
        __locationAddress.name() : __locationAddress,
        __realestateInformation.name() : __realestateInformation,
        __zone.name() : __zone,
        __constructionProjectInformation.name() : __constructionProjectInformation,
        __directive.name() : __directive,
        __decisionRuling.name() : __decisionRuling,
        __document.name() : __document,
        __referencedPlanningPermissionApplication.name() : __referencedPlanningPermissionApplication
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.planningPermissionApplicationType = planningPermissionApplicationType
Namespace.addCategoryObject('typeBinding', 'planningPermissionApplicationType', planningPermissionApplicationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}publicationType with content type ELEMENT_ONLY
class publicationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}publicationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'publicationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 161, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}officialGazette uses Python identifier officialGazette
    __officialGazette = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'officialGazette'), 'officialGazette', '__httpwww_ech_chxmlnseCH_02112_publicationType_httpwww_ech_chxmlnseCH_02112officialGazette', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 163, 3), )

    
    officialGazette = property(__officialGazette.value, __officialGazette.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}publicationText uses Python identifier publicationText
    __publicationText = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'publicationText'), 'publicationText', '__httpwww_ech_chxmlnseCH_02112_publicationType_httpwww_ech_chxmlnseCH_02112publicationText', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 171, 3), )

    
    publicationText = property(__publicationText.value, __publicationText.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}publicationDate uses Python identifier publicationDate
    __publicationDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'publicationDate'), 'publicationDate', '__httpwww_ech_chxmlnseCH_02112_publicationType_httpwww_ech_chxmlnseCH_02112publicationDate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 172, 3), )

    
    publicationDate = property(__publicationDate.value, __publicationDate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}publicationTill uses Python identifier publicationTill
    __publicationTill = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'publicationTill'), 'publicationTill', '__httpwww_ech_chxmlnseCH_02112_publicationType_httpwww_ech_chxmlnseCH_02112publicationTill', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 173, 3), )

    
    publicationTill = property(__publicationTill.value, __publicationTill.set, None, None)

    _ElementMap.update({
        __officialGazette.name() : __officialGazette,
        __publicationText.name() : __publicationText,
        __publicationDate.name() : __publicationDate,
        __publicationTill.name() : __publicationTill
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.publicationType = publicationType
Namespace.addCategoryObject('typeBinding', 'publicationType', publicationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}zoneType with content type ELEMENT_ONLY
class zoneType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}zoneType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'zoneType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 176, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}abbreviatedDesignation uses Python identifier abbreviatedDesignation
    __abbreviatedDesignation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'abbreviatedDesignation'), 'abbreviatedDesignation', '__httpwww_ech_chxmlnseCH_02112_zoneType_httpwww_ech_chxmlnseCH_02112abbreviatedDesignation', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 178, 3), )

    
    abbreviatedDesignation = property(__abbreviatedDesignation.value, __abbreviatedDesignation.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}zoneDesignation uses Python identifier zoneDesignation
    __zoneDesignation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'zoneDesignation'), 'zoneDesignation', '__httpwww_ech_chxmlnseCH_02112_zoneType_httpwww_ech_chxmlnseCH_02112zoneDesignation', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 186, 3), )

    
    zoneDesignation = property(__zoneDesignation.value, __zoneDesignation.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}zoneType uses Python identifier zoneType
    __zoneType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'zoneType'), 'zoneType', '__httpwww_ech_chxmlnseCH_02112_zoneType_httpwww_ech_chxmlnseCH_02112zoneType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 194, 3), )

    
    zoneType = property(__zoneType.value, __zoneType.set, None, None)

    _ElementMap.update({
        __abbreviatedDesignation.name() : __abbreviatedDesignation,
        __zoneDesignation.name() : __zoneDesignation,
        __zoneType.name() : __zoneType
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.zoneType = zoneType
Namespace.addCategoryObject('typeBinding', 'zoneType', zoneType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}decisionRulingType with content type ELEMENT_ONLY
class decisionRulingType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}decisionRulingType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'decisionRulingType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 204, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}judgement uses Python identifier judgement
    __judgement = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'judgement'), 'judgement', '__httpwww_ech_chxmlnseCH_02112_decisionRulingType_httpwww_ech_chxmlnseCH_02112judgement', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 206, 3), )

    
    judgement = property(__judgement.value, __judgement.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}ruling uses Python identifier ruling
    __ruling = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ruling'), 'ruling', '__httpwww_ech_chxmlnseCH_02112_decisionRulingType_httpwww_ech_chxmlnseCH_02112ruling', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 207, 3), )

    
    ruling = property(__ruling.value, __ruling.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}date uses Python identifier date
    __date = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'date'), 'date', '__httpwww_ech_chxmlnseCH_02112_decisionRulingType_httpwww_ech_chxmlnseCH_02112date', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 208, 3), )

    
    date = property(__date.value, __date.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}rulingAuthority uses Python identifier rulingAuthority
    __rulingAuthority = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'rulingAuthority'), 'rulingAuthority', '__httpwww_ech_chxmlnseCH_02112_decisionRulingType_httpwww_ech_chxmlnseCH_02112rulingAuthority', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 209, 3), )

    
    rulingAuthority = property(__rulingAuthority.value, __rulingAuthority.set, None, None)

    _ElementMap.update({
        __judgement.name() : __judgement,
        __ruling.name() : __ruling,
        __date.name() : __date,
        __rulingAuthority.name() : __rulingAuthority
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.decisionRulingType = decisionRulingType
Namespace.addCategoryObject('typeBinding', 'decisionRulingType', decisionRulingType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}decisionAuthorityInformationType with content type ELEMENT_ONLY
class decisionAuthorityInformationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}decisionAuthorityInformationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'decisionAuthorityInformationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 212, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}decisionAuthority uses Python identifier decisionAuthority
    __decisionAuthority = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'decisionAuthority'), 'decisionAuthority', '__httpwww_ech_chxmlnseCH_02112_decisionAuthorityInformationType_httpwww_ech_chxmlnseCH_02112decisionAuthority', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 214, 3), )

    
    decisionAuthority = property(__decisionAuthority.value, __decisionAuthority.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}municipality uses Python identifier municipality
    __municipality = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'municipality'), 'municipality', '__httpwww_ech_chxmlnseCH_02112_decisionAuthorityInformationType_httpwww_ech_chxmlnseCH_02112municipality', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 215, 3), )

    
    municipality = property(__municipality.value, __municipality.set, None, None)

    _ElementMap.update({
        __decisionAuthority.name() : __decisionAuthority,
        __municipality.name() : __municipality
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.decisionAuthorityInformationType = decisionAuthorityInformationType
Namespace.addCategoryObject('typeBinding', 'decisionAuthorityInformationType', decisionAuthorityInformationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}entryOfficeType with content type ELEMENT_ONLY
class entryOfficeType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}entryOfficeType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'entryOfficeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 218, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}entryOfficeIdentification uses Python identifier entryOfficeIdentification
    __entryOfficeIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'entryOfficeIdentification'), 'entryOfficeIdentification', '__httpwww_ech_chxmlnseCH_02112_entryOfficeType_httpwww_ech_chxmlnseCH_02112entryOfficeIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 220, 3), )

    
    entryOfficeIdentification = property(__entryOfficeIdentification.value, __entryOfficeIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}municipality uses Python identifier municipality
    __municipality = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'municipality'), 'municipality', '__httpwww_ech_chxmlnseCH_02112_entryOfficeType_httpwww_ech_chxmlnseCH_02112municipality', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 221, 3), )

    
    municipality = property(__municipality.value, __municipality.set, None, None)

    _ElementMap.update({
        __entryOfficeIdentification.name() : __entryOfficeIdentification,
        __municipality.name() : __municipality
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.entryOfficeType = entryOfficeType
Namespace.addCategoryObject('typeBinding', 'entryOfficeType', entryOfficeType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}specialistDepartmentType with content type ELEMENT_ONLY
class specialistDepartmentType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}specialistDepartmentType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'specialistDepartmentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 224, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}specialistDepartmentIdentification uses Python identifier specialistDepartmentIdentification
    __specialistDepartmentIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'specialistDepartmentIdentification'), 'specialistDepartmentIdentification', '__httpwww_ech_chxmlnseCH_02112_specialistDepartmentType_httpwww_ech_chxmlnseCH_02112specialistDepartmentIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 226, 3), )

    
    specialistDepartmentIdentification = property(__specialistDepartmentIdentification.value, __specialistDepartmentIdentification.set, None, None)

    _ElementMap.update({
        __specialistDepartmentIdentification.name() : __specialistDepartmentIdentification
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.specialistDepartmentType = specialistDepartmentType
Namespace.addCategoryObject('typeBinding', 'specialistDepartmentType', specialistDepartmentType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}relationshipToPersonType with content type ELEMENT_ONLY
class relationshipToPersonType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}relationshipToPersonType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'relationshipToPersonType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 235, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}role uses Python identifier role
    __role = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'role'), 'role', '__httpwww_ech_chxmlnseCH_02112_relationshipToPersonType_httpwww_ech_chxmlnseCH_02112role', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 237, 3), )

    
    role = property(__role.value, __role.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}person uses Python identifier person
    __person = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'person'), 'person', '__httpwww_ech_chxmlnseCH_02112_relationshipToPersonType_httpwww_ech_chxmlnseCH_02112person', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 238, 3), )

    
    person = property(__person.value, __person.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}deputy uses Python identifier deputy
    __deputy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'deputy'), 'deputy', '__httpwww_ech_chxmlnseCH_02112_relationshipToPersonType_httpwww_ech_chxmlnseCH_02112deputy', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 239, 3), )

    
    deputy = property(__deputy.value, __deputy.set, None, None)

    _ElementMap.update({
        __role.name() : __role,
        __person.name() : __person,
        __deputy.name() : __deputy
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.relationshipToPersonType = relationshipToPersonType
Namespace.addCategoryObject('typeBinding', 'relationshipToPersonType', relationshipToPersonType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}realestateInformationType with content type ELEMENT_ONLY
class realestateInformationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}realestateInformationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'realestateInformationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 242, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}realestate uses Python identifier realestate
    __realestate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'realestate'), 'realestate', '__httpwww_ech_chxmlnseCH_02112_realestateInformationType_httpwww_ech_chxmlnseCH_02112realestate', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 244, 3), )

    
    realestate = property(__realestate.value, __realestate.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}municipality uses Python identifier municipality
    __municipality = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'municipality'), 'municipality', '__httpwww_ech_chxmlnseCH_02112_realestateInformationType_httpwww_ech_chxmlnseCH_02112municipality', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 245, 3), )

    
    municipality = property(__municipality.value, __municipality.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}buildingInformation uses Python identifier buildingInformation
    __buildingInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'buildingInformation'), 'buildingInformation', '__httpwww_ech_chxmlnseCH_02112_realestateInformationType_httpwww_ech_chxmlnseCH_02112buildingInformation', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 246, 3), )

    
    buildingInformation = property(__buildingInformation.value, __buildingInformation.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}placeName uses Python identifier placeName
    __placeName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'placeName'), 'placeName', '__httpwww_ech_chxmlnseCH_02112_realestateInformationType_httpwww_ech_chxmlnseCH_02112placeName', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 247, 3), )

    
    placeName = property(__placeName.value, __placeName.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}owner uses Python identifier owner
    __owner = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'owner'), 'owner', '__httpwww_ech_chxmlnseCH_02112_realestateInformationType_httpwww_ech_chxmlnseCH_02112owner', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 248, 3), )

    
    owner = property(__owner.value, __owner.set, None, None)

    _ElementMap.update({
        __realestate.name() : __realestate,
        __municipality.name() : __municipality,
        __buildingInformation.name() : __buildingInformation,
        __placeName.name() : __placeName,
        __owner.name() : __owner
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.realestateInformationType = realestateInformationType
Namespace.addCategoryObject('typeBinding', 'realestateInformationType', realestateInformationType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 249, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}ownerIdentification uses Python identifier ownerIdentification
    __ownerIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ownerIdentification'), 'ownerIdentification', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_httpwww_ech_chxmlnseCH_02112ownerIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 251, 6), )

    
    ownerIdentification = property(__ownerIdentification.value, __ownerIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}ownerAdress uses Python identifier ownerAdress
    __ownerAdress = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ownerAdress'), 'ownerAdress', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_httpwww_ech_chxmlnseCH_02112ownerAdress', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 259, 6), )

    
    ownerAdress = property(__ownerAdress.value, __ownerAdress.set, None, None)

    _ElementMap.update({
        __ownerIdentification.name() : __ownerIdentification,
        __ownerAdress.name() : __ownerAdress
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
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 252, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}personIdentification uses Python identifier personIdentification
    __personIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'personIdentification'), 'personIdentification', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON__httpwww_ech_chxmlnseCH_02112personIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 254, 9), )

    
    personIdentification = property(__personIdentification.value, __personIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}organisationIdentification uses Python identifier organisationIdentification
    __organisationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification'), 'organisationIdentification', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON__httpwww_ech_chxmlnseCH_02112organisationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 255, 9), )

    
    organisationIdentification = property(__organisationIdentification.value, __organisationIdentification.set, None, None)

    _ElementMap.update({
        __personIdentification.name() : __personIdentification,
        __organisationIdentification.name() : __organisationIdentification
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}buildingInformationType with content type ELEMENT_ONLY
class buildingInformationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}buildingInformationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'buildingInformationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 265, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}building uses Python identifier building
    __building = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'building'), 'building', '__httpwww_ech_chxmlnseCH_02112_buildingInformationType_httpwww_ech_chxmlnseCH_02112building', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 267, 3), )

    
    building = property(__building.value, __building.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}dwelling uses Python identifier dwelling
    __dwelling = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dwelling'), 'dwelling', '__httpwww_ech_chxmlnseCH_02112_buildingInformationType_httpwww_ech_chxmlnseCH_02112dwelling', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 268, 3), )

    
    dwelling = property(__dwelling.value, __dwelling.set, None, None)

    _ElementMap.update({
        __building.name() : __building,
        __dwelling.name() : __dwelling
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.buildingInformationType = buildingInformationType
Namespace.addCategoryObject('typeBinding', 'buildingInformationType', buildingInformationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventBaseDeliveryType with content type ELEMENT_ONLY
class eventBaseDeliveryType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventBaseDeliveryType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventBaseDeliveryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 271, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationInformation uses Python identifier planningPermissionApplicationInformation
    __planningPermissionApplicationInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationInformation'), 'planningPermissionApplicationInformation', '__httpwww_ech_chxmlnseCH_02112_eventBaseDeliveryType_httpwww_ech_chxmlnseCH_02112planningPermissionApplicationInformation', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 273, 3), )

    
    planningPermissionApplicationInformation = property(__planningPermissionApplicationInformation.value, __planningPermissionApplicationInformation.set, None, None)

    _ElementMap.update({
        __planningPermissionApplicationInformation.name() : __planningPermissionApplicationInformation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventBaseDeliveryType = eventBaseDeliveryType
Namespace.addCategoryObject('typeBinding', 'eventBaseDeliveryType', eventBaseDeliveryType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 274, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplication uses Python identifier planningPermissionApplication
    __planningPermissionApplication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplication'), 'planningPermissionApplication', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_2_httpwww_ech_chxmlnseCH_02112planningPermissionApplication', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 276, 6), )

    
    planningPermissionApplication = property(__planningPermissionApplication.value, __planningPermissionApplication.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}relationshipToPerson uses Python identifier relationshipToPerson
    __relationshipToPerson = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relationshipToPerson'), 'relationshipToPerson', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_2_httpwww_ech_chxmlnseCH_02112relationshipToPerson', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 277, 6), )

    
    relationshipToPerson = property(__relationshipToPerson.value, __relationshipToPerson.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}decisionAuthority uses Python identifier decisionAuthority
    __decisionAuthority = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'decisionAuthority'), 'decisionAuthority', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_2_httpwww_ech_chxmlnseCH_02112decisionAuthority', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 278, 6), )

    
    decisionAuthority = property(__decisionAuthority.value, __decisionAuthority.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}entryOffice uses Python identifier entryOffice
    __entryOffice = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'entryOffice'), 'entryOffice', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_2_httpwww_ech_chxmlnseCH_02112entryOffice', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 279, 6), )

    
    entryOffice = property(__entryOffice.value, __entryOffice.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}specialistDepartment uses Python identifier specialistDepartment
    __specialistDepartment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'specialistDepartment'), 'specialistDepartment', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_2_httpwww_ech_chxmlnseCH_02112specialistDepartment', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 280, 6), )

    
    specialistDepartment = property(__specialistDepartment.value, __specialistDepartment.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}document uses Python identifier document
    __document = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'document'), 'document', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_2_httpwww_ech_chxmlnseCH_02112document', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 281, 6), )

    
    document = property(__document.value, __document.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_2_httpwww_ech_chxmlnseCH_02112extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 282, 6), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __planningPermissionApplication.name() : __planningPermissionApplication,
        __relationshipToPerson.name() : __relationshipToPerson,
        __decisionAuthority.name() : __decisionAuthority,
        __entryOffice.name() : __entryOffice,
        __specialistDepartment.name() : __specialistDepartment,
        __document.name() : __document,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventSubmitPlanningPermissionApplicationType with content type ELEMENT_ONLY
class eventSubmitPlanningPermissionApplicationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventSubmitPlanningPermissionApplicationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventSubmitPlanningPermissionApplicationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 288, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventType uses Python identifier eventType
    __eventType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventType'), 'eventType', '__httpwww_ech_chxmlnseCH_02112_eventSubmitPlanningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112eventType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 290, 3), )

    
    eventType = property(__eventType.value, __eventType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplication uses Python identifier planningPermissionApplication
    __planningPermissionApplication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplication'), 'planningPermissionApplication', '__httpwww_ech_chxmlnseCH_02112_eventSubmitPlanningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112planningPermissionApplication', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 298, 3), )

    
    planningPermissionApplication = property(__planningPermissionApplication.value, __planningPermissionApplication.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}relationshipToPerson uses Python identifier relationshipToPerson
    __relationshipToPerson = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relationshipToPerson'), 'relationshipToPerson', '__httpwww_ech_chxmlnseCH_02112_eventSubmitPlanningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112relationshipToPerson', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 299, 3), )

    
    relationshipToPerson = property(__relationshipToPerson.value, __relationshipToPerson.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_02112_eventSubmitPlanningPermissionApplicationType_httpwww_ech_chxmlnseCH_02112extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 300, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __eventType.name() : __eventType,
        __planningPermissionApplication.name() : __planningPermissionApplication,
        __relationshipToPerson.name() : __relationshipToPerson,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventSubmitPlanningPermissionApplicationType = eventSubmitPlanningPermissionApplicationType
Namespace.addCategoryObject('typeBinding', 'eventSubmitPlanningPermissionApplicationType', eventSubmitPlanningPermissionApplicationType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventChangeContactType with content type ELEMENT_ONLY
class eventChangeContactType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventChangeContactType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventChangeContactType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 303, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventType uses Python identifier eventType
    __eventType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventType'), 'eventType', '__httpwww_ech_chxmlnseCH_02112_eventChangeContactType_httpwww_ech_chxmlnseCH_02112eventType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 305, 3), )

    
    eventType = property(__eventType.value, __eventType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationIdentification uses Python identifier planningPermissionApplicationIdentification
    __planningPermissionApplicationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), 'planningPermissionApplicationIdentification', '__httpwww_ech_chxmlnseCH_02112_eventChangeContactType_httpwww_ech_chxmlnseCH_02112planningPermissionApplicationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 312, 3), )

    
    planningPermissionApplicationIdentification = property(__planningPermissionApplicationIdentification.value, __planningPermissionApplicationIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}directive uses Python identifier directive
    __directive = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'directive'), 'directive', '__httpwww_ech_chxmlnseCH_02112_eventChangeContactType_httpwww_ech_chxmlnseCH_02112directive', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 313, 3), )

    
    directive = property(__directive.value, __directive.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}relationshipToPerson uses Python identifier relationshipToPerson
    __relationshipToPerson = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relationshipToPerson'), 'relationshipToPerson', '__httpwww_ech_chxmlnseCH_02112_eventChangeContactType_httpwww_ech_chxmlnseCH_02112relationshipToPerson', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 314, 3), )

    
    relationshipToPerson = property(__relationshipToPerson.value, __relationshipToPerson.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}remark uses Python identifier remark
    __remark = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remark'), 'remark', '__httpwww_ech_chxmlnseCH_02112_eventChangeContactType_httpwww_ech_chxmlnseCH_02112remark', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 315, 3), )

    
    remark = property(__remark.value, __remark.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_02112_eventChangeContactType_httpwww_ech_chxmlnseCH_02112extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 316, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __eventType.name() : __eventType,
        __planningPermissionApplicationIdentification.name() : __planningPermissionApplicationIdentification,
        __directive.name() : __directive,
        __relationshipToPerson.name() : __relationshipToPerson,
        __remark.name() : __remark,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventChangeContactType = eventChangeContactType
Namespace.addCategoryObject('typeBinding', 'eventChangeContactType', eventChangeContactType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventRequestType with content type ELEMENT_ONLY
class eventRequestType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventRequestType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventRequestType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 319, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventType uses Python identifier eventType
    __eventType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventType'), 'eventType', '__httpwww_ech_chxmlnseCH_02112_eventRequestType_httpwww_ech_chxmlnseCH_02112eventType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 321, 3), )

    
    eventType = property(__eventType.value, __eventType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationIdentification uses Python identifier planningPermissionApplicationIdentification
    __planningPermissionApplicationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), 'planningPermissionApplicationIdentification', '__httpwww_ech_chxmlnseCH_02112_eventRequestType_httpwww_ech_chxmlnseCH_02112planningPermissionApplicationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 331, 3), )

    
    planningPermissionApplicationIdentification = property(__planningPermissionApplicationIdentification.value, __planningPermissionApplicationIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}directive uses Python identifier directive
    __directive = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'directive'), 'directive', '__httpwww_ech_chxmlnseCH_02112_eventRequestType_httpwww_ech_chxmlnseCH_02112directive', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 332, 3), )

    
    directive = property(__directive.value, __directive.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}document uses Python identifier document
    __document = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'document'), 'document', '__httpwww_ech_chxmlnseCH_02112_eventRequestType_httpwww_ech_chxmlnseCH_02112document', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 333, 3), )

    
    document = property(__document.value, __document.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}remark uses Python identifier remark
    __remark = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remark'), 'remark', '__httpwww_ech_chxmlnseCH_02112_eventRequestType_httpwww_ech_chxmlnseCH_02112remark', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 334, 3), )

    
    remark = property(__remark.value, __remark.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_02112_eventRequestType_httpwww_ech_chxmlnseCH_02112extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 335, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __eventType.name() : __eventType,
        __planningPermissionApplicationIdentification.name() : __planningPermissionApplicationIdentification,
        __directive.name() : __directive,
        __document.name() : __document,
        __remark.name() : __remark,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventRequestType = eventRequestType
Namespace.addCategoryObject('typeBinding', 'eventRequestType', eventRequestType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventAccompanyingReportType with content type ELEMENT_ONLY
class eventAccompanyingReportType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventAccompanyingReportType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventAccompanyingReportType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 338, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventType uses Python identifier eventType
    __eventType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventType'), 'eventType', '__httpwww_ech_chxmlnseCH_02112_eventAccompanyingReportType_httpwww_ech_chxmlnseCH_02112eventType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 340, 3), )

    
    eventType = property(__eventType.value, __eventType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}judgement uses Python identifier judgement
    __judgement = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'judgement'), 'judgement', '__httpwww_ech_chxmlnseCH_02112_eventAccompanyingReportType_httpwww_ech_chxmlnseCH_02112judgement', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 347, 3), )

    
    judgement = property(__judgement.value, __judgement.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationIdentification uses Python identifier planningPermissionApplicationIdentification
    __planningPermissionApplicationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), 'planningPermissionApplicationIdentification', '__httpwww_ech_chxmlnseCH_02112_eventAccompanyingReportType_httpwww_ech_chxmlnseCH_02112planningPermissionApplicationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 348, 3), )

    
    planningPermissionApplicationIdentification = property(__planningPermissionApplicationIdentification.value, __planningPermissionApplicationIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}directive uses Python identifier directive
    __directive = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'directive'), 'directive', '__httpwww_ech_chxmlnseCH_02112_eventAccompanyingReportType_httpwww_ech_chxmlnseCH_02112directive', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 349, 3), )

    
    directive = property(__directive.value, __directive.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}document uses Python identifier document
    __document = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'document'), 'document', '__httpwww_ech_chxmlnseCH_02112_eventAccompanyingReportType_httpwww_ech_chxmlnseCH_02112document', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 350, 3), )

    
    document = property(__document.value, __document.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}remark uses Python identifier remark
    __remark = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remark'), 'remark', '__httpwww_ech_chxmlnseCH_02112_eventAccompanyingReportType_httpwww_ech_chxmlnseCH_02112remark', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 351, 3), )

    
    remark = property(__remark.value, __remark.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}ancillaryClauses uses Python identifier ancillaryClauses
    __ancillaryClauses = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ancillaryClauses'), 'ancillaryClauses', '__httpwww_ech_chxmlnseCH_02112_eventAccompanyingReportType_httpwww_ech_chxmlnseCH_02112ancillaryClauses', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 352, 3), )

    
    ancillaryClauses = property(__ancillaryClauses.value, __ancillaryClauses.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_02112_eventAccompanyingReportType_httpwww_ech_chxmlnseCH_02112extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 353, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __eventType.name() : __eventType,
        __judgement.name() : __judgement,
        __planningPermissionApplicationIdentification.name() : __planningPermissionApplicationIdentification,
        __directive.name() : __directive,
        __document.name() : __document,
        __remark.name() : __remark,
        __ancillaryClauses.name() : __ancillaryClauses,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventAccompanyingReportType = eventAccompanyingReportType
Namespace.addCategoryObject('typeBinding', 'eventAccompanyingReportType', eventAccompanyingReportType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventCloseArchiveDossierType with content type ELEMENT_ONLY
class eventCloseArchiveDossierType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventCloseArchiveDossierType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventCloseArchiveDossierType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 356, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventType uses Python identifier eventType
    __eventType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventType'), 'eventType', '__httpwww_ech_chxmlnseCH_02112_eventCloseArchiveDossierType_httpwww_ech_chxmlnseCH_02112eventType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 358, 3), )

    
    eventType = property(__eventType.value, __eventType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationIdentification uses Python identifier planningPermissionApplicationIdentification
    __planningPermissionApplicationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), 'planningPermissionApplicationIdentification', '__httpwww_ech_chxmlnseCH_02112_eventCloseArchiveDossierType_httpwww_ech_chxmlnseCH_02112planningPermissionApplicationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 366, 3), )

    
    planningPermissionApplicationIdentification = property(__planningPermissionApplicationIdentification.value, __planningPermissionApplicationIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}remark uses Python identifier remark
    __remark = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remark'), 'remark', '__httpwww_ech_chxmlnseCH_02112_eventCloseArchiveDossierType_httpwww_ech_chxmlnseCH_02112remark', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 367, 3), )

    
    remark = property(__remark.value, __remark.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_02112_eventCloseArchiveDossierType_httpwww_ech_chxmlnseCH_02112extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 368, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __eventType.name() : __eventType,
        __planningPermissionApplicationIdentification.name() : __planningPermissionApplicationIdentification,
        __remark.name() : __remark,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventCloseArchiveDossierType = eventCloseArchiveDossierType
Namespace.addCategoryObject('typeBinding', 'eventCloseArchiveDossierType', eventCloseArchiveDossierType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventKindOfProceedingsType with content type ELEMENT_ONLY
class eventKindOfProceedingsType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventKindOfProceedingsType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventKindOfProceedingsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 371, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventType uses Python identifier eventType
    __eventType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventType'), 'eventType', '__httpwww_ech_chxmlnseCH_02112_eventKindOfProceedingsType_httpwww_ech_chxmlnseCH_02112eventType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 373, 3), )

    
    eventType = property(__eventType.value, __eventType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationIdentification uses Python identifier planningPermissionApplicationIdentification
    __planningPermissionApplicationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), 'planningPermissionApplicationIdentification', '__httpwww_ech_chxmlnseCH_02112_eventKindOfProceedingsType_httpwww_ech_chxmlnseCH_02112planningPermissionApplicationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 380, 3), )

    
    planningPermissionApplicationIdentification = property(__planningPermissionApplicationIdentification.value, __planningPermissionApplicationIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}document uses Python identifier document
    __document = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'document'), 'document', '__httpwww_ech_chxmlnseCH_02112_eventKindOfProceedingsType_httpwww_ech_chxmlnseCH_02112document', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 381, 3), )

    
    document = property(__document.value, __document.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}remark uses Python identifier remark
    __remark = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remark'), 'remark', '__httpwww_ech_chxmlnseCH_02112_eventKindOfProceedingsType_httpwww_ech_chxmlnseCH_02112remark', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 382, 3), )

    
    remark = property(__remark.value, __remark.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_02112_eventKindOfProceedingsType_httpwww_ech_chxmlnseCH_02112extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 383, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __eventType.name() : __eventType,
        __planningPermissionApplicationIdentification.name() : __planningPermissionApplicationIdentification,
        __document.name() : __document,
        __remark.name() : __remark,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventKindOfProceedingsType = eventKindOfProceedingsType
Namespace.addCategoryObject('typeBinding', 'eventKindOfProceedingsType', eventKindOfProceedingsType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventNoticeInvolvedPartyType with content type ELEMENT_ONLY
class eventNoticeInvolvedPartyType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventNoticeInvolvedPartyType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventNoticeInvolvedPartyType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 386, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventType uses Python identifier eventType
    __eventType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventType'), 'eventType', '__httpwww_ech_chxmlnseCH_02112_eventNoticeInvolvedPartyType_httpwww_ech_chxmlnseCH_02112eventType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 388, 3), )

    
    eventType = property(__eventType.value, __eventType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationIdentification uses Python identifier planningPermissionApplicationIdentification
    __planningPermissionApplicationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), 'planningPermissionApplicationIdentification', '__httpwww_ech_chxmlnseCH_02112_eventNoticeInvolvedPartyType_httpwww_ech_chxmlnseCH_02112planningPermissionApplicationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 395, 3), )

    
    planningPermissionApplicationIdentification = property(__planningPermissionApplicationIdentification.value, __planningPermissionApplicationIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}decisionAuthority uses Python identifier decisionAuthority
    __decisionAuthority = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'decisionAuthority'), 'decisionAuthority', '__httpwww_ech_chxmlnseCH_02112_eventNoticeInvolvedPartyType_httpwww_ech_chxmlnseCH_02112decisionAuthority', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 396, 3), )

    
    decisionAuthority = property(__decisionAuthority.value, __decisionAuthority.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}entryOffice uses Python identifier entryOffice
    __entryOffice = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'entryOffice'), 'entryOffice', '__httpwww_ech_chxmlnseCH_02112_eventNoticeInvolvedPartyType_httpwww_ech_chxmlnseCH_02112entryOffice', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 397, 3), )

    
    entryOffice = property(__entryOffice.value, __entryOffice.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}specialistDepartment uses Python identifier specialistDepartment
    __specialistDepartment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'specialistDepartment'), 'specialistDepartment', '__httpwww_ech_chxmlnseCH_02112_eventNoticeInvolvedPartyType_httpwww_ech_chxmlnseCH_02112specialistDepartment', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 398, 3), )

    
    specialistDepartment = property(__specialistDepartment.value, __specialistDepartment.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}remark uses Python identifier remark
    __remark = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remark'), 'remark', '__httpwww_ech_chxmlnseCH_02112_eventNoticeInvolvedPartyType_httpwww_ech_chxmlnseCH_02112remark', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 399, 3), )

    
    remark = property(__remark.value, __remark.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}document uses Python identifier document
    __document = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'document'), 'document', '__httpwww_ech_chxmlnseCH_02112_eventNoticeInvolvedPartyType_httpwww_ech_chxmlnseCH_02112document', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 400, 3), )

    
    document = property(__document.value, __document.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_02112_eventNoticeInvolvedPartyType_httpwww_ech_chxmlnseCH_02112extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 401, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __eventType.name() : __eventType,
        __planningPermissionApplicationIdentification.name() : __planningPermissionApplicationIdentification,
        __decisionAuthority.name() : __decisionAuthority,
        __entryOffice.name() : __entryOffice,
        __specialistDepartment.name() : __specialistDepartment,
        __remark.name() : __remark,
        __document.name() : __document,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventNoticeInvolvedPartyType = eventNoticeInvolvedPartyType
Namespace.addCategoryObject('typeBinding', 'eventNoticeInvolvedPartyType', eventNoticeInvolvedPartyType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventNoticeType with content type ELEMENT_ONLY
class eventNoticeType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventNoticeType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventNoticeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 404, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventType uses Python identifier eventType
    __eventType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventType'), 'eventType', '__httpwww_ech_chxmlnseCH_02112_eventNoticeType_httpwww_ech_chxmlnseCH_02112eventType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 406, 3), )

    
    eventType = property(__eventType.value, __eventType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationIdentification uses Python identifier planningPermissionApplicationIdentification
    __planningPermissionApplicationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), 'planningPermissionApplicationIdentification', '__httpwww_ech_chxmlnseCH_02112_eventNoticeType_httpwww_ech_chxmlnseCH_02112planningPermissionApplicationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 413, 3), )

    
    planningPermissionApplicationIdentification = property(__planningPermissionApplicationIdentification.value, __planningPermissionApplicationIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}decisionRuling uses Python identifier decisionRuling
    __decisionRuling = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'decisionRuling'), 'decisionRuling', '__httpwww_ech_chxmlnseCH_02112_eventNoticeType_httpwww_ech_chxmlnseCH_02112decisionRuling', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 414, 3), )

    
    decisionRuling = property(__decisionRuling.value, __decisionRuling.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}document uses Python identifier document
    __document = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'document'), 'document', '__httpwww_ech_chxmlnseCH_02112_eventNoticeType_httpwww_ech_chxmlnseCH_02112document', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 415, 3), )

    
    document = property(__document.value, __document.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}remark uses Python identifier remark
    __remark = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remark'), 'remark', '__httpwww_ech_chxmlnseCH_02112_eventNoticeType_httpwww_ech_chxmlnseCH_02112remark', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 416, 3), )

    
    remark = property(__remark.value, __remark.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_02112_eventNoticeType_httpwww_ech_chxmlnseCH_02112extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 417, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __eventType.name() : __eventType,
        __planningPermissionApplicationIdentification.name() : __planningPermissionApplicationIdentification,
        __decisionRuling.name() : __decisionRuling,
        __document.name() : __document,
        __remark.name() : __remark,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventNoticeType = eventNoticeType
Namespace.addCategoryObject('typeBinding', 'eventNoticeType', eventNoticeType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventChangeResponsibilityType with content type ELEMENT_ONLY
class eventChangeResponsibilityType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventChangeResponsibilityType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventChangeResponsibilityType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 420, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventType uses Python identifier eventType
    __eventType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventType'), 'eventType', '__httpwww_ech_chxmlnseCH_02112_eventChangeResponsibilityType_httpwww_ech_chxmlnseCH_02112eventType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 422, 3), )

    
    eventType = property(__eventType.value, __eventType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationIdentification uses Python identifier planningPermissionApplicationIdentification
    __planningPermissionApplicationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), 'planningPermissionApplicationIdentification', '__httpwww_ech_chxmlnseCH_02112_eventChangeResponsibilityType_httpwww_ech_chxmlnseCH_02112planningPermissionApplicationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 429, 3), )

    
    planningPermissionApplicationIdentification = property(__planningPermissionApplicationIdentification.value, __planningPermissionApplicationIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}entryOffice uses Python identifier entryOffice
    __entryOffice = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'entryOffice'), 'entryOffice', '__httpwww_ech_chxmlnseCH_02112_eventChangeResponsibilityType_httpwww_ech_chxmlnseCH_02112entryOffice', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 430, 3), )

    
    entryOffice = property(__entryOffice.value, __entryOffice.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}responsibleDecisionAuthority uses Python identifier responsibleDecisionAuthority
    __responsibleDecisionAuthority = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'responsibleDecisionAuthority'), 'responsibleDecisionAuthority', '__httpwww_ech_chxmlnseCH_02112_eventChangeResponsibilityType_httpwww_ech_chxmlnseCH_02112responsibleDecisionAuthority', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 431, 3), )

    
    responsibleDecisionAuthority = property(__responsibleDecisionAuthority.value, __responsibleDecisionAuthority.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}remark uses Python identifier remark
    __remark = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remark'), 'remark', '__httpwww_ech_chxmlnseCH_02112_eventChangeResponsibilityType_httpwww_ech_chxmlnseCH_02112remark', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 432, 3), )

    
    remark = property(__remark.value, __remark.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_02112_eventChangeResponsibilityType_httpwww_ech_chxmlnseCH_02112extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 433, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __eventType.name() : __eventType,
        __planningPermissionApplicationIdentification.name() : __planningPermissionApplicationIdentification,
        __entryOffice.name() : __entryOffice,
        __responsibleDecisionAuthority.name() : __responsibleDecisionAuthority,
        __remark.name() : __remark,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventChangeResponsibilityType = eventChangeResponsibilityType
Namespace.addCategoryObject('typeBinding', 'eventChangeResponsibilityType', eventChangeResponsibilityType)


# Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventStatusNotificationType with content type ELEMENT_ONLY
class eventStatusNotificationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.ech.ch/xmlns/eCH-0211/2}eventStatusNotificationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventStatusNotificationType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 436, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventType uses Python identifier eventType
    __eventType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventType'), 'eventType', '__httpwww_ech_chxmlnseCH_02112_eventStatusNotificationType_httpwww_ech_chxmlnseCH_02112eventType', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 438, 3), )

    
    eventType = property(__eventType.value, __eventType.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}planningPermissionApplicationIdentification uses Python identifier planningPermissionApplicationIdentification
    __planningPermissionApplicationIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), 'planningPermissionApplicationIdentification', '__httpwww_ech_chxmlnseCH_02112_eventStatusNotificationType_httpwww_ech_chxmlnseCH_02112planningPermissionApplicationIdentification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 445, 3), )

    
    planningPermissionApplicationIdentification = property(__planningPermissionApplicationIdentification.value, __planningPermissionApplicationIdentification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}status uses Python identifier status
    __status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'status'), 'status', '__httpwww_ech_chxmlnseCH_02112_eventStatusNotificationType_httpwww_ech_chxmlnseCH_02112status', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 446, 3), )

    
    status = property(__status.value, __status.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}remark uses Python identifier remark
    __remark = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'remark'), 'remark', '__httpwww_ech_chxmlnseCH_02112_eventStatusNotificationType_httpwww_ech_chxmlnseCH_02112remark', True, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 447, 3), )

    
    remark = property(__remark.value, __remark.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpwww_ech_chxmlnseCH_02112_eventStatusNotificationType_httpwww_ech_chxmlnseCH_02112extension', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 448, 3), )

    
    extension = property(__extension.value, __extension.set, None, None)

    _ElementMap.update({
        __eventType.name() : __eventType,
        __planningPermissionApplicationIdentification.name() : __planningPermissionApplicationIdentification,
        __status.name() : __status,
        __remark.name() : __remark,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventStatusNotificationType = eventStatusNotificationType
Namespace.addCategoryObject('typeBinding', 'eventStatusNotificationType', eventStatusNotificationType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 452, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}deliveryHeader uses Python identifier deliveryHeader
    __deliveryHeader = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'deliveryHeader'), 'deliveryHeader', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_3_httpwww_ech_chxmlnseCH_02112deliveryHeader', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 454, 4), )

    
    deliveryHeader = property(__deliveryHeader.value, __deliveryHeader.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventBaseDelivery uses Python identifier eventBaseDelivery
    __eventBaseDelivery = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventBaseDelivery'), 'eventBaseDelivery', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_3_httpwww_ech_chxmlnseCH_02112eventBaseDelivery', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 456, 5), )

    
    eventBaseDelivery = property(__eventBaseDelivery.value, __eventBaseDelivery.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventSubmitPlanningPermissionApplication uses Python identifier eventSubmitPlanningPermissionApplication
    __eventSubmitPlanningPermissionApplication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventSubmitPlanningPermissionApplication'), 'eventSubmitPlanningPermissionApplication', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_3_httpwww_ech_chxmlnseCH_02112eventSubmitPlanningPermissionApplication', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 457, 5), )

    
    eventSubmitPlanningPermissionApplication = property(__eventSubmitPlanningPermissionApplication.value, __eventSubmitPlanningPermissionApplication.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventChangeContact uses Python identifier eventChangeContact
    __eventChangeContact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventChangeContact'), 'eventChangeContact', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_3_httpwww_ech_chxmlnseCH_02112eventChangeContact', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 458, 5), )

    
    eventChangeContact = property(__eventChangeContact.value, __eventChangeContact.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventRequest uses Python identifier eventRequest
    __eventRequest = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventRequest'), 'eventRequest', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_3_httpwww_ech_chxmlnseCH_02112eventRequest', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 459, 5), )

    
    eventRequest = property(__eventRequest.value, __eventRequest.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventAccompanyingReport uses Python identifier eventAccompanyingReport
    __eventAccompanyingReport = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventAccompanyingReport'), 'eventAccompanyingReport', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_3_httpwww_ech_chxmlnseCH_02112eventAccompanyingReport', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 460, 5), )

    
    eventAccompanyingReport = property(__eventAccompanyingReport.value, __eventAccompanyingReport.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventCloseArchiveDossier uses Python identifier eventCloseArchiveDossier
    __eventCloseArchiveDossier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventCloseArchiveDossier'), 'eventCloseArchiveDossier', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_3_httpwww_ech_chxmlnseCH_02112eventCloseArchiveDossier', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 461, 5), )

    
    eventCloseArchiveDossier = property(__eventCloseArchiveDossier.value, __eventCloseArchiveDossier.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventKindOfProceedings uses Python identifier eventKindOfProceedings
    __eventKindOfProceedings = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventKindOfProceedings'), 'eventKindOfProceedings', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_3_httpwww_ech_chxmlnseCH_02112eventKindOfProceedings', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 462, 5), )

    
    eventKindOfProceedings = property(__eventKindOfProceedings.value, __eventKindOfProceedings.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventNoticeInvolvedParty uses Python identifier eventNoticeInvolvedParty
    __eventNoticeInvolvedParty = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventNoticeInvolvedParty'), 'eventNoticeInvolvedParty', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_3_httpwww_ech_chxmlnseCH_02112eventNoticeInvolvedParty', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 463, 5), )

    
    eventNoticeInvolvedParty = property(__eventNoticeInvolvedParty.value, __eventNoticeInvolvedParty.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventNotice uses Python identifier eventNotice
    __eventNotice = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventNotice'), 'eventNotice', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_3_httpwww_ech_chxmlnseCH_02112eventNotice', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 464, 5), )

    
    eventNotice = property(__eventNotice.value, __eventNotice.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventStatusNotification uses Python identifier eventStatusNotification
    __eventStatusNotification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventStatusNotification'), 'eventStatusNotification', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_3_httpwww_ech_chxmlnseCH_02112eventStatusNotification', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 465, 5), )

    
    eventStatusNotification = property(__eventStatusNotification.value, __eventStatusNotification.set, None, None)

    
    # Element {http://www.ech.ch/xmlns/eCH-0211/2}eventChangeResponsibility uses Python identifier eventChangeResponsibility
    __eventChangeResponsibility = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventChangeResponsibility'), 'eventChangeResponsibility', '__httpwww_ech_chxmlnseCH_02112_CTD_ANON_3_httpwww_ech_chxmlnseCH_02112eventChangeResponsibility', False, pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 466, 5), )

    
    eventChangeResponsibility = property(__eventChangeResponsibility.value, __eventChangeResponsibility.set, None, None)

    _ElementMap.update({
        __deliveryHeader.name() : __deliveryHeader,
        __eventBaseDelivery.name() : __eventBaseDelivery,
        __eventSubmitPlanningPermissionApplication.name() : __eventSubmitPlanningPermissionApplication,
        __eventChangeContact.name() : __eventChangeContact,
        __eventRequest.name() : __eventRequest,
        __eventAccompanyingReport.name() : __eventAccompanyingReport,
        __eventCloseArchiveDossier.name() : __eventCloseArchiveDossier,
        __eventKindOfProceedings.name() : __eventKindOfProceedings,
        __eventNoticeInvolvedParty.name() : __eventNoticeInvolvedParty,
        __eventNotice.name() : __eventNotice,
        __eventStatusNotification.name() : __eventStatusNotification,
        __eventChangeResponsibility.name() : __eventChangeResponsibility
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


delivery = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'delivery'), CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 451, 1))
Namespace.addCategoryObject('elementBinding', delivery.name().localName(), delivery)



natureRiskType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'riskDesignation'), STD_ANON, scope=natureRiskType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 78, 3)))

natureRiskType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'riskExists'), pyxb.binding.datatypes.boolean, scope=natureRiskType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 86, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(natureRiskType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'riskDesignation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 78, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(natureRiskType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'riskExists')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 86, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
natureRiskType._Automaton = _BuildAutomaton()




constructionProjectInformationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'constructionProject'), _ImportedBinding_camac_echbern_schema_ech_0129_5_0.constructionProjectType, scope=constructionProjectInformationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 91, 3)))

constructionProjectInformationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'municipality'), _ImportedBinding_camac_echbern_schema_ech_0007_6_0.swissMunicipalityType, scope=constructionProjectInformationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 93, 4)))

constructionProjectInformationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'canton'), _ImportedBinding_camac_echbern_schema_ech_0007_6_0.cantonAbbreviationType, scope=constructionProjectInformationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 94, 4)))

constructionProjectInformationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'confederation'), STD_ANON_, scope=constructionProjectInformationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 95, 4)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 92, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(constructionProjectInformationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'constructionProject')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 91, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(constructionProjectInformationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'municipality')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 93, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(constructionProjectInformationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'canton')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 94, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(constructionProjectInformationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'confederation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 95, 4))
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
constructionProjectInformationType._Automaton = _BuildAutomaton_()




planningPermissionApplicationIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'localID'), _ImportedBinding_camac_echbern_schema_ech_0129_5_0.namedIdType, scope=planningPermissionApplicationIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 124, 3)))

planningPermissionApplicationIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherID'), _ImportedBinding_camac_echbern_schema_ech_0129_5_0.namedIdType, scope=planningPermissionApplicationIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 125, 3)))

planningPermissionApplicationIdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dossierIdentification'), dossierIdentificationType, scope=planningPermissionApplicationIdentificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 126, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 126, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'localID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 124, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherID')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 125, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationIdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dossierIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 126, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
planningPermissionApplicationIdentificationType._Automaton = _BuildAutomaton_2()




planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), planningPermissionApplicationIdentificationType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 131, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), descriptionType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 132, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'applicationType'), applicationTypeType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 133, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remark'), remarkType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 134, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'proceedingType'), proceedingTypeType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 135, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'profilingYesNo'), pyxb.binding.datatypes.boolean, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 136, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'profilingDate'), pyxb.binding.datatypes.date, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 137, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'intendedPurpose'), intendedPurposeType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 138, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'parkingLotsYesNo'), pyxb.binding.datatypes.boolean, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 139, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'natureRisk'), natureRiskType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 140, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'constructionCost'), STD_ANON_2, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 141, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'publication'), publicationType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 149, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'namedMetaData'), _ImportedBinding_camac_echbern_schema_ech_0129_5_0.namedMetaDataType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 150, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'locationAddress'), _ImportedBinding_camac_echbern_schema_ech_0010_6_0.swissAddressInformationType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 151, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'realestateInformation'), realestateInformationType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 152, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'zone'), zoneType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 153, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'constructionProjectInformation'), constructionProjectInformationType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 154, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'directive'), _ImportedBinding_camac_echbern_schema_ech_0147_t2_1.directiveType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 155, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'decisionRuling'), decisionRulingType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 156, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'document'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.documentType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 157, 3)))

planningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'referencedPlanningPermissionApplication'), planningPermissionApplicationIdentificationType, scope=planningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 158, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 133, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 134, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 135, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 136, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 137, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 138, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 139, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 140, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 141, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 149, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 150, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 153, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 154, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 155, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 156, 3))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 158, 3))
    counters.add(cc_15)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 131, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 132, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'applicationType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 133, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remark')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 134, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'proceedingType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 135, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'profilingYesNo')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 136, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'profilingDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 137, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'intendedPurpose')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 138, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'parkingLotsYesNo')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 139, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'natureRisk')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 140, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'constructionCost')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 141, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'publication')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 149, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'namedMetaData')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 150, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'locationAddress')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 151, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'realestateInformation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 152, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'zone')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 153, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'constructionProjectInformation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 154, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'directive')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 155, 3))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'decisionRuling')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 156, 3))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'document')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 157, 3))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(planningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'referencedPlanningPermissionApplication')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 158, 3))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
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
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_13, [
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
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_13, [
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
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
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
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
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
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
         ]))
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
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
         ]))
    transitions.append(fac.Transition(st_20, [
         ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_15, True) ]))
    st_20._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
planningPermissionApplicationType._Automaton = _BuildAutomaton_3()




publicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'officialGazette'), STD_ANON_3, scope=publicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 163, 3)))

publicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'publicationText'), remarkType, scope=publicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 171, 3)))

publicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'publicationDate'), pyxb.binding.datatypes.date, scope=publicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 172, 3)))

publicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'publicationTill'), pyxb.binding.datatypes.date, scope=publicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 173, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 173, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(publicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'officialGazette')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 163, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(publicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'publicationText')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 171, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(publicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'publicationDate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 172, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(publicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'publicationTill')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 173, 3))
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
publicationType._Automaton = _BuildAutomaton_4()




zoneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'abbreviatedDesignation'), STD_ANON_4, scope=zoneType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 178, 3)))

zoneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'zoneDesignation'), STD_ANON_5, scope=zoneType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 186, 3)))

zoneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'zoneType'), STD_ANON_6, scope=zoneType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 194, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 178, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 194, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(zoneType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'abbreviatedDesignation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 178, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(zoneType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'zoneDesignation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 186, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(zoneType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'zoneType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 194, 3))
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
zoneType._Automaton = _BuildAutomaton_5()




decisionRulingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'judgement'), judgementType, scope=decisionRulingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 206, 3)))

decisionRulingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ruling'), remarkType, scope=decisionRulingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 207, 3)))

decisionRulingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'date'), pyxb.binding.datatypes.date, scope=decisionRulingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 208, 3)))

decisionRulingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rulingAuthority'), _ImportedBinding_camac_echbern_schema_ech_0097_2_0.organisationIdentificationType, scope=decisionRulingType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 209, 3)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 206, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(decisionRulingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'judgement')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 206, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(decisionRulingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ruling')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 207, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(decisionRulingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'date')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 208, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(decisionRulingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'rulingAuthority')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 209, 3))
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
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
decisionRulingType._Automaton = _BuildAutomaton_6()




decisionAuthorityInformationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'decisionAuthority'), _ImportedBinding_camac_echbern_schema_ech_0129_5_0.buildingAuthorityType, scope=decisionAuthorityInformationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 214, 3)))

decisionAuthorityInformationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'municipality'), _ImportedBinding_camac_echbern_schema_ech_0007_6_0.swissMunicipalityType, scope=decisionAuthorityInformationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 215, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 215, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(decisionAuthorityInformationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'decisionAuthority')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 214, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(decisionAuthorityInformationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'municipality')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 215, 3))
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
decisionAuthorityInformationType._Automaton = _BuildAutomaton_7()




entryOfficeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'entryOfficeIdentification'), _ImportedBinding_camac_echbern_schema_ech_0097_2_0.organisationIdentificationType, scope=entryOfficeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 220, 3)))

entryOfficeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'municipality'), _ImportedBinding_camac_echbern_schema_ech_0007_6_0.swissMunicipalityType, scope=entryOfficeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 221, 3)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 221, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(entryOfficeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'entryOfficeIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 220, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(entryOfficeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'municipality')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 221, 3))
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
entryOfficeType._Automaton = _BuildAutomaton_8()




specialistDepartmentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'specialistDepartmentIdentification'), _ImportedBinding_camac_echbern_schema_ech_0097_2_0.organisationIdentificationType, scope=specialistDepartmentType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 226, 3)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(specialistDepartmentType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'specialistDepartmentIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 226, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
specialistDepartmentType._Automaton = _BuildAutomaton_9()




relationshipToPersonType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'role'), roleType, scope=relationshipToPersonType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 237, 3)))

relationshipToPersonType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'person'), _ImportedBinding_camac_echbern_schema_ech_0129_5_0.personType, scope=relationshipToPersonType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 238, 3)))

relationshipToPersonType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'deputy'), _ImportedBinding_camac_echbern_schema_ech_0010_6_0.mailAddressType, scope=relationshipToPersonType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 239, 3)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 239, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(relationshipToPersonType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'role')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 237, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(relationshipToPersonType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'person')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 238, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(relationshipToPersonType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'deputy')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 239, 3))
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
relationshipToPersonType._Automaton = _BuildAutomaton_10()




realestateInformationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'realestate'), _ImportedBinding_camac_echbern_schema_ech_0129_5_0.realestateType, scope=realestateInformationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 244, 3)))

realestateInformationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'municipality'), _ImportedBinding_camac_echbern_schema_ech_0007_6_0.swissMunicipalityType, scope=realestateInformationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 245, 3)))

realestateInformationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'buildingInformation'), buildingInformationType, scope=realestateInformationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 246, 3)))

realestateInformationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'placeName'), _ImportedBinding_camac_echbern_schema_ech_0129_5_0.placeNameType, scope=realestateInformationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 247, 3)))

realestateInformationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'owner'), CTD_ANON, scope=realestateInformationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 248, 3)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 246, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 247, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(realestateInformationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'realestate')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 244, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(realestateInformationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'municipality')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 245, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(realestateInformationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'buildingInformation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 246, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(realestateInformationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'placeName')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 247, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(realestateInformationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'owner')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 248, 3))
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
    transitions.append(fac.Transition(st_4, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
realestateInformationType._Automaton = _BuildAutomaton_11()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ownerIdentification'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 251, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ownerAdress'), _ImportedBinding_camac_echbern_schema_ech_0010_6_0.mailAddressType, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 259, 6)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 251, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ownerIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 251, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ownerAdress')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 259, 6))
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
CTD_ANON._Automaton = _BuildAutomaton_12()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'personIdentification'), _ImportedBinding_camac_echbern_schema_ech_0044_4_1.personIdentificationLightType, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 254, 9)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification'), _ImportedBinding_camac_echbern_schema_ech_0097_2_0.organisationIdentificationType, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 255, 9)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'personIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 254, 9))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'organisationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 255, 9))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_13()




buildingInformationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'building'), _ImportedBinding_camac_echbern_schema_ech_0129_5_0.buildingType, scope=buildingInformationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 267, 3)))

buildingInformationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dwelling'), _ImportedBinding_camac_echbern_schema_ech_0129_5_0.dwellingType, scope=buildingInformationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 268, 3)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 268, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(buildingInformationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'building')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 267, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(buildingInformationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dwelling')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 268, 3))
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
buildingInformationType._Automaton = _BuildAutomaton_14()




eventBaseDeliveryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationInformation'), CTD_ANON_2, scope=eventBaseDeliveryType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 273, 3)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventBaseDeliveryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationInformation')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 273, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventBaseDeliveryType._Automaton = _BuildAutomaton_15()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplication'), planningPermissionApplicationType, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 276, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relationshipToPerson'), relationshipToPersonType, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 277, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'decisionAuthority'), decisionAuthorityInformationType, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 278, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'entryOffice'), entryOfficeType, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 279, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'specialistDepartment'), specialistDepartmentType, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 280, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'document'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.documentType, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 281, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 282, 6)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 280, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 281, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 282, 6))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplication')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 276, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relationshipToPerson')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 277, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'decisionAuthority')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 278, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'entryOffice')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 279, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'specialistDepartment')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 280, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'document')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 281, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 282, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
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
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_16()




eventSubmitPlanningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventType'), STD_ANON_7, scope=eventSubmitPlanningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 290, 3)))

eventSubmitPlanningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplication'), planningPermissionApplicationType, scope=eventSubmitPlanningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 298, 3)))

eventSubmitPlanningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relationshipToPerson'), relationshipToPersonType, scope=eventSubmitPlanningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 299, 3)))

eventSubmitPlanningPermissionApplicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=eventSubmitPlanningPermissionApplicationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 300, 3)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 300, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventSubmitPlanningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 290, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventSubmitPlanningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplication')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 298, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventSubmitPlanningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relationshipToPerson')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 299, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(eventSubmitPlanningPermissionApplicationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 300, 3))
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
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventSubmitPlanningPermissionApplicationType._Automaton = _BuildAutomaton_17()




eventChangeContactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventType'), STD_ANON_8, scope=eventChangeContactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 305, 3)))

eventChangeContactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), planningPermissionApplicationIdentificationType, scope=eventChangeContactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 312, 3)))

eventChangeContactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'directive'), _ImportedBinding_camac_echbern_schema_ech_0147_t2_1.directiveType, scope=eventChangeContactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 313, 3)))

eventChangeContactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relationshipToPerson'), relationshipToPersonType, scope=eventChangeContactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 314, 3)))

eventChangeContactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remark'), remarkType, scope=eventChangeContactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 315, 3)))

eventChangeContactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=eventChangeContactType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 316, 3)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 313, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 315, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 316, 3))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventChangeContactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 305, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventChangeContactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 312, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventChangeContactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'directive')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 313, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventChangeContactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relationshipToPerson')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 314, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(eventChangeContactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remark')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 315, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(eventChangeContactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 316, 3))
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventChangeContactType._Automaton = _BuildAutomaton_18()




eventRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventType'), STD_ANON_9, scope=eventRequestType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 321, 3)))

eventRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), planningPermissionApplicationIdentificationType, scope=eventRequestType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 331, 3)))

eventRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'directive'), _ImportedBinding_camac_echbern_schema_ech_0147_t2_1.directiveType, scope=eventRequestType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 332, 3)))

eventRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'document'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.documentType, scope=eventRequestType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 333, 3)))

eventRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remark'), remarkType, scope=eventRequestType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 334, 3)))

eventRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=eventRequestType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 335, 3)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 332, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 333, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 334, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 335, 3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 321, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 331, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(eventRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'directive')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 332, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(eventRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'document')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 333, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(eventRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remark')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 334, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(eventRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 335, 3))
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
eventRequestType._Automaton = _BuildAutomaton_19()




eventAccompanyingReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventType'), STD_ANON_10, scope=eventAccompanyingReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 340, 3)))

eventAccompanyingReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'judgement'), judgementType, scope=eventAccompanyingReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 347, 3)))

eventAccompanyingReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), planningPermissionApplicationIdentificationType, scope=eventAccompanyingReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 348, 3)))

eventAccompanyingReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'directive'), _ImportedBinding_camac_echbern_schema_ech_0147_t2_1.directiveType, scope=eventAccompanyingReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 349, 3)))

eventAccompanyingReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'document'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.documentType, scope=eventAccompanyingReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 350, 3)))

eventAccompanyingReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remark'), remarkType, scope=eventAccompanyingReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 351, 3)))

eventAccompanyingReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ancillaryClauses'), remarkType, scope=eventAccompanyingReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 352, 3)))

eventAccompanyingReportType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=eventAccompanyingReportType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 353, 3)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 347, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 349, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 351, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 352, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 353, 3))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventAccompanyingReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 340, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventAccompanyingReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'judgement')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 347, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventAccompanyingReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 348, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventAccompanyingReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'directive')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 349, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventAccompanyingReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'document')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 350, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(eventAccompanyingReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remark')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 351, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(eventAccompanyingReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ancillaryClauses')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 352, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(eventAccompanyingReportType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 353, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
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
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
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
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventAccompanyingReportType._Automaton = _BuildAutomaton_20()




eventCloseArchiveDossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventType'), STD_ANON_11, scope=eventCloseArchiveDossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 358, 3)))

eventCloseArchiveDossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), planningPermissionApplicationIdentificationType, scope=eventCloseArchiveDossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 366, 3)))

eventCloseArchiveDossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remark'), remarkType, scope=eventCloseArchiveDossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 367, 3)))

eventCloseArchiveDossierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=eventCloseArchiveDossierType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 368, 3)))

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 367, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 368, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventCloseArchiveDossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 358, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventCloseArchiveDossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 366, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(eventCloseArchiveDossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remark')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 367, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(eventCloseArchiveDossierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 368, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventCloseArchiveDossierType._Automaton = _BuildAutomaton_21()




eventKindOfProceedingsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventType'), STD_ANON_12, scope=eventKindOfProceedingsType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 373, 3)))

eventKindOfProceedingsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), planningPermissionApplicationIdentificationType, scope=eventKindOfProceedingsType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 380, 3)))

eventKindOfProceedingsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'document'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.documentType, scope=eventKindOfProceedingsType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 381, 3)))

eventKindOfProceedingsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remark'), remarkType, scope=eventKindOfProceedingsType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 382, 3)))

eventKindOfProceedingsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=eventKindOfProceedingsType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 383, 3)))

def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 382, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 383, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventKindOfProceedingsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 373, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventKindOfProceedingsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 380, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventKindOfProceedingsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'document')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 381, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(eventKindOfProceedingsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remark')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 382, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(eventKindOfProceedingsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 383, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
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
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventKindOfProceedingsType._Automaton = _BuildAutomaton_22()




eventNoticeInvolvedPartyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventType'), STD_ANON_13, scope=eventNoticeInvolvedPartyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 388, 3)))

eventNoticeInvolvedPartyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), planningPermissionApplicationIdentificationType, scope=eventNoticeInvolvedPartyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 395, 3)))

eventNoticeInvolvedPartyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'decisionAuthority'), decisionAuthorityInformationType, scope=eventNoticeInvolvedPartyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 396, 3)))

eventNoticeInvolvedPartyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'entryOffice'), entryOfficeType, scope=eventNoticeInvolvedPartyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 397, 3)))

eventNoticeInvolvedPartyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'specialistDepartment'), specialistDepartmentType, scope=eventNoticeInvolvedPartyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 398, 3)))

eventNoticeInvolvedPartyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remark'), remarkType, scope=eventNoticeInvolvedPartyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 399, 3)))

eventNoticeInvolvedPartyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'document'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.documentType, scope=eventNoticeInvolvedPartyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 400, 3)))

eventNoticeInvolvedPartyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=eventNoticeInvolvedPartyType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 401, 3)))

def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 398, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 399, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 400, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 401, 3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventNoticeInvolvedPartyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 388, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventNoticeInvolvedPartyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 395, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventNoticeInvolvedPartyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'decisionAuthority')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 396, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventNoticeInvolvedPartyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'entryOffice')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 397, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(eventNoticeInvolvedPartyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'specialistDepartment')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 398, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(eventNoticeInvolvedPartyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remark')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 399, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(eventNoticeInvolvedPartyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'document')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 400, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(eventNoticeInvolvedPartyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 401, 3))
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
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventNoticeInvolvedPartyType._Automaton = _BuildAutomaton_23()




eventNoticeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventType'), STD_ANON_14, scope=eventNoticeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 406, 3)))

eventNoticeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), planningPermissionApplicationIdentificationType, scope=eventNoticeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 413, 3)))

eventNoticeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'decisionRuling'), decisionRulingType, scope=eventNoticeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 414, 3)))

eventNoticeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'document'), _ImportedBinding_camac_echbern_schema_ech_0147_t0_1.documentType, scope=eventNoticeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 415, 3)))

eventNoticeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remark'), remarkType, scope=eventNoticeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 416, 3)))

eventNoticeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=eventNoticeType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 417, 3)))

def _BuildAutomaton_24 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 415, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 416, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 417, 3))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventNoticeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 406, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventNoticeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 413, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventNoticeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'decisionRuling')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 414, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(eventNoticeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'document')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 415, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(eventNoticeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remark')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 416, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(eventNoticeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 417, 3))
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
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventNoticeType._Automaton = _BuildAutomaton_24()




eventChangeResponsibilityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventType'), STD_ANON_15, scope=eventChangeResponsibilityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 422, 3)))

eventChangeResponsibilityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), planningPermissionApplicationIdentificationType, scope=eventChangeResponsibilityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 429, 3)))

eventChangeResponsibilityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'entryOffice'), entryOfficeType, scope=eventChangeResponsibilityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 430, 3)))

eventChangeResponsibilityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'responsibleDecisionAuthority'), decisionAuthorityInformationType, scope=eventChangeResponsibilityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 431, 3)))

eventChangeResponsibilityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remark'), remarkType, scope=eventChangeResponsibilityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 432, 3)))

eventChangeResponsibilityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=eventChangeResponsibilityType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 433, 3)))

def _BuildAutomaton_25 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 432, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 433, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventChangeResponsibilityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 422, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventChangeResponsibilityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 429, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventChangeResponsibilityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'entryOffice')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 430, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventChangeResponsibilityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'responsibleDecisionAuthority')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 431, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(eventChangeResponsibilityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remark')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 432, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(eventChangeResponsibilityType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 433, 3))
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
    transitions.append(fac.Transition(st_5, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventChangeResponsibilityType._Automaton = _BuildAutomaton_25()




eventStatusNotificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventType'), STD_ANON_16, scope=eventStatusNotificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 438, 3)))

eventStatusNotificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification'), planningPermissionApplicationIdentificationType, scope=eventStatusNotificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 445, 3)))

eventStatusNotificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'status'), planningPermissionApplicationStatusType, scope=eventStatusNotificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 446, 3)))

eventStatusNotificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'remark'), remarkType, scope=eventStatusNotificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 447, 3)))

eventStatusNotificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.anyType, scope=eventStatusNotificationType, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 448, 3)))

def _BuildAutomaton_26 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_26
    del _BuildAutomaton_26
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 447, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 448, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventStatusNotificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventType')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 438, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventStatusNotificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'planningPermissionApplicationIdentification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 445, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventStatusNotificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'status')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 446, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(eventStatusNotificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'remark')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 447, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(eventStatusNotificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 448, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventStatusNotificationType._Automaton = _BuildAutomaton_26()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'deliveryHeader'), _ImportedBinding_camac_echbern_schema_ech_0058_5_0.headerType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 454, 4)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventBaseDelivery'), eventBaseDeliveryType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 456, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventSubmitPlanningPermissionApplication'), eventSubmitPlanningPermissionApplicationType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 457, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventChangeContact'), eventChangeContactType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 458, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventRequest'), eventRequestType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 459, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventAccompanyingReport'), eventAccompanyingReportType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 460, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventCloseArchiveDossier'), eventCloseArchiveDossierType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 461, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventKindOfProceedings'), eventKindOfProceedingsType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 462, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventNoticeInvolvedParty'), eventNoticeInvolvedPartyType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 463, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventNotice'), eventNoticeType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 464, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventStatusNotification'), eventStatusNotificationType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 465, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventChangeResponsibility'), eventChangeResponsibilityType, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 466, 5)))

def _BuildAutomaton_27 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_27
    del _BuildAutomaton_27
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'deliveryHeader')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 454, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventBaseDelivery')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 456, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventSubmitPlanningPermissionApplication')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 457, 5))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventChangeContact')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 458, 5))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventRequest')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 459, 5))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventAccompanyingReport')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 460, 5))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventCloseArchiveDossier')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 461, 5))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventKindOfProceedings')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 462, 5))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventNoticeInvolvedParty')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 463, 5))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventNotice')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 464, 5))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventStatusNotification')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 465, 5))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventChangeResponsibility')), pyxb.utils.utility.Location('/home/dv/Work/camac-ng/django/camac/echbern/xsd/ech_0211_2_0.xsd', 466, 5))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
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
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    transitions = []
    st_4._set_transitionSet(transitions)
    transitions = []
    st_5._set_transitionSet(transitions)
    transitions = []
    st_6._set_transitionSet(transitions)
    transitions = []
    st_7._set_transitionSet(transitions)
    transitions = []
    st_8._set_transitionSet(transitions)
    transitions = []
    st_9._set_transitionSet(transitions)
    transitions = []
    st_10._set_transitionSet(transitions)
    transitions = []
    st_11._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_27()

