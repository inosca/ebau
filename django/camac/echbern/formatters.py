"""
Helpers for exporting instance data to eCH-0211.

Note: This is currently only structurally an export,
it doesn't really render any data from the instance
to the XML just yet. This will need to be done at a
later point in time

"""


import pyxb

from camac.instance.models import Instance

from .schema import (
    ech_0007_6_0,
    ech_0010_6_0 as ns_address,
    ech_0044_4_1,
    ech_0058_5_0,
    ech_0097_2_0,
    ech_0129_5_0 as ns_person,
    ech_0147_t0_1 as ns_document,
    ech_0211_2_0 as ns_application,
)


def application(instance: Instance, answers: dict):
    nature_risk = None
    if "beschreibung-der-prozessart-tabelle" in answers:
        nature_risk = [
            ns_application.natureRiskType(
                riskDesignation=row["prozessart"], riskExists=True
            )
            for row in answers["beschreibung-der-prozessart-tabelle"]
        ]

    return ns_application.planningPermissionApplicationType(
        description=answers.get("beschreibung-bauvorhaben"),
        applicationType=instance.form.get_name(),
        # remark minOccurs=0
        # proceedingType minOccurs=0
        # profilingYesNo minOccurs=0
        # profilingDate minOccurs=0
        # intendedPurpose minOccurs=0
        # parkingLotsYesNo minOccurs=0
        # natureRisk minOccurs=0
        natureRisk=nature_risk,
        constructionCost=answers.get("baukosten-in-chf"),
        # publication minOccurs=0
        # namedMetaData  minOccurs=0
        locationAddress=ns_address.swissAddressInformationType(
            # addressLine1 minOccurs=0
            # addressLine2 minOccurs=0
            town="Bern",
            swissZipCode="3005",
            country="CH",
        ),
        realestateInformation=[
            ns_application.realestateInformationType(
                realestate=ns_person.realestateType(
                    realestateIdentification=ns_person.realestateIdentificationType(
                        # EGRID minOccurs=0
                        number="1234"
                        # numberSuffix minOccurs=0
                        # subDistrict minOccurs=0
                        # lot minOccurs=0
                    ),
                    # authority minOccurs=0
                    # date minOccurs=0
                    realestateType="5",  # mapping?
                    # cantonalSubKind minOccurs=0
                    # status minOccurs=0
                    # mutnumber minOccurs=0
                    # identDN minOccurs 0
                    # squareMeasure minOccurs 0
                    # realestateIncomplete minOccurs 0
                    # coordinates minOccurs 0
                    # namedMetaData minOccurs 0
                ),
                municipality=ech_0007_6_0.swissMunicipalityType(
                    # municipalityId minOccurs 0
                    municipalityName="Bern",
                    cantonAbbreviation="BE",
                ),
                # buildingInformation minOccurs=0
                # placeName  minOccurs=0
                owner=[
                    pyxb.BIND(
                        # ownerIdentification minOccurs=0
                        ownerAdress=ns_address.mailAddressType(
                            person=ns_address.personMailAddressInfoType(
                                mrMrs="1",  # mapping?
                                title="Dr Med",
                                firstName="David",
                                lastName="Vogt",
                            ),
                            addressInformation=ns_address.addressInformationType(
                                # not the same as swissAddressInformationType (obv..)
                                # addressLine1 minOccurs=0
                                # addressLine2 minOccurs=0
                                # (street, houseNumber, dwellingNumber) minOccurs=0
                                # (postOfficeBoxNumber, postOfficeBoxText) minOccurs=0
                                # locality minOccurs=0
                                town=ns_address.townType("Bern"),
                                swissZipCode="3007",
                                # foreignZipCode minOccurs=0
                                country="CH",
                            ),
                        )
                    )
                ],
            )
        ],
        # zone minOccurs=0
        # constructionProjectInformation minOccurs=0
        # directive  minOccurs=0
        # decisionRuling minOccurs=0
        document=[
            ns_document.documentType(
                uuid="12341234-1341234-1234123",  # oder so, todo
                titles=pyxb.BIND(title="foobar"),
                status="signed",  # ech0039 documentStatusType
                files=pyxb.BIND(
                    file=[
                        pyxb.BIND(
                            pathFileName="/foo/bar/asdf.pdf",
                            mimeType="application/pdf",
                            # internalSortOrder minOccurs=0
                            # version minOccurs=0
                            # hashCode minOccurs=0
                            # hashCodeAlgorithm minOccurs=0
                        )
                    ]
                ),
            )
        ],
        # referencedPlanningPermissionApplication minOccurs=0
        planningPermissionApplicationIdentification=ns_application.planningPermissionApplicationIdentificationType(
            localID=[pyxb.BIND(IdCategory="Category", Id="ID")],  # TODO: WHAT
            otherID=[pyxb.BIND(IdCategory="Category", Id="ID")],  # TODO: WHAT
            dossierIdentification=str(instance.instance_id),
        ),
    )


def office(instance: Instance):
    return ns_application.entryOfficeType(
        entryOfficeIdentification=ech_0097_2_0.organisationIdentificationType(
            # uid minOccurs=0
            localOrganisationId=ech_0097_2_0.namedOrganisationIdType(
                organisationIdCategory="blah", organisationId="1234"
            ),
            organisationName="asfdasdfasdf"
            # organisationLegalName minOccurs=0
            # organisationAdditionalName minOccurs=0
            # legalForm minOccurs=0
        ),
        municipality=ech_0007_6_0.swissMunicipalityType(
            # municipalityId minOccurs 0
            municipalityName="Bern",
            cantonAbbreviation="BE",
        ),
    )


def base_delivery(instance: Instance, answers: dict):

    return ns_application.eventBaseDeliveryType(
        planningPermissionApplicationInformation=[
            (
                pyxb.BIND(
                    planningPermissionApplication=application(instance, answers),
                    relationshipToPerson=[
                        ns_application.relationshipToPersonType(
                            role="applicant", person=requestor(instance)
                        )
                    ],
                    decisionAuthority=decision_authority(instance),
                    entryOffice=office(instance),
                )
            )
        ]
    )


def delivery(instance: Instance, answers: dict, **args):
    """
    Generate delivery XML.

    General calling convention:
    >>> delivery(instance, answers, *delivery_type=delivery_data)

    To generate a base delivery, call this:
    >>> delivery(inst, answers, eventBaseDelivery=base_delivery(inst))
    """
    assert len(args) == 1, "Exactly one delivery param required"

    message_types = {"eventBaseDelivery": "5100000"}
    message_type = message_types[list(args.keys())[0]]

    return ns_application.delivery(
        deliveryHeader=ech_0058_5_0.headerType(
            senderId="https://ebau.apps.be.ch",
            messageId=str(id(instance)),
            messageType=message_type,
            sendingApplication=pyxb.BIND(
                manufacturer="Adfinis SyGroup AG",
                product="CAMAC",
                productVersion="2019-09-25",
            ),
            subject=instance.form.get_name(),
            messageDate="2019-09-25T00:00:00.00Z",
            action="1",
            testDeliveryFlag=True,
        ),
        **args,
    )


def decision_authority(instance: Instance):
    return ns_application.decisionAuthorityInformationType(
        decisionAuthority=ns_person.buildingAuthorityType(
            buildingAuthorityIdentificationType=ech_0097_2_0.organisationIdentificationType(
                # uid minOccurs=0
                localOrganisationId=ech_0097_2_0.namedOrganisationIdType(
                    organisationIdCategory="blah", organisationId="1234"
                ),
                organisationName="Gemeinde Bern",
            ),
            # description minOccurs=0
            # shortDescription minOccurs=0
            # contactPerson minOccurs=0
            # contact minOccurs=0
            # address minOccurs=0
        )
    )


def requestor(instance: Instance):
    return ns_person.personType(
        identification=pyxb.BIND(
            personIdentification=ech_0044_4_1.personIdentificationLightType(
                officialName="Vogt", firstName="David"
            )
        )
    )
