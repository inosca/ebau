# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_gis_canton[CH643546955207] 1'] = {
    'data': {
        'archäologisches_objekt': False,
        'bauinventar': False,
        'belasteter_standort': False,
        'besonderer_landschaftsschutz': False,
        'gebiet_mit_naturkatastrophen': False,
        'naturschutzgebiet': False
    }
}
