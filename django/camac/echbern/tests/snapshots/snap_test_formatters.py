# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['test_office 1'] = '<?xml version="1.0" ?><office xmlns:ns1="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0097/2" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0007/6"><ns1:entryOfficeIdentification><ns2:uid><ns2:uidOrganisationIdCategorie>CHE</ns2:uidOrganisationIdCategorie><ns2:uidOrganisationId>123123123</ns2:uidOrganisationId></ns2:uid><ns2:localOrganisationId><ns2:organisationIdCategory>CHE</ns2:organisationIdCategory><ns2:organisationId>123123123</ns2:organisationId></ns2:localOrganisationId><ns2:organisationName>Leitbehörde Burgdorf</ns2:organisationName><ns2:legalForm>0223</ns2:legalForm></ns1:entryOfficeIdentification><ns1:municipality><ns3:municipalityName>Brandontown</ns3:municipalityName><ns3:cantonAbbreviation>BE</ns3:cantonAbbreviation></ns1:municipality></office>'

snapshots['test_get_documents[True-0] 1'] = [
    '''<?xml version="1.0" ?>
<doc xmlns:ns1="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0039/2">
\t<ns1:uuid>00000000-0000-0000-0000-000000000000</ns1:uuid>
\t<ns1:titles>
\t\t<ns2:title>dummy</ns2:title>
\t</ns1:titles>
\t<ns1:status>signed</ns1:status>
\t<ns1:files>
\t\t<ns1:file>
\t\t\t<ns1:pathFileName>unknown</ns1:pathFileName>
\t\t\t<ns1:mimeType>unknown</ns1:mimeType>
\t\t</ns1:file>
\t</ns1:files>
</doc>
'''
]

snapshots['test_get_documents[True-1] 1'] = [
    '''<?xml version="1.0" ?>
<doc xmlns:ns1="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0039/2">
\t<ns1:uuid>7604864d-fada-4431-b63b-fc9f4915233d</ns1:uuid>
\t<ns1:titles>
\t\t<ns2:title>baz</ns2:title>
\t</ns1:titles>
\t<ns1:status>signed</ns1:status>
\t<ns1:files>
\t\t<ns1:file>
\t\t\t<ns1:pathFileName>http://camac-ng.local/api/v1/attachments/files/?attachments=1</ns1:pathFileName>
\t\t\t<ns1:mimeType>message/partial</ns1:mimeType>
\t\t</ns1:file>
\t</ns1:files>
\t<ns1:documentKind/>
</doc>
'''
]

snapshots['test_get_documents[True-2] 1'] = [
    '''<?xml version="1.0" ?>
<doc xmlns:ns1="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0039/2">
\t<ns1:uuid>7604864d-fada-4431-b63b-fc9f4915233d</ns1:uuid>
\t<ns1:titles>
\t\t<ns2:title>baz</ns2:title>
\t</ns1:titles>
\t<ns1:status>signed</ns1:status>
\t<ns1:files>
\t\t<ns1:file>
\t\t\t<ns1:pathFileName>http://camac-ng.local/api/v1/attachments/files/?attachments=1</ns1:pathFileName>
\t\t\t<ns1:mimeType>message/partial</ns1:mimeType>
\t\t</ns1:file>
\t</ns1:files>
\t<ns1:documentKind/>
</doc>
''',
    '''<?xml version="1.0" ?>
<doc xmlns:ns1="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0039/2">
\t<ns1:uuid>23daf554-c2f5-4aa2-b5f2-734a96ed84d8</ns1:uuid>
\t<ns1:titles>
\t\t<ns2:title>baz</ns2:title>
\t</ns1:titles>
\t<ns1:status>signed</ns1:status>
\t<ns1:files>
\t\t<ns1:file>
\t\t\t<ns1:pathFileName>http://camac-ng.local/api/v1/attachments/files/?attachments=2</ns1:pathFileName>
\t\t\t<ns1:mimeType>text/vcard</ns1:mimeType>
\t\t</ns1:file>
\t</ns1:files>
\t<ns1:documentKind/>
</doc>
'''
]

snapshots['test_get_documents[False-0] 1'] = [
    '''<?xml version="1.0" ?>
<doc xmlns:ns1="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0039/2">
\t<ns1:uuid>00000000-0000-0000-0000-000000000000</ns1:uuid>
\t<ns1:titles>
\t\t<ns2:title>dummy</ns2:title>
\t</ns1:titles>
\t<ns1:status>signed</ns1:status>
\t<ns1:files>
\t\t<ns1:file>
\t\t\t<ns1:pathFileName>unknown</ns1:pathFileName>
\t\t\t<ns1:mimeType>unknown</ns1:mimeType>
\t\t</ns1:file>
\t</ns1:files>
</doc>
'''
]

snapshots['test_get_documents[False-1] 1'] = [
    '''<?xml version="1.0" ?>
<doc xmlns:ns1="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0039/2">
\t<ns1:uuid>7604864d-fada-4431-b63b-fc9f4915233d</ns1:uuid>
\t<ns1:titles>
\t\t<ns2:title>foo</ns2:title>
\t</ns1:titles>
\t<ns1:status>signed</ns1:status>
\t<ns1:files>
\t\t<ns1:file>
\t\t\t<ns1:pathFileName>http://camac-ng.local/api/v1/attachments/files/?attachments=1</ns1:pathFileName>
\t\t\t<ns1:mimeType>message/partial</ns1:mimeType>
\t\t</ns1:file>
\t</ns1:files>
\t<ns1:documentKind/>
</doc>
'''
]

snapshots['test_get_documents[False-2] 1'] = [
    '''<?xml version="1.0" ?>
<doc xmlns:ns1="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0039/2">
\t<ns1:uuid>7604864d-fada-4431-b63b-fc9f4915233d</ns1:uuid>
\t<ns1:titles>
\t\t<ns2:title>foo</ns2:title>
\t</ns1:titles>
\t<ns1:status>signed</ns1:status>
\t<ns1:files>
\t\t<ns1:file>
\t\t\t<ns1:pathFileName>http://camac-ng.local/api/v1/attachments/files/?attachments=1</ns1:pathFileName>
\t\t\t<ns1:mimeType>message/partial</ns1:mimeType>
\t\t</ns1:file>
\t</ns1:files>
\t<ns1:documentKind/>
</doc>
''',
    '''<?xml version="1.0" ?>
<doc xmlns:ns1="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns2="http://www.ech.ch/xmlns/eCH-0039/2">
\t<ns1:uuid>23daf554-c2f5-4aa2-b5f2-734a96ed84d8</ns1:uuid>
\t<ns1:titles>
\t\t<ns2:title>foo</ns2:title>
\t</ns1:titles>
\t<ns1:status>signed</ns1:status>
\t<ns1:files>
\t\t<ns1:file>
\t\t\t<ns1:pathFileName>http://camac-ng.local/api/v1/attachments/files/?attachments=2</ns1:pathFileName>
\t\t\t<ns1:mimeType>text/vcard</ns1:mimeType>
\t\t</ns1:file>
\t</ns1:files>
\t<ns1:documentKind/>
</doc>
'''
]
