# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_gwr_data_ur 1'] = {
    'client': {
        'address': {
            'country': 'Schweiz',
            'houseNumber': 123,
            'street': 'Teststrasse',
            'swissZipCode': 1233,
            'town': 'Musterdorf'
        },
        'identification': {
            'isOrganisation': True,
            'organisationIdentification': {
                'organisationName': 'ACME AG'
            },
            'personIdentification': {
                'firstName': 'Max',
                'officialName': 'Mustermann'
            }
        }
    },
    'constructionLocalisation': {
        'municipalityName': 'Altdorf'
    },
    'constructionProjectDescription': 'Grosses Haus',
    'officialConstructionProjectFileNo': '1201-21-003',
    'projectAnnouncementDate': '2021-07-16',
    'realestateIdentification': {
        'EGRID': 'CH123456789',
        'number': 123456789
    },
    'totalCostsOfProject': 129000,
    'typeOfConstruction': None,
    'typeOfConstructionProject': 6011
}
