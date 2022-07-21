# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['test_record_loading_be[dossier_row_patch0-dossier_number-kt_bern] 1'] = None

snapshots['test_record_loading_be[dossier_row_patch1-dossier_number-kt_bern] 1'] = '2017-1'

snapshots['test_record_loading_be[dossier_row_patch10-construction_start_date-kt_bern] 1'] = GenericRepr('datetime.date(2021, 12, 12)')

snapshots['test_record_loading_be[dossier_row_patch11-profile_approval_date-kt_bern] 1'] = GenericRepr('datetime.date(2021, 12, 12)')

snapshots['test_record_loading_be[dossier_row_patch12-decision_date-kt_bern] 1'] = GenericRepr('datetime.date(2021, 12, 12)')

snapshots['test_record_loading_be[dossier_row_patch13-final_approval_date-kt_bern] 1'] = GenericRepr('datetime.date(2021, 12, 12)')

snapshots['test_record_loading_be[dossier_row_patch14-completion_date-kt_bern] 1'] = GenericRepr('datetime.date(2021, 12, 12)')

snapshots['test_record_loading_be[dossier_row_patch15-application_type-kt_bern] 1'] = None

snapshots['test_record_loading_be[dossier_row_patch16-applicants-kt_bern] 1'] = [
    {
        'first_name': 'Willy',
        'is_juristic_person': None,
        'juristic_name': 'Chocolate Factory',
        'last_name': 'Wonka',
        'street': 'Candy Lane',
        'street_number': '13',
        'town': 'Wonderland',
        'zip': 1234
    }
]

snapshots['test_record_loading_be[dossier_row_patch17-landowners-kt_bern] 1'] = [
    {
        'first_name': 'Willy',
        'is_juristic_person': None,
        'juristic_name': 'Chocolate Factory',
        'last_name': 'Wonka',
        'street': 'Candy Lane',
        'street_number': '13',
        'town': 'Wonderland',
        'zip': None
    }
]

snapshots['test_record_loading_be[dossier_row_patch18-project_authors-kt_bern] 1'] = [
    {
        'first_name': 'Willy',
        'is_juristic_person': None,
        'juristic_name': 'Chocolate Factory',
        'last_name': 'Wonka',
        'street': 'Candy Lane',
        'street_number': None,
        'town': 'Wonderland',
        'zip': None
    }
]

snapshots['test_record_loading_be[dossier_row_patch19-project_authors-kt_bern] 1'] = [
]

snapshots['test_record_loading_be[dossier_row_patch2-dossier_number-kt_bern] 1'] = '2017-1'

snapshots['test_record_loading_be[dossier_row_patch3-dossier_number-kt_bern] 1'] = '2020-1'

snapshots['test_record_loading_be[dossier_row_patch4-dossier_number-kt_bern] 1'] = '2017-1'

snapshots['test_record_loading_be[dossier_row_patch5-plot_data-kt_bern] 1'] = [
    {
        'coord_east': 2710662.0,
        'coord_north': 1225997.0,
        'egrid_number': 'HK207838123456',
        'plot_number': '`123`'
    },
    {
        'coord_east': None,
        'coord_north': None,
        'egrid_number': 'EGRIDDELLEY',
        'plot_number': '2BA'
    }
]

snapshots['test_record_loading_be[dossier_row_patch6-plot_data-kt_bern] 1'] = [
    {
        'coord_east': None,
        'coord_north': None,
        'egrid_number': 'HK207838123456',
        'plot_number': '`123`'
    },
    {
        'coord_east': None,
        'coord_north': None,
        'egrid_number': 'EGRIDDELLEY',
        'plot_number': '2BA'
    }
]

snapshots['test_record_loading_be[dossier_row_patch7-plot_data-kt_bern] 1'] = [
    {
        'coord_east': 2710662.0,
        'coord_north': 1225997.0,
        'egrid_number': 'HK207838123456',
        'plot_number': '`123`'
    },
    {
        'coord_east': None,
        'coord_north': None,
        'egrid_number': 'None',
        'plot_number': '2BA'
    }
]

snapshots['test_record_loading_be[dossier_row_patch8-submit_date-kt_bern] 1'] = GenericRepr('datetime.datetime(2021, 12, 12, 0, 0)')

snapshots['test_record_loading_be[dossier_row_patch9-publication_date-kt_bern] 1'] = GenericRepr('datetime.date(2021, 12, 12)')

snapshots['test_record_loading_sz[dossier_row_patch0-coordinates-kt_schwyz-sz_instance] 1'] = [
    {
        'lat': 47.175669937318816,
        'lng': 8.8984885140077
    }
]

snapshots['test_record_loading_sz[dossier_row_patch1-street-kt_schwyz-sz_instance] 1'] = 'Musterstrasse 3a'

snapshots['test_record_loading_sz[dossier_row_patch10-completion_date-kt_schwyz-sz_instance] 1'] = [
    {
        'value': GenericRepr('datetime.date(2021, 12, 12)')
    }
]

snapshots['test_record_loading_sz[dossier_row_patch11-application_type_migrated-kt_schwyz-sz_instance] 1'] = 'Baugesuch'

snapshots['test_record_loading_sz[dossier_row_patch12-applicants-kt_schwyz-sz_instance] 1'] = [
    {
        'company': 'Chocolate Factory',
        'country': 'Schweiz',
        'email': 'candy@example.com',
        'first_name': 'Willy',
        'is_juristic_person': None,
        'juristic_name': 'Chocolate Factory',
        'last_name': 'Wonka',
        'phone': '+1 101 10 01 101',
        'street': 'Candy Lane 13',
        'town': 'Wonderland',
        'zip': 1234
    }
]

snapshots['test_record_loading_sz[dossier_row_patch13-landowners-kt_schwyz-sz_instance] 1'] = [
    {
        'company': 'Chocolate Factory',
        'country': 'Schweiz',
        'email': 'candy@example.com',
        'first_name': 'Willy',
        'is_juristic_person': None,
        'juristic_name': 'Chocolate Factory',
        'last_name': 'Wonka',
        'phone': '+1 101 10 01 101',
        'street': 'Candy Lane 13',
        'town': 'Wonderland',
        'zip': '2345'
    }
]

snapshots['test_record_loading_sz[dossier_row_patch14-project_authors-kt_schwyz-sz_instance] 1'] = [
    {
        'company': 'Chocolate Factory',
        'country': 'Schweiz',
        'email': 'candy@example.com',
        'first_name': 'Willy',
        'is_juristic_person': None,
        'juristic_name': 'Chocolate Factory',
        'last_name': 'Wonka',
        'phone': '+1 101 10 01 101',
        'street': 'Candy Lane',
        'town': 'Wonderland',
        'zip': '3456'
    }
]

snapshots['test_record_loading_sz[dossier_row_patch15-project_authors-kt_schwyz-sz_instance] 1'] = [
]

snapshots['test_record_loading_sz[dossier_row_patch2-plot_data-kt_schwyz-sz_instance] 1'] = [
    {
        'egrid_number': 'HK207838123456',
        'plot_number': '123'
    },
    {
        'egrid_number': 'EGRIDDELLEY',
        'plot_number': '2BA'
    }
]

snapshots['test_record_loading_sz[dossier_row_patch3-submit_date-kt_schwyz-sz_instance] 1'] = GenericRepr('datetime.datetime(2021, 12, 12, 11, 0, tzinfo=<UTC>)')

snapshots['test_record_loading_sz[dossier_row_patch4-publication_date-kt_schwyz-sz_instance] 1'] = GenericRepr('datetime.datetime(2021, 12, 12, 11, 0, tzinfo=<UTC>)')

snapshots['test_record_loading_sz[dossier_row_patch5-construction_start_date-kt_schwyz-sz_instance] 1'] = [
    {
        'value': GenericRepr('datetime.date(2021, 12, 12)')
    }
]

snapshots['test_record_loading_sz[dossier_row_patch6-profile_approval_date-kt_schwyz-sz_instance] 1'] = [
    {
        'value': GenericRepr('datetime.date(2021, 12, 12)')
    }
]

snapshots['test_record_loading_sz[dossier_row_patch7-decision_date-kt_schwyz-sz_instance] 1'] = GenericRepr('datetime.date(2021, 12, 12)')

snapshots['test_record_loading_sz[dossier_row_patch8-final_approval_date-kt_schwyz-sz_instance] 1'] = [
    {
        'value': GenericRepr('datetime.date(2021, 12, 12)')
    }
]

snapshots['test_record_loading_sz[dossier_row_patch9-completion_date-kt_schwyz-sz_instance] 1'] = [
    {
        'value': GenericRepr('datetime.date(2021, 12, 12)')
    }
]
