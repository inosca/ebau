# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_dms_placeholders[Municipality] 1'] = {
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
    'ARRONDISSEMENT_ADMINISTRATIF': 'Emmental',
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
    'BESCHREIBUNG_PROJEKTAENDERUNG': 'Doch eher kleines Haus',
    'BOISSONS_ALCOOLIQUES': 'mit',
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
    'DECISION_POSITIVE': True,
    'DECISION_POSITIVE_PARTIEL': True,
    'DECISION_REFUS': False,
    'DECISION_REFUS_AVEC_RET': False,
    'DECISION_REFUS_SANS_RET': False,
    'DECISION_TYPE': 'GESAMT',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES': [
        {
            'DATE_DOCUMENT': '01.10.2022',
            'DATE_RECEPTION': '02.10.2022',
            'DATUM_DOKUMENT': '01.10.2022',
            'DATUM_EINGANG': '02.10.2022',
            'GRIEFS': '''Test LAB 1
Test LAB 2''',
            'RECHTSBEGEHRENDE': 'Lastenausgleichsbegehren4you AG',
            'REQUERANTS_CONCLUSIONS': 'Lastenausgleichsbegehren4you AG',
            'RUEGEPUNKTE': '''Test LAB 1
Test LAB 2''',
            'TITEL': 'Test Lastenausgleichsbegehren',
            'TITRE': 'Test Lastenausgleichsbegehren'
        }
    ],
    'DEPOT_DEMANDE_DATE': '31. März 2021',
    'DESCRIPTION_MODIFICATION': 'Doch eher kleines Haus',
    'DISPOSITIONS_ACCESSOIRES': 'Nebenbestimmungen 1',
    'DISPOSITIONS_ANNEXES': 'Nebenbestimmungen 1',
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
            'BETRAG': '392.66',
            'FORFAIT': '392.66',
            'POSITION': ''
        },
        {
            'BETRAG': '574.29',
            'FORFAIT': '574.29',
            'POSITION': ''
        }
    ],
    'EIGENE_GEBUEHREN_TOTAL': '966.95',
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
    'EMAIL': '',
    'EMOLUMENTS': [
        {
            'BETRAG': '378.78',
            'FORFAIT': '378.78',
            'POSITION': ''
        },
        {
            'BETRAG': '780.57',
            'FORFAIT': '780.57',
            'POSITION': ''
        },
        {
            'BETRAG': '392.66',
            'FORFAIT': '392.66',
            'POSITION': ''
        },
        {
            'BETRAG': '574.29',
            'FORFAIT': '574.29',
            'POSITION': ''
        }
    ],
    'EMOLUMENTS_TOTAL': '2’126.30',
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
            'BETRAG': '378.78',
            'FORFAIT': '378.78',
            'POSITION': ''
        },
        {
            'BETRAG': '780.57',
            'FORFAIT': '780.57',
            'POSITION': ''
        },
        {
            'BETRAG': '392.66',
            'FORFAIT': '392.66',
            'POSITION': ''
        },
        {
            'BETRAG': '574.29',
            'FORFAIT': '574.29',
            'POSITION': ''
        }
    ],
    'GEBUEHREN_TOTAL': '2’126.30',
    'GEMEINDE': 'Burgdorf',
    'GEMEINDE_ADRESSE': 'Jacobmouth',
    'GEMEINDE_ADRESSE_1': '',
    'GEMEINDE_ADRESSE_2': 'Jacobmouth',
    'GEMEINDE_EMAIL': 'jhill@example.net',
    'GEMEINDE_NAME_ADRESSE': 'Gemeinde Burgdorf, Jacobmouth',
    'GEMEINDE_ORT': 'Jacobmouth',
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
    'INFORMATION_OF_NEIGHBORS_LINK': 'http://ebau-portal.local/public-instances/1/form?key=5a49823',
    'INFORMATION_OF_NEIGHBORS_QR_CODE': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADLElEQVR4nO2bQW7jOBBFX40EeEkBfQAfhbrBHCnom1lHyQEaEJcGSPxZkFSU9Cym4YztRMWFIFp6MAsgqoq/Sib+eCx//TkDDjnkkEMOOeTQ94SsjREWG7E5jUBqU0j9hfkhy3PojhCSJKIkaR3qHTCoPoBBxLVPoyRdntwmhz4DSt0BLGamS7iazRSDkOsL1YM8ankOPQ6K6yB7WakBQ5f/758cekpo/DDXcr6alukXgjIS1zKK9KjlOXR3qO+IICAB8XWEuCKDoV4A2CtZT26TQ58ALWZmNoHNDKpnjbhSLzZT6lHjUctz6N4+Yu8AwtVEKibI9Lv3WveT2+TQ7ZDNQBcgTjKbgGUqzSksVahwH3EEqOoR0gq6hIwuQSKusPtNyrBpFK5HfGtop1DVxAGAqLxtlU2cWvv28R1xCKgYhG1bpHYGsRlawFimRy7PoXtBzUds0mQLHWzhZOcesvuIw0BNmgwS8fUkm4GmbKeeTy7TloF+CZscuuX0aXCSkcZs8XLtRwqGbATBcs6jxbX0Q+iT2+TQLdAugWxlzyARldnVQwF0YfDa5wGgzUdgIk1omZuL0DKt/a3wazTCNn1ymxz6FGio7sFmANKIvbxaK4nH15N0SV4NPxAUlbE5je2s8XOiXgB+L4l/DZscur2uETLVPRBWLKqMtSi6/H01oJhnloeBatEimdlLVayLtY6Zt1gRMjY/ZnkOPUDFzjVg0BorAUKuxY3qPLZmSz9rfGto8wCDDE6C9AMt5zwKattMBhDL+epR42BQVBOn7GUdBMlM0tVamSOd9C/Q/Zbn0F2gra7RS+J6L061Zn36bx41jgH1dEHvShoU08+pWNsWaaQ9/RI2OXSrZgkwZMEglglaL10NGD9qadTziMNAsTdS9ea5rf1WmV4rL95VdyBo+6arjWK9z3JQ65g5yzPLQ0JVe2i9M60/Ikj7TfPlbHLov4+P33S1Q2bII3EtqPXSlXfvPblNDt0C/f5Nl3qsALC41qTyTau66/IcujvU9Yg6BjXtuvdevnXM7PqzXY/4ztDHb7q0zdpdyNvTwTNLhxxyyCGHHHJoN/4BMBD7kv22h4gAAAAASUVORK5CYII=',
    'INSTANCE_ID': 1,
    'INTERIOR_SEATING': 35,
    'INVENTAR': 'Schützenswert, K-Objekt, Baugruppe Bauinventar: Test Baugruppe, RRB vom 1. Januar 2022, Vertrag vom 1. Februar 2022',
    'JURISTIC_NAME': 'ACME AG',
    'JURISTISCHER_NAME': 'ACME AG',
    'KOORDINATEN': '2’599’941 / 1’198’923; 2’601’995 / 1’201’340',
    'LANGUAGE': 'de',
    'LANGUE': 'de',
    'LASTENAUSGLEICHSBEGEHREN': [
        {
            'DATE_DOCUMENT': '01.10.2022',
            'DATE_RECEPTION': '02.10.2022',
            'DATUM_DOKUMENT': '01.10.2022',
            'DATUM_EINGANG': '02.10.2022',
            'GRIEFS': '''Test LAB 1
Test LAB 2''',
            'RECHTSBEGEHRENDE': 'Lastenausgleichsbegehren4you AG',
            'REQUERANTS_CONCLUSIONS': 'Lastenausgleichsbegehren4you AG',
            'RUEGEPUNKTE': '''Test LAB 1
Test LAB 2''',
            'TITEL': 'Test Lastenausgleichsbegehren',
            'TITRE': 'Test Lastenausgleichsbegehren'
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
            'BETRAG': '392.66',
            'FORFAIT': '392.66',
            'POSITION': ''
        },
        {
            'BETRAG': '574.29',
            'FORFAIT': '574.29',
            'POSITION': ''
        }
    ],
    'MES_EMOLUMENTS_TOTAL': '966.95',
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
    'NOM_LEGAL': 'ACME AG',
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
    'OPPOSING': [
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
    'PROTECTION_AREA': 'S1',
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
    'RECHTSVERWAHRUNGEN': [
        {
            'DATE_DOCUMENT': '01.11.2022',
            'DATE_RECEPTION': '02.11.2022',
            'DATUM_DOKUMENT': '01.11.2022',
            'DATUM_EINGANG': '02.11.2022',
            'GRIEFS': '''Test RV 1
Test RV 2''',
            'RECHTSBEGEHRENDE': 'Martha Rechstverwahrungsson',
            'REQUERANTS_CONCLUSIONS': 'Martha Rechstverwahrungsson',
            'RUEGEPUNKTE': '''Test RV 1
Test RV 2''',
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
    'REQUERANT_ADRESSE_1': 'Teststrasse 123',
    'REQUERANT_ADRESSE_2': '1234 Testhausen',
    'REQUERANT_NOM_ADRESSE': 'ACME AG, Max Mustermann, Teststrasse 123, 1234 Testhausen',
    'REQUERANT_TOUS': 'ACME AG, Max Mustermann',
    'REQUERANT_TOUS_NOM_ADRESSE': 'ACME AG, Max Mustermann, Teststrasse 123, 1234 Testhausen',
    'RESERVES_DE_DROIT': [
        {
            'DATE_DOCUMENT': '01.11.2022',
            'DATE_RECEPTION': '02.11.2022',
            'DATUM_DOKUMENT': '01.11.2022',
            'DATUM_EINGANG': '02.11.2022',
            'GRIEFS': '''Test RV 1
Test RV 2''',
            'RECHTSBEGEHRENDE': 'Martha Rechstverwahrungsson',
            'REQUERANTS_CONCLUSIONS': 'Martha Rechstverwahrungsson',
            'RUEGEPUNKTE': '''Test RV 1
Test RV 2''',
            'TITEL': 'Test Rechtsverwahrung',
            'TITRE': 'Test Rechtsverwahrung'
        }
    ],
    'RESPONSABLE_AUTORITE_DIRECTRICE': 'Thomas Morgan',
    'RESPONSABLE_EMAIL': 'tammy30@example.net',
    'RESPONSABLE_NOM': 'Thomas Morgan',
    'RESPONSABLE_TELEPHONE': '',
    'SACHVERHALT': 'Sachverhalt Test',
    'SCHUTZZONE': 'S1',
    'SECTEUR_PROTECTION_EAUX': 'Aᵤ',
    'SITUATION': 'Sachverhalt Test',
    'SITZPLAETZE_AUSSEN': 20,
    'SITZPLAETZE_INNEN': 35,
    'SPRACHE': 'de',
    'STATUS': 'Pamela Horton',
    'STELLUNGNAHME': 'Stellungnahme 1',
    'STICHWORTE': 'Andrew Berg MD, Alex Scott, Jacqueline Herrera, Kaitlyn Mendoza, Mary Mooney',
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

snapshots['test_dms_placeholders_docs 1'] = {
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
    'BAUENTSCHEID_ABSCHREIBUNGSVERFUEGUNG': {
        'aliases': [
            {
                'de': 'BAUENTSCHEID_ABSCHREIBUNGSVERFUEGUNG',
                'fr': 'BAUENTSCHEID_ABSCHREIBUNGSVERFUEGUNG'
            }
        ],
        'description': None,
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
            'de': 'Adresslinie 1 des/r Gesuchsteller/in',
            'fr': "Ligne d'adresse 1 requérant/e"
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
            'de': 'Adresslinie 2 des/r Gesuchsteller/in',
            'fr': "Ligne d'adresse 2 requérant/e"
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
            'de': 'Adresslinie 1 des/r Grundeigentümer/in',
            'fr': "Ligne d'adresse 1 propriétaire foncier/foncière"
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
            'de': 'Adresslinie 2 des/r Grundeigentümer/in',
            'fr': "Ligne d'adresse 2 propriétaire foncier/foncière"
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
            'de': "Alle Rechtsbegehren vom Typ 'Lastenausgleichsbegehren'",
            'fr': "Toutes les conclusions de type 'Demande en compensation des charges'"
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
            'de': "Alle Rechtsbegehren vom Typ 'Einsprache'",
            'fr': "Toutes les conclusions de type 'Opposition'"
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
                'de': 'RECHTSBEGEHRENDE',
                'fr': 'REQUERANTS_CONCLUSIONS'
            },
            {
                'de': 'EINSPRECHENDE',
                'fr': 'OPPOSANTS'
            }
        ],
        'description': {
            'de': 'Alle Rechtsbegehrenden mit Adresse',
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
            'de': 'Adresslinie 1 des/r Projektverfasser/in',
            'fr': "Ligne d'adresse 1 de l'auteur(e) du projet"
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
            'de': 'Adresslinie 2 des/r Projektverfasser/in',
            'fr': "Ligne d'adresse 2 de l'auteur(e) du projet"
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
    'RECHTSVERWAHRUNGEN': {
        'aliases': [
            {
                'de': 'RECHTSVERWAHRUNGEN',
                'fr': 'RESERVES_DE_DROIT'
            }
        ],
        'description': {
            'de': "Alle Rechtsbegehren vom Typ 'Rechtsverwahrung'",
            'fr': "Toutes les conclusions de type 'Réserve de droit'"
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

snapshots['test_dms_placeholders_docs_available_placeholders 1'] = [
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
    'ARRONDISSEMENT_ADMINISTRATIF',
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
    'BAUENTSCHEID_ABSCHREIBUNGSVERFUEGUNG',
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
    'BAUVORHABEN',
    'BESCHREIBUNG_BAUVORHABEN',
    'BESCHREIBUNG_PROJEKTAENDERUNG',
    'BOISSONS_ALCOOLIQUES',
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
    'COORDONEE',
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
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].DATE_DOCUMENT',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].DATE_RECEPTION',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].DATUM_DOKUMENT',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].DATUM_EINGANG',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].GRIEFS',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].RECHTSBEGEHRENDE',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].REQUERANTS_CONCLUSIONS',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].RUEGEPUNKTE',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].TITEL',
    'DEMANDES_EN_COMPENSATION_DES_CHARGES[].TITRE',
    'DEPOT_DEMANDE_DATE',
    'DESCRIPTION_MODIFICATION',
    'DISPOSITIONS_ACCESSOIRES',
    'DISPOSITIONS_ANNEXES',
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
    'FORM_NAME',
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
    'GEMEINDE',
    'GEMEINDE_ADRESSE',
    'GEMEINDE_ADRESSE_1',
    'GEMEINDE_ADRESSE_2',
    'GEMEINDE_EMAIL',
    'GEMEINDE_NAME_ADRESSE',
    'GEMEINDE_ORT',
    'GEMEINDE_TELEFON',
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
    'HEUTE',
    'INFORMATION_OF_NEIGHBORS_LINK',
    'INFORMATION_OF_NEIGHBORS_QR_CODE',
    'INSTANCE_ID',
    'INTERIOR_SEATING',
    'INVENTAR',
    'JURISTIC_NAME',
    'JURISTISCHER_NAME',
    'KOORDINATEN',
    'LANGUAGE',
    'LANGUE',
    'LASTENAUSGLEICHSBEGEHREN',
    'LASTENAUSGLEICHSBEGEHREN[]',
    'LASTENAUSGLEICHSBEGEHREN[].DATE_DOCUMENT',
    'LASTENAUSGLEICHSBEGEHREN[].DATE_RECEPTION',
    'LASTENAUSGLEICHSBEGEHREN[].DATUM_DOKUMENT',
    'LASTENAUSGLEICHSBEGEHREN[].DATUM_EINGANG',
    'LASTENAUSGLEICHSBEGEHREN[].GRIEFS',
    'LASTENAUSGLEICHSBEGEHREN[].RECHTSBEGEHRENDE',
    'LASTENAUSGLEICHSBEGEHREN[].REQUERANTS_CONCLUSIONS',
    'LASTENAUSGLEICHSBEGEHREN[].RUEGEPUNKTE',
    'LASTENAUSGLEICHSBEGEHREN[].TITEL',
    'LASTENAUSGLEICHSBEGEHREN[].TITRE',
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
    'NOM_LEGAL',
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
    'PROTECTION_AREA',
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
    'RECENSEMENT',
    'RECHTSBEGEHRENDE',
    'RECHTSBEGEHRENDE[]',
    'RECHTSBEGEHRENDE[].ADDRESS',
    'RECHTSBEGEHRENDE[].ADRESSE',
    'RECHTSBEGEHRENDE[].NAME',
    'RECHTSBEGEHRENDE[].NOM',
    'RECHTSVERWAHRUNGEN',
    'RECHTSVERWAHRUNGEN[]',
    'RECHTSVERWAHRUNGEN[].DATE_DOCUMENT',
    'RECHTSVERWAHRUNGEN[].DATE_RECEPTION',
    'RECHTSVERWAHRUNGEN[].DATUM_DOKUMENT',
    'RECHTSVERWAHRUNGEN[].DATUM_EINGANG',
    'RECHTSVERWAHRUNGEN[].GRIEFS',
    'RECHTSVERWAHRUNGEN[].RECHTSBEGEHRENDE',
    'RECHTSVERWAHRUNGEN[].REQUERANTS_CONCLUSIONS',
    'RECHTSVERWAHRUNGEN[].RUEGEPUNKTE',
    'RECHTSVERWAHRUNGEN[].TITEL',
    'RECHTSVERWAHRUNGEN[].TITRE',
    'REPRESENTANT',
    'REPRESENTANT_ADRESSE_1',
    'REPRESENTANT_ADRESSE_2',
    'REPRESENTANT_NOM_ADRESSE',
    'REPRESENTANT_TOUS',
    'REPRESENTANT_TOUS_NOM_ADRESSE',
    'REQUERANT',
    'REQUERANTS_CONCLUSIONS',
    'REQUERANTS_CONCLUSIONS[]',
    'REQUERANTS_CONCLUSIONS[].ADDRESS',
    'REQUERANTS_CONCLUSIONS[].ADRESSE',
    'REQUERANTS_CONCLUSIONS[].NAME',
    'REQUERANTS_CONCLUSIONS[].NOM',
    'REQUERANT_ADRESSE_1',
    'REQUERANT_ADRESSE_2',
    'REQUERANT_NOM_ADRESSE',
    'REQUERANT_TOUS',
    'REQUERANT_TOUS_NOM_ADRESSE',
    'RESERVES_DE_DROIT',
    'RESERVES_DE_DROIT[]',
    'RESERVES_DE_DROIT[].DATE_DOCUMENT',
    'RESERVES_DE_DROIT[].DATE_RECEPTION',
    'RESERVES_DE_DROIT[].DATUM_DOKUMENT',
    'RESERVES_DE_DROIT[].DATUM_EINGANG',
    'RESERVES_DE_DROIT[].GRIEFS',
    'RESERVES_DE_DROIT[].RECHTSBEGEHRENDE',
    'RESERVES_DE_DROIT[].REQUERANTS_CONCLUSIONS',
    'RESERVES_DE_DROIT[].RUEGEPUNKTE',
    'RESERVES_DE_DROIT[].TITEL',
    'RESERVES_DE_DROIT[].TITRE',
    'RESPONSABLE_AUTORITE_DIRECTRICE',
    'RESPONSABLE_EMAIL',
    'RESPONSABLE_NOM',
    'RESPONSABLE_TELEPHONE',
    'SACHVERHALT',
    'SCHUTZZONE',
    'SECTEUR_PROTECTION_EAUX',
    'SITUATION',
    'SITZPLAETZE_AUSSEN',
    'SITZPLAETZE_INNEN',
    'SPRACHE',
    'STATUS',
    'STELLUNGNAHME',
    'STICHWORTE',
    'TODAY',
    'UEBERBAUUNGSORDNUNG',
    'UVP_JA_NEIN',
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

snapshots['test_dms_placeholders_empty[Municipality] 1'] = {
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
    'ARRONDISSEMENT_ADMINISTRATIF': '',
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
    'BAUENTSCHEID_ABSCHREIBUNGSVERFUEGUNG': '',
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
    'BAUVORHABEN': '',
    'BESCHREIBUNG_BAUVORHABEN': '',
    'BESCHREIBUNG_PROJEKTAENDERUNG': '',
    'BOISSONS_ALCOOLIQUES': '',
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
    'COORDONEE': '',
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
    'DISPOSITIONS_ACCESSOIRES': '',
    'DISPOSITIONS_ANNEXES': '',
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
    'ETAT': 'David Rangel',
    'FACHSTELLEN_KANTONAL': [
    ],
    'FACHSTELLEN_KANTONAL_LIST': '',
    'FACHSTELLEN_KANTONAL_LISTE': '',
    'FORM_NAME': 'Baugesuch',
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
    'GEMEINDE': '',
    'GEMEINDE_ADRESSE': '',
    'GEMEINDE_ADRESSE_1': '',
    'GEMEINDE_ADRESSE_2': '',
    'GEMEINDE_EMAIL': '',
    'GEMEINDE_NAME_ADRESSE': '',
    'GEMEINDE_ORT': '',
    'GEMEINDE_TELEFON': '',
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
    'HEUTE': '30. August 2021',
    'INFORMATION_OF_NEIGHBORS_LINK': '',
    'INFORMATION_OF_NEIGHBORS_QR_CODE': '',
    'INSTANCE_ID': 1,
    'INTERIOR_SEATING': '',
    'INVENTAR': '',
    'JURISTIC_NAME': '',
    'JURISTISCHER_NAME': '',
    'KOORDINATEN': '',
    'LANGUAGE': 'de',
    'LANGUE': 'de',
    'LASTENAUSGLEICHSBEGEHREN': [
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
    'NOM_LEGAL': '',
    'NUTZUNG': '',
    'NUTZUNGSZONE': '',
    'OBJECTIONS': [
    ],
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
    'PROTECTION_AREA': '',
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
    'RECENSEMENT': '',
    'RECHTSBEGEHRENDE': [
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
    'REQUERANTS_CONCLUSIONS': [
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
    'SACHVERHALT': '',
    'SCHUTZZONE': '',
    'SECTEUR_PROTECTION_EAUX': '',
    'SITUATION': '',
    'SITZPLAETZE_AUSSEN': '',
    'SITZPLAETZE_INNEN': '',
    'SPRACHE': 'de',
    'STATUS': 'David Rangel',
    'STELLUNGNAHME': '',
    'STICHWORTE': '',
    'TODAY': '30. August 2021',
    'UEBERBAUUNGSORDNUNG': '',
    'UVP_JA_NEIN': False,
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
