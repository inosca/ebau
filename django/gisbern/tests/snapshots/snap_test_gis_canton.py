# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_gis_canton[CH643546955207] 1'] = {
    'data': {
        'ARCHINV_FUNDST': False,
        'BALISKBS_KBS': True,
        'BAUINV_BAUINV_VW': True,
        'GK5_SY': False,
        'GSK25_GSK_VW': True,
        'GSKT_BEZEICH_DE': [
            'Gewässerschutzbereich Ao',
            'übriger Bereich üB'
        ],
        'NSG_NSGP': True,
        'UZP_BAU_VW': [
        ],
        'UZP_LSG_VW': False,
        'UZP_UEO_VW': [
            'Teilzonenplan Moorlandschaft 336 Amsoldingen',
            'Teilzonenplan Moorlandschaft Nr. 336 Amsoldingen'
        ]
    }
}

snapshots['test_gis_canton[CH673533354667] 1'] = {
    'data': {
        'ARCHINV_FUNDST': False,
        'BALISKBS_KBS': True,
        'BAUINV_BAUINV_VW': False,
        'GK5_SY': True,
        'GSK25_GSK_VW': True,
        'GSKT_BEZEICH_DE': [
            'Gewässerschutzbereich Au'
        ],
        'NSG_NSGP': False,
        'UZP_BAU_VW': [
            'Gewerbezone G2',
            'Zone für öffentliche Nutzung'
        ],
        'UZP_LSG_VW': False,
        'UZP_UEO_VW': [
            'Aarolina',
            'Chräjeninsel'
        ]
    }
}

snapshots['test_gis_canton[CH851446093521] 1'] = {
    'data': {
        'ARCHINV_FUNDST': True,
        'BALISKBS_KBS': False,
        'BAUINV_BAUINV_VW': True,
        'GK5_SY': False,
        'GSK25_GSK_VW': True,
        'GSKT_BEZEICH_DE': [
            'Gewässerschutzbereich Ao',
            'Gewässerschutzbereich Au'
        ],
        'NSG_NSGP': False,
        'UZP_BAU_VW': [
            'Wohnzone 1 E1',
            'Wohnzone 2 E2',
            'Zone für öffentliche Nutzung ZöN 7'
        ],
        'UZP_LSG_VW': False,
        'UZP_UEO_VW': [
        ]
    }
}

snapshots['test_gis_canton[doesntexist] 1'] = {
    'errors': 'No multisurface found'
}

snapshots['test_gis_canton[emptygis] 1'] = {
    'errors': "Can't parse document"
}

snapshots['test_gis_canton[emptymultisurface] 1'] = {
    'errors': "Can't parse document"
}
