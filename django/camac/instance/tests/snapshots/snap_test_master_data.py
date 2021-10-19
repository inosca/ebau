# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['test_master_data[kt_bern-de-be_master_data_case-select_related0-prefetch_related0-8] 1'] = {
    'applicants': [
        {
            'first_name': 'Max',
            'is_juristic_person': True,
            'juristic_name': 'ACME AG',
            'last_name': 'Mustermann',
            'street': 'Teststrasse',
            'street_number': 123,
            'town': 'Testhausen',
            'zip': 1234
        }
    ],
    'building_owners': [
        {
            'first_name': 'Peter',
            'is_juristic_person': None,
            'juristic_name': None,
            'last_name': 'Meier',
            'street': 'Thunstrasse',
            'street_number': 88,
            'town': 'Bern',
            'zip': 3002
        }
    ],
    'city': 'Musterhausen',
    'construction_costs': 199000,
    'development_regulations': 'Überbauung XY',
    'dossier_number': '2021-1',
    'is_paper': False,
    'landowners': [
        {
            'first_name': 'Sandra',
            'is_juristic_person': None,
            'juristic_name': None,
            'last_name': 'Holzer',
            'street': 'Bernweg',
            'street_number': 12,
            'town': 'Bern',
            'zip': 3002
        }
    ],
    'legal_representatives': [
        {
            'first_name': None,
            'is_juristic_person': True,
            'juristic_name': 'Mustermann und Söhne AG',
            'last_name': None,
            'street': 'Juristenweg',
            'street_number': 99,
            'town': 'Bern',
            'zip': 3008
        }
    ],
    'modification': 'Doch eher kleines Haus',
    'monument_contract': {
        'label': 'Ja',
        'slug': 'vertrag-ja'
    },
    'monument_inventory': {
        'label': 'Nein',
        'slug': 'baugruppe-bauinventar-nein'
    },
    'monument_k_object': {
        'label': 'Nein',
        'slug': 'k-objekt-nein'
    },
    'monument_rrb': {
        'label': 'Ja',
        'slug': 'rrb-ja'
    },
    'monument_worth_preserving': {
        'label': 'Nein',
        'slug': 'erhaltenswert-nein'
    },
    'monument_worth_protecting': {
        'label': 'Ja',
        'slug': 'schuetzenswert-ja'
    },
    'municipality': {
        'label': 'Bern',
        'slug': '1'
    },
    'paper_submit_date': GenericRepr('datetime.datetime(2021, 3, 20, 13, 17, 8, tzinfo=tzutc())'),
    'plot_data': [
        {
            'coord_east': 2599941,
            'coord_north': 1198923,
            'egrid_number': 'CH334687350542',
            'plot_number': 473
        },
        {
            'coord_east': 2601995,
            'coord_north': 1201340,
            'egrid_number': 'CH913553467614',
            'plot_number': 2592
        }
    ],
    'project': {
        'label': 'Neubau',
        'slug': 'baubeschrieb-neubau'
    },
    'project_authors': [
        {
            'first_name': 'Hans',
            'is_juristic_person': None,
            'juristic_name': None,
            'last_name': 'Müller',
            'street': 'Einweg',
            'street_number': 9,
            'town': 'Bern',
            'zip': 3000
        }
    ],
    'proposal': 'Grosses Haus',
    'situation': 'Sachverhalt Test',
    'street': 'Musterstrasse',
    'street_number': 4,
    'submit_date': GenericRepr('datetime.datetime(2021, 3, 31, 13, 17, 8, tzinfo=tzutc())'),
    'usage_type': [
        {
            'label': 'Wohnen',
            'slug': 'nutzungsart-wohnen'
        }
    ],
    'usage_zone': 'Wohnzone W2',
    'water_protection_area': [
        {
            'label': 'Aᵤ',
            'slug': 'gewaesserschutzbereich-v2-au'
        }
    ]
}

snapshots['test_master_data[kt_bern-fr-be_master_data_case-select_related1-prefetch_related1-8] 1'] = {
    'applicants': [
        {
            'first_name': 'Max',
            'is_juristic_person': True,
            'juristic_name': 'ACME AG',
            'last_name': 'Mustermann',
            'street': 'Teststrasse',
            'street_number': 123,
            'town': 'Testhausen',
            'zip': 1234
        }
    ],
    'building_owners': [
        {
            'first_name': 'Peter',
            'is_juristic_person': None,
            'juristic_name': None,
            'last_name': 'Meier',
            'street': 'Thunstrasse',
            'street_number': 88,
            'town': 'Bern',
            'zip': 3002
        }
    ],
    'city': 'Musterhausen',
    'construction_costs': 199000,
    'development_regulations': 'Überbauung XY',
    'dossier_number': '2021-1',
    'is_paper': False,
    'landowners': [
        {
            'first_name': 'Sandra',
            'is_juristic_person': None,
            'juristic_name': None,
            'last_name': 'Holzer',
            'street': 'Bernweg',
            'street_number': 12,
            'town': 'Bern',
            'zip': 3002
        }
    ],
    'legal_representatives': [
        {
            'first_name': None,
            'is_juristic_person': True,
            'juristic_name': 'Mustermann und Söhne AG',
            'last_name': None,
            'street': 'Juristenweg',
            'street_number': 99,
            'town': 'Bern',
            'zip': 3008
        }
    ],
    'modification': 'Doch eher kleines Haus',
    'monument_contract': {
        'label': 'Ja',
        'slug': 'vertrag-ja'
    },
    'monument_inventory': {
        'label': 'Nein',
        'slug': 'baugruppe-bauinventar-nein'
    },
    'monument_k_object': {
        'label': 'Nein',
        'slug': 'k-objekt-nein'
    },
    'monument_rrb': {
        'label': 'Ja',
        'slug': 'rrb-ja'
    },
    'monument_worth_preserving': {
        'label': 'Nein',
        'slug': 'erhaltenswert-nein'
    },
    'monument_worth_protecting': {
        'label': 'Ja',
        'slug': 'schuetzenswert-ja'
    },
    'municipality': {
        'label': 'Berne',
        'slug': '1'
    },
    'paper_submit_date': GenericRepr('datetime.datetime(2021, 3, 20, 13, 17, 8, tzinfo=tzutc())'),
    'plot_data': [
        {
            'coord_east': 2599941,
            'coord_north': 1198923,
            'egrid_number': 'CH334687350542',
            'plot_number': 473
        },
        {
            'coord_east': 2601995,
            'coord_north': 1201340,
            'egrid_number': 'CH913553467614',
            'plot_number': 2592
        }
    ],
    'project': {
        'label': 'Neubau',
        'slug': 'baubeschrieb-neubau'
    },
    'project_authors': [
        {
            'first_name': 'Hans',
            'is_juristic_person': None,
            'juristic_name': None,
            'last_name': 'Müller',
            'street': 'Einweg',
            'street_number': 9,
            'town': 'Bern',
            'zip': 3000
        }
    ],
    'proposal': 'Grosses Haus',
    'situation': 'Sachverhalt Test',
    'street': 'Musterstrasse',
    'street_number': 4,
    'submit_date': GenericRepr('datetime.datetime(2021, 3, 31, 13, 17, 8, tzinfo=tzutc())'),
    'usage_type': [
        {
            'label': 'Vivre',
            'slug': 'nutzungsart-wohnen'
        }
    ],
    'usage_zone': 'Wohnzone W2',
    'water_protection_area': [
        {
            'label': 'Aᵤ',
            'slug': 'gewaesserschutzbereich-v2-au'
        }
    ]
}

snapshots['test_master_data[kt_schwyz-de-sz_master_data_case-select_related3-prefetch_related3-3] 1'] = {
    'applicants': [
        {
            'first_name': 'Max',
            'last_name': 'Mustermann',
            'street': 'Teststrasse',
            'town': 'Musterdorf',
            'zip': 1233
        }
    ],
    'construction_costs': 129000,
    'proposal': 'Grosses Haus',
    'submit_date': GenericRepr('datetime.datetime(2021, 7, 16, 8, 0, 6, tzinfo=<UTC>)')
}

snapshots['test_master_data[kt_uri-de-ur_master_data_case-select_related2-prefetch_related2-8] 1'] = {
    'applicants': [
        {
            'country': 'Schweiz',
            'first_name': 'Max',
            'is_juristic_person': True,
            'juristic_name': 'ACME AG',
            'last_name': 'Mustermann',
            'street': 'Teststrasse',
            'street_number': 123,
            'town': 'Musterdorf',
            'zip': 1233
        }
    ],
    'approval_reason': '5031',
    'buildings': [
        {
            'building_category': 1060,
            'name': 'Villa',
            'proposal': [
                6001
            ]
        }
    ],
    'category': [
        6011,
        6010
    ],
    'city': 'Musterdorf',
    'construction_costs': 129000,
    'construction_end_date': GenericRepr('datetime.datetime(2021, 7, 30, 8, 0, 6, tzinfo=<UTC>)'),
    'construction_start_date': GenericRepr('datetime.datetime(2021, 7, 25, 8, 0, 6, tzinfo=<UTC>)'),
    'decision_date': GenericRepr('datetime.datetime(2021, 7, 20, 8, 0, 6, tzinfo=<UTC>)'),
    'dossier_number': '1201-21-003',
    'dwellings': [
        {
            'area': '420',
            'floor_number': '2',
            'floor_type': 3101,
            'has_kitchen_facilities': True,
            'kitchen_facilities': 'kocheinrichtung-kochnische-greater-4-m2',
            'location_on_floor': 'Süd',
            'multiple_floors': True,
            'name_of_building': 'Villa',
            'number_of_rooms': '20',
            'usage_limitation': 3401
        }
    ],
    'energy_devices': [
        {
            'energy_source': 7570,
            'information_source': 869,
            'is_heating': True,
            'is_main_heating': True,
            'is_warm_water': False,
            'name_of_building': 'Villa',
            'type': 'anlagetyp-hauptheizung'
        }
    ],
    'municipality': {
        'label': 'Altdorf',
        'slug': '1'
    },
    'plot_data': [
        {
            'coordinates_east': 2690970.9,
            'coordinates_north': 1192891.9,
            'egrid_number': 'CH123456789',
            'origin_of_coordinates': 901,
            'plot_number': 123456789
        }
    ],
    'proposal': 'Grosses Haus',
    'street': 'Musterstrasse',
    'street_number': 4,
    'submit_date': GenericRepr('datetime.datetime(2021, 7, 16, 8, 0, 6, tzinfo=<UTC>)'),
    'type_of_applicant': '6161',
    'type_of_construction': [
        {
            'art_der_hochbaute': 6235
        }
    ]
}

snapshots['test_master_data_parsers 1'] = {
    'date': GenericRepr('datetime.date(2021, 8, 18)'),
    'datetime': GenericRepr('datetime.datetime(2021, 8, 18, 6, 58, 8, 397000, tzinfo=tzutc())'),
    'success': True
}
