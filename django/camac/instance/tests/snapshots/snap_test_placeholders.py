# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_dms_placeholders[Municipality] 1'] = {
    'ADDRESS': 'Musterstrasse 4, Musterhausen',
    'ADRESSE': 'Musterstrasse 4, Musterhausen',
    'AFFECTATION': 'Wohnen',
    'AFFECTATION_ZONE': 'Wohnzone W2',
    'ALLE_GEBAEUDEEIGENTUEMER': 'Peter Meier',
    'ALLE_GEBAEUDEEIGENTUEMER_NAME_ADDRESS': 'Peter Meier, Thunstrasse 88, 3002 Bern',
    'ALLE_GEBAEUDEEIGENTUEMER_NAME_ADRESSE': 'Peter Meier, Thunstrasse 88, 3002 Bern',
    'ALLE_GESUCHSTELLER': 'ACME AG, Max Mustermann',
    'ALLE_GESUCHSTELLER_NAME_ADDRESS': 'ACME AG, Max Mustermann, Teststrasse 123, 1234 Testhausen',
    'ALLE_GESUCHSTELLER_NAME_ADRESSE': 'ACME AG, Max Mustermann, Teststrasse 123, 1234 Testhausen',
    'ALLE_GRUNDEIGENTUEMER': 'Sandra Holzer',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADDRESS': 'Sandra Holzer, Bernweg 12, 3002 Bern',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADRESSE': 'Sandra Holzer, Bernweg 12, 3002 Bern',
    'ALLE_PROJEKTVERFASSER': 'Hans Müller',
    'ALLE_PROJEKTVERFASSER_NAME_ADDRESS': 'Hans Müller, Einweg 9, 3000 Bern',
    'ALLE_PROJEKTVERFASSER_NAME_ADRESSE': 'Hans Müller, Einweg 9, 3000 Bern',
    'ALLE_VERTRETER': 'Mustermann und Söhne AG',
    'ALLE_VERTRETER_NAME_ADDRESS': 'Mustermann und Söhne AG, Juristenweg 99, 3008 Bern',
    'ALLE_VERTRETER_NAME_ADRESSE': 'Mustermann und Söhne AG, Juristenweg 99, 3008 Bern',
    'AUJOURD_HUI': '30. August 2021',
    'AUTEUR_PROJET': 'Hans Müller',
    'AUTEUR_PROJET_ADRESSE_1': 'Einweg 9',
    'AUTEUR_PROJET_ADRESSE_2': '3000 Bern',
    'AUTEUR_PROJET_NOM_ADRESSE': 'Hans Müller, Einweg 9, 3000 Bern',
    'AUTEUR_PROJET_TOUS': 'Hans Müller',
    'AUTEUR_PROJET_TOUS_NOM_ADRESSE': 'Hans Müller, Einweg 9, 3000 Bern',
    'AUTORITE_DIRECTRICE_ADRESSE_1': '',
    'AUTORITE_DIRECTRICE_ADRESSE_2': 'Natalieside',
    'AUTORITE_DIRECTRICE_EMAIL': 'vboone@gmail.com',
    'AUTORITE_DIRECTRICE_LIEU': 'Natalieside',
    'AUTORITE_DIRECTRICE_NOM': 'John Thomas',
    'AUTORITE_DIRECTRICE_NOM_ABR': 'John Thomas',
    'AUTORITE_DIRECTRICE_TELEPHONE': '',
    'BASE_URL': 'http://camac-ng.local',
    'BAUEINGABE_DATUM': '31. März 2021',
    'BAUENTSCHEID': 'Positiv',
    'BAUENTSCHEID_ABSCHREIBUNGSVERFUEGUNG': False,
    'BAUENTSCHEID_BAUABSCHLAG': False,
    'BAUENTSCHEID_BAUABSCHLAG_MIT_WHST': False,
    'BAUENTSCHEID_BAUABSCHLAG_OHNE_WHST': False,
    'BAUENTSCHEID_BAUBEWILLIGUNG': False,
    'BAUENTSCHEID_BAUBEWILLIGUNGSFREI': False,
    'BAUENTSCHEID_DATUM': '30. August 2021',
    'BAUENTSCHEID_GENERELL': False,
    'BAUENTSCHEID_GESAMT': True,
    'BAUENTSCHEID_KLEIN': False,
    'BAUENTSCHEID_POSITIV': True,
    'BAUENTSCHEID_POSITIV_TEILWEISE': True,
    'BAUENTSCHEID_PROJEKTAENDERUNG': False,
    'BAUENTSCHEID_TEILBAUBEWILLIGUNG': False,
    'BAUENTSCHEID_TYP': 'GESAMT',
    'BAUENTSCHEID_TYPE': 'GESAMT',
    'BAUVORHABEN': 'Neubau, Grosses Haus',
    'BESCHREIBUNG_BAUVORHABEN': 'Grosses Haus',
    'CIRCULATION_COMMUNES': [
        {
            'FRIST': '18.09.2021',
            'NAME': 'Christopher Murphy'
        },
        {
            'FRIST': '08.09.2021',
            'NAME': 'Kaitlin Smith'
        }
    ],
    'CIRCULATION_PREAVIS': [
        {
            'ANTWORT': 'Christopher Woods',
            'NEBENBESTIMMUNGEN': 'Baby strategy majority address eight least season.',
            'STELLUNGNAHME': 'Rich individual challenge crime hotel.',
            'VON': 'John Thomas'
        },
        {
            'ANTWORT': 'Priscilla Rogers',
            'NEBENBESTIMMUNGEN': 'Within foot assume management floor free.',
            'STELLUNGNAHME': 'Expect mother role economy sense model tonight leave.',
            'VON': 'Alison Russell'
        }
    ],
    'CIRCULATION_PREF': [
        {
            'FRIST': '05.09.2021',
            'NAME': 'Amy Ho'
        },
        {
            'FRIST': '07.09.2021',
            'NAME': 'Angela Roberts'
        }
    ],
    'CIRCULATION_SERVICES': [
        {
            'FRIST': '17.09.2021',
            'NAME': 'Alison Russell'
        }
    ],
    'COMMUNE': 'William Rodriguez',
    'COMMUNE_ADRESSE': 'West Hannahfort',
    'COMMUNE_ADRESSE_1': '',
    'COMMUNE_ADRESSE_2': 'West Hannahfort',
    'COMMUNE_EMAIL': 'nicholasharper@gmail.com',
    'COMMUNE_LIEU': 'West Hannahfort',
    'COMMUNE_NOM_ADRESSE': 'Gemeinde William Rodriguez, West Hannahfort',
    'COMMUNE_TELEPHONE': '',
    'COORDONEE': '2’599’941 / 1’198’923; 2’601’995 / 1’201’340',
    'DECISION': 'positive',
    'DECISION_CATEGORIE': 'GESAMT',
    'DECISION_DATE': '30. August 2021',
    'DECISION_GENERAL': False,
    'DECISION_GLOBALE': True,
    'DECISION_MODIF': False,
    'DECISION_PARTIEL': False,
    'DECISION_PERMIS': False,
    'DECISION_PETIT': False,
    'DECISION_REFUS': False,
    'DECISION_REFUS_AVEC_RET': False,
    'DECISION_REFUS_SANS_RET': False,
    'DECISION_TYPE': 'GESAMT',
    'DEPOT_DEMANDE_DATE': '31. März 2021',
    'DISPOSITIONS_ANNEXES': 'Baby strategy majority address eight least season.',
    'DOSSIER_LINK': 'http://camac-ng.local/index/redirect-to-instance-resource/instance-id/9999',
    'DOSSIER_NR': 9999,
    'DOSSIER_NUMERO': 9999,
    'DOSSIER_TYP': 'Baugesuch',
    'DOSSIER_TYPE': 'Baugesuch',
    'EBAU_NR': '2021-1',
    'EBAU_NUMBER': '2021-1',
    'EBAU_NUMERO': '2021-1',
    'EBAU_URL': 'http://camac-ng.local',
    'EIGENE_GEBUEHREN': [
        {
            'BETRAG': '739.39',
            'POSITION': ''
        },
        {
            'BETRAG': '871.33',
            'POSITION': ''
        }
    ],
    'EIGENE_GEBUEHREN_TOTAL': '1’610.72',
    'EIGENE_NEBENBESTIMMUNGEN': 'Baby strategy majority address eight least season.',
    'EIGENE_STELLUNGNAHMEN': 'Rich individual challenge crime hotel.',
    'EMAIL': '',
    'EMOLUMENTS': [
        {
            'BETRAG': '816.18',
            'POSITION': ''
        },
        {
            'BETRAG': '404.50',
            'POSITION': ''
        },
        {
            'BETRAG': '739.39',
            'POSITION': ''
        },
        {
            'BETRAG': '871.33',
            'POSITION': ''
        }
    ],
    'EMOLUMENTS_TOTAL': '2’831.40',
    'ETAT': 'David Rangel',
    'FACHSTELLEN_KANTONAL': [
        {
            'FRIST': '05.09.2021',
            'NAME': 'Amy Ho'
        },
        {
            'FRIST': '07.09.2021',
            'NAME': 'Angela Roberts'
        },
        {
            'FRIST': '18.09.2021',
            'NAME': 'Christopher Murphy'
        },
        {
            'FRIST': '08.09.2021',
            'NAME': 'Kaitlin Smith'
        },
        {
            'FRIST': '23.09.2021',
            'NAME': 'John Thomas'
        },
        {
            'FRIST': '17.09.2021',
            'NAME': 'Alison Russell'
        }
    ],
    'FACHSTELLEN_KANTONAL_LIST': '''- Amy Ho
- Angela Roberts
- Christopher Murphy
- Kaitlin Smith
- John Thomas
- Alison Russell''',
    'FACHSTELLEN_KANTONAL_LISTE': '''- Amy Ho
- Angela Roberts
- Christopher Murphy
- Kaitlin Smith
- John Thomas
- Alison Russell''',
    'FORM_NAME': 'Baugesuch',
    'GEBAEUDEEIGENTUEMER': 'Peter Meier',
    'GEBAEUDEEIGENTUEMER_ADDRESS_1': 'Thunstrasse 88',
    'GEBAEUDEEIGENTUEMER_ADDRESS_2': '3002 Bern',
    'GEBAEUDEEIGENTUEMER_ADRESSE_1': 'Thunstrasse 88',
    'GEBAEUDEEIGENTUEMER_ADRESSE_2': '3002 Bern',
    'GEBAEUDEEIGENTUEMER_NAME_ADDRESS': 'Peter Meier, Thunstrasse 88, 3002 Bern',
    'GEBAEUDEEIGENTUEMER_NAME_ADRESSE': 'Peter Meier, Thunstrasse 88, 3002 Bern',
    'GEBUEHREN': [
        {
            'BETRAG': '816.18',
            'POSITION': ''
        },
        {
            'BETRAG': '404.50',
            'POSITION': ''
        },
        {
            'BETRAG': '739.39',
            'POSITION': ''
        },
        {
            'BETRAG': '871.33',
            'POSITION': ''
        }
    ],
    'GEBUEHREN_TOTAL': '2’831.40',
    'GEMEINDE': 'William Rodriguez',
    'GEMEINDE_ADRESSE': 'West Hannahfort',
    'GEMEINDE_ADRESSE_1': '',
    'GEMEINDE_ADRESSE_2': 'West Hannahfort',
    'GEMEINDE_EMAIL': 'nicholasharper@gmail.com',
    'GEMEINDE_NAME_ADRESSE': 'Gemeinde William Rodriguez, West Hannahfort',
    'GEMEINDE_ORT': 'West Hannahfort',
    'GEMEINDE_TELEFON': '',
    'GESUCHSTELLER': 'ACME AG, Max Mustermann',
    'GESUCHSTELLER_ADDRESS_1': 'Teststrasse 123',
    'GESUCHSTELLER_ADDRESS_2': '1234 Testhausen',
    'GESUCHSTELLER_ADRESSE_1': 'Teststrasse 123',
    'GESUCHSTELLER_ADRESSE_2': '1234 Testhausen',
    'GESUCHSTELLER_NAME_ADDRESS': 'ACME AG, Max Mustermann, Teststrasse 123, 1234 Testhausen',
    'GESUCHSTELLER_NAME_ADRESSE': 'ACME AG, Max Mustermann, Teststrasse 123, 1234 Testhausen',
    'GEWAESSERSCHUTZBEREICH': 'Aᵤ',
    'GRUNDEIGENTUEMER': 'Sandra Holzer',
    'GRUNDEIGENTUEMER_ADDRESS_1': 'Bernweg 12',
    'GRUNDEIGENTUEMER_ADDRESS_2': '3002 Bern',
    'GRUNDEIGENTUEMER_ADRESSE_1': 'Bernweg 12',
    'GRUNDEIGENTUEMER_ADRESSE_2': '3002 Bern',
    'GRUNDEIGENTUEMER_NAME_ADDRESS': 'Sandra Holzer, Bernweg 12, 3002 Bern',
    'GRUNDEIGENTUEMER_NAME_ADRESSE': 'Sandra Holzer, Bernweg 12, 3002 Bern',
    'HEUTE': '30. August 2021',
    'INSTANCE_ID': 9999,
    'INVENTAR': 'Ja, Nein, Nein, Nein, Ja, Ja',
    'JURISTIC_NAME': 'ACME AG',
    'JURISTISCHER_NAME': 'ACME AG',
    'KOORDINATEN': '2’599’941 / 1’198’923; 2’601’995 / 1’201’340',
    'LANGUAGE': 'de',
    'LANGUE': 'de',
    'LEITBEHOERDE_ADDRESS_1': '',
    'LEITBEHOERDE_ADDRESS_2': 'Natalieside',
    'LEITBEHOERDE_ADRESSE_1': '',
    'LEITBEHOERDE_ADRESSE_2': 'Natalieside',
    'LEITBEHOERDE_CITY': 'Natalieside',
    'LEITBEHOERDE_EMAIL': 'vboone@gmail.com',
    'LEITBEHOERDE_NAME': 'John Thomas',
    'LEITBEHOERDE_NAME_KURZ': 'John Thomas',
    'LEITBEHOERDE_PHONE': '',
    'LEITBEHOERDE_STADT': 'Natalieside',
    'LEITBEHOERDE_TELEFON': '',
    'LEITPERSON': 'Jasmine Hogan',
    'MEINE_ORGANISATION_ADRESSE_1': '',
    'MEINE_ORGANISATION_ADRESSE_2': 'Natalieside',
    'MEINE_ORGANISATION_EMAIL': 'vboone@gmail.com',
    'MEINE_ORGANISATION_NAME': 'John Thomas',
    'MEINE_ORGANISATION_NAME_ADRESSE': 'John Thomas, Natalieside',
    'MEINE_ORGANISATION_NAME_KURZ': 'John Thomas',
    'MEINE_ORGANISATION_ORT': 'Natalieside',
    'MEINE_ORGANISATION_TELEFON': '',
    'MES_EMOLUMENTS': [
        {
            'BETRAG': '739.39',
            'POSITION': ''
        },
        {
            'BETRAG': '871.33',
            'POSITION': ''
        }
    ],
    'MES_EMOLUMENTS_TOTAL': '1’610.72',
    'MODIFICATION_DATE': '',
    'MODIFICATION_TIME': '',
    'MON_ORGANISATION_ADRESSE_1': '',
    'MON_ORGANISATION_ADRESSE_2': 'Natalieside',
    'MON_ORGANISATION_EMAIL': 'vboone@gmail.com',
    'MON_ORGANISATION_LIEU': 'Natalieside',
    'MON_ORGANISATION_NOM': 'John Thomas',
    'MON_ORGANISATION_NOM_ABR': 'John Thomas',
    'MON_ORGANISATION_NOM_ADRESSE': 'John Thomas, Natalieside',
    'MON_ORGANISATION_TELEPHONE': '',
    'MUNICIPALITY': 'William Rodriguez',
    'MUNICIPALITY_ADDRESS': 'West Hannahfort',
    'NAME': '',
    'NEBENBESTIMMUNGEN': 'Baby strategy majority address eight least season.',
    'NEBENBESTIMMUNGEN_MAPPED': [
        {
            'FACHSTELLE': 'John Thomas',
            'TEXT': 'Baby strategy majority address eight least season.'
        }
    ],
    'NOM_LEGAL': 'ACME AG',
    'NUTZUNG': 'Wohnen',
    'NUTZUNGSZONE': 'Wohnzone W2',
    'OFFICES_CANTONAUX': [
        {
            'FRIST': '05.09.2021',
            'NAME': 'Amy Ho'
        },
        {
            'FRIST': '07.09.2021',
            'NAME': 'Angela Roberts'
        },
        {
            'FRIST': '18.09.2021',
            'NAME': 'Christopher Murphy'
        },
        {
            'FRIST': '08.09.2021',
            'NAME': 'Kaitlin Smith'
        },
        {
            'FRIST': '23.09.2021',
            'NAME': 'John Thomas'
        },
        {
            'FRIST': '17.09.2021',
            'NAME': 'Alison Russell'
        }
    ],
    'OFFICES_CANTONAUX_LISTE': '''- Amy Ho
- Angela Roberts
- Christopher Murphy
- Kaitlin Smith
- John Thomas
- Alison Russell''',
    'PARCELLE': '473, 2592',
    'PARZELLE': '473, 2592',
    'PLAN_QUARTIER': 'Überbauung XY',
    'PRISE_DE_POSITION': 'Rich individual challenge crime hotel.',
    'PROJEKTVERFASSER': 'Hans Müller',
    'PROJEKTVERFASSER_ADDRESS_1': 'Einweg 9',
    'PROJEKTVERFASSER_ADDRESS_2': '3000 Bern',
    'PROJEKTVERFASSER_ADRESSE_1': 'Einweg 9',
    'PROJEKTVERFASSER_ADRESSE_2': '3000 Bern',
    'PROJEKTVERFASSER_NAME_ADDRESS': 'Hans Müller, Einweg 9, 3000 Bern',
    'PROJEKTVERFASSER_NAME_ADRESSE': 'Hans Müller, Einweg 9, 3000 Bern',
    'PROJET_CONSTR': 'Neubau, Grosses Haus',
    'PROJET_CONSTR_DESCR': 'Grosses Haus',
    'PROPRIETAIRE_FONC': 'Sandra Holzer',
    'PROPRIETAIRE_FONC_ADRESSE_1': 'Bernweg 12',
    'PROPRIETAIRE_FONC_ADRESSE_2': '3002 Bern',
    'PROPRIETAIRE_FONC_NOM_ADRESSE': 'Sandra Holzer, Bernweg 12, 3002 Bern',
    'PROPRIETAIRE_FONC_TOUS': 'Sandra Holzer',
    'PROPRIETAIRE_FONC_TOUS_NOM_ADRESSE': 'Sandra Holzer, Bernweg 12, 3002 Bern',
    'PROPRIETAIRE_IMMOB': 'Peter Meier',
    'PROPRIETAIRE_IMMOB_ADRESSE_1': 'Thunstrasse 88',
    'PROPRIETAIRE_IMMOB_ADRESSE_2': '3002 Bern',
    'PROPRIETAIRE_IMMOB_NOM_ADRESSE': 'Peter Meier, Thunstrasse 88, 3002 Bern',
    'PROPRIETAIRE_IMMOB_TOUS_NOM_ADRESSE': 'Peter Meier, Thunstrasse 88, 3002 Bern',
    'PUBLICATION_1_FEUILLE_AVIS': '30. August 2021',
    'PUBLICATION_2_FEUILLE_AVIS': '20. August 2021',
    'PUBLICATION_DEBUT': '1. September 2021',
    'PUBLICATION_EXPIRATION': '15. September 2021',
    'PUBLICATION_FEUILLE_AVIS_NOM': 'Bärnerblatt',
    'PUBLICATION_FEUILLE_OFFICIELLE': '10. August 2021',
    'PUBLICATION_TEXTE': 'Text',
    'PUBLIKATION_1_ANZEIGER': '30. August 2021',
    'PUBLIKATION_2_ANZEIGER': '20. August 2021',
    'PUBLIKATION_AMTSBLATT': '10. August 2021',
    'PUBLIKATION_ANZEIGER_NAME': 'Bärnerblatt',
    'PUBLIKATION_ENDE': '15. September 2021',
    'PUBLIKATION_START': '1. September 2021',
    'PUBLIKATION_TEXT': 'Text',
    'RECENSEMENT': 'Ja, Nein, Nein, Nein, Ja, Ja',
    'REPRESENTANT': 'Mustermann und Söhne AG',
    'REPRESENTANT_ADRESSE_1': 'Juristenweg 99',
    'REPRESENTANT_ADRESSE_2': '3008 Bern',
    'REPRESENTANT_NOM_ADRESSE': 'Mustermann und Söhne AG, Juristenweg 99, 3008 Bern',
    'REPRESENTANT_TOUS': 'Mustermann und Söhne AG',
    'REPRESENTANT_TOUS_NOM_ADRESSE': 'Mustermann und Söhne AG, Juristenweg 99, 3008 Bern',
    'REQUERANT': 'ACME AG, Max Mustermann',
    'REQUERANT_ADRESSE_1': 'Teststrasse 123',
    'REQUERANT_ADRESSE_2': '1234 Testhausen',
    'REQUERANT_NOM_ADRESSE': 'ACME AG, Max Mustermann, Teststrasse 123, 1234 Testhausen',
    'REQUERANT_TOUS': 'ACME AG, Max Mustermann',
    'REQUERANT_TOUS_NOM_ADRESSE': 'ACME AG, Max Mustermann, Teststrasse 123, 1234 Testhausen',
    'RESPONSABLE_AUTORITE_DIRECTRICE': 'Jasmine Hogan',
    'RESPONSABLE_EMAIL': 'operez@yahoo.com',
    'RESPONSABLE_NOM': 'Jasmine Hogan',
    'RESPONSABLE_TELEPHONE': '',
    'SACHVERHALT': 'Sachverhalt Test',
    'SECTEUR_PROTECTION_EAUX': 'Aᵤ',
    'SITUATION': 'Sachverhalt Test',
    'SPRACHE': 'de',
    'STATUS': 'David Rangel',
    'STELLUNGNAHME': 'Rich individual challenge crime hotel.',
    'STICHWORTE': 'Robert Hernandez, Edward Travis, Robert Manning, Jesus Serrano, Ryan Jones',
    'TODAY': '30. August 2021',
    'UEBERBAUUNGSORDNUNG': 'Überbauung XY',
    'UVP_JA_NEIN': False,
    'VERTRETER': 'Mustermann und Söhne AG',
    'VERTRETER_ADDRESS_1': 'Juristenweg 99',
    'VERTRETER_ADDRESS_2': '3008 Bern',
    'VERTRETER_ADRESSE_1': 'Juristenweg 99',
    'VERTRETER_ADRESSE_2': '3008 Bern',
    'VERTRETER_NAME_ADDRESS': 'Mustermann und Söhne AG, Juristenweg 99, 3008 Bern',
    'VERTRETER_NAME_ADRESSE': 'Mustermann und Söhne AG, Juristenweg 99, 3008 Bern',
    'ZIRKULATION_ALLE': [
        {
            'FRIST': '05.09.2021',
            'NAME': 'Amy Ho'
        },
        {
            'FRIST': '07.09.2021',
            'NAME': 'Angela Roberts'
        },
        {
            'FRIST': '18.09.2021',
            'NAME': 'Christopher Murphy'
        },
        {
            'FRIST': '08.09.2021',
            'NAME': 'Kaitlin Smith'
        },
        {
            'FRIST': '23.09.2021',
            'NAME': 'John Thomas'
        },
        {
            'FRIST': '17.09.2021',
            'NAME': 'Alison Russell'
        }
    ],
    'ZIRKULATION_FACHSTELLEN': [
        {
            'FRIST': '17.09.2021',
            'NAME': 'Alison Russell'
        }
    ],
    'ZIRKULATION_GEMEINDEN': [
        {
            'FRIST': '18.09.2021',
            'NAME': 'Christopher Murphy'
        },
        {
            'FRIST': '08.09.2021',
            'NAME': 'Kaitlin Smith'
        }
    ],
    'ZIRKULATION_RSTA': [
        {
            'FRIST': '05.09.2021',
            'NAME': 'Amy Ho'
        },
        {
            'FRIST': '07.09.2021',
            'NAME': 'Angela Roberts'
        }
    ],
    'ZIRKULATION_RUECKMELDUNGEN': [
        {
            'ANTWORT': 'Christopher Woods',
            'NEBENBESTIMMUNGEN': 'Baby strategy majority address eight least season.',
            'STELLUNGNAHME': 'Rich individual challenge crime hotel.',
            'VON': 'John Thomas'
        },
        {
            'ANTWORT': 'Priscilla Rogers',
            'NEBENBESTIMMUNGEN': 'Within foot assume management floor free.',
            'STELLUNGNAHME': 'Expect mother role economy sense model tonight leave.',
            'VON': 'Alison Russell'
        }
    ],
    'ZUSTAENDIG_EMAIL': 'operez@yahoo.com',
    'ZUSTAENDIG_NAME': 'Jasmine Hogan',
    'ZUSTAENDIG_PHONE': '',
    'ZUSTAENDIG_TELEFON': ''
}
