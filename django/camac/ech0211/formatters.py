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
from camac.constants.kt_schwyz import DECISION_JUDGEMENT
from camac.core.models import Answer
from camac.document.models import Attachment
from camac.instance.models import Instance
from camac.utils import build_url

from ..instance.master_data import MasterData
from .data_preparation import AnswersDict
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


def list_to_string(data, key, delimiter=", "):
    if key in data:
        return delimiter.join(data[key])


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
        return f"{value}{'.' * (min_length - len(value))}"
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


def get_ebau_nr(instance):
    return instance.case.meta.get("ebau-number")


def get_related_instances(instance, ebau_nr=None):
    ebau_nr = ebau_nr if ebau_nr else get_ebau_nr(instance)
    related_instances = []
    if ebau_nr:
        instance_pks = (
            Answer.objects.filter(question__trans__name="eBau-Nummer", answer=ebau_nr)
            .exclude(instance__pk=instance.pk)
            .select_related("instance")
            .values_list("instance", flat=True)
        )
        related_instances = Instance.objects.filter(pk__in=instance_pks)
    return related_instances


def get_document_sections(attachment):
    sections = [s.get_name() for s in attachment.attachment_sections.all()]
    return "; ".join(sections)


def get_plz(value):
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


def normalize_personalien(pers: dict):
    new_pers = {}
    for key, value in pers.items():
        new_key = key
        if "-" in key:
            new_key = "-".join(key.split("-")[:-1])
        new_pers[new_key] = value
    return new_pers


def get_owners(answers):
    """
    Get owners of the building.

    We use "personalien-grundeigentumerin" if available and fallback to
    "personalien-gesuchstellerin" if not.

    Then we normalize all the keys.
    :param answers: AnswersDict
    :return: dict
    """
    raw_owners = answers.get("personalien-grundeigentumerin")
    if not raw_owners:  # answers.get could return []
        raw_owners = answers.get("personalien-gesuchstellerin", [])
    owners = [normalize_personalien(o) for o in raw_owners]

    return owners


def get_realestateinformation(answers):
    owners = get_owners(answers)

    re_info = [
        ns_application.realestateInformationType(
            realestate=ns_objektwesen.realestateType(
                realestateIdentification=ns_objektwesen.realestateIdentificationType(
                    EGRID=parzelle.get("e-grid-nr"),
                    number=parzelle["parzellennummer"],
                    # numberSuffix minOccurs=0
                    # subDistrict minOccurs=0
                    # lot minOccurs=0
                ),
                # authority minOccurs=0
                # date minOccurs=0
                realestateType="8",  # mapping?
                # cantonalSubKind minOccurs=0
                # status minOccurs=0
                # mutnumber minOccurs=0
                # identDN minOccurs 0
                # squareMeasure minOccurs 0
                # realestateIncomplete minOccurs 0
                coordinates=ns_objektwesen.coordinatesType(
                    LV95=pyxb.BIND(
                        east=handle_coordinate_value(parzelle["lagekoordinaten-ost"]),
                        north=handle_coordinate_value(parzelle["lagekoordinaten-nord"]),
                        originOfCoordinates=904,
                    )
                )
                if all(
                    k in parzelle and parzelle[k]
                    for k in ("lagekoordinaten-ost", "lagekoordinaten-nord")
                )
                else None
                # namedMetaData minOccurs 0
            ),
            municipality=ech_0007_6_0.swissMunicipalityType(
                # municipalityId minOccurs 0
                municipalityName=assure_string_length(
                    answers["gemeinde"], max_length=40
                ),
                cantonAbbreviation="BE",
            ),
            buildingInformation=[
                ns_application.buildingInformationType(
                    building=ns_objektwesen.buildingType(
                        EGID=answers.get("gwr-egid"),
                        numberOfFloors=answers.get("effektive-geschosszahl"),
                        civilDefenseShelter=handle_ja_nein_bool(
                            answers.get("sammelschutzraum")
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
            ],
            # placeName  minOccurs=0
            owner=[
                pyxb.BIND(
                    # ownerIdentification minOccurs=0
                    ownerAdress=ns_address.mailAddressType(
                        person=ns_address.personMailAddressInfoType(
                            # mrMrs="1",  # mapping?
                            # title="Dr Med",
                            firstName=assure_string_length(
                                owner.get("vorname", "unknown"), max_length=30
                            ),
                            lastName=assure_string_length(
                                owner.get("name", "unknown"), max_length=30
                            ),
                        ),
                        addressInformation=ns_address.addressInformationType(
                            # not the same as swissAddressInformationType (obv..)
                            # addressLine1 minOccurs=0
                            # addressLine2 minOccurs=0
                            # (street, houseNumber, dwellingNumber) minOccurs=0
                            # (postOfficeBoxNumber, postOfficeBoxText) minOccurs=0
                            # locality minOccurs=0
                            street=assure_string_length(
                                owner.get("strasse"), max_length=60
                            ),
                            houseNumber=assure_string_length(
                                owner.get("nummer"), max_length=12
                            ),
                            town=assure_string_length(
                                ns_address.townType(owner["ort"]), max_length=40
                            ),
                            swissZipCode=get_plz(owner["plz"]),
                            # foreignZipCode minOccurs=0
                            country="CH",
                        ),
                    )
                )
                for owner in owners
            ],
        )
        for parzelle in answers.get("parzelle", [])
    ]

    if not re_info:
        # happens if no parcels are filled (preliminary clarification)
        re_info = [
            ns_application.realestateInformationType(
                realestate=ns_objektwesen.realestateType(
                    realestateIdentification=ns_objektwesen.realestateIdentificationType(
                        number="0"
                    ),
                    realestateType="8",
                    coordinates=None,
                ),
                municipality=ech_0007_6_0.swissMunicipalityType(
                    municipalityName=assure_string_length(
                        answers["gemeinde"], max_length=40
                    ),
                    cantonAbbreviation="BE",
                ),
                buildingInformation=[
                    ns_application.buildingInformationType(
                        building=ns_objektwesen.buildingType(
                            buildingCategory=1040  # TODO: map category to GWR categories
                        )
                    )
                ],
                owner=[
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
                ],
            )
        ]

    return re_info


def extract_street_number(string):
    """Very simple street number extractor.

    Split string at first digit if any.
    """
    split = list(re.split(r"(\d+)", string))
    if len(split) > 1:
        return "".join(split[1:])
    return ""


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


def determine_decision_state(instance: Instance):
    """Retrieve decision state and pertaining modalities.

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

    decision_task_id = "make-decision"
    if instance.case.work_items.filter(
        task_id=decision_task_id, status=WorkItem.STATUS_CANCELED
    ).first():
        return DECISION_JUDGEMENT["denied"], MasterData(instance.case).decision_date

    if instance.case.work_items.filter(
        task_id=decision_task_id, status=WorkItem.STATUS_COMPLETED
    ).first():
        return DECISION_JUDGEMENT["accepted"], MasterData(instance.case).decision_date

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
        judgement = 3
        return judgement, decision_date
    return None, None


def application_md(instance: Instance):
    """Create and format an application's properties based on the instance's MasterData."""
    md = MasterData(instance.case)
    if md.decision_date and not isinstance(
        md.decision_date, datetime.date
    ):  # pragma: no cover
        raise IncompleteElementContentError("Decision date is not a valid date.")

    judgement, judgement_date = determine_decision_state(instance)

    def format_decision_ruling_type(instance, judgement, judgement_date):
        ruling = (
            instance.form.get_name()
        )  # TODO: is this valid for Entscheid/ruling 3.4.1.2?
        return ns_application.decisionRulingType(
            judgement=judgement,
            date=judgement_date,
            ruling=ruling.upper(),
            rulingAuthority=authority(
                instance.responsible_service(filter_type="municipality"),
                organization_category=md.organization_category,
            ),
        )

    decision_ruling_type = format_decision_ruling_type(
        instance, judgement, judgement_date
    )

    realestate_info = [
        ns_application.realestateInformationType(
            realestate=ns_objektwesen.realestateType(  # eCH0129 4.8.1
                realestateIdentification=ns_objektwesen.realestateIdentificationType(
                    EGRID=plot.get("egrid_number", "unknown"),
                    number=str(plot.get("plot_number", "unknown")),
                ),
                realestateType="8",  # mentioned in swagger README
                coordinates=ns_objektwesen.coordinatesType(
                    LV95=pyxb.BIND(
                        east=handle_coordinate_value(plot.get("coord_east")),
                        north=handle_coordinate_value(plot.get("coord_north")),
                        originofCoordinates=904,
                    )
                )
                if all(k in plot and plot[k] for k in ["coord_east", "coord_north"])
                else None,
            ),
            municipality=ech_0007_6_0.swissMunicipalityType(
                # municipalityid minoccurs 0
                municipalityName=assure_string_length(md.municipality, max_length=40),
                cantonAbbreviation=settings.APPLICATION["SHORT_NAME"].upper(),
            ),
            owner=make_dummy_address_ech0044(),
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
                municipality=ech_0007_6_0.swissMunicipalityType(
                    municipalityName=assure_string_length(
                        md.municipality, max_length=40
                    ),
                    cantonAbbreviation=settings.APPLICATION["SHORT_NAME"].upper(),
                ),
                owner=make_dummy_address_ech0044(),
            )
        ]
    related_instances = Instance.objects.exclude(pk=instance.pk).filter(
        identifier=instance.identifier
    )
    planning_permission_application_type = ns_application.planningPermissionApplicationType(
        planningPermissionApplicationIdentification=permission_application_identification(
            instance
        ),  # 3.1.1.1
        description=assure_string_length(
            md.proposal, min_length=3, max_length=950
        ),  # 3.1.1.2
        applicationType=assure_string_length(
            md.application_type, max_length=100
        ),  # 3.1.1.3  #
        remark=[
            assure_string_length(md.remark, max_length=950)
        ],  # 3.1.1.4  TODO: verify!
        proceedingType=md.proceeding_type,  # 3.1.1.5
        profilingYesNo=isinstance(
            md.profile_approval_date, datetime.datetime
        ),  # 3.1.1.6
        profilingDate=None  # TODO: fix master_data for construction_control items returning []
        if not md.profile_approval_date
        else md.profile_approval_date[0],  # 3.1.1.7
        intendedPurpose=assure_string_length(md.usage_type, max_length=255),  # 3.1.1.8
        constructionCost=md.construction_costs,  # 3.1.1.11
        namedMetaData=[  # Erweiterungsfelder 3.1.1.14  TODO: verify!
            ns_objektwesen.namedMetaDataType(
                metaDataName="status", metaDataValue=instance.instance_state.get_name()
            )
        ],
        locationAddress=ns_address.swissAddressInformationType(  # 3.1.1.15
            houseNumber=assure_string_length(
                getattr(md, "street", "") and extract_street_number(md.street) or "",
                max_length=12,  # TODO: split street at first number
            ),
            street=assure_string_length(
                getattr(md, "street", "unknown"), max_length=60
            ),
            town=assure_string_length(getattr(md, "city", "unknown"), max_length=40),
            swissZipCode=get_plz(getattr(md, "plz", 0000)),
            country="CH",
        ),
        realestateInformation=realestate_info,  # TODO: 3.1.1.16 incl subtype
        referencedPlanningPermissionApplication=[
            permission_application_identification(i) for i in related_instances
        ],  # Referenzierte Baugesuche 3.1.1.22 TODO: verify!
        document=get_documents(instance.attachments.all()),  # 3.2
        decisionRuling=[decision_ruling_type]
        if judgement_date
        else [],  # TODO: verify Verfügung 3.4
        zone=[  # TODO: 3.8
            ns_application.zoneType(
                zoneDesignation=assure_string_length(md.usage_zone, max_length=255)
            )
        ]
        if md.usage_zone
        else [],  # eCH allows for max 225 chars
    )
    return planning_permission_application_type


def application(instance: Instance, answers: AnswersDict):
    nature_risk = []
    if "beschreibung-der-prozessart-tabelle" in answers:
        nature_risk = [
            ns_application.natureRiskType(
                riskDesignation=assure_string_length(row["prozessart"], max_length=255),
                riskExists=True,
            )
            for row in answers.get("beschreibung-der-prozessart-tabelle", [])
        ]

    ebau_nr = get_ebau_nr(instance)
    related_instances = get_related_instances(instance, ebau_nr)

    return ns_application.planningPermissionApplicationType(
        description=assure_string_length(
            answers.get("beschreibung-bauvorhaben", "unknown"),
            min_length=3,
            max_length=950,
        ),
        applicationType=assure_string_length(answers["ech-subject"], max_length=100),
        remark=[assure_string_length(answers["bemerkungen"], max_length=950)]
        if "bemerkungen" in answers
        else [],
        # proceedingType minOccurs=0
        # profilingYesNo minOccurs=0
        # profilingDate minOccurs=0
        intendedPurpose=assure_string_length(
            list_to_string(answers, "nutzungsart"), max_length=255
        ),
        parkingLotsYesNo=answers.get("anzahl-abstellplaetze-fur-motorfahrzeuge", 0) > 0,
        natureRisk=nature_risk,
        constructionCost=get_cost(answers.get("baukosten-in-chf")),
        # publication minOccurs=0
        namedMetaData=[
            ns_objektwesen.namedMetaDataType(
                metaDataName="status", metaDataValue=instance.instance_state.get_name()
            )
        ],
        locationAddress=ns_address.swissAddressInformationType(
            # addressLine1 minOccurs=0
            # addressLine2 minOccurs=0
            houseNumber=assure_string_length(answers.get("nr", "0"), max_length=12),
            street=assure_string_length(
                answers.get("strasse-flurname", "unknown"), max_length=60
            ),
            town=assure_string_length(
                answers.get("ort-grundstueck", "unknown"), max_length=40
            ),
            swissZipCode=get_plz(answers.get("plz")),
            country="CH",
        ),
        realestateInformation=get_realestateinformation(answers),
        zone=[
            ns_application.zoneType(
                zoneDesignation=assure_string_length(
                    answers["nutzungszone"], max_length=255
                )
            )
        ]  # eCH allows for max 225 chars
        if "nutzungszone" in answers and answers["nutzungszone"] is not None
        else [],
        constructionProjectInformation=ns_application.constructionProjectInformationType(
            constructionProject=ns_objektwesen.constructionProject(
                status=6701,  # we always send this. The real status is in namedMetaData
                description=assure_string_length(
                    answers.get("beschreibung-bauvorhaben", "unknown"),
                    min_length=3,
                    max_length=1000,
                ),
                projectStartDate=answers.get("geplanter-baustart"),
                durationOfConstructionPhase=answers.get("dauer-in-monaten"),
                totalCostsOfProject=get_cost(answers.get("baukosten-in-chf")),
            ),
            municipality=ech_0007_6_0.swissMunicipalityType(
                municipalityName=assure_string_length(
                    answers["parzelle"][0].get("ort-parzelle", answers["gemeinde"]),
                    max_length=40,
                ),
                cantonAbbreviation="BE",
            )
            if "parzelle" in answers
            else None,
        ),
        # directive  minOccurs=0
        decisionRuling=decision_ruling(
            instance,
            answers["caluma-workflow-slug"],
        ),
        document=get_documents(instance.attachments.all()),
        referencedPlanningPermissionApplication=[
            permission_application_identification(i) for i in related_instances
        ],
        planningPermissionApplicationIdentification=permission_application_identification(
            instance
        ),
    )


def decision_ruling(instance, caluma_workflow_slug):
    work_item = instance.case.work_items.filter(
        task_id="decision",
        status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
    ).first()

    if not work_item:
        return []

    answers = work_item.document.answers.all()

    decision = (
        answers.filter(question_id=settings.DECISION["QUESTION_SLUG"]).first().value
    )
    date = answers.filter(question_id="decision-date").first().date
    ruling = (
        answers.filter(question_id="decision-approval-type").first().value
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


def office(service, organization_category=None, canton="BE"):
    return ns_application.entryOfficeType(
        entryOfficeIdentification=authority(
            service, organization_category=organization_category
        ),
        municipality=ech_0007_6_0.swissMunicipalityType(
            # municipalityId minOccurs 0
            municipalityName=assure_string_length(
                service.get_trans_attr("city") or "unknown", max_length=40
            ),
            cantonAbbreviation=canton,
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
    def __init__(self, config):
        self.config = config

    def _caluma_config(self, instance: Instance, answers: AnswersDict):
        """
        Make a well formatted baseDeliveryType from caluma workflow based config.

        Supported config:
         - kt_bern
        """
        municipality = instance.responsible_service(filter_type="municipality")
        organization_category = "ebaube"  # TODO: put this some better place

        return ns_application.eventBaseDeliveryType(
            planningPermissionApplicationInformation=[
                (
                    pyxb.BIND(
                        planningPermissionApplication=application(instance, answers),
                        relationshipToPerson=get_relationship_to_person(answers),
                        decisionAuthority=decision_authority(
                            municipality, organization_category=organization_category
                        ),
                        entryOffice=office(
                            municipality,
                            organization_category=organization_category,
                            canton="BE",
                        ),
                    )
                )
            ]
        )

    def _masterdata_config(self, instance: Instance):
        """
        Make a well formatted baseDeliveryType from MasterData ready config.

        Supported config:
         - kt_schwyz
        """
        responsible_service = instance.group.service

        md = MasterData(instance.case)

        return ns_application.eventBaseDeliveryType(
            planningPermissionApplicationInformation=[
                (
                    pyxb.BIND(
                        planningPermissionApplication=application_md(instance),
                        relationshipToPerson=format_relationships_to_persons(md),
                        decisionAuthority=decision_authority(
                            responsible_service,
                            organization_category=md.organization_category,
                        ),
                        entryOffice=office(
                            responsible_service,
                            organization_category=md.organization_category,
                            canton=settings.APPLICATION["SHORT_NAME"].upper(),
                        ),
                    )
                )
            ]
        )

    def format_base_delivery(self, instance: Instance, **kwargs):
        avaliable_configs = {
            "kt_bern": self._caluma_config,
            "kt_schwyz": self._masterdata_config,
        }
        return avaliable_configs[self.config](instance, **kwargs)


def base_delivery(instance: Instance, answers: AnswersDict):  # pragma: no cover
    municipality = instance.responsible_service(filter_type="municipality")

    return ns_application.eventBaseDeliveryType(
        planningPermissionApplicationInformation=[
            (
                pyxb.BIND(
                    planningPermissionApplication=application(instance, answers),
                    relationshipToPerson=get_relationship_to_person(answers),
                    decisionAuthority=decision_authority(municipality),
                    entryOffice=office(
                        municipality, organization_category="ebaube", canton="BE"
                    ),
                )
            )
        ]
    )


def submit(instance: Instance, answers: AnswersDict, event_type: str):
    return ns_application.eventSubmitPlanningPermissionApplicationType(
        eventType=ns_application.eventTypeType(event_type),
        planningPermissionApplication=application(instance, answers),
        relationshipToPerson=get_relationship_to_person(answers),
    )


def submit_md(instance: Instance, event_type: str = "submit"):
    # Submit with master data conforming answer processing.
    return ns_application.eventSubmitPlanningPermissionApplicationType(
        eventType=ns_application.eventTypeType(event_type),
        planningPermissionApplication=application_md(instance),
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
            houseNumber=assure_string_length("", max_length=12),
            town=assure_string_length(
                ns_address.townType(person.get("town", "")), max_length=40
            ),
            swissZipCode=get_plz(person.get("zip", "")),
            country="CH",
        ),
    )


def format_relationships_to_persons(md: MasterData):
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


def get_relationship_to_person(answers: AnswersDict):
    people = []

    slug_map = [
        ("personalien-gesuchstellerin", "applicant"),
        ("personalien-vertreterin-mit-vollmacht", "contact"),
        ("personalien-projektverfasserin", "project author"),
        ("personalien-grundeigentumerin", "landowner"),
    ]

    for slug, role in slug_map:
        form = answers.get(slug)
        if form:
            for row in form:
                people.append((role, normalize_personalien(row)))
        elif role == "applicant":
            # No applicant given (should not be possible)
            people.append(
                (
                    role,
                    {
                        "vorname": None,
                        "name": None,
                        "strasse": None,
                        "nummer": None,
                        "ort": None,
                        "plz": None,
                        "juristische-person": "Nein",
                    },
                )
            )

    return [
        ns_application.relationshipToPersonType(role=role, person=person_type(pers))
        for role, pers in people
    ]


def person_type(person):
    pers_identification = ech_0044_4_1.personIdentificationLightType(
        officialName=assure_string_length(person.get("name"), max_length=30),
        firstName=assure_string_length(person.get("vorname"), max_length=30),
    )
    org_identification = None
    if handle_ja_nein_bool(person["juristische-person"]):
        pers_identification = None
        org_identification = ns_company_identification.organisationIdentificationType(
            organisationName=assure_string_length(
                person["name-juristische-person"], max_length=255
            ),
            organisationAdditionalName=assure_string_length(
                f'{person.get("vorname", "")} {person.get("name", "")}'.strip(),
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
            street=assure_string_length(person["strasse"], max_length=60),
            houseNumber=assure_string_length(person.get("nummer"), max_length=12),
            town=assure_string_length(
                ns_address.townType(person["ort"]), max_length=40
            ),
            swissZipCode=get_plz(person["plz"]),
            country="CH",
        ),
    )


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
        entryOffice=office(
            prev_municipality, organization_category="ebaube", canton="BE"
        ),
        responsibleDecisionAuthority=decision_authority(
            municipality, organization_category="ebaube"
        ),
    )


def delivery(
    instance: Instance,
    answers: AnswersDict,
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
    >>> delivery(instance, answers, *delivery_type=delivery_data)

    To generate a base delivery, call this:
    >>> delivery(instance, answers, eventBaseDelivery=base_delivery(instance))
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
                subject=answers["ech-subject"],
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
