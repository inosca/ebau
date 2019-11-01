# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots[
    "test_office 1"
] = '<?xml version="1.0" ?><office xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0097/2" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0007/6"><ns1:entryOfficeIdentification><ns2:uid><ns2:uidOrganisationIdCategorie>CHE</ns2:uidOrganisationIdCategorie><ns2:uidOrganisationId>123123123</ns2:uidOrganisationId></ns2:uid><ns2:localOrganisationId><ns2:organisationIdCategory>CHE</ns2:organisationIdCategory><ns2:organisationId>123123123</ns2:organisationId></ns2:localOrganisationId><ns2:organisationName>Leitbehörde Burgdorf</ns2:organisationName><ns2:legalForm>0223</ns2:legalForm></ns1:entryOfficeIdentification><ns1:municipality><ns3:municipalityName>Burgdorf</ns3:municipalityName><ns3:cantonAbbreviation>BE</ns3:cantonAbbreviation></ns1:municipality></office>'
