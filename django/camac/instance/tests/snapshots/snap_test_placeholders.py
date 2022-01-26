# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_dms_placeholders[False-Municipality] 1'] = {
    'ADDRESS': 'Musterstrasse 4, Musterhausen',
    'ADMINISTRATIVE_DISTRICT': 'Emmental',
    'ADRESSE': 'Musterstrasse 4, Musterhausen',
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
    'AUTORITE_DIRECTRICE_ADRESSE_2': 'Johnsburgh',
    'AUTORITE_DIRECTRICE_EMAIL': 'michelleboone@example.org',
    'AUTORITE_DIRECTRICE_LIEU': 'Johnsburgh',
    'AUTORITE_DIRECTRICE_NOM': 'David Brown',
    'AUTORITE_DIRECTRICE_NOM_ABR': 'David Brown',
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
    'BOISSONS_ALCOOLIQUES': 'mit',
    'CIRCULATION_COMMUNES': [
        {
            'FRIST': '10.09.2021',
            'NAME': 'Kelsey Snow'
        },
        {
            'FRIST': '10.09.2021',
            'NAME': 'Kelly James'
        }
    ],
    'CIRCULATION_PREAVIS': [
        {
            'ANTWORT': 'Brian Kelley',
            'NEBENBESTIMMUNGEN': 'Store a true choice.',
            'STELLUNGNAHME': 'However teach party fact ability anyone.',
            'VON': 'Melissa Lane'
        },
        {
            'ANTWORT': 'Marco Russell',
            'NEBENBESTIMMUNGEN': 'Bank eye feeling.',
            'STELLUNGNAHME': 'Policy phone one determine red out agreement window.',
            'VON': 'David Brown'
        }
    ],
    'CIRCULATION_PREF': [
        {
            'FRIST': '30.08.2021',
            'NAME': 'Kayla Daniel'
        },
        {
            'FRIST': '02.09.2021',
            'NAME': 'Catherine Davis'
        }
    ],
    'CIRCULATION_SERVICES': [
        {
            'FRIST': '13.09.2021',
            'NAME': 'Melissa Lane'
        }
    ],
    'COMMUNE': 'Burgdorf',
    'COMMUNE_ADRESSE': 'Anthonyborough',
    'COMMUNE_ADRESSE_1': '',
    'COMMUNE_ADRESSE_2': 'Anthonyborough',
    'COMMUNE_EMAIL': 'colejoanne@example.net',
    'COMMUNE_LIEU': 'Anthonyborough',
    'COMMUNE_NOM_ADRESSE': 'Gemeinde Burgdorf, Anthonyborough',
    'COMMUNE_TELEPHONE': '',
    'COMMUNICATION_AUX_VOISINS_CODE_QR': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADAElEQVR4nO2cTW6jQBCFvxqQsgTJB8hR2jeYM82R5gZwlBxgJFhGavRm0T/gZJWxBzu4vEAB8wlaqbx+9aBj4suf8cfXGXDIIYcccsghh44JWf60wGxmZ8DOs5lZv1j+yfIX32RMDl0FBUnSBNBFgMWgkzTQ5I0kXUL73Z5D+0OrMqTdqhZzm45lBbnT7Tm0G9R+PDD2k4DYauyBMICYb3Alh74pFKalKEMX0TBX93DrKzn0kFDRiE6QpGDuYXxNlkEGTYQZtknWg4/JoRtAo5mZ9QA0Iry12HluIUxgZ5bUatzr9hzaWyO2AtC9myCmHY09pssTHn5MDl0DkbrKMAHQSJpyu5m6T02w/VaShgcfk0M3giRFGF8jdu4iMOdpooQStTf9PmNy6Ouf/GdPk4RiDaKSWqRNkhHXiGeAckVoqtOEItDFWhuNNHQlrgxeEUeHNj4iC8XGVsA22e7kGvEEUJGCTiq/+KIRQ90NU6O06xpxeKim2Esr5hcBCxp/gtE1MmgEvJuY29KEPviYHLoBFKZGuc2YcziVJ4wUTr0kR3Gv23PoDs6yeIYwre5htZx5wvBZ4/hQqQhtvWOSDACCYiqQ1Xd6RRwaqnkEaEhHqoucaglcpBVeEYeGNhWxNp6bSGooyfb25Acfk0PXQJ9DStUmMylDTag69xHPABU9KHaiKAPFQiQfUaNsr4ijQ9uKGEp/qaG70IiNjHhFHB26eBq+JpU1z65GM5lPr4jDQzWzbKLlzLIRzCc09n9aMZ8waLEgsDDse3sO7Q7VPKL4iPVBRs4sqU2I5xHPA61rukoosRhjXzxmWr7BYnn3W4zJoatmjTQbzCcsvLVofI2thelEftc2e4u4++05tDu0dZZpXpgAytq+TZ5dH274rPFkUOorFiPo3fSrz8f+w5UcekTo0yo/5h4LU4+F3ydZ0LK+GuFPw58A+rimS3nTRCCitAy0i625j3gOaPNcA6pxSK9dpj60nlnexnUfcWjI/D+TOeSQQw455JBD/wj9BfLKhenNnOo8AAAAAElFTkSuQmCC',
    'COMMUNICATION_AUX_VOISINS_LIEN': 'http://caluma-portal.local/public-instances/1?key=5a49823',
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
    'DISPOSITIONS_ANNEXES': 'Bank eye feeling.',
    'DOSSIER_LINK': 'http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1',
    'DOSSIER_NR': 1,
    'DOSSIER_NUMERO': 1,
    'DOSSIER_TYP': 'Baugesuch',
    'DOSSIER_TYPE': 'Baugesuch',
    'EBAU_NR': '2021-1',
    'EBAU_NUMBER': '2021-1',
    'EBAU_NUMERO': '2021-1',
    'EBAU_URL': 'http://camac-ng.local',
    'EIGENE_GEBUEHREN': [
        {
            'BETRAG': '129.56',
            'POSITION': ''
        },
        {
            'BETRAG': '846.16',
            'POSITION': ''
        }
    ],
    'EIGENE_GEBUEHREN_TOTAL': '975.72',
    'EIGENE_NEBENBESTIMMUNGEN': 'Bank eye feeling.',
    'EIGENE_STELLUNGNAHMEN': 'Policy phone one determine red out agreement window.',
    'EINSPRECHENDE': '',
    'EMAIL': '',
    'EMOLUMENTS': [
        {
            'BETRAG': '766.79',
            'POSITION': ''
        },
        {
            'BETRAG': '402.79',
            'POSITION': ''
        },
        {
            'BETRAG': '129.56',
            'POSITION': ''
        },
        {
            'BETRAG': '846.16',
            'POSITION': ''
        }
    ],
    'EMOLUMENTS_TOTAL': '2’145.30',
    'ETAT': 'David Rangel',
    'FACHSTELLEN_KANTONAL': [
        {
            'FRIST': '18.09.2021',
            'NAME': 'David Brown'
        }
    ],
    'FACHSTELLEN_KANTONAL_LIST': '- David Brown',
    'FACHSTELLEN_KANTONAL_LISTE': '- David Brown',
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
            'BETRAG': '766.79',
            'POSITION': ''
        },
        {
            'BETRAG': '402.79',
            'POSITION': ''
        },
        {
            'BETRAG': '129.56',
            'POSITION': ''
        },
        {
            'BETRAG': '846.16',
            'POSITION': ''
        }
    ],
    'GEBUEHREN_TOTAL': '2’145.30',
    'GEMEINDE': 'Burgdorf',
    'GEMEINDE_ADRESSE': 'Anthonyborough',
    'GEMEINDE_ADRESSE_1': '',
    'GEMEINDE_ADRESSE_2': 'Anthonyborough',
    'GEMEINDE_EMAIL': 'colejoanne@example.net',
    'GEMEINDE_NAME_ADRESSE': 'Gemeinde Burgdorf, Anthonyborough',
    'GEMEINDE_ORT': 'Anthonyborough',
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
    'INFORMATION_OF_NEIGHBORS_LINK': 'http://caluma-portal.local/public-instances/1?key=5a49823',
    'INFORMATION_OF_NEIGHBORS_QR_CODE': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADAElEQVR4nO2cTW6jQBCFvxqQsgTJB8hR2jeYM82R5gZwlBxgJFhGavRm0T/gZJWxBzu4vEAB8wlaqbx+9aBj4suf8cfXGXDIIYcccsghh44JWf60wGxmZ8DOs5lZv1j+yfIX32RMDl0FBUnSBNBFgMWgkzTQ5I0kXUL73Z5D+0OrMqTdqhZzm45lBbnT7Tm0G9R+PDD2k4DYauyBMICYb3Alh74pFKalKEMX0TBX93DrKzn0kFDRiE6QpGDuYXxNlkEGTYQZtknWg4/JoRtAo5mZ9QA0Iry12HluIUxgZ5bUatzr9hzaWyO2AtC9myCmHY09pssTHn5MDl0DkbrKMAHQSJpyu5m6T02w/VaShgcfk0M3giRFGF8jdu4iMOdpooQStTf9PmNy6Ouf/GdPk4RiDaKSWqRNkhHXiGeAckVoqtOEItDFWhuNNHQlrgxeEUeHNj4iC8XGVsA22e7kGvEEUJGCTiq/+KIRQ90NU6O06xpxeKim2Esr5hcBCxp/gtE1MmgEvJuY29KEPviYHLoBFKZGuc2YcziVJ4wUTr0kR3Gv23PoDs6yeIYwre5htZx5wvBZ4/hQqQhtvWOSDACCYiqQ1Xd6RRwaqnkEaEhHqoucaglcpBVeEYeGNhWxNp6bSGooyfb25Acfk0PXQJ9DStUmMylDTag69xHPABU9KHaiKAPFQiQfUaNsr4ijQ9uKGEp/qaG70IiNjHhFHB26eBq+JpU1z65GM5lPr4jDQzWzbKLlzLIRzCc09n9aMZ8waLEgsDDse3sO7Q7VPKL4iPVBRs4sqU2I5xHPA61rukoosRhjXzxmWr7BYnn3W4zJoatmjTQbzCcsvLVofI2thelEftc2e4u4++05tDu0dZZpXpgAytq+TZ5dH274rPFkUOorFiPo3fSrz8f+w5UcekTo0yo/5h4LU4+F3ydZ0LK+GuFPw58A+rimS3nTRCCitAy0i625j3gOaPNcA6pxSK9dpj60nlnexnUfcWjI/D+TOeSQQw455JBD/wj9BfLKhenNnOo8AAAAAElFTkSuQmCC',
    'INSTANCE_ID': 1,
    'INTERIOR_SEATING': 35,
    'INVENTAR': 'Ja, Nein, Nein, Nein, Ja, Ja',
    'JURISTIC_NAME': 'ACME AG',
    'JURISTISCHER_NAME': 'ACME AG',
    'KOORDINATEN': '2’599’941 / 1’198’923; 2’601’995 / 1’201’340',
    'LANGUAGE': 'de',
    'LANGUE': 'de',
    'LEITBEHOERDE_ADDRESS_1': '',
    'LEITBEHOERDE_ADDRESS_2': 'Johnsburgh',
    'LEITBEHOERDE_ADRESSE_1': '',
    'LEITBEHOERDE_ADRESSE_2': 'Johnsburgh',
    'LEITBEHOERDE_CITY': 'Johnsburgh',
    'LEITBEHOERDE_EMAIL': 'michelleboone@example.org',
    'LEITBEHOERDE_NAME': 'David Brown',
    'LEITBEHOERDE_NAME_KURZ': 'David Brown',
    'LEITBEHOERDE_PHONE': '',
    'LEITBEHOERDE_STADT': 'Johnsburgh',
    'LEITBEHOERDE_TELEFON': '',
    'LEITPERSON': 'Evelyn Bowman',
    'MEINE_ORGANISATION_ADRESSE_1': '',
    'MEINE_ORGANISATION_ADRESSE_2': 'Johnsburgh',
    'MEINE_ORGANISATION_EMAIL': 'michelleboone@example.org',
    'MEINE_ORGANISATION_NAME': 'David Brown',
    'MEINE_ORGANISATION_NAME_ADRESSE': 'David Brown, Johnsburgh',
    'MEINE_ORGANISATION_NAME_KURZ': 'David Brown',
    'MEINE_ORGANISATION_ORT': 'Johnsburgh',
    'MEINE_ORGANISATION_TELEFON': '',
    'MES_EMOLUMENTS': [
        {
            'BETRAG': '129.56',
            'POSITION': ''
        },
        {
            'BETRAG': '846.16',
            'POSITION': ''
        }
    ],
    'MES_EMOLUMENTS_TOTAL': '975.72',
    'MODIFICATION_DATE': '',
    'MODIFICATION_TIME': '',
    'MON_ORGANISATION_ADRESSE_1': '',
    'MON_ORGANISATION_ADRESSE_2': 'Johnsburgh',
    'MON_ORGANISATION_EMAIL': 'michelleboone@example.org',
    'MON_ORGANISATION_LIEU': 'Johnsburgh',
    'MON_ORGANISATION_NOM': 'David Brown',
    'MON_ORGANISATION_NOM_ABR': 'David Brown',
    'MON_ORGANISATION_NOM_ADRESSE': 'David Brown, Johnsburgh',
    'MON_ORGANISATION_TELEPHONE': '',
    'MOTS_CLES': 'Carrie Stanley, Tom Barrett, Mark Nelson, Christopher Buck, Darrell Daniels',
    'MUNICIPALITY': 'Burgdorf',
    'MUNICIPALITY_ADDRESS': 'Anthonyborough',
    'NACHBARSCHAFTSORIENTIERUNG_LINK': 'http://caluma-portal.local/public-instances/1?key=5a49823',
    'NACHBARSCHAFTSORIENTIERUNG_QR_CODE': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADAElEQVR4nO2cTW6jQBCFvxqQsgTJB8hR2jeYM82R5gZwlBxgJFhGavRm0T/gZJWxBzu4vEAB8wlaqbx+9aBj4suf8cfXGXDIIYcccsghh44JWf60wGxmZ8DOs5lZv1j+yfIX32RMDl0FBUnSBNBFgMWgkzTQ5I0kXUL73Z5D+0OrMqTdqhZzm45lBbnT7Tm0G9R+PDD2k4DYauyBMICYb3Alh74pFKalKEMX0TBX93DrKzn0kFDRiE6QpGDuYXxNlkEGTYQZtknWg4/JoRtAo5mZ9QA0Iry12HluIUxgZ5bUatzr9hzaWyO2AtC9myCmHY09pssTHn5MDl0DkbrKMAHQSJpyu5m6T02w/VaShgcfk0M3giRFGF8jdu4iMOdpooQStTf9PmNy6Ouf/GdPk4RiDaKSWqRNkhHXiGeAckVoqtOEItDFWhuNNHQlrgxeEUeHNj4iC8XGVsA22e7kGvEEUJGCTiq/+KIRQ90NU6O06xpxeKim2Esr5hcBCxp/gtE1MmgEvJuY29KEPviYHLoBFKZGuc2YcziVJ4wUTr0kR3Gv23PoDs6yeIYwre5htZx5wvBZ4/hQqQhtvWOSDACCYiqQ1Xd6RRwaqnkEaEhHqoucaglcpBVeEYeGNhWxNp6bSGooyfb25Acfk0PXQJ9DStUmMylDTag69xHPABU9KHaiKAPFQiQfUaNsr4ijQ9uKGEp/qaG70IiNjHhFHB26eBq+JpU1z65GM5lPr4jDQzWzbKLlzLIRzCc09n9aMZ8waLEgsDDse3sO7Q7VPKL4iPVBRs4sqU2I5xHPA61rukoosRhjXzxmWr7BYnn3W4zJoatmjTQbzCcsvLVofI2thelEftc2e4u4++05tDu0dZZpXpgAytq+TZ5dH274rPFkUOorFiPo3fSrz8f+w5UcekTo0yo/5h4LU4+F3ydZ0LK+GuFPw58A+rimS3nTRCCitAy0i625j3gOaPNcA6pxSK9dpj60nlnexnUfcWjI/D+TOeSQQw455JBD/wj9BfLKhenNnOo8AAAAAElFTkSuQmCC',
    'NAME': '',
    'NEBENBESTIMMUNGEN': 'Bank eye feeling.',
    'NEBENBESTIMMUNGEN_MAPPED': [
        {
            'FACHSTELLE': 'David Brown',
            'TEXT': 'Bank eye feeling.'
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
    'OEFFENTLICHKEIT': 'Öffentlich',
    'OFFICES_CANTONAUX': [
        {
            'FRIST': '18.09.2021',
            'NAME': 'David Brown'
        }
    ],
    'OFFICES_CANTONAUX_LISTE': '- David Brown',
    'OPPOSANTS': '',
    'OPPOSING': '',
    'OUTSIDE_SEATING': 20,
    'OUVERTURE_PUBLIC': 'Öffentlich',
    'PARCELLE': '473, 2592',
    'PARZELLE': '473, 2592',
    'PLACES_ASSISES_EXT': 20,
    'PLACES_ASSISES_INT': 35,
    'PLAN_QUARTIER': 'Überbauung XY',
    'PRISE_DE_POSITION': 'Policy phone one determine red out agreement window.',
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
    'RESPONSABLE_AUTORITE_DIRECTRICE': 'Evelyn Bowman',
    'RESPONSABLE_EMAIL': 'danielcruz@example.com',
    'RESPONSABLE_NOM': 'Evelyn Bowman',
    'RESPONSABLE_TELEPHONE': '',
    'SACHVERHALT': 'Sachverhalt Test',
    'SCHUTZZONE': 'S1',
    'SECTEUR_PROTECTION_EAUX': 'Aᵤ',
    'SITUATION': 'Sachverhalt Test',
    'SITZPLAETZE_AUSSEN': 20,
    'SITZPLAETZE_INNEN': 35,
    'SPRACHE': 'de',
    'STATUS': 'David Rangel',
    'STELLUNGNAHME': 'Policy phone one determine red out agreement window.',
    'STICHWORTE': 'Carrie Stanley, Tom Barrett, Mark Nelson, Christopher Buck, Darrell Daniels',
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
            'FRIST': '18.09.2021',
            'NAME': 'David Brown'
        }
    ],
    'ZIRKULATION_FACHSTELLEN': [
        {
            'FRIST': '13.09.2021',
            'NAME': 'Melissa Lane'
        }
    ],
    'ZIRKULATION_GEMEINDEN': [
        {
            'FRIST': '10.09.2021',
            'NAME': 'Kelsey Snow'
        },
        {
            'FRIST': '10.09.2021',
            'NAME': 'Kelly James'
        }
    ],
    'ZIRKULATION_RSTA': [
        {
            'FRIST': '30.08.2021',
            'NAME': 'Kayla Daniel'
        },
        {
            'FRIST': '02.09.2021',
            'NAME': 'Catherine Davis'
        }
    ],
    'ZIRKULATION_RUECKMELDUNGEN': [
        {
            'ANTWORT': 'Brian Kelley',
            'NEBENBESTIMMUNGEN': 'Store a true choice.',
            'STELLUNGNAHME': 'However teach party fact ability anyone.',
            'VON': 'Melissa Lane'
        },
        {
            'ANTWORT': 'Marco Russell',
            'NEBENBESTIMMUNGEN': 'Bank eye feeling.',
            'STELLUNGNAHME': 'Policy phone one determine red out agreement window.',
            'VON': 'David Brown'
        }
    ],
    'ZONE_PROTEGEE': 'S1',
    'ZUSTAENDIG_EMAIL': 'danielcruz@example.com',
    'ZUSTAENDIG_NAME': 'Evelyn Bowman',
    'ZUSTAENDIG_PHONE': '',
    'ZUSTAENDIG_TELEFON': ''
}

snapshots['test_dms_placeholders[True-Municipality] 1'] = {
    'ADDRESS': 'Musterstrasse 4, Musterhausen',
    'ADMINISTRATIVE_DISTRICT': 'Emmental',
    'ADRESSE': 'Musterstrasse 4, Musterhausen',
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
    'AUTORITE_DIRECTRICE_ADRESSE_2': 'Johnsburgh',
    'AUTORITE_DIRECTRICE_EMAIL': 'michelleboone@example.org',
    'AUTORITE_DIRECTRICE_LIEU': 'Johnsburgh',
    'AUTORITE_DIRECTRICE_NOM': 'David Brown',
    'AUTORITE_DIRECTRICE_NOM_ABR': 'David Brown',
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
    'BOISSONS_ALCOOLIQUES': 'mit',
    'CIRCULATION_COMMUNES': [
        {
            'FRIST': '19.09.2021',
            'NAME': 'Shelly Reese'
        },
        {
            'FRIST': '16.09.2021',
            'NAME': 'Susan Rivers'
        }
    ],
    'CIRCULATION_PREAVIS': [
        {
            'ANTWORT': 'Brian Kelley',
            'NEBENBESTIMMUNGEN': 'Store a true choice.',
            'STELLUNGNAHME': 'However teach party fact ability anyone.',
            'VON': 'Melissa Lane'
        },
        {
            'ANTWORT': 'Marco Russell',
            'NEBENBESTIMMUNGEN': 'Bank eye feeling.',
            'STELLUNGNAHME': 'Policy phone one determine red out agreement window.',
            'VON': 'David Brown'
        }
    ],
    'CIRCULATION_PREF': [
        {
            'FRIST': '21.09.2021',
            'NAME': 'Daniel Moody'
        },
        {
            'FRIST': '16.09.2021',
            'NAME': 'Todd Brown'
        }
    ],
    'CIRCULATION_SERVICES': [
        {
            'FRIST': '13.09.2021',
            'NAME': 'Melissa Lane'
        }
    ],
    'COMMUNE': 'Burgdorf',
    'COMMUNE_ADRESSE': 'East Andrew',
    'COMMUNE_ADRESSE_1': '',
    'COMMUNE_ADRESSE_2': 'East Andrew',
    'COMMUNE_EMAIL': 'campbellandrew@example.org',
    'COMMUNE_LIEU': 'East Andrew',
    'COMMUNE_NOM_ADRESSE': 'Gemeinde Burgdorf, East Andrew',
    'COMMUNE_TELEPHONE': '',
    'COMMUNICATION_AUX_VOISINS_CODE_QR': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADAElEQVR4nO2cTW6jQBCFvxqQsgTJB8hR2jeYM82R5gZwlBxgJFhGavRm0T/gZJWxBzu4vEAB8wlaqbx+9aBj4suf8cfXGXDIIYcccsghh44JWf60wGxmZ8DOs5lZv1j+yfIX32RMDl0FBUnSBNBFgMWgkzTQ5I0kXUL73Z5D+0OrMqTdqhZzm45lBbnT7Tm0G9R+PDD2k4DYauyBMICYb3Alh74pFKalKEMX0TBX93DrKzn0kFDRiE6QpGDuYXxNlkEGTYQZtknWg4/JoRtAo5mZ9QA0Iry12HluIUxgZ5bUatzr9hzaWyO2AtC9myCmHY09pssTHn5MDl0DkbrKMAHQSJpyu5m6T02w/VaShgcfk0M3giRFGF8jdu4iMOdpooQStTf9PmNy6Ouf/GdPk4RiDaKSWqRNkhHXiGeAckVoqtOEItDFWhuNNHQlrgxeEUeHNj4iC8XGVsA22e7kGvEEUJGCTiq/+KIRQ90NU6O06xpxeKim2Esr5hcBCxp/gtE1MmgEvJuY29KEPviYHLoBFKZGuc2YcziVJ4wUTr0kR3Gv23PoDs6yeIYwre5htZx5wvBZ4/hQqQhtvWOSDACCYiqQ1Xd6RRwaqnkEaEhHqoucaglcpBVeEYeGNhWxNp6bSGooyfb25Acfk0PXQJ9DStUmMylDTag69xHPABU9KHaiKAPFQiQfUaNsr4ijQ9uKGEp/qaG70IiNjHhFHB26eBq+JpU1z65GM5lPr4jDQzWzbKLlzLIRzCc09n9aMZ8waLEgsDDse3sO7Q7VPKL4iPVBRs4sqU2I5xHPA61rukoosRhjXzxmWr7BYnn3W4zJoatmjTQbzCcsvLVofI2thelEftc2e4u4++05tDu0dZZpXpgAytq+TZ5dH274rPFkUOorFiPo3fSrz8f+w5UcekTo0yo/5h4LU4+F3ydZ0LK+GuFPw58A+rimS3nTRCCitAy0i625j3gOaPNcA6pxSK9dpj60nlnexnUfcWjI/D+TOeSQQw455JBD/wj9BfLKhenNnOo8AAAAAElFTkSuQmCC',
    'COMMUNICATION_AUX_VOISINS_LIEN': 'http://caluma-portal.local/public-instances/1?key=5a49823',
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
    'DISPOSITIONS_ANNEXES': 'Bank eye feeling.',
    'DOSSIER_LINK': 'http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1',
    'DOSSIER_NR': 1,
    'DOSSIER_NUMERO': 1,
    'DOSSIER_TYP': 'Baugesuch',
    'DOSSIER_TYPE': 'Baugesuch',
    'EBAU_NR': '2021-1',
    'EBAU_NUMBER': '2021-1',
    'EBAU_NUMERO': '2021-1',
    'EBAU_URL': 'http://camac-ng.local',
    'EIGENE_GEBUEHREN': [
        {
            'BETRAG': '129.56',
            'POSITION': ''
        },
        {
            'BETRAG': '846.16',
            'POSITION': ''
        }
    ],
    'EIGENE_GEBUEHREN_TOTAL': '975.72',
    'EIGENE_NEBENBESTIMMUNGEN': 'Bank eye feeling.',
    'EIGENE_STELLUNGNAHMEN': 'Policy phone one determine red out agreement window.',
    'EINSPRECHENDE': 'Test AG, Müller Hans, Teststrasse 1, 1234 Testdorf, Beispiel AG, Muster Max, Bahnhofstrasse 32, 9874 Testingen',
    'EMAIL': '',
    'EMOLUMENTS': [
        {
            'BETRAG': '766.79',
            'POSITION': ''
        },
        {
            'BETRAG': '402.79',
            'POSITION': ''
        },
        {
            'BETRAG': '129.56',
            'POSITION': ''
        },
        {
            'BETRAG': '846.16',
            'POSITION': ''
        }
    ],
    'EMOLUMENTS_TOTAL': '2’145.30',
    'ETAT': 'David Rangel',
    'FACHSTELLEN_KANTONAL': [
        {
            'FRIST': '21.09.2021',
            'NAME': 'Daniel Moody'
        },
        {
            'FRIST': '19.09.2021',
            'NAME': 'Shelly Reese'
        },
        {
            'FRIST': '16.09.2021',
            'NAME': 'Susan Rivers'
        },
        {
            'FRIST': '13.09.2021',
            'NAME': 'Melissa Lane'
        },
        {
            'FRIST': '18.09.2021',
            'NAME': 'David Brown'
        },
        {
            'FRIST': '16.09.2021',
            'NAME': 'Todd Brown'
        }
    ],
    'FACHSTELLEN_KANTONAL_LIST': '''- Daniel Moody
- Shelly Reese
- Susan Rivers
- Melissa Lane
- David Brown
- Todd Brown''',
    'FACHSTELLEN_KANTONAL_LISTE': '''- Daniel Moody
- Shelly Reese
- Susan Rivers
- Melissa Lane
- David Brown
- Todd Brown''',
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
            'BETRAG': '766.79',
            'POSITION': ''
        },
        {
            'BETRAG': '402.79',
            'POSITION': ''
        },
        {
            'BETRAG': '129.56',
            'POSITION': ''
        },
        {
            'BETRAG': '846.16',
            'POSITION': ''
        }
    ],
    'GEBUEHREN_TOTAL': '2’145.30',
    'GEMEINDE': 'Burgdorf',
    'GEMEINDE_ADRESSE': 'East Andrew',
    'GEMEINDE_ADRESSE_1': '',
    'GEMEINDE_ADRESSE_2': 'East Andrew',
    'GEMEINDE_EMAIL': 'campbellandrew@example.org',
    'GEMEINDE_NAME_ADRESSE': 'Gemeinde Burgdorf, East Andrew',
    'GEMEINDE_ORT': 'East Andrew',
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
    'INFORMATION_OF_NEIGHBORS_LINK': 'http://caluma-portal.local/public-instances/1?key=5a49823',
    'INFORMATION_OF_NEIGHBORS_QR_CODE': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADAElEQVR4nO2cTW6jQBCFvxqQsgTJB8hR2jeYM82R5gZwlBxgJFhGavRm0T/gZJWxBzu4vEAB8wlaqbx+9aBj4suf8cfXGXDIIYcccsghh44JWf60wGxmZ8DOs5lZv1j+yfIX32RMDl0FBUnSBNBFgMWgkzTQ5I0kXUL73Z5D+0OrMqTdqhZzm45lBbnT7Tm0G9R+PDD2k4DYauyBMICYb3Alh74pFKalKEMX0TBX93DrKzn0kFDRiE6QpGDuYXxNlkEGTYQZtknWg4/JoRtAo5mZ9QA0Iry12HluIUxgZ5bUatzr9hzaWyO2AtC9myCmHY09pssTHn5MDl0DkbrKMAHQSJpyu5m6T02w/VaShgcfk0M3giRFGF8jdu4iMOdpooQStTf9PmNy6Ouf/GdPk4RiDaKSWqRNkhHXiGeAckVoqtOEItDFWhuNNHQlrgxeEUeHNj4iC8XGVsA22e7kGvEEUJGCTiq/+KIRQ90NU6O06xpxeKim2Esr5hcBCxp/gtE1MmgEvJuY29KEPviYHLoBFKZGuc2YcziVJ4wUTr0kR3Gv23PoDs6yeIYwre5htZx5wvBZ4/hQqQhtvWOSDACCYiqQ1Xd6RRwaqnkEaEhHqoucaglcpBVeEYeGNhWxNp6bSGooyfb25Acfk0PXQJ9DStUmMylDTag69xHPABU9KHaiKAPFQiQfUaNsr4ijQ9uKGEp/qaG70IiNjHhFHB26eBq+JpU1z65GM5lPr4jDQzWzbKLlzLIRzCc09n9aMZ8waLEgsDDse3sO7Q7VPKL4iPVBRs4sqU2I5xHPA61rukoosRhjXzxmWr7BYnn3W4zJoatmjTQbzCcsvLVofI2thelEftc2e4u4++05tDu0dZZpXpgAytq+TZ5dH274rPFkUOorFiPo3fSrz8f+w5UcekTo0yo/5h4LU4+F3ydZ0LK+GuFPw58A+rimS3nTRCCitAy0i625j3gOaPNcA6pxSK9dpj60nlnexnUfcWjI/D+TOeSQQw455JBD/wj9BfLKhenNnOo8AAAAAElFTkSuQmCC',
    'INSTANCE_ID': 1,
    'INTERIOR_SEATING': 35,
    'INVENTAR': 'Ja, Nein, Nein, Nein, Ja, Ja',
    'JURISTIC_NAME': 'ACME AG',
    'JURISTISCHER_NAME': 'ACME AG',
    'KOORDINATEN': '2’599’941 / 1’198’923; 2’601’995 / 1’201’340',
    'LANGUAGE': 'de',
    'LANGUE': 'de',
    'LEITBEHOERDE_ADDRESS_1': '',
    'LEITBEHOERDE_ADDRESS_2': 'Johnsburgh',
    'LEITBEHOERDE_ADRESSE_1': '',
    'LEITBEHOERDE_ADRESSE_2': 'Johnsburgh',
    'LEITBEHOERDE_CITY': 'Johnsburgh',
    'LEITBEHOERDE_EMAIL': 'michelleboone@example.org',
    'LEITBEHOERDE_NAME': 'David Brown',
    'LEITBEHOERDE_NAME_KURZ': 'David Brown',
    'LEITBEHOERDE_PHONE': '',
    'LEITBEHOERDE_STADT': 'Johnsburgh',
    'LEITBEHOERDE_TELEFON': '',
    'LEITPERSON': 'Evelyn Bowman',
    'MEINE_ORGANISATION_ADRESSE_1': '',
    'MEINE_ORGANISATION_ADRESSE_2': 'Johnsburgh',
    'MEINE_ORGANISATION_EMAIL': 'michelleboone@example.org',
    'MEINE_ORGANISATION_NAME': 'David Brown',
    'MEINE_ORGANISATION_NAME_ADRESSE': 'David Brown, Johnsburgh',
    'MEINE_ORGANISATION_NAME_KURZ': 'David Brown',
    'MEINE_ORGANISATION_ORT': 'Johnsburgh',
    'MEINE_ORGANISATION_TELEFON': '',
    'MES_EMOLUMENTS': [
        {
            'BETRAG': '129.56',
            'POSITION': ''
        },
        {
            'BETRAG': '846.16',
            'POSITION': ''
        }
    ],
    'MES_EMOLUMENTS_TOTAL': '975.72',
    'MODIFICATION_DATE': '',
    'MODIFICATION_TIME': '',
    'MON_ORGANISATION_ADRESSE_1': '',
    'MON_ORGANISATION_ADRESSE_2': 'Johnsburgh',
    'MON_ORGANISATION_EMAIL': 'michelleboone@example.org',
    'MON_ORGANISATION_LIEU': 'Johnsburgh',
    'MON_ORGANISATION_NOM': 'David Brown',
    'MON_ORGANISATION_NOM_ABR': 'David Brown',
    'MON_ORGANISATION_NOM_ADRESSE': 'David Brown, Johnsburgh',
    'MON_ORGANISATION_TELEPHONE': '',
    'MOTS_CLES': 'Carrie Stanley, Tom Barrett, Mark Nelson, Christopher Buck, Darrell Daniels',
    'MUNICIPALITY': 'Burgdorf',
    'MUNICIPALITY_ADDRESS': 'East Andrew',
    'NACHBARSCHAFTSORIENTIERUNG_LINK': 'http://caluma-portal.local/public-instances/1?key=5a49823',
    'NACHBARSCHAFTSORIENTIERUNG_QR_CODE': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADAElEQVR4nO2cTW6jQBCFvxqQsgTJB8hR2jeYM82R5gZwlBxgJFhGavRm0T/gZJWxBzu4vEAB8wlaqbx+9aBj4suf8cfXGXDIIYcccsghh44JWf60wGxmZ8DOs5lZv1j+yfIX32RMDl0FBUnSBNBFgMWgkzTQ5I0kXUL73Z5D+0OrMqTdqhZzm45lBbnT7Tm0G9R+PDD2k4DYauyBMICYb3Alh74pFKalKEMX0TBX93DrKzn0kFDRiE6QpGDuYXxNlkEGTYQZtknWg4/JoRtAo5mZ9QA0Iry12HluIUxgZ5bUatzr9hzaWyO2AtC9myCmHY09pssTHn5MDl0DkbrKMAHQSJpyu5m6T02w/VaShgcfk0M3giRFGF8jdu4iMOdpooQStTf9PmNy6Ouf/GdPk4RiDaKSWqRNkhHXiGeAckVoqtOEItDFWhuNNHQlrgxeEUeHNj4iC8XGVsA22e7kGvEEUJGCTiq/+KIRQ90NU6O06xpxeKim2Esr5hcBCxp/gtE1MmgEvJuY29KEPviYHLoBFKZGuc2YcziVJ4wUTr0kR3Gv23PoDs6yeIYwre5htZx5wvBZ4/hQqQhtvWOSDACCYiqQ1Xd6RRwaqnkEaEhHqoucaglcpBVeEYeGNhWxNp6bSGooyfb25Acfk0PXQJ9DStUmMylDTag69xHPABU9KHaiKAPFQiQfUaNsr4ijQ9uKGEp/qaG70IiNjHhFHB26eBq+JpU1z65GM5lPr4jDQzWzbKLlzLIRzCc09n9aMZ8waLEgsDDse3sO7Q7VPKL4iPVBRs4sqU2I5xHPA61rukoosRhjXzxmWr7BYnn3W4zJoatmjTQbzCcsvLVofI2thelEftc2e4u4++05tDu0dZZpXpgAytq+TZ5dH274rPFkUOorFiPo3fSrz8f+w5UcekTo0yo/5h4LU4+F3ydZ0LK+GuFPw58A+rimS3nTRCCitAy0i625j3gOaPNcA6pxSK9dpj60nlnexnUfcWjI/D+TOeSQQw455JBD/wj9BfLKhenNnOo8AAAAAElFTkSuQmCC',
    'NAME': '',
    'NEBENBESTIMMUNGEN': 'Bank eye feeling.',
    'NEBENBESTIMMUNGEN_MAPPED': [
        {
            'FACHSTELLE': 'David Brown',
            'TEXT': 'Bank eye feeling.'
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
    'OEFFENTLICHKEIT': 'Öffentlich',
    'OFFICES_CANTONAUX': [
        {
            'FRIST': '21.09.2021',
            'NAME': 'Daniel Moody'
        },
        {
            'FRIST': '19.09.2021',
            'NAME': 'Shelly Reese'
        },
        {
            'FRIST': '16.09.2021',
            'NAME': 'Susan Rivers'
        },
        {
            'FRIST': '13.09.2021',
            'NAME': 'Melissa Lane'
        },
        {
            'FRIST': '18.09.2021',
            'NAME': 'David Brown'
        },
        {
            'FRIST': '16.09.2021',
            'NAME': 'Todd Brown'
        }
    ],
    'OFFICES_CANTONAUX_LISTE': '''- Daniel Moody
- Shelly Reese
- Susan Rivers
- Melissa Lane
- David Brown
- Todd Brown''',
    'OPPOSANTS': 'Test AG, Müller Hans, Teststrasse 1, 1234 Testdorf, Beispiel AG, Muster Max, Bahnhofstrasse 32, 9874 Testingen',
    'OPPOSING': 'Test AG, Müller Hans, Teststrasse 1, 1234 Testdorf, Beispiel AG, Muster Max, Bahnhofstrasse 32, 9874 Testingen',
    'OUTSIDE_SEATING': 20,
    'OUVERTURE_PUBLIC': 'Öffentlich',
    'PARCELLE': '473, 2592',
    'PARZELLE': '473, 2592',
    'PLACES_ASSISES_EXT': 20,
    'PLACES_ASSISES_INT': 35,
    'PLAN_QUARTIER': 'Überbauung XY',
    'PRISE_DE_POSITION': 'Policy phone one determine red out agreement window.',
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
    'RESPONSABLE_AUTORITE_DIRECTRICE': 'Evelyn Bowman',
    'RESPONSABLE_EMAIL': 'danielcruz@example.com',
    'RESPONSABLE_NOM': 'Evelyn Bowman',
    'RESPONSABLE_TELEPHONE': '',
    'SACHVERHALT': 'Sachverhalt Test',
    'SCHUTZZONE': 'S1',
    'SECTEUR_PROTECTION_EAUX': 'Aᵤ',
    'SITUATION': 'Sachverhalt Test',
    'SITZPLAETZE_AUSSEN': 20,
    'SITZPLAETZE_INNEN': 35,
    'SPRACHE': 'de',
    'STATUS': 'David Rangel',
    'STELLUNGNAHME': 'Policy phone one determine red out agreement window.',
    'STICHWORTE': 'Carrie Stanley, Tom Barrett, Mark Nelson, Christopher Buck, Darrell Daniels',
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
            'FRIST': '21.09.2021',
            'NAME': 'Daniel Moody'
        },
        {
            'FRIST': '19.09.2021',
            'NAME': 'Shelly Reese'
        },
        {
            'FRIST': '16.09.2021',
            'NAME': 'Susan Rivers'
        },
        {
            'FRIST': '13.09.2021',
            'NAME': 'Melissa Lane'
        },
        {
            'FRIST': '18.09.2021',
            'NAME': 'David Brown'
        },
        {
            'FRIST': '16.09.2021',
            'NAME': 'Todd Brown'
        }
    ],
    'ZIRKULATION_FACHSTELLEN': [
        {
            'FRIST': '13.09.2021',
            'NAME': 'Melissa Lane'
        }
    ],
    'ZIRKULATION_GEMEINDEN': [
        {
            'FRIST': '19.09.2021',
            'NAME': 'Shelly Reese'
        },
        {
            'FRIST': '16.09.2021',
            'NAME': 'Susan Rivers'
        }
    ],
    'ZIRKULATION_RSTA': [
        {
            'FRIST': '21.09.2021',
            'NAME': 'Daniel Moody'
        },
        {
            'FRIST': '16.09.2021',
            'NAME': 'Todd Brown'
        }
    ],
    'ZIRKULATION_RUECKMELDUNGEN': [
        {
            'ANTWORT': 'Brian Kelley',
            'NEBENBESTIMMUNGEN': 'Store a true choice.',
            'STELLUNGNAHME': 'However teach party fact ability anyone.',
            'VON': 'Melissa Lane'
        },
        {
            'ANTWORT': 'Marco Russell',
            'NEBENBESTIMMUNGEN': 'Bank eye feeling.',
            'STELLUNGNAHME': 'Policy phone one determine red out agreement window.',
            'VON': 'David Brown'
        }
    ],
    'ZONE_PROTEGEE': 'S1',
    'ZUSTAENDIG_EMAIL': 'danielcruz@example.com',
    'ZUSTAENDIG_NAME': 'Evelyn Bowman',
    'ZUSTAENDIG_PHONE': '',
    'ZUSTAENDIG_TELEFON': ''
}
