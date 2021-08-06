# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_gwr_data_ur 1'] = {
    'client': {
        'address': {
            'country': None,
            'houseNumber': None,
            'street': None,
            'swissZipCode': None,
            'town': None
        },
        'identification': {
            'isOrganisation': True,
            'organisationIdentification': {
                'organisationName': None
            },
            'personIdentification': {
                'firstName': None,
                'officialName': None
            }
        }
    },
    'constructionLocalisation': {
        'municipalityName': 'Musterhausen'
    },
    'constructionProjectDescription': 'Neues Haus',
    'officialConstructionProjectFileNo': '1200-00-00',
    'projectAnnouncementDate': '2021-07-16',
    'realestateIdentification': {
        'EGRID': '12345',
        'number': '2021-07-15T08:00:06Z'
    },
    'totalCostsOfProject': None,
    'typeOfConstruction': None,
    'typeOfConstructionProject': 6011
}
