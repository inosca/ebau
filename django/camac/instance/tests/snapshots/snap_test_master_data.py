# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['test_master_data_be[de] 1'] = {
    'construction_costs': 199000,
    'ebau_number': '2021-1',
    'is_paper': False,
    'modification': 'Doch eher kleines Haus',
    'municipality': {
        'label': 'Bern',
        'slug': '1'
    },
    'paper_submit_date': GenericRepr('datetime.datetime(2021, 3, 20, 13, 17, 8, tzinfo=tzutc())'),
    'personal_data': [
        {
            'first_name': 'Max',
            'is_juristic_person': True,
            'juristic_person_name': 'ACME AG',
            'last_name': 'Mustermann'
        }
    ],
    'plot_data': [
        {
            'e_grid_number': 'CH123456789',
            'plot_number': '123456789'
        }
    ],
    'proposal': 'Grosses Haus',
    'street': 'Musterstrasse',
    'street_number': 4,
    'submit_date': GenericRepr('datetime.datetime(2021, 3, 31, 13, 17, 8, tzinfo=tzutc())')
}

snapshots['test_master_data_be[fr] 1'] = {
    'construction_costs': 199000,
    'ebau_number': '2021-1',
    'is_paper': False,
    'modification': 'Doch eher kleines Haus',
    'municipality': {
        'label': 'Berne',
        'slug': '1'
    },
    'paper_submit_date': GenericRepr('datetime.datetime(2021, 3, 20, 13, 17, 8, tzinfo=tzutc())'),
    'personal_data': [
        {
            'first_name': 'Max',
            'is_juristic_person': True,
            'juristic_person_name': 'ACME AG',
            'last_name': 'Mustermann'
        }
    ],
    'plot_data': [
        {
            'e_grid_number': 'CH123456789',
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
    'municipality': {
        'label': 'Altdorf',
        'slug': '1'
    },
    'personal_data': [
        {
            'first_name': 'Max',
            'is_juristic_person': True,
            'juristic_name': 'ACME AG',
            'last_name': 'Mustermann'
        }
    ],
    'plot_data': [
        {
            'plot_number': '123456789'
        }
    ],
    'proposal': 'Grosses Haus',
    'street': 'Musterstrasse',
    'street_number': 4
}
