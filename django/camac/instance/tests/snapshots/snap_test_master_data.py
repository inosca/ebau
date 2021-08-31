# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['test_master_data_be[de] 1'] = {
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
    'city': 'Musterhausen',
    'construction_costs': 199000,
    'dossier_number': '2021-1',
    'is_paper': False,
    'modification': 'Doch eher kleines Haus',
    'municipality': {
        'label': 'Bern',
        'slug': '1'
    },
    'paper_submit_date': GenericRepr('datetime.datetime(2021, 3, 20, 13, 17, 8, tzinfo=tzutc())'),
    'plot_data': [
        {
            'egrid_number': 'CH123456789',
            'plot_number': '123456789'
        }
    ],
    'proposal': 'Grosses Haus',
    'street': 'Musterstrasse',
    'street_number': 4,
    'submit_date': GenericRepr('datetime.datetime(2021, 3, 31, 13, 17, 8, tzinfo=tzutc())')
}

snapshots['test_master_data_be[fr] 1'] = {
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
    'city': 'Musterhausen',
    'construction_costs': 199000,
    'dossier_number': '2021-1',
    'is_paper': False,
    'modification': 'Doch eher kleines Haus',
    'municipality': {
        'label': 'Berne',
        'slug': '1'
    },
    'paper_submit_date': GenericRepr('datetime.datetime(2021, 3, 20, 13, 17, 8, tzinfo=tzutc())'),
    'plot_data': [
        {
            'egrid_number': 'CH123456789',
            'plot_number': '123456789'
        }
    ],
    'proposal': 'Grosses Haus',
    'street': 'Musterstrasse',
    'street_number': 4,
    'submit_date': GenericRepr('datetime.datetime(2021, 3, 31, 13, 17, 8, tzinfo=tzutc())')
}

snapshots['test_master_data_parsers 1'] = {
    'date': GenericRepr('datetime.date(2021, 8, 18)'),
    'datetime': GenericRepr('datetime.datetime(2021, 8, 18, 6, 58, 8, 397000, tzinfo=tzutc())'),
    'success': True
}

snapshots['test_master_data_ur 1'] = {
    'applicants': [
        {
            'country': 'Schweiz',
            'first_name': 'Max',
            'is_juristic_person': True,
            'juristic_name': 'ACME AG',
            'last_name': 'Mustermann',
            'street': 'Teststrasse',
            'street_number': '123',
            'town': 'Musterdorf',
            'zip': '1233'
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
            'plot_number': '123456789'
        }
    ],
    'proposal': 'Grosses Haus',
    'street': 'Musterstrasse',
    'street_number': 4,
    'submit_date': GenericRepr('datetime.datetime(2021, 7, 16, 8, 0, 6, tzinfo=<UTC>)'),
    'type_of_construction': [
    ]
}
