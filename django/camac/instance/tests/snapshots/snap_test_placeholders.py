# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['test_dms_placeholders[Municipality] 1'] = {
    'ACE': 'Ja',
    'ADDRESS': 'Musterstrasse 4, 3000 Musterhausen',
    'ADMINISTRATIVE_DISTRICT': 'Emmental',
    'ADRESSE': 'Musterstrasse 4, 3000 Musterhausen',
    'AFFECTATION': 'Wohnen',
    'AFFECTATION_ZONE': 'Wohnzone W2',
    'ALCOHOL_SERVING': 'mit',
    'ALKOHOLAUSSCHANK': 'mit',
    'ALLE_GEBAEUDEEIGENTUEMER': 'Peter Meier',
    'ALLE_GEBAEUDEEIGENTUEMER_NAME_ADDRESS': 'Peter Meier, Thunstrasse 88, 3002 Bern',
    'ALLE_GEBAEUDEEIGENTUEMER_NAME_ADRESSE': 'Peter Meier, Thunstrasse 88, 3002 Bern',
    'ALLE_GESUCHSTELLER': 'ACME AG, Max Mustermann',
    'ALLE_GESUCHSTELLER_NAME_ADDRESS': 'ACME AG, Max Mustermann, Teststrasse 123, 1234 Testhausen',
    'ALLE_GESUCHSTELLER_NAME_ADRESSE': 'ACME AG, Max Mustermann, Teststrasse 123, 1234 Testhausen',
    'ALLE_GRUNDEIGENTUEMER': 'Sandra Holzer',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADDRESS': 'Sandra Holzer, Bernweg 12, 3002 Bern',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADRESSE': 'Sandra Holzer, Bernweg 12, 3002 Bern',
    'ALLE_NACHBARN': [
        {
            'ADDRESS_1': 'Teststrasse 124',
            'ADDRESS_2': '1234 Testhausen',
            'ADRESSE_1': 'Teststrasse 124',
            'ADRESSE_2': '1234 Testhausen',
            'NAME': 'Karl Nachbarsson',
            'NOM': 'Karl Nachbarsson'
        }
    ],
    'ALLE_PROJEKTVERFASSER': 'Hans Müller',
    'ALLE_PROJEKTVERFASSER_NAME_ADDRESS': 'Hans Müller, Einweg 9, 3000 Bern',
    'ALLE_PROJEKTVERFASSER_NAME_ADRESSE': 'Hans Müller, Einweg 9, 3000 Bern',
    'ALLE_VERTRETER': 'Mustermann und Söhne AG',
    'ALLE_VERTRETER_NAME_ADDRESS': 'Mustermann und Söhne AG, Juristenweg 99, 3008 Bern',
    'ALLE_VERTRETER_NAME_ADRESSE': 'Mustermann und Söhne AG, Juristenweg 99, 3008 Bern',
    'ANZAHL_BEHERBERGTE_PERSONEN': '',
    'ARRONDISSEMENT_ADMINISTRATIF': 'Emmental',
    'ASCENSEURS': [
    ],
    'AUFZUGSANLAGEN': [
    ],
    'AUJOURD_HUI': '30. August 2021',
    'AUTEUR_PROJET': 'Hans Müller',
    'AUTEUR_PROJET_ADRESSE_1': 'Einweg 9',
    'AUTEUR_PROJET_ADRESSE_2': '3000 Bern',
    'AUTEUR_PROJET_NOM_ADRESSE': 'Hans Müller, Einweg 9, 3000 Bern',
    'AUTEUR_PROJET_TOUS': 'Hans Müller',
    'AUTEUR_PROJET_TOUS_NOM_ADRESSE': 'Hans Müller, Einweg 9, 3000 Bern',
    'AUTORITE_DIRECTRICE_ADRESSE_1': '',
    'AUTORITE_DIRECTRICE_ADRESSE_2': 'Jeffreyfort',
    'AUTORITE_DIRECTRICE_EMAIL': 'judithallen@example.com',
    'AUTORITE_DIRECTRICE_LIEU': 'Jeffreyfort',
    'AUTORITE_DIRECTRICE_NOM': 'Matthew Bowen',
    'AUTORITE_DIRECTRICE_NOM_ABR': 'Matthew Bowen',
    'AUTORITE_DIRECTRICE_TELEPHONE': '',
    'BASE_URL': 'http://ebau.local',
    'BAUEINGABE_DATUM': '31. März 2021',
    'BAUENTSCHEID': 'Bewilligt',
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
    'BAUGRUPPE': 'Ja',
    'BAUGRUPPE_BEZEICHNUNG': 'Test Baugruppe',
    'BAUKOSTEN': 199000,
    'BAUVORHABEN': 'Neubau, Grosses Haus',
    'BESCHREIBUNG_BAUVORHABEN': 'Grosses Haus',
    'BESCHREIBUNG_PROJEKTAENDERUNG': 'Doch eher kleines Haus',
    'BOISSONS_ALCOOLIQUES': 'mit',
    'BUILDING_DISTANCES': [
    ],
    'CHAMBRES_AVEC_PLUS_DE_50_PERSONNES': [
    ],
    'CIRCULATION_COMMUNES': [
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '03.03.1970',
            'ERSTELLT': '30.08.2021',
            'FRIST': '03.03.1970',
            'NAME': 'John Ward',
            'NOM': 'John Ward',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '26.01.1999',
            'ERSTELLT': '30.08.2021',
            'FRIST': '26.01.1999',
            'NAME': 'Brittany Hill',
            'NOM': 'Brittany Hill',
            'REPONDU': ''
        }
    ],
    'CIRCULATION_PREAVIS': [
        {
            'ANTWORT': 'Baubewilligungspflichtig',
            'DE': 'Dale Summers',
            'DISPOSITIONS_ACCESSOIRES': 'Nebenbestimmungen 5',
            'NEBENBESTIMMUNGEN': 'Nebenbestimmungen 5',
            'POINT_DE_VUE': 'Stellungnahme 5',
            'REPONSE': 'Baubewilligungspflichtig',
            'STELLUNGNAHME': 'Stellungnahme 5',
            'VON': 'Dale Summers'
        },
        {
            'ANTWORT': 'Nicht betroffen / nicht zuständig',
            'DE': 'Robert Cowan',
            'DISPOSITIONS_ACCESSOIRES': 'Nebenbestimmungen 6',
            'NEBENBESTIMMUNGEN': 'Nebenbestimmungen 6',
            'POINT_DE_VUE': 'Stellungnahme 6',
            'REPONSE': 'Nicht betroffen / nicht zuständig',
            'STELLUNGNAHME': 'Stellungnahme 6',
            'VON': 'Robert Cowan'
        }
    ],
    'CIRCULATION_PREF': [
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '29.01.2021',
            'ERSTELLT': '30.08.2021',
            'FRIST': '29.01.2021',
            'NAME': 'Scott Clark',
            'NOM': 'Scott Clark',
            'REPONDU': ''
        }
    ],
    'CIRCULATION_SERVICES': [
        {
            'BEANTWORTET': '13.02.1982',
            'CREE': '30.08.2021',
            'DELAI': '17.06.1987',
            'ERSTELLT': '30.08.2021',
            'FRIST': '17.06.1987',
            'NAME': 'Dale Summers',
            'NOM': 'Dale Summers',
            'REPONDU': '13.02.1982'
        },
        {
            'BEANTWORTET': '15.08.1971',
            'CREE': '30.08.2021',
            'DELAI': '24.08.2008',
            'ERSTELLT': '30.08.2021',
            'FRIST': '24.08.2008',
            'NAME': 'Robert Cowan',
            'NOM': 'Robert Cowan',
            'REPONDU': '15.08.1971'
        }
    ],
    'COMMUNE': 'Burgdorf',
    'COMMUNE_ADRESSE': 'Jacobmouth',
    'COMMUNE_ADRESSE_1': '',
    'COMMUNE_ADRESSE_2': 'Jacobmouth',
    'COMMUNE_EMAIL': 'jhill@example.net',
    'COMMUNE_LIEU': 'Jacobmouth',
    'COMMUNE_NOM_ADRESSE': 'Gemeinde Burgdorf, Jacobmouth',
    'COMMUNE_TELEPHONE': '',
    'COMMUNICATION_AUX_VOISINS_CODE_QR': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADLElEQVR4nO2bQW7jOBBFX40EeEkBfQAfhbrBHCnom1lHyQEaEJcGSPxZkFSU9Cym4YztRMWFIFp6MAsgqoq/Sib+eCx//TkDDjnkkEMOOeTQ94SsjREWG7E5jUBqU0j9hfkhy3PojhCSJKIkaR3qHTCoPoBBxLVPoyRdntwmhz4DSt0BLGamS7iazRSDkOsL1YM8ankOPQ6K6yB7WakBQ5f/758cekpo/DDXcr6alukXgjIS1zKK9KjlOXR3qO+IICAB8XWEuCKDoV4A2CtZT26TQ58ALWZmNoHNDKpnjbhSLzZT6lHjUctz6N4+Yu8AwtVEKibI9Lv3WveT2+TQ7ZDNQBcgTjKbgGUqzSksVahwH3EEqOoR0gq6hIwuQSKusPtNyrBpFK5HfGtop1DVxAGAqLxtlU2cWvv28R1xCKgYhG1bpHYGsRlawFimRy7PoXtBzUds0mQLHWzhZOcesvuIw0BNmgwS8fUkm4GmbKeeTy7TloF+CZscuuX0aXCSkcZs8XLtRwqGbATBcs6jxbX0Q+iT2+TQLdAugWxlzyARldnVQwF0YfDa5wGgzUdgIk1omZuL0DKt/a3wazTCNn1ymxz6FGio7sFmANKIvbxaK4nH15N0SV4NPxAUlbE5je2s8XOiXgB+L4l/DZscur2uETLVPRBWLKqMtSi6/H01oJhnloeBatEimdlLVayLtY6Zt1gRMjY/ZnkOPUDFzjVg0BorAUKuxY3qPLZmSz9rfGto8wCDDE6C9AMt5zwKattMBhDL+epR42BQVBOn7GUdBMlM0tVamSOd9C/Q/Zbn0F2gra7RS+J6L061Zn36bx41jgH1dEHvShoU08+pWNsWaaQ9/RI2OXSrZgkwZMEglglaL10NGD9qadTziMNAsTdS9ea5rf1WmV4rL95VdyBo+6arjWK9z3JQ65g5yzPLQ0JVe2i9M60/Ikj7TfPlbHLov4+P33S1Q2bII3EtqPXSlXfvPblNDt0C/f5Nl3qsALC41qTyTau66/IcujvU9Yg6BjXtuvdevnXM7PqzXY/4ztDHb7q0zdpdyNvTwTNLhxxyyCGHHHJoN/4BMBD7kv22h4gAAAAASUVORK5CYII=',
    'COMMUNICATION_AUX_VOISINS_LIEN': 'http://ebau-portal.local/public-instances/1/form?key=5a49823',
    'CONSERVABLE': 'Nein',
    'CONSTRUCTION_COSTS': 199000,
    'CONSTRUCTION_GROUP': 'Ja',
    'CONSTRUCTION_GROUP_DESIGNATION': 'Test Baugruppe',
    'CONTRACT': 'Ja',
    'CONTRACT_START': '1. Februar 2022',
    'CONTRAT': 'Ja',
    'CONTRAT_DATE': '1. Februar 2022',
    'COORDONEE': '2’599’941 / 1’198’923; 2’601’995 / 1’201’340',
    'COUTS_DE_CONSTRUCTION': 199000,
    'DECISION': 'accepted',
    'DECISION_CATEGORIE': 'GESAMT',
    'DECISION_DATE': '30. August 2021',
    'DECISION_GENERAL': False,
    'DECISION_GLOBALE': True,
    'DECISION_MODIF': False,
    'DECISION_PARTIEL': False,
    'DECISION_PERMIS': False,
    'DECISION_PETIT': False,
    'DECISION_POSITIVE': True,
    'DECISION_POSITIVE_PARTIEL': True,
    'DECISION_REFUS': False,
    'DECISION_REFUS_AVEC_RET': False,
    'DECISION_REFUS_SANS_RET': False,
    'DECISION_TYPE': 'GESAMT',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES': [
        {
            'ANLIEGEN': '''Test LAB 1
Test LAB 2''',
            'DATE_DOCUMENT': '01.10.2022',
            'DATE_RECEPTION': '02.10.2022',
            'DATUM_DOKUMENT': '01.10.2022',
            'DATUM_EINGANG': '02.10.2022',
            'DEMANDE_REQUETE': '''Test LAB 1
Test LAB 2''',
            'PREOCCUPATION': '''Test LAB 1
Test LAB 2''',
            'RECHTSBEGEHRENDE': 'Lastenausgleichsbegehren4you AG',
            'REQUERANTS_CONCLUSIONS': 'Lastenausgleichsbegehren4you AG',
            'TITEL': 'Test Lastenausgleichsbegehren',
            'TITRE': 'Test Lastenausgleichsbegehren'
        }
    ],
    'DEPOT_DEMANDE_DATE': '31. März 2021',
    'DESCRIPTION_MODIFICATION': 'Doch eher kleines Haus',
    'DIMENSIONEN_HOEHE': '',
    'DIMENSION_HAUTEUR': '',
    'DIMENSION_HEIGHT': '',
    'DISPOSITIONS_ACCESSOIRES': 'Nebenbestimmungen 1',
    'DISPOSITIONS_ANNEXES': 'Nebenbestimmungen 1',
    'DISTANCES_ENTRE_LES_BATIMENTS': [
    ],
    'DOSSIER_LINK': 'http://ebau.local/index/redirect-to-instance-resource/instance-id/1',
    'DOSSIER_NR': 1,
    'DOSSIER_NUMERO': 1,
    'DOSSIER_TYP': 'Baugesuch',
    'DOSSIER_TYPE': 'Baugesuch',
    'EBAU_NR': '2021-1',
    'EBAU_NUMBER': '2021-1',
    'EBAU_NUMERO': '2021-1',
    'EBAU_URL': 'http://ebau.local',
    'EIGENE_GEBUEHREN': [
        {
            'BETRAG': '103.04',
            'FORFAIT': '103.04',
            'POSITION': ''
        },
        {
            'BETRAG': '31.59',
            'FORFAIT': '31.59',
            'POSITION': ''
        }
    ],
    'EIGENE_GEBUEHREN_TOTAL': '134.63',
    'EIGENE_NEBENBESTIMMUNGEN': 'Nebenbestimmungen 1',
    'EIGENE_STELLUNGNAHMEN': 'Stellungnahme 1',
    'EINSPRACHEN': [
        {
            'DATE_DOCUMENT': '01.12.2022',
            'DATE_RECEPTION': '02.12.2022',
            'DATUM_DOKUMENT': '01.12.2022',
            'DATUM_EINGANG': '02.12.2022',
            'GRIEFS': '''Test E 1
Test E 2''',
            'RECHTSBEGEHRENDE': 'Heinz Einsprachenmann',
            'REQUERANTS_CONCLUSIONS': 'Heinz Einsprachenmann',
            'RUEGEPUNKTE': '''Test E 1
Test E 2''',
            'TITEL': 'Test Einsprache',
            'TITRE': 'Test Einsprache'
        }
    ],
    'EINSPRECHENDE': [
        {
            'ADDRESS': 'Beispielstrasse 1, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 1, 4321 Beispieldorf',
            'NAME': 'Heinz Einsprachenmann',
            'NOM': 'Heinz Einsprachenmann'
        }
    ],
    'EMAIL': '',
    'EMOLUMENTS': [
        {
            'BETRAG': '553.85',
            'FORFAIT': '553.85',
            'POSITION': ''
        },
        {
            'BETRAG': '21.60',
            'FORFAIT': '21.60',
            'POSITION': ''
        },
        {
            'BETRAG': '103.04',
            'FORFAIT': '103.04',
            'POSITION': ''
        },
        {
            'BETRAG': '31.59',
            'FORFAIT': '31.59',
            'POSITION': ''
        }
    ],
    'EMOLUMENTS_TOTAL': '710.08',
    'ENSEMBLE_BÂTI': 'Ja',
    'ENSEMBLE_BÂTI_DÉNOMINATION': 'Test Baugruppe',
    'ERHALTENSWERT': 'Nein',
    'ETAT': 'Pamela Horton',
    'FACHSTELLEN_KANTONAL': [
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '16.10.2004',
            'ERSTELLT': '30.08.2021',
            'FRIST': '16.10.2004',
            'NAME': 'Matthew Bowen',
            'NOM': 'Matthew Bowen',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '29.01.2021',
            'ERSTELLT': '30.08.2021',
            'FRIST': '29.01.2021',
            'NAME': 'Scott Clark',
            'NOM': 'Scott Clark',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '03.03.1970',
            'ERSTELLT': '30.08.2021',
            'FRIST': '03.03.1970',
            'NAME': 'John Ward',
            'NOM': 'John Ward',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '26.01.1999',
            'ERSTELLT': '30.08.2021',
            'FRIST': '26.01.1999',
            'NAME': 'Brittany Hill',
            'NOM': 'Brittany Hill',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '13.02.1982',
            'CREE': '30.08.2021',
            'DELAI': '17.06.1987',
            'ERSTELLT': '30.08.2021',
            'FRIST': '17.06.1987',
            'NAME': 'Dale Summers',
            'NOM': 'Dale Summers',
            'REPONDU': '13.02.1982'
        },
        {
            'BEANTWORTET': '15.08.1971',
            'CREE': '30.08.2021',
            'DELAI': '24.08.2008',
            'ERSTELLT': '30.08.2021',
            'FRIST': '24.08.2008',
            'NAME': 'Robert Cowan',
            'NOM': 'Robert Cowan',
            'REPONDU': '15.08.1971'
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '',
            'ERSTELLT': '30.08.2021',
            'FRIST': '',
            'NAME': 'Matthew Bowen',
            'NOM': 'Matthew Bowen',
            'REPONDU': ''
        }
    ],
    'FACHSTELLEN_KANTONAL_LIST': '''- Matthew Bowen
- Scott Clark
- John Ward
- Brittany Hill
- Dale Summers
- Robert Cowan
- Matthew Bowen''',
    'FACHSTELLEN_KANTONAL_LISTE': '''- Matthew Bowen
- Scott Clark
- John Ward
- Brittany Hill
- Dale Summers
- Robert Cowan
- Matthew Bowen''',
    'FIRE_PROTECTION_SYSTEMS': [
    ],
    'FLOOR_AREA': '',
    'FORM_NAME': 'Baugesuch',
    'GEBAEUDEABSTAENDE': [
    ],
    'GEBAEUDEEIGENTUEMER': 'Peter Meier',
    'GEBAEUDEEIGENTUEMER_ADDRESS_1': 'Thunstrasse 88',
    'GEBAEUDEEIGENTUEMER_ADDRESS_2': '3002 Bern',
    'GEBAEUDEEIGENTUEMER_ADRESSE_1': 'Thunstrasse 88',
    'GEBAEUDEEIGENTUEMER_ADRESSE_2': '3002 Bern',
    'GEBAEUDEEIGENTUEMER_NAME_ADDRESS': 'Peter Meier, Thunstrasse 88, 3002 Bern',
    'GEBAEUDEEIGENTUEMER_NAME_ADRESSE': 'Peter Meier, Thunstrasse 88, 3002 Bern',
    'GEBUEHREN': [
        {
            'BETRAG': '553.85',
            'FORFAIT': '553.85',
            'POSITION': ''
        },
        {
            'BETRAG': '21.60',
            'FORFAIT': '21.60',
            'POSITION': ''
        },
        {
            'BETRAG': '103.04',
            'FORFAIT': '103.04',
            'POSITION': ''
        },
        {
            'BETRAG': '31.59',
            'FORFAIT': '31.59',
            'POSITION': ''
        }
    ],
    'GEBUEHREN_TOTAL': '710.08',
    'GEFAEHRLICHE_STOFFE': [
    ],
    'GEMEINDE': 'Burgdorf',
    'GEMEINDE_ADRESSE': 'Jacobmouth',
    'GEMEINDE_ADRESSE_1': '',
    'GEMEINDE_ADRESSE_2': 'Jacobmouth',
    'GEMEINDE_EMAIL': 'jhill@example.net',
    'GEMEINDE_NAME_ADRESSE': 'Gemeinde Burgdorf, Jacobmouth',
    'GEMEINDE_ORT': 'Jacobmouth',
    'GEMEINDE_TELEFON': '',
    'GESCHOSSFLAECHE': '',
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
    'HAZARDOUS_SUBSTANCES': [
    ],
    'HEATING_SYSTEMS': [
    ],
    'HEUTE': '30. August 2021',
    'INFORMATION_OF_NEIGHBORS_LINK': 'http://ebau-portal.local/public-instances/1/form?key=5a49823',
    'INFORMATION_OF_NEIGHBORS_QR_CODE': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADLElEQVR4nO2bQW7jOBBFX40EeEkBfQAfhbrBHCnom1lHyQEaEJcGSPxZkFSU9Cym4YztRMWFIFp6MAsgqoq/Sib+eCx//TkDDjnkkEMOOeTQ94SsjREWG7E5jUBqU0j9hfkhy3PojhCSJKIkaR3qHTCoPoBBxLVPoyRdntwmhz4DSt0BLGamS7iazRSDkOsL1YM8ankOPQ6K6yB7WakBQ5f/758cekpo/DDXcr6alukXgjIS1zKK9KjlOXR3qO+IICAB8XWEuCKDoV4A2CtZT26TQ58ALWZmNoHNDKpnjbhSLzZT6lHjUctz6N4+Yu8AwtVEKibI9Lv3WveT2+TQ7ZDNQBcgTjKbgGUqzSksVahwH3EEqOoR0gq6hIwuQSKusPtNyrBpFK5HfGtop1DVxAGAqLxtlU2cWvv28R1xCKgYhG1bpHYGsRlawFimRy7PoXtBzUds0mQLHWzhZOcesvuIw0BNmgwS8fUkm4GmbKeeTy7TloF+CZscuuX0aXCSkcZs8XLtRwqGbATBcs6jxbX0Q+iT2+TQLdAugWxlzyARldnVQwF0YfDa5wGgzUdgIk1omZuL0DKt/a3wazTCNn1ymxz6FGio7sFmANKIvbxaK4nH15N0SV4NPxAUlbE5je2s8XOiXgB+L4l/DZscur2uETLVPRBWLKqMtSi6/H01oJhnloeBatEimdlLVayLtY6Zt1gRMjY/ZnkOPUDFzjVg0BorAUKuxY3qPLZmSz9rfGto8wCDDE6C9AMt5zwKattMBhDL+epR42BQVBOn7GUdBMlM0tVamSOd9C/Q/Zbn0F2gra7RS+J6L061Zn36bx41jgH1dEHvShoU08+pWNsWaaQ9/RI2OXSrZgkwZMEglglaL10NGD9qadTziMNAsTdS9ea5rf1WmV4rL95VdyBo+6arjWK9z3JQ65g5yzPLQ0JVe2i9M60/Ikj7TfPlbHLov4+P33S1Q2bII3EtqPXSlXfvPblNDt0C/f5Nl3qsALC41qTyTau66/IcujvU9Yg6BjXtuvdevnXM7PqzXY/4ztDHb7q0zdpdyNvTwTNLhxxyyCGHHHJoN/4BMBD7kv22h4gAAAAASUVORK5CYII=',
    'INSTALLATIONS_AERAULIQUES': [
    ],
    'INSTALLATIONS_TECH_LINCENDIE': [
    ],
    'INSTANCE_ID': 1,
    'INTERIOR_SEATING': 35,
    'INVENTAR': 'Schützenswert, K-Objekt, Baugruppe Bauinventar: Test Baugruppe, RRB vom 1. Januar 2022, Vertrag vom 1. Februar 2022',
    'JURISTIC_NAME': 'ACME AG',
    'JURISTISCHER_NAME': 'ACME AG',
    'KOORDINATEN': '2’599’941 / 1’198’923; 2’601’995 / 1’201’340',
    'K_OBJECT': 'Ja',
    'K_OBJEKT': 'Ja',
    'LANGUAGE': 'de',
    'LANGUE': 'de',
    'LASTENAUSGLEICHSBEGEHREN': [
        {
            'ANLIEGEN': '''Test LAB 1
Test LAB 2''',
            'DATE_DOCUMENT': '01.10.2022',
            'DATE_RECEPTION': '02.10.2022',
            'DATUM_DOKUMENT': '01.10.2022',
            'DATUM_EINGANG': '02.10.2022',
            'DEMANDE_REQUETE': '''Test LAB 1
Test LAB 2''',
            'PREOCCUPATION': '''Test LAB 1
Test LAB 2''',
            'RECHTSBEGEHRENDE': 'Lastenausgleichsbegehren4you AG',
            'REQUERANTS_CONCLUSIONS': 'Lastenausgleichsbegehren4you AG',
            'TITEL': 'Test Lastenausgleichsbegehren',
            'TITRE': 'Test Lastenausgleichsbegehren'
        }
    ],
    'LASTENAUSGLEICHSBEGEHRENDE': [
        {
            'ADDRESS': 'Beispielstrasse 3, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 3, 4321 Beispieldorf',
            'NAME': 'Lastenausgleichsbegehren4you AG',
            'NOM': 'Lastenausgleichsbegehren4you AG'
        }
    ],
    'LEGAL_CLAIMANTS': [
        {
            'ADDRESS': 'Beispielstrasse 1, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 1, 4321 Beispieldorf',
            'NAME': 'Heinz Einsprachenmann',
            'NOM': 'Heinz Einsprachenmann'
        },
        {
            'ADDRESS': 'Beispielstrasse 2, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 2, 4321 Beispieldorf',
            'NAME': 'Martha Rechstverwahrungsson',
            'NOM': 'Martha Rechstverwahrungsson'
        },
        {
            'ADDRESS': 'Beispielstrasse 3, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 3, 4321 Beispieldorf',
            'NAME': 'Lastenausgleichsbegehren4you AG',
            'NOM': 'Lastenausgleichsbegehren4you AG'
        }
    ],
    'LEGAL_CUSTODIANS': [
        {
            'ADDRESS': 'Beispielstrasse 2, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 2, 4321 Beispieldorf',
            'NAME': 'Martha Rechstverwahrungsson',
            'NOM': 'Martha Rechstverwahrungsson'
        }
    ],
    'LEITBEHOERDE_ADDRESS_1': '',
    'LEITBEHOERDE_ADDRESS_2': 'Jeffreyfort',
    'LEITBEHOERDE_ADRESSE_1': '',
    'LEITBEHOERDE_ADRESSE_2': 'Jeffreyfort',
    'LEITBEHOERDE_CITY': 'Jeffreyfort',
    'LEITBEHOERDE_EMAIL': 'judithallen@example.com',
    'LEITBEHOERDE_NAME': 'Matthew Bowen',
    'LEITBEHOERDE_NAME_KURZ': 'Matthew Bowen',
    'LEITBEHOERDE_PHONE': '',
    'LEITBEHOERDE_STADT': 'Jeffreyfort',
    'LEITBEHOERDE_TELEFON': '',
    'LEITPERSON': 'Thomas Morgan',
    'LIEN_PUBLICATION': 'http://ebau-portal.local/public-instances/1',
    'LIFTS': [
    ],
    'LOAD_COMPENSATION_REQUESTING': [
        {
            'ADDRESS': 'Beispielstrasse 3, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 3, 4321 Beispieldorf',
            'NAME': 'Lastenausgleichsbegehren4you AG',
            'NOM': 'Lastenausgleichsbegehren4you AG'
        }
    ],
    'LUEFTUNGSANLAGEN': [
    ],
    'MATIERES_DANGEREUSES': [
    ],
    'MEINE_ORGANISATION_ADRESSE_1': '',
    'MEINE_ORGANISATION_ADRESSE_2': 'Jeffreyfort',
    'MEINE_ORGANISATION_EMAIL': 'judithallen@example.com',
    'MEINE_ORGANISATION_NAME': 'Matthew Bowen',
    'MEINE_ORGANISATION_NAME_ADRESSE': 'Matthew Bowen, Jeffreyfort',
    'MEINE_ORGANISATION_NAME_KURZ': 'Matthew Bowen',
    'MEINE_ORGANISATION_ORT': 'Jeffreyfort',
    'MEINE_ORGANISATION_TELEFON': '',
    'MES_EMOLUMENTS': [
        {
            'BETRAG': '103.04',
            'FORFAIT': '103.04',
            'POSITION': ''
        },
        {
            'BETRAG': '31.59',
            'FORFAIT': '31.59',
            'POSITION': ''
        }
    ],
    'MES_EMOLUMENTS_TOTAL': '134.63',
    'MODIFICATION_DATE': '',
    'MODIFICATION_TIME': '',
    'MON_ORGANISATION_ADRESSE_1': '',
    'MON_ORGANISATION_ADRESSE_2': 'Jeffreyfort',
    'MON_ORGANISATION_EMAIL': 'judithallen@example.com',
    'MON_ORGANISATION_LIEU': 'Jeffreyfort',
    'MON_ORGANISATION_NOM': 'Matthew Bowen',
    'MON_ORGANISATION_NOM_ABR': 'Matthew Bowen',
    'MON_ORGANISATION_NOM_ADRESSE': 'Matthew Bowen, Jeffreyfort',
    'MON_ORGANISATION_TELEPHONE': '',
    'MOTS_CLES': 'Andrew Berg MD, Alex Scott, Jacqueline Herrera, Kaitlyn Mendoza, Mary Mooney',
    'MUNICIPALITY': 'Burgdorf',
    'MUNICIPALITY_ADDRESS': 'Jacobmouth',
    'NACHBARSCHAFTSORIENTIERUNG_LINK': 'http://ebau-portal.local/public-instances/1/form?key=5a49823',
    'NACHBARSCHAFTSORIENTIERUNG_QR_CODE': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADLElEQVR4nO2bQW7jOBBFX40EeEkBfQAfhbrBHCnom1lHyQEaEJcGSPxZkFSU9Cym4YztRMWFIFp6MAsgqoq/Sib+eCx//TkDDjnkkEMOOeTQ94SsjREWG7E5jUBqU0j9hfkhy3PojhCSJKIkaR3qHTCoPoBBxLVPoyRdntwmhz4DSt0BLGamS7iazRSDkOsL1YM8ankOPQ6K6yB7WakBQ5f/758cekpo/DDXcr6alukXgjIS1zKK9KjlOXR3qO+IICAB8XWEuCKDoV4A2CtZT26TQ58ALWZmNoHNDKpnjbhSLzZT6lHjUctz6N4+Yu8AwtVEKibI9Lv3WveT2+TQ7ZDNQBcgTjKbgGUqzSksVahwH3EEqOoR0gq6hIwuQSKusPtNyrBpFK5HfGtop1DVxAGAqLxtlU2cWvv28R1xCKgYhG1bpHYGsRlawFimRy7PoXtBzUds0mQLHWzhZOcesvuIw0BNmgwS8fUkm4GmbKeeTy7TloF+CZscuuX0aXCSkcZs8XLtRwqGbATBcs6jxbX0Q+iT2+TQLdAugWxlzyARldnVQwF0YfDa5wGgzUdgIk1omZuL0DKt/a3wazTCNn1ymxz6FGio7sFmANKIvbxaK4nH15N0SV4NPxAUlbE5je2s8XOiXgB+L4l/DZscur2uETLVPRBWLKqMtSi6/H01oJhnloeBatEimdlLVayLtY6Zt1gRMjY/ZnkOPUDFzjVg0BorAUKuxY3qPLZmSz9rfGto8wCDDE6C9AMt5zwKattMBhDL+epR42BQVBOn7GUdBMlM0tVamSOd9C/Q/Zbn0F2gra7RS+J6L061Zn36bx41jgH1dEHvShoU08+pWNsWaaQ9/RI2OXSrZgkwZMEglglaL10NGD9qadTziMNAsTdS9ea5rf1WmV4rL95VdyBo+6arjWK9z3JQ65g5yzPLQ0JVe2i9M60/Ikj7TfPlbHLov4+P33S1Q2bII3EtqPXSlXfvPblNDt0C/f5Nl3qsALC41qTyTau66/IcujvU9Yg6BjXtuvdevnXM7PqzXY/4ztDHb7q0zdpdyNvTwTNLhxxyyCGHHHJoN/4BMBD7kv22h4gAAAAASUVORK5CYII=',
    'NAME': '',
    'NEBENBESTIMMUNGEN': 'Nebenbestimmungen 1',
    'NEBENBESTIMMUNGEN_MAPPED': [
        {
            'FACHSTELLE': 'Matthew Bowen',
            'SERVICE': 'Matthew Bowen',
            'TEXT': 'Nebenbestimmungen 1',
            'TEXTE': 'Nebenbestimmungen 1'
        }
    ],
    'NEIGHBORS': [
        {
            'ADDRESS_1': 'Teststrasse 124',
            'ADDRESS_2': '1234 Testhausen',
            'ADRESSE_1': 'Teststrasse 124',
            'ADRESSE_2': '1234 Testhausen',
            'NAME': 'Karl Nachbarsson',
            'NOM': 'Karl Nachbarsson'
        }
    ],
    'NOMBRE_DE_PERSONNES_ACCOMPAGNEES': '',
    'NOM_LEGAL': 'ACME AG',
    'NUMBER_OF_ACCOMODATED_PERSONS': '',
    'NUTZUNG': 'Wohnen',
    'NUTZUNGSZONE': 'Wohnzone W2',
    'OBJECTIONS': [
        {
            'DATE_DOCUMENT': '01.12.2022',
            'DATE_RECEPTION': '02.12.2022',
            'DATUM_DOKUMENT': '01.12.2022',
            'DATUM_EINGANG': '02.12.2022',
            'GRIEFS': '''Test E 1
Test E 2''',
            'RECHTSBEGEHRENDE': 'Heinz Einsprachenmann',
            'REQUERANTS_CONCLUSIONS': 'Heinz Einsprachenmann',
            'RUEGEPUNKTE': '''Test E 1
Test E 2''',
            'TITEL': 'Test Einsprache',
            'TITRE': 'Test Einsprache'
        }
    ],
    'OBJECT_C': 'Ja',
    'OCCUPATION_CHAMBRES_PLUS_50_PERSONNES': '',
    'OEFFENTLICHKEIT': 'Öffentlich',
    'OFFICES_CANTONAUX': [
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '16.10.2004',
            'ERSTELLT': '30.08.2021',
            'FRIST': '16.10.2004',
            'NAME': 'Matthew Bowen',
            'NOM': 'Matthew Bowen',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '29.01.2021',
            'ERSTELLT': '30.08.2021',
            'FRIST': '29.01.2021',
            'NAME': 'Scott Clark',
            'NOM': 'Scott Clark',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '03.03.1970',
            'ERSTELLT': '30.08.2021',
            'FRIST': '03.03.1970',
            'NAME': 'John Ward',
            'NOM': 'John Ward',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '26.01.1999',
            'ERSTELLT': '30.08.2021',
            'FRIST': '26.01.1999',
            'NAME': 'Brittany Hill',
            'NOM': 'Brittany Hill',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '13.02.1982',
            'CREE': '30.08.2021',
            'DELAI': '17.06.1987',
            'ERSTELLT': '30.08.2021',
            'FRIST': '17.06.1987',
            'NAME': 'Dale Summers',
            'NOM': 'Dale Summers',
            'REPONDU': '13.02.1982'
        },
        {
            'BEANTWORTET': '15.08.1971',
            'CREE': '30.08.2021',
            'DELAI': '24.08.2008',
            'ERSTELLT': '30.08.2021',
            'FRIST': '24.08.2008',
            'NAME': 'Robert Cowan',
            'NOM': 'Robert Cowan',
            'REPONDU': '15.08.1971'
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '',
            'ERSTELLT': '30.08.2021',
            'FRIST': '',
            'NAME': 'Matthew Bowen',
            'NOM': 'Matthew Bowen',
            'REPONDU': ''
        }
    ],
    'OFFICES_CANTONAUX_LISTE': '''- Matthew Bowen
- Scott Clark
- John Ward
- Brittany Hill
- Dale Summers
- Robert Cowan
- Matthew Bowen''',
    'OPPOSANTS': [
        {
            'ADDRESS': 'Beispielstrasse 1, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 1, 4321 Beispieldorf',
            'NAME': 'Heinz Einsprachenmann',
            'NOM': 'Heinz Einsprachenmann'
        }
    ],
    'OPPOSING': [
        {
            'ADDRESS': 'Beispielstrasse 1, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 1, 4321 Beispieldorf',
            'NAME': 'Heinz Einsprachenmann',
            'NOM': 'Heinz Einsprachenmann'
        }
    ],
    'OPPOSITIONS': [
        {
            'DATE_DOCUMENT': '01.12.2022',
            'DATE_RECEPTION': '02.12.2022',
            'DATUM_DOKUMENT': '01.12.2022',
            'DATUM_EINGANG': '02.12.2022',
            'GRIEFS': '''Test E 1
Test E 2''',
            'RECHTSBEGEHRENDE': 'Heinz Einsprachenmann',
            'REQUERANTS_CONCLUSIONS': 'Heinz Einsprachenmann',
            'RUEGEPUNKTE': '''Test E 1
Test E 2''',
            'TITEL': 'Test Einsprache',
            'TITRE': 'Test Einsprache'
        }
    ],
    'OUTSIDE_SEATING': 20,
    'OUVERTURE_PUBLIC': 'Öffentlich',
    'PANNEAUX_SOLAIRES': [
    ],
    'PARCELLE': '473, 2592',
    'PARZELLE': '473, 2592',
    'PLACES_ASSISES_EXT': 20,
    'PLACES_ASSISES_INT': 35,
    'PLAN_QUARTIER': 'Überbauung XY',
    'POINT_DE_VUE': 'Stellungnahme 1',
    'PRISE_DE_POSITION': 'Stellungnahme 1',
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
    'PROPRIETAIRE_IMMOB_TOUS': 'Peter Meier',
    'PROPRIETAIRE_IMMOB_TOUS_NOM_ADRESSE': 'Peter Meier, Thunstrasse 88, 3002 Bern',
    'PROTECTED': 'Ja',
    'PROTECTION_AREA': 'S1',
    'PROTÉGÉ': 'Ja',
    'PUBLIC': 'Öffentlich',
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
    'PUBLIKATION_LINK': 'http://ebau-portal.local/public-instances/1',
    'PUBLIKATION_START': '1. September 2021',
    'PUBLIKATION_TEXT': 'Text',
    'QS_RESPONSIBLE': '',
    'QS_VERANTWORTLICHER': '',
    'RAEUME_MEHR_50_PERSONEN': [
    ],
    'RAUM_BELEGUNG_MEHR_50_PERSONEN': '',
    'RECENSEMENT': 'Schützenswert, K-Objekt, Baugruppe Bauinventar: Test Baugruppe, RRB vom 1. Januar 2022, Vertrag vom 1. Februar 2022',
    'RECHTSBEGEHRENDE': [
        {
            'ADDRESS': 'Beispielstrasse 1, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 1, 4321 Beispieldorf',
            'NAME': 'Heinz Einsprachenmann',
            'NOM': 'Heinz Einsprachenmann'
        },
        {
            'ADDRESS': 'Beispielstrasse 2, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 2, 4321 Beispieldorf',
            'NAME': 'Martha Rechstverwahrungsson',
            'NOM': 'Martha Rechstverwahrungsson'
        },
        {
            'ADDRESS': 'Beispielstrasse 3, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 3, 4321 Beispieldorf',
            'NAME': 'Lastenausgleichsbegehren4you AG',
            'NOM': 'Lastenausgleichsbegehren4you AG'
        }
    ],
    'RECHTSVERWAHRENDE': [
        {
            'ADDRESS': 'Beispielstrasse 2, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 2, 4321 Beispieldorf',
            'NAME': 'Martha Rechstverwahrungsson',
            'NOM': 'Martha Rechstverwahrungsson'
        }
    ],
    'RECHTSVERWAHRUNGEN': [
        {
            'ANLIEGEN': '''Test RV 1
Test RV 2''',
            'DATE_DOCUMENT': '01.11.2022',
            'DATE_RECEPTION': '02.11.2022',
            'DATUM_DOKUMENT': '01.11.2022',
            'DATUM_EINGANG': '02.11.2022',
            'DEMANDE_REQUETE': '''Test RV 1
Test RV 2''',
            'PREOCCUPATION': '''Test RV 1
Test RV 2''',
            'RECHTSBEGEHRENDE': 'Martha Rechstverwahrungsson',
            'REQUERANTS_CONCLUSIONS': 'Martha Rechstverwahrungsson',
            'TITEL': 'Test Rechtsverwahrung',
            'TITRE': 'Test Rechtsverwahrung'
        }
    ],
    'REPRESENTANT': 'Mustermann und Söhne AG',
    'REPRESENTANT_ADRESSE_1': 'Juristenweg 99',
    'REPRESENTANT_ADRESSE_2': '3008 Bern',
    'REPRESENTANT_NOM_ADRESSE': 'Mustermann und Söhne AG, Juristenweg 99, 3008 Bern',
    'REPRESENTANT_TOUS': 'Mustermann und Söhne AG',
    'REPRESENTANT_TOUS_NOM_ADRESSE': 'Mustermann und Söhne AG, Juristenweg 99, 3008 Bern',
    'REQUERANT': 'ACME AG, Max Mustermann',
    'REQUERANTS_COMPENSATION_DES_CHARGES': [
        {
            'ADDRESS': 'Beispielstrasse 3, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 3, 4321 Beispieldorf',
            'NAME': 'Lastenausgleichsbegehren4you AG',
            'NOM': 'Lastenausgleichsbegehren4you AG'
        }
    ],
    'REQUERANTS_CONCLUSIONS': [
        {
            'ADDRESS': 'Beispielstrasse 1, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 1, 4321 Beispieldorf',
            'NAME': 'Heinz Einsprachenmann',
            'NOM': 'Heinz Einsprachenmann'
        },
        {
            'ADDRESS': 'Beispielstrasse 2, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 2, 4321 Beispieldorf',
            'NAME': 'Martha Rechstverwahrungsson',
            'NOM': 'Martha Rechstverwahrungsson'
        },
        {
            'ADDRESS': 'Beispielstrasse 3, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 3, 4321 Beispieldorf',
            'NAME': 'Lastenausgleichsbegehren4you AG',
            'NOM': 'Lastenausgleichsbegehren4you AG'
        }
    ],
    'REQUERANTS_RESERVE_DE_DROIT': [
        {
            'ADDRESS': 'Beispielstrasse 2, 4321 Beispieldorf',
            'ADRESSE': 'Beispielstrasse 2, 4321 Beispieldorf',
            'NAME': 'Martha Rechstverwahrungsson',
            'NOM': 'Martha Rechstverwahrungsson'
        }
    ],
    'REQUERANT_ADRESSE_1': 'Teststrasse 123',
    'REQUERANT_ADRESSE_2': '1234 Testhausen',
    'REQUERANT_NOM_ADRESSE': 'ACME AG, Max Mustermann, Teststrasse 123, 1234 Testhausen',
    'REQUERANT_TOUS': 'ACME AG, Max Mustermann',
    'REQUERANT_TOUS_NOM_ADRESSE': 'ACME AG, Max Mustermann, Teststrasse 123, 1234 Testhausen',
    'RESERVES_DE_DROIT': [
        {
            'ANLIEGEN': '''Test RV 1
Test RV 2''',
            'DATE_DOCUMENT': '01.11.2022',
            'DATE_RECEPTION': '02.11.2022',
            'DATUM_DOKUMENT': '01.11.2022',
            'DATUM_EINGANG': '02.11.2022',
            'DEMANDE_REQUETE': '''Test RV 1
Test RV 2''',
            'PREOCCUPATION': '''Test RV 1
Test RV 2''',
            'RECHTSBEGEHRENDE': 'Martha Rechstverwahrungsson',
            'REQUERANTS_CONCLUSIONS': 'Martha Rechstverwahrungsson',
            'TITEL': 'Test Rechtsverwahrung',
            'TITRE': 'Test Rechtsverwahrung'
        }
    ],
    'RESPONSABLE_AUTORITE_DIRECTRICE': 'Thomas Morgan',
    'RESPONSABLE_EMAIL': 'tammy30@example.net',
    'RESPONSABLE_NOM': 'Thomas Morgan',
    'RESPONSABLE_TELEPHONE': '',
    'ROOMS_WITH_MORE_THAN_50_PERSONS': [
    ],
    'ROOM_OCCUPANCY_ROOMS_MORE_THAN_50_PERSONS': '',
    'RRB': 'Ja',
    'RRB_DATE': '1. Januar 2022',
    'RRB_DATUM': '1. Januar 2022',
    'RRB_START': '1. Januar 2022',
    'SACHVERHALT': 'Sachverhalt Test',
    'SCHUTZZONE': 'S1',
    'SCHÜTZENSWERT': 'Ja',
    'SECTEUR_PROTECTION_EAUX': 'Aᵤ',
    'SITUATION': 'Sachverhalt Test',
    'SITZPLAETZE_AUSSEN': 20,
    'SITZPLAETZE_INNEN': 35,
    'SOLARANLAGEN': [
    ],
    'SOLAR_PANELS': [
    ],
    'SPRACHE': 'de',
    'STATUS': 'Pamela Horton',
    'STELLUNGNAHME': 'Stellungnahme 1',
    'STFV_CRITIAL_VALUE_EXCEEDED': '',
    'STFV_DATE_DU_RAPPORT_COURT': '',
    'STFV_KRITISCHER_WERT_UEBERSCHRITTEN': '',
    'STFV_KURZ_BERICHT_DATUM': '',
    'STFV_SHORT_REPORT_DATE': '',
    'STFV_VALEUR_CRITIQUE_DEPASSEE': '',
    'STICHWORTE': 'Andrew Berg MD, Alex Scott, Jacqueline Herrera, Kaitlyn Mendoza, Mary Mooney',
    'SURFACE_DE_PLANCHER': '',
    'SYSTEMES_DE_VENTILATION': [
    ],
    'TECHNISCHE_BRANDSCHUTZANLAGEN': [
    ],
    'TODAY': '30. August 2021',
    'UEBERBAUUNGSORDNUNG': 'Überbauung XY',
    'UVP_JA_NEIN': False,
    'VENTILATION_SYSTEMS': [
    ],
    'VERTRAG': 'Ja',
    'VERTRAG_DATUM': '1. Februar 2022',
    'VERTRETER': 'Mustermann und Söhne AG',
    'VERTRETER_ADDRESS_1': 'Juristenweg 99',
    'VERTRETER_ADDRESS_2': '3008 Bern',
    'VERTRETER_ADRESSE_1': 'Juristenweg 99',
    'VERTRETER_ADRESSE_2': '3008 Bern',
    'VERTRETER_NAME_ADDRESS': 'Mustermann und Söhne AG, Juristenweg 99, 3008 Bern',
    'VERTRETER_NAME_ADRESSE': 'Mustermann und Söhne AG, Juristenweg 99, 3008 Bern',
    'VERWALTUNGSKREIS': 'Emmental',
    'VOISINS_TOUS': [
        {
            'ADDRESS_1': 'Teststrasse 124',
            'ADDRESS_2': '1234 Testhausen',
            'ADRESSE_1': 'Teststrasse 124',
            'ADRESSE_2': '1234 Testhausen',
            'NAME': 'Karl Nachbarsson',
            'NOM': 'Karl Nachbarsson'
        }
    ],
    'WAERMETECHNISCHE_ANLAGEN': [
    ],
    'ZIRKULATION_ALLE': [
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '16.10.2004',
            'ERSTELLT': '30.08.2021',
            'FRIST': '16.10.2004',
            'NAME': 'Matthew Bowen',
            'NOM': 'Matthew Bowen',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '29.01.2021',
            'ERSTELLT': '30.08.2021',
            'FRIST': '29.01.2021',
            'NAME': 'Scott Clark',
            'NOM': 'Scott Clark',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '03.03.1970',
            'ERSTELLT': '30.08.2021',
            'FRIST': '03.03.1970',
            'NAME': 'John Ward',
            'NOM': 'John Ward',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '26.01.1999',
            'ERSTELLT': '30.08.2021',
            'FRIST': '26.01.1999',
            'NAME': 'Brittany Hill',
            'NOM': 'Brittany Hill',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '13.02.1982',
            'CREE': '30.08.2021',
            'DELAI': '17.06.1987',
            'ERSTELLT': '30.08.2021',
            'FRIST': '17.06.1987',
            'NAME': 'Dale Summers',
            'NOM': 'Dale Summers',
            'REPONDU': '13.02.1982'
        },
        {
            'BEANTWORTET': '15.08.1971',
            'CREE': '30.08.2021',
            'DELAI': '24.08.2008',
            'ERSTELLT': '30.08.2021',
            'FRIST': '24.08.2008',
            'NAME': 'Robert Cowan',
            'NOM': 'Robert Cowan',
            'REPONDU': '15.08.1971'
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '',
            'ERSTELLT': '30.08.2021',
            'FRIST': '',
            'NAME': 'Matthew Bowen',
            'NOM': 'Matthew Bowen',
            'REPONDU': ''
        }
    ],
    'ZIRKULATION_FACHSTELLEN': [
        {
            'BEANTWORTET': '13.02.1982',
            'CREE': '30.08.2021',
            'DELAI': '17.06.1987',
            'ERSTELLT': '30.08.2021',
            'FRIST': '17.06.1987',
            'NAME': 'Dale Summers',
            'NOM': 'Dale Summers',
            'REPONDU': '13.02.1982'
        },
        {
            'BEANTWORTET': '15.08.1971',
            'CREE': '30.08.2021',
            'DELAI': '24.08.2008',
            'ERSTELLT': '30.08.2021',
            'FRIST': '24.08.2008',
            'NAME': 'Robert Cowan',
            'NOM': 'Robert Cowan',
            'REPONDU': '15.08.1971'
        }
    ],
    'ZIRKULATION_GEMEINDEN': [
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '03.03.1970',
            'ERSTELLT': '30.08.2021',
            'FRIST': '03.03.1970',
            'NAME': 'John Ward',
            'NOM': 'John Ward',
            'REPONDU': ''
        },
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '26.01.1999',
            'ERSTELLT': '30.08.2021',
            'FRIST': '26.01.1999',
            'NAME': 'Brittany Hill',
            'NOM': 'Brittany Hill',
            'REPONDU': ''
        }
    ],
    'ZIRKULATION_RSTA': [
        {
            'BEANTWORTET': '',
            'CREE': '30.08.2021',
            'DELAI': '29.01.2021',
            'ERSTELLT': '30.08.2021',
            'FRIST': '29.01.2021',
            'NAME': 'Scott Clark',
            'NOM': 'Scott Clark',
            'REPONDU': ''
        }
    ],
    'ZIRKULATION_RUECKMELDUNGEN': [
        {
            'ANTWORT': 'Baubewilligungspflichtig',
            'DE': 'Dale Summers',
            'DISPOSITIONS_ACCESSOIRES': 'Nebenbestimmungen 5',
            'NEBENBESTIMMUNGEN': 'Nebenbestimmungen 5',
            'POINT_DE_VUE': 'Stellungnahme 5',
            'REPONSE': 'Baubewilligungspflichtig',
            'STELLUNGNAHME': 'Stellungnahme 5',
            'VON': 'Dale Summers'
        },
        {
            'ANTWORT': 'Nicht betroffen / nicht zuständig',
            'DE': 'Robert Cowan',
            'DISPOSITIONS_ACCESSOIRES': 'Nebenbestimmungen 6',
            'NEBENBESTIMMUNGEN': 'Nebenbestimmungen 6',
            'POINT_DE_VUE': 'Stellungnahme 6',
            'REPONSE': 'Nicht betroffen / nicht zuständig',
            'STELLUNGNAHME': 'Stellungnahme 6',
            'VON': 'Robert Cowan'
        }
    ],
    'ZONE_PROTEGEE': 'S1',
    'ZUSTAENDIG_EMAIL': 'tammy30@example.net',
    'ZUSTAENDIG_NAME': 'Thomas Morgan',
    'ZUSTAENDIG_PHONE': '',
    'ZUSTAENDIG_TELEFON': ''
}

snapshots['test_dms_placeholders_docs[be_dms_config] 1'] = {
    'ADDRESS': {
        'aliases': [
            {
                'de': 'ADRESSE',
                'fr': 'ADRESSE'
            }
        ],
        'description': {
            'de': 'Adresse des betroffenen Grundstückes',
            'fr': "Lieu-dit de l'immeuble concerné"
        },
        'nested_aliases': {
        }
    },
    'ADMINISTRATIVE_DISTRICT': {
        'aliases': [
            {
                'de': 'VERWALTUNGSKREIS',
                'fr': 'ARRONDISSEMENT_ADMINISTRATIF'
            }
        ],
        'description': {
            'de': 'Verwaltungskreis der Gemeinde',
            'fr': 'Arrondissement administratif'
        },
        'nested_aliases': {
        }
    },
    'ALCOHOL_SERVING': {
        'aliases': [
            {
                'de': 'ALKOHOLAUSSCHANK',
                'fr': 'BOISSONS_ALCOOLIQUES'
            }
        ],
        'description': {
            'de': 'Alkoholausschank mit/ohne',
            'fr': 'Débit de boissons alcooliques (avec/sans)'
        },
        'nested_aliases': {
        }
    },
    'ALLE_GEBAEUDEEIGENTUEMER': {
        'aliases': [
            {
                'de': 'ALLE_GEBAEUDEEIGENTUEMER',
                'fr': 'PROPRIETAIRE_IMMOB_TOUS'
            }
        ],
        'description': {
            'de': 'Namen aller Gebäudeeigentümer/innen',
            'fr': 'Noms de tous les propriétaires immobiliers/immobilières'
        },
        'nested_aliases': {
        }
    },
    'ALLE_GEBAEUDEEIGENTUEMER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'ALLE_GEBAEUDEEIGENTUEMER_NAME_ADRESSE',
                'fr': 'PROPRIETAIRE_IMMOB_TOUS_NOM_ADRESSE'
            }
        ],
        'description': {
            'de': 'Namen und Adressen aller Gebäudeeigentümer/innen',
            'fr': 'Noms et adresses de tous les propriétaires immobiliers/immobilières'
        },
        'nested_aliases': {
        }
    },
    'ALLE_GESUCHSTELLER': {
        'aliases': [
            {
                'de': 'ALLE_GESUCHSTELLER',
                'fr': 'REQUERANT_TOUS'
            }
        ],
        'description': {
            'de': 'Namen aller Gesuchsteller/innen',
            'fr': 'Noms de toutes les personnes requérantes'
        },
        'nested_aliases': {
        }
    },
    'ALLE_GESUCHSTELLER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'ALLE_GESUCHSTELLER_NAME_ADRESSE',
                'fr': 'REQUERANT_TOUS_NOM_ADRESSE'
            }
        ],
        'description': {
            'de': 'Namen und Adressen aller Gesuchsteller/innen',
            'fr': 'Noms et adresses de toutes les personnes requérantes'
        },
        'nested_aliases': {
        }
    },
    'ALLE_GRUNDEIGENTUEMER': {
        'aliases': [
            {
                'de': 'ALLE_GRUNDEIGENTUEMER',
                'fr': 'PROPRIETAIRE_FONC_TOUS'
            }
        ],
        'description': {
            'de': 'Namen aller Grundeigentümer/innen',
            'fr': 'Noms de tous les propriétaires fonciers/foncières'
        },
        'nested_aliases': {
        }
    },
    'ALLE_GRUNDEIGENTUEMER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'ALLE_GRUNDEIGENTUEMER_NAME_ADRESSE',
                'fr': 'PROPRIETAIRE_FONC_TOUS_NOM_ADRESSE'
            }
        ],
        'description': {
            'de': 'Namen und Adressen aller Grundeigentümer/innen',
            'fr': 'Noms et adresses de tous les propriétaires fonciers/foncières'
        },
        'nested_aliases': {
        }
    },
    'ALLE_PROJEKTVERFASSER': {
        'aliases': [
            {
                'de': 'ALLE_PROJEKTVERFASSER',
                'fr': 'AUTEUR_PROJET_TOUS'
            }
        ],
        'description': {
            'de': 'Namen aller Projektverfasser/innen',
            'fr': 'Noms de tous les auteur(e)s du projet'
        },
        'nested_aliases': {
        }
    },
    'ALLE_PROJEKTVERFASSER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'ALLE_PROJEKTVERFASSER_NAME_ADRESSE',
                'fr': 'AUTEUR_PROJET_TOUS_NOM_ADRESSE'
            }
        ],
        'description': {
            'de': 'Namen und Adressen aller Projektverfasser/innen',
            'fr': 'Noms et adresses de tous les auteur(e)s du projet'
        },
        'nested_aliases': {
        }
    },
    'ALLE_VERTRETER': {
        'aliases': [
            {
                'de': 'ALLE_VERTRETER',
                'fr': 'REPRESENTANT_TOUS'
            }
        ],
        'description': {
            'de': 'Namen aller Vertreter/innen',
            'fr': 'Noms de toutes les personnes resprésentantes'
        },
        'nested_aliases': {
        }
    },
    'ALLE_VERTRETER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'ALLE_VERTRETER_NAME_ADRESSE',
                'fr': 'REPRESENTANT_TOUS_NOM_ADRESSE'
            }
        ],
        'description': {
            'de': 'Namen und Adressen aller Vertreter/innen',
            'fr': 'Noms et adresses de toutes les personnes resprésentantes'
        },
        'nested_aliases': {
        }
    },
    'BASE_URL': {
        'aliases': [
            {
                'de': 'EBAU_URL',
                'fr': 'EBAU_URL'
            }
        ],
        'description': {
            'de': 'Die URL vom eBau-System',
            'fr': "L'adresse URL du système eBau"
        },
        'nested_aliases': {
        }
    },
    'BAUEINGABE_DATUM': {
        'aliases': [
            {
                'de': 'BAUEINGABE_DATUM',
                'fr': 'DEPOT_DEMANDE_DATE'
            }
        ],
        'description': {
            'de': 'Datum an dem das Dossier eingereicht wurde',
            'fr': 'Date du dépôt de la demande'
        },
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID',
                'fr': 'DECISION'
            }
        ],
        'description': {
            'de': 'Bauentscheid',
            'fr': 'Décision relative à la demande de permis de construire'
        },
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID_BAUABSCHLAG': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_BAUABSCHLAG',
                'fr': 'DECISION_REFUS'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID_BAUABSCHLAG_MIT_WHST': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_BAUABSCHLAG_MIT_WHST',
                'fr': 'DECISION_REFUS_AVEC_RET'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID_BAUABSCHLAG_OHNE_WHST': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_BAUABSCHLAG_OHNE_WHST',
                'fr': 'DECISION_REFUS_SANS_RET'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID_BAUBEWILLIGUNG': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_BAUBEWILLIGUNG',
                'fr': 'DECISION_PERMIS'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID_BAUBEWILLIGUNGSFREI': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_BAUBEWILLIGUNGSFREI',
                'fr': 'BAUENTSCHEID_BAUBEWILLIGUNGSFREI'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID_GENERELL': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_GENERELL',
                'fr': 'DECISION_GENERAL'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID_GESAMT': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_GESAMT',
                'fr': 'DECISION_GLOBALE'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID_KLEIN': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_KLEIN',
                'fr': 'DECISION_PETIT'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID_POSITIV': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_POSITIV',
                'fr': 'DECISION_POSITIVE'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID_POSITIV_TEILWEISE': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_POSITIV_TEILWEISE',
                'fr': 'DECISION_POSITIVE_PARTIEL'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID_PROJEKTAENDERUNG': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_PROJEKTAENDERUNG',
                'fr': 'DECISION_MODIF'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID_TEILBAUBEWILLIGUNG': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_TEILBAUBEWILLIGUNG',
                'fr': 'DECISION_PARTIEL'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID_TYPE': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_TYP',
                'fr': 'DECISION_CATEGORIE'
            }
        ],
        'description': {
            'de': 'Typ Bauentscheid',
            'fr': 'Type de décision relative à la demande de permis de construire'
        },
        'nested_aliases': {
        }
    },
    'BAUVORHABEN': {
        'aliases': [
            {
                'de': 'BAUVORHABEN',
                'fr': 'PROJET_CONSTR'
            }
        ],
        'description': {
            'de': 'Das Bauvohaben des Dossiers',
            'fr': 'Le projet de construction du dossier'
        },
        'nested_aliases': {
        }
    },
    'BESCHREIBUNG_BAUVORHABEN': {
        'aliases': [
            {
                'de': 'BESCHREIBUNG_BAUVORHABEN',
                'fr': 'PROJET_CONSTR_DESCR'
            }
        ],
        'description': {
            'de': 'Beschreibung des Bauvorhabens',
            'fr': 'Description du projet de construction'
        },
        'nested_aliases': {
        }
    },
    'BUILDING_DISTANCES': {
        'aliases': [
            {
                'de': 'GEBAEUDEABSTAENDE',
                'fr': 'DISTANCES_ENTRE_LES_BATIMENTS'
            }
        ],
        'description': {
            'de': 'Abstände zwischen benachbarten Gebäuden',
            'fr': 'Distances entre les bâtiments adjacents'
        },
        'nested_aliases': {
            'distance': [
                {
                    'de': 'ABSTAND_M',
                    'fr': 'DISTANCE'
                }
            ],
            'side': [
                {
                    'de': 'SEITE',
                    'fr': 'COTE'
                }
            ]
        }
    },
    'CONSERVABLE': {
        'aliases': [
            {
                'de': 'ERHALTENSWERT',
                'fr': 'CONSERVABLE'
            }
        ],
        'description': {
            'de': 'Einstufung «erhaltenswert»',
            'fr': 'Classement «digne de conservation»'
        },
        'nested_aliases': {
        }
    },
    'CONSTRUCTION_COSTS': {
        'aliases': [
            {
                'de': 'BAUKOSTEN',
                'fr': 'COUTS_DE_CONSTRUCTION'
            }
        ],
        'description': {
            'de': 'Baukosten',
            'fr': 'Coûts de construction'
        },
        'nested_aliases': {
        }
    },
    'CONSTRUCTION_GROUP': {
        'aliases': [
            {
                'de': 'BAUGRUPPE',
                'fr': 'ENSEMBLE_BÂTI'
            }
        ],
        'description': {
            'de': 'Zugehörigkeit zu einer Baugruppe',
            'fr': 'Appartenance à un ensemble bâti'
        },
        'nested_aliases': {
        }
    },
    'CONSTRUCTION_GROUP_DESIGNATION': {
        'aliases': [
            {
                'de': 'BAUGRUPPE_BEZEICHNUNG',
                'fr': 'ENSEMBLE_BÂTI_DÉNOMINATION'
            }
        ],
        'description': {
            'de': 'Bezeichnung der Baugruppe',
            'fr': "Désignation de l'ensemble bâti"
        },
        'nested_aliases': {
        }
    },
    'CONTRACT': {
        'aliases': [
            {
                'de': 'VERTRAG',
                'fr': 'CONTRAT'
            }
        ],
        'description': {
            'de': 'Unterschutzstellungsvertrag',
            'fr': 'Contrat de mise sous protection'
        },
        'nested_aliases': {
        }
    },
    'CONTRACT_START': {
        'aliases': [
            {
                'de': 'VERTRAG_DATUM',
                'fr': 'CONTRAT_DATE'
            }
        ],
        'description': {
            'de': 'Datum der Unterschutzstellung',
            'fr': 'Date du contrat de mise sous protection'
        },
        'nested_aliases': {
        }
    },
    'DECISION': {
        'aliases': [
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'DECISION_DATE': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_DATUM',
                'fr': 'DECISION_DATE'
            }
        ],
        'description': {
            'de': 'Datum des Bauentscheids',
            'fr': 'Date de la décision relative à la demande de permis de construire'
        },
        'nested_aliases': {
        }
    },
    'DECISION_TYPE': {
        'aliases': [
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'DESCRIPTION_MODIFICATION': {
        'aliases': [
            {
                'de': 'BESCHREIBUNG_PROJEKTAENDERUNG',
                'fr': 'DESCRIPTION_MODIFICATION'
            }
        ],
        'description': {
            'de': 'Projektänderung',
            'fr': 'Modification du projet'
        },
        'nested_aliases': {
        }
    },
    'DIMENSION_HEIGHT': {
        'aliases': [
            {
                'de': 'DIMENSIONEN_HOEHE',
                'fr': 'DIMENSION_HAUTEUR'
            }
        ],
        'description': {
            'de': 'Höhe',
            'fr': 'Hauteur'
        },
        'nested_aliases': {
        }
    },
    'DOSSIER_LINK': {
        'aliases': [
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'EBAU_NUMBER': {
        'aliases': [
            {
                'de': 'EBAU_NR',
                'fr': 'EBAU_NUMERO'
            }
        ],
        'description': {
            'de': 'Die eBau-Nummer des Dossiers',
            'fr': 'Numéro eBau du dossier'
        },
        'nested_aliases': {
        }
    },
    'EIGENE_GEBUEHREN': {
        'aliases': [
            {
                'de': 'EIGENE_GEBUEHREN',
                'fr': 'MES_EMOLUMENTS'
            }
        ],
        'description': {
            'de': 'Eigene Gebühren des Dossiers',
            'fr': 'Les frais propres du dossier'
        },
        'nested_aliases': {
            'BETRAG': [
                {
                    'de': 'BETRAG',
                    'fr': 'FORFAIT'
                }
            ],
            'POSITION': [
                {
                    'de': 'POSITION',
                    'fr': 'POSITION'
                }
            ]
        }
    },
    'EIGENE_GEBUEHREN_TOTAL': {
        'aliases': [
            {
                'de': 'EIGENE_GEBUEHREN_TOTAL',
                'fr': 'MES_EMOLUMENTS_TOTAL'
            }
        ],
        'description': {
            'de': 'Totalbetrag aller eigenen Gebühren des Dossiers',
            'fr': 'Montant total de tous les frais propres du dossier'
        },
        'nested_aliases': {
        }
    },
    'EMAIL': {
        'aliases': [
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'FACHSTELLEN_KANTONAL': {
        'aliases': [
            {
                'de': 'ZIRKULATION_ALLE',
                'fr': 'OFFICES_CANTONAUX'
            },
            {
                'de': 'FACHSTELLEN_KANTONAL',
                'fr': 'FACHSTELLEN_KANTONAL'
            }
        ],
        'description': {
            'de': 'In Dossier involvierte Stellen',
            'fr': 'Offices impliqués dans les dossiers'
        },
        'nested_aliases': {
            'BEANTWORTET': [
                {
                    'de': 'BEANTWORTET',
                    'fr': 'REPONDU'
                }
            ],
            'ERSTELLT': [
                {
                    'de': 'ERSTELLT',
                    'fr': 'CREE'
                }
            ],
            'FRIST': [
                {
                    'de': 'FRIST',
                    'fr': 'DELAI'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME',
                    'fr': 'NOM'
                }
            ]
        }
    },
    'FACHSTELLEN_KANTONAL_LIST': {
        'aliases': [
            {
                'de': 'FACHSTELLEN_KANTONAL_LISTE',
                'fr': 'OFFICES_CANTONAUX_LISTE'
            }
        ],
        'description': {
            'de': 'Namen aller involvierten kantonalen Fachstellen als Aufzählung',
            'fr': 'Noms de tous les offices cantonaux concernés sous forme de liste'
        },
        'nested_aliases': {
        }
    },
    'FIRE_PROTECTION_SYSTEMS': {
        'aliases': [
            {
                'de': 'TECHNISCHE_BRANDSCHUTZANLAGEN',
                'fr': 'INSTALLATIONS_TECH_LINCENDIE'
            }
        ],
        'description': {
            'de': 'Technische Brandschutzanlagen',
            'fr': "Installations techniques de protection contre l'incendie"
        },
        'nested_aliases': {
            'new_or_existing': [
                {
                    'de': 'NEU_BESTEHEND',
                    'fr': 'NOUVEAU_OU_EXISTANT'
                }
            ],
            'type': [
                {
                    'de': 'TYP',
                    'fr': 'TYPE'
                }
            ]
        }
    },
    'FLOOR_AREA': {
        'aliases': [
            {
                'de': 'GESCHOSSFLAECHE',
                'fr': 'SURFACE_DE_PLANCHER'
            }
        ],
        'description': {
            'de': 'Geschossfläche',
            'fr': 'Surface de plancher'
        },
        'nested_aliases': {
        }
    },
    'FORM_NAME': {
        'aliases': [
            {
                'de': 'DOSSIER_TYP',
                'fr': 'DOSSIER_TYPE'
            }
        ],
        'description': {
            'de': 'Typ des Dossiers',
            'fr': 'Type du dossier'
        },
        'nested_aliases': {
        }
    },
    'GEBAEUDEEIGENTUEMER': {
        'aliases': [
            {
                'de': 'GEBAEUDEEIGENTUEMER',
                'fr': 'PROPRIETAIRE_IMMOB'
            }
        ],
        'description': {
            'de': 'Name des/r Gebäudeeigentümer/in',
            'fr': 'Nom propriétaire immobilier/immobilière'
        },
        'nested_aliases': {
        }
    },
    'GEBAEUDEEIGENTUEMER_ADDRESS_1': {
        'aliases': [
            {
                'de': 'GEBAEUDEEIGENTUEMER_ADRESSE_1',
                'fr': 'PROPRIETAIRE_IMMOB_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 des/r Gebäudeeigentümer/in',
            'fr': "Ligne d'adresse 1 propriétaire immobilier/immobilière"
        },
        'nested_aliases': {
        }
    },
    'GEBAEUDEEIGENTUEMER_ADDRESS_2': {
        'aliases': [
            {
                'de': 'GEBAEUDEEIGENTUEMER_ADRESSE_2',
                'fr': 'PROPRIETAIRE_IMMOB_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 des/r Gebäudeeigentümer/in',
            'fr': "Ligne d'adresse 2 propriétaire immobilier/immobilière"
        },
        'nested_aliases': {
        }
    },
    'GEBAEUDEEIGENTUEMER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'GEBAEUDEEIGENTUEMER_NAME_ADRESSE',
                'fr': 'PROPRIETAIRE_IMMOB_NOM_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse des/r Gebäudeeigentümer/in',
            'fr': 'Nom et adresse propriétaire immobilier/immobilière'
        },
        'nested_aliases': {
        }
    },
    'GEBUEHREN': {
        'aliases': [
            {
                'de': 'GEBUEHREN',
                'fr': 'EMOLUMENTS'
            }
        ],
        'description': {
            'de': 'Gebühren des Dossiers',
            'fr': 'Les frais officiels de procédure'
        },
        'nested_aliases': {
            'BETRAG': [
                {
                    'de': 'BETRAG',
                    'fr': 'FORFAIT'
                }
            ],
            'POSITION': [
                {
                    'de': 'POSITION',
                    'fr': 'POSITION'
                }
            ]
        }
    },
    'GEBUEHREN_TOTAL': {
        'aliases': [
            {
                'de': 'GEBUEHREN_TOTAL',
                'fr': 'EMOLUMENTS_TOTAL'
            }
        ],
        'description': {
            'de': 'Totalbetrag aller Gebühren des Dossiers',
            'fr': 'Montant total de tous les frais de procédure'
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_ADRESSE_1': {
        'aliases': [
            {
                'de': 'GEMEINDE_ADRESSE_1',
                'fr': 'COMMUNE_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 der Gemeinde',
            'fr': "Ligne d'adresse 1 de la commune"
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_ADRESSE_2': {
        'aliases': [
            {
                'de': 'GEMEINDE_ADRESSE_2',
                'fr': 'COMMUNE_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 der Gemeinde',
            'fr': "Ligne d'adresse 2 de la commune"
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_EMAIL': {
        'aliases': [
            {
                'de': 'GEMEINDE_EMAIL',
                'fr': 'COMMUNE_EMAIL'
            }
        ],
        'description': {
            'de': 'Email-Adresse der Gemeinde',
            'fr': 'Adresse électronique de la commune'
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_NAME_ADRESSE': {
        'aliases': [
            {
                'de': 'GEMEINDE_NAME_ADRESSE',
                'fr': 'COMMUNE_NOM_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse der Gemeinde',
            'fr': 'Nom et adresse de la commune'
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_ORT': {
        'aliases': [
            {
                'de': 'GEMEINDE_ORT',
                'fr': 'COMMUNE_LIEU'
            }
        ],
        'description': {
            'de': 'Ort der Gemeinde',
            'fr': 'Lieu de la commune'
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_TELEFON': {
        'aliases': [
            {
                'de': 'GEMEINDE_TELEFON',
                'fr': 'COMMUNE_TELEPHONE'
            }
        ],
        'description': {
            'de': 'Telefonnummer der Gemeinde',
            'fr': 'Numéro de téléphone de la commune'
        },
        'nested_aliases': {
        }
    },
    'GESUCHSTELLER': {
        'aliases': [
            {
                'de': 'GESUCHSTELLER',
                'fr': 'REQUERANT'
            }
        ],
        'description': {
            'de': 'Name des/r Gesuchsteller/in',
            'fr': 'Nom requérant/e'
        },
        'nested_aliases': {
        }
    },
    'GESUCHSTELLER_ADDRESS_1': {
        'aliases': [
            {
                'de': 'GESUCHSTELLER_ADRESSE_1',
                'fr': 'REQUERANT_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 des/r ersten Gesuchsteller/in',
            'fr': "Ligne d'adresse 1 du premier requérant/e"
        },
        'nested_aliases': {
        }
    },
    'GESUCHSTELLER_ADDRESS_2': {
        'aliases': [
            {
                'de': 'GESUCHSTELLER_ADRESSE_2',
                'fr': 'REQUERANT_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 des/r ersten Gesuchsteller/in',
            'fr': "Ligne d'adresse 2 du premier requérant/e"
        },
        'nested_aliases': {
        }
    },
    'GESUCHSTELLER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'GESUCHSTELLER_NAME_ADRESSE',
                'fr': 'REQUERANT_NOM_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse des/r Gesuchsteller/in',
            'fr': 'Nom et adresse requérant/e'
        },
        'nested_aliases': {
        }
    },
    'GEWAESSERSCHUTZBEREICH': {
        'aliases': [
            {
                'de': 'GEWAESSERSCHUTZBEREICH',
                'fr': 'SECTEUR_PROTECTION_EAUX'
            }
        ],
        'description': {
            'de': 'Gewässerschutzbereich',
            'fr': 'Secteur de protection des eaux'
        },
        'nested_aliases': {
        }
    },
    'GRUNDEIGENTUEMER': {
        'aliases': [
            {
                'de': 'GRUNDEIGENTUEMER',
                'fr': 'PROPRIETAIRE_FONC'
            }
        ],
        'description': {
            'de': 'Name des/r Grundeigentümer/in',
            'fr': 'Nom propriétaire foncier/foncière'
        },
        'nested_aliases': {
        }
    },
    'GRUNDEIGENTUEMER_ADDRESS_1': {
        'aliases': [
            {
                'de': 'GRUNDEIGENTUEMER_ADRESSE_1',
                'fr': 'PROPRIETAIRE_FONC_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 des/r ersten Grundeigentümer/in',
            'fr': "Ligne d'adresse 1 propriétaire du premier foncier/foncière"
        },
        'nested_aliases': {
        }
    },
    'GRUNDEIGENTUEMER_ADDRESS_2': {
        'aliases': [
            {
                'de': 'GRUNDEIGENTUEMER_ADRESSE_2',
                'fr': 'PROPRIETAIRE_FONC_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 des/r ersten Grundeigentümer/in',
            'fr': "Ligne d'adresse 2 propriétaire du premier foncier/foncière"
        },
        'nested_aliases': {
        }
    },
    'GRUNDEIGENTUEMER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'GRUNDEIGENTUEMER_NAME_ADRESSE',
                'fr': 'PROPRIETAIRE_FONC_NOM_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse des/r Grundeigentümer/in',
            'fr': 'Nom et adresse propriétaire foncier/foncière'
        },
        'nested_aliases': {
        }
    },
    'HAZARDOUS_SUBSTANCES': {
        'aliases': [
            {
                'de': 'GEFAEHRLICHE_STOFFE',
                'fr': 'MATIERES_DANGEREUSES'
            }
        ],
        'description': {
            'de': 'Gefährliche Stoffe',
            'fr': 'Matières dangereuses'
        },
        'nested_aliases': {
            'amount': [
                {
                    'de': 'BETRAG',
                    'fr': 'FORFAIT'
                }
            ],
            'material': [
                {
                    'de': 'MATERIAL',
                    'fr': 'MATERIAU'
                }
            ],
            'material_group': [
                {
                    'de': 'STOFFGRUPPE',
                    'fr': 'GROUPE_DE_MATIERES'
                }
            ]
        }
    },
    'HEATING_SYSTEMS': {
        'aliases': [
            {
                'de': 'WAERMETECHNISCHE_ANLAGEN',
                'fr': 'INSTALLATIONS_AERAULIQUES'
            }
        ],
        'description': {
            'de': 'Wärmetechnische Anlagen',
            'fr': 'Installations aerauliques'
        },
        'nested_aliases': {
            'combusitble_storage': [
                {
                    'de': 'BRENNSTOFFLAGERUNG',
                    'fr': 'STOCKAGE_COMBUSTIBLE'
                }
            ],
            'new_or_existing': [
                {
                    'de': 'NEU_BESTEHEND',
                    'fr': 'NOUVEAU_OU_EXISTANT'
                }
            ],
            'power': [
                {
                    'de': 'LEISTUNG',
                    'fr': 'PUISSANCE'
                }
            ],
            'storage_amount': [
                {
                    'de': 'LAGERMENGE',
                    'fr': 'QUANTITE_STOCKEE'
                }
            ],
            'type': [
                {
                    'de': 'TYP',
                    'fr': 'TYPE'
                }
            ]
        }
    },
    'INFORMATION_OF_NEIGHBORS_LINK': {
        'aliases': [
            {
                'de': 'NACHBARSCHAFTSORIENTIERUNG_LINK',
                'fr': 'COMMUNICATION_AUX_VOISINS_LIEN'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'INFORMATION_OF_NEIGHBORS_QR_CODE': {
        'aliases': [
            {
                'de': 'NACHBARSCHAFTSORIENTIERUNG_QR_CODE',
                'fr': 'COMMUNICATION_AUX_VOISINS_CODE_QR'
            }
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'INSTANCE_ID': {
        'aliases': [
            {
                'de': 'DOSSIER_NR',
                'fr': 'DOSSIER_NUMERO'
            }
        ],
        'description': {
            'de': 'Die Nummer des Dossiers',
            'fr': 'Numéro du dossier'
        },
        'nested_aliases': {
        }
    },
    'INTERIOR_SEATING': {
        'aliases': [
            {
                'de': 'SITZPLAETZE_INNEN',
                'fr': 'PLACES_ASSISES_INT'
            }
        ],
        'description': {
            'de': 'Summe aller Sitzplätze innen',
            'fr': "Total places assises à l'intérieur"
        },
        'nested_aliases': {
        }
    },
    'INVENTAR': {
        'aliases': [
            {
                'de': 'INVENTAR',
                'fr': 'RECENSEMENT'
            }
        ],
        'description': {
            'de': 'Bauinventar',
            'fr': 'Recensement (architectural)'
        },
        'nested_aliases': {
        }
    },
    'JURISTIC_NAME': {
        'aliases': [
            {
                'de': 'JURISTISCHER_NAME',
                'fr': 'NOM_LEGAL'
            }
        ],
        'description': {
            'de': 'Juristischer Name des/r Gesuchsteller/in',
            'fr': 'Nom légal requérant/e'
        },
        'nested_aliases': {
        }
    },
    'KOORDINATEN': {
        'aliases': [
            {
                'de': 'KOORDINATEN',
                'fr': 'COORDONEE'
            }
        ],
        'description': {
            'de': 'Lagekoordinaten der Parzelle(n)',
            'fr': 'Coordonnées planimétriques de/des parcelle(s) selectionnée(s)'
        },
        'nested_aliases': {
        }
    },
    'K_OBJECT': {
        'aliases': [
            {
                'de': 'K_OBJEKT',
                'fr': 'OBJECT_C'
            }
        ],
        'description': {
            'de': 'K-Objekt',
            'fr': 'Objet-C'
        },
        'nested_aliases': {
        }
    },
    'LANGUAGE': {
        'aliases': [
            {
                'de': 'SPRACHE',
                'fr': 'LANGUE'
            }
        ],
        'description': {
            'de': 'Die momentan ausgewählte Systemsprache',
            'fr': 'La langue du système actuellement sélectionnée'
        },
        'nested_aliases': {
        }
    },
    'LASTENAUSGLEICHSBEGEHREN': {
        'aliases': [
            {
                'de': 'LASTENAUSGLEICHSBEGEHREN',
                'fr': 'DEMANDES_EN_COMPENSATION_DES_CHARGES'
            }
        ],
        'description': {
            'de': 'Alle Rechtsbegehren vom Typ "Lastenausgleichsbegehren"',
            'fr': 'Toutes les conclusions de type "Demande en compensation des charges"'
        },
        'nested_aliases': {
            'ANLIEGEN': [
                {
                    'de': 'ANLIEGEN',
                    'fr': 'DEMANDE_REQUETE'
                },
                {
                    'de': 'ANLIEGEN',
                    'fr': 'PREOCCUPATION'
                }
            ],
            'DATUM_DOKUMENT': [
                {
                    'de': 'DATUM_DOKUMENT',
                    'fr': 'DATE_DOCUMENT'
                }
            ],
            'DATUM_EINGANG': [
                {
                    'de': 'DATUM_EINGANG',
                    'fr': 'DATE_RECEPTION'
                }
            ],
            'RECHTSBEGEHRENDE': [
                {
                    'de': 'RECHTSBEGEHRENDE',
                    'fr': 'REQUERANTS_CONCLUSIONS'
                }
            ],
            'TITEL': [
                {
                    'de': 'TITEL',
                    'fr': 'TITRE'
                }
            ]
        }
    },
    'LEGAL_CLAIMANTS': {
        'aliases': [
            {
                'de': 'RECHTSBEGEHRENDE',
                'fr': 'REQUERANTS_CONCLUSIONS'
            }
        ],
        'description': {
            'de': 'Alle Rechtsbegehrende mit Adresse',
            'fr': 'Tous les requérants conclusions avec adresse'
        },
        'nested_aliases': {
            'ADDRESS': [
                {
                    'de': 'ADRESSE',
                    'fr': 'ADRESSE'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME',
                    'fr': 'NOM'
                }
            ]
        }
    },
    'LEGAL_CUSTODIANS': {
        'aliases': [
            {
                'de': 'RECHTSVERWAHRENDE',
                'fr': 'REQUERANTS_RESERVE_DE_DROIT'
            }
        ],
        'description': {
            'de': 'Rechtsverwahrende mit Adresse',
            'fr': 'Requérants réserve de droit avec adresse'
        },
        'nested_aliases': {
            'ADDRESS': [
                {
                    'de': 'ADRESSE',
                    'fr': 'ADRESSE'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME',
                    'fr': 'NOM'
                }
            ]
        }
    },
    'LEITBEHOERDE_ADDRESS_1': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_ADRESSE_1',
                'fr': 'AUTORITE_DIRECTRICE_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 der zuständigen Leitbehörde',
            'fr': "Ligne d'adresse 1 de l'autorité directrice compétente"
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_ADDRESS_2': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_ADRESSE_2',
                'fr': 'AUTORITE_DIRECTRICE_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 der zuständigen Leitbehörde',
            'fr': "Ligne d'adresse 2 de l'autorité directrice compétente"
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_CITY': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_STADT',
                'fr': 'AUTORITE_DIRECTRICE_LIEU'
            }
        ],
        'description': {
            'de': 'Ort der zuständigen Leitbehörde',
            'fr': "Lieu de l'autorité directrice compétente"
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_EMAIL': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_EMAIL',
                'fr': 'AUTORITE_DIRECTRICE_EMAIL'
            }
        ],
        'description': {
            'de': 'Email-Adresse der zuständigen Leitbehörde',
            'fr': "Adresse électronique de l'autorité directrice compétente"
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_NAME': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_NAME',
                'fr': 'AUTORITE_DIRECTRICE_NOM'
            }
        ],
        'description': {
            'de': 'Name der zuständigen Leitbehörde',
            'fr': "Nom de l'autorité directrice compétente"
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_NAME_KURZ': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_NAME_KURZ',
                'fr': 'AUTORITE_DIRECTRICE_NOM_ABR'
            }
        ],
        'description': {
            'de': 'Abgekürzter Name der zuständigen Leitbehörde',
            'fr': "Nom abrégé de l'autorité directrice compétente"
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_PHONE': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_TELEFON',
                'fr': 'AUTORITE_DIRECTRICE_TELEPHONE'
            }
        ],
        'description': {
            'de': 'Telefonnummer der zuständigen Leitbehörde',
            'fr': "Numéro de téléphone de l'autorité directrice compétente"
        },
        'nested_aliases': {
        }
    },
    'LEITPERSON': {
        'aliases': [
            {
                'de': 'LEITPERSON',
                'fr': 'RESPONSABLE_AUTORITE_DIRECTRICE'
            }
        ],
        'description': {
            'de': 'Zuständige Person der zuständigen Leitbehörde',
            'fr': "Personne responsable de l'autorité directrice compétente"
        },
        'nested_aliases': {
        }
    },
    'LIFTS': {
        'aliases': [
            {
                'de': 'AUFZUGSANLAGEN',
                'fr': 'ASCENSEURS'
            }
        ],
        'description': {
            'de': 'Aufzugsanlagen',
            'fr': 'Ascenseurs'
        },
        'nested_aliases': {
            'new_or_existing': [
                {
                    'de': 'NEU_BESTEHEND',
                    'fr': 'NOUVEAU_OU_EXISTANT'
                }
            ],
            'system_type': [
                {
                    'de': 'ANLAGENTYP',
                    'fr': 'TYPE_INSTALLATION'
                }
            ]
        }
    },
    'LOAD_COMPENSATION_REQUESTING': {
        'aliases': [
            {
                'de': 'LASTENAUSGLEICHSBEGEHRENDE',
                'fr': 'REQUERANTS_COMPENSATION_DES_CHARGES'
            }
        ],
        'description': {
            'de': 'Lastenausgleichsbegehrende mit Adresse',
            'fr': 'Requérants compensation des charges avec adresse'
        },
        'nested_aliases': {
            'ADDRESS': [
                {
                    'de': 'ADRESSE',
                    'fr': 'ADRESSE'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME',
                    'fr': 'NOM'
                }
            ]
        }
    },
    'MEINE_ORGANISATION_ADRESSE_1': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_ADRESSE_1',
                'fr': 'MON_ORGANISATION_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 der momentan ausgewählten Organisation',
            'fr': "Ligne d'adresse 1 de l'organisation actuellement sélectionnée"
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_ADRESSE_2': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_ADRESSE_2',
                'fr': 'MON_ORGANISATION_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 der momentan ausgewählten Organisation',
            'fr': "Ligne d'adresse 2 de l'organisation actuellement sélectionnée"
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_EMAIL': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_EMAIL',
                'fr': 'MON_ORGANISATION_EMAIL'
            }
        ],
        'description': {
            'de': 'Email-Adresse der momentan ausgewählten Organisation',
            'fr': "Adresse électronique de l'organisation actuellement sélectionnée"
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_NAME': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_NAME',
                'fr': 'MON_ORGANISATION_NOM'
            }
        ],
        'description': {
            'de': 'Name der momentan ausgewählten Organisation',
            'fr': "Nom de l'organisation actuellement sélectionnée"
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_NAME_ADRESSE': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_NAME_ADRESSE',
                'fr': 'MON_ORGANISATION_NOM_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse der momentan ausgewählten Organisation',
            'fr': "Nom et adresse de l'organisation actuellement sélectionnée"
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_NAME_KURZ': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_NAME_KURZ',
                'fr': 'MON_ORGANISATION_NOM_ABR'
            }
        ],
        'description': {
            'de': 'Abgekürzter Name der momentan ausgewählten Organisation',
            'fr': "Nom abrégé de l'organisation actuellement sélectionnée"
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_ORT': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_ORT',
                'fr': 'MON_ORGANISATION_LIEU'
            }
        ],
        'description': {
            'de': 'Ort der momentan ausgewählten Organisation',
            'fr': "Lieu de l'organisation actuellement sélectionnée"
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_TELEFON': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_TELEFON',
                'fr': 'MON_ORGANISATION_TELEPHONE'
            }
        ],
        'description': {
            'de': 'Telefonnummer der momentan ausgewählten Organisation',
            'fr': "Numéro de téléphone de l'organisation actuellement sélectionnée"
        },
        'nested_aliases': {
        }
    },
    'MODIFICATION_DATE': {
        'aliases': [
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'MODIFICATION_TIME': {
        'aliases': [
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'MUNICIPALITY': {
        'aliases': [
            {
                'de': 'GEMEINDE',
                'fr': 'COMMUNE'
            }
        ],
        'description': {
            'de': 'Die ausgewählte Gemeinde des/der Gesuchsteller/in',
            'fr': 'Commune sélectionnée par la personne requérante'
        },
        'nested_aliases': {
        }
    },
    'MUNICIPALITY_ADDRESS': {
        'aliases': [
            {
                'de': 'GEMEINDE_ADRESSE',
                'fr': 'COMMUNE_ADRESSE'
            }
        ],
        'description': {
            'de': 'Die Adresse der ausgewählten Gemeinde des/der Gesuchsteller/in',
            'fr': 'Adresse de la commune sélectionnée par la personne requérante'
        },
        'nested_aliases': {
        }
    },
    'NAME': {
        'aliases': [
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'NEBENBESTIMMUNGEN': {
        'aliases': [
            {
                'de': 'EIGENE_NEBENBESTIMMUNGEN',
                'fr': 'DISPOSITIONS_ANNEXES'
            },
            {
                'de': 'NEBENBESTIMMUNGEN',
                'fr': 'DISPOSITIONS_ACCESSOIRES'
            }
        ],
        'description': {
            'de': 'Eigene Nebenbestimmungen',
            'fr': 'Dispositions annexes propres'
        },
        'nested_aliases': {
        }
    },
    'NEBENBESTIMMUNGEN_MAPPED': {
        'aliases': [
            {
                'de': 'NEBENBESTIMMUNGEN_MAPPED',
                'fr': 'NEBENBESTIMMUNGEN_MAPPED'
            }
        ],
        'description': None,
        'nested_aliases': {
            'FACHSTELLE': [
                {
                    'de': 'FACHSTELLE',
                    'fr': 'SERVICE'
                }
            ],
            'TEXT': [
                {
                    'de': 'TEXT',
                    'fr': 'TEXTE'
                }
            ]
        }
    },
    'NEIGHBORS': {
        'aliases': [
            {
                'de': 'ALLE_NACHBARN',
                'fr': 'VOISINS_TOUS'
            }
        ],
        'description': None,
        'nested_aliases': {
            'ADDRESS_1': [
                {
                    'de': 'ADRESSE_1',
                    'fr': 'ADRESSE_1'
                }
            ],
            'ADDRESS_2': [
                {
                    'de': 'ADRESSE_2',
                    'fr': 'ADRESSE_2'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME',
                    'fr': 'NOM'
                }
            ]
        }
    },
    'NUMBER_OF_ACCOMODATED_PERSONS': {
        'aliases': [
            {
                'de': 'ANZAHL_BEHERBERGTE_PERSONEN',
                'fr': 'NOMBRE_DE_PERSONNES_ACCOMPAGNEES'
            }
        ],
        'description': {
            'de': 'Anzahl beherbergte Personen',
            'fr': 'Nombre de personnes hébergées'
        },
        'nested_aliases': {
        }
    },
    'NUTZUNG': {
        'aliases': [
            {
                'de': 'NUTZUNG',
                'fr': 'AFFECTATION'
            }
        ],
        'description': {
            'de': 'Art der geplanten Nutzung des Grundstückes',
            'fr': 'Affectation visée par le projet de construction'
        },
        'nested_aliases': {
        }
    },
    'NUTZUNGSZONE': {
        'aliases': [
            {
                'de': 'NUTZUNGSZONE',
                'fr': 'AFFECTATION_ZONE'
            }
        ],
        'description': {
            'de': 'Momentane Nutzungszone des Grundstückes',
            'fr': "Zone d'affectation actuelle de l'immeuble"
        },
        'nested_aliases': {
        }
    },
    'OBJECTIONS': {
        'aliases': [
            {
                'de': 'EINSPRACHEN',
                'fr': 'OPPOSITIONS'
            }
        ],
        'description': {
            'de': 'Alle Rechtsbegehren vom Typ "Einsprache"',
            'fr': 'Toutes les conclusions de type "Opposition"'
        },
        'nested_aliases': {
            'DATUM_DOKUMENT': [
                {
                    'de': 'DATUM_DOKUMENT',
                    'fr': 'DATE_DOCUMENT'
                }
            ],
            'DATUM_EINGANG': [
                {
                    'de': 'DATUM_EINGANG',
                    'fr': 'DATE_RECEPTION'
                }
            ],
            'RECHTSBEGEHRENDE': [
                {
                    'de': 'RECHTSBEGEHRENDE',
                    'fr': 'REQUERANTS_CONCLUSIONS'
                }
            ],
            'RUEGEPUNKTE': [
                {
                    'de': 'RUEGEPUNKTE',
                    'fr': 'GRIEFS'
                }
            ],
            'TITEL': [
                {
                    'de': 'TITEL',
                    'fr': 'TITRE'
                }
            ]
        }
    },
    'OPPOSING': {
        'aliases': [
            {
                'de': 'EINSPRECHENDE',
                'fr': 'OPPOSANTS'
            }
        ],
        'description': {
            'de': 'Einsprechende mit Adresse',
            'fr': 'Opposants avec adresse'
        },
        'nested_aliases': {
            'ADDRESS': [
                {
                    'de': 'ADRESSE',
                    'fr': 'ADRESSE'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME',
                    'fr': 'NOM'
                }
            ]
        }
    },
    'OUTSIDE_SEATING': {
        'aliases': [
            {
                'de': 'SITZPLAETZE_AUSSEN',
                'fr': 'PLACES_ASSISES_EXT'
            }
        ],
        'description': {
            'de': 'Alle Sitzplätze aussen',
            'fr': "Total Places assises à l'extérieur"
        },
        'nested_aliases': {
        }
    },
    'PARZELLE': {
        'aliases': [
            {
                'de': 'PARZELLE',
                'fr': 'PARCELLE'
            }
        ],
        'description': {
            'de': 'Die ausgewählte Parzelle(n) des/der Gesuchsteller/in',
            'fr': 'Parcelle(s) sélectionnée(s) par la personne requérante'
        },
        'nested_aliases': {
        }
    },
    'PROJEKTVERFASSER': {
        'aliases': [
            {
                'de': 'PROJEKTVERFASSER',
                'fr': 'AUTEUR_PROJET'
            }
        ],
        'description': {
            'de': 'Name des/r Projektverfasser/in',
            'fr': "Nom de l'auteur(e) du projet"
        },
        'nested_aliases': {
        }
    },
    'PROJEKTVERFASSER_ADDRESS_1': {
        'aliases': [
            {
                'de': 'PROJEKTVERFASSER_ADRESSE_1',
                'fr': 'AUTEUR_PROJET_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 des/r ersten Projektverfasser/in',
            'fr': "Ligne d'adresse 1 du premier l'auteur(e) du projet"
        },
        'nested_aliases': {
        }
    },
    'PROJEKTVERFASSER_ADDRESS_2': {
        'aliases': [
            {
                'de': 'PROJEKTVERFASSER_ADRESSE_2',
                'fr': 'AUTEUR_PROJET_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 des/r ersten Projektverfasser/in',
            'fr': "Ligne d'adresse 2 du premier l'auteur(e) du projet"
        },
        'nested_aliases': {
        }
    },
    'PROJEKTVERFASSER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'PROJEKTVERFASSER_NAME_ADRESSE',
                'fr': 'AUTEUR_PROJET_NOM_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse des/r Projektverfasser/in',
            'fr': "Nom et adresse de l'auteur(e) du projet"
        },
        'nested_aliases': {
        }
    },
    'PROTECTED': {
        'aliases': [
            {
                'de': 'SCHÜTZENSWERT',
                'fr': 'PROTÉGÉ'
            }
        ],
        'description': {
            'de': 'Einstufung «schützenswert»',
            'fr': 'Classement «digne de protection»'
        },
        'nested_aliases': {
        }
    },
    'PROTECTION_AREA': {
        'aliases': [
            {
                'de': 'SCHUTZZONE',
                'fr': 'ZONE_PROTEGEE'
            }
        ],
        'description': {
            'de': 'Grundwasserschutzzonen / -areale',
            'fr': 'Zone/périmètre de protection des eaux souterraines'
        },
        'nested_aliases': {
        }
    },
    'PUBLIC': {
        'aliases': [
            {
                'de': 'OEFFENTLICHKEIT',
                'fr': 'OUVERTURE_PUBLIC'
            }
        ],
        'description': {
            'de': 'Gastgewerbe Öffentlichkeit',
            'fr': 'Hôtellerie et restauration - Ouverture au public'
        },
        'nested_aliases': {
        }
    },
    'PUBLIKATION_1_ANZEIGER': {
        'aliases': [
            {
                'de': 'PUBLIKATION_1_ANZEIGER',
                'fr': 'PUBLICATION_1_FEUILLE_AVIS'
            }
        ],
        'description': {
            'de': 'Datum der ersten Publikation im Anzeiger',
            'fr': "Date de la première publication dans la feuille d'avis"
        },
        'nested_aliases': {
        }
    },
    'PUBLIKATION_2_ANZEIGER': {
        'aliases': [
            {
                'de': 'PUBLIKATION_2_ANZEIGER',
                'fr': 'PUBLICATION_2_FEUILLE_AVIS'
            }
        ],
        'description': {
            'de': 'Datum der zweiten Publikation im Anzeiger',
            'fr': "Date de la deuxième publication dans la feuille d'avis"
        },
        'nested_aliases': {
        }
    },
    'PUBLIKATION_AMTSBLATT': {
        'aliases': [
            {
                'de': 'PUBLIKATION_AMTSBLATT',
                'fr': 'PUBLICATION_FEUILLE_OFFICIELLE'
            }
        ],
        'description': {
            'de': 'Datum der Publikation im Amtsblatt',
            'fr': 'Date de la publication dans la feuille offcielle'
        },
        'nested_aliases': {
        }
    },
    'PUBLIKATION_ANZEIGER_NAME': {
        'aliases': [
            {
                'de': 'PUBLIKATION_ANZEIGER_NAME',
                'fr': 'PUBLICATION_FEUILLE_AVIS_NOM'
            }
        ],
        'description': {
            'de': 'Name des Anzeigers',
            'fr': "Nom de la feuille d'avis"
        },
        'nested_aliases': {
        }
    },
    'PUBLIKATION_ENDE': {
        'aliases': [
            {
                'de': 'PUBLIKATION_ENDE',
                'fr': 'PUBLICATION_EXPIRATION'
            }
        ],
        'description': {
            'de': 'Enddatum der Publikation des Dossiers',
            'fr': "Date d'expiration de la publication du dossier"
        },
        'nested_aliases': {
        }
    },
    'PUBLIKATION_LINK': {
        'aliases': [
            {
                'de': 'PUBLIKATION_LINK',
                'fr': 'LIEN_PUBLICATION'
            }
        ],
        'description': {
            'de': 'Link zur öffentlichen Auflage',
            'fr': "Lien pour la mise à l'enquête publique"
        },
        'nested_aliases': {
        }
    },
    'PUBLIKATION_START': {
        'aliases': [
            {
                'de': 'PUBLIKATION_START',
                'fr': 'PUBLICATION_DEBUT'
            }
        ],
        'description': {
            'de': 'Startdatum der Publikation des Dossiers',
            'fr': 'Date de début de la publication du dossier'
        },
        'nested_aliases': {
        }
    },
    'PUBLIKATION_TEXT': {
        'aliases': [
            {
                'de': 'PUBLIKATION_TEXT',
                'fr': 'PUBLICATION_TEXTE'
            }
        ],
        'description': {
            'de': 'Publikationstext des Dossiers',
            'fr': 'Texte de la publication du dossier'
        },
        'nested_aliases': {
        }
    },
    'QS_RESPONSIBLE': {
        'aliases': [
            {
                'de': 'QS_VERANTWORTLICHER',
                'fr': 'QS_RESPONSIBLE'
            }
        ],
        'description': {
            'de': 'Angaben des QS Verantwortlichen',
            'fr': 'Nom de la personne responsable du QS'
        },
        'nested_aliases': {
        }
    },
    'RECHTSVERWAHRUNGEN': {
        'aliases': [
            {
                'de': 'RECHTSVERWAHRUNGEN',
                'fr': 'RESERVES_DE_DROIT'
            }
        ],
        'description': {
            'de': 'Alle Rechtsbegehren vom Typ "Rechtsverwahrung"',
            'fr': 'Toutes les conclusions de type "Réserve de droit"'
        },
        'nested_aliases': {
            'ANLIEGEN': [
                {
                    'de': 'ANLIEGEN',
                    'fr': 'DEMANDE_REQUETE'
                },
                {
                    'de': 'ANLIEGEN',
                    'fr': 'PREOCCUPATION'
                }
            ],
            'DATUM_DOKUMENT': [
                {
                    'de': 'DATUM_DOKUMENT',
                    'fr': 'DATE_DOCUMENT'
                }
            ],
            'DATUM_EINGANG': [
                {
                    'de': 'DATUM_EINGANG',
                    'fr': 'DATE_RECEPTION'
                }
            ],
            'RECHTSBEGEHRENDE': [
                {
                    'de': 'RECHTSBEGEHRENDE',
                    'fr': 'REQUERANTS_CONCLUSIONS'
                }
            ],
            'TITEL': [
                {
                    'de': 'TITEL',
                    'fr': 'TITRE'
                }
            ]
        }
    },
    'ROOMS_WITH_MORE_THAN_50_PERSONS': {
        'aliases': [
            {
                'de': 'RAEUME_MEHR_50_PERSONEN',
                'fr': 'CHAMBRES_AVEC_PLUS_DE_50_PERSONNES'
            }
        ],
        'description': {
            'de': 'Liste der Räume mit mehr als 50 Personen',
            'fr': 'Liste des salles de plus de 50 personnes'
        },
        'nested_aliases': {
            'number_of_persons': [
                {
                    'de': 'ANZAHL_BEHERBERGTE_PERSONEN',
                    'fr': 'NOMBRE_DE_PERSONNES'
                }
            ],
            'room': [
                {
                    'de': 'RAUM',
                    'fr': 'CHAMBRE'
                }
            ]
        }
    },
    'ROOM_OCCUPANCY_ROOMS_MORE_THAN_50_PERSONS': {
        'aliases': [
            {
                'de': 'RAUM_BELEGUNG_MEHR_50_PERSONEN',
                'fr': 'OCCUPATION_CHAMBRES_PLUS_50_PERSONNES'
            }
        ],
        'description': {
            'de': 'Belegung der Räume mit mehr als 50 Personen',
            'fr': 'Occupation des chambres plus de 50 personnes'
        },
        'nested_aliases': {
        }
    },
    'RRB': {
        'aliases': [
            {
                'de': 'RRB',
                'fr': 'ACE'
            }
        ],
        'description': {
            'de': 'Unterschutzstellung RRB',
            'fr': 'Mise sous protection ACE'
        },
        'nested_aliases': {
        }
    },
    'RRB_START': {
        'aliases': [
            {
                'de': 'RRB_DATUM',
                'fr': 'RRB_DATE'
            }
        ],
        'description': {
            'de': 'Datum der Unterschutzstellung RRB',
            'fr': 'Date de mise sous protection ACE'
        },
        'nested_aliases': {
        }
    },
    'SACHVERHALT': {
        'aliases': [
            {
                'de': 'SACHVERHALT',
                'fr': 'SITUATION'
            }
        ],
        'description': {
            'de': 'Sachverhalt der Anfrage',
            'fr': 'Situation de la demande'
        },
        'nested_aliases': {
        }
    },
    'SOLAR_PANELS': {
        'aliases': [
            {
                'de': 'SOLARANLAGEN',
                'fr': 'PANNEAUX_SOLAIRES'
            }
        ],
        'description': {
            'de': 'Solaranlagen',
            'fr': 'Panneaux solaires'
        },
        'nested_aliases': {
            'energy_storage': [
                {
                    'de': 'ENERGIE_SPEICHER',
                    'fr': 'STOCKAGE_D_ENERGIE'
                }
            ],
            'energy_storage_capacity': [
                {
                    'de': 'ENERGIE_SPEICHER_KAPAZITAET',
                    'fr': 'CAPACITE_DE_STOCKAGE_D_ENERGIE'
                }
            ],
            'new_or_existing': [
                {
                    'de': 'NEU_BESTEHEND',
                    'fr': 'NOUVEAU_OU_EXISTANT'
                }
            ],
            'type': [
                {
                    'de': 'TYP',
                    'fr': 'TYPE'
                }
            ]
        }
    },
    'STATUS': {
        'aliases': [
            {
                'de': 'STATUS',
                'fr': 'ETAT'
            }
        ],
        'description': {
            'de': 'Momentaner Status des Dossiers',
            'fr': 'État actuel du dossier'
        },
        'nested_aliases': {
        }
    },
    'STELLUNGNAHME': {
        'aliases': [
            {
                'de': 'EIGENE_STELLUNGNAHMEN',
                'fr': 'PRISE_DE_POSITION'
            },
            {
                'de': 'STELLUNGNAHME',
                'fr': 'POINT_DE_VUE'
            }
        ],
        'description': {
            'de': 'Eigene Stellungnahmen',
            'fr': 'Prises de position propres'
        },
        'nested_aliases': {
        }
    },
    'STFV_CRITIAL_VALUE_EXCEEDED': {
        'aliases': [
            {
                'de': 'STFV_KRITISCHER_WERT_UEBERSCHRITTEN',
                'fr': 'STFV_VALEUR_CRITIQUE_DEPASSEE'
            }
        ],
        'description': {
            'de': 'StfV kritischer Wert überschritten',
            'fr': 'Dépassement de la valeur critique StfV'
        },
        'nested_aliases': {
        }
    },
    'STFV_SHORT_REPORT_DATE': {
        'aliases': [
            {
                'de': 'STFV_KURZ_BERICHT_DATUM',
                'fr': 'STFV_DATE_DU_RAPPORT_COURT'
            }
        ],
        'description': {
            'de': 'StfV Kurzbericht Datum',
            'fr': 'StfV date du rapport court'
        },
        'nested_aliases': {
        }
    },
    'STICHWORTE': {
        'aliases': [
            {
                'de': 'STICHWORTE',
                'fr': 'MOTS_CLES'
            }
        ],
        'description': {
            'de': 'Liste aller Stichworte',
            'fr': 'Liste des mots-clés'
        },
        'nested_aliases': {
        }
    },
    'TODAY': {
        'aliases': [
            {
                'de': 'HEUTE',
                'fr': 'AUJOURD_HUI'
            }
        ],
        'description': {
            'de': 'Das heutige Datum',
            'fr': "Date d'aujourd'hui"
        },
        'nested_aliases': {
        }
    },
    'UEBERBAUUNGSORDNUNG': {
        'aliases': [
            {
                'de': 'UEBERBAUUNGSORDNUNG',
                'fr': 'PLAN_QUARTIER'
            }
        ],
        'description': {
            'de': 'Erfasste Überbauungsordnung des/r Gesuchsteller/in',
            'fr': 'Plan de quartier saisi par la personne requérante'
        },
        'nested_aliases': {
        }
    },
    'UVP_JA_NEIN': {
        'aliases': [
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'VENTILATION_SYSTEMS': {
        'aliases': [
            {
                'de': 'LUEFTUNGSANLAGEN',
                'fr': 'SYSTEMES_DE_VENTILATION'
            }
        ],
        'description': {
            'de': 'Lüftungsanlagen',
            'fr': 'Systèmes de ventilation'
        },
        'nested_aliases': {
            'air_volume': [
                {
                    'de': 'VOLUMENSTROM',
                    'fr': 'VOLUME_D_AIR'
                }
            ],
            'new_or_existing': [
                {
                    'de': 'NEU_BESTEHEND',
                    'fr': 'NOUVEAU_OU_EXISTANT'
                }
            ],
            'system_type': [
                {
                    'de': 'TYP',
                    'fr': 'TYPE'
                }
            ]
        }
    },
    'VERTRETER': {
        'aliases': [
            {
                'de': 'VERTRETER',
                'fr': 'REPRESENTANT'
            }
        ],
        'description': {
            'de': 'Name des/r Vertreter/in',
            'fr': 'Nom de la personne resprésentante'
        },
        'nested_aliases': {
        }
    },
    'VERTRETER_ADDRESS_1': {
        'aliases': [
            {
                'de': 'VERTRETER_ADRESSE_1',
                'fr': 'REPRESENTANT_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 des/r Vertreter/in',
            'fr': "Ligne d'adresse 1 de la personne resprésentante"
        },
        'nested_aliases': {
        }
    },
    'VERTRETER_ADDRESS_2': {
        'aliases': [
            {
                'de': 'VERTRETER_ADRESSE_2',
                'fr': 'REPRESENTANT_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 des/r Vertreter/in',
            'fr': "Ligne d'adresse 2 de la personne resprésentante"
        },
        'nested_aliases': {
        }
    },
    'VERTRETER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'VERTRETER_NAME_ADRESSE',
                'fr': 'REPRESENTANT_NOM_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse des/r Vertreter/in',
            'fr': 'Nom et adresse de la personne resprésentante'
        },
        'nested_aliases': {
        }
    },
    'ZIRKULATION_FACHSTELLEN': {
        'aliases': [
            {
                'de': 'ZIRKULATION_FACHSTELLEN',
                'fr': 'CIRCULATION_SERVICES'
            }
        ],
        'description': {
            'de': 'In Dossier involvierte Fachstellen',
            'fr': 'Tous les services impliqués dans les dossiers'
        },
        'nested_aliases': {
            'BEANTWORTET': [
                {
                    'de': 'BEANTWORTET',
                    'fr': 'REPONDU'
                }
            ],
            'ERSTELLT': [
                {
                    'de': 'ERSTELLT',
                    'fr': 'CREE'
                }
            ],
            'FRIST': [
                {
                    'de': 'FRIST',
                    'fr': 'DELAI'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME',
                    'fr': 'NOM'
                }
            ]
        }
    },
    'ZIRKULATION_GEMEINDEN': {
        'aliases': [
            {
                'de': 'ZIRKULATION_GEMEINDEN',
                'fr': 'CIRCULATION_COMMUNES'
            }
        ],
        'description': {
            'de': 'In Dossier involvierte Gemeinden',
            'fr': 'Toutes les communes impliquées dans les dossiers'
        },
        'nested_aliases': {
            'BEANTWORTET': [
                {
                    'de': 'BEANTWORTET',
                    'fr': 'REPONDU'
                }
            ],
            'ERSTELLT': [
                {
                    'de': 'ERSTELLT',
                    'fr': 'CREE'
                }
            ],
            'FRIST': [
                {
                    'de': 'FRIST',
                    'fr': 'DELAI'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME',
                    'fr': 'NOM'
                }
            ]
        }
    },
    'ZIRKULATION_RSTA': {
        'aliases': [
            {
                'de': 'ZIRKULATION_RSTA',
                'fr': 'CIRCULATION_PREF'
            }
        ],
        'description': {
            'de': 'In Dossier involvierte Regierungsstatthalterämter',
            'fr': 'Toutes les préfectures impliquées dans les dossiers'
        },
        'nested_aliases': {
            'BEANTWORTET': [
                {
                    'de': 'BEANTWORTET',
                    'fr': 'REPONDU'
                }
            ],
            'ERSTELLT': [
                {
                    'de': 'ERSTELLT',
                    'fr': 'CREE'
                }
            ],
            'FRIST': [
                {
                    'de': 'FRIST',
                    'fr': 'DELAI'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME',
                    'fr': 'NOM'
                }
            ]
        }
    },
    'ZIRKULATION_RUECKMELDUNGEN': {
        'aliases': [
            {
                'de': 'ZIRKULATION_RUECKMELDUNGEN',
                'fr': 'CIRCULATION_PREAVIS'
            }
        ],
        'description': {
            'de': 'Stellungnahmen und Nebenbestimmungen der eingeladenen Fachstellen',
            'fr': 'Préavis et dispositions annexes des services invités à la procédure de circulation'
        },
        'nested_aliases': {
            'ANTWORT': [
                {
                    'de': 'ANTWORT',
                    'fr': 'REPONSE'
                }
            ],
            'NEBENBESTIMMUNGEN': [
                {
                    'de': 'NEBENBESTIMMUNGEN',
                    'fr': 'DISPOSITIONS_ACCESSOIRES'
                }
            ],
            'STELLUNGNAHME': [
                {
                    'de': 'STELLUNGNAHME',
                    'fr': 'POINT_DE_VUE'
                }
            ],
            'VON': [
                {
                    'de': 'VON',
                    'fr': 'DE'
                }
            ]
        }
    },
    'ZUSTAENDIG_EMAIL': {
        'aliases': [
            {
                'de': 'ZUSTAENDIG_EMAIL',
                'fr': 'RESPONSABLE_EMAIL'
            }
        ],
        'description': {
            'de': 'Email-Adresse des/r zuständigen/r Mitarbeiter/in',
            'fr': 'Adresse électronique de la personne responsable'
        },
        'nested_aliases': {
        }
    },
    'ZUSTAENDIG_NAME': {
        'aliases': [
            {
                'de': 'ZUSTAENDIG_NAME',
                'fr': 'RESPONSABLE_NOM'
            }
        ],
        'description': {
            'de': 'Name des/r zuständigen/r Mitarbeiter/in',
            'fr': 'Nom de la personne responsable'
        },
        'nested_aliases': {
        }
    },
    'ZUSTAENDIG_PHONE': {
        'aliases': [
            {
                'de': 'ZUSTAENDIG_TELEFON',
                'fr': 'RESPONSABLE_TELEPHONE'
            }
        ],
        'description': {
            'de': 'Telefonnummer des/r zuständigen/r Mitarbeiter/in',
            'fr': 'Numéro de téléphone de la personne responsable'
        },
        'nested_aliases': {
        }
    }
}

snapshots['test_dms_placeholders_docs[gr_dms_config] 1'] = {
    'ADDRESS': {
        'aliases': [
            {
                'de': 'ADRESSE'
            }
        ],
        'description': {
            'de': 'Adresse des betroffenen Grundstückes'
        },
        'nested_aliases': {
        }
    },
    'ALLE_GESUCHSTELLER': {
        'aliases': [
            {
                'de': 'ALLE_GESUCHSTELLER'
            }
        ],
        'description': {
            'de': 'Namen aller Gesuchsteller/innen'
        },
        'nested_aliases': {
        }
    },
    'ALLE_GESUCHSTELLER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'ALLE_GESUCHSTELLER_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Namen und Adressen aller Gesuchsteller/innen'
        },
        'nested_aliases': {
        }
    },
    'ALLE_GRUNDEIGENTUEMER': {
        'aliases': [
            {
                'de': 'ALLE_GRUNDEIGENTUEMER'
            }
        ],
        'description': {
            'de': 'Namen aller Grundeigentümer/innen'
        },
        'nested_aliases': {
        }
    },
    'ALLE_GRUNDEIGENTUEMER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'ALLE_GRUNDEIGENTUEMER_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Namen und Adressen aller Grundeigentümer/innen'
        },
        'nested_aliases': {
        }
    },
    'ALLE_PROJEKTVERFASSER': {
        'aliases': [
            {
                'de': 'ALLE_PROJEKTVERFASSER'
            }
        ],
        'description': {
            'de': 'Namen aller Projektverfasser/innen'
        },
        'nested_aliases': {
        }
    },
    'ALLE_PROJEKTVERFASSER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'ALLE_PROJEKTVERFASSER_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Namen und Adressen aller Projektverfasser/innen'
        },
        'nested_aliases': {
        }
    },
    'BASE_URL': {
        'aliases': [
            {
                'de': 'EBAU_URL'
            }
        ],
        'description': {
            'de': 'Die URL vom eBau-System'
        },
        'nested_aliases': {
        }
    },
    'BAUEINGABE_DATUM': {
        'aliases': [
            {
                'de': 'BAUEINGABE_DATUM'
            }
        ],
        'description': {
            'de': 'Datum an dem das Dossier eingereicht wurde'
        },
        'nested_aliases': {
        }
    },
    'BAUENTSCHEID': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID'
            }
        ],
        'description': {
            'de': 'Bauentscheid'
        },
        'nested_aliases': {
        }
    },
    'BEGINN_PUBLIKATIONSORGAN_GEMEINDE': {
        'aliases': [
            {
                'de': 'START_PUBLIKATION_GEMEINDE'
            }
        ],
        'description': {
            'de': 'Startdatum der Publikation im Publikationsorgan der Gemeinde'
        },
        'nested_aliases': {
        }
    },
    'BEGINN_PUBLIKATION_KANTONSAMTSBLATT': {
        'aliases': [
            {
                'de': 'START_PUBLIKATION_KANTON'
            }
        ],
        'description': {
            'de': 'Startdatum der Publikation im Kantonsamtsblatt'
        },
        'nested_aliases': {
        }
    },
    'BESCHREIBUNG_BAUVORHABEN': {
        'aliases': [
            {
                'de': 'BESCHREIBUNG_BAUVORHABEN'
            }
        ],
        'description': {
            'de': 'Beschreibung des Bauvorhabens'
        },
        'nested_aliases': {
        }
    },
    'DECISION_DATE': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_DATUM'
            }
        ],
        'description': {
            'de': 'Datum des Bauentscheids'
        },
        'nested_aliases': {
        }
    },
    'DESCRIPTION_MODIFICATION': {
        'aliases': [
            {
                'de': 'BESCHREIBUNG_PROJEKTAENDERUNG'
            }
        ],
        'description': {
            'de': 'Projektänderung'
        },
        'nested_aliases': {
        }
    },
    'DOSSIER_NUMBER': {
        'aliases': [
            {
                'de': 'DOSSIER_NUMMER'
            }
        ],
        'description': {
            'de': 'Die Nummer des Dossiers'
        },
        'nested_aliases': {
        }
    },
    'ENDE_PUBLIKATIONSORGAN_GEMEINDE': {
        'aliases': [
            {
                'de': 'ENDE_PUBLIKATION_GEMEINDE'
            }
        ],
        'description': {
            'de': 'Enddatum der Publikation im Publikationsorgan der Gemeinde'
        },
        'nested_aliases': {
        }
    },
    'ENDE_PUBLIKATION_KANTONSAMTSBLATT': {
        'aliases': [
            {
                'de': 'ENDE_PUBLIKATION_KANTON'
            }
        ],
        'description': {
            'de': 'Enddatum der Publikation im Kantonsamtsblatt'
        },
        'nested_aliases': {
        }
    },
    'ENTSCHEIDDOKUMENTE': {
        'aliases': [
            {
                'de': 'ENTSCHEIDDOKUMENTE'
            }
        ],
        'description': {
            'de': 'Alle Dokumente die als Entscheiddokument markiert wurden'
        },
        'nested_aliases': {
        }
    },
    'FACHSTELLEN_KANTONAL': {
        'aliases': [
            {
                'de': 'ZIRKULATION_ALLE'
            },
            {
                'de': 'FACHSTELLEN_KANTONAL'
            }
        ],
        'description': {
            'de': 'In Dossier involvierte Stellen'
        },
        'nested_aliases': {
            'BEANTWORTET': [
                {
                    'de': 'BEANTWORTET'
                }
            ],
            'ERSTELLT': [
                {
                    'de': 'ERSTELLT'
                }
            ],
            'FRIST': [
                {
                    'de': 'FRIST'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME'
                }
            ]
        }
    },
    'FOLGEPLANUNG': {
        'aliases': [
            {
                'de': 'FOLGEPLANUNG'
            }
        ],
        'description': {
            'de': 'Folgeplanung'
        },
        'nested_aliases': {
        }
    },
    'FORM_NAME': {
        'aliases': [
            {
                'de': 'DOSSIER_TYP'
            }
        ],
        'description': {
            'de': 'Typ des Dossiers'
        },
        'nested_aliases': {
        }
    },
    'GEBAEUDEVERSICHERUNGSNUMMER': {
        'aliases': [
            {
                'de': 'GEBAEUDEVERSICHERUNGSNUMMER'
            }
        ],
        'description': {
            'de': 'Gebäudeversicherungsnummer'
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_EMAIL': {
        'aliases': [
            {
                'de': 'GEMEINDE_EMAIL'
            }
        ],
        'description': {
            'de': 'Email-Adresse der Gemeinde'
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_NAME_ADRESSE': {
        'aliases': [
            {
                'de': 'GEMEINDE_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse der Gemeinde'
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_ORT': {
        'aliases': [
            {
                'de': 'GEMEINDE_ORT'
            }
        ],
        'description': {
            'de': 'Ort der Gemeinde'
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_TELEFON': {
        'aliases': [
            {
                'de': 'GEMEINDE_TELEFON'
            }
        ],
        'description': {
            'de': 'Telefonnummer der Gemeinde'
        },
        'nested_aliases': {
        }
    },
    'GENERELLER_ERSCHLIESSUNGSPLAN': {
        'aliases': [
            {
                'de': 'GENERELLER_ERSCHLIESSUNGSPLAN'
            }
        ],
        'description': {
            'de': 'Genereller Erschliessungsplan'
        },
        'nested_aliases': {
        }
    },
    'GENERELLER_GESTALTUNGSPLAN': {
        'aliases': [
            {
                'de': 'GENERELLER_GESTALTUNGSPLAN'
            }
        ],
        'description': {
            'de': 'Genereller Gestaltungsplan'
        },
        'nested_aliases': {
        }
    },
    'GESUCHSTELLER': {
        'aliases': [
            {
                'de': 'GESUCHSTELLER'
            }
        ],
        'description': {
            'de': 'Name des/r Gesuchsteller/in'
        },
        'nested_aliases': {
        }
    },
    'GESUCHSTELLER_ADDRESS_1': {
        'aliases': [
            {
                'de': 'GESUCHSTELLER_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 des/r ersten Gesuchsteller/in'
        },
        'nested_aliases': {
        }
    },
    'GESUCHSTELLER_ADDRESS_2': {
        'aliases': [
            {
                'de': 'GESUCHSTELLER_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 des/r ersten Gesuchsteller/in'
        },
        'nested_aliases': {
        }
    },
    'GESUCHSTELLER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'GESUCHSTELLER_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse des/r Gesuchsteller/in'
        },
        'nested_aliases': {
        }
    },
    'GRUNDEIGENTUEMER': {
        'aliases': [
            {
                'de': 'GRUNDEIGENTUEMER'
            }
        ],
        'description': {
            'de': 'Name des/r Grundeigentümer/in'
        },
        'nested_aliases': {
        }
    },
    'GRUNDEIGENTUEMER_ADDRESS_1': {
        'aliases': [
            {
                'de': 'GRUNDEIGENTUEMER_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 des/r ersten Grundeigentümer/in'
        },
        'nested_aliases': {
        }
    },
    'GRUNDEIGENTUEMER_ADDRESS_2': {
        'aliases': [
            {
                'de': 'GRUNDEIGENTUEMER_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 des/r ersten Grundeigentümer/in'
        },
        'nested_aliases': {
        }
    },
    'GRUNDEIGENTUEMER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'GRUNDEIGENTUEMER_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse des/r Grundeigentümer/in'
        },
        'nested_aliases': {
        }
    },
    'INSTANCE_ID': {
        'aliases': [
            {
                'de': 'ID'
            }
        ],
        'description': {
            'de': 'Die Nummer des Dossiers'
        },
        'nested_aliases': {
        }
    },
    'JURISTIC_NAME': {
        'aliases': [
            {
                'de': 'JURISTISCHER_NAME'
            }
        ],
        'description': {
            'de': 'Juristischer Name des/r Gesuchsteller/in'
        },
        'nested_aliases': {
        }
    },
    'KOORDINATEN': {
        'aliases': [
            {
                'de': 'KOORDINATEN'
            }
        ],
        'description': {
            'de': 'Lagekoordinaten der Parzelle(n)'
        },
        'nested_aliases': {
        }
    },
    'LANGUAGE': {
        'aliases': [
            {
                'de': 'SPRACHE'
            }
        ],
        'description': {
            'de': 'Die momentan ausgewählte Systemsprache'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_ADDRESS_1': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_ADDRESS_2': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_CITY': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_STADT'
            }
        ],
        'description': {
            'de': 'Ort der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_EMAIL': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_EMAIL'
            }
        ],
        'description': {
            'de': 'Email-Adresse der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_NAME': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_NAME'
            }
        ],
        'description': {
            'de': 'Name der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_NAME_KURZ': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_NAME_KURZ'
            }
        ],
        'description': {
            'de': 'Abgekürzter Name der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_PHONE': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_TELEFON'
            }
        ],
        'description': {
            'de': 'Telefonnummer der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_ADRESSE_1': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_ADRESSE_2': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_EMAIL': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_EMAIL'
            }
        ],
        'description': {
            'de': 'Email-Adresse der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_NAME': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_NAME'
            }
        ],
        'description': {
            'de': 'Name der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_NAME_ADRESSE': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_NAME_KURZ': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_NAME_KURZ'
            }
        ],
        'description': {
            'de': 'Abgekürzter Name der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_ORT': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_ORT'
            }
        ],
        'description': {
            'de': 'Ort der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_TELEFON': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_TELEFON'
            }
        ],
        'description': {
            'de': 'Telefonnummer der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MUNICIPALITY': {
        'aliases': [
            {
                'de': 'GEMEINDE'
            }
        ],
        'description': {
            'de': 'Die ausgewählte Gemeinde des/der Gesuchsteller/in'
        },
        'nested_aliases': {
        }
    },
    'MUNICIPALITY_ADDRESS': {
        'aliases': [
            {
                'de': 'GEMEINDE_ADRESSE'
            }
        ],
        'description': {
            'de': 'Die Adresse der ausgewählten Gemeinde des/der Gesuchsteller/in'
        },
        'nested_aliases': {
        }
    },
    'NAME': {
        'aliases': [
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'NEBENBESTIMMUNGEN': {
        'aliases': [
            {
                'de': 'EIGENE_NEBENBESTIMMUNGEN'
            },
            {
                'de': 'NEBENBESTIMMUNGEN'
            }
        ],
        'description': {
            'de': 'Eigene Nebenbestimmungen'
        },
        'nested_aliases': {
        }
    },
    'NEBENBESTIMMUNGEN_MAPPED': {
        'aliases': [
            {
                'de': 'NEBENBESTIMMUNGEN_MAPPED'
            }
        ],
        'description': None,
        'nested_aliases': {
            'FACHSTELLE': [
                {
                    'de': 'FACHSTELLE'
                }
            ],
            'TEXT': [
                {
                    'de': 'TEXT'
                }
            ]
        }
    },
    'PARZELLE': {
        'aliases': [
            {
                'de': 'PARZELLE'
            }
        ],
        'description': {
            'de': 'Die ausgewählte Parzelle(n) des/der Gesuchsteller/in'
        },
        'nested_aliases': {
        }
    },
    'PROJEKTVERFASSER': {
        'aliases': [
            {
                'de': 'PROJEKTVERFASSER'
            }
        ],
        'description': {
            'de': 'Name des/r Projektverfasser/in'
        },
        'nested_aliases': {
        }
    },
    'PROJEKTVERFASSER_ADDRESS_1': {
        'aliases': [
            {
                'de': 'PROJEKTVERFASSER_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 des/r ersten Projektverfasser/in'
        },
        'nested_aliases': {
        }
    },
    'PROJEKTVERFASSER_ADDRESS_2': {
        'aliases': [
            {
                'de': 'PROJEKTVERFASSER_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 des/r ersten Projektverfasser/in'
        },
        'nested_aliases': {
        }
    },
    'PROJEKTVERFASSER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'PROJEKTVERFASSER_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse des/r Projektverfasser/in'
        },
        'nested_aliases': {
        }
    },
    'PUBLIKATION_LINK': {
        'aliases': [
            {
                'de': 'PUBLIKATION_LINK'
            }
        ],
        'description': {
            'de': 'Link zur öffentlichen Auflage'
        },
        'nested_aliases': {
        }
    },
    'PUBLIKATION_TEXT': {
        'aliases': [
            {
                'de': 'PUBLIKATION_TEXT'
            }
        ],
        'description': {
            'de': 'Publikationstext des Dossiers'
        },
        'nested_aliases': {
        }
    },
    'STATUS': {
        'aliases': [
            {
                'de': 'STATUS'
            }
        ],
        'description': {
            'de': 'Momentaner Status des Dossiers'
        },
        'nested_aliases': {
        }
    },
    'STELLUNGNAHME': {
        'aliases': [
            {
                'de': 'EIGENE_STELLUNGNAHMEN'
            },
            {
                'de': 'STELLUNGNAHME'
            }
        ],
        'description': {
            'de': 'Eigene Stellungnahmen'
        },
        'nested_aliases': {
        }
    },
    'TODAY': {
        'aliases': [
            {
                'de': 'HEUTE'
            }
        ],
        'description': {
            'de': 'Das heutige Datum'
        },
        'nested_aliases': {
        }
    },
    'ZIRKULATION_FACHSTELLEN': {
        'aliases': [
            {
                'de': 'ZIRKULATION_FACHSTELLEN'
            }
        ],
        'description': {
            'de': 'In Dossier involvierte Fachstellen'
        },
        'nested_aliases': {
            'BEANTWORTET': [
                {
                    'de': 'BEANTWORTET'
                }
            ],
            'ERSTELLT': [
                {
                    'de': 'ERSTELLT'
                }
            ],
            'FRIST': [
                {
                    'de': 'FRIST'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME'
                }
            ]
        }
    },
    'ZIRKULATION_GEMEINDEN': {
        'aliases': [
            {
                'de': 'ZIRKULATION_GEMEINDEN'
            }
        ],
        'description': {
            'de': 'In Dossier involvierte Gemeinden'
        },
        'nested_aliases': {
            'BEANTWORTET': [
                {
                    'de': 'BEANTWORTET'
                }
            ],
            'ERSTELLT': [
                {
                    'de': 'ERSTELLT'
                }
            ],
            'FRIST': [
                {
                    'de': 'FRIST'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME'
                }
            ]
        }
    },
    'ZIRKULATION_RUECKMELDUNGEN': {
        'aliases': [
            {
                'de': 'ZIRKULATION_RUECKMELDUNGEN'
            }
        ],
        'description': {
            'de': 'Stellungnahmen und Nebenbestimmungen der eingeladenen Fachstellen'
        },
        'nested_aliases': {
            'ANTWORT': [
                {
                    'de': 'ANTWORT'
                }
            ],
            'NEBENBESTIMMUNGEN': [
                {
                    'de': 'NEBENBESTIMMUNGEN'
                }
            ],
            'STELLUNGNAHME': [
                {
                    'de': 'STELLUNGNAHME'
                }
            ],
            'VON': [
                {
                    'de': 'VON'
                }
            ]
        }
    },
    'ZONENPLAN': {
        'aliases': [
            {
                'de': 'ZONENPLAN'
            }
        ],
        'description': {
            'de': 'Zonenplan'
        },
        'nested_aliases': {
        }
    },
    'ZUSTAENDIG_NAME': {
        'aliases': [
            {
                'de': 'ZUSTAENDIG_NAME'
            }
        ],
        'description': {
            'de': 'Name des/r zuständigen/r Mitarbeiter/in'
        },
        'nested_aliases': {
        }
    }
}

snapshots['test_dms_placeholders_docs[so_dms_config] 1'] = {
    'ALLE_GESUCHSTELLER': {
        'aliases': [
            {
                'de': 'ALLE_BAUHERREN'
            }
        ],
        'description': {
            'de': 'Namen aller Bauherr/innen'
        },
        'nested_aliases': {
        }
    },
    'ALLE_GESUCHSTELLER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'ALLE_BAUHERREN_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Namen und Adressen aller Bauherr/innen'
        },
        'nested_aliases': {
        }
    },
    'ALLE_GRUNDEIGENTUEMER': {
        'aliases': [
            {
                'de': 'ALLE_GRUNDEIGENTUEMER'
            }
        ],
        'description': {
            'de': 'Namen aller Grundeigentümer/innen'
        },
        'nested_aliases': {
        }
    },
    'ALLE_GRUNDEIGENTUEMER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'ALLE_GRUNDEIGENTUEMER_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Namen und Adressen aller Grundeigentümer/innen'
        },
        'nested_aliases': {
        }
    },
    'ALLE_PROJEKTVERFASSER': {
        'aliases': [
            {
                'de': 'ALLE_PROJEKTVERFASSER'
            }
        ],
        'description': {
            'de': 'Namen aller Projektverfasser/innen'
        },
        'nested_aliases': {
        }
    },
    'ALLE_PROJEKTVERFASSER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'ALLE_PROJEKTVERFASSER_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Namen und Adressen aller Projektverfasser/innen'
        },
        'nested_aliases': {
        }
    },
    'BASE_URL': {
        'aliases': [
            {
                'de': 'EBAU_URL'
            }
        ],
        'description': {
            'de': 'Die URL vom eBau-System'
        },
        'nested_aliases': {
        }
    },
    'BAUEINGABE_DATUM': {
        'aliases': [
            {
                'de': 'BAUEINGABE_DATUM'
            }
        ],
        'description': {
            'de': 'Datum an dem das Dossier eingereicht wurde'
        },
        'nested_aliases': {
        }
    },
    'BESCHREIBUNG_BAUVORHABEN': {
        'aliases': [
            {
                'de': 'BESCHREIBUNG_BAUVORHABEN'
            }
        ],
        'description': {
            'de': 'Beschreibung des Bauvorhabens'
        },
        'nested_aliases': {
        }
    },
    'DECISION_DATE': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_DATUM'
            }
        ],
        'description': {
            'de': 'Datum des Bauentscheids'
        },
        'nested_aliases': {
        }
    },
    'DOSSIER_NUMBER': {
        'aliases': [
            {
                'de': 'DOSSIER_NUMMER'
            }
        ],
        'description': {
            'de': 'Die Nummer des Dossiers'
        },
        'nested_aliases': {
        }
    },
    'EIGENE_GEBUEHREN': {
        'aliases': [
            {
                'de': 'EIGENE_GEBUEHREN'
            }
        ],
        'description': {
            'de': 'Eigene Gebühren des Dossiers'
        },
        'nested_aliases': {
            'BETRAG': [
                {
                    'de': 'BETRAG'
                }
            ],
            'POSITION': [
                {
                    'de': 'POSITION'
                }
            ]
        }
    },
    'EIGENE_GEBUEHREN_TOTAL': {
        'aliases': [
            {
                'de': 'EIGENE_GEBUEHREN_TOTAL'
            }
        ],
        'description': {
            'de': 'Totalbetrag aller eigenen Gebühren des Dossiers'
        },
        'nested_aliases': {
        }
    },
    'FACHSTELLEN_KANTONAL': {
        'aliases': [
            {
                'de': 'ZIRKULATION_ALLE'
            },
            {
                'de': 'FACHSTELLEN_KANTONAL'
            }
        ],
        'description': {
            'de': 'In Dossier involvierte Stellen'
        },
        'nested_aliases': {
            'BEANTWORTET': [
                {
                    'de': 'BEANTWORTET'
                }
            ],
            'ERSTELLT': [
                {
                    'de': 'ERSTELLT'
                }
            ],
            'FRIST': [
                {
                    'de': 'FRIST'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME'
                }
            ]
        }
    },
    'FORM_NAME': {
        'aliases': [
            {
                'de': 'DOSSIER_TYP'
            }
        ],
        'description': {
            'de': 'Typ des Dossiers'
        },
        'nested_aliases': {
        }
    },
    'GEBUEHREN': {
        'aliases': [
            {
                'de': 'GEBUEHREN'
            }
        ],
        'description': {
            'de': 'Gebühren des Dossiers'
        },
        'nested_aliases': {
            'BETRAG': [
                {
                    'de': 'BETRAG'
                }
            ],
            'POSITION': [
                {
                    'de': 'POSITION'
                }
            ]
        }
    },
    'GEBUEHREN_TOTAL': {
        'aliases': [
            {
                'de': 'GEBUEHREN_TOTAL'
            }
        ],
        'description': {
            'de': 'Totalbetrag aller Gebühren des Dossiers'
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_EMAIL': {
        'aliases': [
            {
                'de': 'GEMEINDE_EMAIL'
            }
        ],
        'description': {
            'de': 'Email-Adresse der Gemeinde'
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_NAME_ADRESSE': {
        'aliases': [
            {
                'de': 'GEMEINDE_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse der Gemeinde'
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_ORT': {
        'aliases': [
            {
                'de': 'GEMEINDE_ORT'
            }
        ],
        'description': {
            'de': 'Ort der Gemeinde'
        },
        'nested_aliases': {
        }
    },
    'GEMEINDE_TELEFON': {
        'aliases': [
            {
                'de': 'GEMEINDE_TELEFON'
            }
        ],
        'description': {
            'de': 'Telefonnummer der Gemeinde'
        },
        'nested_aliases': {
        }
    },
    'GESUCHSTELLER': {
        'aliases': [
            {
                'de': 'BAUHERR'
            }
        ],
        'description': {
            'de': 'Name des/r Bauherr/in'
        },
        'nested_aliases': {
        }
    },
    'GESUCHSTELLER_ADDRESS_1': {
        'aliases': [
            {
                'de': 'BAUHERR_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 des/r ersten Bauherr/in'
        },
        'nested_aliases': {
        }
    },
    'GESUCHSTELLER_ADDRESS_2': {
        'aliases': [
            {
                'de': 'BAUHERR_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 des/r ersten Bauherr/in'
        },
        'nested_aliases': {
        }
    },
    'GESUCHSTELLER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'BAUHERR_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse des/r Bauherr/in'
        },
        'nested_aliases': {
        }
    },
    'GRUNDEIGENTUEMER': {
        'aliases': [
            {
                'de': 'GRUNDEIGENTUEMER'
            }
        ],
        'description': {
            'de': 'Name des/r Grundeigentümer/in'
        },
        'nested_aliases': {
        }
    },
    'GRUNDEIGENTUEMER_ADDRESS_1': {
        'aliases': [
            {
                'de': 'GRUNDEIGENTUEMER_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 des/r ersten Grundeigentümer/in'
        },
        'nested_aliases': {
        }
    },
    'GRUNDEIGENTUEMER_ADDRESS_2': {
        'aliases': [
            {
                'de': 'GRUNDEIGENTUEMER_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 des/r ersten Grundeigentümer/in'
        },
        'nested_aliases': {
        }
    },
    'GRUNDEIGENTUEMER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'GRUNDEIGENTUEMER_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse des/r Grundeigentümer/in'
        },
        'nested_aliases': {
        }
    },
    'JURISTIC_NAME': {
        'aliases': [
            {
                'de': 'JURISTISCHER_NAME'
            }
        ],
        'description': {
            'de': 'Juristischer Name des/r Bauherr/in\t'
        },
        'nested_aliases': {
        }
    },
    'KOORDINATEN': {
        'aliases': [
            {
                'de': 'KOORDINATEN'
            }
        ],
        'description': {
            'de': 'Lagekoordinaten der Parzelle(n)'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_ADDRESS_1': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_ADDRESS_2': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_CITY': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_STADT'
            }
        ],
        'description': {
            'de': 'Ort der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_EMAIL': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_EMAIL'
            }
        ],
        'description': {
            'de': 'Email-Adresse der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_NAME': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_NAME'
            }
        ],
        'description': {
            'de': 'Name der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_NAME_KURZ': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_NAME_KURZ'
            }
        ],
        'description': {
            'de': 'Abgekürzter Name der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'LEITBEHOERDE_PHONE': {
        'aliases': [
            {
                'de': 'LEITBEHOERDE_TELEFON'
            }
        ],
        'description': {
            'de': 'Telefonnummer der zuständigen Leitbehörde'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_ADRESSE_1': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_ADRESSE_2': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_EMAIL': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_EMAIL'
            }
        ],
        'description': {
            'de': 'Email-Adresse der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_NAME': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_NAME'
            }
        ],
        'description': {
            'de': 'Name der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_NAME_ADRESSE': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_NAME_KURZ': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_NAME_KURZ'
            }
        ],
        'description': {
            'de': 'Abgekürzter Name der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_ORT': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_ORT'
            }
        ],
        'description': {
            'de': 'Ort der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MEINE_ORGANISATION_TELEFON': {
        'aliases': [
            {
                'de': 'MEINE_ORGANISATION_TELEFON'
            }
        ],
        'description': {
            'de': 'Telefonnummer der momentan ausgewählten Organisation'
        },
        'nested_aliases': {
        }
    },
    'MUNICIPALITY': {
        'aliases': [
            {
                'de': 'GEMEINDE'
            }
        ],
        'description': {
            'de': 'Die ausgewählte Gemeinde des/der Bauherr/in'
        },
        'nested_aliases': {
        }
    },
    'MUNICIPALITY_ADDRESS': {
        'aliases': [
            {
                'de': 'GEMEINDE_ADRESSE'
            }
        ],
        'description': {
            'de': 'Die Adresse der ausgewählten Gemeinde des/der Bauherr/in'
        },
        'nested_aliases': {
        }
    },
    'NAME': {
        'aliases': [
        ],
        'description': None,
        'nested_aliases': {
        }
    },
    'NEBENBESTIMMUNGEN_MAPPED': {
        'aliases': [
            {
                'de': 'NEBENBESTIMMUNGEN_MAPPED'
            }
        ],
        'description': None,
        'nested_aliases': {
            'FACHSTELLE': [
                {
                    'de': 'FACHSTELLE'
                }
            ],
            'TEXT': [
                {
                    'de': 'TEXT'
                }
            ]
        }
    },
    'PARZELLE': {
        'aliases': [
            {
                'de': 'PARZELLE'
            }
        ],
        'description': {
            'de': 'Die ausgewählte Parzelle(n) des/der Bauherr/in'
        },
        'nested_aliases': {
        }
    },
    'PROJEKTVERFASSER': {
        'aliases': [
            {
                'de': 'PROJEKTVERFASSER'
            }
        ],
        'description': {
            'de': 'Name des/r Projektverfasser/in'
        },
        'nested_aliases': {
        }
    },
    'PROJEKTVERFASSER_ADDRESS_1': {
        'aliases': [
            {
                'de': 'PROJEKTVERFASSER_ADRESSE_1'
            }
        ],
        'description': {
            'de': 'Adresslinie 1 des/r ersten Projektverfasser/in'
        },
        'nested_aliases': {
        }
    },
    'PROJEKTVERFASSER_ADDRESS_2': {
        'aliases': [
            {
                'de': 'PROJEKTVERFASSER_ADRESSE_2'
            }
        ],
        'description': {
            'de': 'Adresslinie 2 des/r ersten Projektverfasser/in'
        },
        'nested_aliases': {
        }
    },
    'PROJEKTVERFASSER_NAME_ADDRESS': {
        'aliases': [
            {
                'de': 'PROJEKTVERFASSER_NAME_ADRESSE'
            }
        ],
        'description': {
            'de': 'Name und Adresse des/r Projektverfasser/in'
        },
        'nested_aliases': {
        }
    },
    'PUBLIKATION_LINK': {
        'aliases': [
            {
                'de': 'PUBLIKATION_LINK'
            }
        ],
        'description': {
            'de': 'Link zur öffentlichen Auflage'
        },
        'nested_aliases': {
        }
    },
    'STATUS': {
        'aliases': [
            {
                'de': 'STATUS'
            }
        ],
        'description': {
            'de': 'Momentaner Status des Dossiers'
        },
        'nested_aliases': {
        }
    },
    'TODAY': {
        'aliases': [
            {
                'de': 'HEUTE'
            }
        ],
        'description': {
            'de': 'Das heutige Datum'
        },
        'nested_aliases': {
        }
    },
    'ZIRKULATION_FACHSTELLEN': {
        'aliases': [
            {
                'de': 'ZIRKULATION_FACHSTELLEN'
            }
        ],
        'description': {
            'de': 'In Dossier involvierte Fachstellen'
        },
        'nested_aliases': {
            'BEANTWORTET': [
                {
                    'de': 'BEANTWORTET'
                }
            ],
            'ERSTELLT': [
                {
                    'de': 'ERSTELLT'
                }
            ],
            'FRIST': [
                {
                    'de': 'FRIST'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME'
                }
            ]
        }
    },
    'ZIRKULATION_GEMEINDEN': {
        'aliases': [
            {
                'de': 'ZIRKULATION_GEMEINDEN'
            }
        ],
        'description': {
            'de': 'In Dossier involvierte Gemeinden'
        },
        'nested_aliases': {
            'BEANTWORTET': [
                {
                    'de': 'BEANTWORTET'
                }
            ],
            'ERSTELLT': [
                {
                    'de': 'ERSTELLT'
                }
            ],
            'FRIST': [
                {
                    'de': 'FRIST'
                }
            ],
            'NAME': [
                {
                    'de': 'NAME'
                }
            ]
        }
    }
}

snapshots['test_dms_placeholders_docs_available_placeholders[be_dms_config] 1'] = [
    'ACE',
    'ADDRESS',
    'ADMINISTRATIVE_DISTRICT',
    'ADRESSE',
    'AFFECTATION',
    'AFFECTATION_ZONE',
    'ALCOHOL_SERVING',
    'ALKOHOLAUSSCHANK',
    'ALLE_GEBAEUDEEIGENTUEMER',
    'ALLE_GEBAEUDEEIGENTUEMER_NAME_ADDRESS',
    'ALLE_GEBAEUDEEIGENTUEMER_NAME_ADRESSE',
    'ALLE_GESUCHSTELLER',
    'ALLE_GESUCHSTELLER_NAME_ADDRESS',
    'ALLE_GESUCHSTELLER_NAME_ADRESSE',
    'ALLE_GRUNDEIGENTUEMER',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADDRESS',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADRESSE',
    'ALLE_NACHBARN',
    'ALLE_NACHBARN[]',
    'ALLE_NACHBARN[].ADDRESS_1',
    'ALLE_NACHBARN[].ADDRESS_2',
    'ALLE_NACHBARN[].ADRESSE_1',
    'ALLE_NACHBARN[].ADRESSE_2',
    'ALLE_NACHBARN[].NAME',
    'ALLE_NACHBARN[].NOM',
    'ALLE_PROJEKTVERFASSER',
    'ALLE_PROJEKTVERFASSER_NAME_ADDRESS',
    'ALLE_PROJEKTVERFASSER_NAME_ADRESSE',
    'ALLE_VERTRETER',
    'ALLE_VERTRETER_NAME_ADDRESS',
    'ALLE_VERTRETER_NAME_ADRESSE',
    'ANZAHL_BEHERBERGTE_PERSONEN',
    'ARRONDISSEMENT_ADMINISTRATIF',
    'ASCENSEURS',
    'ASCENSEURS[]',
    'ASCENSEURS[].ANLAGENTYP',
    'ASCENSEURS[].NEU_BESTEHEND',
    'ASCENSEURS[].NOUVEAU_OU_EXISTANT',
    'ASCENSEURS[].TYPE_INSTALLATION',
    'ASCENSEURS[].new_or_existing',
    'ASCENSEURS[].system_type',
    'AUFZUGSANLAGEN',
    'AUFZUGSANLAGEN[]',
    'AUFZUGSANLAGEN[].ANLAGENTYP',
    'AUFZUGSANLAGEN[].NEU_BESTEHEND',
    'AUFZUGSANLAGEN[].NOUVEAU_OU_EXISTANT',
    'AUFZUGSANLAGEN[].TYPE_INSTALLATION',
    'AUFZUGSANLAGEN[].new_or_existing',
    'AUFZUGSANLAGEN[].system_type',
    'AUJOURD_HUI',
    'AUTEUR_PROJET',
    'AUTEUR_PROJET_ADRESSE_1',
    'AUTEUR_PROJET_ADRESSE_2',
    'AUTEUR_PROJET_NOM_ADRESSE',
    'AUTEUR_PROJET_TOUS',
    'AUTEUR_PROJET_TOUS_NOM_ADRESSE',
    'AUTORITE_DIRECTRICE_ADRESSE_1',
    'AUTORITE_DIRECTRICE_ADRESSE_2',
    'AUTORITE_DIRECTRICE_EMAIL',
    'AUTORITE_DIRECTRICE_LIEU',
    'AUTORITE_DIRECTRICE_NOM',
    'AUTORITE_DIRECTRICE_NOM_ABR',
    'AUTORITE_DIRECTRICE_TELEPHONE',
    'BASE_URL',
    'BAUEINGABE_DATUM',
    'BAUENTSCHEID',
    'BAUENTSCHEID_BAUABSCHLAG',
    'BAUENTSCHEID_BAUABSCHLAG_MIT_WHST',
    'BAUENTSCHEID_BAUABSCHLAG_OHNE_WHST',
    'BAUENTSCHEID_BAUBEWILLIGUNG',
    'BAUENTSCHEID_BAUBEWILLIGUNGSFREI',
    'BAUENTSCHEID_DATUM',
    'BAUENTSCHEID_GENERELL',
    'BAUENTSCHEID_GESAMT',
    'BAUENTSCHEID_KLEIN',
    'BAUENTSCHEID_POSITIV',
    'BAUENTSCHEID_POSITIV_TEILWEISE',
    'BAUENTSCHEID_PROJEKTAENDERUNG',
    'BAUENTSCHEID_TEILBAUBEWILLIGUNG',
    'BAUENTSCHEID_TYP',
    'BAUENTSCHEID_TYPE',
    'BAUGRUPPE',
    'BAUGRUPPE_BEZEICHNUNG',
    'BAUKOSTEN',
    'BAUVORHABEN',
    'BESCHREIBUNG_BAUVORHABEN',
    'BESCHREIBUNG_PROJEKTAENDERUNG',
    'BOISSONS_ALCOOLIQUES',
    'BUILDING_DISTANCES',
    'BUILDING_DISTANCES[]',
    'BUILDING_DISTANCES[].ABSTAND_M',
    'BUILDING_DISTANCES[].COTE',
    'BUILDING_DISTANCES[].DISTANCE',
    'BUILDING_DISTANCES[].SEITE',
    'BUILDING_DISTANCES[].distance',
    'BUILDING_DISTANCES[].side',
    'CHAMBRES_AVEC_PLUS_DE_50_PERSONNES',
    'CHAMBRES_AVEC_PLUS_DE_50_PERSONNES[]',
    'CHAMBRES_AVEC_PLUS_DE_50_PERSONNES[].ANZAHL_BEHERBERGTE_PERSONEN',
    'CHAMBRES_AVEC_PLUS_DE_50_PERSONNES[].CHAMBRE',
    'CHAMBRES_AVEC_PLUS_DE_50_PERSONNES[].NOMBRE_DE_PERSONNES',
    'CHAMBRES_AVEC_PLUS_DE_50_PERSONNES[].RAUM',
    'CHAMBRES_AVEC_PLUS_DE_50_PERSONNES[].number_of_persons',
    'CHAMBRES_AVEC_PLUS_DE_50_PERSONNES[].room',
    'CIRCULATION_COMMUNES',
    'CIRCULATION_COMMUNES[]',
    'CIRCULATION_COMMUNES[].BEANTWORTET',
    'CIRCULATION_COMMUNES[].CREE',
    'CIRCULATION_COMMUNES[].DELAI',
    'CIRCULATION_COMMUNES[].ERSTELLT',
    'CIRCULATION_COMMUNES[].FRIST',
    'CIRCULATION_COMMUNES[].NAME',
    'CIRCULATION_COMMUNES[].NOM',
    'CIRCULATION_COMMUNES[].REPONDU',
    'CIRCULATION_PREAVIS',
    'CIRCULATION_PREAVIS[]',
    'CIRCULATION_PREAVIS[].ANTWORT',
    'CIRCULATION_PREAVIS[].DE',
    'CIRCULATION_PREAVIS[].DISPOSITIONS_ACCESSOIRES',
    'CIRCULATION_PREAVIS[].NEBENBESTIMMUNGEN',
    'CIRCULATION_PREAVIS[].POINT_DE_VUE',
    'CIRCULATION_PREAVIS[].REPONSE',
    'CIRCULATION_PREAVIS[].STELLUNGNAHME',
    'CIRCULATION_PREAVIS[].VON',
    'CIRCULATION_PREF',
    'CIRCULATION_PREF[]',
    'CIRCULATION_PREF[].BEANTWORTET',
    'CIRCULATION_PREF[].CREE',
    'CIRCULATION_PREF[].DELAI',
    'CIRCULATION_PREF[].ERSTELLT',
    'CIRCULATION_PREF[].FRIST',
    'CIRCULATION_PREF[].NAME',
    'CIRCULATION_PREF[].NOM',
    'CIRCULATION_PREF[].REPONDU',
    'CIRCULATION_SERVICES',
    'CIRCULATION_SERVICES[]',
    'CIRCULATION_SERVICES[].BEANTWORTET',
    'CIRCULATION_SERVICES[].CREE',
    'CIRCULATION_SERVICES[].DELAI',
    'CIRCULATION_SERVICES[].ERSTELLT',
    'CIRCULATION_SERVICES[].FRIST',
    'CIRCULATION_SERVICES[].NAME',
    'CIRCULATION_SERVICES[].NOM',
    'CIRCULATION_SERVICES[].REPONDU',
    'COMMUNE',
    'COMMUNE_ADRESSE',
    'COMMUNE_ADRESSE_1',
    'COMMUNE_ADRESSE_2',
    'COMMUNE_EMAIL',
    'COMMUNE_LIEU',
    'COMMUNE_NOM_ADRESSE',
    'COMMUNE_TELEPHONE',
    'COMMUNICATION_AUX_VOISINS_CODE_QR',
    'COMMUNICATION_AUX_VOISINS_LIEN',
    'CONSERVABLE',
    'CONSTRUCTION_COSTS',
    'CONSTRUCTION_GROUP',
    'CONSTRUCTION_GROUP_DESIGNATION',
    'CONTRACT',
    'CONTRACT_START',
    'CONTRAT',
    'CONTRAT_DATE',
    'COORDONEE',
    'COUTS_DE_CONSTRUCTION',
    'DECISION',
    'DECISION_CATEGORIE',
    'DECISION_DATE',
    'DECISION_GENERAL',
    'DECISION_GLOBALE',
    'DECISION_MODIF',
    'DECISION_PARTIEL',
    'DECISION_PERMIS',
    'DECISION_PETIT',
    'DECISION_POSITIVE',
    'DECISION_POSITIVE_PARTIEL',
    'DECISION_REFUS',
    'DECISION_REFUS_AVEC_RET',
    'DECISION_REFUS_SANS_RET',
    'DECISION_TYPE',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[]',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].ANLIEGEN',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].DATE_DOCUMENT',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].DATE_RECEPTION',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].DATUM_DOKUMENT',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].DATUM_EINGANG',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].DEMANDE_REQUETE',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].PREOCCUPATION',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].RECHTSBEGEHRENDE',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].REQUERANTS_CONCLUSIONS',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].TITEL',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].TITRE',
    'DEPOT_DEMANDE_DATE',
    'DESCRIPTION_MODIFICATION',
    'DIMENSIONEN_HOEHE',
    'DIMENSION_HAUTEUR',
    'DIMENSION_HEIGHT',
    'DISPOSITIONS_ACCESSOIRES',
    'DISPOSITIONS_ANNEXES',
    'DISTANCES_ENTRE_LES_BATIMENTS',
    'DISTANCES_ENTRE_LES_BATIMENTS[]',
    'DISTANCES_ENTRE_LES_BATIMENTS[].ABSTAND_M',
    'DISTANCES_ENTRE_LES_BATIMENTS[].COTE',
    'DISTANCES_ENTRE_LES_BATIMENTS[].DISTANCE',
    'DISTANCES_ENTRE_LES_BATIMENTS[].SEITE',
    'DISTANCES_ENTRE_LES_BATIMENTS[].distance',
    'DISTANCES_ENTRE_LES_BATIMENTS[].side',
    'DOSSIER_LINK',
    'DOSSIER_NR',
    'DOSSIER_NUMERO',
    'DOSSIER_TYP',
    'DOSSIER_TYPE',
    'EBAU_NR',
    'EBAU_NUMBER',
    'EBAU_NUMERO',
    'EBAU_URL',
    'EIGENE_GEBUEHREN',
    'EIGENE_GEBUEHREN[]',
    'EIGENE_GEBUEHREN[].BETRAG',
    'EIGENE_GEBUEHREN[].FORFAIT',
    'EIGENE_GEBUEHREN[].POSITION',
    'EIGENE_GEBUEHREN_TOTAL',
    'EIGENE_NEBENBESTIMMUNGEN',
    'EIGENE_STELLUNGNAHMEN',
    'EINSPRACHEN',
    'EINSPRACHEN[]',
    'EINSPRACHEN[].DATE_DOCUMENT',
    'EINSPRACHEN[].DATE_RECEPTION',
    'EINSPRACHEN[].DATUM_DOKUMENT',
    'EINSPRACHEN[].DATUM_EINGANG',
    'EINSPRACHEN[].GRIEFS',
    'EINSPRACHEN[].RECHTSBEGEHRENDE',
    'EINSPRACHEN[].REQUERANTS_CONCLUSIONS',
    'EINSPRACHEN[].RUEGEPUNKTE',
    'EINSPRACHEN[].TITEL',
    'EINSPRACHEN[].TITRE',
    'EINSPRECHENDE',
    'EINSPRECHENDE[]',
    'EINSPRECHENDE[].ADDRESS',
    'EINSPRECHENDE[].ADRESSE',
    'EINSPRECHENDE[].NAME',
    'EINSPRECHENDE[].NOM',
    'EMAIL',
    'EMOLUMENTS',
    'EMOLUMENTS[]',
    'EMOLUMENTS[].BETRAG',
    'EMOLUMENTS[].FORFAIT',
    'EMOLUMENTS[].POSITION',
    'EMOLUMENTS_TOTAL',
    'ENSEMBLE_BÂTI',
    'ENSEMBLE_BÂTI_DÉNOMINATION',
    'ERHALTENSWERT',
    'ETAT',
    'FACHSTELLEN_KANTONAL',
    'FACHSTELLEN_KANTONAL[]',
    'FACHSTELLEN_KANTONAL[].BEANTWORTET',
    'FACHSTELLEN_KANTONAL[].CREE',
    'FACHSTELLEN_KANTONAL[].DELAI',
    'FACHSTELLEN_KANTONAL[].ERSTELLT',
    'FACHSTELLEN_KANTONAL[].FRIST',
    'FACHSTELLEN_KANTONAL[].NAME',
    'FACHSTELLEN_KANTONAL[].NOM',
    'FACHSTELLEN_KANTONAL[].REPONDU',
    'FACHSTELLEN_KANTONAL_LIST',
    'FACHSTELLEN_KANTONAL_LISTE',
    'FIRE_PROTECTION_SYSTEMS',
    'FIRE_PROTECTION_SYSTEMS[]',
    'FIRE_PROTECTION_SYSTEMS[].NEU_BESTEHEND',
    'FIRE_PROTECTION_SYSTEMS[].NOUVEAU_OU_EXISTANT',
    'FIRE_PROTECTION_SYSTEMS[].TYP',
    'FIRE_PROTECTION_SYSTEMS[].TYPE',
    'FIRE_PROTECTION_SYSTEMS[].new_or_existing',
    'FIRE_PROTECTION_SYSTEMS[].type',
    'FLOOR_AREA',
    'FORM_NAME',
    'GEBAEUDEABSTAENDE',
    'GEBAEUDEABSTAENDE[]',
    'GEBAEUDEABSTAENDE[].ABSTAND_M',
    'GEBAEUDEABSTAENDE[].COTE',
    'GEBAEUDEABSTAENDE[].DISTANCE',
    'GEBAEUDEABSTAENDE[].SEITE',
    'GEBAEUDEABSTAENDE[].distance',
    'GEBAEUDEABSTAENDE[].side',
    'GEBAEUDEEIGENTUEMER',
    'GEBAEUDEEIGENTUEMER_ADDRESS_1',
    'GEBAEUDEEIGENTUEMER_ADDRESS_2',
    'GEBAEUDEEIGENTUEMER_ADRESSE_1',
    'GEBAEUDEEIGENTUEMER_ADRESSE_2',
    'GEBAEUDEEIGENTUEMER_NAME_ADDRESS',
    'GEBAEUDEEIGENTUEMER_NAME_ADRESSE',
    'GEBUEHREN',
    'GEBUEHREN[]',
    'GEBUEHREN[].BETRAG',
    'GEBUEHREN[].FORFAIT',
    'GEBUEHREN[].POSITION',
    'GEBUEHREN_TOTAL',
    'GEFAEHRLICHE_STOFFE',
    'GEFAEHRLICHE_STOFFE[]',
    'GEFAEHRLICHE_STOFFE[].BETRAG',
    'GEFAEHRLICHE_STOFFE[].FORFAIT',
    'GEFAEHRLICHE_STOFFE[].GROUPE_DE_MATIERES',
    'GEFAEHRLICHE_STOFFE[].MATERIAL',
    'GEFAEHRLICHE_STOFFE[].MATERIAU',
    'GEFAEHRLICHE_STOFFE[].STOFFGRUPPE',
    'GEFAEHRLICHE_STOFFE[].amount',
    'GEFAEHRLICHE_STOFFE[].material',
    'GEFAEHRLICHE_STOFFE[].material_group',
    'GEMEINDE',
    'GEMEINDE_ADRESSE',
    'GEMEINDE_ADRESSE_1',
    'GEMEINDE_ADRESSE_2',
    'GEMEINDE_EMAIL',
    'GEMEINDE_NAME_ADRESSE',
    'GEMEINDE_ORT',
    'GEMEINDE_TELEFON',
    'GESCHOSSFLAECHE',
    'GESUCHSTELLER',
    'GESUCHSTELLER_ADDRESS_1',
    'GESUCHSTELLER_ADDRESS_2',
    'GESUCHSTELLER_ADRESSE_1',
    'GESUCHSTELLER_ADRESSE_2',
    'GESUCHSTELLER_NAME_ADDRESS',
    'GESUCHSTELLER_NAME_ADRESSE',
    'GEWAESSERSCHUTZBEREICH',
    'GRUNDEIGENTUEMER',
    'GRUNDEIGENTUEMER_ADDRESS_1',
    'GRUNDEIGENTUEMER_ADDRESS_2',
    'GRUNDEIGENTUEMER_ADRESSE_1',
    'GRUNDEIGENTUEMER_ADRESSE_2',
    'GRUNDEIGENTUEMER_NAME_ADDRESS',
    'GRUNDEIGENTUEMER_NAME_ADRESSE',
    'HAZARDOUS_SUBSTANCES',
    'HAZARDOUS_SUBSTANCES[]',
    'HAZARDOUS_SUBSTANCES[].BETRAG',
    'HAZARDOUS_SUBSTANCES[].FORFAIT',
    'HAZARDOUS_SUBSTANCES[].GROUPE_DE_MATIERES',
    'HAZARDOUS_SUBSTANCES[].MATERIAL',
    'HAZARDOUS_SUBSTANCES[].MATERIAU',
    'HAZARDOUS_SUBSTANCES[].STOFFGRUPPE',
    'HAZARDOUS_SUBSTANCES[].amount',
    'HAZARDOUS_SUBSTANCES[].material',
    'HAZARDOUS_SUBSTANCES[].material_group',
    'HEATING_SYSTEMS',
    'HEATING_SYSTEMS[]',
    'HEATING_SYSTEMS[].BRENNSTOFFLAGERUNG',
    'HEATING_SYSTEMS[].LAGERMENGE',
    'HEATING_SYSTEMS[].LEISTUNG',
    'HEATING_SYSTEMS[].NEU_BESTEHEND',
    'HEATING_SYSTEMS[].NOUVEAU_OU_EXISTANT',
    'HEATING_SYSTEMS[].PUISSANCE',
    'HEATING_SYSTEMS[].QUANTITE_STOCKEE',
    'HEATING_SYSTEMS[].STOCKAGE_COMBUSTIBLE',
    'HEATING_SYSTEMS[].TYP',
    'HEATING_SYSTEMS[].TYPE',
    'HEATING_SYSTEMS[].combusitble_storage',
    'HEATING_SYSTEMS[].new_or_existing',
    'HEATING_SYSTEMS[].power',
    'HEATING_SYSTEMS[].storage_amount',
    'HEATING_SYSTEMS[].type',
    'HEUTE',
    'INFORMATION_OF_NEIGHBORS_LINK',
    'INFORMATION_OF_NEIGHBORS_QR_CODE',
    'INSTALLATIONS_AERAULIQUES',
    'INSTALLATIONS_AERAULIQUES[]',
    'INSTALLATIONS_AERAULIQUES[].BRENNSTOFFLAGERUNG',
    'INSTALLATIONS_AERAULIQUES[].LAGERMENGE',
    'INSTALLATIONS_AERAULIQUES[].LEISTUNG',
    'INSTALLATIONS_AERAULIQUES[].NEU_BESTEHEND',
    'INSTALLATIONS_AERAULIQUES[].NOUVEAU_OU_EXISTANT',
    'INSTALLATIONS_AERAULIQUES[].PUISSANCE',
    'INSTALLATIONS_AERAULIQUES[].QUANTITE_STOCKEE',
    'INSTALLATIONS_AERAULIQUES[].STOCKAGE_COMBUSTIBLE',
    'INSTALLATIONS_AERAULIQUES[].TYP',
    'INSTALLATIONS_AERAULIQUES[].TYPE',
    'INSTALLATIONS_AERAULIQUES[].combusitble_storage',
    'INSTALLATIONS_AERAULIQUES[].new_or_existing',
    'INSTALLATIONS_AERAULIQUES[].power',
    'INSTALLATIONS_AERAULIQUES[].storage_amount',
    'INSTALLATIONS_AERAULIQUES[].type',
    'INSTALLATIONS_TECH_LINCENDIE',
    'INSTALLATIONS_TECH_LINCENDIE[]',
    'INSTALLATIONS_TECH_LINCENDIE[].NEU_BESTEHEND',
    'INSTALLATIONS_TECH_LINCENDIE[].NOUVEAU_OU_EXISTANT',
    'INSTALLATIONS_TECH_LINCENDIE[].TYP',
    'INSTALLATIONS_TECH_LINCENDIE[].TYPE',
    'INSTALLATIONS_TECH_LINCENDIE[].new_or_existing',
    'INSTALLATIONS_TECH_LINCENDIE[].type',
    'INSTANCE_ID',
    'INTERIOR_SEATING',
    'INVENTAR',
    'JURISTIC_NAME',
    'JURISTISCHER_NAME',
    'KOORDINATEN',
    'K_OBJECT',
    'K_OBJEKT',
    'LANGUAGE',
    'LANGUE',
    'LASTENAUSGLEICHSBEGEHREN',
    'LASTENAUSGLEICHSBEGEHRENDE',
    'LASTENAUSGLEICHSBEGEHRENDE[]',
    'LASTENAUSGLEICHSBEGEHRENDE[].ADDRESS',
    'LASTENAUSGLEICHSBEGEHRENDE[].ADRESSE',
    'LASTENAUSGLEICHSBEGEHRENDE[].NAME',
    'LASTENAUSGLEICHSBEGEHRENDE[].NOM',
    'LASTENAUSGLEICHSBEGEHREN[]',
    'LASTENAUSGLEICHSBEGEHREN[].ANLIEGEN',
    'LASTENAUSGLEICHSBEGEHREN[].DATE_DOCUMENT',
    'LASTENAUSGLEICHSBEGEHREN[].DATE_RECEPTION',
    'LASTENAUSGLEICHSBEGEHREN[].DATUM_DOKUMENT',
    'LASTENAUSGLEICHSBEGEHREN[].DATUM_EINGANG',
    'LASTENAUSGLEICHSBEGEHREN[].DEMANDE_REQUETE',
    'LASTENAUSGLEICHSBEGEHREN[].PREOCCUPATION',
    'LASTENAUSGLEICHSBEGEHREN[].RECHTSBEGEHRENDE',
    'LASTENAUSGLEICHSBEGEHREN[].REQUERANTS_CONCLUSIONS',
    'LASTENAUSGLEICHSBEGEHREN[].TITEL',
    'LASTENAUSGLEICHSBEGEHREN[].TITRE',
    'LEGAL_CLAIMANTS',
    'LEGAL_CLAIMANTS[]',
    'LEGAL_CLAIMANTS[].ADDRESS',
    'LEGAL_CLAIMANTS[].ADRESSE',
    'LEGAL_CLAIMANTS[].NAME',
    'LEGAL_CLAIMANTS[].NOM',
    'LEGAL_CUSTODIANS',
    'LEGAL_CUSTODIANS[]',
    'LEGAL_CUSTODIANS[].ADDRESS',
    'LEGAL_CUSTODIANS[].ADRESSE',
    'LEGAL_CUSTODIANS[].NAME',
    'LEGAL_CUSTODIANS[].NOM',
    'LEITBEHOERDE_ADDRESS_1',
    'LEITBEHOERDE_ADDRESS_2',
    'LEITBEHOERDE_ADRESSE_1',
    'LEITBEHOERDE_ADRESSE_2',
    'LEITBEHOERDE_CITY',
    'LEITBEHOERDE_EMAIL',
    'LEITBEHOERDE_NAME',
    'LEITBEHOERDE_NAME_KURZ',
    'LEITBEHOERDE_PHONE',
    'LEITBEHOERDE_STADT',
    'LEITBEHOERDE_TELEFON',
    'LEITPERSON',
    'LIEN_PUBLICATION',
    'LIFTS',
    'LIFTS[]',
    'LIFTS[].ANLAGENTYP',
    'LIFTS[].NEU_BESTEHEND',
    'LIFTS[].NOUVEAU_OU_EXISTANT',
    'LIFTS[].TYPE_INSTALLATION',
    'LIFTS[].new_or_existing',
    'LIFTS[].system_type',
    'LOAD_COMPENSATION_REQUESTING',
    'LOAD_COMPENSATION_REQUESTING[]',
    'LOAD_COMPENSATION_REQUESTING[].ADDRESS',
    'LOAD_COMPENSATION_REQUESTING[].ADRESSE',
    'LOAD_COMPENSATION_REQUESTING[].NAME',
    'LOAD_COMPENSATION_REQUESTING[].NOM',
    'LUEFTUNGSANLAGEN',
    'LUEFTUNGSANLAGEN[]',
    'LUEFTUNGSANLAGEN[].NEU_BESTEHEND',
    'LUEFTUNGSANLAGEN[].NOUVEAU_OU_EXISTANT',
    'LUEFTUNGSANLAGEN[].TYP',
    'LUEFTUNGSANLAGEN[].TYPE',
    'LUEFTUNGSANLAGEN[].VOLUMENSTROM',
    'LUEFTUNGSANLAGEN[].VOLUME_D_AIR',
    'LUEFTUNGSANLAGEN[].air_volume',
    'LUEFTUNGSANLAGEN[].new_or_existing',
    'LUEFTUNGSANLAGEN[].system_type',
    'MATIERES_DANGEREUSES',
    'MATIERES_DANGEREUSES[]',
    'MATIERES_DANGEREUSES[].BETRAG',
    'MATIERES_DANGEREUSES[].FORFAIT',
    'MATIERES_DANGEREUSES[].GROUPE_DE_MATIERES',
    'MATIERES_DANGEREUSES[].MATERIAL',
    'MATIERES_DANGEREUSES[].MATERIAU',
    'MATIERES_DANGEREUSES[].STOFFGRUPPE',
    'MATIERES_DANGEREUSES[].amount',
    'MATIERES_DANGEREUSES[].material',
    'MATIERES_DANGEREUSES[].material_group',
    'MEINE_ORGANISATION_ADRESSE_1',
    'MEINE_ORGANISATION_ADRESSE_2',
    'MEINE_ORGANISATION_EMAIL',
    'MEINE_ORGANISATION_NAME',
    'MEINE_ORGANISATION_NAME_ADRESSE',
    'MEINE_ORGANISATION_NAME_KURZ',
    'MEINE_ORGANISATION_ORT',
    'MEINE_ORGANISATION_TELEFON',
    'MES_EMOLUMENTS',
    'MES_EMOLUMENTS[]',
    'MES_EMOLUMENTS[].BETRAG',
    'MES_EMOLUMENTS[].FORFAIT',
    'MES_EMOLUMENTS[].POSITION',
    'MES_EMOLUMENTS_TOTAL',
    'MODIFICATION_DATE',
    'MODIFICATION_TIME',
    'MON_ORGANISATION_ADRESSE_1',
    'MON_ORGANISATION_ADRESSE_2',
    'MON_ORGANISATION_EMAIL',
    'MON_ORGANISATION_LIEU',
    'MON_ORGANISATION_NOM',
    'MON_ORGANISATION_NOM_ABR',
    'MON_ORGANISATION_NOM_ADRESSE',
    'MON_ORGANISATION_TELEPHONE',
    'MOTS_CLES',
    'MUNICIPALITY',
    'MUNICIPALITY_ADDRESS',
    'NACHBARSCHAFTSORIENTIERUNG_LINK',
    'NACHBARSCHAFTSORIENTIERUNG_QR_CODE',
    'NAME',
    'NEBENBESTIMMUNGEN',
    'NEBENBESTIMMUNGEN_MAPPED',
    'NEBENBESTIMMUNGEN_MAPPED[]',
    'NEBENBESTIMMUNGEN_MAPPED[].FACHSTELLE',
    'NEBENBESTIMMUNGEN_MAPPED[].SERVICE',
    'NEBENBESTIMMUNGEN_MAPPED[].TEXT',
    'NEBENBESTIMMUNGEN_MAPPED[].TEXTE',
    'NEIGHBORS',
    'NEIGHBORS[]',
    'NEIGHBORS[].ADDRESS_1',
    'NEIGHBORS[].ADDRESS_2',
    'NEIGHBORS[].ADRESSE_1',
    'NEIGHBORS[].ADRESSE_2',
    'NEIGHBORS[].NAME',
    'NEIGHBORS[].NOM',
    'NOMBRE_DE_PERSONNES_ACCOMPAGNEES',
    'NOM_LEGAL',
    'NUMBER_OF_ACCOMODATED_PERSONS',
    'NUTZUNG',
    'NUTZUNGSZONE',
    'OBJECTIONS',
    'OBJECTIONS[]',
    'OBJECTIONS[].DATE_DOCUMENT',
    'OBJECTIONS[].DATE_RECEPTION',
    'OBJECTIONS[].DATUM_DOKUMENT',
    'OBJECTIONS[].DATUM_EINGANG',
    'OBJECTIONS[].GRIEFS',
    'OBJECTIONS[].RECHTSBEGEHRENDE',
    'OBJECTIONS[].REQUERANTS_CONCLUSIONS',
    'OBJECTIONS[].RUEGEPUNKTE',
    'OBJECTIONS[].TITEL',
    'OBJECTIONS[].TITRE',
    'OBJECT_C',
    'OCCUPATION_CHAMBRES_PLUS_50_PERSONNES',
    'OEFFENTLICHKEIT',
    'OFFICES_CANTONAUX',
    'OFFICES_CANTONAUX[]',
    'OFFICES_CANTONAUX[].BEANTWORTET',
    'OFFICES_CANTONAUX[].CREE',
    'OFFICES_CANTONAUX[].DELAI',
    'OFFICES_CANTONAUX[].ERSTELLT',
    'OFFICES_CANTONAUX[].FRIST',
    'OFFICES_CANTONAUX[].NAME',
    'OFFICES_CANTONAUX[].NOM',
    'OFFICES_CANTONAUX[].REPONDU',
    'OFFICES_CANTONAUX_LISTE',
    'OPPOSANTS',
    'OPPOSANTS[]',
    'OPPOSANTS[].ADDRESS',
    'OPPOSANTS[].ADRESSE',
    'OPPOSANTS[].NAME',
    'OPPOSANTS[].NOM',
    'OPPOSING',
    'OPPOSING[]',
    'OPPOSING[].ADDRESS',
    'OPPOSING[].ADRESSE',
    'OPPOSING[].NAME',
    'OPPOSING[].NOM',
    'OPPOSITIONS',
    'OPPOSITIONS[]',
    'OPPOSITIONS[].DATE_DOCUMENT',
    'OPPOSITIONS[].DATE_RECEPTION',
    'OPPOSITIONS[].DATUM_DOKUMENT',
    'OPPOSITIONS[].DATUM_EINGANG',
    'OPPOSITIONS[].GRIEFS',
    'OPPOSITIONS[].RECHTSBEGEHRENDE',
    'OPPOSITIONS[].REQUERANTS_CONCLUSIONS',
    'OPPOSITIONS[].RUEGEPUNKTE',
    'OPPOSITIONS[].TITEL',
    'OPPOSITIONS[].TITRE',
    'OUTSIDE_SEATING',
    'OUVERTURE_PUBLIC',
    'PANNEAUX_SOLAIRES',
    'PANNEAUX_SOLAIRES[]',
    'PANNEAUX_SOLAIRES[].CAPACITE_DE_STOCKAGE_D_ENERGIE',
    'PANNEAUX_SOLAIRES[].ENERGIE_SPEICHER',
    'PANNEAUX_SOLAIRES[].ENERGIE_SPEICHER_KAPAZITAET',
    'PANNEAUX_SOLAIRES[].NEU_BESTEHEND',
    'PANNEAUX_SOLAIRES[].NOUVEAU_OU_EXISTANT',
    'PANNEAUX_SOLAIRES[].STOCKAGE_D_ENERGIE',
    'PANNEAUX_SOLAIRES[].TYP',
    'PANNEAUX_SOLAIRES[].TYPE',
    'PANNEAUX_SOLAIRES[].energy_storage',
    'PANNEAUX_SOLAIRES[].energy_storage_capacity',
    'PANNEAUX_SOLAIRES[].new_or_existing',
    'PANNEAUX_SOLAIRES[].type',
    'PARCELLE',
    'PARZELLE',
    'PLACES_ASSISES_EXT',
    'PLACES_ASSISES_INT',
    'PLAN_QUARTIER',
    'POINT_DE_VUE',
    'PRISE_DE_POSITION',
    'PROJEKTVERFASSER',
    'PROJEKTVERFASSER_ADDRESS_1',
    'PROJEKTVERFASSER_ADDRESS_2',
    'PROJEKTVERFASSER_ADRESSE_1',
    'PROJEKTVERFASSER_ADRESSE_2',
    'PROJEKTVERFASSER_NAME_ADDRESS',
    'PROJEKTVERFASSER_NAME_ADRESSE',
    'PROJET_CONSTR',
    'PROJET_CONSTR_DESCR',
    'PROPRIETAIRE_FONC',
    'PROPRIETAIRE_FONC_ADRESSE_1',
    'PROPRIETAIRE_FONC_ADRESSE_2',
    'PROPRIETAIRE_FONC_NOM_ADRESSE',
    'PROPRIETAIRE_FONC_TOUS',
    'PROPRIETAIRE_FONC_TOUS_NOM_ADRESSE',
    'PROPRIETAIRE_IMMOB',
    'PROPRIETAIRE_IMMOB_ADRESSE_1',
    'PROPRIETAIRE_IMMOB_ADRESSE_2',
    'PROPRIETAIRE_IMMOB_NOM_ADRESSE',
    'PROPRIETAIRE_IMMOB_TOUS',
    'PROPRIETAIRE_IMMOB_TOUS_NOM_ADRESSE',
    'PROTECTED',
    'PROTECTION_AREA',
    'PROTÉGÉ',
    'PUBLIC',
    'PUBLICATION_1_FEUILLE_AVIS',
    'PUBLICATION_2_FEUILLE_AVIS',
    'PUBLICATION_DEBUT',
    'PUBLICATION_EXPIRATION',
    'PUBLICATION_FEUILLE_AVIS_NOM',
    'PUBLICATION_FEUILLE_OFFICIELLE',
    'PUBLICATION_TEXTE',
    'PUBLIKATION_1_ANZEIGER',
    'PUBLIKATION_2_ANZEIGER',
    'PUBLIKATION_AMTSBLATT',
    'PUBLIKATION_ANZEIGER_NAME',
    'PUBLIKATION_ENDE',
    'PUBLIKATION_LINK',
    'PUBLIKATION_START',
    'PUBLIKATION_TEXT',
    'QS_RESPONSIBLE',
    'QS_VERANTWORTLICHER',
    'RAEUME_MEHR_50_PERSONEN',
    'RAEUME_MEHR_50_PERSONEN[]',
    'RAEUME_MEHR_50_PERSONEN[].ANZAHL_BEHERBERGTE_PERSONEN',
    'RAEUME_MEHR_50_PERSONEN[].CHAMBRE',
    'RAEUME_MEHR_50_PERSONEN[].NOMBRE_DE_PERSONNES',
    'RAEUME_MEHR_50_PERSONEN[].RAUM',
    'RAEUME_MEHR_50_PERSONEN[].number_of_persons',
    'RAEUME_MEHR_50_PERSONEN[].room',
    'RAUM_BELEGUNG_MEHR_50_PERSONEN',
    'RECENSEMENT',
    'RECHTSBEGEHRENDE',
    'RECHTSBEGEHRENDE[]',
    'RECHTSBEGEHRENDE[].ADDRESS',
    'RECHTSBEGEHRENDE[].ADRESSE',
    'RECHTSBEGEHRENDE[].NAME',
    'RECHTSBEGEHRENDE[].NOM',
    'RECHTSVERWAHRENDE',
    'RECHTSVERWAHRENDE[]',
    'RECHTSVERWAHRENDE[].ADDRESS',
    'RECHTSVERWAHRENDE[].ADRESSE',
    'RECHTSVERWAHRENDE[].NAME',
    'RECHTSVERWAHRENDE[].NOM',
    'RECHTSVERWAHRUNGEN',
    'RECHTSVERWAHRUNGEN[]',
    'RECHTSVERWAHRUNGEN[].ANLIEGEN',
    'RECHTSVERWAHRUNGEN[].DATE_DOCUMENT',
    'RECHTSVERWAHRUNGEN[].DATE_RECEPTION',
    'RECHTSVERWAHRUNGEN[].DATUM_DOKUMENT',
    'RECHTSVERWAHRUNGEN[].DATUM_EINGANG',
    'RECHTSVERWAHRUNGEN[].DEMANDE_REQUETE',
    'RECHTSVERWAHRUNGEN[].PREOCCUPATION',
    'RECHTSVERWAHRUNGEN[].RECHTSBEGEHRENDE',
    'RECHTSVERWAHRUNGEN[].REQUERANTS_CONCLUSIONS',
    'RECHTSVERWAHRUNGEN[].TITEL',
    'RECHTSVERWAHRUNGEN[].TITRE',
    'REPRESENTANT',
    'REPRESENTANT_ADRESSE_1',
    'REPRESENTANT_ADRESSE_2',
    'REPRESENTANT_NOM_ADRESSE',
    'REPRESENTANT_TOUS',
    'REPRESENTANT_TOUS_NOM_ADRESSE',
    'REQUERANT',
    'REQUERANTS_COMPENSATION_DES_CHARGES',
    'REQUERANTS_COMPENSATION_DES_CHARGES[]',
    'REQUERANTS_COMPENSATION_DES_CHARGES[].ADDRESS',
    'REQUERANTS_COMPENSATION_DES_CHARGES[].ADRESSE',
    'REQUERANTS_COMPENSATION_DES_CHARGES[].NAME',
    'REQUERANTS_COMPENSATION_DES_CHARGES[].NOM',
    'REQUERANTS_CONCLUSIONS',
    'REQUERANTS_CONCLUSIONS[]',
    'REQUERANTS_CONCLUSIONS[].ADDRESS',
    'REQUERANTS_CONCLUSIONS[].ADRESSE',
    'REQUERANTS_CONCLUSIONS[].NAME',
    'REQUERANTS_CONCLUSIONS[].NOM',
    'REQUERANTS_RESERVE_DE_DROIT',
    'REQUERANTS_RESERVE_DE_DROIT[]',
    'REQUERANTS_RESERVE_DE_DROIT[].ADDRESS',
    'REQUERANTS_RESERVE_DE_DROIT[].ADRESSE',
    'REQUERANTS_RESERVE_DE_DROIT[].NAME',
    'REQUERANTS_RESERVE_DE_DROIT[].NOM',
    'REQUERANT_ADRESSE_1',
    'REQUERANT_ADRESSE_2',
    'REQUERANT_NOM_ADRESSE',
    'REQUERANT_TOUS',
    'REQUERANT_TOUS_NOM_ADRESSE',
    'RESERVES_DE_DROIT',
    'RESERVES_DE_DROIT[]',
    'RESERVES_DE_DROIT[].ANLIEGEN',
    'RESERVES_DE_DROIT[].DATE_DOCUMENT',
    'RESERVES_DE_DROIT[].DATE_RECEPTION',
    'RESERVES_DE_DROIT[].DATUM_DOKUMENT',
    'RESERVES_DE_DROIT[].DATUM_EINGANG',
    'RESERVES_DE_DROIT[].DEMANDE_REQUETE',
    'RESERVES_DE_DROIT[].PREOCCUPATION',
    'RESERVES_DE_DROIT[].RECHTSBEGEHRENDE',
    'RESERVES_DE_DROIT[].REQUERANTS_CONCLUSIONS',
    'RESERVES_DE_DROIT[].TITEL',
    'RESERVES_DE_DROIT[].TITRE',
    'RESPONSABLE_AUTORITE_DIRECTRICE',
    'RESPONSABLE_EMAIL',
    'RESPONSABLE_NOM',
    'RESPONSABLE_TELEPHONE',
    'ROOMS_WITH_MORE_THAN_50_PERSONS',
    'ROOMS_WITH_MORE_THAN_50_PERSONS[]',
    'ROOMS_WITH_MORE_THAN_50_PERSONS[].ANZAHL_BEHERBERGTE_PERSONEN',
    'ROOMS_WITH_MORE_THAN_50_PERSONS[].CHAMBRE',
    'ROOMS_WITH_MORE_THAN_50_PERSONS[].NOMBRE_DE_PERSONNES',
    'ROOMS_WITH_MORE_THAN_50_PERSONS[].RAUM',
    'ROOMS_WITH_MORE_THAN_50_PERSONS[].number_of_persons',
    'ROOMS_WITH_MORE_THAN_50_PERSONS[].room',
    'ROOM_OCCUPANCY_ROOMS_MORE_THAN_50_PERSONS',
    'RRB',
    'RRB_DATE',
    'RRB_DATUM',
    'RRB_START',
    'SACHVERHALT',
    'SCHUTZZONE',
    'SCHÜTZENSWERT',
    'SECTEUR_PROTECTION_EAUX',
    'SITUATION',
    'SITZPLAETZE_AUSSEN',
    'SITZPLAETZE_INNEN',
    'SOLARANLAGEN',
    'SOLARANLAGEN[]',
    'SOLARANLAGEN[].CAPACITE_DE_STOCKAGE_D_ENERGIE',
    'SOLARANLAGEN[].ENERGIE_SPEICHER',
    'SOLARANLAGEN[].ENERGIE_SPEICHER_KAPAZITAET',
    'SOLARANLAGEN[].NEU_BESTEHEND',
    'SOLARANLAGEN[].NOUVEAU_OU_EXISTANT',
    'SOLARANLAGEN[].STOCKAGE_D_ENERGIE',
    'SOLARANLAGEN[].TYP',
    'SOLARANLAGEN[].TYPE',
    'SOLARANLAGEN[].energy_storage',
    'SOLARANLAGEN[].energy_storage_capacity',
    'SOLARANLAGEN[].new_or_existing',
    'SOLARANLAGEN[].type',
    'SOLAR_PANELS',
    'SOLAR_PANELS[]',
    'SOLAR_PANELS[].CAPACITE_DE_STOCKAGE_D_ENERGIE',
    'SOLAR_PANELS[].ENERGIE_SPEICHER',
    'SOLAR_PANELS[].ENERGIE_SPEICHER_KAPAZITAET',
    'SOLAR_PANELS[].NEU_BESTEHEND',
    'SOLAR_PANELS[].NOUVEAU_OU_EXISTANT',
    'SOLAR_PANELS[].STOCKAGE_D_ENERGIE',
    'SOLAR_PANELS[].TYP',
    'SOLAR_PANELS[].TYPE',
    'SOLAR_PANELS[].energy_storage',
    'SOLAR_PANELS[].energy_storage_capacity',
    'SOLAR_PANELS[].new_or_existing',
    'SOLAR_PANELS[].type',
    'SPRACHE',
    'STATUS',
    'STELLUNGNAHME',
    'STFV_CRITIAL_VALUE_EXCEEDED',
    'STFV_DATE_DU_RAPPORT_COURT',
    'STFV_KRITISCHER_WERT_UEBERSCHRITTEN',
    'STFV_KURZ_BERICHT_DATUM',
    'STFV_SHORT_REPORT_DATE',
    'STFV_VALEUR_CRITIQUE_DEPASSEE',
    'STICHWORTE',
    'SURFACE_DE_PLANCHER',
    'SYSTEMES_DE_VENTILATION',
    'SYSTEMES_DE_VENTILATION[]',
    'SYSTEMES_DE_VENTILATION[].NEU_BESTEHEND',
    'SYSTEMES_DE_VENTILATION[].NOUVEAU_OU_EXISTANT',
    'SYSTEMES_DE_VENTILATION[].TYP',
    'SYSTEMES_DE_VENTILATION[].TYPE',
    'SYSTEMES_DE_VENTILATION[].VOLUMENSTROM',
    'SYSTEMES_DE_VENTILATION[].VOLUME_D_AIR',
    'SYSTEMES_DE_VENTILATION[].air_volume',
    'SYSTEMES_DE_VENTILATION[].new_or_existing',
    'SYSTEMES_DE_VENTILATION[].system_type',
    'TECHNISCHE_BRANDSCHUTZANLAGEN',
    'TECHNISCHE_BRANDSCHUTZANLAGEN[]',
    'TECHNISCHE_BRANDSCHUTZANLAGEN[].NEU_BESTEHEND',
    'TECHNISCHE_BRANDSCHUTZANLAGEN[].NOUVEAU_OU_EXISTANT',
    'TECHNISCHE_BRANDSCHUTZANLAGEN[].TYP',
    'TECHNISCHE_BRANDSCHUTZANLAGEN[].TYPE',
    'TECHNISCHE_BRANDSCHUTZANLAGEN[].new_or_existing',
    'TECHNISCHE_BRANDSCHUTZANLAGEN[].type',
    'TODAY',
    'UEBERBAUUNGSORDNUNG',
    'UVP_JA_NEIN',
    'VENTILATION_SYSTEMS',
    'VENTILATION_SYSTEMS[]',
    'VENTILATION_SYSTEMS[].NEU_BESTEHEND',
    'VENTILATION_SYSTEMS[].NOUVEAU_OU_EXISTANT',
    'VENTILATION_SYSTEMS[].TYP',
    'VENTILATION_SYSTEMS[].TYPE',
    'VENTILATION_SYSTEMS[].VOLUMENSTROM',
    'VENTILATION_SYSTEMS[].VOLUME_D_AIR',
    'VENTILATION_SYSTEMS[].air_volume',
    'VENTILATION_SYSTEMS[].new_or_existing',
    'VENTILATION_SYSTEMS[].system_type',
    'VERTRAG',
    'VERTRAG_DATUM',
    'VERTRETER',
    'VERTRETER_ADDRESS_1',
    'VERTRETER_ADDRESS_2',
    'VERTRETER_ADRESSE_1',
    'VERTRETER_ADRESSE_2',
    'VERTRETER_NAME_ADDRESS',
    'VERTRETER_NAME_ADRESSE',
    'VERWALTUNGSKREIS',
    'VOISINS_TOUS',
    'VOISINS_TOUS[]',
    'VOISINS_TOUS[].ADDRESS_1',
    'VOISINS_TOUS[].ADDRESS_2',
    'VOISINS_TOUS[].ADRESSE_1',
    'VOISINS_TOUS[].ADRESSE_2',
    'VOISINS_TOUS[].NAME',
    'VOISINS_TOUS[].NOM',
    'WAERMETECHNISCHE_ANLAGEN',
    'WAERMETECHNISCHE_ANLAGEN[]',
    'WAERMETECHNISCHE_ANLAGEN[].BRENNSTOFFLAGERUNG',
    'WAERMETECHNISCHE_ANLAGEN[].LAGERMENGE',
    'WAERMETECHNISCHE_ANLAGEN[].LEISTUNG',
    'WAERMETECHNISCHE_ANLAGEN[].NEU_BESTEHEND',
    'WAERMETECHNISCHE_ANLAGEN[].NOUVEAU_OU_EXISTANT',
    'WAERMETECHNISCHE_ANLAGEN[].PUISSANCE',
    'WAERMETECHNISCHE_ANLAGEN[].QUANTITE_STOCKEE',
    'WAERMETECHNISCHE_ANLAGEN[].STOCKAGE_COMBUSTIBLE',
    'WAERMETECHNISCHE_ANLAGEN[].TYP',
    'WAERMETECHNISCHE_ANLAGEN[].TYPE',
    'WAERMETECHNISCHE_ANLAGEN[].combusitble_storage',
    'WAERMETECHNISCHE_ANLAGEN[].new_or_existing',
    'WAERMETECHNISCHE_ANLAGEN[].power',
    'WAERMETECHNISCHE_ANLAGEN[].storage_amount',
    'WAERMETECHNISCHE_ANLAGEN[].type',
    'ZIRKULATION_ALLE',
    'ZIRKULATION_ALLE[]',
    'ZIRKULATION_ALLE[].BEANTWORTET',
    'ZIRKULATION_ALLE[].CREE',
    'ZIRKULATION_ALLE[].DELAI',
    'ZIRKULATION_ALLE[].ERSTELLT',
    'ZIRKULATION_ALLE[].FRIST',
    'ZIRKULATION_ALLE[].NAME',
    'ZIRKULATION_ALLE[].NOM',
    'ZIRKULATION_ALLE[].REPONDU',
    'ZIRKULATION_FACHSTELLEN',
    'ZIRKULATION_FACHSTELLEN[]',
    'ZIRKULATION_FACHSTELLEN[].BEANTWORTET',
    'ZIRKULATION_FACHSTELLEN[].CREE',
    'ZIRKULATION_FACHSTELLEN[].DELAI',
    'ZIRKULATION_FACHSTELLEN[].ERSTELLT',
    'ZIRKULATION_FACHSTELLEN[].FRIST',
    'ZIRKULATION_FACHSTELLEN[].NAME',
    'ZIRKULATION_FACHSTELLEN[].NOM',
    'ZIRKULATION_FACHSTELLEN[].REPONDU',
    'ZIRKULATION_GEMEINDEN',
    'ZIRKULATION_GEMEINDEN[]',
    'ZIRKULATION_GEMEINDEN[].BEANTWORTET',
    'ZIRKULATION_GEMEINDEN[].CREE',
    'ZIRKULATION_GEMEINDEN[].DELAI',
    'ZIRKULATION_GEMEINDEN[].ERSTELLT',
    'ZIRKULATION_GEMEINDEN[].FRIST',
    'ZIRKULATION_GEMEINDEN[].NAME',
    'ZIRKULATION_GEMEINDEN[].NOM',
    'ZIRKULATION_GEMEINDEN[].REPONDU',
    'ZIRKULATION_RSTA',
    'ZIRKULATION_RSTA[]',
    'ZIRKULATION_RSTA[].BEANTWORTET',
    'ZIRKULATION_RSTA[].CREE',
    'ZIRKULATION_RSTA[].DELAI',
    'ZIRKULATION_RSTA[].ERSTELLT',
    'ZIRKULATION_RSTA[].FRIST',
    'ZIRKULATION_RSTA[].NAME',
    'ZIRKULATION_RSTA[].NOM',
    'ZIRKULATION_RSTA[].REPONDU',
    'ZIRKULATION_RUECKMELDUNGEN',
    'ZIRKULATION_RUECKMELDUNGEN[]',
    'ZIRKULATION_RUECKMELDUNGEN[].ANTWORT',
    'ZIRKULATION_RUECKMELDUNGEN[].DE',
    'ZIRKULATION_RUECKMELDUNGEN[].DISPOSITIONS_ACCESSOIRES',
    'ZIRKULATION_RUECKMELDUNGEN[].NEBENBESTIMMUNGEN',
    'ZIRKULATION_RUECKMELDUNGEN[].POINT_DE_VUE',
    'ZIRKULATION_RUECKMELDUNGEN[].REPONSE',
    'ZIRKULATION_RUECKMELDUNGEN[].STELLUNGNAHME',
    'ZIRKULATION_RUECKMELDUNGEN[].VON',
    'ZONE_PROTEGEE',
    'ZUSTAENDIG_EMAIL',
    'ZUSTAENDIG_NAME',
    'ZUSTAENDIG_PHONE',
    'ZUSTAENDIG_TELEFON'
]

snapshots['test_dms_placeholders_docs_available_placeholders[gr_dms_config] 1'] = [
    'ADDRESS',
    'ADRESSE',
    'ALLE_GESUCHSTELLER',
    'ALLE_GESUCHSTELLER_NAME_ADDRESS',
    'ALLE_GESUCHSTELLER_NAME_ADRESSE',
    'ALLE_GRUNDEIGENTUEMER',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADDRESS',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADRESSE',
    'ALLE_PROJEKTVERFASSER',
    'ALLE_PROJEKTVERFASSER_NAME_ADDRESS',
    'ALLE_PROJEKTVERFASSER_NAME_ADRESSE',
    'BASE_URL',
    'BAUEINGABE_DATUM',
    'BAUENTSCHEID',
    'BAUENTSCHEID_DATUM',
    'BEGINN_PUBLIKATIONSORGAN_GEMEINDE',
    'BEGINN_PUBLIKATION_KANTONSAMTSBLATT',
    'BESCHREIBUNG_BAUVORHABEN',
    'BESCHREIBUNG_PROJEKTAENDERUNG',
    'DECISION_DATE',
    'DESCRIPTION_MODIFICATION',
    'DOSSIER_NUMBER',
    'DOSSIER_NUMMER',
    'DOSSIER_TYP',
    'EBAU_URL',
    'EIGENE_NEBENBESTIMMUNGEN',
    'EIGENE_STELLUNGNAHMEN',
    'ENDE_PUBLIKATIONSORGAN_GEMEINDE',
    'ENDE_PUBLIKATION_GEMEINDE',
    'ENDE_PUBLIKATION_KANTON',
    'ENDE_PUBLIKATION_KANTONSAMTSBLATT',
    'ENTSCHEIDDOKUMENTE',
    'FACHSTELLEN_KANTONAL',
    'FACHSTELLEN_KANTONAL[]',
    'FACHSTELLEN_KANTONAL[].BEANTWORTET',
    'FACHSTELLEN_KANTONAL[].ERSTELLT',
    'FACHSTELLEN_KANTONAL[].FRIST',
    'FACHSTELLEN_KANTONAL[].NAME',
    'FOLGEPLANUNG',
    'FORM_NAME',
    'GEBAEUDEVERSICHERUNGSNUMMER',
    'GEMEINDE',
    'GEMEINDE_ADRESSE',
    'GEMEINDE_EMAIL',
    'GEMEINDE_NAME_ADRESSE',
    'GEMEINDE_ORT',
    'GEMEINDE_TELEFON',
    'GENERELLER_ERSCHLIESSUNGSPLAN',
    'GENERELLER_GESTALTUNGSPLAN',
    'GESUCHSTELLER',
    'GESUCHSTELLER_ADDRESS_1',
    'GESUCHSTELLER_ADDRESS_2',
    'GESUCHSTELLER_ADRESSE_1',
    'GESUCHSTELLER_ADRESSE_2',
    'GESUCHSTELLER_NAME_ADDRESS',
    'GESUCHSTELLER_NAME_ADRESSE',
    'GRUNDEIGENTUEMER',
    'GRUNDEIGENTUEMER_ADDRESS_1',
    'GRUNDEIGENTUEMER_ADDRESS_2',
    'GRUNDEIGENTUEMER_ADRESSE_1',
    'GRUNDEIGENTUEMER_ADRESSE_2',
    'GRUNDEIGENTUEMER_NAME_ADDRESS',
    'GRUNDEIGENTUEMER_NAME_ADRESSE',
    'HEUTE',
    'ID',
    'INSTANCE_ID',
    'JURISTIC_NAME',
    'JURISTISCHER_NAME',
    'KOORDINATEN',
    'LANGUAGE',
    'LEITBEHOERDE_ADDRESS_1',
    'LEITBEHOERDE_ADDRESS_2',
    'LEITBEHOERDE_ADRESSE_1',
    'LEITBEHOERDE_ADRESSE_2',
    'LEITBEHOERDE_CITY',
    'LEITBEHOERDE_EMAIL',
    'LEITBEHOERDE_NAME',
    'LEITBEHOERDE_NAME_KURZ',
    'LEITBEHOERDE_PHONE',
    'LEITBEHOERDE_STADT',
    'LEITBEHOERDE_TELEFON',
    'MEINE_ORGANISATION_ADRESSE_1',
    'MEINE_ORGANISATION_ADRESSE_2',
    'MEINE_ORGANISATION_EMAIL',
    'MEINE_ORGANISATION_NAME',
    'MEINE_ORGANISATION_NAME_ADRESSE',
    'MEINE_ORGANISATION_NAME_KURZ',
    'MEINE_ORGANISATION_ORT',
    'MEINE_ORGANISATION_TELEFON',
    'MUNICIPALITY',
    'MUNICIPALITY_ADDRESS',
    'NAME',
    'NEBENBESTIMMUNGEN',
    'NEBENBESTIMMUNGEN_MAPPED',
    'NEBENBESTIMMUNGEN_MAPPED[]',
    'NEBENBESTIMMUNGEN_MAPPED[].FACHSTELLE',
    'NEBENBESTIMMUNGEN_MAPPED[].TEXT',
    'PARZELLE',
    'PROJEKTVERFASSER',
    'PROJEKTVERFASSER_ADDRESS_1',
    'PROJEKTVERFASSER_ADDRESS_2',
    'PROJEKTVERFASSER_ADRESSE_1',
    'PROJEKTVERFASSER_ADRESSE_2',
    'PROJEKTVERFASSER_NAME_ADDRESS',
    'PROJEKTVERFASSER_NAME_ADRESSE',
    'PUBLIKATION_LINK',
    'PUBLIKATION_TEXT',
    'SPRACHE',
    'START_PUBLIKATION_GEMEINDE',
    'START_PUBLIKATION_KANTON',
    'STATUS',
    'STELLUNGNAHME',
    'TODAY',
    'ZIRKULATION_ALLE',
    'ZIRKULATION_ALLE[]',
    'ZIRKULATION_ALLE[].BEANTWORTET',
    'ZIRKULATION_ALLE[].ERSTELLT',
    'ZIRKULATION_ALLE[].FRIST',
    'ZIRKULATION_ALLE[].NAME',
    'ZIRKULATION_FACHSTELLEN',
    'ZIRKULATION_FACHSTELLEN[]',
    'ZIRKULATION_FACHSTELLEN[].BEANTWORTET',
    'ZIRKULATION_FACHSTELLEN[].ERSTELLT',
    'ZIRKULATION_FACHSTELLEN[].FRIST',
    'ZIRKULATION_FACHSTELLEN[].NAME',
    'ZIRKULATION_GEMEINDEN',
    'ZIRKULATION_GEMEINDEN[]',
    'ZIRKULATION_GEMEINDEN[].BEANTWORTET',
    'ZIRKULATION_GEMEINDEN[].ERSTELLT',
    'ZIRKULATION_GEMEINDEN[].FRIST',
    'ZIRKULATION_GEMEINDEN[].NAME',
    'ZIRKULATION_RUECKMELDUNGEN',
    'ZIRKULATION_RUECKMELDUNGEN[]',
    'ZIRKULATION_RUECKMELDUNGEN[].ANTWORT',
    'ZIRKULATION_RUECKMELDUNGEN[].NEBENBESTIMMUNGEN',
    'ZIRKULATION_RUECKMELDUNGEN[].STELLUNGNAHME',
    'ZIRKULATION_RUECKMELDUNGEN[].VON',
    'ZONENPLAN',
    'ZUSTAENDIG_NAME'
]

snapshots['test_dms_placeholders_docs_available_placeholders[so_dms_config] 1'] = [
    'ALLE_BAUHERREN',
    'ALLE_BAUHERREN_NAME_ADRESSE',
    'ALLE_GESUCHSTELLER',
    'ALLE_GESUCHSTELLER_NAME_ADDRESS',
    'ALLE_GRUNDEIGENTUEMER',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADDRESS',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADRESSE',
    'ALLE_PROJEKTVERFASSER',
    'ALLE_PROJEKTVERFASSER_NAME_ADDRESS',
    'ALLE_PROJEKTVERFASSER_NAME_ADRESSE',
    'BASE_URL',
    'BAUEINGABE_DATUM',
    'BAUENTSCHEID_DATUM',
    'BAUHERR',
    'BAUHERR_ADRESSE_1',
    'BAUHERR_ADRESSE_2',
    'BAUHERR_NAME_ADRESSE',
    'BESCHREIBUNG_BAUVORHABEN',
    'DECISION_DATE',
    'DOSSIER_NUMBER',
    'DOSSIER_NUMMER',
    'DOSSIER_TYP',
    'EBAU_URL',
    'EIGENE_GEBUEHREN',
    'EIGENE_GEBUEHREN[]',
    'EIGENE_GEBUEHREN[].BETRAG',
    'EIGENE_GEBUEHREN[].POSITION',
    'EIGENE_GEBUEHREN_TOTAL',
    'FACHSTELLEN_KANTONAL',
    'FACHSTELLEN_KANTONAL[]',
    'FACHSTELLEN_KANTONAL[].BEANTWORTET',
    'FACHSTELLEN_KANTONAL[].ERSTELLT',
    'FACHSTELLEN_KANTONAL[].FRIST',
    'FACHSTELLEN_KANTONAL[].NAME',
    'FORM_NAME',
    'GEBUEHREN',
    'GEBUEHREN[]',
    'GEBUEHREN[].BETRAG',
    'GEBUEHREN[].POSITION',
    'GEBUEHREN_TOTAL',
    'GEMEINDE',
    'GEMEINDE_ADRESSE',
    'GEMEINDE_EMAIL',
    'GEMEINDE_NAME_ADRESSE',
    'GEMEINDE_ORT',
    'GEMEINDE_TELEFON',
    'GESUCHSTELLER',
    'GESUCHSTELLER_ADDRESS_1',
    'GESUCHSTELLER_ADDRESS_2',
    'GESUCHSTELLER_NAME_ADDRESS',
    'GRUNDEIGENTUEMER',
    'GRUNDEIGENTUEMER_ADDRESS_1',
    'GRUNDEIGENTUEMER_ADDRESS_2',
    'GRUNDEIGENTUEMER_ADRESSE_1',
    'GRUNDEIGENTUEMER_ADRESSE_2',
    'GRUNDEIGENTUEMER_NAME_ADDRESS',
    'GRUNDEIGENTUEMER_NAME_ADRESSE',
    'HEUTE',
    'JURISTIC_NAME',
    'JURISTISCHER_NAME',
    'KOORDINATEN',
    'LEITBEHOERDE_ADDRESS_1',
    'LEITBEHOERDE_ADDRESS_2',
    'LEITBEHOERDE_ADRESSE_1',
    'LEITBEHOERDE_ADRESSE_2',
    'LEITBEHOERDE_CITY',
    'LEITBEHOERDE_EMAIL',
    'LEITBEHOERDE_NAME',
    'LEITBEHOERDE_NAME_KURZ',
    'LEITBEHOERDE_PHONE',
    'LEITBEHOERDE_STADT',
    'LEITBEHOERDE_TELEFON',
    'MEINE_ORGANISATION_ADRESSE_1',
    'MEINE_ORGANISATION_ADRESSE_2',
    'MEINE_ORGANISATION_EMAIL',
    'MEINE_ORGANISATION_NAME',
    'MEINE_ORGANISATION_NAME_ADRESSE',
    'MEINE_ORGANISATION_NAME_KURZ',
    'MEINE_ORGANISATION_ORT',
    'MEINE_ORGANISATION_TELEFON',
    'MUNICIPALITY',
    'MUNICIPALITY_ADDRESS',
    'NAME',
    'NEBENBESTIMMUNGEN_MAPPED',
    'NEBENBESTIMMUNGEN_MAPPED[]',
    'NEBENBESTIMMUNGEN_MAPPED[].FACHSTELLE',
    'NEBENBESTIMMUNGEN_MAPPED[].TEXT',
    'PARZELLE',
    'PROJEKTVERFASSER',
    'PROJEKTVERFASSER_ADDRESS_1',
    'PROJEKTVERFASSER_ADDRESS_2',
    'PROJEKTVERFASSER_ADRESSE_1',
    'PROJEKTVERFASSER_ADRESSE_2',
    'PROJEKTVERFASSER_NAME_ADDRESS',
    'PROJEKTVERFASSER_NAME_ADRESSE',
    'PUBLIKATION_LINK',
    'STATUS',
    'TODAY',
    'ZIRKULATION_ALLE',
    'ZIRKULATION_ALLE[]',
    'ZIRKULATION_ALLE[].BEANTWORTET',
    'ZIRKULATION_ALLE[].ERSTELLT',
    'ZIRKULATION_ALLE[].FRIST',
    'ZIRKULATION_ALLE[].NAME',
    'ZIRKULATION_FACHSTELLEN',
    'ZIRKULATION_FACHSTELLEN[]',
    'ZIRKULATION_FACHSTELLEN[].BEANTWORTET',
    'ZIRKULATION_FACHSTELLEN[].ERSTELLT',
    'ZIRKULATION_FACHSTELLEN[].FRIST',
    'ZIRKULATION_FACHSTELLEN[].NAME',
    'ZIRKULATION_GEMEINDEN',
    'ZIRKULATION_GEMEINDEN[]',
    'ZIRKULATION_GEMEINDEN[].BEANTWORTET',
    'ZIRKULATION_GEMEINDEN[].ERSTELLT',
    'ZIRKULATION_GEMEINDEN[].FRIST',
    'ZIRKULATION_GEMEINDEN[].NAME'
]

snapshots['test_dms_placeholders_empty[Municipality] 1'] = {
    'ACE': '',
    'ADDRESS': '',
    'ADMINISTRATIVE_DISTRICT': '',
    'ADRESSE': '',
    'AFFECTATION': '',
    'AFFECTATION_ZONE': '',
    'ALCOHOL_SERVING': '',
    'ALKOHOLAUSSCHANK': '',
    'ALLE_GEBAEUDEEIGENTUEMER': '',
    'ALLE_GEBAEUDEEIGENTUEMER_NAME_ADDRESS': '',
    'ALLE_GEBAEUDEEIGENTUEMER_NAME_ADRESSE': '',
    'ALLE_GESUCHSTELLER': '',
    'ALLE_GESUCHSTELLER_NAME_ADDRESS': '',
    'ALLE_GESUCHSTELLER_NAME_ADRESSE': '',
    'ALLE_GRUNDEIGENTUEMER': '',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADDRESS': '',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADRESSE': '',
    'ALLE_NACHBARN': [
    ],
    'ALLE_PROJEKTVERFASSER': '',
    'ALLE_PROJEKTVERFASSER_NAME_ADDRESS': '',
    'ALLE_PROJEKTVERFASSER_NAME_ADRESSE': '',
    'ALLE_VERTRETER': '',
    'ALLE_VERTRETER_NAME_ADDRESS': '',
    'ALLE_VERTRETER_NAME_ADRESSE': '',
    'ANZAHL_BEHERBERGTE_PERSONEN': '',
    'ARRONDISSEMENT_ADMINISTRATIF': '',
    'ASCENSEURS': [
    ],
    'AUFZUGSANLAGEN': [
    ],
    'AUJOURD_HUI': '30. August 2021',
    'AUTEUR_PROJET': '',
    'AUTEUR_PROJET_ADRESSE_1': '',
    'AUTEUR_PROJET_ADRESSE_2': '',
    'AUTEUR_PROJET_NOM_ADRESSE': '',
    'AUTEUR_PROJET_TOUS': '',
    'AUTEUR_PROJET_TOUS_NOM_ADRESSE': '',
    'AUTORITE_DIRECTRICE_ADRESSE_1': '',
    'AUTORITE_DIRECTRICE_ADRESSE_2': '',
    'AUTORITE_DIRECTRICE_EMAIL': 'michelleboone@example.org',
    'AUTORITE_DIRECTRICE_LIEU': '',
    'AUTORITE_DIRECTRICE_NOM': 'Alex Smith',
    'AUTORITE_DIRECTRICE_NOM_ABR': 'Alex Smith',
    'AUTORITE_DIRECTRICE_TELEPHONE': '',
    'BASE_URL': 'http://ebau.local',
    'BAUEINGABE_DATUM': '30. August 2021',
    'BAUENTSCHEID': '',
    'BAUENTSCHEID_BAUABSCHLAG': '',
    'BAUENTSCHEID_BAUABSCHLAG_MIT_WHST': '',
    'BAUENTSCHEID_BAUABSCHLAG_OHNE_WHST': '',
    'BAUENTSCHEID_BAUBEWILLIGUNG': '',
    'BAUENTSCHEID_BAUBEWILLIGUNGSFREI': '',
    'BAUENTSCHEID_DATUM': '',
    'BAUENTSCHEID_GENERELL': '',
    'BAUENTSCHEID_GESAMT': '',
    'BAUENTSCHEID_KLEIN': '',
    'BAUENTSCHEID_POSITIV': '',
    'BAUENTSCHEID_POSITIV_TEILWEISE': '',
    'BAUENTSCHEID_PROJEKTAENDERUNG': '',
    'BAUENTSCHEID_TEILBAUBEWILLIGUNG': '',
    'BAUENTSCHEID_TYP': '',
    'BAUENTSCHEID_TYPE': '',
    'BAUGRUPPE': '',
    'BAUGRUPPE_BEZEICHNUNG': '',
    'BAUKOSTEN': '',
    'BAUVORHABEN': '',
    'BESCHREIBUNG_BAUVORHABEN': '',
    'BESCHREIBUNG_PROJEKTAENDERUNG': '',
    'BOISSONS_ALCOOLIQUES': '',
    'BUILDING_DISTANCES': [
    ],
    'CHAMBRES_AVEC_PLUS_DE_50_PERSONNES': [
    ],
    'CIRCULATION_COMMUNES': [
    ],
    'CIRCULATION_PREAVIS': [
    ],
    'CIRCULATION_PREF': [
    ],
    'CIRCULATION_SERVICES': [
    ],
    'COMMUNE': '',
    'COMMUNE_ADRESSE': '',
    'COMMUNE_ADRESSE_1': '',
    'COMMUNE_ADRESSE_2': '',
    'COMMUNE_EMAIL': '',
    'COMMUNE_LIEU': '',
    'COMMUNE_NOM_ADRESSE': '',
    'COMMUNE_TELEPHONE': '',
    'COMMUNICATION_AUX_VOISINS_CODE_QR': '',
    'COMMUNICATION_AUX_VOISINS_LIEN': '',
    'CONSERVABLE': '',
    'CONSTRUCTION_COSTS': '',
    'CONSTRUCTION_GROUP': '',
    'CONSTRUCTION_GROUP_DESIGNATION': '',
    'CONTRACT': '',
    'CONTRACT_START': '',
    'CONTRAT': '',
    'CONTRAT_DATE': '',
    'COORDONEE': '',
    'COUTS_DE_CONSTRUCTION': '',
    'DECISION': '',
    'DECISION_CATEGORIE': '',
    'DECISION_DATE': '',
    'DECISION_GENERAL': '',
    'DECISION_GLOBALE': '',
    'DECISION_MODIF': '',
    'DECISION_PARTIEL': '',
    'DECISION_PERMIS': '',
    'DECISION_PETIT': '',
    'DECISION_POSITIVE': '',
    'DECISION_POSITIVE_PARTIEL': '',
    'DECISION_REFUS': '',
    'DECISION_REFUS_AVEC_RET': '',
    'DECISION_REFUS_SANS_RET': '',
    'DECISION_TYPE': '',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES': [
    ],
    'DEPOT_DEMANDE_DATE': '30. August 2021',
    'DESCRIPTION_MODIFICATION': '',
    'DIMENSIONEN_HOEHE': '',
    'DIMENSION_HAUTEUR': '',
    'DIMENSION_HEIGHT': '',
    'DISPOSITIONS_ACCESSOIRES': '',
    'DISPOSITIONS_ANNEXES': '',
    'DISTANCES_ENTRE_LES_BATIMENTS': [
    ],
    'DOSSIER_LINK': 'http://ebau.local/index/redirect-to-instance-resource/instance-id/1',
    'DOSSIER_NR': 1,
    'DOSSIER_NUMERO': 1,
    'DOSSIER_TYP': 'Baugesuch',
    'DOSSIER_TYPE': 'Baugesuch',
    'EBAU_NR': '',
    'EBAU_NUMBER': '',
    'EBAU_NUMERO': '',
    'EBAU_URL': 'http://ebau.local',
    'EIGENE_GEBUEHREN': [
    ],
    'EIGENE_GEBUEHREN_TOTAL': '0.00',
    'EIGENE_NEBENBESTIMMUNGEN': '',
    'EIGENE_STELLUNGNAHMEN': '',
    'EINSPRACHEN': [
    ],
    'EINSPRECHENDE': [
    ],
    'EMAIL': '',
    'EMOLUMENTS': [
    ],
    'EMOLUMENTS_TOTAL': '0.00',
    'ENSEMBLE_BÂTI': '',
    'ENSEMBLE_BÂTI_DÉNOMINATION': '',
    'ERHALTENSWERT': '',
    'ETAT': 'David Rangel',
    'FACHSTELLEN_KANTONAL': [
    ],
    'FACHSTELLEN_KANTONAL_LIST': '',
    'FACHSTELLEN_KANTONAL_LISTE': '',
    'FIRE_PROTECTION_SYSTEMS': [
    ],
    'FLOOR_AREA': '',
    'FORM_NAME': 'Baugesuch',
    'GEBAEUDEABSTAENDE': [
    ],
    'GEBAEUDEEIGENTUEMER': '',
    'GEBAEUDEEIGENTUEMER_ADDRESS_1': '',
    'GEBAEUDEEIGENTUEMER_ADDRESS_2': '',
    'GEBAEUDEEIGENTUEMER_ADRESSE_1': '',
    'GEBAEUDEEIGENTUEMER_ADRESSE_2': '',
    'GEBAEUDEEIGENTUEMER_NAME_ADDRESS': '',
    'GEBAEUDEEIGENTUEMER_NAME_ADRESSE': '',
    'GEBUEHREN': [
    ],
    'GEBUEHREN_TOTAL': '0.00',
    'GEFAEHRLICHE_STOFFE': [
    ],
    'GEMEINDE': '',
    'GEMEINDE_ADRESSE': '',
    'GEMEINDE_ADRESSE_1': '',
    'GEMEINDE_ADRESSE_2': '',
    'GEMEINDE_EMAIL': '',
    'GEMEINDE_NAME_ADRESSE': '',
    'GEMEINDE_ORT': '',
    'GEMEINDE_TELEFON': '',
    'GESCHOSSFLAECHE': '',
    'GESUCHSTELLER': '',
    'GESUCHSTELLER_ADDRESS_1': '',
    'GESUCHSTELLER_ADDRESS_2': '',
    'GESUCHSTELLER_ADRESSE_1': '',
    'GESUCHSTELLER_ADRESSE_2': '',
    'GESUCHSTELLER_NAME_ADDRESS': '',
    'GESUCHSTELLER_NAME_ADRESSE': '',
    'GEWAESSERSCHUTZBEREICH': '',
    'GRUNDEIGENTUEMER': '',
    'GRUNDEIGENTUEMER_ADDRESS_1': '',
    'GRUNDEIGENTUEMER_ADDRESS_2': '',
    'GRUNDEIGENTUEMER_ADRESSE_1': '',
    'GRUNDEIGENTUEMER_ADRESSE_2': '',
    'GRUNDEIGENTUEMER_NAME_ADDRESS': '',
    'GRUNDEIGENTUEMER_NAME_ADRESSE': '',
    'HAZARDOUS_SUBSTANCES': [
    ],
    'HEATING_SYSTEMS': [
    ],
    'HEUTE': '30. August 2021',
    'INFORMATION_OF_NEIGHBORS_LINK': '',
    'INFORMATION_OF_NEIGHBORS_QR_CODE': '',
    'INSTALLATIONS_AERAULIQUES': [
    ],
    'INSTALLATIONS_TECH_LINCENDIE': [
    ],
    'INSTANCE_ID': 1,
    'INTERIOR_SEATING': '',
    'INVENTAR': '',
    'JURISTIC_NAME': '',
    'JURISTISCHER_NAME': '',
    'KOORDINATEN': '',
    'K_OBJECT': '',
    'K_OBJEKT': '',
    'LANGUAGE': 'de',
    'LANGUE': 'de',
    'LASTENAUSGLEICHSBEGEHREN': [
    ],
    'LASTENAUSGLEICHSBEGEHRENDE': [
    ],
    'LEGAL_CLAIMANTS': [
    ],
    'LEGAL_CUSTODIANS': [
    ],
    'LEITBEHOERDE_ADDRESS_1': '',
    'LEITBEHOERDE_ADDRESS_2': '',
    'LEITBEHOERDE_ADRESSE_1': '',
    'LEITBEHOERDE_ADRESSE_2': '',
    'LEITBEHOERDE_CITY': '',
    'LEITBEHOERDE_EMAIL': 'michelleboone@example.org',
    'LEITBEHOERDE_NAME': 'Alex Smith',
    'LEITBEHOERDE_NAME_KURZ': 'Alex Smith',
    'LEITBEHOERDE_PHONE': '',
    'LEITBEHOERDE_STADT': '',
    'LEITBEHOERDE_TELEFON': '',
    'LEITPERSON': '',
    'LIEN_PUBLICATION': 'http://ebau-portal.local/public-instances/1',
    'LIFTS': [
    ],
    'LOAD_COMPENSATION_REQUESTING': [
    ],
    'LUEFTUNGSANLAGEN': [
    ],
    'MATIERES_DANGEREUSES': [
    ],
    'MEINE_ORGANISATION_ADRESSE_1': '',
    'MEINE_ORGANISATION_ADRESSE_2': '',
    'MEINE_ORGANISATION_EMAIL': 'michelleboone@example.org',
    'MEINE_ORGANISATION_NAME': 'Alex Smith',
    'MEINE_ORGANISATION_NAME_ADRESSE': 'Alex Smith',
    'MEINE_ORGANISATION_NAME_KURZ': 'Alex Smith',
    'MEINE_ORGANISATION_ORT': '',
    'MEINE_ORGANISATION_TELEFON': '',
    'MES_EMOLUMENTS': [
    ],
    'MES_EMOLUMENTS_TOTAL': '0.00',
    'MODIFICATION_DATE': '',
    'MODIFICATION_TIME': '',
    'MON_ORGANISATION_ADRESSE_1': '',
    'MON_ORGANISATION_ADRESSE_2': '',
    'MON_ORGANISATION_EMAIL': 'michelleboone@example.org',
    'MON_ORGANISATION_LIEU': '',
    'MON_ORGANISATION_NOM': 'Alex Smith',
    'MON_ORGANISATION_NOM_ABR': 'Alex Smith',
    'MON_ORGANISATION_NOM_ADRESSE': 'Alex Smith',
    'MON_ORGANISATION_TELEPHONE': '',
    'MOTS_CLES': '',
    'MUNICIPALITY': '',
    'MUNICIPALITY_ADDRESS': '',
    'NACHBARSCHAFTSORIENTIERUNG_LINK': '',
    'NACHBARSCHAFTSORIENTIERUNG_QR_CODE': '',
    'NAME': '',
    'NEBENBESTIMMUNGEN': '',
    'NEBENBESTIMMUNGEN_MAPPED': [
    ],
    'NEIGHBORS': [
    ],
    'NOMBRE_DE_PERSONNES_ACCOMPAGNEES': '',
    'NOM_LEGAL': '',
    'NUMBER_OF_ACCOMODATED_PERSONS': '',
    'NUTZUNG': '',
    'NUTZUNGSZONE': '',
    'OBJECTIONS': [
    ],
    'OBJECT_C': '',
    'OCCUPATION_CHAMBRES_PLUS_50_PERSONNES': '',
    'OEFFENTLICHKEIT': '',
    'OFFICES_CANTONAUX': [
    ],
    'OFFICES_CANTONAUX_LISTE': '',
    'OPPOSANTS': [
    ],
    'OPPOSING': [
    ],
    'OPPOSITIONS': [
    ],
    'OUTSIDE_SEATING': '',
    'OUVERTURE_PUBLIC': '',
    'PANNEAUX_SOLAIRES': [
    ],
    'PARCELLE': '',
    'PARZELLE': '',
    'PLACES_ASSISES_EXT': '',
    'PLACES_ASSISES_INT': '',
    'PLAN_QUARTIER': '',
    'POINT_DE_VUE': '',
    'PRISE_DE_POSITION': '',
    'PROJEKTVERFASSER': '',
    'PROJEKTVERFASSER_ADDRESS_1': '',
    'PROJEKTVERFASSER_ADDRESS_2': '',
    'PROJEKTVERFASSER_ADRESSE_1': '',
    'PROJEKTVERFASSER_ADRESSE_2': '',
    'PROJEKTVERFASSER_NAME_ADDRESS': '',
    'PROJEKTVERFASSER_NAME_ADRESSE': '',
    'PROJET_CONSTR': '',
    'PROJET_CONSTR_DESCR': '',
    'PROPRIETAIRE_FONC': '',
    'PROPRIETAIRE_FONC_ADRESSE_1': '',
    'PROPRIETAIRE_FONC_ADRESSE_2': '',
    'PROPRIETAIRE_FONC_NOM_ADRESSE': '',
    'PROPRIETAIRE_FONC_TOUS': '',
    'PROPRIETAIRE_FONC_TOUS_NOM_ADRESSE': '',
    'PROPRIETAIRE_IMMOB': '',
    'PROPRIETAIRE_IMMOB_ADRESSE_1': '',
    'PROPRIETAIRE_IMMOB_ADRESSE_2': '',
    'PROPRIETAIRE_IMMOB_NOM_ADRESSE': '',
    'PROPRIETAIRE_IMMOB_TOUS': '',
    'PROPRIETAIRE_IMMOB_TOUS_NOM_ADRESSE': '',
    'PROTECTED': '',
    'PROTECTION_AREA': '',
    'PROTÉGÉ': '',
    'PUBLIC': '',
    'PUBLICATION_1_FEUILLE_AVIS': '',
    'PUBLICATION_2_FEUILLE_AVIS': '',
    'PUBLICATION_DEBUT': '',
    'PUBLICATION_EXPIRATION': '',
    'PUBLICATION_FEUILLE_AVIS_NOM': '',
    'PUBLICATION_FEUILLE_OFFICIELLE': '',
    'PUBLICATION_TEXTE': '',
    'PUBLIKATION_1_ANZEIGER': '',
    'PUBLIKATION_2_ANZEIGER': '',
    'PUBLIKATION_AMTSBLATT': '',
    'PUBLIKATION_ANZEIGER_NAME': '',
    'PUBLIKATION_ENDE': '',
    'PUBLIKATION_LINK': 'http://ebau-portal.local/public-instances/1',
    'PUBLIKATION_START': '',
    'PUBLIKATION_TEXT': '',
    'QS_RESPONSIBLE': '',
    'QS_VERANTWORTLICHER': '',
    'RAEUME_MEHR_50_PERSONEN': [
    ],
    'RAUM_BELEGUNG_MEHR_50_PERSONEN': '',
    'RECENSEMENT': '',
    'RECHTSBEGEHRENDE': [
    ],
    'RECHTSVERWAHRENDE': [
    ],
    'RECHTSVERWAHRUNGEN': [
    ],
    'REPRESENTANT': '',
    'REPRESENTANT_ADRESSE_1': '',
    'REPRESENTANT_ADRESSE_2': '',
    'REPRESENTANT_NOM_ADRESSE': '',
    'REPRESENTANT_TOUS': '',
    'REPRESENTANT_TOUS_NOM_ADRESSE': '',
    'REQUERANT': '',
    'REQUERANTS_COMPENSATION_DES_CHARGES': [
    ],
    'REQUERANTS_CONCLUSIONS': [
    ],
    'REQUERANTS_RESERVE_DE_DROIT': [
    ],
    'REQUERANT_ADRESSE_1': '',
    'REQUERANT_ADRESSE_2': '',
    'REQUERANT_NOM_ADRESSE': '',
    'REQUERANT_TOUS': '',
    'REQUERANT_TOUS_NOM_ADRESSE': '',
    'RESERVES_DE_DROIT': [
    ],
    'RESPONSABLE_AUTORITE_DIRECTRICE': '',
    'RESPONSABLE_EMAIL': '',
    'RESPONSABLE_NOM': '',
    'RESPONSABLE_TELEPHONE': '',
    'ROOMS_WITH_MORE_THAN_50_PERSONS': [
    ],
    'ROOM_OCCUPANCY_ROOMS_MORE_THAN_50_PERSONS': '',
    'RRB': '',
    'RRB_DATE': '',
    'RRB_DATUM': '',
    'RRB_START': '',
    'SACHVERHALT': '',
    'SCHUTZZONE': '',
    'SCHÜTZENSWERT': '',
    'SECTEUR_PROTECTION_EAUX': '',
    'SITUATION': '',
    'SITZPLAETZE_AUSSEN': '',
    'SITZPLAETZE_INNEN': '',
    'SOLARANLAGEN': [
    ],
    'SOLAR_PANELS': [
    ],
    'SPRACHE': 'de',
    'STATUS': 'David Rangel',
    'STELLUNGNAHME': '',
    'STFV_CRITIAL_VALUE_EXCEEDED': '',
    'STFV_DATE_DU_RAPPORT_COURT': '',
    'STFV_KRITISCHER_WERT_UEBERSCHRITTEN': '',
    'STFV_KURZ_BERICHT_DATUM': '',
    'STFV_SHORT_REPORT_DATE': '',
    'STFV_VALEUR_CRITIQUE_DEPASSEE': '',
    'STICHWORTE': '',
    'SURFACE_DE_PLANCHER': '',
    'SYSTEMES_DE_VENTILATION': [
    ],
    'TECHNISCHE_BRANDSCHUTZANLAGEN': [
    ],
    'TODAY': '30. August 2021',
    'UEBERBAUUNGSORDNUNG': '',
    'UVP_JA_NEIN': False,
    'VENTILATION_SYSTEMS': [
    ],
    'VERTRAG': '',
    'VERTRAG_DATUM': '',
    'VERTRETER': '',
    'VERTRETER_ADDRESS_1': '',
    'VERTRETER_ADDRESS_2': '',
    'VERTRETER_ADRESSE_1': '',
    'VERTRETER_ADRESSE_2': '',
    'VERTRETER_NAME_ADDRESS': '',
    'VERTRETER_NAME_ADRESSE': '',
    'VERWALTUNGSKREIS': '',
    'VOISINS_TOUS': [
    ],
    'WAERMETECHNISCHE_ANLAGEN': [
    ],
    'ZIRKULATION_ALLE': [
    ],
    'ZIRKULATION_FACHSTELLEN': [
    ],
    'ZIRKULATION_GEMEINDEN': [
    ],
    'ZIRKULATION_RSTA': [
    ],
    'ZIRKULATION_RUECKMELDUNGEN': [
    ],
    'ZONE_PROTEGEE': '',
    'ZUSTAENDIG_EMAIL': '',
    'ZUSTAENDIG_NAME': '',
    'ZUSTAENDIG_PHONE': '',
    'ZUSTAENDIG_TELEFON': ''
}

snapshots['test_dms_placeholders_gr[Municipality] 1'] = {
    'ADDRESS': 'Teststrasse 12, Testhausen',
    'ADRESSE': 'Teststrasse 12, Testhausen',
    'ALLE_GESUCHSTELLER': 'Test AG, Esther Tester',
    'ALLE_GESUCHSTELLER_NAME_ADDRESS': 'Test AG, Esther Tester, Testweg 321, 4321 Testingen',
    'ALLE_GESUCHSTELLER_NAME_ADRESSE': 'Test AG, Esther Tester, Testweg 321, 4321 Testingen',
    'ALLE_GRUNDEIGENTUEMER': 'Sandra Beispiel',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADDRESS': 'Sandra Beispiel, Beispielstrasse 16, 2222 Beispieldorf',
    'ALLE_GRUNDEIGENTUEMER_NAME_ADRESSE': 'Sandra Beispiel, Beispielstrasse 16, 2222 Beispieldorf',
    'ALLE_PROJEKTVERFASSER': 'Hans Muster',
    'ALLE_PROJEKTVERFASSER_NAME_ADDRESS': 'Hans Muster, Bahnhofstrasse 3, 3600 Thun',
    'ALLE_PROJEKTVERFASSER_NAME_ADRESSE': 'Hans Muster, Bahnhofstrasse 3, 3600 Thun',
    'BASE_URL': 'http://ember-ebau.local',
    'BAUEINGABE_DATUM': '31. März 2021',
    'BAUENTSCHEID': 'Bewilligt',
    'BAUENTSCHEID_DATUM': '30. August 2021',
    'BEGINN_PUBLIKATIONSORGAN_GEMEINDE': '20. August 2021',
    'BEGINN_PUBLIKATION_KANTONSAMTSBLATT': '22. August 2021',
    'BESCHREIBUNG_BAUVORHABEN': 'Einfamilienhaus',
    'BESCHREIBUNG_PROJEKTAENDERUNG': 'Projektänderung',
    'DECISION_DATE': '30. August 2021',
    'DESCRIPTION_MODIFICATION': 'Projektänderung',
    'DOSSIER_NUMBER': '2023-1',
    'DOSSIER_NUMMER': '2023-1',
    'DOSSIER_TYP': 'Baugesuch',
    'EBAU_URL': 'http://ember-ebau.local',
    'EIGENE_NEBENBESTIMMUNGEN': '',
    'EIGENE_STELLUNGNAHMEN': '',
    'ENDE_PUBLIKATIONSORGAN_GEMEINDE': '21. August 2021',
    'ENDE_PUBLIKATION_GEMEINDE': '21. August 2021',
    'ENDE_PUBLIKATION_KANTON': '23. August 2021',
    'ENDE_PUBLIKATION_KANTONSAMTSBLATT': '23. August 2021',
    'ENTSCHEIDDOKUMENTE': 'Grundriss (eingereicht als Situationsplan) am 30.08.2021 um 00:00',
    'FACHSTELLEN_KANTONAL': [
        {
            'BEANTWORTET': '',
            'ERSTELLT': '30.08.2021',
            'FRIST': '26.01.2015',
            'NAME': 'Dillon Peterson'
        },
        {
            'BEANTWORTET': '',
            'ERSTELLT': '30.08.2021',
            'FRIST': '19.12.1991',
            'NAME': 'Christopher Gonzalez'
        },
        {
            'BEANTWORTET': '',
            'ERSTELLT': '30.08.2021',
            'FRIST': '25.07.1995',
            'NAME': 'Susan Gonzalez'
        },
        {
            'BEANTWORTET': '',
            'ERSTELLT': '30.08.2021',
            'FRIST': '23.03.1972',
            'NAME': 'Steven Davis'
        },
        {
            'BEANTWORTET': '26.04.2001',
            'ERSTELLT': '30.08.2021',
            'FRIST': '08.01.2016',
            'NAME': 'Gloria Jenkins'
        },
        {
            'BEANTWORTET': '04.03.2000',
            'ERSTELLT': '30.08.2021',
            'FRIST': '07.02.2012',
            'NAME': 'Jessica Hutchinson'
        }
    ],
    'FOLGEPLANUNG': 'Baulinie allgemein',
    'FORM_NAME': 'Baugesuch',
    'GEBAEUDEVERSICHERUNGSNUMMER': '123456789, 987654321',
    'GEMEINDE': 'Robert Li',
    'GEMEINDE_ADRESSE': '',
    'GEMEINDE_EMAIL': 'froach@example.com',
    'GEMEINDE_NAME_ADRESSE': 'Gemeinde Robert Li',
    'GEMEINDE_ORT': '',
    'GEMEINDE_TELEFON': '',
    'GENERELLER_ERSCHLIESSUNGSPLAN': 'Fuss- / Spazierweg, Parkierung Gebiete D',
    'GENERELLER_GESTALTUNGSPLAN': 'Historischer Weg',
    'GESUCHSTELLER': 'Test AG, Esther Tester',
    'GESUCHSTELLER_ADDRESS_1': 'Testweg 321',
    'GESUCHSTELLER_ADDRESS_2': '4321 Testingen',
    'GESUCHSTELLER_ADRESSE_1': 'Testweg 321',
    'GESUCHSTELLER_ADRESSE_2': '4321 Testingen',
    'GESUCHSTELLER_NAME_ADDRESS': 'Test AG, Esther Tester, Testweg 321, 4321 Testingen',
    'GESUCHSTELLER_NAME_ADRESSE': 'Test AG, Esther Tester, Testweg 321, 4321 Testingen',
    'GRUNDEIGENTUEMER': 'Sandra Beispiel',
    'GRUNDEIGENTUEMER_ADDRESS_1': 'Beispielstrasse 16',
    'GRUNDEIGENTUEMER_ADDRESS_2': '2222 Beispieldorf',
    'GRUNDEIGENTUEMER_ADRESSE_1': 'Beispielstrasse 16',
    'GRUNDEIGENTUEMER_ADRESSE_2': '2222 Beispieldorf',
    'GRUNDEIGENTUEMER_NAME_ADDRESS': 'Sandra Beispiel, Beispielstrasse 16, 2222 Beispieldorf',
    'GRUNDEIGENTUEMER_NAME_ADRESSE': 'Sandra Beispiel, Beispielstrasse 16, 2222 Beispieldorf',
    'HEUTE': '30. August 2021',
    'ID': 1,
    'INSTANCE_ID': 1,
    'JURISTIC_NAME': 'Test AG',
    'JURISTISCHER_NAME': 'Test AG',
    'KOORDINATEN': '2’569’941 / 1’298’923; 2’609’995 / 1’271’340',
    'LANGUAGE': 'de',
    'LEITBEHOERDE_ADDRESS_1': 'Teststrasse 1, 1234 Testdorf',
    'LEITBEHOERDE_ADDRESS_2': '1234 Testdorf',
    'LEITBEHOERDE_ADRESSE_1': 'Teststrasse 1, 1234 Testdorf',
    'LEITBEHOERDE_ADRESSE_2': '1234 Testdorf',
    'LEITBEHOERDE_CITY': 'Testdorf',
    'LEITBEHOERDE_EMAIL': 'michelleboone@example.org',
    'LEITBEHOERDE_NAME': 'Alex Smith',
    'LEITBEHOERDE_NAME_KURZ': 'Alex Smith',
    'LEITBEHOERDE_PHONE': '032163546546',
    'LEITBEHOERDE_STADT': 'Testdorf',
    'LEITBEHOERDE_TELEFON': '032163546546',
    'MEINE_ORGANISATION_ADRESSE_1': 'Teststrasse 1, 1234 Testdorf',
    'MEINE_ORGANISATION_ADRESSE_2': '1234 Testdorf',
    'MEINE_ORGANISATION_EMAIL': 'michelleboone@example.org',
    'MEINE_ORGANISATION_NAME': 'Alex Smith',
    'MEINE_ORGANISATION_NAME_ADRESSE': 'Alex Smith, Teststrasse 1, 1234 Testdorf, 1234 Testdorf',
    'MEINE_ORGANISATION_NAME_KURZ': 'Alex Smith',
    'MEINE_ORGANISATION_ORT': 'Testdorf',
    'MEINE_ORGANISATION_TELEFON': '032163546546',
    'MUNICIPALITY': 'Robert Li',
    'MUNICIPALITY_ADDRESS': '',
    'NAME': '',
    'NEBENBESTIMMUNGEN': '',
    'NEBENBESTIMMUNGEN_MAPPED': [
    ],
    'PARZELLE': '123465, 789876',
    'PROJEKTVERFASSER': 'Hans Muster',
    'PROJEKTVERFASSER_ADDRESS_1': 'Bahnhofstrasse 3',
    'PROJEKTVERFASSER_ADDRESS_2': '3600 Thun',
    'PROJEKTVERFASSER_ADRESSE_1': 'Bahnhofstrasse 3',
    'PROJEKTVERFASSER_ADRESSE_2': '3600 Thun',
    'PROJEKTVERFASSER_NAME_ADDRESS': 'Hans Muster, Bahnhofstrasse 3, 3600 Thun',
    'PROJEKTVERFASSER_NAME_ADRESSE': 'Hans Muster, Bahnhofstrasse 3, 3600 Thun',
    'PUBLIKATION_LINK': 'http://ebau-portal.local/public-instances/1',
    'PUBLIKATION_TEXT': 'Text',
    'SPRACHE': 'de',
    'START_PUBLIKATION_GEMEINDE': '20. August 2021',
    'START_PUBLIKATION_KANTON': '22. August 2021',
    'STATUS': 'David Rangel',
    'STELLUNGNAHME': '',
    'TODAY': '30. August 2021',
    'ZIRKULATION_ALLE': [
        {
            'BEANTWORTET': '',
            'ERSTELLT': '30.08.2021',
            'FRIST': '26.01.2015',
            'NAME': 'Dillon Peterson'
        },
        {
            'BEANTWORTET': '',
            'ERSTELLT': '30.08.2021',
            'FRIST': '19.12.1991',
            'NAME': 'Christopher Gonzalez'
        },
        {
            'BEANTWORTET': '',
            'ERSTELLT': '30.08.2021',
            'FRIST': '25.07.1995',
            'NAME': 'Susan Gonzalez'
        },
        {
            'BEANTWORTET': '',
            'ERSTELLT': '30.08.2021',
            'FRIST': '23.03.1972',
            'NAME': 'Steven Davis'
        },
        {
            'BEANTWORTET': '26.04.2001',
            'ERSTELLT': '30.08.2021',
            'FRIST': '08.01.2016',
            'NAME': 'Gloria Jenkins'
        },
        {
            'BEANTWORTET': '04.03.2000',
            'ERSTELLT': '30.08.2021',
            'FRIST': '07.02.2012',
            'NAME': 'Jessica Hutchinson'
        }
    ],
    'ZIRKULATION_FACHSTELLEN': [
        {
            'BEANTWORTET': '26.04.2001',
            'ERSTELLT': '30.08.2021',
            'FRIST': '08.01.2016',
            'NAME': 'Gloria Jenkins'
        },
        {
            'BEANTWORTET': '04.03.2000',
            'ERSTELLT': '30.08.2021',
            'FRIST': '07.02.2012',
            'NAME': 'Jessica Hutchinson'
        }
    ],
    'ZIRKULATION_GEMEINDEN': [
        {
            'BEANTWORTET': '',
            'ERSTELLT': '30.08.2021',
            'FRIST': '25.07.1995',
            'NAME': 'Susan Gonzalez'
        },
        {
            'BEANTWORTET': '',
            'ERSTELLT': '30.08.2021',
            'FRIST': '23.03.1972',
            'NAME': 'Steven Davis'
        }
    ],
    'ZIRKULATION_RUECKMELDUNGEN': [
        {
            'ANTWORT': '',
            'NEBENBESTIMMUNGEN': 'Nebenbestimmungen 5',
            'STELLUNGNAHME': 'Stellungnahme 5',
            'VON': 'Gloria Jenkins'
        },
        {
            'ANTWORT': '',
            'NEBENBESTIMMUNGEN': 'Nebenbestimmungen 6',
            'STELLUNGNAHME': 'Stellungnahme 6',
            'VON': 'Jessica Hutchinson'
        }
    ],
    'ZONENPLAN': 'Rebwirtschaftszone',
    'ZUSTAENDIG_NAME': 'Rebecca Gonzalez'
}
