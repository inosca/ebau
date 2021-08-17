# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_master_data_be[de] 1'] = {
    'construction_costs': 199000,
    'ebau_number': '2021-1',
    'modification': 'Doch eher kleines Haus',
    'municipality': {
        'label': 'Bern',
        'slug': '1'
    },
    'paper_submit_date': '2021-03-20T13:17:08+0000',
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
    'submit_date': '2021-03-31T13:17:08+0000'
}

snapshots['test_master_data_be[fr] 1'] = {
    'construction_costs': 199000,
    'ebau_number': '2021-1',
    'modification': 'Doch eher kleines Haus',
    'municipality': {
        'label': 'Berne',
        'slug': '1'
    },
    'paper_submit_date': '2021-03-20T13:17:08+0000',
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
    'submit_date': '2021-03-31T13:17:08+0000'
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
