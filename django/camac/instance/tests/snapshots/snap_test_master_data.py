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
    'monument_contract': 'Ja',
    'monument_inventory': 'Nein',
    'monument_k_object': 'Nein',
    'monument_rrb': 'Ja',
    'monument_worth_preserving': 'Nein',
    'monument_worth_protecting': 'Ja',
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
    'project': 'Neubau',
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
        'Wohnen'
    ],
    'usage_zone': 'Wohnzone W2',
    'water_protection_area': [
        'Aᵤ'
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
    'monument_contract': 'Ja',
    'monument_inventory': 'Nein',
    'monument_k_object': 'Nein',
    'monument_rrb': 'Ja',
    'monument_worth_preserving': 'Nein',
    'monument_worth_protecting': 'Ja',
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
    'project': 'Neubau',
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
        'Vivre'
    ],
    'usage_zone': 'Wohnzone W2',
    'water_protection_area': [
        'Aᵤ'
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

snapshots['test_master_data[kt_uri-de-ur_master_data_case-select_related2-prefetch_related2-7] 1'] = {
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
    'category': [
        6011,
        6010
    ],
    'city': 'Musterdorf',
    'construction_costs': 129000,
    'dossier_number': '1201-21-003',
    'municipality': {
        'label': 'Altdorf',
        'slug': '1'
    },
    'plot_data': [
        {
            'egrid_number': 'CH123456789',
            'plot_number': 123456789
        }
    ],
    'proposal': 'Grosses Haus',
    'street': 'Musterstrasse',
    'street_number': 4,
    'submit_date': GenericRepr('datetime.datetime(2021, 7, 16, 8, 0, 6, tzinfo=<UTC>)'),
    'type_of_construction': [
    ]
}

snapshots['test_master_data_parsers 1'] = {
    'date': GenericRepr('datetime.date(2021, 8, 18)'),
    'datetime': GenericRepr('datetime.datetime(2021, 8, 18, 6, 58, 8, 397000, tzinfo=tzutc())'),
    'success': True
}
