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
    'authorityHeader': 'Rebecca Gonzalez',
    'authorityHeaderLabel': 'Leitbehörde',
    'caseId': 1,
    'caseType': 'Baugesuch',
    'descriptionHeader': 'Bau Einfamilienhaus',
    'descriptionHeaderLabel': 'Beschreibung',
    'dossierNr': '2021-99',
    'formType': None,
    'inputDateHeader': GenericRepr('datetime.datetime(2021, 1, 1, 0, 0)'),
    'inputDateHeaderLabel': 'Eingangsdatum',
    'modificationHeader': 'Anbau Haus',
    'modificationHeaderLabel': 'Projektänderung',
    'municipality': 'Testhausen',
    'municipalityHeader': 'Testhausen',
    'municipalityHeaderLabel': 'Gemeinde',
    'paperInputDateHeader': GenericRepr('datetime.datetime(2021, 1, 2, 0, 0)'),
    'plotsHeader': '123',
    'plotsHeaderLabel': 'Parzelle(n)',
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
    'applicantHeader': None,
    'applicantHeaderLabel': 'Gesuchsteller/in',
    'authorityHeader': None,
    'authorityHeaderLabel': 'Leitbehörde',
    'caseId': 1,
    'caseType': 'Baugesuch',
    'descriptionHeader': None,
    'descriptionHeaderLabel': 'Beschreibung',
    'dossierNr': None,
    'formType': None,
    'inputDateHeader': GenericRepr('datetime.datetime(2021, 1, 1, 0, 0)'),
    'inputDateHeaderLabel': 'Eingangsdatum',
    'modificationHeader': None,
    'modificationHeaderLabel': 'Projektänderung',
    'municipality': None,
    'municipalityHeader': None,
    'municipalityHeaderLabel': 'Gemeinde',
    'paperInputDateHeader': None,
    'plotsHeader': None,
    'plotsHeaderLabel': 'Parzelle(n)',
    'responsibleHeader': None,
    'responsibleHeaderLabel': 'Zuständig',
    'signatureMetadata': 'Ort und Datum',
    'signatureSectionTitle': 'Unterschriften',
    'signatureTitle': 'Unterschrift',
    'tagHeader': None,
    'tagHeaderLabel': 'Stichworte'
}

snapshots['test_document_merge_service_snapshot[baugesuch] 1'] = [
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
                            'Hinweis Gesuchsteller/in'
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
                                },
                                {
                                    'content': None,
                                    'label': 'Hinweis Gesuchsteller/in',
                                    'slug': 'hinweis-personalien',
                                    'type': 'StaticQuestion'
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
                                'label': 'Grundeigentümer/in'
                            },
                            {
                                'checked': False,
                                'label': 'Gebäudeeigentümer/in'
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
                        'content': None,
                        'label': 'bauvorhaben-separator',
                        'slug': 'bauvorhaben-separator',
                        'type': 'StaticQuestion'
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
                        'content': None,
                        'label': 'Hinweis Naturgefahren',
                        'slug': 'hinweis-naturgefahren',
                        'type': 'StaticQuestion'
                    },
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
                        'label': 'Der/die Gesuchsteller/in ist verantwortlich für die Einhaltung der Radonvorgaben gemäss Strahlenschutzverordnung des Bundes.'
                    }
                ],
                'label': 'Der/die Gesuchsteller/in ist verantwortlich für die Einhaltung der Radonvorgaben gemäss Strahlenschutzverordnung des Bundes.',
                'slug': 'einhaltung-radonvorgaben',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Der/die Gesuchsteller/in ist verantwortlich für die Einhaltung der Asbestvorgaben des Bundes (Chemikalien-Risikoreduktions-Verordnung, ChemRRV).'
                    }
                ],
                'label': 'Der/die Gesuchsteller/in ist verantwortlich für die Einhaltung der Asbestvorgaben des Bundes (Chemikalien-Risikoreduktions-Verordnung, ChemRRV).',
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
                        'label': 'Der/die Gesuchsteller/in bestätigt, dass die Bauherrschaft Berechtigung (via Tab "Berechtigungen") auf das Dossier erhalten hat.'
                    }
                ],
                'label': 'Der/die Gesuchsteller/in bestätigt, dass die Bauherrschaft Berechtigung (via Tab "Berechtigungen") auf das Dossier erhalten hat.',
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
            },
            {
                'content': None,
                'label': 'freigabequittung-text',
                'slug': 'freigabequittung-text',
                'type': 'StaticQuestion'
            },
            {
                'content': None,
                'label': 'Formulardownload (PDF)',
                'slug': 'formulardownload-pdf',
                'type': 'StaticQuestion'
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

snapshots['test_document_merge_service_snapshot[mp-form] 1'] = [
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
                        'checked': False,
                        'label': 'Nein'
                    }
                ],
                'label': 'Sind die erforderlichen Beilagen zum Baugesuch vorhanden?',
                'slug': 'mp-erforderliche-beilagen-vorhanden',
                'type': 'ChoiceQuestion'
            }
        ],
        'label': 'Abschluss',
        'slug': 'mp-abschluss',
        'type': 'FormQuestion'
    }
]

snapshots['test_document_merge_service_snapshot[sb1] 1'] = [
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
                    'Hinweis Gesuchsteller/in'
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
                        },
                        {
                            'content': None,
                            'label': 'Hinweis Gesuchsteller/in',
                            'slug': 'hinweis-personalien',
                            'type': 'StaticQuestion'
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
                        },
                        {
                            'content': None,
                            'label': 'Hinweis Gesuchsteller/in',
                            'slug': 'hinweis-personalien',
                            'type': 'StaticQuestion'
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
            },
            {
                'content': None,
                'label': 'Formulardownload (PDF)',
                'slug': 'formulardownload-pdf',
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
                        'givenName': 'Max'
                    },
                    {
                        'familyName': 'Egger',
                        'givenName': 'Ernst'
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

snapshots['test_document_merge_service_snapshot[sb2] 1'] = [
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
                    'Hinweis Gesuchsteller/in'
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
                        },
                        {
                            'content': None,
                            'label': 'Hinweis Gesuchsteller/in',
                            'slug': 'hinweis-personalien',
                            'type': 'StaticQuestion'
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
                        },
                        {
                            'content': None,
                            'label': 'Hinweis Gesuchsteller/in',
                            'slug': 'hinweis-personalien',
                            'type': 'StaticQuestion'
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
            },
            {
                'content': None,
                'label': 'Formulardownload (PDF)',
                'slug': 'formulardownload-pdf',
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
                        'givenName': 'Ernst'
                    },
                    {
                        'familyName': 'Muster',
                        'givenName': 'Max'
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
