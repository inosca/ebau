# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_gwr_data_ur 1'] = {
    'buildingPermitIssueDate': '2021-07-20',
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
            'personIdentification': None
        }
    },
    'constructionLocalisation': {
        'municipalityName': 'Altdorf'
    },
    'constructionProjectDescription': 'Grosses Haus',
    'officialConstructionProjectFileNo': '1201-21-003',
    'projectAnnouncementDate': '2021-07-16',
    'projectCompletionDate': '2021-08-05',
    'projectStartDate': '2021-07-25',
    'realestateIdentification': {
        'EGRID': 'CH123456789',
        'number': 123456789
    },
    'totalCostsOfProject': 129000,
    'typeOfClient': 6161,
    'typeOfConstruction': 6235,
    'typeOfConstructionProject': 6011,
    'typeOfPermit': 5031,
    'work': [
        {
            'building': {
                'buildingCategory': 1060,
                'dateOfConstruction': {
                    'yearMonthDay': '2021-08-05'
                },
                'dwellings': [
                    {
                        'floor': 3102,
                        'floorNumber': 2,
                        'floorType': 3101,
                        'kitchen': True,
                        'locationOfDwellingOnFloor': 'Süd',
                        'multipleFloor': True,
                        'noOfHabitableRooms': '20',
                        'surfaceAreaOfDwelling': '420',
                        'usageLimitation': 3401
                    }
                ],
                'nameOfBuilding': 'Villa',
                'realestateIdentification': {
                    'EGRID': 'CH123456789',
                    'number': 123456789
                },
                'thermotechnicalDeviceForHeating1': {
                    'energySourceHeating': 7570,
                    'informationSourceHeating': 869,
                    'revisionDate': '2021-10-07'
                },
                'thermotechnicalDeviceForHeating2': None,
                'thermotechnicalDeviceForWarmWater1': None,
                'thermotechnicalDeviceForWarmWater2': {
                    'energySourceHeating': 7520,
                    'informationSourceHeating': 869,
                    'revisionDate': '2021-10-07'
                }
            },
            'kindOfWork': 6001
        }
    ]
}
