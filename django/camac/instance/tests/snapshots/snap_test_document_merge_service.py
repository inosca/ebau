# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_document_merge_service_snapshot[1-baugesuch] 1'] = [
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
                        'hidden': False,
                        'label': 'Wurden Vorabklärungen durchgeführt?',
                        'slug': 'wurden-vorabklaerungen-durchgefuehrt',
                        'type': 'ChoiceQuestion'
                    }
                ],
                'hidden': False,
                'label': 'Durchgeführte Vorabklärungen',
                'slug': 'durchgefuehrte-vorabklaerungen',
                'type': 'FormQuestion'
            },
            {
                'children': [
                    {
                        'columns': [
                            'E-Mail',
                            'Handelt es sich um eine juristische Person?',
                            'Name',
                            'Name juristische Person',
                            'Nummer',
                            'Ort',
                            'PLZ',
                            'Strasse',
                            'Telefon oder Mobile',
                            'Vorname'
                        ],
                        'hidden': False,
                        'label': 'Personalien - Gesuchsteller/in',
                        'rows': [
                            [
                                {
                                    'hidden': False,
                                    'label': 'Handelt es sich um eine juristische Person?',
                                    'slug': 'juristische-person-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': 'Nein'
                                },
                                {
                                    'hidden': False,
                                    'label': 'Name',
                                    'slug': 'name-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': 'Mustermann'
                                },
                                {
                                    'hidden': False,
                                    'label': 'Vorname',
                                    'slug': 'vorname-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': 'Max'
                                },
                                {
                                    'hidden': False,
                                    'label': 'Strasse',
                                    'slug': 'strasse-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': 'Strasse'
                                },
                                {
                                    'hidden': False,
                                    'label': 'Nummer',
                                    'slug': 'nummer-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': '14'
                                },
                                {
                                    'hidden': False,
                                    'label': 'PLZ',
                                    'slug': 'plz-gesuchstellerin',
                                    'type': 'IntegerQuestion',
                                    'value': 3000
                                },
                                {
                                    'hidden': False,
                                    'label': 'Ort',
                                    'slug': 'ort-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': 'Bern'
                                },
                                {
                                    'hidden': False,
                                    'label': 'Telefon oder Mobile',
                                    'slug': 'telefon-oder-mobile-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': '000 000 00 00'
                                },
                                {
                                    'hidden': False,
                                    'label': 'E-Mail',
                                    'slug': 'e-mail-gesuchstellerin',
                                    'type': 'TextQuestion',
                                    'value': 'mm@test.ch'
                                }
                            ]
                        ],
                        'slug': 'personalien-gesuchstellerin',
                        'type': 'TableQuestion'
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
                        'hidden': False,
                        'label': 'Sind neben den Gesuchstellenden weitere Personen beteiligt?',
                        'slug': 'weitere-personen',
                        'type': 'MultipleChoiceQuestion'
                    }
                ],
                'hidden': False,
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
                        'hidden': False,
                        'label': 'Baubeschrieb',
                        'slug': 'baubeschrieb',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'hidden': False,
                        'label': 'Beschreibung',
                        'slug': 'beschreibung-bauvorhaben',
                        'type': 'TextareaQuestion',
                        'value': 'Dachstock anbauen'
                    },
                    {
                        'hidden': False,
                        'label': 'Bisherige Nutzung',
                        'slug': 'bisherige-nutzung',
                        'type': 'TextareaQuestion',
                        'value': None
                    },
                    {
                        'content': None,
                        'hidden': False,
                        'label': 'Tragkonstruktion',
                        'slug': 'tragkonstruktion',
                        'type': 'StaticQuestion'
                    },
                    {
                        'hidden': False,
                        'label': 'System der Fundation',
                        'slug': 'fundation-system',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Stützen',
                        'slug': 'tragkonstruktion-stuetzen',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Wände',
                        'slug': 'tragkonstruktion-waende',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Decken',
                        'slug': 'tragkonstruktion-decken',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'content': None,
                        'hidden': False,
                        'label': 'Fassaden',
                        'slug': 'fassaden',
                        'type': 'StaticQuestion'
                    },
                    {
                        'hidden': False,
                        'label': 'Material',
                        'slug': 'fassaden-material',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Farbe',
                        'slug': 'fassaden-farbe',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'content': None,
                        'hidden': False,
                        'label': 'Dach',
                        'slug': 'dach',
                        'type': 'StaticQuestion'
                    },
                    {
                        'hidden': False,
                        'label': 'Form',
                        'slug': 'dach-form',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Neigung',
                        'slug': 'dach-neigung',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Material',
                        'slug': 'dach-material',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Farbe',
                        'slug': 'dach-farbe',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'content': None,
                        'hidden': False,
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
                        'hidden': False,
                        'label': 'Vorbereitende Massnahmen',
                        'slug': 'vorbereitende-massnahmen',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'hidden': False,
                        'label': 'Baukosten in CHF',
                        'slug': 'baukosten-in-chf',
                        'type': 'IntegerQuestion',
                        'value': 100000
                    },
                    {
                        'hidden': False,
                        'label': 'Geplanter Baustart',
                        'slug': 'geplanter-baustart',
                        'type': 'DateQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Dauer in Monaten',
                        'slug': 'dauer-in-monaten',
                        'type': 'IntegerQuestion',
                        'value': None
                    }
                ],
                'hidden': False,
                'label': 'Bauvorhaben',
                'slug': 'bauvorhaben',
                'type': 'FormQuestion'
            }
        ],
        'hidden': False,
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
                                'label': 'Andere'
                            }
                        ],
                        'hidden': False,
                        'label': 'Für welche Nutzungsart dient das Bauvorhaben?',
                        'slug': 'nutzungsart',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'choices': [
                            {
                                'checked': True,
                                'label': 'EFH'
                            },
                            {
                                'checked': False,
                                'label': 'MFH'
                            }
                        ],
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
                        'label': 'Ist der Bau im Wald oder innerhalb von 30 m Abstand zum Wald?',
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
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
                        'label': 'Welche Wärmepumpen sind im Bauvorhaben vorgesehen?',
                        'slug': 'welche-waermepumpen',
                        'type': 'MultipleChoiceQuestion'
                    }
                ],
                'hidden': False,
                'label': 'Triage',
                'slug': 'triage',
                'type': 'FormQuestion'
            }
        ],
        'hidden': False,
        'label': 'Nutzung Bauvorhaben',
        'slug': '2-nutzung-bauvorhaben',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'children': [
                    {
                        'hidden': False,
                        'label': 'Karte',
                        'slug': 'karte',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Strasse/Flurname',
                        'slug': 'strasse-flurname',
                        'type': 'TextQuestion',
                        'value': 'Strasse'
                    },
                    {
                        'hidden': False,
                        'label': 'Nr.',
                        'slug': 'nr',
                        'type': 'TextQuestion',
                        'value': '14'
                    },
                    {
                        'hidden': False,
                        'label': 'Ort',
                        'slug': 'ort-grundstueck',
                        'type': 'TextQuestion',
                        'value': 'Burgdorf'
                    },
                    {
                        'hidden': False,
                        'label': 'Zuständige Gemeinde',
                        'slug': 'gemeinde',
                        'type': 'TextQuestion',
                        'value': 'Burgdorf'
                    },
                    {
                        'columns': [
                            'Baurecht-Nummer',
                            'E-GRID-Nr.',
                            'Lagekoordinaten - Nord',
                            'Lagekoordinaten - Ost',
                            'Liegenschaftsnummer',
                            'Nummer',
                            'Ort',
                            'Parzellennummer',
                            'PLZ',
                            'Strasse'
                        ],
                        'hidden': False,
                        'label': 'Parzelle',
                        'rows': [
                            [
                                {
                                    'hidden': False,
                                    'label': 'Parzellennummer',
                                    'slug': 'parzellennummer',
                                    'type': 'TextQuestion',
                                    'value': '921'
                                },
                                {
                                    'hidden': False,
                                    'label': 'Liegenschaftsnummer',
                                    'slug': 'liegenschaftsnummer',
                                    'type': 'IntegerQuestion',
                                    'value': None
                                },
                                {
                                    'hidden': False,
                                    'label': 'Baurecht-Nummer',
                                    'slug': 'baurecht-nummer',
                                    'type': 'TextQuestion',
                                    'value': None
                                },
                                {
                                    'hidden': False,
                                    'label': 'E-GRID-Nr.',
                                    'slug': 'e-grid-nr',
                                    'type': 'TextQuestion',
                                    'value': 'CH208935354670'
                                },
                                {
                                    'hidden': False,
                                    'label': 'Strasse',
                                    'slug': 'strasse-parzelle',
                                    'type': 'TextQuestion',
                                    'value': None
                                },
                                {
                                    'hidden': False,
                                    'label': 'Nummer',
                                    'slug': 'nummer-parzelle',
                                    'type': 'TextQuestion',
                                    'value': None
                                },
                                {
                                    'hidden': False,
                                    'label': 'PLZ',
                                    'slug': 'plz-parzelle',
                                    'type': 'IntegerQuestion',
                                    'value': None
                                },
                                {
                                    'hidden': False,
                                    'label': 'Ort',
                                    'slug': 'ort-parzelle',
                                    'type': 'TextQuestion',
                                    'value': None
                                },
                                {
                                    'hidden': False,
                                    'label': 'Lagekoordinaten - Ost',
                                    'slug': 'lagekoordinaten-ost',
                                    'type': 'FloatQuestion',
                                    'value': '2614411'
                                },
                                {
                                    'hidden': False,
                                    'label': 'Lagekoordinaten - Nord',
                                    'slug': 'lagekoordinaten-nord',
                                    'type': 'FloatQuestion',
                                    'value': '1211395'
                                }
                            ]
                        ],
                        'slug': 'parzelle',
                        'type': 'TableQuestion'
                    },
                    {
                        'hidden': False,
                        'label': 'BE-GID',
                        'slug': 'be-gid',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'GWR-EGID',
                        'slug': 'gwr-egid',
                        'type': 'IntegerQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Ausnützung',
                        'slug': 'ausnuetzung',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Grünfläche in m²',
                        'slug': 'gruenflache-in-quadratmeter',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Überbauung in %',
                        'slug': 'ueberbauung-in-prozent',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
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
                        'hidden': False,
                        'label': 'Rechtliche Sicherung fremden Bodens?',
                        'slug': 'rechtliche-sicherung-fremden-bodens',
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
                        'hidden': False,
                        'label': 'Papierdossier',
                        'slug': 'papierdossier',
                        'type': 'ChoiceQuestion'
                    }
                ],
                'hidden': False,
                'label': 'Allgemeine Angaben',
                'slug': 'allgemeine-angaben',
                'type': 'FormQuestion'
            },
            {
                'children': [
                    {
                        'hidden': False,
                        'label': 'Nutzungszone',
                        'slug': 'nutzungszone',
                        'type': 'TextQuestion',
                        'value': 'Mischzone 3a '
                    },
                    {
                        'hidden': False,
                        'label': 'Überbauungsordnung',
                        'slug': 'ueberbauungsordnung',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Zulässige Geschosszahl',
                        'slug': 'zulaessige-geschosszahl',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'hidden': False,
                        'label': 'Empfindlichkeitsstufe (ES)',
                        'slug': 'empfindlichkeitsstufe',
                        'type': 'TextQuestion',
                        'value': None
                    },
                    {
                        'content': None,
                        'hidden': False,
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
                        'hidden': False,
                        'label': 'Höhe',
                        'slug': 'hoehe',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'hidden': False,
                        'label': 'Effektive Geschosszahl',
                        'slug': 'effektive-geschosszahl',
                        'type': 'IntegerQuestion',
                        'value': None
                    }
                ],
                'hidden': False,
                'label': 'Zonenvorschriften - Baurechtliche Grundordnung',
                'slug': 'zonenvorschriften-baurechtliche-grundordnung',
                'type': 'FormQuestion'
            },
            {
                'children': [
                    {
                        'choices': [
                            {
                                'checked': True,
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
                        'hidden': False,
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
                                'label': 'Ao'
                            },
                            {
                                'checked': True,
                                'label': 'Au'
                            },
                            {
                                'checked': False,
                                'label': 'Zu'
                            }
                        ],
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
                        'label': 'Bauten oder Pfählen im Grundwasser oder Grundwasserabsenkung',
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
                        'hidden': False,
                        'label': 'Gebiet mit bekannten oder vermuteten Naturgefahren',
                        'slug': 'gebiet-mit-naturgefahren',
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
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
                        'label': 'Wildtierschutz',
                        'slug': 'wildtierschutz',
                        'type': 'ChoiceQuestion'
                    }
                ],
                'hidden': False,
                'label': 'Zonenvorschriften - Schutzzonen',
                'slug': 'zonenvorschriften-schutzzonen',
                'type': 'FormQuestion'
            }
        ],
        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
                        'label': 'QSS-Stufe',
                        'slug': 'qss-stufe',
                        'type': 'MultipleChoiceQuestion'
                    }
                ],
                'hidden': False,
                'label': 'Brandschutz',
                'slug': 'brandschutz',
                'type': 'FormQuestion'
            },
            {
                'children': [
                    {
                        'content': None,
                        'hidden': False,
                        'label': 'Wohnungen',
                        'slug': 'wohnungen-titel',
                        'type': 'StaticQuestion'
                    },
                    {
                        'columns': [
                            'Anzahl bestehender Wohnungen dieser Grösse',
                            'Anzahl neuer Wohnungen dieser Grösse',
                            'Wohnungsgrösse (Anzahl Zimmer)'
                        ],
                        'hidden': False,
                        'label': 'Wohnungskategorie',
                        'rows': [
                        ],
                        'slug': 'wohnungen',
                        'type': 'TableQuestion'
                    },
                    {
                        'content': None,
                        'hidden': False,
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
                        'hidden': False,
                        'label': 'Autoabstellplätze für Fahrzeuge oder Fahrradabstellplätze?',
                        'slug': 'auto-oder-fahrradabstellplaetze',
                        'type': 'ChoiceQuestion'
                    }
                ],
                'hidden': False,
                'label': 'Wohnen',
                'slug': 'wohnen',
                'type': 'FormQuestion'
            }
        ],
        'hidden': False,
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
                        'hidden': False,
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
                            },
                            {
                                'checked': False,
                                'label': 'Nicht überprüft'
                            }
                        ],
                        'hidden': False,
                        'label': 'Werden die Planungs- oder Immissionsgrenzwerte der massgebenden Empfindlichkeitsstufe auf der bebaubaren Fläche überschritten?',
                        'slug': 'grenzwerte-ueberschritten',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'content': None,
                        'hidden': False,
                        'label': 'Immissionsschutz - Allgemeine Angaben',
                        'slug': 'immissionsschutz-allgemeine-angaben-titel',
                        'type': 'StaticQuestion'
                    },
                    {
                        'hidden': False,
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
                        'hidden': False,
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
                        'hidden': False,
                        'label': 'Beinhaltet das Vorhaben Neubauten, Umbauten, Erweiterungen oder Umnutzungen mit Anlagen oder Prozessen, welche Aussenlärm erzeugen?',
                        'slug': 'wird-aussenlaerm-erzeugt',
                        'type': 'ChoiceQuestion'
                    },
                    {
                        'content': None,
                        'hidden': False,
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
                        'hidden': False,
                        'label': 'Werden Luftemissionen erzeugt?',
                        'slug': 'werden-luftemissionen-erzeugt',
                        'type': 'ChoiceQuestion'
                    }
                ],
                'hidden': False,
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
                        'hidden': False,
                        'label': 'Gefahrenstufe',
                        'slug': 'gefahrenstufe',
                        'type': 'MultipleChoiceQuestion'
                    },
                    {
                        'columns': [
                            'Beschreibung der Gefährdung',
                            'Hauptprozessart',
                            'Prozessart'
                        ],
                        'hidden': False,
                        'label': 'Beschreibung der Prozessart',
                        'rows': [
                        ],
                        'slug': 'beschreibung-der-prozessart-tabelle',
                        'type': 'TableQuestion'
                    }
                ],
                'hidden': False,
                'label': 'Naturgefahren',
                'slug': 'naturgefahren',
                'type': 'FormQuestion'
            },
            {
                'children': [
                    {
                        'hidden': False,
                        'label': 'Gebäudeversicherungswert vor der Erneuerung in CHF',
                        'slug': 'gebaeudeversicherungswert-in-chf',
                        'type': 'IntegerQuestion',
                        'value': 2000000
                    }
                ],
                'hidden': False,
                'label': 'Hindernisfreies Bauen',
                'slug': 'hindernisfreies-bauen',
                'type': 'FormQuestion'
            }
        ],
        'hidden': False,
        'label': 'Spezialformulare',
        'slug': '5-spezialformulare',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Andere'
                    }
                ],
                'hidden': False,
                'label': 'Andere',
                'slug': 'andere-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Grundstücksentwässerungsplan SN 592 000'
                    }
                ],
                'hidden': False,
                'label': 'Grundstücksentwässerungsplan SN 592 000',
                'slug': 'grundstuecksentwaesserungsplan-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Vollmacht'
                    }
                ],
                'hidden': False,
                'label': 'Vollmacht',
                'slug': 'vollmacht-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Vorabklärung'
                    }
                ],
                'hidden': False,
                'label': 'Vorabklärung',
                'slug': 'vorabklaerung-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Sicherungsmassnahme'
                    }
                ],
                'hidden': False,
                'label': 'Sicherungsmassnahme',
                'slug': 'sicherungsmassnahme-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Berechnungen Abstellplätze'
                    }
                ],
                'hidden': False,
                'label': 'Berechnungen Abstellplätze',
                'slug': 'berechnungen-abstellplaetze-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Berechnung Kinderspielplätze / Aufenthaltsbereiche'
                    }
                ],
                'hidden': False,
                'label': 'Berechnung Kinderspielplätze / Aufenthaltsbereiche',
                'slug': 'berechnung-kinderspielplaetze-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Ausnützung'
                    }
                ],
                'hidden': False,
                'label': 'Ausnützung',
                'slug': 'ausnuetzung-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Grünfläche'
                    }
                ],
                'hidden': False,
                'label': 'Grünfläche',
                'slug': 'gruenflaeche-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Überbauung'
                    }
                ],
                'hidden': False,
                'label': 'Überbauung',
                'slug': 'ueberbauung-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Geschossflächen'
                    }
                ],
                'hidden': False,
                'label': 'Geschossflächen',
                'slug': 'geschossflaechen-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Regierungsratsbeschluss zum Bauinventar'
                    }
                ],
                'hidden': False,
                'label': 'Regierungsratsbeschluss zum Bauinventar',
                'slug': 'regierungsratsbeschluss-bauinventar-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Vertrag zum Bauinventar'
                    }
                ],
                'hidden': False,
                'label': 'Vertrag zum Bauinventar',
                'slug': 'vertrag-zum-bauinventar-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Inanspruchnahme Boden'
                    }
                ],
                'hidden': False,
                'label': 'Inanspruchnahme Boden',
                'slug': 'inanspruchnahme-boden-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Zustimmung des Eigentümers für den Anschluss an die Sammelkanäle bzw. zur Einleitung in einen Vorfluter wenn die Gemeinde nicht Eigentümerin ist'
                    }
                ],
                'hidden': False,
                'label': 'Zustimmung des Eigentümers für den Anschluss an die Sammelkanäle bzw. zur Einleitung in einen Vorfluter wenn die Gemeinde nicht Eigentümerin ist',
                'slug': 'anschluss-sammelkanaele-vorfluter-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Zustimmung der Anstösser falls die Versickerung nicht publiziert wurde'
                    }
                ],
                'hidden': False,
                'label': 'Zustimmung der Anstösser falls die Versickerung nicht publiziert wurde',
                'slug': 'zustimmung-der-anstoesser-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Zustimmung der Nachbarn nach 27 / 4 BewD'
                    }
                ],
                'hidden': False,
                'label': 'Zustimmung der Nachbarn nach 27 / 4 BewD',
                'slug': 'zustimmung-der-nachbarn-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Näherbau- / Grenzbaurecht'
                    }
                ],
                'hidden': False,
                'label': 'Näherbau- / Grenzbaurecht',
                'slug': 'naeherbau-grenzbaurecht-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'QS-Verantwortlicher und Projektorganisation'
                    }
                ],
                'hidden': False,
                'label': 'QS-Verantwortlicher und Projektorganisation',
                'slug': 'qs-verantwortlicher-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Brandschutzkonzept'
                    }
                ],
                'hidden': False,
                'label': 'Brandschutzkonzept',
                'slug': 'brandschutzkonzept-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Brandschutzplan'
                    }
                ],
                'hidden': False,
                'label': 'Brandschutzplan',
                'slug': 'brandschutzplan-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Qualitätssicherungskonzept'
                    }
                ],
                'hidden': False,
                'label': 'Qualitätssicherungskonzept',
                'slug': 'qualitaetssicherungskonzept-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Weitere Angaben bei Regeneration der EWS'
                    }
                ],
                'hidden': False,
                'label': 'Weitere Angaben bei Regeneration der EWS',
                'slug': 'weitere-angaben-regeneration-ews-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Formular für andere thermoaktive Elemente'
                    }
                ],
                'hidden': False,
                'label': 'Formular für andere thermoaktive Elemente',
                'slug': 'formular-andere-thermoaktive-elemente-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Sondenmodell mit Datenblatt'
                    }
                ],
                'hidden': False,
                'label': 'Sondenmodell mit Datenblatt',
                'slug': 'sondenmodell-mit-datenblatt-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Erdwärmensondendimensionierung'
                    }
                ],
                'hidden': False,
                'label': 'Erdwärmensondendimensionierung',
                'slug': 'erdwaermensondendimensionierung-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Auftragsbestätigung für Hydrogeologische Begleitung'
                    }
                ],
                'hidden': False,
                'label': 'Auftragsbestätigung für Hydrogeologische Begleitung',
                'slug': 'hydrogeologische-begleitung-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Konzessionsgesuch für den Betrieb einer Wärmepumpe'
                    }
                ],
                'hidden': False,
                'label': 'Konzessionsgesuch für den Betrieb einer Wärmepumpe',
                'slug': 'konzessionsgesuch-waermepumpe-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Konzessionsgesuch für den Betrieb einer Kühlwasseranlage'
                    }
                ],
                'hidden': False,
                'label': 'Konzessionsgesuch für den Betrieb einer Kühlwasseranlage',
                'slug': 'konzessionsgesuch-kuehlwasser-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Hydrogeologisches Gutachten bei Grundwassernutzung oder Bericht über die ökologischen Auswirkungen auf das Oberflächengewässer'
                    }
                ],
                'hidden': False,
                'label': 'Hydrogeologisches Gutachten bei Grundwassernutzung oder Bericht über die ökologischen Auswirkungen auf das Oberflächengewässer',
                'slug': 'hydrogeo-gutachten-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Vertrag - mit Sicherungsleistung befreite Gebäude'
                    }
                ],
                'hidden': False,
                'label': 'Vertrag - mit Sicherungsleistung befreite Gebäude',
                'slug': 'sicherungsleistung-befreit-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Schutzraum (1:50)'
                    }
                ],
                'hidden': False,
                'label': 'Schutzraum (1:50)',
                'slug': 'schutzraum-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Bewehrungsplan und Bewehrungsliste'
                    }
                ],
                'hidden': False,
                'label': 'Bewehrungsplan und Bewehrungsliste',
                'slug': 'bewehrungsplan-bewehrungsliste-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Betriebskonzept Gastgewerbe'
                    }
                ],
                'hidden': False,
                'label': 'Betriebskonzept Gastgewerbe',
                'slug': 'betriebskonzept-gastgewerbe-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Beschrieb der Lüftung/Bestätigung des Lüftungsbauers, dass die Lüftung keinen Rauch in die übrigen Räume des Betriebs gelangen lässt'
                    }
                ],
                'hidden': False,
                'label': 'Beschrieb der Lüftung/Bestätigung des Lüftungsbauers, dass die Lüftung keinen Rauch in die übrigen Räume des Betriebs gelangen lässt',
                'slug': 'beschrieb-der-lueftung-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Grundriss (Massstäblich (1:100 / 1:50) mit Angabe der Bodenfläche)'
                    }
                ],
                'hidden': False,
                'label': 'Grundriss (Massstäblich (1:100 / 1:50) mit Angabe der Bodenfläche)',
                'slug': 'grundriss-angabe-bodenflaeche-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Pläne Gastgewerbebetrieb'
                    }
                ],
                'hidden': False,
                'label': 'Pläne Gastgewerbebetrieb',
                'slug': 'plane-gastgewerbebetrieb-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Pläne Fumoir'
                    }
                ],
                'hidden': False,
                'label': 'Pläne Fumoir',
                'slug': 'plaene-fumoir-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Situationsplan'
                    }
                ],
                'hidden': False,
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
                'hidden': False,
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
                'hidden': False,
                'label': 'Schnitt',
                'slug': 'schnitt-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Fassaden / Ansichten (inklusive Angaben zu Fensterflächen)'
                    }
                ],
                'hidden': False,
                'label': 'Fassaden / Ansichten (inklusive Angaben zu Fensterflächen)',
                'slug': 'fassaden-ansichten-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Umgebungsplan'
                    }
                ],
                'hidden': False,
                'label': 'Umgebungsplan',
                'slug': 'umgebungsplan-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Werkleitungsplan'
                    }
                ],
                'hidden': False,
                'label': 'Werkleitungsplan',
                'slug': 'werkleitungsplan-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Pläne - Zugang zum Arbeitsbereich über Schleusen'
                    }
                ],
                'hidden': False,
                'label': 'Pläne - Zugang zum Arbeitsbereich über Schleusen',
                'slug': 'plaene-schleusen-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Pläne - Atmosphärischer Unterdruck'
                    }
                ],
                'hidden': False,
                'label': 'Pläne - Atmosphärischer Unterdruck',
                'slug': 'plaene-unterdruck-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Sterilisation Abwasser'
                    }
                ],
                'hidden': False,
                'label': 'Sterilisation Abwasser',
                'slug': 'sterilisation-abwasser-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Kurzbericht gemäss StFV'
                    }
                ],
                'hidden': False,
                'label': 'Kurzbericht gemäss StFV',
                'slug': 'kurzbericht-gemaess-stfv-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Risikoermittlung gemäss StFV'
                    }
                ],
                'hidden': False,
                'label': 'Risikoermittlung gemäss StFV',
                'slug': 'risikoermittlung-gemaess-stfv-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Stoffliste Störfallvorsorge'
                    }
                ],
                'hidden': False,
                'label': 'Stoffliste Störfallvorsorge',
                'slug': 'stoffliste-stoerfallvorsorge-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Sicherheitsdatenblätter Störfallvorsorge'
                    }
                ],
                'hidden': False,
                'label': 'Sicherheitsdatenblätter Störfallvorsorge',
                'slug': 'sicherheitsdaten-stoerfallvorsorge-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Entwässerung über Regenwasserkanal'
                    }
                ],
                'hidden': False,
                'label': 'Entwässerung über Regenwasserkanal',
                'slug': 'entwaesserung-ueber-regenwasserkanal-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Entwässerung über Oberflächengewässer'
                    }
                ],
                'hidden': False,
                'label': 'Entwässerung über Oberflächengewässer',
                'slug': 'entwaesserung-oberflaechengewaesser-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Entwässerung über Mischwasserkanal'
                    }
                ],
                'hidden': False,
                'label': 'Entwässerung über Mischwasserkanal',
                'slug': 'entwaesserung-ueber-mischwasserkanal-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Kanalisationskatasterplan'
                    }
                ],
                'hidden': False,
                'label': 'Kanalisationskatasterplan',
                'slug': 'kanalisationskatasterplan-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Pläne, Berichte und Berechnungen über neue und bestehende Versickerungsanlagen'
                    }
                ],
                'hidden': False,
                'label': 'Pläne, Berichte und Berechnungen über neue und bestehende Versickerungsanlagen',
                'slug': 'versickerungsanlagen-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Gewässerschutz Landwirtschaft'
                    }
                ],
                'hidden': False,
                'label': 'Gewässerschutz Landwirtschaft',
                'slug': 'gewaesserschutz-landwirtschaft-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Auftragsbestätigung des Fachbüro für die hydrogeologische Begleitung'
                    }
                ],
                'hidden': False,
                'label': 'Auftragsbestätigung des Fachbüro für die hydrogeologische Begleitung',
                'slug': 'bestaetigung-hydrogeo-begleitung-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Schnittplan mit Untergeschoss und Baugrubenumschliessung, eingezeichneter Wasserhaltung sowie mittlerem Grundwasserspiegel (mit den entsprechenden Koten in m ü.M.)'
                    }
                ],
                'hidden': False,
                'label': 'Schnittplan mit Untergeschoss und Baugrubenumschliessung, eingezeichneter Wasserhaltung sowie mittlerem Grundwasserspiegel (mit den entsprechenden Koten in m ü.M.)',
                'slug': 'schnittplan-gewaesserschutz-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Pfahl-, Injektions- oder Ankerpläne, Situation und Schnittpläne mit Koten in m ü.M. (falls geplant)'
                    }
                ],
                'hidden': False,
                'label': 'Pfahl-, Injektions- oder Ankerpläne, Situation und Schnittpläne mit Koten in m ü.M. (falls geplant)',
                'slug': 'plaene-gewaesserschutz-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Baugrunduntersuchung / Hydrogeologisches Gutachten'
                    }
                ],
                'hidden': False,
                'label': 'Baugrunduntersuchung / Hydrogeologisches Gutachten',
                'slug': 'baugrunduntersuchung-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Gesuch für eine Ausnahmebewilligung mit hydrogeologisches Gutachten und Nachweis, dass die Durchflusskapazität des Grundwassers gegenüber dem unbeinflussten Zustand um höchstens 10% vemindert wird.'
                    }
                ],
                'hidden': False,
                'label': 'Gesuch für eine Ausnahmebewilligung mit hydrogeologisches Gutachten und Nachweis, dass die Durchflusskapazität des Grundwassers gegenüber dem unbeinflussten Zustand um höchstens 10% vemindert wird.',
                'slug': 'gesuch-ausnahmebewilligung-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Energiedokumente'
                    }
                ],
                'hidden': False,
                'label': 'Energiedokumente',
                'slug': 'energiedokumente-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Gesuch um Erleichterung oder Befreiung Wärmeschutz'
                    }
                ],
                'hidden': False,
                'label': 'Gesuch um Erleichterung oder Befreiung Wärmeschutz',
                'slug': 'gesuch-erleichterung-waermeschutz-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Ausnahmegesuch Energie'
                    }
                ],
                'hidden': False,
                'label': 'Ausnahmegesuch Energie',
                'slug': 'ausnahmegesuch-energie-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Gesuch zur Ausnahme gemäss Art 31 Abs. 2 LSV'
                    }
                ],
                'hidden': False,
                'label': 'Gesuch zur Ausnahme gemäss Art 31 Abs. 2 LSV',
                'slug': 'gesuch-zur-ausnahme-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Nachweis Anforderungen gemäss Art 31 LSV'
                    }
                ],
                'hidden': False,
                'label': 'Lärmgutachten',
                'slug': 'nachweis-anforderungen-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Rückbau Checkliste / Selbstdeklaration'
                    }
                ],
                'hidden': False,
                'label': 'Rückbau Checkliste / Selbstdeklaration',
                'slug': 'rueckbau-checkliste-selbstdeklaration-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Entsorgungskonzept'
                    }
                ],
                'hidden': False,
                'label': 'Entsorgungskonzept',
                'slug': 'entsorgungskonzept-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Schadstoffermittlung / Gutachten'
                    }
                ],
                'hidden': False,
                'label': 'Schadstoffermittlung / Gutachten',
                'slug': 'schadstoffermittlung-gutachten-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Bodenschutzkonzept'
                    }
                ],
                'hidden': False,
                'label': 'Bodenschutzkonzept',
                'slug': 'bodenschutzkonzept-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Meldeblatt zur Fruchtfolgefläche'
                    }
                ],
                'hidden': False,
                'label': 'Meldeblatt zur Fruchtfolgefläche',
                'slug': 'meldeblatt-zur-fruchtfolgeflaeche-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Meldeblatt für Terrainveränderungen zur Bodenaufwertung'
                    }
                ],
                'hidden': False,
                'label': 'Meldeblatt für Terrainveränderungen zur Bodenaufwertung',
                'slug': 'meldeblatt-terrainveraenderungen-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Deklaration zur Verwertung von abgetragenem Boden'
                    }
                ],
                'hidden': False,
                'label': 'Deklaration zur Verwertung von abgetragenem Boden',
                'slug': 'verwertung-abgetragenem-boden-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Einverständniserklärung Rodung / Aufforstung'
                    }
                ],
                'hidden': False,
                'label': 'Einverständniserklärung Rodung / Aufforstung',
                'slug': 'einverstaendniserklaerung-wald-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Rodungsgesuchsformular BAFU'
                    }
                ],
                'hidden': False,
                'label': 'Rodungsgesuchsformular BAFU',
                'slug': 'rodungsgesuchsformular-bafu-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': "Übersichtsplan 1:25'000"
                    }
                ],
                'hidden': False,
                'label': "Übersichtsplan 1:25'000",
                'slug': 'uebersichtsplan-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Rodungs- und Ersatzaufforstungsplan'
                    }
                ],
                'hidden': False,
                'label': 'Rodungs- und Ersatzaufforstungsplan',
                'slug': 'rodungs-und-ersatzaufforstungsplan-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Gefahrengutachten'
                    }
                ],
                'hidden': False,
                'label': 'Gefahrengutachten',
                'slug': 'gefahrengutachten-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Voruntersuchung'
                    }
                ],
                'hidden': False,
                'label': 'Voruntersuchung',
                'slug': 'voruntersuchung-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Umweltverträglichkeitsbericht'
                    }
                ],
                'hidden': False,
                'label': 'Umweltverträglichkeitsbericht',
                'slug': 'umweltvertraeglichkeitsbericht-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Fassadenplan mit eingezeichnetem Reklamestandort'
                    }
                ],
                'hidden': False,
                'label': 'Fassadenplan mit eingezeichnetem Reklamestandort',
                'slug': 'fassadenplan-reklamestandort-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Skizze der Reklame mit Farbangaben'
                    }
                ],
                'hidden': False,
                'label': 'Skizze der Reklame mit Farbangaben',
                'slug': 'skizze-der-reklame-mit-farbangaben-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Baubewilligung von Um- und Ausbauprojekten'
                    }
                ],
                'hidden': False,
                'label': 'Baubewilligung von Um- und Ausbauprojekten',
                'slug': 'baubewilligung-ausbauprojekte-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Baubewilligungsakte'
                    }
                ],
                'hidden': False,
                'label': 'Baubewilligungsakte',
                'slug': 'baubewilligungsakte-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Ausnahmebegründung'
                    }
                ],
                'hidden': False,
                'label': 'Ausnahmebegründung',
                'slug': 'ausnahmebegruendung-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Dokumente der Bauausführung'
                    }
                ],
                'hidden': False,
                'label': 'Dokumente der Bauausführung',
                'slug': 'dokumente-der-bauausfuehrung-dokument',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Formular Erdbebensicherheit (EbS)'
                    }
                ],
                'hidden': False,
                'label': 'Formular Erdbebensicherheit (EbS)',
                'slug': 'formular-erdbebensicherheit-ebs',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': 'Gemeindespezifisches Formular (5.0, 5.1, 5.2, 5.3 5.4, 5.5, 5.8)'
                    }
                ],
                'hidden': False,
                'label': 'Gemeindespezifisches Formular (5.0, 5.1, 5.2, 5.3 5.4, 5.5, 5.8)',
                'slug': 'gemeindespezifisches-formular',
                'type': 'MultipleChoiceQuestion'
            }
        ],
        'hidden': False,
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
                'hidden': False,
                'label': 'Die Anforderungen sind gemäss Art. 11 – 15 BewD eingehalten.',
                'slug': 'anforderungen-eingehalten',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Der/die Gesuchsteller/in verzichtet für sich und seine/ihre Rechtsnachfolger ausdrücklich auf jeden Ersatz von Schaden, der durch den Forstbetrieb oder durch Naturereignisse, wie Schneedruck, Windfall usw. an der zu erstellenden Baute, bzw. ähnlichen Anlage verursacht werden könnte. Vorbehalten bleiben jedoch die Bestimmungen der Art. 41 ff. OR.'
                    }
                ],
                'hidden': False,
                'label': 'Der/die Gesuchsteller/in verzichtet für sich und seine/ihre Rechtsnachfolger ausdrücklich auf jeden Ersatz von Schaden, der durch den Forstbetrieb oder durch Naturereignisse, wie Schneedruck, Windfall usw. an der zu erstellenden Baute, bzw. ähnlichen Anlage verursacht werden könnte. Vorbehalten bleiben jedoch die Bestimmungen der Art. 41 ff. OR.',
                'slug': 'verzicht-schadensersatz-naturereignisse',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Bei einer allfälligen Handänderung verpflichten sich die Bauherrschaft und Grundeigentümerin/Grundeigentümer, bzw. Baurechtsnehmerin/Baurechtsnehmer, diese Erklärung einer allfälligen Rechtsnachfolge zu überbinden.'
                    }
                ],
                'hidden': False,
                'label': 'Bei einer allfälligen Handänderung verpflichten sich die Bauherrschaft und Grundeigentümerin/Grundeigentümer, bzw. Baurechtsnehmerin/Baurechtsnehmer, diese Erklärung einer allfälligen Rechtsnachfolge zu überbinden.',
                'slug': 'verpflichtung-bei-handaenderung',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Der/die Gesuchsteller/in ist verantwortlich für die Einhaltung der Radonvorgaben gemäss Strahlenschutzverordnung des Bundes.'
                    }
                ],
                'hidden': False,
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
                'hidden': False,
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
                'hidden': False,
                'label': 'Der/die Gesuchsteller/in bestätigt, dass die Liegenschaftsentwässerung gemäss dem AWA-Merkblatt "Entwässerung von Industrie- und Gewerbeliegenschaften" geplant und realisiert werden. Als Beilage enthält das Gesuch einen Umgebungsplan, auf dem bei allen Teilfächen die vorgesehene Nutzung, die Befestigungsart, das Gefälle sowie die Entwässerungsart eingetragen sind.',
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
                'hidden': False,
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
                'hidden': False,
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
                'hidden': False,
                'label': 'Der/die Gesuchsteller/in bestätigt, dass die vom GIS-System übernommen Daten mit den baurechtlichen Grundlagen übereinstimmen.',
                'slug': 'bestaetigung-gis',
                'type': 'MultipleChoiceQuestion'
            }
        ],
        'hidden': False,
        'label': 'Bestätigung',
        'slug': '7-bestaetigung',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'label': 'Gesuchsteller/in',
                'people': [
                    {
                        'familyName': 'Mustermann',
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

snapshots['test_document_merge_service_snapshot[1-sb1] 1'] = [
    {
        'children': [
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
                'hidden': False,
                'label': 'Sind die Bedingungen und Auflagen der Baubewilligung (vor Baubeginn) erfüllt?',
                'slug': 'bedingungen-und-auflagen-erfuellt',
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
                'hidden': False,
                'label': 'Ist eine Schnurgerüstabnahme erforderlich?',
                'slug': 'ist-eine-schnurgerustabnahme-erforderlich',
                'type': 'ChoiceQuestion'
            },
            {
                'hidden': False,
                'label': 'Beginn Bauarbeiten',
                'slug': 'beginn-bauarbeiten',
                'type': 'DateQuestion',
                'value': None
            },
            {
                'hidden': False,
                'label': 'Bemerkungen',
                'slug': 'bemerkungen-sb1',
                'type': 'TextareaQuestion',
                'value': None
            }
        ],
        'hidden': False,
        'label': 'Selbstdeklaration',
        'slug': 'selbstdeklaration-sb1',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'content': None,
                'hidden': False,
                'label': 'Dokumente Platzhalter',
                'slug': 'dokumente-platzhalter',
                'type': 'StaticQuestion'
            }
        ],
        'hidden': False,
        'label': 'Dokumente',
        'slug': 'dokumente-sb1',
        'type': 'FormQuestion'
    }
]

snapshots['test_document_merge_service_snapshot[1-sb2] 1'] = [
    {
        'children': [
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
                'hidden': False,
                'label': 'Ist das Bauvorhaben nach der Baubewilligung und evtl. Projektänderungsbewilligung ausgeführt?',
                'slug': 'bauvorhaben-nach-baubewilligung-ausgefuehrt',
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
                'hidden': False,
                'label': 'Sind die Bedingungen und Auflagen der Baubewilligung eingehalten?',
                'slug': 'bedingungen-auflagen-eingehalten',
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
                'hidden': False,
                'label': 'Sind die Sicherheitsvorschriften eingehalten?',
                'slug': 'sicherheitsvorschriften-eingehalten',
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
                'hidden': False,
                'label': 'Sind die Nebengebäude fertiggestellt?',
                'slug': 'sind-die-nebengebaeude-fertiggestellt',
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
                'hidden': False,
                'label': 'Sind die Umgebungsarbeiten fertiggestellt?',
                'slug': 'sind-die-umgebungsarbeiten-fertiggestellt',
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
                'hidden': False,
                'label': 'Meldung Tankanlage',
                'slug': 'meldung-tankanlage',
                'type': 'ChoiceQuestion'
            },
            {
                'hidden': False,
                'label': 'Bemerkungen',
                'slug': 'bemerkungen-abschluss-sb2',
                'type': 'TextareaQuestion',
                'value': None
            }
        ],
        'hidden': False,
        'label': 'Abschluss',
        'slug': 'abschluss-sb2',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'content': None,
                'hidden': False,
                'label': 'Dokumente Platzhalter',
                'slug': 'dokumente-platzhalter',
                'type': 'StaticQuestion'
            }
        ],
        'hidden': False,
        'label': 'Dokumente',
        'slug': 'dokumente-sb2',
        'type': 'FormQuestion'
    }
]

snapshots['test_document_merge_service_snapshot[3-None] 1'] = [
    {
        'children': [
            {
                'hidden': False,
                'label': 'Name',
                'slug': 'name-gesuchstellerin-vorabklaerung',
                'type': 'TextQuestion',
                'value': 'Muster'
            },
            {
                'hidden': False,
                'label': 'Vorname',
                'slug': 'vorname-gesuchstellerin-vorabklaerung',
                'type': 'TextQuestion',
                'value': 'Max'
            },
            {
                'hidden': False,
                'label': 'Strasse',
                'slug': 'strasse-gesuchstellerin',
                'type': 'TextQuestion',
                'value': 'asdfstr.'
            },
            {
                'hidden': False,
                'label': 'Nummer',
                'slug': 'nummer-gesuchstellerin',
                'type': 'TextQuestion',
                'value': '1'
            },
            {
                'hidden': False,
                'label': 'PLZ',
                'slug': 'plz-gesuchstellerin',
                'type': 'IntegerQuestion',
                'value': 3000
            },
            {
                'hidden': False,
                'label': 'Ort',
                'slug': 'ort-gesuchstellerin',
                'type': 'TextQuestion',
                'value': 'Bern'
            },
            {
                'hidden': False,
                'label': 'Zuständige Gemeinde',
                'slug': 'gemeinde',
                'type': 'TextQuestion',
                'value': 'Burgdorf'
            },
            {
                'hidden': False,
                'label': 'Karte',
                'slug': 'karte-einfache-vorabklaerung',
                'type': 'TextQuestion',
                'value': 'undefined'
            },
            {
                'hidden': False,
                'label': 'Lagekoordinaten - Ost',
                'slug': 'lagekoordinaten-ost-einfache-vorabklaerung',
                'type': 'FloatQuestion',
                'value': '2614314'
            },
            {
                'hidden': False,
                'label': 'Lagekoordinaten – Nord',
                'slug': 'lagekoordinaten-nord-einfache-vorabklaerung',
                'type': 'FloatQuestion',
                'value': '1211926'
            },
            {
                'hidden': False,
                'label': 'Parzellennummer',
                'slug': 'parzellennummer',
                'type': 'TextQuestion',
                'value': '1'
            },
            {
                'hidden': False,
                'label': 'Liegenschaftsnummer',
                'slug': 'liegenschaftsnummer',
                'type': 'IntegerQuestion',
                'value': None
            },
            {
                'hidden': False,
                'label': 'BE-GID',
                'slug': 'be-gid',
                'type': 'TextQuestion',
                'value': None
            },
            {
                'hidden': False,
                'label': 'GWR-EGID',
                'slug': 'gwr-egid',
                'type': 'IntegerQuestion',
                'value': None
            },
            {
                'hidden': False,
                'label': 'E-GRID-Nr.',
                'slug': 'e-grid-nr',
                'type': 'TextQuestion',
                'value': 'CH273589324696'
            },
            {
                'hidden': False,
                'label': 'Anfrage zur Vorabklärung',
                'slug': 'anfrage-zur-vorabklaerung',
                'type': 'TextareaQuestion',
                'value': 'bitte abklaeren'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': 'Der/die Gesuchsteller/in bestätigt, dass die vom GIS-System übernommen Daten mit den baurechtlichen Grundlagen übereinstimmen.'
                    }
                ],
                'hidden': False,
                'label': 'Der/die Gesuchsteller/in bestätigt, dass die vom GIS-System übernommen Daten mit den baurechtlichen Grundlagen übereinstimmen.',
                'slug': 'bestaetigung-gis',
                'type': 'MultipleChoiceQuestion'
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
                'hidden': False,
                'label': 'Papierdossier',
                'slug': 'papierdossier',
                'type': 'ChoiceQuestion'
            }
        ],
        'hidden': False,
        'label': 'Allgemeine Informationen',
        'slug': 'allgemeine-informationen-vorabklaerung-form',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'content': None,
                'hidden': False,
                'label': 'Dokumente Platzhalter',
                'slug': 'dokumente-platzhalter',
                'type': 'StaticQuestion'
            }
        ],
        'hidden': False,
        'label': 'Dokumente',
        'slug': 'dokumente-vorabklaerung-form',
        'type': 'FormQuestion'
    },
    {
        'label': 'Gesuchsteller/in',
        'people': [
            {
                'familyName': 'Muster',
                'givenName': 'Max'
            }
        ],
        'type': 'SignatureQuestion'
    }
]
