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
        'GSKT_BEZEICH_DE': 'übriger Bereich üB',
        'NSG_NSGP': True,
        'UZP_LSG_VW': False,
        'UZP_UEO_VW': 'Teilzonenplan Moorlandschaft Nr. 336 Amsoldingen'
    }
}

snapshots['test_gis_canton[CH673533354667] 1'] = {
    'data': {
        'ARCHINV_FUNDST': False,
        'BALISKBS_KBS': True,
        'BAUINV_BAUINV_VW': False,
        'GK5_SY': True,
        'GSK25_GSK_VW': True,
        'GSKT_BEZEICH_DE': 'Gewässerschutzbereich Au',
        'NSG_NSGP': False,
        'UZP_BAU_VW': [
            'Zone für öffentliche Nutzung'
        ],
        'UZP_LSG_VW': False,
        'UZP_UEO_VW': 'Chräjeninsel'
    }
}

snapshots['test_gis_canton[CH851446093521] 1'] = {
    'data': {
        'ARCHINV_FUNDST': True,
        'BALISKBS_KBS': False,
        'BAUINV_BAUINV_VW': True,
        'GK5_SY': False,
        'GSK25_GSK_VW': True,
        'GSKT_BEZEICH_DE': 'Gewässerschutzbereich Ao',
        'NSG_NSGP': False,
        'UZP_BAU_VW': [
            'Wohnzone 2 E2 '
        ],
        'UZP_LSG_VW': False
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
