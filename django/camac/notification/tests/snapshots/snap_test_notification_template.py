# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_notification_caluma_placeholders[False-2-1-user@example.com-Municipality] 1'] = '''Hinweis: Diese Nachricht wurde von einem Testsystem versendet.
Es dient nur zu Testzwecken und kann ignoriert werden


        BASE_URL: http://ebau.local
        EBAU_NUMBER: 2019-01
        FORM_NAME_DE: Baugesuch
        FORM_NAME_FR: Demande de permis de construire
        MUNICIPALITY_DE: Gemeinde Bern
        MUNICIPALITY_FR: Municipalité Berne
        INSTANCE_ID: 1
        LEITBEHOERDE_NAME_DE: Leitbehörde Bern
        LEITBEHOERDE_NAME_FR: Municipalité Berne
        INTERNAL_DOSSIER_LINK: http://ebau.local/index/redirect-to-instance-resource/instance-id/1
        PUBLIC_DOSSIER_LINK: http://ebau-portal.local/instances/1
        DISTRIBUTION_STATUS_DE: 
        DISTRIBUTION_STATUS_FR: 
        INQUIRY_ANSWER_DE: 
        INQUIRY_ANSWER_FR: 
        INQUIRY_REMARK: 
        CURRENT_SERVICE: Leitbehörde Bern
        CURRENT_SERVICE_DE: Leitbehörde Bern
        CURRENT_SERVICE_FR: Municipalité Berne
        CURRENT_USER_NAME: User Admin
        WORK_ITEM_NAME: Gesuch einreichen
    '''

snapshots['test_notification_caluma_placeholders[False-2-2-user@example.com-Municipality] 1'] = '''Hinweis: Diese Nachricht wurde von einem Testsystem versendet.
Es dient nur zu Testzwecken und kann ignoriert werden


        BASE_URL: http://ebau.local
        EBAU_NUMBER: 2019-01
        FORM_NAME_DE: Baugesuch
        FORM_NAME_FR: Demande de permis de construire
        MUNICIPALITY_DE: Gemeinde Bern
        MUNICIPALITY_FR: Municipalité Berne
        INSTANCE_ID: 1
        LEITBEHOERDE_NAME_DE: Leitbehörde Bern
        LEITBEHOERDE_NAME_FR: Municipalité Berne
        INTERNAL_DOSSIER_LINK: http://ebau.local/index/redirect-to-instance-resource/instance-id/1
        PUBLIC_DOSSIER_LINK: http://ebau-portal.local/instances/1
        DISTRIBUTION_STATUS_DE: 
        DISTRIBUTION_STATUS_FR: 
        INQUIRY_ANSWER_DE: 
        INQUIRY_ANSWER_FR: 
        INQUIRY_REMARK: 
        CURRENT_SERVICE: Leitbehörde Bern
        CURRENT_SERVICE_DE: Leitbehörde Bern
        CURRENT_SERVICE_FR: Municipalité Berne
        CURRENT_USER_NAME: User Admin
        WORK_ITEM_NAME: Gesuch einreichen
    '''

snapshots['test_notification_caluma_placeholders[True-2-1-user@example.com-Municipality] 1'] = '''Hinweis: Diese Nachricht wurde von einem Testsystem versendet.
Es dient nur zu Testzwecken und kann ignoriert werden


        BASE_URL: http://ebau.local
        EBAU_NUMBER: 2019-01
        FORM_NAME_DE: Baugesuch
        FORM_NAME_FR: Demande de permis de construire
        MUNICIPALITY_DE: Gemeinde Bern
        MUNICIPALITY_FR: Municipalité Berne
        INSTANCE_ID: 1
        LEITBEHOERDE_NAME_DE: Leitbehörde Bern
        LEITBEHOERDE_NAME_FR: Municipalité Berne
        INTERNAL_DOSSIER_LINK: http://ebau.local/index/redirect-to-instance-resource/instance-id/1
        PUBLIC_DOSSIER_LINK: http://ebau-portal.local/instances/1
        DISTRIBUTION_STATUS_DE: 1 von 2 Stellungnahmen stehen noch aus.
        DISTRIBUTION_STATUS_FR: 1 de 2 prises de position sont toujours en attente.
        INQUIRY_ANSWER_DE: Nicht betroffen / nicht zuständig
        INQUIRY_ANSWER_FR: Non concerné/e / non compétent/e
        INQUIRY_REMARK: Bemerkung Anfrage
        CURRENT_SERVICE: Leitbehörde Bern
        CURRENT_SERVICE_DE: Leitbehörde Bern
        CURRENT_SERVICE_FR: Municipalité Berne
        CURRENT_USER_NAME: User Admin
        WORK_ITEM_NAME: Gesuch einreichen
    '''

snapshots['test_notification_caluma_placeholders[True-2-2-user@example.com-Municipality] 1'] = '''Hinweis: Diese Nachricht wurde von einem Testsystem versendet.
Es dient nur zu Testzwecken und kann ignoriert werden


        BASE_URL: http://ebau.local
        EBAU_NUMBER: 2019-01
        FORM_NAME_DE: Baugesuch
        FORM_NAME_FR: Demande de permis de construire
        MUNICIPALITY_DE: Gemeinde Bern
        MUNICIPALITY_FR: Municipalité Berne
        INSTANCE_ID: 1
        LEITBEHOERDE_NAME_DE: Leitbehörde Bern
        LEITBEHOERDE_NAME_FR: Municipalité Berne
        INTERNAL_DOSSIER_LINK: http://ebau.local/index/redirect-to-instance-resource/instance-id/1
        PUBLIC_DOSSIER_LINK: http://ebau-portal.local/instances/1
        DISTRIBUTION_STATUS_DE: Alle 2 Stellungnahmen sind nun eingegangen.
        DISTRIBUTION_STATUS_FR: Tous les 2 prises de position ont été reçues.
        INQUIRY_ANSWER_DE: Nicht betroffen / nicht zuständig
        INQUIRY_ANSWER_FR: Non concerné/e / non compétent/e
        INQUIRY_REMARK: Bemerkung Anfrage
        CURRENT_SERVICE: Leitbehörde Bern
        CURRENT_SERVICE_DE: Leitbehörde Bern
        CURRENT_SERVICE_FR: Municipalité Berne
        CURRENT_USER_NAME: User Admin
        WORK_ITEM_NAME: Gesuch einreichen
    '''
