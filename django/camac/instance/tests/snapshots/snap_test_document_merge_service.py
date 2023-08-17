# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['test_document_merge_service_cover_sheet_with_header_values 1'] = {
    'addressHeader': 'Bahnhofstrasse 2, Testhausen',
    'addressHeaderLabel': 'Adresse',
    'applicantHeader': 'Test AG, Foo Bar',
    'applicantHeaderLabel': 'Gesuchsteller/in',
    'applicants': [
        {
            'first_name': 'Foo',
            'full_name': 'Test AG, Foo Bar',
            'is_juristic_person': True,
            'juristic_name': 'Test AG',
            'last_name': 'Bar',
            'street': ' ',
            'street_number': ' ',
            'town': ' ',
            'zip': ' '
        }
    ],
    'authorityHeader': 'Rebecca Gonzalez',
    'authorityHeaderLabel': 'Leitbehörde',
    'caseId': 1,
    'caseType': 'Baugesuch',
    'coordEast': '',
    'coordNorth': '',
    'createdAt': 'Erstellt am 03.08.2022 um 09:19',
    'descriptionHeader': 'Bau Einfamilienhaus',
    'descriptionHeaderLabel': 'Beschreibung',
    'documents': [
    ],
    'dossierNr': '2021-99',
    'formType': None,
    'generatedAt': 'Generiert am 07.09.2022 um 14:01',
    'inputDateHeader': GenericRepr('FakeDatetime(2021, 1, 1, 0, 0)'),
    'inputDateHeaderLabel': 'Eingangsdatum',
    'landownerHeaderLabel': 'Grundeigentümer/in',
    'landowners': [
    ],
    'modificationHeader': 'Anbau Haus',
    'modificationHeaderLabel': 'Projektänderung',
    'modifiedAt': 'Zuletzt bearbeitet am 06.09.2022 um 15:37',
    'municipality': 'Testhausen',
    'municipalityHeader': 'Testhausen',
    'municipalityHeaderLabel': 'Gemeinde',
    'paperInputDateHeader': GenericRepr('FakeDatetime(2021, 1, 2, 0, 0)'),
    'plotsHeader': '123',
    'plotsHeaderLabel': 'Parzelle(n)',
    'projectAuthorHeaderLabel': 'Projektverfasser/in',
    'projectAuthors': [
    ],
    'responsibleHeader': 'testuser',
    'responsibleHeaderLabel': 'Zuständig',
    'signatureMetadata': 'Ort und Datum',
    'signatureSectionTitle': 'Unterschriften',
    'signatureTitle': 'Unterschrift',
    'tagHeader': 'some tag',
    'tagHeaderLabel': 'Stichworte'
}

snapshots['test_document_merge_service_cover_sheet_without_header_values 1'] = {
    'addressHeader': '',
    'addressHeaderLabel': 'Adresse',
    'applicantHeader': '',
    'applicantHeaderLabel': 'Gesuchsteller/in',
    'applicants': [
    ],
    'authorityHeader': None,
    'authorityHeaderLabel': 'Leitbehörde',
    'caseId': 1,
    'caseType': 'Baugesuch',
    'coordEast': '',
    'coordNorth': '',
    'createdAt': 'Erstellt am 06.09.2022 um 15:37',
    'descriptionHeader': None,
    'descriptionHeaderLabel': 'Beschreibung',
    'documents': [
    ],
    'dossierNr': None,
    'formType': None,
    'generatedAt': 'Generiert am 06.09.2022 um 15:37',
    'inputDateHeader': GenericRepr('FakeDatetime(2021, 1, 1, 0, 0)'),
    'inputDateHeaderLabel': 'Eingangsdatum',
    'landownerHeaderLabel': 'Grundeigentümer/in',
    'landowners': [
    ],
    'modificationHeader': None,
    'modificationHeaderLabel': 'Projektänderung',
    'modifiedAt': 'Zuletzt bearbeitet am 06.09.2022 um 15:37',
    'municipality': None,
    'municipalityHeader': None,
    'municipalityHeaderLabel': 'Gemeinde',
    'paperInputDateHeader': None,
    'plotsHeader': '',
    'plotsHeaderLabel': 'Parzelle(n)',
    'projectAuthorHeaderLabel': 'Projektverfasser/in',
    'projectAuthors': [
    ],
    'responsibleHeader': None,
    'responsibleHeaderLabel': 'Zuständig',
    'signatureMetadata': 'Ort und Datum',
    'signatureSectionTitle': 'Unterschriften',
    'signatureTitle': 'Unterschrift',
    'tagHeader': None,
    'tagHeaderLabel': 'Stichworte'
}

snapshots['test_document_merge_service_snapshot baugesuch'] = [
    {
        'children': [
            {
                'children': [
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Wurden Vorabklärungen durchgeführt?',
                        'slug': 'wurden-vorabklaerungen-durchgefuehrt',
                        'type': 'ChoiceQuestion'
                    }
                ],
                'label': 'Durchgeführte Vorabklärungen',
                'slug': 'durchgefuehrte-vorabklaerungen',
                'type': 'FormQuestion'
            },
            {
                'children': [
                    {
                        'columns': [
                            'Handelt es sich um eine juristische Person?',
                            'Name juristische Person',
                            'Name',
                            'Vorname',
                            'Strasse',
                            'Nummer',
                            'PLZ',
                            'Ort',
                            'Telefon oder Mobile',
                            'E-Mail',
                            'Hinweis Gesuchsteller/in',
                            'Vertreter/in?'
                        ],
                        'label': 'Gesuchsteller/in',
                        'rows': [
                            [
                                {
                                    'label': 'Handelt es sich um eine juristische Person?',
                                    'slug': 'juristische-person-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': 'Nein'
                                },
                                {
                                    'label': 'Name',
                                    'slug': 'name-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': 'Meier'
                                },
                                {
                                    'label': 'Vorname',
                                    'slug': 'vorname-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': 'Hans'
                                },
                                {
                                    'label': 'Strasse',
                                    'slug': 'strasse-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': 'Strasse'
                                },
                                {
                                    'label': 'Nummer',
                                    'slug': 'nummer-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': '33'
                                },
                                {
                                    'label': 'PLZ',
                                    'slug': 'plz-gesuchstellerin',
                                    'type': 'IntegerQuestion',
                                    'value': 3000
                                },
                                {
                                    'label': 'Ort',
                                    'slug': 'ort-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': 'Bern'
                                },
                                {
                                    'label': 'Telefon oder Mobile',
                                    'slug': 'telefon-oder-mobile-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': '0999999999'
                                },
                                {
                                    'label': 'E-Mail',
                                    'slug': 'e-mail-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': 'test@example.ch'
                                }
                            ]
                        ],
                        'slug': 'personalien-gesuchstellerin',
                        'type': 'TableQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': True,
                                'label': 'Ja'
                            },
                            {
                                'checked': False,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Ist die verantwortliche Person für die Selbstdeklaration Baukontrolle identisch mit dem/r Gesuchsteller/in?',
                        'slug': 'verantwortliche-person-sb-identisch',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Vertreter/in mit Vollmacht'
                            },
                            {
                                'checked': False,
                                'label': 'Projektverfasser/in'
                            },
                            {
                                'checked': False,
                                'label': 'Grundeigentümer/in (falls nicht mit Gesuchsteller/in identisch)'
                            },
                            {
                                'checked': False,
                                'label': 'Gebäudeeigentümer/in (falls nicht mit Gesuchsteller/in identisch)'
                            }
                        ],
                        'label': 'Sind neben den Gesuchstellenden weitere Personen beteiligt?',
                        'slug': 'weitere-personen',
                        'type': 'MultipleChoiceQuestion'
                    }
                ],
                'label': 'Personalien',
                'slug': 'personalien',
                'type': 'FormQuestion'
            },
            {
                'children': [
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Neubau'
                            },
                            {
                                'checked': True,
                                'label': 'Um- / Ausbau'
                            },
                            {
                                'checked': False,
                                'label': 'Umnutzung'
                            },
                            {
                                'checked': False,
                                'label': 'Erweiterung / Anbau'
                            },
                            {
                                'checked': False,
                                'label': 'Abbruch'
                            },
                            {
                                'checked': False,
                                'label': 'Technische Anlage'
                            },
                            {
                                'checked': False,
                                'label': 'Reklame'
                            },
                            {
                                'checked': False,
                                'label': 'Tiefbauanlage'
                            },
                            {
                                'checked': False,
                                'label': 'Andere'
                            }
                        ],
                        'label': 'Baubeschrieb',
                        'slug': 'baubeschrieb',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'label': 'Beschreibung',
                        'slug': 'beschreibung-bauvorhaben',
                        'type': 'TextareaQuestion',
                        'value': 'Testanfrage'
                    },
                    {
                        'label': 'Bisherige Nutzung',
                        'slug': 'bisherige-nutzung',
                        'type': 'TextareaQuestion',
                        'value': None
                    },
                    {
                        'content': None,
                        'label': 'Tragkonstruktion',
                        'slug': 'tragkonstruktion',
                        'type': 'StaticQuestion'
                    },
                    {
                        'label': 'System der Fundation',
                        'slug': 'fundation-system',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'label': 'Stützen',
                        'slug': 'tragkonstruktion-stuetzen',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'label': 'Wände',
                        'slug': 'tragkonstruktion-waende',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'label': 'Decken',
                        'slug': 'tragkonstruktion-decken',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'content': None,
                        'label': 'Fassaden',
                        'slug': 'fassaden',
                        'type': 'StaticQuestion'
                    },
                    {
                        'label': 'Material',
                        'slug': 'fassaden-material',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'label': 'Farbe',
                        'slug': 'fassaden-farbe',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'content': None,
                        'label': 'Dach',
                        'slug': 'dach',
                        'type': 'StaticQuestion'
                    },
                    {
                        'label': 'Form',
                        'slug': 'dach-form',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'label': 'Neigung',
                        'slug': 'dach-neigung',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'label': 'Material',
                        'slug': 'dach-material',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'label': 'Farbe',
                        'slug': 'dach-farbe',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Rammen'
                            },
                            {
                                'checked': False,
                                'label': 'Pfählen'
                            },
                            {
                                'checked': False,
                                'label': 'Sprengen'
                            }
                        ],
                        'label': 'Vorbereitende Sicherungsmassnahmen',
                        'slug': 'vorbereitende-massnahmen',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'label': 'Baukosten in CHF',
                        'slug': 'baukosten-in-chf',
                        'type': 'IntegerQuestion',
                        'value': 10000
                    },
                    {
                        'label': 'Baukosten total, inkl. Erschliessung, ohne Landerwerb in CHF',
                        'slug': 'baukosten-total-chf',
                        'type': 'IntegerQuestion',
                        'value': None
                    },
                    {
                        'label': 'Gebäudevolumen GV nach SN 504 416 in m³',
                        'slug': 'gebaeudevolumen',
                        'type': 'FloatQuestion',
                        'value': None
                    },
                    {
                        'label': 'Baukosten total, inkl. Erschliessung, ohne Landerwerb pro m³ in CHF',
                        'slug': 'baukosten-total-pro-m3',
                        'type': 'CalculatedFloatQuestion'
                    },
                    {
                        'label': 'Geplanter Baustart',
                        'slug': 'geplanter-baustart',
                        'type': 'DateQuestion',
                        'value': None
                    },
                    {
                        'label': 'Dauer in Monaten',
                        'slug': 'dauer-in-monaten',
                        'type': 'IntegerQuestion',
                        'value': None
                    }
                ],
                'label': 'Bauvorhaben',
                'slug': 'bauvorhaben',
                'type': 'FormQuestion'
            }
        ],
        'label': 'Allgemeine Informationen',
        'slug': '1-allgemeine-informationen',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'children': [
                    {
                        'choices': [
                            {
                                'checked': True,
                                'label': 'Wohnen'
                            },
                            {
                                'checked': False,
                                'label': 'Industrie'
                            },
                            {
                                'checked': False,
                                'label': 'Gewerbe'
                            },
                            {
                                'checked': False,
                                'label': 'Dienstleistung'
                            },
                            {
                                'checked': False,
                                'label': 'Verkauf'
                            },
                            {
                                'checked': False,
                                'label': 'Lager'
                            },
                            {
                                'checked': False,
                                'label': 'Landwirtschaft'
                            },
                            {
                                'checked': False,
                                'label': 'Gastgewerbe'
                            },
                            {
                                'checked': False,
                                'label': 'Andere (z.B. Tiefbauanlage, Reklamevorhaben, ...)'
                            }
                        ],
                        'label': 'Für welche Nutzungsart dient das Bauvorhaben?',
                        'slug': 'nutzungsart',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'EFH'
                            },
                            {
                                'checked': True,
                                'label': 'MFH'
                            }
                        ],
                        'label': 'Um was für ein Gebäude handelt es sich?',
                        'slug': 'um-was-fuer-ein-gebaeude-handelt-es-sich',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Öl- oder Gasfeuerungen mit einer Feuerungswärmeleistung ≥ 350 kW'
                            },
                            {
                                'checked': False,
                                'label': 'Holzfeuerungen mit einer Feuerungswärmeleistung ≥ 70 kW'
                            },
                            {
                                'checked': False,
                                'label': 'Pellet-, Späne- oder Schnitzelfeuerungsanlage'
                            }
                        ],
                        'label': 'Umfasst das Vorhaben folgende Feuerungsanlagen?',
                        'slug': 'feuerungsanlagen',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Handelt es sich um ein landwirtschaftliches Bauvorhaben mit Ableitung (Abwasser aus Wohn- und/oder Ökonomieanteil) in eine Güllegrube?',
                        'slug': 'ableitung-in-guellegrube',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Sind Belange des Gewässerschutzes betroffen?',
                        'slug': 'sind-belange-des-gewasserschutzes-betroffen',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Ist ein Schutzraum für das entsprechende Baugesuch Pflicht?',
                        'slug': 'schutzraum-pflicht',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Handelt es sich um eine Anlage, in welcher mit gentechnisch veränderten oder pathogenen Organismen (Klasse 3 oder 4) Tätigkeiten durchgeführt werden?',
                        'slug': 'gentechnisch-veraenderte-pathogene-organismen',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Befindet sich das Bauvorhaben im Wald / Wytweide oder innerhalb von 30 m Abstand zum Wald / Wytweide?',
                        'slug': 'bau-im-wald-oder-innerhalb-von-30-m-abstand',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Gibt es bewilligungspflichtige Reklame?',
                        'slug': 'gibt-es-bewilligungspflichtige-reklame',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Ist beim Bauvorhaben mit Bauabfällen zu rechnen (inklusive Boden)?',
                        'slug': 'ist-mit-bauabfaellen-zu-rechnen',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Ist das Vorhaben energierelevant?',
                        'slug': 'ist-das-vorhaben-energierelevant',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Naturgefahren: Handelt es sich um ein sensibles Objekt?',
                        'slug': 'handelt-es-sich-um-ein-sensibles-objekt',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': False,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Ist durch das Bauvorhaben Boden betroffen?',
                        'slug': 'ist-durch-das-bauvorhaben-boden-betroffen',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Solar- oder Photovoltaik-Anlage'
                            },
                            {
                                'checked': False,
                                'label': 'Sendeanlage'
                            }
                        ],
                        'label': 'Welche der folgenden Anlagen sind geplant?',
                        'slug': 'geplante-anlagen',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Boden / Untergrund'
                            },
                            {
                                'checked': False,
                                'label': 'Wasser'
                            },
                            {
                                'checked': False,
                                'label': 'Luft'
                            }
                        ],
                        'label': 'Welche Wärmepumpen sind im Bauvorhaben vorgesehen?',
                        'slug': 'welche-waermepumpen',
                        'type': 'MultipleChoiceQuestion'
                    }
                ],
                'label': 'Triage',
                'slug': 'triage',
                'type': 'FormQuestion'
            }
        ],
        'label': 'Nutzung Bauvorhaben',
        'slug': '2-nutzung-bauvorhaben',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'children': [
                    {
                        'label': 'Strasse/Flurname',
                        'slug': 'strasse-flurname',
                        'type': 'TextQuestion',
                        'value': 'Teststrasse'
                    },
                    {
                        'label': 'Nr.',
                        'slug': 'nr',
                        'type': 'TextQuestion',
                        'value': '3'
                    },
                    {
                        'label': 'Ort',
                        'slug': 'ort-grundstueck',
                        'type': 'TextQuestion',
                        'value': 'Burgdorf'
                    },
                    {
                        'label': 'Zuständige Gemeinde',
                        'slug': 'gemeinde',
                        'type': 'TextQuestion',
                        'value': 'Burgdorf'
                    },
                    {
                        'columns': [
                            'Parzellennummer',
                            'Grundeigentümer/in',
                            'Liegenschaftsnummer',
                            'Baurecht-Nummer',
                            'E-GRID-Nr.',
                            'Strasse',
                            'Nummer',
                            'PLZ',
                            'Ort',
                            'Lagekoordinaten - Ost',
                            'Lagekoordinaten - Nord'
                        ],
                        'label': 'Parzelle',
                        'rows': [
                            [
                                {
                                    'label': 'Parzellennummer',
                                    'slug': 'parzellennummer',
                                    'type': 'TextQuestion',
                                    'value': '1'
                                },
                                {
                                    'label': 'Grundeigentümer/in',
                                    'slug': 'grundeigentuemerin',
                                    'type': 'TextQuestion',
                                    'value': ''
                                },
                                {
                                    'label': 'Liegenschaftsnummer',
                                    'slug': 'liegenschaftsnummer',
                                    'type': 'IntegerQuestion',
                                    'value': None
                                },
                                {
                                    'label': 'Baurecht-Nummer',
                                    'slug': 'baurecht-nummer',
                                    'type': 'TextQuestion',
                                    'value': None
                                },
                                {
                                    'label': 'E-GRID-Nr.',
                                    'slug': 'e-grid-nr',
                                    'type': 'TextQuestion',
                                    'value': 'CH273589324696'
                                },
                                {
                                    'label': 'Strasse',
                                    'slug': 'strasse-parzelle',
                                    'type': 'TextQuestion',
                                    'value': None
                                },
                                {
                                    'label': 'Nummer',
                                    'slug': 'nummer-parzelle',
                                    'type': 'TextQuestion',
                                    'value': None
                                },
                                {
                                    'label': 'PLZ',
                                    'slug': 'plz-parzelle',
                                    'type': 'IntegerQuestion',
                                    'value': None
                                },
                                {
                                    'label': 'Ort',
                                    'slug': 'ort-parzelle',
                                    'type': 'TextQuestion',
                                    'value': None
                                },
                                {
                                    'label': 'Lagekoordinaten - Ost',
                                    'slug': 'lagekoordinaten-ost',
                                    'type': 'FloatQuestion',
                                    'value': 2614314.0
                                },
                                {
                                    'label': 'Lagekoordinaten - Nord',
                                    'slug': 'lagekoordinaten-nord',
                                    'type': 'FloatQuestion',
                                    'value': 1211926.0
                                }
                            ]
                        ],
                        'slug': 'parzelle',
                        'type': 'TableQuestion'
                    },
                    {
                        'label': 'BE-GID',
                        'slug': 'be-gid',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'label': 'GWR-EGID',
                        'slug': 'gwr-egid',
                        'type': 'IntegerQuestion',
                        'value': None
                    },
                    {
                        'label': 'Ausnützung',
                        'slug': 'ausnuetzung',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'label': 'Grünfläche in m²',
                        'slug': 'gruenflache-in-quadratmeter',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'label': 'Überbauung in %',
                        'slug': 'ueberbauung-in-prozent',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'label': 'Geschossfläche in m²',
                        'slug': 'geschossflaeche-in-quadratmeter',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': False,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Rechtliche Sicherung fremden Bodens?',
                        'slug': 'rechtliche-sicherung-fremden-bodens',
                        'type': 'ChoiceQuestion'
                    }
                ],
                'label': 'Allgemeine Angaben',
                'slug': 'allgemeine-angaben',
                'type': 'FormQuestion'
            },
            {
                'children': [
                    {
                        'label': 'Nutzungszone',
                        'slug': 'nutzungszone',
                        'type': 'TextQuestion',
                        'value': 'Ensembleschutzzone '
                    },
                    {
                        'label': 'Überbauungsordnung',
                        'slug': 'ueberbauungsordnung',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'label': 'Zulässige Geschosszahl',
                        'slug': 'zulaessige-geschosszahl',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'label': 'Empfindlichkeitsstufe (ES)',
                        'slug': 'empfindlichkeitsstufe',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'content': None,
                        'label': 'Dimensionen des Baus',
                        'slug': 'dimensionen-des-baus',
                        'type': 'StaticQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Geringe Höhe bis 11 m'
                            },
                            {
                                'checked': False,
                                'label': 'Mittlere Höhe zwischen 11 m und 30 m'
                            },
                            {
                                'checked': False,
                                'label': 'Grosse Höhe ab 30 m'
                            }
                        ],
                        'label': 'Höhe',
                        'slug': 'hoehe',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'label': 'Effektive Geschosszahl',
                        'slug': 'effektive-geschosszahl',
                        'type': 'IntegerQuestion',
                        'value': None
                    }
                ],
                'label': 'Zonenvorschriften - Baurechtliche Grundordnung',
                'slug': 'zonenvorschriften-baurechtliche-grundordnung',
                'type': 'FormQuestion'
            },
            {
                'children': [
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'S1'
                            },
                            {
                                'checked': False,
                                'label': 'S2/Sh'
                            },
                            {
                                'checked': False,
                                'label': 'S3/Sm'
                            }
                        ],
                        'label': 'Grundwasserschutzzonen / -areale',
                        'slug': 'grundwasserschutzzonen',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'üB'
                            },
                            {
                                'checked': False,
                                'label': 'Aₒ'
                            },
                            {
                                'checked': True,
                                'label': 'Aᵤ'
                            }
                        ],
                        'label': 'Gewässerschutzbereich',
                        'slug': 'gewaesserschutzbereich',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Belasteter Standort?',
                        'slug': 'belasteter-standort',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Bauten (inkl. Pfähle) im Grundwasser oder Grundwasserabsenkung?',
                        'slug': 'bauten-oder-pfaehlen-im-grundwasser',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': True,
                                'label': 'Ja'
                            },
                            {
                                'checked': False,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Gebiet mit bekannten oder vermuteten Naturgefahren',
                        'slug': 'gebiet-mit-naturgefahren',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': True,
                                'label': 'Ja'
                            },
                            {
                                'checked': False,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Handelt es sich bei der Liegenschaft um ein Baudenkmal?',
                        'slug': 'handelt-es-sich-um-ein-baudenkmal',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Schützenswert',
                        'slug': 'schuetzenswert',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Erhaltenswert',
                        'slug': 'erhaltenswert',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'K-Objekt',
                        'slug': 'k-objekt',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Baugruppe Bauinventar',
                        'slug': 'baugruppe-bauinventar',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'RRB',
                        'slug': 'rrb',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Vertrag',
                        'slug': 'vertrag',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Objekt des besonderen Landschaftsschutzes',
                        'slug': 'objekt-des-besonderen-landschaftsschutzes',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Gebiet mit bekannten oder vermuteten archäologischen Objekten',
                        'slug': 'gebiet-mit-archaeologischen-objekten',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Naturschutz',
                        'slug': 'naturschutz',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Wildtierschutz',
                        'slug': 'wildtierschutz',
                        'type': 'ChoiceQuestion'
                    }
                ],
                'label': 'Zonenvorschriften - Schutzzonen',
                'slug': 'zonenvorschriften-schutzzonen',
                'type': 'FormQuestion'
            }
        ],
        'label': 'Grundstück',
        'slug': '3-grundstueck',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'children': [
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Ist das Bauvorhaben besonderen Brandrisiken ausgesetzt?',
                        'slug': 'besondere-brandrisiken',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Werden Brandschutzabstände unterschritten?',
                        'slug': 'werden-brandschutzabstaende-unterschritten',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': True,
                                'label': '1'
                            },
                            {
                                'checked': False,
                                'label': '2'
                            },
                            {
                                'checked': False,
                                'label': '3'
                            },
                            {
                                'checked': False,
                                'label': '4'
                            }
                        ],
                        'label': 'QSS-Stufe',
                        'slug': 'qss-stufe',
                        'type': 'MultipleChoiceQuestion'
                    }
                ],
                'label': 'Brandschutz',
                'slug': 'brandschutz',
                'type': 'FormQuestion'
            },
            {
                'children': [
                    {
                        'content': None,
                        'label': 'Wohnungen',
                        'slug': 'wohnungen-titel',
                        'type': 'StaticQuestion'
                    },
                    {
                        'columns': [
                            'Wohnungsgrösse (Anzahl Zimmer)',
                            'Anzahl bestehender Wohnungen dieser Grösse',
                            'Anzahl neuer Wohnungen dieser Grösse'
                        ],
                        'label': 'Wohnungskategorie',
                        'rows': [
                        ],
                        'slug': 'wohnungen',
                        'type': 'TableQuestion'
                    },
                    {
                        'content': None,
                        'label': 'Total',
                        'slug': 'total-wohnungen-titel',
                        'type': 'StaticQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Autoabstellplätze für Fahrzeuge oder Fahrradabstellplätze?',
                        'slug': 'auto-oder-fahrradabstellplaetze',
                        'type': 'ChoiceQuestion'
                    }
                ],
                'label': 'Wohnen',
                'slug': 'wohnen',
                'type': 'FormQuestion'
            }
        ],
        'label': 'Bauwerk',
        'slug': '4-bauwerk',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'children': [
                    {
                        'content': None,
                        'label': 'Immissionsschutz - Bauen im lärmbelasteten Gebiet',
                        'slug': 'immissionsschutz-laermbelastetes-gebiet-titel',
                        'type': 'StaticQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Werden die Planungs- oder Immissionsgrenzwerte der massgebenden Empfindlichkeitsstufe auf der bebaubaren Fläche überschritten?',
                        'slug': 'grenzwerte-ueberschritten',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'content': None,
                        'label': 'Immissionsschutz - Allgemeine Angaben',
                        'slug': 'immissionsschutz-allgemeine-angaben-titel',
                        'type': 'StaticQuestion'
                    },
                    {
                        'label': 'Seit welchem Jahr besteht der Betrieb an diesem Standort?',
                        'slug': 'seit-welchem-jahr-besteht-der-betrieb-am-standort',
                        'type': 'IntegerQuestion',
                        'value': None
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Beinhaltet das Vorhaben Neubauten, Umbauten, Erweiterungen oder Umnutzungen, welche mit Schadstoffen oder Gerüchen belastete Luft aus Gebäuden oder Anlagen emittiert?',
                        'slug': 'mit-schadstoffen-belastete-luft-aus-gebaeuden',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Beinhaltet das Vorhaben Neubauten, Umbauten, Erweiterungen oder Umnutzungen mit Anlagen oder Prozessen, welche Aussenlärm erzeugen?',
                        'slug': 'wird-aussenlaerm-erzeugt',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'content': None,
                        'label': 'Immissionsschutz - Luftreinhaltung',
                        'slug': 'immissionsschutz-luftreinhaltung-titel',
                        'type': 'StaticQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': False,
                                'label': 'Ja'
                            },
                            {
                                'checked': True,
                                'label': 'Nein'
                            }
                        ],
                        'label': 'Werden Luftemissionen erzeugt?',
                        'slug': 'werden-luftemissionen-erzeugt',
                        'type': 'ChoiceQuestion'
                    }
                ],
                'label': 'Immissionsschutz I',
                'slug': 'immissionsschutz',
                'type': 'FormQuestion'
            },
            {
                'children': [
                    {
                        'choices': [
                            {
                                'checked': True,
                                'label': 'Unbestimmt'
                            },
                            {
                                'checked': False,
                                'label': 'Rot'
                            },
                            {
                                'checked': False,
                                'label': 'Blau'
                            },
                            {
                                'checked': False,
                                'label': 'Gelb'
                            },
                            {
                                'checked': False,
                                'label': 'Gelb-Weiss'
                            }
                        ],
                        'label': 'Gefahrenstufe',
                        'slug': 'gefahrenstufe',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'columns': [
                            'Hauptprozessart',
                            'Prozessart',
                            'Beschreibung der Gefährdung'
                        ],
                        'label': 'Beschreibung der Prozessart',
                        'rows': [
                        ],
                        'slug': 'beschreibung-der-prozessart-tabelle',
                        'type': 'TableQuestion'
                    }
                ],
                'label': 'Naturgefahren',
                'slug': 'naturgefahren',
                'type': 'FormQuestion'
            },
            {
                'children': [
                    {
                        'label': 'Gebäudeversicherungswert vor der Erneuerung in CHF',
                        'slug': 'gebaeudeversicherungswert-in-chf',
                        'type': 'IntegerQuestion',
                        'value': 10000
                    }
                ],
                'label': 'Hindernisfreies Bauen',
                'slug': 'hindernisfreies-bauen',
                'type': 'FormQuestion'
            }
        ],
        'label': 'Spezialformulare',
        'slug': '5-spezialformulare',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Grundriss (Massstäblich (1:100 / 1:50) mit Angabe der Bodenfläche)'
                    }
                ],
                'label': 'Grundriss (Massstäblich (1:100 / 1:50) mit Angabe der Bodenfläche)',
                'slug': 'grundriss-angabe-bodenflaeche-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Situationsplan'
                    }
                ],
                'label': 'Situationsplan',
                'slug': 'situationsplan-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Grundriss'
                    }
                ],
                'label': 'Grundriss',
                'slug': 'grundriss-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Schnitt'
                    }
                ],
                'label': 'Schnitt',
                'slug': 'schnitt-dokument',
                'type': 'MultipleChoiceQuestion'
            }
        ],
        'label': 'Dokumente',
        'slug': '6-dokumente',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Die Anforderungen sind gemäss Art. 11 – 15 BewD eingehalten.'
                    }
                ],
                'label': 'Die Anforderungen sind gemäss Art. 11 – 15 BewD eingehalten.',
                'slug': 'anforderungen-eingehalten',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Die Bauherrschaft bestätigt, dass die erforderlichen Massnahmen zum Schutz vor erhöhten Radongaskonzentrationen nach den anerkannten Regeln der Baukunde getroffen werden (siehe "Mehr Informationen"). Die Bauherrschaft hat zur Kenntnis genommen, dass die Bauabnahme grundsätzlich auch eine Radonmessung umfassen kann.'
                    }
                ],
                'label': 'Die Bauherrschaft bestätigt, dass die erforderlichen Massnahmen zum Schutz vor erhöhten Radongaskonzentrationen nach den anerkannten Regeln der Baukunde getroffen werden (siehe "Mehr Informationen"). Die Bauherrschaft hat zur Kenntnis genommen, dass die Bauabnahme grundsätzlich auch eine Radonmessung umfassen kann.',
                'slug': 'einhaltung-radonvorgaben',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Die Bauherrschaft bestätigt, dass sie die Ausführungen zu den Asbestfragen (siehe "Mehr Informationen") zur Kenntnis genommen hat. Bei der Umsetzung des Bauvorhabens wird die Bauherrschaft ein Augenmerk auf mögliche asbesthaltige Materialien richten. Sollte ein Asbestverdacht vorhanden sein, verpflichtet sich die Bauherrschaft, das fragliche Material auf Asbest untersuchen zu lassen. Wenn sich dieses Material als astbesthaltig erweist, muss die Bauherrschaft dafür besorgt sein, dass dieses von einer Spezialfirma fachgerecht entsorgt wird (zu Lasten Auftraggeber).'
                    }
                ],
                'label': 'Die Bauherrschaft bestätigt, dass sie die Ausführungen zu den Asbestfragen (siehe "Mehr Informationen") zur Kenntnis genommen hat. Bei der Umsetzung des Bauvorhabens wird die Bauherrschaft ein Augenmerk auf mögliche asbesthaltige Materialien richten. Sollte ein Asbestverdacht vorhanden sein, verpflichtet sich die Bauherrschaft, das fragliche Material auf Asbest untersuchen zu lassen. Wenn sich dieses Material als astbesthaltig erweist, muss die Bauherrschaft dafür besorgt sein, dass dieses von einer Spezialfirma fachgerecht entsorgt wird (zu Lasten Auftraggeber).',
                'slug': 'einhaltung-asbestvorgaben',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Der/die Gesuchsteller/in bestätigt, dass die Liegenschaftsentwässerung gemäss dem AWA-Merkblatt "Entwässerung von Industrie- und Gewerbeliegenschaften" geplant und realisiert werden. Als Beilage enthält das Gesuch einen Umgebungsplan, auf dem bei allen Teilfächen die vorgesehene Nutzung, die Befestigungsart, das Gefälle sowie die Entwässerungsart eingetragen sind.'
                    }
                ],
                'label': 'Der/die Gesuchsteller/in bestätigt, dass die Liegenschaftsentwässerung gemäss dem AWA-Merkblatt "Entwässerung von Industrie- und Gewerbeliegenschaften" geplant und realisiert werden. Als Beilage enthält das Gesuch einen Umgebungsplan, auf dem bei allen Teilflächen die vorgesehene Nutzung, die Befestigungsart, das Gefälle sowie die Entwässerungsart eingetragen sind.',
                'slug': 'bestaetigung-liegenschaftsentwaesserung',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Der/die Gesuchsteller/in bestätigt, dass er keinen Tatbestand zu den Bestimmungen zum Natur-, Wild- und Vogelschutz tangiert.'
                    }
                ],
                'label': 'Der/die Gesuchsteller/in bestätigt, dass er keinen Tatbestand zu den Bestimmungen zum Natur-, Wild- und Vogelschutz tangiert.',
                'slug': 'keine-tangierung-natur-wild-vogelschutz',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Der/die Gesuchsteller/in resp. die bevollmächtigte Vertretung bestätigt mit rechtsgültiger Unterschrift, dass die elektronisch übermittelten Daten (inkl. dem unterzeichneten Situationsplan) vollständig und wahrheitsgetreu ausgefüllt und eingereicht worden sind.'
                    }
                ],
                'label': 'Der/die Gesuchsteller/in resp. die bevollmächtigte Vertretung bestätigt mit rechtsgültiger Unterschrift, dass die elektronisch übermittelten Daten (inkl. dem unterzeichneten Situationsplan) vollständig und wahrheitsgetreu ausgefüllt und eingereicht worden sind.',
                'slug': 'bestaetigung-mit-unterschrift',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Der/die Gesuchsteller/in bestätigt, dass die vom GIS-System übernommen Daten mit den baurechtlichen Grundlagen übereinstimmen.'
                    }
                ],
                'label': 'Der/die Gesuchsteller/in bestätigt, dass die vom GIS-System übernommen Daten mit den baurechtlichen Grundlagen übereinstimmen.',
                'slug': 'bestaetigung-gis',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Die gesuchstellende Person bestätigt, dass sie die Berechtigung auf das eBau Dossier hat.  Sofern das Baugesuch nicht durch die gesuchstellende Person selbst, sondern durch eine Drittperson (z.B. Vertretung, Architekt(in), Projektverfasser(in) etc.) in eBau erfasst wurde, bestätigt diese Drittperson, welche das Baugesuch ausgefüllt hat, dass sie der gesuchstellenden Person bzw. der Bauherrschaft die Berechtigung (via Tab «Berechtigungen») auf das eBau Dossier erteilt hat.'
                    }
                ],
                'label': 'Die gesuchstellende Person bestätigt, dass sie die Berechtigung auf das eBau Dossier hat.  Sofern das Baugesuch nicht durch die gesuchstellende Person selbst, sondern durch eine Drittperson (z.B. Vertretung, Architekt(in), Projektverfasser(in) etc.) in eBau erfasst wurde, bestätigt diese Drittperson, welche das Baugesuch ausgefüllt hat, dass sie der gesuchstellenden Person bzw. der Bauherrschaft die Berechtigung (via Tab «Berechtigungen») auf das eBau Dossier erteilt hat.',
                'slug': 'bestaetigung-berechtigung-bauherrschaft',
                'type': 'MultipleChoiceQuestion'
            }
        ],
        'label': 'Bestätigung',
        'slug': '7-bestaetigung',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'label': 'Ausnahmegesuche',
                'slug': 'ausnahmegesuche',
                'type': 'TextareaQuestion',
                'value': None
            },
            {
                'label': 'Bemerkungen',
                'slug': 'freigabequittung-bemerkungen',
                'type': 'TextareaQuestion',
                'value': None
            }
        ],
        'label': 'Einreichen',
        'slug': '8-freigabequittung',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'label': 'Gesuchsteller/in',
                'people': [
                    {
                        'familyName': 'Meier',
                        'givenName': 'Hans'
                    }
                ],
                'type': 'SignatureQuestion'
            }
        ],
        'label': 'Unterschriften',
        'slug': '8-unterschriften',
        'type': 'FormQuestion'
    }
]

snapshots['test_document_merge_service_snapshot baugesuch_header'] = {
    'addressHeader': 'Teststrasse 3, Burgdorf',
    'addressHeaderLabel': 'Adresse',
    'applicantHeader': 'Hans Meier',
    'applicantHeaderLabel': 'Gesuchsteller/in',
    'applicants': [
        {
            'first_name': 'Hans',
            'full_name': 'Hans Meier',
            'is_juristic_person': False,
            'juristic_name': ' ',
            'last_name': 'Meier',
            'street': 'Strasse',
            'street_number': '33',
            'town': 'Bern',
            'zip': 3000
        }
    ],
    'authorityHeader': None,
    'authorityHeaderLabel': 'Leitbehörde',
    'caseId': 1,
    'caseType': 'Baugesuch',
    'coordEast': '2614314.0',
    'coordNorth': '1211926.0',
    'createdAt': 'Erstellt am 06.03.2020 um 12:10',
    'descriptionHeader': 'Testanfrage',
    'descriptionHeaderLabel': 'Beschreibung',
    'documents': [
    ],
    'dossierNr': None,
    'formType': None,
    'generatedAt': 'Generiert am 06.01.2023 um 17:10',
    'inputDateHeader': None,
    'inputDateHeaderLabel': 'Eingangsdatum',
    'landownerHeaderLabel': 'Grundeigentümer/in',
    'landowners': [
    ],
    'modificationHeader': None,
    'modificationHeaderLabel': 'Projektänderung',
    'modifiedAt': 'Zuletzt bearbeitet am 05.08.2021 um 11:05',
    'municipality': 'Burgdorf',
    'municipalityHeader': 'Burgdorf',
    'municipalityHeaderLabel': 'Gemeinde',
    'paperInputDateHeader': None,
    'plotsHeader': '1',
    'plotsHeaderLabel': 'Parzelle(n)',
    'projectAuthorHeaderLabel': 'Projektverfasser/in',
    'projectAuthors': [
    ],
    'responsibleHeader': None,
    'responsibleHeaderLabel': 'Zuständig',
    'signatureMetadata': 'Ort und Datum',
    'signatureSectionTitle': 'Unterschriften',
    'signatureTitle': 'Unterschrift',
    'tagHeader': None,
    'tagHeaderLabel': 'Stichworte'
}

snapshots['test_document_merge_service_snapshot mp-form'] = [
    {
        'children': [
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Prüfungsgegenstand'
                    },
                    {
                        'checked': False,
                        'label': 'Kein Prüfungsgegenstand'
                    }
                ],
                'label': 'Bepflanzung GBR/EG ZGB',
                'slug': 'mp-bepflanzung',
                'type': 'ChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Eingehalten'
                    },
                    {
                        'checked': False,
                        'label': 'Mangel'
                    },
                    {
                        'checked': False,
                        'label': 'Mangel behoben'
                    }
                ],
                'label': 'Prüfergebnis',
                'slug': 'mp-bepflanzung-ergebnis',
                'type': 'ChoiceQuestion'
            },
            {
                'label': 'Bemerkungen',
                'slug': 'mp-bepflanzung-bemerkungen',
                'type': 'TextareaQuestion',
                'value': 'Test Bepflanzung'
            }
        ],
        'label': 'Weitere Vorschriften',
        'slug': 'mp-weitere-vorschriften',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Ja'
                    },
                    {
                        'checked': True,
                        'label': 'Nein'
                    }
                ],
                'label': 'Sind die erforderlichen Beilagen zum Baugesuch vorhanden?',
                'slug': 'mp-erforderliche-beilagen-vorhanden',
                'type': 'ChoiceQuestion'
            },
            {
                'label': 'Welche Beilagen fehlen?',
                'slug': 'mp-welche-beilagen-fehlen',
                'type': 'TextareaQuestion',
                'value': 'Alle'
            }
        ],
        'label': 'Abschluss',
        'slug': 'mp-abschluss',
        'type': 'FormQuestion'
    }
]

snapshots['test_document_merge_service_snapshot mp-form_header'] = {
    'addressHeader': 'Wiesenweg, Burgdorf',
    'addressHeaderLabel': 'Adresse',
    'applicantHeader': 'Max Muster',
    'applicantHeaderLabel': 'Gesuchsteller/in',
    'applicants': [
        {
            'first_name': 'Max',
            'full_name': 'Max Muster',
            'is_juristic_person': False,
            'juristic_name': ' ',
            'last_name': 'Muster',
            'street': 'Wiesenweg',
            'street_number': '33',
            'town': 'Bern',
            'zip': 3007
        }
    ],
    'authorityHeader': None,
    'authorityHeaderLabel': 'Leitbehörde',
    'caseId': 3,
    'caseType': 'Baugesuch',
    'coordEast': '2614296.0',
    'coordNorth': '1211900.0',
    'createdAt': 'Erstellt am 05.07.2022 um 18:29',
    'descriptionHeader': 'Neubad',
    'descriptionHeaderLabel': 'Beschreibung',
    'documents': [
    ],
    'dossierNr': '2021-1',
    'formType': 'Materielle Prüfung',
    'generatedAt': 'Generiert am 06.01.2023 um 17:10',
    'inputDateHeader': GenericRepr('FakeDatetime(2021, 3, 31, 13, 17, 8, tzinfo=tzutc())'),
    'inputDateHeaderLabel': 'Eingangsdatum',
    'landownerHeaderLabel': 'Grundeigentümer/in',
    'landowners': [
    ],
    'modificationHeader': None,
    'modificationHeaderLabel': 'Projektänderung',
    'modifiedAt': 'Zuletzt bearbeitet am 05.07.2022 um 18:34',
    'municipality': 'Burgdorf',
    'municipalityHeader': 'Burgdorf',
    'municipalityHeaderLabel': 'Gemeinde',
    'paperInputDateHeader': None,
    'plotsHeader': '3',
    'plotsHeaderLabel': 'Parzelle(n)',
    'projectAuthorHeaderLabel': 'Projektverfasser/in',
    'projectAuthors': [
    ],
    'responsibleHeader': None,
    'responsibleHeaderLabel': 'Zuständig',
    'signatureMetadata': 'Ort und Datum',
    'signatureSectionTitle': 'Unterschriften',
    'signatureTitle': 'Unterschrift',
    'tagHeader': None,
    'tagHeaderLabel': 'Stichworte'
}

snapshots['test_document_merge_service_snapshot sb1'] = [
    {
        'children': [
            {
                'columns': [
                    'Handelt es sich um eine juristische Person?',
                    'Name juristische Person',
                    'Name',
                    'Vorname',
                    'Strasse',
                    'Nummer',
                    'PLZ',
                    'Ort',
                    'Telefon oder Mobile',
                    'E-Mail',
                    'Hinweis Gesuchsteller/in',
                    'Vertreter/in?'
                ],
                'label': 'Verantwortliche Person Selbstdeklaration Baukontrolle',
                'rows': [
                    [
                        {
                            'label': 'Handelt es sich um eine juristische Person?',
                            'slug': 'juristische-person-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Nein'
                        },
                        {
                            'label': 'Name juristische Person',
                            'slug': 'name-juristische-person-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': None
                        },
                        {
                            'label': 'Name',
                            'slug': 'name-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Muster'
                        },
                        {
                            'label': 'Vorname',
                            'slug': 'vorname-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Max'
                        },
                        {
                            'label': 'Strasse',
                            'slug': 'strasse-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Wiesenweg'
                        },
                        {
                            'label': 'Nummer',
                            'slug': 'nummer-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': '33'
                        },
                        {
                            'label': 'PLZ',
                            'slug': 'plz-gesuchstellerin',
                            'type': 'IntegerQuestion',
                            'value': 3007
                        },
                        {
                            'label': 'Ort',
                            'slug': 'ort-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Bern'
                        },
                        {
                            'label': 'Telefon oder Mobile',
                            'slug': 'telefon-oder-mobile-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': '077777777'
                        },
                        {
                            'label': 'E-Mail',
                            'slug': 'e-mail-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'info@example.com'
                        }
                    ],
                    [
                        {
                            'label': 'Handelt es sich um eine juristische Person?',
                            'slug': 'juristische-person-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Ja'
                        },
                        {
                            'label': 'Name juristische Person',
                            'slug': 'name-juristische-person-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Architekturbüro Asdf'
                        },
                        {
                            'label': 'Name',
                            'slug': 'name-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Egger'
                        },
                        {
                            'label': 'Vorname',
                            'slug': 'vorname-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Ernst'
                        },
                        {
                            'label': 'Strasse',
                            'slug': 'strasse-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Eggistrasse'
                        },
                        {
                            'label': 'Nummer',
                            'slug': 'nummer-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': None
                        },
                        {
                            'label': 'PLZ',
                            'slug': 'plz-gesuchstellerin',
                            'type': 'IntegerQuestion',
                            'value': 3456
                        },
                        {
                            'label': 'Ort',
                            'slug': 'ort-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Ebersecken'
                        },
                        {
                            'label': 'Telefon oder Mobile',
                            'slug': 'telefon-oder-mobile-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': '01010101'
                        },
                        {
                            'label': 'E-Mail',
                            'slug': 'e-mail-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'i@e.org'
                        }
                    ]
                ],
                'slug': 'personalien-sb1-sb2',
                'type': 'TableQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Ja'
                    },
                    {
                        'checked': False,
                        'label': 'Nein'
                    }
                ],
                'label': 'Sind die Bedingungen und Auflagen der Baubewilligung (vor Baubeginn) erfüllt?',
                'slug': 'bedingungen-und-auflagen-erfuellt',
                'type': 'ChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Ja'
                    },
                    {
                        'checked': False,
                        'label': 'Nein'
                    }
                ],
                'label': 'Ist eine Schnurgerüstabnahme erforderlich?',
                'slug': 'ist-eine-schnurgerustabnahme-erforderlich',
                'type': 'ChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Ja'
                    },
                    {
                        'checked': False,
                        'label': 'Nein'
                    }
                ],
                'label': 'Sind Schnurgerüst und die bewilligte Höhe zur Abnahme bereit?',
                'slug': 'schnurgeruest-zur-abnahme-bereit',
                'type': 'ChoiceQuestion'
            },
            {
                'label': 'Ab wann ist eine Kontrolle möglich?',
                'slug': 'ab-wann-ist-eine-kontrolle-moeglich',
                'type': 'DateQuestion',
                'value': GenericRepr('datetime.date(2021, 4, 7)')
            }
        ],
        'label': 'Selbstdeklaration',
        'slug': 'selbstdeklaration-sb1',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'label': 'Bemerkungen',
                'slug': 'bemerkungen-sb1',
                'type': 'TextareaQuestion',
                'value': None
            },
            {
                'content': None,
                'label': '',
                'slug': 'freigabequittung-druckansicht',
                'type': 'StaticQuestion'
            }
        ],
        'label': 'Freigabequittung',
        'slug': 'freigabequittung-sb1',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'label': 'Verantwortliche Person Selbstdeklaration Baukontrolle',
                'people': [
                    {
                        'familyName': 'Muster',
                        'givenName': 'Max',
                        'juristicName': None
                    },
                    {
                        'familyName': 'Egger',
                        'givenName': 'Ernst',
                        'juristicName': 'Architekturbüro Asdf'
                    }
                ],
                'type': 'SignatureQuestion'
            }
        ],
        'label': 'Unterschriften',
        'slug': '8-unterschriften',
        'type': 'FormQuestion'
    }
]

snapshots['test_document_merge_service_snapshot sb1_header'] = {
    'addressHeader': 'Wiesenweg, Burgdorf',
    'addressHeaderLabel': 'Adresse',
    'applicantHeader': 'Max Muster',
    'applicantHeaderLabel': 'Gesuchsteller/in',
    'applicants': [
        {
            'first_name': 'Max',
            'full_name': 'Max Muster',
            'is_juristic_person': False,
            'juristic_name': ' ',
            'last_name': 'Muster',
            'street': 'Wiesenweg',
            'street_number': '33',
            'town': 'Bern',
            'zip': 3007
        }
    ],
    'authorityHeader': None,
    'authorityHeaderLabel': 'Leitbehörde',
    'caseId': 3,
    'caseType': 'Baugesuch',
    'coordEast': '2614296.0',
    'coordNorth': '1211900.0',
    'createdAt': 'Erstellt am 06.04.2021 um 14:19',
    'descriptionHeader': 'Neubad',
    'descriptionHeaderLabel': 'Beschreibung',
    'documents': [
    ],
    'dossierNr': '2021-1',
    'formType': 'Selbstdeklaration Baukontrolle 1',
    'generatedAt': 'Generiert am 06.01.2023 um 17:10',
    'inputDateHeader': GenericRepr('FakeDatetime(2021, 3, 31, 13, 17, 8, tzinfo=tzutc())'),
    'inputDateHeaderLabel': 'Eingangsdatum',
    'landownerHeaderLabel': 'Grundeigentümer/in',
    'landowners': [
    ],
    'modificationHeader': None,
    'modificationHeaderLabel': 'Projektänderung',
    'modifiedAt': 'Zuletzt bearbeitet am 06.04.2021 um 14:22',
    'municipality': 'Burgdorf',
    'municipalityHeader': 'Burgdorf',
    'municipalityHeaderLabel': 'Gemeinde',
    'paperInputDateHeader': None,
    'plotsHeader': '3',
    'plotsHeaderLabel': 'Parzelle(n)',
    'projectAuthorHeaderLabel': 'Projektverfasser/in',
    'projectAuthors': [
    ],
    'responsibleHeader': None,
    'responsibleHeaderLabel': 'Zuständig',
    'signatureMetadata': 'Ort und Datum',
    'signatureSectionTitle': 'Unterschriften',
    'signatureTitle': 'Unterschrift',
    'tagHeader': None,
    'tagHeaderLabel': 'Stichworte'
}

snapshots['test_document_merge_service_snapshot sb2'] = [
    {
        'children': [
            {
                'columns': [
                    'Handelt es sich um eine juristische Person?',
                    'Name juristische Person',
                    'Name',
                    'Vorname',
                    'Strasse',
                    'Nummer',
                    'PLZ',
                    'Ort',
                    'Telefon oder Mobile',
                    'E-Mail',
                    'Hinweis Gesuchsteller/in',
                    'Vertreter/in?'
                ],
                'label': 'Verantwortliche Person Selbstdeklaration Baukontrolle',
                'rows': [
                    [
                        {
                            'label': 'Handelt es sich um eine juristische Person?',
                            'slug': 'juristische-person-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Ja'
                        },
                        {
                            'label': 'Name juristische Person',
                            'slug': 'name-juristische-person-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Architekturbüro Asdf'
                        },
                        {
                            'label': 'Name',
                            'slug': 'name-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Egger'
                        },
                        {
                            'label': 'Vorname',
                            'slug': 'vorname-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Ernst'
                        },
                        {
                            'label': 'Strasse',
                            'slug': 'strasse-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Eggistrasse'
                        },
                        {
                            'label': 'Nummer',
                            'slug': 'nummer-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': None
                        },
                        {
                            'label': 'PLZ',
                            'slug': 'plz-gesuchstellerin',
                            'type': 'IntegerQuestion',
                            'value': 3456
                        },
                        {
                            'label': 'Ort',
                            'slug': 'ort-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Ebersecken'
                        },
                        {
                            'label': 'Telefon oder Mobile',
                            'slug': 'telefon-oder-mobile-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': '01010101'
                        },
                        {
                            'label': 'E-Mail',
                            'slug': 'e-mail-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'i@e.org'
                        }
                    ],
                    [
                        {
                            'label': 'Handelt es sich um eine juristische Person?',
                            'slug': 'juristische-person-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Nein'
                        },
                        {
                            'label': 'Name juristische Person',
                            'slug': 'name-juristische-person-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': None
                        },
                        {
                            'label': 'Name',
                            'slug': 'name-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Muster'
                        },
                        {
                            'label': 'Vorname',
                            'slug': 'vorname-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Max'
                        },
                        {
                            'label': 'Strasse',
                            'slug': 'strasse-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Wiesenweg'
                        },
                        {
                            'label': 'Nummer',
                            'slug': 'nummer-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': '33'
                        },
                        {
                            'label': 'PLZ',
                            'slug': 'plz-gesuchstellerin',
                            'type': 'IntegerQuestion',
                            'value': 3007
                        },
                        {
                            'label': 'Ort',
                            'slug': 'ort-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'Bern'
                        },
                        {
                            'label': 'Telefon oder Mobile',
                            'slug': 'telefon-oder-mobile-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': '077777777'
                        },
                        {
                            'label': 'E-Mail',
                            'slug': 'e-mail-gesuchstellerin',
                            'type': 'TextQuestion',
                            'value': 'info@example.com'
                        }
                    ]
                ],
                'slug': 'personalien-sb1-sb2',
                'type': 'TableQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Ja'
                    },
                    {
                        'checked': False,
                        'label': 'Nein'
                    }
                ],
                'label': 'Ist das Bauvorhaben nach der Baubewilligung und evtl. Projektänderungsbewilligung ausgeführt?',
                'slug': 'bauvorhaben-nach-baubewilligung-ausgefuehrt',
                'type': 'ChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Ja'
                    },
                    {
                        'checked': False,
                        'label': 'Nein'
                    }
                ],
                'label': 'Sind die Bedingungen und Auflagen der Baubewilligung eingehalten?',
                'slug': 'bedingungen-auflagen-eingehalten',
                'type': 'ChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Ja'
                    },
                    {
                        'checked': False,
                        'label': 'Nein'
                    }
                ],
                'label': 'Sind die Sicherheitsvorschriften eingehalten?',
                'slug': 'sicherheitsvorschriften-eingehalten',
                'type': 'ChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Ja'
                    },
                    {
                        'checked': False,
                        'label': 'Nein'
                    }
                ],
                'label': 'Sind die Nebengebäude fertiggestellt?',
                'slug': 'sind-die-nebengebaeude-fertiggestellt',
                'type': 'ChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Ja'
                    },
                    {
                        'checked': False,
                        'label': 'Nein'
                    }
                ],
                'label': 'Sind die Umgebungsarbeiten fertiggestellt?',
                'slug': 'sind-die-umgebungsarbeiten-fertiggestellt',
                'type': 'ChoiceQuestion'
            },
            {
                'label': 'Bauende',
                'slug': 'bauende',
                'type': 'DateQuestion',
                'value': None
            }
        ],
        'label': 'Abschluss',
        'slug': 'abschluss-sb2',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'columns': [
                    'Lagerstoff',
                    'Neu / Bestehend',
                    'Menge',
                    'Massangabe',
                    'Anlageart',
                    'Anzahl Behälter',
                    'Lagerort',
                    'Brennbare Flüssigkeit / Gas',
                    'Flammpunkt',
                    'Gesundheitsschädlich oder explosiv',
                    'Wassergefährdend',
                    'Wassergefährdungsklasse',
                    'Bewilligungspflichtig?'
                ],
                'label': 'Lagerung von Stoffen',
                'rows': [
                ],
                'slug': 'lagerung-von-stoffen-v2',
                'type': 'TableQuestion'
            }
        ],
        'label': 'Lagerung von Stoffen',
        'slug': 'lagerung-von-stoffen-sb2',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'label': 'Bemerkungen',
                'slug': 'bemerkungen-abschluss-sb2',
                'type': 'TextareaQuestion',
                'value': None
            },
            {
                'content': None,
                'label': '',
                'slug': 'freigabequittung-sb2-druckansicht',
                'type': 'StaticQuestion'
            }
        ],
        'label': 'Freigabequittung',
        'slug': 'freigabequittung-sb2',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'label': 'Verantwortliche Person Selbstdeklaration Baukontrolle',
                'people': [
                    {
                        'familyName': 'Egger',
                        'givenName': 'Ernst',
                        'juristicName': 'Architekturbüro Asdf'
                    },
                    {
                        'familyName': 'Muster',
                        'givenName': 'Max',
                        'juristicName': None
                    }
                ],
                'type': 'SignatureQuestion'
            }
        ],
        'label': 'Unterschriften',
        'slug': '8-unterschriften',
        'type': 'FormQuestion'
    }
]

snapshots['test_document_merge_service_snapshot sb2_header'] = {
    'addressHeader': 'Wiesenweg, Burgdorf',
    'addressHeaderLabel': 'Adresse',
    'applicantHeader': 'Max Muster',
    'applicantHeaderLabel': 'Gesuchsteller/in',
    'applicants': [
        {
            'first_name': 'Max',
            'full_name': 'Max Muster',
            'is_juristic_person': False,
            'juristic_name': ' ',
            'last_name': 'Muster',
            'street': 'Wiesenweg',
            'street_number': '33',
            'town': 'Bern',
            'zip': 3007
        }
    ],
    'authorityHeader': None,
    'authorityHeaderLabel': 'Leitbehörde',
    'caseId': 3,
    'caseType': 'Baugesuch',
    'coordEast': '2614296.0',
    'coordNorth': '1211900.0',
    'createdAt': 'Erstellt am 06.04.2021 um 14:23',
    'descriptionHeader': 'Neubad',
    'descriptionHeaderLabel': 'Beschreibung',
    'documents': [
    ],
    'dossierNr': '2021-1',
    'formType': 'Selbstdeklaration Baukontrolle 2',
    'generatedAt': 'Generiert am 06.01.2023 um 17:10',
    'inputDateHeader': GenericRepr('FakeDatetime(2021, 3, 31, 13, 17, 8, tzinfo=tzutc())'),
    'inputDateHeaderLabel': 'Eingangsdatum',
    'landownerHeaderLabel': 'Grundeigentümer/in',
    'landowners': [
    ],
    'modificationHeader': None,
    'modificationHeaderLabel': 'Projektänderung',
    'modifiedAt': 'Zuletzt bearbeitet am 06.04.2021 um 14:23',
    'municipality': 'Burgdorf',
    'municipalityHeader': 'Burgdorf',
    'municipalityHeaderLabel': 'Gemeinde',
    'paperInputDateHeader': None,
    'plotsHeader': '3',
    'plotsHeaderLabel': 'Parzelle(n)',
    'projectAuthorHeaderLabel': 'Projektverfasser/in',
    'projectAuthors': [
    ],
    'responsibleHeader': None,
    'responsibleHeaderLabel': 'Zuständig',
    'signatureMetadata': 'Ort und Datum',
    'signatureSectionTitle': 'Unterschriften',
    'signatureTitle': 'Unterschrift',
    'tagHeader': None,
    'tagHeaderLabel': 'Stichworte'
}

snapshots['test_eingabebestaetigung_gr 1'] = {
    'addressHeader': 'Bahnhofstrasse 2, Testhausen',
    'addressHeaderLabel': 'Adresse',
    'applicantHeader': 'Test AG, Foo Bar',
    'applicantHeaderLabel': 'Gesuchsteller/in',
    'applicants': [
        {
            'email': ' ',
            'first_name': 'Foo',
            'full_name': 'Test AG, Foo Bar',
            'is_juristic_person': True,
            'juristic_name': 'Test AG',
            'last_name': 'Bar',
            'street': ' ',
            'street_number': ' ',
            'tel': ' ',
            'town': ' ',
            'zip': ' '
        }
    ],
    'authorityHeader': 'Rebecca Gonzalez',
    'authorityHeaderLabel': 'Leitbehörde',
    'caseId': 1,
    'caseType': 'Baugesuch',
    'coordEast': '',
    'coordNorth': '',
    'createdAt': 'Erstellt am 03.08.2022 um 09:19',
    'descriptionHeader': 'Bau Einfamilienhaus',
    'descriptionHeaderLabel': 'Beschreibung',
    'documents': [
        'Test, erstellt am 06.09.2022 um 13:37 Uhr'
    ],
    'dossierNr': None,
    'formType': None,
    'generatedAt': 'Generiert am 07.09.2022 um 14:01',
    'inputDateHeader': GenericRepr('FakeDatetime(2021, 1, 1, 0, 0)'),
    'inputDateHeaderLabel': 'Eingangsdatum',
    'landownerHeaderLabel': 'Grundeigentümer/in',
    'landowners': [
        {
            'email': ' ',
            'first_name': 'Grund',
            'full_name': 'Eigentümer AG, Grund Eigentümerin',
            'is_juristic_person': True,
            'juristic_name': 'Eigentümer AG',
            'last_name': 'Eigentümerin',
            'street': ' ',
            'street_number': ' ',
            'tel': ' ',
            'town': ' ',
            'zip': ' '
        }
    ],
    'modificationHeader': None,
    'modificationHeaderLabel': 'Projektänderung',
    'modifiedAt': 'Zuletzt bearbeitet am 06.09.2022 um 15:37',
    'municipality': 'Testhausen',
    'municipalityHeader': 'Testhausen',
    'municipalityHeaderLabel': 'Gemeinde',
    'paperInputDateHeader': GenericRepr('FakeDatetime(2021, 1, 2, 0, 0)'),
    'plotsHeader': '123',
    'plotsHeaderLabel': 'Parzelle(n)',
    'projectAuthorHeaderLabel': 'Projektverfasser/in',
    'projectAuthors': [
        {
            'email': ' ',
            'first_name': 'Projekt',
            'full_name': 'Projektverfasserin AG, Projekt Verfasserin',
            'is_juristic_person': True,
            'juristic_name': 'Projektverfasserin AG',
            'last_name': 'Verfasserin',
            'street': ' ',
            'street_number': ' ',
            'tel': ' ',
            'town': ' ',
            'zip': ' '
        }
    ],
    'responsibleHeader': None,
    'responsibleHeaderLabel': 'Zuständig',
    'signatureMetadata': 'Ort und Datum',
    'signatureSectionTitle': 'Unterschriften',
    'signatureTitle': 'Unterschrift',
    'tagHeader': None,
    'tagHeaderLabel': 'Stichworte'
}
