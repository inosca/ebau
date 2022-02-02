# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_dms_placeholders[Municipality] 1'] = {
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
            'FRIST': '13.09.2021',
            'NAME': 'Tiffany Brown MD'
        },
        {
            'FRIST': '10.09.2021',
            'NAME': 'Melissa Coleman'
        }
    ],
    'CIRCULATION_PREAVIS': [
        {
            'ANTWORT': 'Austin Snyder',
            'NEBENBESTIMMUNGEN': 'Indicate whether especially design.',
            'STELLUNGNAHME': 'Reveal analysis candidate unit knowledge American statement.',
            'VON': 'David Brown'
        },
        {
            'ANTWORT': 'Sydney Colon',
            'NEBENBESTIMMUNGEN': 'Father pick throughout region prevent important positive husband.',
            'STELLUNGNAHME': 'Surface system gas evening game understand.',
            'VON': 'Mr. Thomas Schroeder DDS'
        }
    ],
    'CIRCULATION_PREF': [
        {
            'FRIST': '02.09.2021',
            'NAME': 'James Mathis'
        },
        {
            'FRIST': '28.09.2021',
            'NAME': 'Christine Bean'
        }
    ],
    'CIRCULATION_SERVICES': [
        {
            'FRIST': '08.09.2021',
            'NAME': 'Mr. Thomas Schroeder DDS'
        }
    ],
    'COMMUNE': 'Burgdorf',
    'COMMUNE_ADRESSE': 'New Jill',
    'COMMUNE_ADRESSE_1': '',
    'COMMUNE_ADRESSE_2': 'New Jill',
    'COMMUNE_EMAIL': 'michael98@example.org',
    'COMMUNE_LIEU': 'New Jill',
    'COMMUNE_NOM_ADRESSE': 'Gemeinde Burgdorf, New Jill',
    'COMMUNE_TELEPHONE': '',
    'COMMUNICATION_AUX_VOISINS_CODE_QR': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADG0lEQVR4nO2bQa6jMAyGPw9Ib5lK7wA9SrjBHGk0R5obwFF6gErJslKQZ5EEaDWbN62AV8wCQcsnEsUy9m9HlC8fw4+vM2CQQQYZZJBBBr0nJOVokS62iEgLQz1JF+sD3SbDM2h9yKuqagDtXcon+RUArwmgUVVVvYfWG55B60OxOIDsI7ooor/PCYbTKADFb2w1PINWg9qHeyUCuICAoNCovORNBn1TaDincuVVFX95tJmXvcmgXUJ1vZ0CkewZAFDiZxL/h3q7xfAM2goaRETkBPjQZM8g3eKxMacaWw3PoLV9xOwAFBLgEgo3UeIoxYNsMTyDNoKkiy0Q5T6IbFQ6pwqMAnHyG99iTgb9H0TRGVw5ZT1CtTqKHsAH0N6pZt2i3/mcDHoGqhZBo3X1G8WH+rfXhPbzv2YR7w5NuUYA3LUtegRNgviZhPipgrsKuGt9eOdzMugZqPgIH5opeCxXqqHRIkoEypfEfMRRoOEEOZjwYZRczSgC9ij5gzGYin0IKPuIOZgAl5idgvbAMsAwH/Hu0CKyLHVONxU7A1NkWXKNfJhFHATS3/Kh+MtHTkFLRgqlLp5Fie2GZ9A60EKzFNxVFG4CbmyXyQVNAhoV3687PINWh8qaDx0osUVwVxRGdPhZTKUo27GtVdGdz8mgZ6ASWfbMoWRVqHyonVNZsMpipsURbw6xWPNJqcwipYZqJZptwyziCNCUfaZqG7Wdcm67LMmoZZ+HgKbsEyjFjbnCsfySmEUcBKo+Itz7g0nZzvJ2Lopa7fMIUM41BJda8ZcWHc6phXiiaFXuJhAFcFNnzc7nZNAz0ELFrnFEbY3ITRJQe3DVfMRxoHlPF5OAXdouVRVia5Wug0F+DiZyf13Rs0unnUuLCsd3mZNBT0F1TxfD+ZavtHe3YgyD3DdgfpM5GfQSyF/axd4+iB8lzRhsJ/AhIemoeegicGCUWiZ/2ZsM2if0uKdLh7NCbpcIp1zkEh9Qmdrtdj8ng56BHjXLKknVUHLKSGeN27LPt4b+uadLy0+1B3d5te7wDDLIIIMMMsigHUN/AYOiOcBhfa4tAAAAAElFTkSuQmCC',
    'COMMUNICATION_AUX_VOISINS_LIEN': 'http://caluma-portal.local/public-instances/1/form?key=5a49823',
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
    'DISPOSITIONS_ANNEXES': 'Indicate whether especially design.',
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
            'BETRAG': '152.25',
            'POSITION': ''
        },
        {
            'BETRAG': '111.84',
            'POSITION': ''
        }
    ],
    'EIGENE_GEBUEHREN_TOTAL': '264.09',
    'EIGENE_NEBENBESTIMMUNGEN': 'Indicate whether especially design.',
    'EIGENE_STELLUNGNAHMEN': 'Reveal analysis candidate unit knowledge American statement.',
    'EINSPRECHENDE': [
        {
            'ADDRESS': 'Teststrasse 1, 1234 Testdorf',
            'ADRESSE': 'Teststrasse 1, 1234 Testdorf',
            'NAME': 'Test AG, Müller Hans',
            'NOM': 'Test AG, Müller Hans'
        },
        {
            'ADDRESS': 'Bahnhofstrasse 32, 9874 Testingen',
            'ADRESSE': 'Bahnhofstrasse 32, 9874 Testingen',
            'NAME': 'Muster Max',
            'NOM': 'Muster Max'
        }
    ],
    'EMAIL': '',
    'EMOLUMENTS': [
        {
            'BETRAG': '680.18',
            'POSITION': ''
        },
        {
            'BETRAG': '473.13',
            'POSITION': ''
        },
        {
            'BETRAG': '152.25',
            'POSITION': ''
        },
        {
            'BETRAG': '111.84',
            'POSITION': ''
        }
    ],
    'EMOLUMENTS_TOTAL': '1’417.40',
    'ETAT': 'David Rangel',
    'FACHSTELLEN_KANTONAL': [
        {
            'FRIST': '02.09.2021',
            'NAME': 'James Mathis'
        },
        {
            'FRIST': '16.09.2021',
            'NAME': 'David Brown'
        },
        {
            'FRIST': '08.09.2021',
            'NAME': 'Mr. Thomas Schroeder DDS'
        },
        {
            'FRIST': '28.09.2021',
            'NAME': 'Christine Bean'
        },
        {
            'FRIST': '13.09.2021',
            'NAME': 'Tiffany Brown MD'
        },
        {
            'FRIST': '10.09.2021',
            'NAME': 'Melissa Coleman'
        }
    ],
    'FACHSTELLEN_KANTONAL_LIST': '''- James Mathis
- David Brown
- Mr. Thomas Schroeder DDS
- Christine Bean
- Tiffany Brown MD
- Melissa Coleman''',
    'FACHSTELLEN_KANTONAL_LISTE': '''- James Mathis
- David Brown
- Mr. Thomas Schroeder DDS
- Christine Bean
- Tiffany Brown MD
- Melissa Coleman''',
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
            'BETRAG': '680.18',
            'POSITION': ''
        },
        {
            'BETRAG': '473.13',
            'POSITION': ''
        },
        {
            'BETRAG': '152.25',
            'POSITION': ''
        },
        {
            'BETRAG': '111.84',
            'POSITION': ''
        }
    ],
    'GEBUEHREN_TOTAL': '1’417.40',
    'GEMEINDE': 'Burgdorf',
    'GEMEINDE_ADRESSE': 'New Jill',
    'GEMEINDE_ADRESSE_1': '',
    'GEMEINDE_ADRESSE_2': 'New Jill',
    'GEMEINDE_EMAIL': 'michael98@example.org',
    'GEMEINDE_NAME_ADRESSE': 'Gemeinde Burgdorf, New Jill',
    'GEMEINDE_ORT': 'New Jill',
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
    'INFORMATION_OF_NEIGHBORS_LINK': 'http://caluma-portal.local/public-instances/1/form?key=5a49823',
    'INFORMATION_OF_NEIGHBORS_QR_CODE': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADG0lEQVR4nO2bQa6jMAyGPw9Ib5lK7wA9SrjBHGk0R5obwFF6gErJslKQZ5EEaDWbN62AV8wCQcsnEsUy9m9HlC8fw4+vM2CQQQYZZJBBBr0nJOVokS62iEgLQz1JF+sD3SbDM2h9yKuqagDtXcon+RUArwmgUVVVvYfWG55B60OxOIDsI7ooor/PCYbTKADFb2w1PINWg9qHeyUCuICAoNCovORNBn1TaDincuVVFX95tJmXvcmgXUJ1vZ0CkewZAFDiZxL/h3q7xfAM2goaRETkBPjQZM8g3eKxMacaWw3PoLV9xOwAFBLgEgo3UeIoxYNsMTyDNoKkiy0Q5T6IbFQ6pwqMAnHyG99iTgb9H0TRGVw5ZT1CtTqKHsAH0N6pZt2i3/mcDHoGqhZBo3X1G8WH+rfXhPbzv2YR7w5NuUYA3LUtegRNgviZhPipgrsKuGt9eOdzMugZqPgIH5opeCxXqqHRIkoEypfEfMRRoOEEOZjwYZRczSgC9ij5gzGYin0IKPuIOZgAl5idgvbAMsAwH/Hu0CKyLHVONxU7A1NkWXKNfJhFHATS3/Kh+MtHTkFLRgqlLp5Fie2GZ9A60EKzFNxVFG4CbmyXyQVNAhoV3687PINWh8qaDx0osUVwVxRGdPhZTKUo27GtVdGdz8mgZ6ASWfbMoWRVqHyonVNZsMpipsURbw6xWPNJqcwipYZqJZptwyziCNCUfaZqG7Wdcm67LMmoZZ+HgKbsEyjFjbnCsfySmEUcBKo+Itz7g0nZzvJ2Lopa7fMIUM41BJda8ZcWHc6phXiiaFXuJhAFcFNnzc7nZNAz0ELFrnFEbY3ITRJQe3DVfMRxoHlPF5OAXdouVRVia5Wug0F+DiZyf13Rs0unnUuLCsd3mZNBT0F1TxfD+ZavtHe3YgyD3DdgfpM5GfQSyF/axd4+iB8lzRhsJ/AhIemoeegicGCUWiZ/2ZsM2if0uKdLh7NCbpcIp1zkEh9Qmdrtdj8ng56BHjXLKknVUHLKSGeN27LPt4b+uadLy0+1B3d5te7wDDLIIIMMMsigHUN/AYOiOcBhfa4tAAAAAElFTkSuQmCC',
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
    'LEITPERSON': 'Nicole Rodriguez',
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
            'BETRAG': '152.25',
            'POSITION': ''
        },
        {
            'BETRAG': '111.84',
            'POSITION': ''
        }
    ],
    'MES_EMOLUMENTS_TOTAL': '264.09',
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
    'MOTS_CLES': 'Kevin Flores, Jack Moore, Thomas Johnson, Mario Mann, Antonio Thornton',
    'MUNICIPALITY': 'Burgdorf',
    'MUNICIPALITY_ADDRESS': 'New Jill',
    'NACHBARSCHAFTSORIENTIERUNG_LINK': 'http://caluma-portal.local/public-instances/1/form?key=5a49823',
    'NACHBARSCHAFTSORIENTIERUNG_QR_CODE': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADG0lEQVR4nO2bQa6jMAyGPw9Ib5lK7wA9SrjBHGk0R5obwFF6gErJslKQZ5EEaDWbN62AV8wCQcsnEsUy9m9HlC8fw4+vM2CQQQYZZJBBBr0nJOVokS62iEgLQz1JF+sD3SbDM2h9yKuqagDtXcon+RUArwmgUVVVvYfWG55B60OxOIDsI7ooor/PCYbTKADFb2w1PINWg9qHeyUCuICAoNCovORNBn1TaDincuVVFX95tJmXvcmgXUJ1vZ0CkewZAFDiZxL/h3q7xfAM2goaRETkBPjQZM8g3eKxMacaWw3PoLV9xOwAFBLgEgo3UeIoxYNsMTyDNoKkiy0Q5T6IbFQ6pwqMAnHyG99iTgb9H0TRGVw5ZT1CtTqKHsAH0N6pZt2i3/mcDHoGqhZBo3X1G8WH+rfXhPbzv2YR7w5NuUYA3LUtegRNgviZhPipgrsKuGt9eOdzMugZqPgIH5opeCxXqqHRIkoEypfEfMRRoOEEOZjwYZRczSgC9ij5gzGYin0IKPuIOZgAl5idgvbAMsAwH/Hu0CKyLHVONxU7A1NkWXKNfJhFHATS3/Kh+MtHTkFLRgqlLp5Fie2GZ9A60EKzFNxVFG4CbmyXyQVNAhoV3687PINWh8qaDx0osUVwVxRGdPhZTKUo27GtVdGdz8mgZ6ASWfbMoWRVqHyonVNZsMpipsURbw6xWPNJqcwipYZqJZptwyziCNCUfaZqG7Wdcm67LMmoZZ+HgKbsEyjFjbnCsfySmEUcBKo+Itz7g0nZzvJ2Lopa7fMIUM41BJda8ZcWHc6phXiiaFXuJhAFcFNnzc7nZNAz0ELFrnFEbY3ITRJQe3DVfMRxoHlPF5OAXdouVRVia5Wug0F+DiZyf13Rs0unnUuLCsd3mZNBT0F1TxfD+ZavtHe3YgyD3DdgfpM5GfQSyF/axd4+iB8lzRhsJ/AhIemoeegicGCUWiZ/2ZsM2if0uKdLh7NCbpcIp1zkEh9Qmdrtdj8ng56BHjXLKknVUHLKSGeN27LPt4b+uadLy0+1B3d5te7wDDLIIIMMMsigHUN/AYOiOcBhfa4tAAAAAElFTkSuQmCC',
    'NAME': '',
    'NEBENBESTIMMUNGEN': 'Indicate whether especially design.',
    'NEBENBESTIMMUNGEN_MAPPED': [
        {
            'FACHSTELLE': 'David Brown',
            'TEXT': 'Indicate whether especially design.'
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
            'FRIST': '02.09.2021',
            'NAME': 'James Mathis'
        },
        {
            'FRIST': '16.09.2021',
            'NAME': 'David Brown'
        },
        {
            'FRIST': '08.09.2021',
            'NAME': 'Mr. Thomas Schroeder DDS'
        },
        {
            'FRIST': '28.09.2021',
            'NAME': 'Christine Bean'
        },
        {
            'FRIST': '13.09.2021',
            'NAME': 'Tiffany Brown MD'
        },
        {
            'FRIST': '10.09.2021',
            'NAME': 'Melissa Coleman'
        }
    ],
    'OFFICES_CANTONAUX_LISTE': '''- James Mathis
- David Brown
- Mr. Thomas Schroeder DDS
- Christine Bean
- Tiffany Brown MD
- Melissa Coleman''',
    'OPPOSANTS': [
        {
            'ADDRESS': 'Teststrasse 1, 1234 Testdorf',
            'ADRESSE': 'Teststrasse 1, 1234 Testdorf',
            'NAME': 'Test AG, Müller Hans',
            'NOM': 'Test AG, Müller Hans'
        },
        {
            'ADDRESS': 'Bahnhofstrasse 32, 9874 Testingen',
            'ADRESSE': 'Bahnhofstrasse 32, 9874 Testingen',
            'NAME': 'Muster Max',
            'NOM': 'Muster Max'
        }
    ],
    'OPPOSING': [
        {
            'ADDRESS': 'Teststrasse 1, 1234 Testdorf',
            'ADRESSE': 'Teststrasse 1, 1234 Testdorf',
            'NAME': 'Test AG, Müller Hans',
            'NOM': 'Test AG, Müller Hans'
        },
        {
            'ADDRESS': 'Bahnhofstrasse 32, 9874 Testingen',
            'ADRESSE': 'Bahnhofstrasse 32, 9874 Testingen',
            'NAME': 'Muster Max',
            'NOM': 'Muster Max'
        }
    ],
    'OUTSIDE_SEATING': 20,
    'OUVERTURE_PUBLIC': 'Öffentlich',
    'PARCELLE': '473, 2592',
    'PARZELLE': '473, 2592',
    'PLACES_ASSISES_EXT': 20,
    'PLACES_ASSISES_INT': 35,
    'PLAN_QUARTIER': 'Überbauung XY',
    'PRISE_DE_POSITION': 'Reveal analysis candidate unit knowledge American statement.',
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
    'RESPONSABLE_AUTORITE_DIRECTRICE': 'Nicole Rodriguez',
    'RESPONSABLE_EMAIL': 'cody51@example.com',
    'RESPONSABLE_NOM': 'Nicole Rodriguez',
    'RESPONSABLE_TELEPHONE': '',
    'SACHVERHALT': 'Sachverhalt Test',
    'SCHUTZZONE': 'S1',
    'SECTEUR_PROTECTION_EAUX': 'Aᵤ',
    'SITUATION': 'Sachverhalt Test',
    'SITZPLAETZE_AUSSEN': 20,
    'SITZPLAETZE_INNEN': 35,
    'SPRACHE': 'de',
    'STATUS': 'David Rangel',
    'STELLUNGNAHME': 'Reveal analysis candidate unit knowledge American statement.',
    'STICHWORTE': 'Kevin Flores, Jack Moore, Thomas Johnson, Mario Mann, Antonio Thornton',
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
            'FRIST': '02.09.2021',
            'NAME': 'James Mathis'
        },
        {
            'FRIST': '16.09.2021',
            'NAME': 'David Brown'
        },
        {
            'FRIST': '08.09.2021',
            'NAME': 'Mr. Thomas Schroeder DDS'
        },
        {
            'FRIST': '28.09.2021',
            'NAME': 'Christine Bean'
        },
        {
            'FRIST': '13.09.2021',
            'NAME': 'Tiffany Brown MD'
        },
        {
            'FRIST': '10.09.2021',
            'NAME': 'Melissa Coleman'
        }
    ],
    'ZIRKULATION_FACHSTELLEN': [
        {
            'FRIST': '08.09.2021',
            'NAME': 'Mr. Thomas Schroeder DDS'
        }
    ],
    'ZIRKULATION_GEMEINDEN': [
        {
            'FRIST': '13.09.2021',
            'NAME': 'Tiffany Brown MD'
        },
        {
            'FRIST': '10.09.2021',
            'NAME': 'Melissa Coleman'
        }
    ],
    'ZIRKULATION_RSTA': [
        {
            'FRIST': '02.09.2021',
            'NAME': 'James Mathis'
        },
        {
            'FRIST': '28.09.2021',
            'NAME': 'Christine Bean'
        }
    ],
    'ZIRKULATION_RUECKMELDUNGEN': [
        {
            'ANTWORT': 'Austin Snyder',
            'NEBENBESTIMMUNGEN': 'Indicate whether especially design.',
            'STELLUNGNAHME': 'Reveal analysis candidate unit knowledge American statement.',
            'VON': 'David Brown'
        },
        {
            'ANTWORT': 'Sydney Colon',
            'NEBENBESTIMMUNGEN': 'Father pick throughout region prevent important positive husband.',
            'STELLUNGNAHME': 'Surface system gas evening game understand.',
            'VON': 'Mr. Thomas Schroeder DDS'
        }
    ],
    'ZONE_PROTEGEE': 'S1',
    'ZUSTAENDIG_EMAIL': 'cody51@example.com',
    'ZUSTAENDIG_NAME': 'Nicole Rodriguez',
    'ZUSTAENDIG_PHONE': '',
    'ZUSTAENDIG_TELEFON': ''
}

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
    'ALLE_NACHBARN': '',
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
    'BASE_URL': 'http://camac-ng.local',
    'BAUEINGABE_DATUM': '30. August 2021',
    'BAUENTSCHEID': '',
    'BAUENTSCHEID_ABSCHREIBUNGSVERFUEGUNG': False,
    'BAUENTSCHEID_BAUABSCHLAG': False,
    'BAUENTSCHEID_BAUABSCHLAG_MIT_WHST': False,
    'BAUENTSCHEID_BAUABSCHLAG_OHNE_WHST': False,
    'BAUENTSCHEID_BAUBEWILLIGUNG': False,
    'BAUENTSCHEID_BAUBEWILLIGUNGSFREI': False,
    'BAUENTSCHEID_DATUM': '',
    'BAUENTSCHEID_GENERELL': False,
    'BAUENTSCHEID_GESAMT': False,
    'BAUENTSCHEID_KLEIN': False,
    'BAUENTSCHEID_POSITIV': False,
    'BAUENTSCHEID_POSITIV_TEILWEISE': False,
    'BAUENTSCHEID_PROJEKTAENDERUNG': False,
    'BAUENTSCHEID_TEILBAUBEWILLIGUNG': False,
    'BAUENTSCHEID_TYP': '',
    'BAUENTSCHEID_TYPE': '',
    'BAUVORHABEN': '',
    'BESCHREIBUNG_BAUVORHABEN': '',
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
    'DECISION_GENERAL': False,
    'DECISION_GLOBALE': False,
    'DECISION_MODIF': False,
    'DECISION_PARTIEL': False,
    'DECISION_PERMIS': False,
    'DECISION_PETIT': False,
    'DECISION_REFUS': False,
    'DECISION_REFUS_AVEC_RET': False,
    'DECISION_REFUS_SANS_RET': False,
    'DECISION_TYPE': '',
    'DEPOT_DEMANDE_DATE': '30. August 2021',
    'DISPOSITIONS_ANNEXES': '',
    'DOSSIER_LINK': 'http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1',
    'DOSSIER_NR': 1,
    'DOSSIER_NUMERO': 1,
    'DOSSIER_TYP': 'Baugesuch',
    'DOSSIER_TYPE': 'Baugesuch',
    'EBAU_NR': '',
    'EBAU_NUMBER': '',
    'EBAU_NUMERO': '',
    'EBAU_URL': 'http://camac-ng.local',
    'EIGENE_GEBUEHREN': [
    ],
    'EIGENE_GEBUEHREN_TOTAL': '0.00',
    'EIGENE_NEBENBESTIMMUNGEN': '',
    'EIGENE_STELLUNGNAHMEN': '',
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
    'NEIGHBORS': '',
    'NOM_LEGAL': '',
    'NUTZUNG': '',
    'NUTZUNGSZONE': '',
    'OEFFENTLICHKEIT': '',
    'OFFICES_CANTONAUX': [
    ],
    'OFFICES_CANTONAUX_LISTE': '',
    'OPPOSANTS': [
    ],
    'OPPOSING': [
    ],
    'OUTSIDE_SEATING': '',
    'OUVERTURE_PUBLIC': '',
    'PARCELLE': '',
    'PARZELLE': '',
    'PLACES_ASSISES_EXT': '',
    'PLACES_ASSISES_INT': '',
    'PLAN_QUARTIER': '',
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
    'PUBLIKATION_START': '',
    'PUBLIKATION_TEXT': '',
    'RECENSEMENT': '',
    'REPRESENTANT': '',
    'REPRESENTANT_ADRESSE_1': '',
    'REPRESENTANT_ADRESSE_2': '',
    'REPRESENTANT_NOM_ADRESSE': '',
    'REPRESENTANT_TOUS': '',
    'REPRESENTANT_TOUS_NOM_ADRESSE': '',
    'REQUERANT': '',
    'REQUERANT_ADRESSE_1': '',
    'REQUERANT_ADRESSE_2': '',
    'REQUERANT_NOM_ADRESSE': '',
    'REQUERANT_TOUS': '',
    'REQUERANT_TOUS_NOM_ADRESSE': '',
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
    'VOISINS_TOUS': '',
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
