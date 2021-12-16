# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_file_validation[None-400-Support] 1'] = "[{'detail': ErrorDetail(string='Bitte eine Datei mitreichen, um einen Import zu starten.', code='archive_file_missing'), 'status': '400', 'source': {'pointer': '/data/attributes/source-file'}, 'code': 'archive_file_missing'}]"

snapshots['test_file_validation[garbage.zip-400-Support] 1'] = "[{'detail': ErrorDetail(string='Die hochgeladene Datei ist kein gültiges Zip-Format.', code='invalid-zip-file'), 'status': '400', 'source': {'pointer': '/data/attributes/source-file'}, 'code': 'invalid-zip-file'}]"

snapshots['test_file_validation[import-dossiers-file-wrong-format.zip-400-Support] 1'] = "[{'detail': ErrorDetail(string='Die Metadatendatei `dossiers.xlsx` ist kein gültiges Xlsx-Format.', code='invalid'), 'status': '400', 'source': {'pointer': '/data/attributes/source-file'}, 'code': 'invalid'}]"

snapshots['test_file_validation[import-example-no-errors.zip-201-Support] 1'] = '{\'created_at\': \'2021-12-12T01:00:00+01:00\', \'status\': \'verified\', \'service\': OrderedDict([(\'type\', \'services\'), (\'id\', \'21326\')]), \'group\': OrderedDict([(\'type\', \'groups\'), (\'id\', \'23608\')]), \'user\': OrderedDict([(\'type\', \'users\'), (\'id\', \'346\')]), \'location\': OrderedDict([(\'type\', \'locations\'), (\'id\', \'379\')]), \'id\': \'504c319e-7965-4c2e-b7ea-14316375abec\', \'messages\': {\'import\': {\'details\': [], \'summary\': {\'error\': [], \'stats\': {\'dossiers\': 0, \'documents\': 0}, \'warning\': []}, \'completed\': None}, \'validation\': {\'details\': [{\'status\': \'error\', \'dossier_id\': \'2017-84\', \'details\': [{\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-12 00:00:00\', \'field\': \'submit-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-15 00:00:00\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-17 00:00:00\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-19 00:00:00\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-20 00:00:00\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-23 00:00:00\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-24 00:00:00\', \'field\': \'completion-date\'}]}, {\'status\': \'error\', \'dossier_id\': \'2017-53\', \'details\': [{\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-12 00:00:00\', \'field\': \'submit-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-15 00:00:00\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-17 00:00:00\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-19 00:00:00\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-20 00:00:00\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-23 00:00:00\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-24 00:00:00\', \'field\': \'completion-date\'}]}], \'summary\': {\'error\': [], \'stats\': {\'attachments\': 4, \'dossiers\': 0}, \'warning\': [\'2 dossiers have an invalid value in date field. Please use the format "DD.MM.YYYY" (e.g. "13.04.2021"). Affected dossiers:\\n2017-84: \\\'2017-04-12 00:00:00\\\' (submit-date), \\\'2017-04-15 00:00:00\\\' (publication-date), \\\'2017-04-17 00:00:00\\\' (decision-date), \\\'2017-04-19 00:00:00\\\' (construction-start-date), \\\'2017-04-20 00:00:00\\\' (profile-approval-date), \\\'2017-04-23 00:00:00\\\' (final-approval-date), \\\'2017-04-24 00:00:00\\\' (completion-date), 2017-53: \\\'2017-04-12 00:00:00\\\' (submit-date), \\\'2017-04-15 00:00:00\\\' (publication-date), \\\'2017-04-17 00:00:00\\\' (decision-date), \\\'2017-04-19 00:00:00\\\' (construction-start-date), \\\'2017-04-20 00:00:00\\\' (profile-approval-date), \\\'2017-04-23 00:00:00\\\' (final-approval-date), \\\'2017-04-24 00:00:00\\\' (completion-date)\']}, \'completed\': \'2021-12-12T01:00:00+0100\'}}, \'source_file\': \'http://testserver/api/v1/dossier_imports/files/504c319e-7965-4c2e-b7ea-14316375abec/import-example-no-errors.zip\', \'mime_type\': None, \'dossier_loader_type\': \'zip-archive-xlsx\'}'

snapshots['test_file_validation[import-example-orphan-dirs.zip-201-Support] 1'] = '{\'created_at\': \'2021-12-12T01:00:00+01:00\', \'status\': \'verified\', \'service\': OrderedDict([(\'type\', \'services\'), (\'id\', \'21332\')]), \'group\': OrderedDict([(\'type\', \'groups\'), (\'id\', \'23614\')]), \'user\': OrderedDict([(\'type\', \'users\'), (\'id\', \'352\')]), \'location\': OrderedDict([(\'type\', \'locations\'), (\'id\', \'385\')]), \'id\': \'2de278f8-89f9-424d-8108-750c3a0960bc\', \'messages\': {\'import\': {\'details\': [], \'summary\': {\'error\': [], \'stats\': {\'dossiers\': 0, \'documents\': 0}, \'warning\': []}, \'completed\': None}, \'validation\': {\'details\': [{\'status\': \'error\', \'dossier_id\': \'2017-84\', \'details\': [{\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-12 00:00:00\', \'field\': \'submit-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-15 00:00:00\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-17 00:00:00\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-19 00:00:00\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-20 00:00:00\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-23 00:00:00\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-24 00:00:00\', \'field\': \'completion-date\'}]}, {\'status\': \'error\', \'dossier_id\': \'2017-53\', \'details\': [{\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-12 00:00:00\', \'field\': \'submit-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-15 00:00:00\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-17 00:00:00\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-19 00:00:00\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-20 00:00:00\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-23 00:00:00\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-24 00:00:00\', \'field\': \'completion-date\'}]}], \'summary\': {\'error\': [], \'stats\': {\'attachments\': 0, \'dossiers\': 0}, \'warning\': [\'2 dossiers have an invalid value in date field. Please use the format "DD.MM.YYYY" (e.g. "13.04.2021"). Affected dossiers:\\n2017-84: \\\'2017-04-12 00:00:00\\\' (submit-date), \\\'2017-04-15 00:00:00\\\' (publication-date), \\\'2017-04-17 00:00:00\\\' (decision-date), \\\'2017-04-19 00:00:00\\\' (construction-start-date), \\\'2017-04-20 00:00:00\\\' (profile-approval-date), \\\'2017-04-23 00:00:00\\\' (final-approval-date), \\\'2017-04-24 00:00:00\\\' (completion-date), 2017-53: \\\'2017-04-12 00:00:00\\\' (submit-date), \\\'2017-04-15 00:00:00\\\' (publication-date), \\\'2017-04-17 00:00:00\\\' (decision-date), \\\'2017-04-19 00:00:00\\\' (construction-start-date), \\\'2017-04-20 00:00:00\\\' (profile-approval-date), \\\'2017-04-23 00:00:00\\\' (final-approval-date), \\\'2017-04-24 00:00:00\\\' (completion-date)\', \'2 document folders were not found in the metadata file and will not be imported:\\n2017-11, 2017-22\', \'2 dossiers have no document folder.\']}, \'completed\': \'2021-12-12T01:00:00+0100\'}}, \'source_file\': \'http://testserver/api/v1/dossier_imports/files/2de278f8-89f9-424d-8108-750c3a0960bc/import-example-orphan-dirs.zip\', \'mime_type\': None, \'dossier_loader_type\': \'zip-archive-xlsx\'}'

snapshots['test_file_validation[import-example-validation-errors.zip-201-Support] 1'] = '{\'created_at\': \'2021-12-12T01:00:00+01:00\', \'status\': \'failed\', \'service\': OrderedDict([(\'type\', \'services\'), (\'id\', \'21331\')]), \'group\': OrderedDict([(\'type\', \'groups\'), (\'id\', \'23613\')]), \'user\': OrderedDict([(\'type\', \'users\'), (\'id\', \'351\')]), \'location\': OrderedDict([(\'type\', \'locations\'), (\'id\', \'384\')]), \'id\': \'9c256380-2df3-49b6-9d22-6c85c01b0935\', \'messages\': {\'import\': {\'details\': [], \'summary\': {\'error\': [], \'stats\': {\'dossiers\': 0, \'documents\': 0}, \'warning\': []}, \'completed\': None}, \'validation\': {\'details\': [{\'status\': \'error\', \'dossier_id\': \'2017-84\', \'details\': [{\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'not-a-date\', \'field\': \'submit-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'not-a-date\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'not-a-date\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'not-a-date\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'not-a-date\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'not-a-date\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'not-a-date\', \'field\': \'completion-date\'}]}, {\'status\': \'error\', \'dossier_id\': \'2017-86\', \'details\': [{\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1872\', \'field\': \'submit-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1872\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1872\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1872\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1872\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1872\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1872\', \'field\': \'completion-date\'}, {\'level\': 3, \'code\': \'status-choice-validation-error\', \'detail\': \'DONKED\', \'field\': \'status\'}]}, {\'status\': \'error\', \'dossier_id\': \'2017-87\', \'details\': [{\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1873\', \'field\': \'submit-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1873\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1873\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1873\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1873\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1873\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1873\', \'field\': \'completion-date\'}, {\'level\': 3, \'code\': \'missing-required-field-error\', \'detail\': None, \'field\': \'status\'}]}, {\'status\': \'error\', \'dossier_id\': \'2017-88\', \'details\': [{\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1874\', \'field\': \'submit-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1874\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1874\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1874\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1874\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1874\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1874\', \'field\': \'completion-date\'}]}, {\'status\': \'error\', \'dossier_id\': 9, \'details\': [{\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1875\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1875\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1875\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1875\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1875\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'22.01.1875\', \'field\': \'completion-date\'}, {\'level\': 3, \'code\': \'missing-required-field-error\', \'detail\': None, \'field\': \'submit_date\'}]}], \'summary\': {\'error\': ["1 dossiers have an invalid status. Affected dossiers:\\n2017-86: \'DONKED\' (status)", \'2 dossiers miss a value in a required field. Affected dossiers:\\n2017-87: status, 9: submit_date\'], \'stats\': {\'attachments\': 4, \'dossiers\': 0}, \'warning\': [\'5 dossiers have an invalid value in date field. Please use the format "DD.MM.YYYY" (e.g. "13.04.2021"). Affected dossiers:\\n2017-84: \\\'not-a-date\\\' (submit-date), \\\'not-a-date\\\' (publication-date), \\\'not-a-date\\\' (decision-date), \\\'not-a-date\\\' (construction-start-date), \\\'not-a-date\\\' (profile-approval-date), \\\'not-a-date\\\' (final-approval-date), \\\'not-a-date\\\' (completion-date), 2017-86: \\\'22.01.1872\\\' (submit-date), \\\'22.01.1872\\\' (publication-date), \\\'22.01.1872\\\' (decision-date), \\\'22.01.1872\\\' (construction-start-date), \\\'22.01.1872\\\' (profile-approval-date), \\\'22.01.1872\\\' (final-approval-date), \\\'22.01.1872\\\' (completion-date), 2017-87: \\\'22.01.1873\\\' (submit-date), \\\'22.01.1873\\\' (publication-date), \\\'22.01.1873\\\' (decision-date), \\\'22.01.1873\\\' (construction-start-date), \\\'22.01.1873\\\' (profile-approval-date), \\\'22.01.1873\\\' (final-approval-date), \\\'22.01.1873\\\' (completion-date), 2017-88: \\\'22.01.1874\\\' (submit-date), \\\'22.01.1874\\\' (publication-date), \\\'22.01.1874\\\' (decision-date), \\\'22.01.1874\\\' (construction-start-date), \\\'22.01.1874\\\' (profile-approval-date), \\\'22.01.1874\\\' (final-approval-date), \\\'22.01.1874\\\' (completion-date), 9: \\\'22.01.1875\\\' (publication-date), \\\'22.01.1875\\\' (decision-date), \\\'22.01.1875\\\' (construction-start-date), \\\'22.01.1875\\\' (profile-approval-date), \\\'22.01.1875\\\' (final-approval-date), \\\'22.01.1875\\\' (completion-date)\', \'4 dossiers have no document folder.\']}, \'completed\': \'2021-12-12T01:00:00+0100\'}}, \'source_file\': None, \'mime_type\': None, \'dossier_loader_type\': \'zip-archive-xlsx\'}'

snapshots['test_file_validation[import-example.zip-201-Support] 1'] = '{\'created_at\': \'2021-12-12T01:00:00+01:00\', \'status\': \'failed\', \'service\': OrderedDict([(\'type\', \'services\'), (\'id\', \'21327\')]), \'group\': OrderedDict([(\'type\', \'groups\'), (\'id\', \'23609\')]), \'user\': OrderedDict([(\'type\', \'users\'), (\'id\', \'347\')]), \'location\': OrderedDict([(\'type\', \'locations\'), (\'id\', \'380\')]), \'id\': \'4659ae40-20be-4aaf-a99e-c35b8e9d2f0e\', \'messages\': {\'import\': {\'details\': [], \'summary\': {\'error\': [], \'stats\': {\'dossiers\': 0, \'documents\': 0}, \'warning\': []}, \'completed\': None}, \'validation\': {\'details\': [{\'status\': \'error\', \'dossier_id\': \'2017-54\', \'details\': [{\'level\': 2, \'code\': \'duplicate-identifier-error\', \'detail\': \'2017-54 is not unique.\', \'field\': \'id\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-12 00:00:00\', \'field\': \'submit-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-12 00:00:00\', \'field\': \'submit-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-15 00:00:00\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-15 00:00:00\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-17 00:00:00\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-17 00:00:00\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-19 00:00:00\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-19 00:00:00\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-20 00:00:00\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-20 00:00:00\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-23 00:00:00\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-23 00:00:00\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-24 00:00:00\', \'field\': \'completion-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-24 00:00:00\', \'field\': \'completion-date\'}]}, {\'status\': \'error\', \'dossier_id\': \'2017-84\', \'details\': [{\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-12 00:00:00\', \'field\': \'submit-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-15 00:00:00\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-17 00:00:00\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-19 00:00:00\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-20 00:00:00\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-23 00:00:00\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-24 00:00:00\', \'field\': \'completion-date\'}]}, {\'status\': \'error\', \'dossier_id\': \'2017-53\', \'details\': [{\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-12 00:00:00\', \'field\': \'submit-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-15 00:00:00\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-17 00:00:00\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-19 00:00:00\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-20 00:00:00\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-23 00:00:00\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-24 00:00:00\', \'field\': \'completion-date\'}]}, {\'status\': \'error\', \'dossier_id\': \'missing required fields\', \'details\': [{\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-12 00:00:00\', \'field\': \'submit-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-15 00:00:00\', \'field\': \'publication-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-17 00:00:00\', \'field\': \'decision-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-19 00:00:00\', \'field\': \'construction-start-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-20 00:00:00\', \'field\': \'profile-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-23 00:00:00\', \'field\': \'final-approval-date\'}, {\'level\': 2, \'code\': \'date-field-validation-error\', \'detail\': \'2017-04-24 00:00:00\', \'field\': \'completion-date\'}, {\'level\': 3, \'code\': \'missing-required-field-error\', \'detail\': None, \'field\': \'status\'}]}], \'summary\': {\'error\': [\'1 dossiers miss a value in a required field. Affected dossiers:\\nmissing required fields: status\'], \'stats\': {\'attachments\': 4, \'dossiers\': 0}, \'warning\': [\'4 dossiers have an invalid value in date field. Please use the format "DD.MM.YYYY" (e.g. "13.04.2021"). Affected dossiers:\\n2017-54: \\\'2017-04-12 00:00:00\\\' (submit-date), \\\'2017-04-12 00:00:00\\\' (submit-date), \\\'2017-04-15 00:00:00\\\' (publication-date), \\\'2017-04-15 00:00:00\\\' (publication-date), \\\'2017-04-17 00:00:00\\\' (decision-date), \\\'2017-04-17 00:00:00\\\' (decision-date), \\\'2017-04-19 00:00:00\\\' (construction-start-date), \\\'2017-04-19 00:00:00\\\' (construction-start-date), \\\'2017-04-20 00:00:00\\\' (profile-approval-date), \\\'2017-04-20 00:00:00\\\' (profile-approval-date), \\\'2017-04-23 00:00:00\\\' (final-approval-date), \\\'2017-04-23 00:00:00\\\' (final-approval-date), \\\'2017-04-24 00:00:00\\\' (completion-date), \\\'2017-04-24 00:00:00\\\' (completion-date), 2017-84: \\\'2017-04-12 00:00:00\\\' (submit-date), \\\'2017-04-15 00:00:00\\\' (publication-date), \\\'2017-04-17 00:00:00\\\' (decision-date), \\\'2017-04-19 00:00:00\\\' (construction-start-date), \\\'2017-04-20 00:00:00\\\' (profile-approval-date), \\\'2017-04-23 00:00:00\\\' (final-approval-date), \\\'2017-04-24 00:00:00\\\' (completion-date), 2017-53: \\\'2017-04-12 00:00:00\\\' (submit-date), \\\'2017-04-15 00:00:00\\\' (publication-date), \\\'2017-04-17 00:00:00\\\' (decision-date), \\\'2017-04-19 00:00:00\\\' (construction-start-date), \\\'2017-04-20 00:00:00\\\' (profile-approval-date), \\\'2017-04-23 00:00:00\\\' (final-approval-date), \\\'2017-04-24 00:00:00\\\' (completion-date), missing required fields: \\\'2017-04-12 00:00:00\\\' (submit-date), \\\'2017-04-15 00:00:00\\\' (publication-date), \\\'2017-04-17 00:00:00\\\' (decision-date), \\\'2017-04-19 00:00:00\\\' (construction-start-date), \\\'2017-04-20 00:00:00\\\' (profile-approval-date), \\\'2017-04-23 00:00:00\\\' (final-approval-date), \\\'2017-04-24 00:00:00\\\' (completion-date)\', "1 dossiers have the same ID. Affected dossiers:\\n2017-54: \'2017-54 is not unique.\' (id)", \'2 dossiers have no document folder.\']}, \'completed\': \'2021-12-12T01:00:00+0100\'}}, \'source_file\': None, \'mime_type\': None, \'dossier_loader_type\': \'zip-archive-xlsx\'}'

snapshots['test_file_validation[import-no-dossiers-file.zip-400-Support] 1'] = "[{'detail': ErrorDetail(string='Metadatendatei `dossiers.xlsx` fehlt im hochgeladenen Archiv.', code='metadata-file-missing'), 'status': '400', 'source': {'pointer': '/data/attributes/source-file'}, 'code': 'metadata-file-missing'}]"

snapshots['test_validation_errors[import-example-validation-errors.zip-kt_schwyz-None-400-Municipality-en] 1'] = {
    'errors': [
        {
            'code': 'required-location-missing',
            'detail': 'No location assigned.',
            'source': {
                'pointer': '/data/attributes/non-field-errors'
            },
            'status': '400'
        }
    ]
}

snapshots['test_validation_errors[import-example-validation-errors.zip-kt_schwyz-location-201-Municipality-en] 1'] = {
    'created-at': '2021-12-12T01:00:00+01:00',
    'dossier-loader-type': 'zip-archive-xlsx',
    'messages': {
        'import': {
            'completed': None,
            'details': [
            ],
            'summary': {
                'error': [
                ],
                'stats': {
                    'documents': 0,
                    'dossiers': 0
                },
                'warning': [
                ]
            }
        },
        'validation': {
            'completed': '2021-12-12T01:00:00+0100',
            'details': [
                {
                    'details': [
                        {
                            'code': 'date-field-validation-error',
                            'detail': 'not-a-date',
                            'field': 'submit-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': 'not-a-date',
                            'field': 'publication-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': 'not-a-date',
                            'field': 'decision-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': 'not-a-date',
                            'field': 'construction-start-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': 'not-a-date',
                            'field': 'profile-approval-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': 'not-a-date',
                            'field': 'final-approval-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': 'not-a-date',
                            'field': 'completion-date',
                            'level': 2
                        }
                    ],
                    'dossier_id': '2017-84',
                    'status': 'error'
                },
                {
                    'details': [
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1872',
                            'field': 'submit-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1872',
                            'field': 'publication-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1872',
                            'field': 'decision-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1872',
                            'field': 'construction-start-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1872',
                            'field': 'profile-approval-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1872',
                            'field': 'final-approval-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1872',
                            'field': 'completion-date',
                            'level': 2
                        },
                        {
                            'code': 'status-choice-validation-error',
                            'detail': 'DONKED',
                            'field': 'status',
                            'level': 3
                        }
                    ],
                    'dossier_id': '2017-86',
                    'status': 'error'
                },
                {
                    'details': [
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1873',
                            'field': 'submit-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1873',
                            'field': 'publication-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1873',
                            'field': 'decision-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1873',
                            'field': 'construction-start-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1873',
                            'field': 'profile-approval-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1873',
                            'field': 'final-approval-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1873',
                            'field': 'completion-date',
                            'level': 2
                        },
                        {
                            'code': 'missing-required-field-error',
                            'detail': None,
                            'field': 'status',
                            'level': 3
                        }
                    ],
                    'dossier_id': '2017-87',
                    'status': 'error'
                },
                {
                    'details': [
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1874',
                            'field': 'submit-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1874',
                            'field': 'publication-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1874',
                            'field': 'decision-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1874',
                            'field': 'construction-start-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1874',
                            'field': 'profile-approval-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1874',
                            'field': 'final-approval-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1874',
                            'field': 'completion-date',
                            'level': 2
                        }
                    ],
                    'dossier_id': '2017-88',
                    'status': 'error'
                },
                {
                    'details': [
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1875',
                            'field': 'publication-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1875',
                            'field': 'decision-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1875',
                            'field': 'construction-start-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1875',
                            'field': 'profile-approval-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1875',
                            'field': 'final-approval-date',
                            'level': 2
                        },
                        {
                            'code': 'date-field-validation-error',
                            'detail': '22.01.1875',
                            'field': 'completion-date',
                            'level': 2
                        },
                        {
                            'code': 'missing-required-field-error',
                            'detail': None,
                            'field': 'submit_date',
                            'level': 3
                        }
                    ],
                    'dossier_id': 9,
                    'status': 'error'
                }
            ],
            'summary': {
                'error': [
                    '''1 dossiers have an invalid status. Affected dossiers: 
2017-86: 'DONKED' (status)''',
                    '''2 dossiers miss a value in a required field. Affected dossiers: 
2017-87: status,
9: submit_date'''
                ],
                'stats': {
                    'attachments': 4,
                    'dossiers': 0
                },
                'warning': [
                    '''5 dossiers have an invalid value in date field. Please use the format "DD.MM.YYYY" (e.g. "13.04.2021"). Affected dossiers: 
2017-84: 'not-a-date' (submit-date), 'not-a-date' (publication-date), 'not-a-date' (decision-date), 'not-a-date' (construction-start-date), 'not-a-date' (profile-approval-date), 'not-a-date' (final-approval-date), 'not-a-date' (completion-date),
2017-86: '22.01.1872' (submit-date), '22.01.1872' (publication-date), '22.01.1872' (decision-date), '22.01.1872' (construction-start-date), '22.01.1872' (profile-approval-date), '22.01.1872' (final-approval-date), '22.01.1872' (completion-date),
2017-87: '22.01.1873' (submit-date), '22.01.1873' (publication-date), '22.01.1873' (decision-date), '22.01.1873' (construction-start-date), '22.01.1873' (profile-approval-date), '22.01.1873' (final-approval-date), '22.01.1873' (completion-date),
2017-88: '22.01.1874' (submit-date), '22.01.1874' (publication-date), '22.01.1874' (decision-date), '22.01.1874' (construction-start-date), '22.01.1874' (profile-approval-date), '22.01.1874' (final-approval-date), '22.01.1874' (completion-date),
9: '22.01.1875' (publication-date), '22.01.1875' (decision-date), '22.01.1875' (construction-start-date), '22.01.1875' (profile-approval-date), '22.01.1875' (final-approval-date), '22.01.1875' (completion-date)''',
                    '4 dossiers have no document folder.'
                ]
            }
        }
    },
    'mime-type': None,
    'status': 'failed'
}
