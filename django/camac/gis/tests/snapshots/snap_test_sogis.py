# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_sogis_client[coords0-so_simple_config-200] 1'] = {
    'gemeinde': {
        'label': 'Suse Junk',
        'value': 'Solothurn'
    }
}

snapshots['test_sogis_client[coords1-so_filter_config-200] 1'] = {
    'wald': {
        'label': 'Suse Junk',
        'value': 'geschlossener_Wald'
    }
}

snapshots['test_sogis_client[coords2-so_nested_config-200] 1'] = {
    'parzellen': {
        'label': 'Suse Junk',
        'value': {
            'e-grid': {
                'label': 'Trudi Thanel',
                'value': 'CH354732700648'
            },
            'parzellennummer': {
                'label': 'Elwira Pärtzelt',
                'value': 850
            }
        }
    }
}

snapshots['test_sogis_client[coords3-so_all_config-200] 1'] = {
    'gemeinde': {
        'label': 'Suse Junk',
        'value': 'Solothurn'
    },
    'parzellen': {
        'label': 'Valerij Hahn-Holt',
        'value': {
            'e-grid': {
                'label': 'Sandor Wulf',
                'value': 'CH354732700648'
            },
            'parzellennummer': {
                'form': 'total-series-worry',
                'label': 'Angelica Flantz',
                'value': 850
            }
        }
    },
    'wald': {
        'label': 'Prof. Leila Heser MBA.',
        'value': None
    }
}

snapshots['test_sogis_client[coords4-so_unknown_layer_config-400] 1'] = [
    'Error 404 while fetching data from the API'
]

snapshots['test_sogis_client[coords5-so_unknown_property_config-200] 1'] = {
    'gemeinde': {
        'label': 'Suse Junk',
        'value': None
    }
}

snapshots['test_sogis_client[coords6-so_unknown_question_config-200] 1'] = {
    'unknown_question': {
        'label': None,
        'value': 'Solothurn'
    }
}
