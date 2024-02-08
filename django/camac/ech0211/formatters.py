"""Helpers for exporting instance data to eCH-0211."""

import datetime
import itertools
import logging
import re
from typing import List

import pyxb
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from pyxb import IncompleteElementContentError, UnprocessedElementContentError

from camac import camac_metadata
from camac.caluma.utils import find_answer
from camac.core.utils import canton_aware
from camac.document.models import Attachment
from camac.ech0211.constants import (
    ECH_JUDGEMENT_APPROVED,
    ECH_JUDGEMENT_DECLINED,
    ECH_JUDGEMENT_WRITTEN_OFF,
)
from camac.instance.models import Instance
from camac.utils import build_url

from ..instance.master_data import MasterData
from .schema import (
    ech_0007_6_0,
    ech_0010_6_0 as ns_address,
    ech_0044_4_1,
    ech_0058_5_0,
    ech_0097_2_0 as ns_company_identification,
    ech_0129_5_0 as ns_objektwesen,
    ech_0147_t0_1 as ns_nachrichten_t0,
    ech_0147_t2_1 as ns_nachrichten_t2,
    ech_0211_2_0 as ns_application,
)
from .utils import decision_to_judgement, handle_string_values, strip_whitespace

logger = logging.getLogger(__name__)


def clean_version(full_version: str) -> str:
    """Remove prerelease info from version.

    This is needed because the eCH standard only allows a maximum of 10
    characters in the version field.
    """
    match = re.search(r"^\d+.\d+.\d+", full_version)

    return match.group(0) if match else full_version


def handle_ja_nein_bool(value):
    if value in ["Ja", "ja"]:
        return True
    elif value in ["Nein", "nein"]:  # pragma: no cover
        return False


def assure_string_length(value, min_length=1, max_length=0):
    value = strip_whitespace(
        str(value)
    )  # Handle None and bool and also computed values
    if len(value) > max_length:
        return f"{value[:max_length - 1]}…"
    elif len(value) < min_length:
        return f"{value}{'.' * (min_length - len(value))}"  # TODO cover
    return value


def handle_coordinate_value(value):
    return round(float(value), 3)


def authority(service, organization_category=None):
    return ns_company_identification.organisationIdentificationType(
        uid=ns_company_identification.uidStructureType(
            # We don't bother with UIDs
            uidOrganisationIdCategorie="CHE",
            uidOrganisationId="123123123",
        ),
        localOrganisationId=ns_company_identification.namedOrganisationIdType(
            organisationIdCategory=organization_category, organisationId=str(service.pk)
        ),
        organisationName=service.get_name(),
        legalForm="0223",
    )


def get_document_sections(attachment):
    sections = [s.get_name() for s in attachment.attachment_sections.all()]
    return "; ".join(sections)


def get_zip(value):
    if not value or not len(str(value)) == 4:
        # use 9999 for non swiss zips
        return 9999
    return value


def get_cost(value):
    if value and value < 1000:
        return 1000
    return value


def get_keywords(attachment):
    tags = attachment.context.get("tags")
    if tags:
        return pyxb.BIND(keyword=tags)


def get_documents(attachments):
    documents = [
        ns_nachrichten_t0.documentType(
            uuid=str(attachment.uuid),
            titles=pyxb.BIND(title=[attachment.display_name]),
            status="signed",  # ech0039 documentStatusType
            documentKind=get_document_sections(attachment),
            keywords=get_keywords(attachment),
            files=ns_nachrichten_t0.filesType(
                file=[
                    ns_nachrichten_t0.fileType(
                        pathFileName=build_url(
                            settings.INTERNAL_BASE_URL,
                            f"{reverse('multi-attachment-download')}?attachments={attachment.pk}",
                        ),
                        mimeType=attachment.mime_type,
                        # internalSortOrder minOccurs=0
                        # version minOccurs=0
                        # hashCode minOccurs=0
                        # hashCodeAlgorithm minOccurs=0
                    )
                ]
            ),
        )
        for attachment in attachments.order_by("-date", "pk")
    ]
    if not documents:
        documents = [
            ns_nachrichten_t0.documentType(
                uuid="00000000-0000-0000-0000-000000000000",
                titles=pyxb.BIND(title=["dummy"]),
                status="signed",
                files=ns_nachrichten_t0.filesType(
                    file=[
                        ns_nachrichten_t0.fileType(
                            pathFileName="unknown", mimeType="unknown"
                        )
                    ]
                ),
            )
        ]
    return documents


def extract_street_number(string, fallback="0"):
    """Very simple street number extractor.

    Split string at first digit if any.
    """
    if not string:
        return fallback

    split = list(re.split(r"(\d+)", string))
    if len(split) > 1:
        return "".join(split[1:])
    return fallback


def make_dummy_address_ech0044():
    return [
        pyxb.BIND(
            ownerAdress=ns_address.mailAddressType(
                person=ns_address.personMailAddressInfoType(
                    firstName="unknown", lastName="unknown"
                ),
                addressInformation=ns_address.addressInformationType(
                    street="unknown",
                    houseNumber="0",
                    town=ns_address.townType("unknown"),
                    swissZipCode=9999,
                    country="CH",
                ),
            )
        )
    ]


def municipality(md):
    return ech_0007_6_0.swissMunicipalityType(
        municipalityName=assure_string_length(md.municipality_name, max_length=40),
        cantonAbbreviation=settings.APPLICATION["SHORT_NAME"].upper(),
    )


def application(instance: Instance):
    """Create and format an application's properties based on the instance's MasterData."""
    md = MasterData(instance.case)
    if md.decision_date and not isinstance(
        md.decision_date, datetime.date
    ):  # pragma: no cover
        raise IncompleteElementContentError("Decision date is not a valid date.")

    realestate_info = [
        ns_application.realestateInformationType(
            realestate=ns_objektwesen.realestateType(  # eCH0129 4.8.1
                realestateIdentification=ns_objektwesen.realestateIdentificationType(
                    EGRID=plot.get("egrid_number", "unknown"),
                    number=str(plot.get("plot_number", "unknown")),
                ),
                realestateType="8",  # mentioned in swagger README
                coordinates=(
                    ns_objektwesen.coordinatesType(
                        LV95=pyxb.BIND(
                            east=handle_coordinate_value(plot.get("coord_east")),
                            north=handle_coordinate_value(plot.get("coord_north")),
                            originOfCoordinates=904,
                        )
                    )
                    if all(k in plot and plot[k] for k in ["coord_east", "coord_north"])
                    else None
                ),
            ),
            municipality=municipality(md),
            buildingInformation=CantonSpecific.building_information(instance, md),
            owner=[
                pyxb.BIND(
                    ownerAdress=ns_address.mailAddressType(
                        person=ns_address.personMailAddressInfoType(
                            firstName=assure_string_length(
                                owner.get("first_name", "unknown"), max_length=30
                            ),
                            lastName=assure_string_length(
                                owner.get("last_name", "unknown"), max_length=30
                            ),
                        ),
                        # not the same as swissAddressInformationType (obv..)
                        addressInformation=ns_address.addressInformationType(
                            street=assure_string_length(
                                owner.get("street"), max_length=60
                            ),
                            houseNumber=assure_string_length(
                                owner.get("street_number", "0"), max_length=12
                            ),
                            town=assure_string_length(
                                ns_address.townType(owner.get("town")), max_length=40
                            ),
                            swissZipCode=get_zip(owner.get("zip")),
                            # foreignZipCode minOccurs=0
                            country="CH",
                        ),
                    )
                )
                for owner in (
                    md.landowners if len(md.landowners) > 0 else md.applicants
                )
            ],
        )
        for plot in md.plot_data
    ]
    if not realestate_info:
        # happens if no parcels are filled (e. g.: application_type: Vorabklärung)
        realestate_info = [
            ns_application.realestateInformationType(
                realestate=ns_objektwesen.realestateType(
                    realestateIdentification=ns_objektwesen.realestateIdentificationType(
                        number="0"
                    ),
                    realestateType="8",
                    coordinates=None,
                ),
                municipality=municipality(md),
                owner=make_dummy_address_ech0044(),
            )
        ]
    related_instances = instance.get_linked_instances()
    planning_permission_application_type = ns_application.planningPermissionApplicationType(
        planningPermissionApplicationIdentification=permission_application_identification(
            instance
        ),  # 3.1.1.1
        description=assure_string_length(
            md.proposal, min_length=3, max_length=950
        ),  # 3.1.1.2
        applicationType=assure_string_length(
            md.application_type, max_length=100
        ),  # 3.1.1.3
        remark=(
            [assure_string_length(md.remark, max_length=950)] if md.remark else []
        ),  # 3.1.1.4
        proceedingType=md.proceeding_type,  # 3.1.1.5
        profilingYesNo=isinstance(
            md.profile_approval_date, datetime.datetime
        ),  # 3.1.1.6
        profilingDate=md.profile_approval_date,  # 3.1.1.7
        parkingLotsYesNo=bool(md.parking_lots),
        natureRisk=(
            [
                ns_application.natureRiskType(
                    riskDesignation=assure_string_length(
                        risk["risk_type"], max_length=255
                    ),
                    riskExists=True,
                )
                for risk in md.nature_risk
            ]
            if md.nature_risk
            else None
        ),
        intendedPurpose=assure_string_length(
            ", ".join(md.usage_type or []), max_length=255
        ),  # 3.1.1.8
        constructionCost=get_cost(md.construction_costs),  # 3.1.1.11
        namedMetaData=[  # Erweiterungsfelder 3.1.1.14  TODO: verify!
            ns_objektwesen.namedMetaDataType(
                metaDataName="status", metaDataValue=instance.instance_state.get_name()
            )
        ],
        locationAddress=ns_address.swissAddressInformationType(  # 3.1.1.15
            houseNumber=assure_string_length(
                md.street_number or extract_street_number(md.street), max_length=12
            ),
            street=assure_string_length(
                md.street if md.street else "unknown", max_length=60
            ),
            town=assure_string_length(md.city if md.city else "unknown", max_length=40),
            swissZipCode=get_zip(md.zip),
            country="CH",
        ),
        realestateInformation=realestate_info,  # TODO: 3.1.1.16 incl subtype
        constructionProjectInformation=ns_application.constructionProjectInformationType(
            constructionProject=ns_objektwesen.constructionProject(
                status=6701,  # we always send this. The real status is in namedMetaData
                description=assure_string_length(
                    md.proposal if md.proposal else "unknown",
                    min_length=3,
                    max_length=1000,
                ),
                projectStartDate=md.construction_start_date,
                durationOfConstructionPhase=(
                    md.construction_duration if md.construction_duration else 999
                ),
                totalCostsOfProject=get_cost(md.construction_costs),
            ),
            municipality=municipality(md),
        ),
        referencedPlanningPermissionApplication=[
            permission_application_identification(i) for i in related_instances
        ],  # Referenzierte Baugesuche 3.1.1.22 TODO: verify!
        document=get_documents(instance.attachments.all()),  # 3.2
        decisionRuling=CantonSpecific.decision_ruling(instance, md),  # 3.4
        zone=(
            [  # TODO: 3.8
                ns_application.zoneType(
                    zoneDesignation=assure_string_length(md.usage_zone, max_length=255)
                )
            ]
            if md.usage_zone
            else []
        ),  # eCH allows for max 225 chars
    )
    return planning_permission_application_type


def office(service, organization_category=None):
    return ns_application.entryOfficeType(
        entryOfficeIdentification=authority(
            service, organization_category=organization_category
        ),
        municipality=ech_0007_6_0.swissMunicipalityType(
            municipalityName=assure_string_length(
                service.get_trans_attr("city") or "unknown", max_length=40
            ),
            cantonAbbreviation=settings.APPLICATION["SHORT_NAME"].upper(),
        ),
    )


def permission_application_identification(instance: Instance):
    ebau_nr = MasterData(instance.case).dossier_number or "unknown"
    return ns_application.planningPermissionApplicationIdentificationType(  # 3.1.1.1
        localID=[
            ns_objektwesen.namedIdType(IdCategory="eBauNr", Id=ebau_nr)
        ],  # 3.1.1.1.1
        otherID=[
            ns_objektwesen.namedIdType(IdCategory="eBauNr", Id=ebau_nr)
        ],  # 3.1.1.1.2
        dossierIdentification=str(instance.instance_id),  # 3.1.1.1.3
    )


def status_notification(instance: Instance):
    return ns_application.eventStatusNotificationType(
        eventType="status notification",
        planningPermissionApplicationIdentification=permission_application_identification(
            instance
        ),
        status="in progress",  # real status is in remark
        remark=[
            assure_string_length(
                str(instance.instance_state.get_name()), max_length=950
            )
        ],
    )


class BaseDeliveryFormatter:
    def format_base_delivery(self, instance: Instance):
        """Make a well formatted baseDeliveryType from MasterData ready config."""

        responsible_service = instance.responsible_service(filter_type="municipality")

        md = MasterData(instance.case)

        return ns_application.eventBaseDeliveryType(
            planningPermissionApplicationInformation=[
                (
                    pyxb.BIND(
                        planningPermissionApplication=application(instance),
                        relationshipToPerson=format_relationships_to_persons(md),
                        decisionAuthority=decision_authority(
                            responsible_service,
                            organization_category=md.organization_category,
                        ),
                        entryOffice=office(
                            responsible_service,
                            organization_category=md.organization_category,
                        ),
                    )
                )
            ]
        )


def submit(instance: Instance, event_type: str = "submit"):
    # Submit with master data conforming answer processing.
    return ns_application.eventSubmitPlanningPermissionApplicationType(
        eventType=ns_application.eventTypeType(event_type),
        planningPermissionApplication=application(instance),
        relationshipToPerson=format_relationships_to_persons(MasterData(instance.case)),
    )


def person_to_ech0129_personIdentifcationType(person):
    pers_identification = ech_0044_4_1.personIdentificationLightType(
        officialName=assure_string_length(person.get("last_name", ""), max_length=30),
        firstName=assure_string_length(person.get("first_name", ""), max_length=30),
    )
    org_identification = None
    if person["is_juristic_person"]:
        pers_identification = None
        org_identification = ns_company_identification.organisationIdentificationType(
            organisationName=assure_string_length(
                person.get("juristic_name", ""), max_length=255
            ),
            organisationAdditionalName=assure_string_length(
                f'{person.get("first_name", "")} {person.get("last_name", "")}'.strip(),
                max_length=255,
            ),
            uid=ns_company_identification.uidStructureType(
                # We don't bother with UIDs
                uidOrganisationIdCategorie="CHE",
                uidOrganisationId="123123123",
            ),
            localOrganisationId=ns_company_identification.namedOrganisationIdType(
                organisationIdCategory="unknown", organisationId="unknown"
            ),
            legalForm="0223",
        )

    return ns_objektwesen.personType(
        identification=pyxb.BIND(
            personIdentification=pers_identification,
            organisationIdentification=org_identification,
        ),
        address=ns_address.addressInformationType(
            street=assure_string_length(person.get("street", ""), max_length=60),
            houseNumber=assure_string_length(
                person.get("street_number", "0"), max_length=12
            ),
            town=assure_string_length(
                ns_address.townType(person.get("town", "")), max_length=40
            ),
            swissZipCode=get_zip(person.get("zip", "")),
            country="CH",
        ),
    )


def format_relationships_to_persons(md: MasterData):
    # map eCH-0211 attribute names to master data keys
    role_map = {
        "applicant": "applicants",
        "contact": "legal_representatives",
        "project author": "project_authors",
        "landowner": "landowners",
    }
    relationships = list(
        itertools.chain(
            *[
                [
                    ns_application.relationshipToPersonType(
                        role=role,
                        person=person_to_ech0129_personIdentifcationType(person),
                    )
                    for person in getattr(md, mapped_to)
                ]
                for role, mapped_to in role_map.items()
            ]
        )
    )
    return relationships


def directive(comment, deadline=None):
    # Instruction can be one of
    #  - "process"
    #  - "external_process"
    #  - "information"
    #  - "comment"
    #  - "approve"
    #  - "sign"
    #  - "send"
    #  - "complete"
    return ns_nachrichten_t2.directiveType(
        uuid="00000000-0000-0000-0000-000000000000",
        instruction="process",
        priority="undefined",
        comments=comment,
        deadline=deadline.date() if deadline else None,
    )


def request(
    instance: Instance, event_type: str, comment=None, deadline=None, attachments=None
):
    return ns_application.eventRequestType(
        eventType=ns_application.eventTypeType(event_type),
        planningPermissionApplicationIdentification=permission_application_identification(
            instance
        ),
        directive=directive(comment, deadline) if comment else None,
        document=get_documents(attachments) if attachments else None,
    )


def accompanying_report(
    instance: Instance,
    event_type: str,
    attachments: List[Attachment],
    inquiry: WorkItem,
):
    judgement_mapping = {
        settings.DISTRIBUTION["ANSWERS"]["STATUS"]["POSITIVE"]: 1,
        settings.DISTRIBUTION["ANSWERS"]["STATUS"]["NEGATIVE"]: 4,
        settings.DISTRIBUTION["ANSWERS"]["STATUS"]["NOT_INVOLVED"]: 1,
        settings.DISTRIBUTION["ANSWERS"]["STATUS"]["CLAIM"]: 4,
        settings.DISTRIBUTION["ANSWERS"]["STATUS"]["UNKNOWN"]: None,
    }

    status = inquiry.child_case.document.answers.get(
        question_id=settings.DISTRIBUTION["QUESTIONS"]["STATUS"]
    )

    def prepare_notice(answer):
        if not answer:
            return []

        return [assure_string_length(handle_string_values(answer), max_length=950)]

    return ns_application.eventAccompanyingReportType(
        eventType=ns_application.eventTypeType(event_type),
        planningPermissionApplicationIdentification=permission_application_identification(
            instance
        ),
        document=get_documents(attachments),
        remark=prepare_notice(
            find_answer(
                inquiry.child_case.document,
                settings.DISTRIBUTION["QUESTIONS"]["STATEMENT"],
            )
        ),
        ancillaryClauses=prepare_notice(
            find_answer(
                inquiry.child_case.document,
                settings.DISTRIBUTION["QUESTIONS"]["ANCILLARY_CLAUSES"],
            )
        ),
        judgement=judgement_mapping.get(status.value),
    )


def change_responsibility(instance: Instance):
    prev_municipality = (
        instance.instance_services.filter(
            active=0,
            **(
                settings.APPLICATION.get("ACTIVE_SERVICES", {})
                .get("MUNICIPALITY", {})
                .get("FILTERS", {})
            ),
        )
        .order_by("-pk")
        .first()
        .service
    )
    municipality = instance.responsible_service(filter_type="municipality")
    return ns_application.eventChangeResponsibilityType(
        eventType=ns_application.eventTypeType("change responsibility"),
        planningPermissionApplicationIdentification=permission_application_identification(
            instance
        ),
        entryOffice=office(prev_municipality, organization_category="ebaube"),
        responsibleDecisionAuthority=decision_authority(
            municipality, organization_category="ebaube"
        ),
    )


def delivery(
    instance: Instance,
    subject: str,
    message_type: str,
    config: str = None,
    message_date=None,
    message_id=None,
    url=None,
    **args,
):
    """
    Generate delivery XML.

    General calling convention:
    >>> delivery(instance, subject, *delivery_type=delivery_data)

    To generate a base delivery, call this:
    >>> delivery(instance, subject, eventBaseDelivery=base_delivery(instance))
    """
    assert len(args) == 1, "Exactly one delivery param required"

    try:
        return ns_application.delivery(
            deliveryHeader=ech_0058_5_0.headerType(
                senderId=settings.APPLICATION["DOSSIER_IMPORT"]["PROD_URL"],
                messageId=message_id or str(id(instance)),
                messageType=message_type,
                sendingApplication=pyxb.BIND(
                    manufacturer=camac_metadata.__author__,
                    product=camac_metadata.__title__,
                    productVersion=clean_version(camac_metadata.__version__),
                ),
                subject=subject,
                messageDate=message_date or timezone.now(),
                action="1",
                testDeliveryFlag=settings.ENV != "production",
            ),
            **args,
        )
    except (
        IncompleteElementContentError,
        UnprocessedElementContentError,
    ) as e:  # pragma: no cover
        logger.error(e.details())
        raise


def decision_authority(service, organization_category=None):
    return ns_application.decisionAuthorityInformationType(
        decisionAuthority=ns_objektwesen.buildingAuthorityType(
            buildingAuthorityIdentificationType=authority(
                service, organization_category=organization_category
            ),
            # description minOccurs=0
            # shortDescription minOccurs=0
            # contactPerson minOccurs=0
            # contact minOccurs=0
            address=ns_address.addressInformationType(
                town=assure_string_length(
                    service.get_trans_attr("city") or "unknown", max_length=40
                ),
                swissZipCode=service.zip,
                street=assure_string_length(service.address, max_length=60),
                country="CH",
            ),
        )
    )


class CantonSpecific:
    @classmethod
    @canton_aware
    def decision_ruling(cls, instance, md):  # pragma: no cover
        raise RuntimeError("not implemented")

    @classmethod
    def determine_decision_state_sz(cls, instance: Instance):
        """Retrieve decision state and related things.

        eCH defines decision in 3.4 complete with properties
            - judgement
            - date
            - ruling
            - rulingAuthority

        where no decision module exists (such as the decision form in BE) these have
        to be collected from different locations, usually a combination of work-item
        and history entry.

        rulings are a set of categories such as 'building-permit' and
        'preliminary-clarification' (or assessment) to which the various
        form-slugs should be assigned (-v2, ...)
        """
        # one of "positive", "conditionally-positive", "negative", "rejected"

        decision_wi = instance.case.work_items.filter(task_id="make-decision").first()
        if decision_wi:
            if decision_wi.status == WorkItem.STATUS_CANCELED:
                return ECH_JUDGEMENT_DECLINED, MasterData(instance.case).decision_date
            if decision_wi.status == WorkItem.STATUS_COMPLETED:
                return ECH_JUDGEMENT_APPROVED, MasterData(instance.case).decision_date

        # Rejection should only be considered if no positive decision exists
        if instance.case.work_items.filter(  # pragma: no cover
            # TODO: Cover this after confirmation that it's correct
            task_id="reject-form",
            status=WorkItem.STATUS_COMPLETED,
        ).first():
            # Get date from history
            decision_date = (
                instance.history.filter(
                    # CAVEAT: when changing translation this must be updated to reflect the changes
                    trans__language="de",
                    trans__title="Dossier zurückgewiesen",
                )
                .order_by("-created_at")
                .first()
                .created_at
            )
            return ECH_JUDGEMENT_WRITTEN_OFF, decision_date
        return None, None

    @classmethod
    def decision_ruling_sz(cls, instance, md):
        judgement, judgement_date = cls.determine_decision_state_sz(instance)

        if not judgement_date:
            return []

        ruling = (
            instance.form.get_name()
        )  # TODO: is this valid for Entscheid/ruling 3.4.1.2?

        return [
            ns_application.decisionRulingType(
                judgement=judgement,
                date=judgement_date,
                ruling=ruling.upper(),
                rulingAuthority=authority(
                    instance.responsible_service(filter_type="municipality"),
                    organization_category=md.organization_category,
                ),
            )
        ]

    @classmethod
    def decision_ruling_be(cls, instance, md):
        caluma_workflow_slug = instance.case.workflow.slug
        work_item = instance.case.work_items.filter(
            task_id="decision",
            status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
        ).first()

        if not work_item:
            return []

        answers = work_item.document.answers.all()

        decision = (
            answers.filter(question_id=settings.DECISION["QUESTIONS"]["DECISION"])
            .first()
            .value
        )
        date = (
            answers.filter(question_id=settings.DECISION["QUESTIONS"]["DATE"])
            .first()
            .date
        )
        ruling = (
            answers.filter(question_id=settings.DECISION["QUESTIONS"]["APPROVAL_TYPE"])
            .first()
            .value
            if caluma_workflow_slug == "building-permit"
            else "VORABKLAERUNG"
        )

        return [
            ns_application.decisionRulingType(
                judgement=decision_to_judgement(decision, caluma_workflow_slug),
                date=date,
                ruling=ruling,
                rulingAuthority=authority(
                    instance.responsible_service(filter_type="municipality"),
                    organization_category="ebaube",
                ),
            )
        ]

    @classmethod
    @canton_aware
    def building_information(cls, instance, md):
        raise RuntimeError("not implemented")  # pragma: no cover

    @classmethod
    def building_information_sz(cls, instance, md):
        # currently not implemented
        return []

    @classmethod
    def building_information_be(cls, instance, md):
        document = instance.case.document

        return [
            ns_application.buildingInformationType(
                building=ns_objektwesen.buildingType(
                    EGID=find_answer(document, "gwr-egid") or 900000000,
                    numberOfFloors=find_answer(document, "effektive-geschosszahl"),
                    civilDefenseShelter=handle_ja_nein_bool(
                        find_answer(document, "sammelschutzraum")
                    ),
                    buildingCategory=1040,  # TODO: map category to GWR categories
                    # We don't want to map the heatings, hence omitting
                    # heating=[
                    #     ns_person.heatingType(
                    #         heatGeneratorHeating=7410,
                    #         energySourceHeating=7511,
                    #     )
                    #     for heating in answers.get("feuerungsanlagen", [])[:2]
                    # ],  # eCH only accepts 2 heatingTypes
                )
            )
        ]
