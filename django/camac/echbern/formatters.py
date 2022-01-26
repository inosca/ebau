"""Helpers for exporting instance data to eCH-0211."""


import logging
import re

import pyxb
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from pyxb import IncompleteElementContentError, UnprocessedElementContentError

from camac import camac_metadata
from camac.constants.kt_bern import QUESTION_EBAU_NR
from camac.core.models import Answer, DocxDecision
from camac.instance.models import Instance
from camac.utils import build_url

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
from .utils import decision_to_judgement, strip_whitespace

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
        return (
            "." if not len(value) else f"{value} {'.' * (min_length - len(value) - 1)}"
        )
    return value


def handle_coordinate_value(value):
    return round(float(value), 3)


def authority(service):
    return ns_company_identification.organisationIdentificationType(
        uid=ns_company_identification.uidStructureType(
            # We don't bother with UIDs
            uidOrganisationIdCategorie="CHE",
            uidOrganisationId="123123123",
        ),
        localOrganisationId=ns_company_identification.namedOrganisationIdType(
            organisationIdCategory="ebaube", organisationId=str(service.pk)
        ),
        organisationName=service.get_name(),
        legalForm="0223",
    )


def get_ebau_nr(instance):
    ebau_answer = Answer.objects.filter(
        question__pk=QUESTION_EBAU_NR, instance=instance
    ).first()
    if ebau_answer:
        return ebau_answer.answer


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
        for attachment in attachments
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
        decisionRuling=[
            decision_ruling(instance, decision, answers)
            for decision in DocxDecision.objects.filter(instance=instance)
        ],
        document=get_documents(instance.attachments.all()),
        referencedPlanningPermissionApplication=[
            permission_application_identification(i) for i in related_instances
        ],
        planningPermissionApplicationIdentification=permission_application_identification(
            instance
        ),
    )


def decision_ruling(instance, decision, answers):
    ruling = decision.decision_type
    if answers["ech-subject"] in ["Einfache Vorabklärung", "Vollständige Vorabklärung"]:
        ruling = "VORABKLAERUNG"
    return ns_application.decisionRulingType(
        judgement=decision_to_judgement(
            decision.decision, answers["caluma-workflow-slug"]
        ),
        date=decision.decision_date,
        ruling=ruling,
        rulingAuthority=authority(
            instance.responsible_service(filter_type="municipality")
        ),
    )


def office(service):
    return ns_application.entryOfficeType(
        entryOfficeIdentification=authority(service),
        municipality=ech_0007_6_0.swissMunicipalityType(
            # municipalityId minOccurs 0
            municipalityName=assure_string_length(
                service.get_trans_attr("city") or "unknown", max_length=40
            ),
            cantonAbbreviation="BE",
        ),
    )


def permission_application_identification(instance: Instance):
    ebau_nr = get_ebau_nr(instance) or "unknown"
    return ns_application.planningPermissionApplicationIdentificationType(
        localID=[ns_objektwesen.namedIdType(IdCategory="eBauNr", Id=ebau_nr)],
        otherID=[ns_objektwesen.namedIdType(IdCategory="eBauNr", Id=ebau_nr)],
        dossierIdentification=str(instance.instance_id),
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


def base_delivery(instance: Instance, answers: AnswersDict):
    municipality = instance.responsible_service(filter_type="municipality")

    return ns_application.eventBaseDeliveryType(
        planningPermissionApplicationInformation=[
            (
                pyxb.BIND(
                    planningPermissionApplication=application(instance, answers),
                    relationshipToPerson=get_relationship_to_person(answers),
                    decisionAuthority=decision_authority(municipality),
                    entryOffice=office(municipality),
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


def get_relationship_to_person(answers: AnswersDict):
    people = {"applicant": get_applicant_data(answers)}

    slug_map = [
        ("personalien-vertreterin-mit-vollmacht", "contact"),
        ("personalien-projektverfasserin", "project author"),
        ("personalien-grundeigentumerin", "landowner"),
    ]

    for slug, role in slug_map:
        form = answers.get(slug)
        if form:
            people[role] = normalize_personalien(form[0])

    return [
        ns_application.relationshipToPersonType(role=role, person=person_type(pers))
        for role, pers in people.items()
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


def get_applicant_data(answers):
    if "personalien-gesuchstellerin" in answers:
        pers_infos = answers["personalien-gesuchstellerin"][0]
        return {
            "vorname": pers_infos.get("vorname-gesuchstellerin"),
            "name": pers_infos.get("name-gesuchstellerin"),
            "strasse": pers_infos["strasse-gesuchstellerin"],
            "nummer": pers_infos.get("nummer-gesuchstellerin"),
            "ort": pers_infos["ort-gesuchstellerin"],
            "plz": pers_infos["plz-gesuchstellerin"],
            "juristische-person": pers_infos["juristische-person-gesuchstellerin"],
            "name-juristische-person": pers_infos.get(
                "name-juristische-person-gesuchstellerin"
            ),
        }

    # No value given (should not be possible)
    return {
        "vorname": None,
        "name": None,
        "strasse": None,
        "nummer": None,
        "ort": None,
        "plz": None,
        "juristische-person": "Nein",
    }


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
    attachments,
    circulation_answer,
    stellungnahme,
    nebenbestimmung,
):
    judgement_mapping = {
        "positive": 1,
        "negative": 4,
        "not_concerned": 1,
        "claim": 4,
        "unknown": None,
    }

    return ns_application.eventAccompanyingReportType(
        eventType=ns_application.eventTypeType(event_type),
        planningPermissionApplicationIdentification=permission_application_identification(
            instance
        ),
        document=get_documents(attachments),
        remark=[assure_string_length(stellungnahme, max_length=950)]
        if stellungnahme
        else [],
        ancillaryClauses=[assure_string_length(nebenbestimmung, max_length=950)]
        if nebenbestimmung
        else [],
        judgement=judgement_mapping.get(circulation_answer.name)
        if circulation_answer
        else None,
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
        entryOffice=office(prev_municipality),
        responsibleDecisionAuthority=decision_authority(municipality),
    )


def delivery(
    instance: Instance,
    answers: AnswersDict,
    message_type: str,
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
                senderId="https://ebau.apps.be.ch",
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


def decision_authority(service):
    return ns_application.decisionAuthorityInformationType(
        decisionAuthority=ns_objektwesen.buildingAuthorityType(
            buildingAuthorityIdentificationType=authority(service),
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
