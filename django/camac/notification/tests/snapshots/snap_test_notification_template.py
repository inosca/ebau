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
        INQUIRY_LINK: 
        CURRENT_SERVICE: Leitbehörde Bern
        CURRENT_SERVICE_DE: Leitbehörde Bern
        CURRENT_SERVICE_FR: Municipalité Berne
        CURRENT_USER_NAME: User Admin
        WORK_ITEM_NAME_DE: Gesuch einreichen
        WORK_ITEM_NAME_FR: Envoyer la demande
        DECISION_DE: Bewilligt
        DECISION_FR: Approuveé
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
        INQUIRY_LINK: 
        CURRENT_SERVICE: Leitbehörde Bern
        CURRENT_SERVICE_DE: Leitbehörde Bern
        CURRENT_SERVICE_FR: Municipalité Berne
        CURRENT_USER_NAME: User Admin
        WORK_ITEM_NAME_DE: Gesuch einreichen
        WORK_ITEM_NAME_FR: Envoyer la demande
        DECISION_DE: Bewilligt
        DECISION_FR: Approuveé
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
        INQUIRY_LINK: http://ebau.local/index/redirect-to-instance-resource/instance-id/1/?instance-resource-name=distribution&ember-hash=/distribution/DISTRIBUTION_UUID/from/1/to/1/INQUIRY_UUID/answer
        CURRENT_SERVICE: Leitbehörde Bern
        CURRENT_SERVICE_DE: Leitbehörde Bern
        CURRENT_SERVICE_FR: Municipalité Berne
        CURRENT_USER_NAME: User Admin
        WORK_ITEM_NAME_DE: Gesuch einreichen
        WORK_ITEM_NAME_FR: Envoyer la demande
        DECISION_DE: Bewilligt
        DECISION_FR: Approuveé
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
        INQUIRY_LINK: http://ebau.local/index/redirect-to-instance-resource/instance-id/1/?instance-resource-name=distribution&ember-hash=/distribution/DISTRIBUTION_UUID/from/1/to/1/INQUIRY_UUID/answer
        CURRENT_SERVICE: Leitbehörde Bern
        CURRENT_SERVICE_DE: Leitbehörde Bern
        CURRENT_SERVICE_FR: Municipalité Berne
        CURRENT_USER_NAME: User Admin
        WORK_ITEM_NAME_DE: Gesuch einreichen
        WORK_ITEM_NAME_FR: Envoyer la demande
        DECISION_DE: Bewilligt
        DECISION_FR: Approuveé
    '''

snapshots['test_notification_template_merge[Canton-identifier-{{identifier}}-200] 1'] = '''
        identifier: identifier
        answer_period_date: 21.01.2017
        field_punkte: 2’690’881 / 1’208’835
        field_bezeichnung: abc
        field_durchmesser_der_bohrung: 1
        billing_entries:
            - Alex Smith: 903.24 CHF, erstellt am 12.05.1999 auf Kostenstelle John Bonilla / Shannon Cruz (Nr. 0000)
        bauverwaltung:
            - beschwerdeverfahren_weiterzug_durch: Beschwerdegegner
            - bewilligungsverfahren_gr_sitzung_beschluss: foo
            - bewilligungsverfahren_gr_sitzung_datum: 01.01.2017
            - beschwerdeverfahren: []
            - baukontrolle_realisierung_table: []
            - bewilligungsverfahren_sistierung: []
            - bewilligungsverfahren_sitzung_baukommission:
                - Bemerkung: Foo Bar, Nr: 78
        publications:
            - 14.05.1990 - 19.09.2002 (W20)
    '''
