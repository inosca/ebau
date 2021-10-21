# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_gwr_data_ur 1'] = {
    'buildingPermitIssueDate': '2021-07-20',
    'client': {
        'address': {
            'country': {
                'countryNameShort': 'ch'
            },
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
    'typeOfClient': 6141,
    'typeOfConstruction': 6235,
    'typeOfConstructionProject': 6011,
    'typeOfPermit': 5031,
    'work': [
        {
            'building': {
                'buildingCategory': 1060,
                'civilDefenseShelter': None,
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
                    },
                    {
                        'floor': 3100,
                        'floorNumber': None,
                        'floorType': 3100,
                        'kitchen': False,
                        'locationOfDwellingOnFloor': 'Nord',
                        'multipleFloor': False,
                        'noOfHabitableRooms': '10',
                        'surfaceAreaOfDwelling': '72',
                        'usageLimitation': 3402
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

snapshots['test_instance_gwr_data_sz_gwr 1'] = {
    'buildingPermitIssueDate': None,
    'client': {
        'address': {
            'country': {
                'countryNameShort': 'ch'
            },
            'houseNumber': None,
            'street': 'Teststrasse 3',
            'swissZipCode': 5678,
            'town': 'Musterdorf'
        },
        'identification': {
            'isOrganisation': False,
            'organisationIdentification': {
                'organisationName': None
            },
            'personIdentification': {
                'firstName': 'Max',
                'officialName': 'Mustermann'
            }
        }
    },
    'constructionLocalisation': None,
    'constructionProjectDescription': 'Grosses Haus',
    'officialConstructionProjectFileNo': None,
    'projectAnnouncementDate': None,
    'projectCompletionDate': None,
    'projectStartDate': None,
    'realestateIdentification': {
        'EGRID': 'CH1234567890',
        'number': 1234
    },
    'totalCostsOfProject': 129000,
    'typeOfClient': 6161,
    'typeOfConstruction': None,
    'typeOfConstructionProject': None,
    'typeOfPermit': None,
    'work': [
        {
            'building': {
                'buildingCategory': 1060,
                'civilDefenseShelter': None,
                'dateOfConstruction': None,
                'dwellings': [
                    {
                        'floor': None,
                        'floorNumber': None,
                        'floorType': None,
                        'kitchen': True,
                        'locationOfDwellingOnFloor': 'Nord',
                        'multipleFloor': True,
                        'noOfHabitableRooms': 4,
                        'surfaceAreaOfDwelling': 42,
                        'usageLimitation': None
                    }
                ],
                'nameOfBuilding': None,
                'realestateIdentification': None,
                'thermotechnicalDeviceForHeating1': {
                    'energySourceHeating': 7540,
                    'heatGeneratorHeating': 7436
                },
                'thermotechnicalDeviceForHeating2': None,
                'thermotechnicalDeviceForWarmWater1': {
                    'energySourceHeating': 7560,
                    'heatGeneratorHotWater': None
                },
                'thermotechnicalDeviceForWarmWater2': None
            },
            'kindOfWork': None
        }
    ]
}

snapshots['test_instance_gwr_data_sz_gwr_v2 1'] = {
    'buildingPermitIssueDate': None,
    'client': {
        'address': {
            'country': {
                'countryNameShort': 'ch'
            },
            'houseNumber': None,
            'street': 'Teststrasse 3',
            'swissZipCode': 5678,
            'town': 'Musterdorf'
        },
        'identification': {
            'isOrganisation': False,
            'organisationIdentification': {
                'organisationName': None
            },
            'personIdentification': {
                'firstName': 'Max',
                'officialName': 'Mustermann'
            }
        }
    },
    'constructionLocalisation': None,
    'constructionProjectDescription': 'Grosses Haus',
    'officialConstructionProjectFileNo': None,
    'projectAnnouncementDate': None,
    'projectCompletionDate': None,
    'projectStartDate': None,
    'realestateIdentification': {
        'EGRID': 'CH1234567890',
        'number': 1234
    },
    'totalCostsOfProject': 129000,
    'typeOfClient': 6161,
    'typeOfConstruction': None,
    'typeOfConstructionProject': None,
    'typeOfPermit': None,
    'work': [
        {
            'building': {
                'buildingCategory': 1020,
                'civilDefenseShelter': True,
                'dateOfConstruction': None,
                'dwellings': [
                    {
                        'floor': None,
                        'floorNumber': None,
                        'floorType': None,
                        'kitchen': True,
                        'locationOfDwellingOnFloor': 'West',
                        'multipleFloor': False,
                        'noOfHabitableRooms': 2,
                        'surfaceAreaOfDwelling': 70,
                        'usageLimitation': None
                    },
                    {
                        'floor': None,
                        'floorNumber': None,
                        'floorType': None,
                        'kitchen': False,
                        'locationOfDwellingOnFloor': 'Ost',
                        'multipleFloor': False,
                        'noOfHabitableRooms': 3,
                        'surfaceAreaOfDwelling': 24,
                        'usageLimitation': None
                    }
                ],
                'nameOfBuilding': 'Grosses Haus',
                'realestateIdentification': None,
                'thermotechnicalDeviceForHeating1': {
                    'energySourceHeating': 7510,
                    'heatGeneratorHeating': 7411
                },
                'thermotechnicalDeviceForHeating2': None,
                'thermotechnicalDeviceForWarmWater1': {
                    'energySourceHeating': 7570,
                    'heatGeneratorHotWater': 7650
                },
                'thermotechnicalDeviceForWarmWater2': None
            },
            'kindOfWork': None
        }
    ]
}
