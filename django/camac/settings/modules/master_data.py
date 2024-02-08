SO_PERSONAL_DATA_MAPPING = {
    "last_name": "nachname",
    "first_name": "vorname",
    "street": "strasse",
    "street_number": "strasse-nummer",
    "zip": "plz",
    "town": "ort",
    "email": "e-mail",
    "tel": "telefon",
    "is_juristic_person": (
        "juristische-person",
        {
            "value_parser": (
                "value_mapping",
                {
                    "mapping": {
                        "juristische-person-ja": True,
                        "juristische-person-nein": False,
                    }
                },
            )
        },
    ),
    "juristic_name": "juristische-person-name",
}


MASTER_DATA = {
    "default": {},
    "kt_schwyz": {
        "ENABLED": True,
        "CONFIG": {
            "organization_category": (
                "static",
                "ebausz",
            ),  # TODO: change this value 'decisionRulingType'
            "applicants": (
                "ng_table",
                [
                    "bauherrschaft",
                    "bauherrschaft-v2",
                    "bauherrschaft-v3",
                    "bauherrschaft-override",
                ],
                {
                    "column_mapping": {
                        "last_name": "name",
                        "first_name": "vorname",
                        "street": "strasse",
                        "zip": "plz",
                        "town": "ort",
                        "country": ("static", "Schweiz"),
                        "is_juristic_person": (
                            "anrede",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Herr": False,
                                            "Frau": False,
                                            "Firma": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "firma",
                        "company": "firma",
                        "email": "email",
                        "phone": "tel",
                    }
                },
            ),
            "building_owners": (
                "ng_table",
                [
                    "bauherrschaft",
                    "bauherrschaft-v2",
                    "bauherrschaft-v3",
                    "bauherrschaft-override",
                ],  # TODO: hauseigentümerschaft in SZ?
                {
                    "column_mapping": {
                        "last_name": "name",
                        "first_name": "vorname",
                        "street": "strasse",
                        "zip": "plz",
                        "town": "ort",
                        "country": ("static", "Schweiz"),
                        "is_juristic_person": (
                            "anrede",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Herr": False,
                                            "Frau": False,
                                            "Firma": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "firma",
                        "company": "firma",
                        "email": "email",
                        "phone": "tel",
                    }
                },
            ),
            "legal_representatives": (
                "ng_table",
                [
                    "vertreter-mit-vollmacht",
                    "vertreter-mit-vollmacht-v2",
                    "vertreter-mit-vollmacht-override",
                ],
                {
                    "column_mapping": {
                        "last_name": "name",
                        "first_name": "vorname",
                        "street": "strasse",
                        "zip": "plz",
                        "town": "ort",
                        "country": ("static", "Schweiz"),
                        "is_juristic_person": (
                            "anrede",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Herr": False,
                                            "Frau": False,
                                            "Firma": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "firma",
                        "company": "firma",
                        "email": "email",
                        "phone": "tel",
                    }
                },
            ),
            "landowners": (
                "ng_table",
                [
                    "grundeigentumerschaft",
                    "grundeigentumerschaft-v2",
                    "grundeigentumerschaft-override",
                ],
                {
                    "column_mapping": {
                        "last_name": "name",
                        "first_name": "vorname",
                        "street": "strasse",
                        "zip": "plz",
                        "town": "ort",
                        "country": ("static", "Schweiz"),
                        "is_juristic_person": (
                            "anrede",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Herr": False,
                                            "Frau": False,
                                            "Firma": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "firma",
                        "company": "firma",
                        "email": "email",
                        "phone": "tel",
                    }
                },
            ),
            "project_authors": (
                "ng_table",
                [
                    "projektverfasser-planer",
                    "projektverfasser-planer-v2",
                    "projektverfasser-planer-v3",
                    "projektverfasser-planer-override",
                ],
                {
                    "column_mapping": {
                        "last_name": "name",
                        "first_name": "vorname",
                        "street": "strasse",
                        "zip": "plz",
                        "town": "ort",
                        "country": ("static", "Schweiz"),
                        "is_juristic_person": (
                            "anrede",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Herr": False,
                                            "Frau": False,
                                            "Firma": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "firma",
                        "company": "firma",
                        "email": "email",
                        "phone": "tel",
                    }
                },
            ),
            "street": ("ng_answer", "ortsbezeichnung-des-vorhabens"),
            "street_addition": ("ng_answer", "standort-spezialbezeichnung"),
            "street_number": ("static", None),
            "city": ("ng_answer", "standort-ort"),
            "zip": ("static", None),
            "submit_date": ("first_workflow_entry", [10]),
            "publication_date": ("first_workflow_entry", [15]),
            "decision_date": (
                "answer",
                "bewilligungsverfahren-gr-sitzung-bewilligungsdatum",
                {
                    "document_from_work_item": "building-authority",
                    "value_key": "date",
                },
            ),
            "construction_start_date": (
                "baukontrolle",
                "baukontrolle-realisierung-baubeginn",
            ),
            "construction_duration": ("static", None),
            "profile_approval_date": (
                "baukontrolle",
                "baukontrolle-realisierung-schnurgeruestabnahme",
            ),
            "final_approval_date": (
                "baukontrolle",
                "baukontrolle-realisierung-schlussabnahme",
            ),
            "completion_date": (
                "baukontrolle",
                "baukontrolle-realisierung-bauende",
            ),
            "dossier_number": (
                "instance_property",
                "identifier",
            ),  # eCH0211: 3.1.1.1.1, 3.1.1.1.2
            # TODO remove?
            "municipality": ("instance_property", "location"),
            "municipality_name": ("instance_property", "location"),
            "nature_risk": ("static", None),
            "proposal": (
                "ng_answer",
                ["bezeichnung", "bezeichnung-override"],
            ),  # eCH0211: 3.1.1.2
            "remark": (
                "ng_answer",
                "vollstaendigkeitspruefung-bemerkung",
            ),  # eCH0211: 3.1.1.4
            "construction_costs": ("ng_answer", "baukosten"),  # eCH0211: 3.1.1.11
            "usage_zone": (
                "ng_answer",
                "betroffene-nutzungszonen",
            ),  # eCH0211: 3.8.1.3 TODO: verify!
            "usage_type": ("ng_answer", "art-der-nutzung"),  # TODO: verify!
            "application_type": (
                "instance_property",
                "form.description",
            ),  # `proceeding_type` in context of eCH standard
            #  SZ stores this as `instance.form.name`  # TODO: verify!
            "application_type_migrated": (  # not the same as regular application_type that requires predefined choices
                "ng_answer",
                "verfahrensart-migriertes-dossier",
            ),
            "proceeding_type": (  # TODO: verify!
                ("ng_answer", "verfahrensart")
            ),  # this is called "Verfahrensart" in context of eCH
            "coordinates": (
                "ng_table",
                "punkte",
                {"column_mapping": {"lat": "lat", "lng": "lng"}},
            ),
            "plot_data": (
                "ng_table",
                "parzellen",
                {
                    "column_mapping": {
                        "plot_number": "number",
                        "egrid_number": "egrid",
                    }
                },
            ),
            "parking_lots": ("static", None),
            "buildings": (
                "ng_table",
                ["gwr", "gwr-v2"],
                {
                    "column_mapping": {
                        "name": "gebaeudebezeichnung",
                        "building_category": (
                            "kategorie",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Andere Wohngebäude (Wohngebäude mit Nebennutzung)": 1030,
                                            "Gebäude mit ausschliesslicher Wohnnutzung": 1020,
                                            "Gebäude ohne Wohnnutzung": 1060,
                                            "Provisorische Unterkunft": 1010,
                                            "Sonderbau": 1080,
                                            "Gebäude mit teilweiser Wohnnutzung": 1040,
                                        }
                                    },
                                )
                            },
                        ),
                        "civil_defense_shelter": (
                            "zivilschutzraum",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Ja": True,
                                            "Nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "heating_heat_generator": (
                            "heizungsart",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Einzelofenheizung": 7436,
                                            "Etagenheizung": 7499,
                                            "Zentralheizung für das Gebäude": 7450,
                                            "Zentralheizung für mehrere Gebäude": 7451,
                                            "Öffentliche Fernwärmeversorgung": 7461,
                                            "Keine Heizung": 7400,
                                            "Kein Wärmeerzeuger": 7400,
                                            "Wärmepumpe für ein Gebäude": 7410,
                                            "Wärmepumpe für mehrere Gebäude": 7411,
                                            "Thermische Solaranlage für ein Gebäude": 7420,
                                            "Thermische Solaranlage für mehrere Gebäude": 7421,
                                            "Heizkessel (generisch) für ein Gebäude": 7430,
                                            "Heizkessel (generisch) für mehrere Gebäude": 7431,
                                            "Heizkessel nicht kondensierend für ein Gebäude": 7431,
                                            "Heizkessel nicht kondensierend für mehrere Gebäude": 7432,
                                            "Heizkessel kondensierend für ein Gebäude": 7434,
                                            "Heizkessel kondensierend für mehrere Gebäude": 7435,
                                            "Ofen": 7436,
                                            "Wärmekraftkopplungsanlage für ein Gebäude": 7440,
                                            "Wärmekraftkopplungsanlage für mehrere Gebäude": 7441,
                                            "Elektrospeicher-Zentralheizung für ein Gebäude": 7450,
                                            "Elektrospeicher-Zentralheizung für mehrere Gebäude": 7451,
                                            "Elektro direkt": 7452,
                                            "Wärmetauscher (einschliesslich für Fernwärme) für ein Gebäude": 7460,
                                            "Wärmetauscher (einschliesslich für Fernwärme) für mehrere Gebäude": 7461,
                                            "Andere": 7499,
                                            "Noch nicht festgelegt": None,
                                        }
                                    },
                                )
                            },
                        ),
                        "heating_energy_source": (
                            "energietrager-heizung",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Heizöl": 7530,
                                            "Holz": 7540,
                                            "Altholz": 7541,
                                            "Wärmepumpe": 7599,
                                            "Elektrizität": 7560,
                                            "Gas": 7520,
                                            "Fernwärme (Heisswasser oder Dampf)": 7581,
                                            "Kohle": 7599,
                                            "Sonnenkollektor": 7570,
                                            "Keine": 7500,
                                            "Luft": 7501,
                                            "Erdwärme (generisch)": 7510,
                                            "Erdwärmesonde": 7511,
                                            "Erdregister": 7512,
                                            "Wasser (Grundwasser, Oberflächenwasser, Abwasser)": 7513,
                                            "Holz (generisch)": 7540,
                                            "Holz (Stückholz)": 7541,
                                            "Holz (Pellets)": 7542,
                                            "Abwärme (innerhalb des Gebäudes)": 7550,
                                            "Sonne (thermisch)": 7570,
                                            "Fernwärme (generisch)": 7580,
                                            "Fernwärme (Hochtemperatur)": 7581,
                                            "Fernwärme (Niedertemperatur)": 7582,
                                            "Unbestimmt": 7598,
                                            "Andere": 7599,
                                            "Noch nicht festgelegt": None,
                                        }
                                    },
                                )
                            },
                        ),
                        "warmwater_heat_generator": (
                            "waermeerzeuger-warmwasser",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Kein Wärmeerzeuger": 7600,
                                            "Wärmepumpe": 7610,
                                            "Thermische Solaranlage": 7620,
                                            "Heizkessel (generisch)": 7630,
                                            "Heizkessel nicht kondensierend": 7632,
                                            "Heizkessel kondensierend": 7634,
                                            "Wärmekraftkopplungsanlage": 7640,
                                            "Zentraler Elektroboiler": 7650,
                                            "Kleinboiler": 7651,
                                            "Wärmetauscher (einschliesslich für Fernwärme)": 7660,
                                            "Andere": 7699,
                                        }
                                    },
                                )
                            },
                        ),
                        "warmwater_energy_source": (
                            "energietrager-warmwasser",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Heizöl": 7530,
                                            "Holz": 7540,
                                            "Altholz": 7541,
                                            "Wärmepumpe": 7599,
                                            "Elektrizität": 7560,
                                            "Gas": 7520,
                                            "Fernwärme (Heisswasser oder Dampf)": 7581,
                                            "Kohle": 7599,
                                            "Sonnenkollektor": 7570,
                                            "Keine": 7500,
                                            "Luft": 7501,
                                            "Erdwärme (generisch)": 7510,
                                            "Erdwärmesonde": 7511,
                                            "Erdregister": 7512,
                                            "Wasser (Grundwasser, Oberflächenwasser, Abwasser)": 7513,
                                            "Holz (generisch)": 7540,
                                            "Holz (Stückholz)": 7541,
                                            "Holz (Pellets)": 7542,
                                            "Abwärme (innerhalb des Gebäudes)": 7550,
                                            "Sonne (thermisch)": 7570,
                                            "Fernwärme (generisch)": 7580,
                                            "Fernwärme (Hochtemperatur)": 7581,
                                            "Fernwärme (Niedertemperatur)": 7582,
                                            "Unbestimmt": 7598,
                                            "Andere": 7599,
                                            "Noch nicht festgelegt": None,
                                        }
                                    },
                                )
                            },
                        ),
                        "number_of_floors": "geschosse",
                        "number_of_rooms": "wohnraeume",
                        "dwellings": (
                            "wohnungen",
                            {
                                "value_parser": (
                                    "list_mapping",
                                    {
                                        "mapping": {
                                            "location_on_floor": "lage",
                                            "number_of_rooms": "zimmer",
                                            "kitchen_facilities": "kuchenart",
                                            "has_kitchen_facilities": (
                                                ["kuchenart", "kocheinrichtung"],
                                                {
                                                    "value_parser": (
                                                        "value_mapping",
                                                        {
                                                            "mapping": {
                                                                "Ja": True,
                                                                "Nein": False,
                                                                "Küche (min. 4m²)": True,
                                                                "Kochnische (unter 4m²)": True,
                                                                "Weder Küche noch Kochnische": False,
                                                            }
                                                        },
                                                    )
                                                },
                                            ),
                                            "area": "flache",
                                            "multiple_floors": (
                                                "maisonette",
                                                {
                                                    "value_parser": (
                                                        "value_mapping",
                                                        {
                                                            "mapping": {
                                                                "Ja": True,
                                                                "Nein": False,
                                                            }
                                                        },
                                                    )
                                                },
                                            ),
                                        }
                                    },
                                )
                            },
                        ),
                    }
                },
            ),
        },
    },
    "kt_bern": {
        "ENABLED": True,
        "CONFIG": {
            "organization_category": ("static", "ebaube"),
            "remark": ("answer", "bemerkungen"),
            "applicants": (
                "table",
                "personalien-gesuchstellerin",
                {
                    "column_mapping": {
                        "last_name": "name-gesuchstellerin",
                        "first_name": "vorname-gesuchstellerin",
                        "street": "strasse-gesuchstellerin",
                        "street_number": "nummer-gesuchstellerin",
                        "zip": "plz-gesuchstellerin",
                        "town": "ort-gesuchstellerin",
                        "is_juristic_person": (
                            "juristische-person-gesuchstellerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-gesuchstellerin-ja": True,
                                            "juristische-person-gesuchstellerin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-gesuchstellerin",
                    }
                },
            ),
            "building_owners": (
                "table",
                "personalien-gebaudeeigentumerin",
                {
                    "column_mapping": {
                        "last_name": "name-gebaeudeeigentuemerin",
                        "first_name": "vorname-gebaeudeeigentuemerin",
                        "street": "strasse-gebaeudeeigentuemerin",
                        "street_number": "nummer-gebaeudeeigentuemerin",
                        "zip": "plz-gebaeudeeigentuemerin",
                        "town": "ort-gebaeudeeigentuemerin",
                        "is_juristic_person": (
                            "juristische-person-gebaeudeeigentuemerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-gebaeudeeigentuemer-ja": True,
                                            "juristische-person-gebaeudeeigentuemer-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-gebaeudeeigentuemerin",
                    }
                },
            ),
            "landowners": (
                "table",
                "personalien-grundeigentumerin",
                {
                    "column_mapping": {
                        "last_name": "name-grundeigentuemerin",
                        "first_name": "vorname-grundeigentuemerin",
                        "street": "strasse-grundeigentuemerin",
                        "street_number": "nummer-grundeigentuemerin",
                        "zip": "plz-grundeigentuemerin",
                        "town": "ort-grundeigentuemerin",
                        "is_juristic_person": (
                            "juristische-person-grundeigentuemerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-grundeigentuemerin-ja": True,
                                            "juristische-person-grundeigentuemerin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-grundeigentuemerin",
                    }
                },
            ),
            "project_authors": (
                "table",
                "personalien-projektverfasserin",
                {
                    "column_mapping": {
                        "last_name": "name-projektverfasserin",
                        "first_name": "vorname-projektverfasserin",
                        "street": "strasse-projektverfasserin",
                        "street_number": "nummer-projektverfasserin",
                        "zip": "plz-projektverfasserin",
                        "town": "ort-projektverfasserin",
                        "is_juristic_person": (
                            "juristische-person-projektverfasserin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-projektverfasserin-ja": True,
                                            "juristische-person-projektverfasserin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-projektverfasserin",
                    }
                },
            ),
            "legal_representatives": (
                "table",
                "personalien-vertreterin-mit-vollmacht",
                {
                    "column_mapping": {
                        "last_name": "name-vertreterin",
                        "first_name": "vorname-vertreterin",
                        "street": "strasse-vertreterin",
                        "street_number": "nummer-vertreterin",
                        "zip": "plz-vertreterin",
                        "town": "ort-vertreterin",
                        "is_juristic_person": (
                            "juristische-person-vertreterin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-vertreterin-ja": True,
                                            "juristische-person-vertreterin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-vertreterin",
                    }
                },
            ),
            "dossier_number": ("case_meta", "ebau-number"),
            "project": ("answer", "baubeschrieb", {"value_parser": "option"}),
            "water_protection_area": (
                "answer",
                ["gewaesserschutzbereich", "gewaesserschutzbereich-v2"],
                {"value_parser": "option"},
            ),
            "protection_area": (
                "answer",
                ["grundwasserschutzzonen", "grundwasserschutzzonen-v2"],
                {"value_parser": "option"},
            ),
            "public": ("answer", "oeffentlichkeit", {"value_parser": "option"}),
            "protected": ("answer", "schuetzenswert", {"value_parser": "option"}),
            "conservable": ("answer", "erhaltenswert", {"value_parser": "option"}),
            "k_object": ("answer", "k-objekt", {"value_parser": "option"}),
            "construction_group_designation": ("answer", "bezeichnung-baugruppe"),
            "construction_group": (
                "answer",
                "baugruppe-bauinventar",
                {"value_parser": "option"},
            ),
            "rrb": ("answer", "rrb", {"value_parser": "option"}),
            "rrb_start": ("answer", "rrb-vom", {"value_key": "date"}),
            "contract": ("answer", "vertrag", {"value_parser": "option"}),
            "contract_start": ("answer", "vertrag-vom", {"value_key": "date"}),
            "alcohol_serving": (
                "answer",
                "alkoholausschank",
                {
                    "value_parser": (
                        "value_mapping",
                        {
                            "mapping": {
                                "alkoholausschank-ja": "mit",
                                "alkoholausschank-nein": "ohne",
                            }
                        },
                    )
                },
            ),
            "interior_seating": (
                "table",
                "ausschankraeume",
                {"column_mapping": {"total_seats": "sitzplaetze"}},
            ),
            "outside_seating": (
                "answer",
                "sitzplaetze-garten",
            ),
            "usage_type": (
                "answer",
                "nutzungsart",
                {"value_parser": "option", "prop": "label"},
            ),
            "usage_zone": ("answer", "nutzungszone"),
            "application_type": ("form_name",),
            "proceeding_type": (
                "static",
                None,
            ),  # TODO: consider "Um welche Gesuchsbewilligungsart handelt es sich?" from formal exam
            "development_regulations": ("answer", "ueberbauungsordnung"),
            "situation": ("answer", "sachverhalt"),
            "proposal": ("answer", "beschreibung-bauvorhaben"),
            "description_modification": ("answer", "beschreibung-projektaenderung"),
            "street": ("answer", "strasse-flurname"),
            "street_number": ("answer", "nr"),
            "zip": ("answer", "plz-grundstueck-v3"),
            "city": ("answer", "ort-grundstueck"),
            "construction_costs": ("answer", "baukosten-in-chf"),
            "construction_duration": ("answer", "dauer-in-monaten"),
            "municipality": ("answer", "gemeinde", {"value_parser": "dynamic_option"}),
            "municipality_name": (
                "answer",
                "gemeinde",
                {"value_parser": "dynamic_option", "prop": "label"},
            ),
            "nature_risk": (
                "table",
                "beschreibung-der-prozessart-tabelle",
                {
                    "column_mapping": {
                        "risk_type": (
                            "prozessart",
                            {"value_parser": "option", "prop": "label"},
                        )
                    }
                },
            ),
            "plot_data": (
                "table",
                "parzelle",
                {
                    "column_mapping": {
                        "plot_number": "parzellennummer",
                        "egrid_number": "e-grid-nr",
                        "coord_east": "lagekoordinaten-ost",
                        "coord_north": "lagekoordinaten-nord",
                    }
                },
            ),
            "submit_date": ("case_meta", "submit-date", {"value_parser": "datetime"}),
            "paper_submit_date": (
                "case_meta",
                "paper-submit-date",
                {"value_parser": "datetime"},
            ),
            "decision_date": (
                "answer",
                "decision-date",
                {
                    "document_from_work_item": "decision",
                    "value_key": "date",
                },
            ),
            "publication_date": ("answer", "datum-publikation", {"value_key": "date"}),
            "construction_start_date": (
                "answer",
                [
                    "geplanter-baubeginn",  # regular dossiers
                    "datum-baubeginn",  # migrated dossiers
                ],
                {"value_key": "date"},
            ),
            "profile_approval_date": (
                "answer",
                "datum-schnurgeruestabnahme",
                {"value_key": "date"},
            ),
            "parking_lots": ("answer", "anzahl-abstellplaetze-fur-motorfahrzeuge"),
            "final_approval_date": (
                "answer",
                "datum-schlussabnahme",
                {"value_key": "date"},
            ),
            "completion_date": ("answer", "bauende", {"value_key": "date"}),
            "is_paper": (
                "answer",
                "is-paper",
                {
                    "value_parser": (
                        "value_mapping",
                        {"mapping": {"is-paper-yes": True, "is-paper-no": False}},
                    )
                },
            ),
            "number_of_accomodated_persons": (
                "answer",
                "bs-beherbergte-personen-mehr-50-v3",
            ),
            "lifts": (
                "table",
                "bs-aufzugsanlagen-v3",
                {
                    "column_mapping": {
                        "system_type": (
                            "bs-aufzugsanlage-typ-v3",
                            {"value_parser": "option"},
                        ),
                        "new_or_existing": (
                            "bs-aufzugsanlage-zustand-v3",
                            {"value_parser": "option"},
                        ),
                    }
                },
            ),
            "dimension_height": ("answer", "hoehe", {"value_parser": "option"}),
            "building_distances": (
                "table",
                "brandschutz-gebaeudeabstaende-v3",
                {
                    "column_mapping": {
                        "side": "bg-gebaeudeseite-v3",
                        "distance": "bg-abstand-v3",
                    }
                },
            ),
            "hazardous_substances": (
                "table",
                "bs-gefaehrliche-stoffe-v3",
                {
                    "column_mapping": {
                        "material": "bs-gefaehrlicher-stoff-lagerstoff-v3",
                        "material_group": (
                            "bs-gefaehrlicher-stoff-stoffgruppe-v3",
                            {"value_parser": "option"},
                        ),
                        "amount": "bs-gefaehrlicher-stoff-menge-v3",
                    }
                },
            ),
            "ventilation_systems": (
                "table",
                "bs-lufttechnische-anlagen-v3",
                {
                    "column_mapping": {
                        "system_type": (
                            "bs-lufttechnische-anlagen-typ-v3",
                            {"value_parser": "option"},
                        ),
                        "air_volume": "bs-lufttechnische-anlage-luftvolumenstrom-v3",
                        "new_or_existing": (
                            "bs-lufttechnische-anlage-zustand-v3",
                            {"value_parser": "option"},
                        ),
                    }
                },
            ),
            "rooms_with_more_than_50_persons": (
                "table",
                "bs-raeume-mehr-50-v3",
                {
                    "column_mapping": {
                        "room": "bs-raum-v3",
                        "number_of_persons": "bs-anzahl-personen-v3",
                    }
                },
            ),
            "room_occupancy_rooms_more_than_50_persons": (
                "answer",
                "bs-raumbelegung-mehr-50-v3",
            ),
            "solar_panels": (
                "table",
                "solaranlagen-v3",
                {
                    "column_mapping": {
                        "type": ("solaranlage-typ-v3", {"value_parser": "option"}),
                        "energy_storage": (
                            "solaranlage-elektrische-energiespeicherung-v3",
                            {"value_parser": "option"},
                        ),
                        "energy_storage_capacity": "solaranlage-energiespeicherkapazitaet-v3",
                        "new_or_existing": (
                            "solaranlage-zustand-v3",
                            {"value_parser": "option"},
                        ),
                    }
                },
            ),
            "stfv_short_report_date": (
                "answer",
                "sv-vollzug-kurzbericht-v3",
                {"value_key": "date"},
            ),
            "stfv_critial_value_exceeded": (
                "answer",
                "triagefrage-stoerfallvorsorge-v3",
                {"value_parser": "option"},
            ),
            "stfv_risk_assessment": (
                "answer",
                "sv-vollzug-risikoermittlung-v3",
                {"value_key": "date"},
            ),
            "fire_protection_systems": (
                "table",
                "bs-brandschutzanlagen-v3",
                {
                    "column_mapping": {
                        "type": (
                            "bs-brandschutzanlage-typ-v3",
                            {"value_parser": "option"},
                        ),
                        "new_or_existing": (
                            "bs-brandschutzanlage-zustand-v3",
                            {"value_parser": "option"},
                        ),
                    }
                },
            ),
            "heating_systems": (
                "table",
                "bs-waermetechnische-anlagen-v3",
                {
                    "column_mapping": {
                        "type": (
                            "bs-waermetechnische-anlagen-typ-v3",
                            {"value_parser": "option"},
                        ),
                        "power": "bs-waermetechnische-anlage-leistung-v3",
                        "combusitble_storage": (
                            "bs-waermetechnische-anlage-brennstofflagerung-v3",
                            {"value_parser": "option"},
                        ),
                        "storage_amount": "bs-waermetechnische-anlage-lagermenge-v3",
                        "new_or_existing": (
                            "bs-waermetechnische-anlage-zustand-v3",
                            {"value_parser": "option"},
                        ),
                    }
                },
            ),
            "floor_area": ("answer", "geschossflaeche-in-quadratmeter"),
            "qs_responsible": (
                "table",
                "qs-verantwortlicher-v3",
                {
                    "column_mapping": {
                        "is_juristic_person": (
                            "juristische-person-gesuchstellerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-gesuchstellerin-ja": True,
                                            "juristische-person-gesuchstellerin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-gesuchstellerin",
                        "last_name": "name-gesuchstellerin",
                        "first_name": "vorname-gesuchstellerin",
                        "street": "strasse-gesuchstellerin",
                        "street_number": "nummer-gesuchstellerin",
                        "zip": "plz-gesuchstellerin",
                        "town": "ort-gesuchstellerin",
                        "phone": "telefon-oder-mobile-gesuchstellerin",
                        "email": "e-mail-gesuchstellerin",
                        "stand_in": (
                            "vertreterin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "vertreterin-ja": True,
                                            "vertreterin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                    }
                },
            ),
        },
    },
    "kt_uri": {
        "ENABLED": True,
        "CONFIG": {
            "applicants": (
                "table",
                "applicant",
                {
                    "column_mapping": {
                        "last_name": "last-name",
                        "first_name": "first-name",
                        "street": "street",
                        "street_number": "street-number",
                        "zip": "zip",
                        "town": "city",
                        "country": "country",
                        "is_juristic_person": (
                            "is-juristic-person",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "is-juristic-person-no": False,
                                            "is-juristic-person-yes": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "juristic-person-name",
                    }
                },
            ),
            "proposal": (
                "answer",
                [
                    "proposal-description",
                    "beschreibung-zu-mbv",
                    "bezeichnung",
                    "vorhaben-proposal-description",
                    "veranstaltung-beschrieb",
                    "beschrieb-verfahren",
                ],
            ),
            "veranstaltung_art": (
                "answer",
                "veranstaltung-art",
            ),
            "leitbehoerde_internal_form": (
                "answer",
                "leitbehoerde-internal-form",
            ),
            "oereb_topic": (
                "answer",
                ["oereb-thema", "oereb-thema-gemeinde"],
            ),
            "legal_state": (
                "answer",
                "typ-des-verfahrens",
            ),
            "form_type": (
                "answer",
                "form-type",
            ),
            "authority": (
                "answer",
                "leitbehoerde",
                {"value_parser": "dynamic_option"},
            ),
            "plot_data": (
                "table",
                "parcels",
                {
                    "column_mapping": {
                        "plot_number": "parcel-number",
                        "egrid_number": "e-grid",
                        "coordinates_east": "coordinates-east",
                        "coordinates_north": "coordinates-north",
                        "origin_of_coordinates": ("default", {"default": 901}),
                    }
                },
            ),
            "street": ("answer", "parcel-street"),
            "street_number": ("answer", "parcel-street-number"),
            "city": ("answer", "parcel-city"),
            "dossier_number": ("case_meta", "dossier-number"),
            "municipality": (
                "answer",
                "municipality",
                {"value_parser": "dynamic_option"},
            ),
            "municipality_name": (
                "answer",
                "gemeinde",
                {"value_parser": "dynamic_option", "prop": "label"},
            ),
            "category": (
                "answer",
                "category",
                {
                    "value_parser": (
                        "value_mapping",
                        {
                            "mapping": {
                                "category-hochbaute": 6011,
                                "category-tiefbaute": 6010,
                            }
                        },
                    ),
                    "default": [],
                },
            ),
            "type_of_construction": (
                "table",
                "gebaeude",
                {
                    "column_mapping": {
                        "art_der_hochbaute": (
                            "art-der-hochbaute",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "art-der-hochbaute-einfamilienhaus": 6271,
                                            "art-der-hochbaute-doppeleinfamilienhaus": 6272,
                                            "art-der-hochbaute-mehrfamilienhaus": 6273,
                                            "art-der-hochbaute-wohn-und-geschaftshaus": 6274,
                                            "art-der-hochbaute-geschaftshaus": 6294,
                                            "art-der-hochbaute-garage-oder-carport": 6278,
                                            "art-der-hochbaute-parkhaus": 6235,
                                            "art-der-hochbaute-bauten-und-anlagen-gastgewerbe": 6295,
                                            "art-der-hochbaute-heim-mit-unterkunft": 6254,
                                            "art-der-hochbaute-wohnheim-ohne-pflege": 6276,
                                            "art-der-hochbaute-spital": 6253,
                                            "art-der-hochbaute-schulen": 6251,
                                            "art-der-hochbaute-sporthallen": 6259,
                                            "art-der-hochbaute-tourismusanlagen": 6256,
                                            "art-der-hochbaute-kirchen": 6257,
                                            "art-der-hochbaute-kulturbauten": 6258,
                                            "art-der-hochbaute-oekonomie-mit-tieren-mit-tieren": 6281,
                                            "art-der-hochbaute-oekonomiegebaude": 6281,
                                            "art-der-hochbaute-forstwirtschaft": 6282,
                                            "art-der-hochbaute-materiallager": 6292,
                                            "art-der-hochbaute-silo": 6292,
                                            "art-der-hochbaute-kommunikationsanlagen": 6245,
                                            "art-der-hochbaute-kehrichtentsorgungsanlagen": 6222,
                                            "art-der-hochbaute-andere": 6299,
                                            "art-der-hochbaute-energieholzlager": 6292,
                                            "art-der-hochbaute-industrie": 6299,
                                            "art-der-hochbaute-landwirtschaft-betrieb-wohnteil": 6281,
                                            "art-der-hochbaute-reklamebauten": 6299,
                                            "art-der-hochbaute-brennstofflager": 6292,
                                        }
                                    },
                                )
                            },
                        )
                    }
                },
            ),
            "construction_costs": ("answer", "construction-cost"),
            "submit_date": ("first_workflow_entry", [10, 12]),
            "decision_date": ("last_workflow_entry", [47]),
            "construction_start_date": (
                "first_workflow_entry",
                [55],
            ),
            "construction_end_date": (
                "last_workflow_entry",
                [67],
            ),
            "approval_reason": ("php_answer", 264, {"default": 5000}),
            "type_of_applicant": ("php_answer", 267),
            "energy_devices": (
                "table",
                "haustechnik-tabelle",
                {
                    "column_mapping": {
                        "name_of_building": "gehoert-zu-gebaeudenummer",
                        "type": "anlagetyp",
                        "information_source": (
                            "default",
                            {"default": 869},
                        ),  # Gemäss Baubewilligung
                        "is_heating": (
                            "anlagetyp",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "anlagetyp-analgetyp-klima": False,
                                            "anlagetyp-aufzuege": False,
                                            "anlagetyp-betankungsanlage": False,
                                            "anlagetyp-lueftungsanlage": False,
                                            "anlagetyp-notstrom-aggregat": False,
                                            "anlagetyp-photovoltaische-solaranlage": False,
                                            "anlagetyp-tankanlagen": False,
                                            "anlagetyp-thermische-solaranlage": False,
                                            "anlagetyp-warmwasser": False,
                                            "anlagetyp-hauptheizung": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "is_warm_water": (
                            "anlagetyp",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "anlagetyp-analgetyp-klima": False,
                                            "anlagetyp-aufzuege": False,
                                            "anlagetyp-betankungsanlage": False,
                                            "anlagetyp-lueftungsanlage": False,
                                            "anlagetyp-notstrom-aggregat": False,
                                            "anlagetyp-photovoltaische-solaranlage": False,
                                            "anlagetyp-tankanlagen": False,
                                            "anlagetyp-thermische-solaranlage": False,
                                            "anlagetyp-warmwasser": True,
                                            "anlagetyp-hauptheizung": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "is_main_heating": (
                            "heizsystem-art",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "-hauptheizung": True,
                                            "-zusatzheizung": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "energy_source": (
                            "hauptheizungsanlage",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "hauptheizungsanlage-abwaerme": 7550,
                                            "hauptheizungsanlage-andere": 7599,
                                            "hauptheizungsanlage-elektrizitaet": 7560,
                                            "hauptheizungsanlage-erdsonde": 7511,
                                            "hauptheizungsanlage-erdwaerme": 7510,
                                            "hauptheizungsanlage-erdwaermesonde": 7511,
                                            "hauptheizungsanlage-fernwaerme": 7580,
                                            "hauptheizungsanlage-gas": 7520,
                                            "hauptheizungsanlage-grundwasserwaermepumpe": 7513,
                                            "hauptheizungsanlage-heizoel": 7530,
                                            "hauptheizungsanlage-holz": 7540,
                                            "hauptheizungsanlage-holzschnitzel-pellets": 7542,
                                            "hauptheizungsanlage-kachelofen-schwedenofen": 7550,
                                            "hauptheizungsanlage-luftwaermepumpe": 7501,
                                            "hauptheizungsanlage-sonne-thermisch": 7570,
                                            "hauptheizungsanlage-stueckholz": 7541,
                                            "hauptheizungsanlage-unbestimmt": 7598,
                                        }
                                    },
                                )
                            },
                        ),
                    },
                },
            ),
            "buildings": (
                "table",
                "gebaeude",
                {
                    "column_mapping": {
                        "name": "gebaeudenummer-bezeichnung",
                        "proposal": (
                            "proposal",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "proposal-neubau": 6001,
                                            "proposal-umbau-erneuerung-sanierung": 6002,
                                            "proposal-abbruch-rueckbau": 6007,
                                        }
                                    },
                                ),
                                "default": [],
                            },
                        ),
                        "building_category": (
                            "gebaeudekategorie",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "gebaeudekategorie-andere": 1030,
                                            "gebaeudekategorie-ausschliessliche-wohnnutzung": 1020,
                                            "gebaeudekategorie-ohne-wohnnutzung": 1060,
                                            "gebaeudekategorie-provisorische-unterkunft": 1010,
                                            "gebaeudekategorie-sonderbau": 1080,
                                            "gebaeudekategorie-teilweise-wohnnutzung": 1040,
                                        }
                                    },
                                )
                            },
                        ),
                    }
                },
            ),
            "dwellings": (
                "table",
                "wohnungen",
                {
                    "column_mapping": {
                        "name_of_building": "zugehoerigkeit",
                        "floor_type": (
                            "stockwerktyp",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "stockwerktyp-obergeschoss": 3101,
                                            "stockwerktyp-untergeschoss": 3401,
                                            "stockwerktyp-parterre": 3100,
                                        }
                                    },
                                )
                            },
                        ),
                        "floor_number": "stockwerknummer",
                        "location_on_floor": "lage",
                        "number_of_rooms": "wohnungsgroesse",
                        "kitchen_facilities": "kocheinrichtung",
                        "has_kitchen_facilities": (
                            "kocheinrichtung",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "kocheinrichtung-keine-kocheinrichtung": False,
                                            "kocheinrichtung-kochnische-greater-4-m2": True,
                                            "kocheinrichtung-kueche-less-4-m2": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "area": "flaeche-in-m2",
                        "multiple_floors": (
                            "mehrgeschossige-wohnung",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "mehrgeschossige-wohnung-ja": True,
                                            "mehrgeschossige-wohnung-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "usage_limitation": (
                            "zwg",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "zwg-keine": 3401,
                                            "zwg-erstwohnung": 3402,
                                            "zwg-touristisch-a": 3403,
                                            "zwg-touristisch-b": 3404,
                                        }
                                    },
                                )
                            },
                        ),
                    }
                },
            ),
        },
    },
    "demo": {
        "ENABLED": True,
        "CONFIG": {
            "applicants": (
                "table",
                "personalien-gesuchstellerin",
                {
                    "column_mapping": {
                        "last_name": "name-gesuchstellerin",
                        "first_name": "vorname-gesuchstellerin",
                        "street": "strasse-gesuchstellerin",
                        "street_number": "nummer-gesuchstellerin",
                        "zip": "plz-gesuchstellerin",
                        "town": "ort-gesuchstellerin",
                        "is_juristic_person": (
                            "juristische-person-gesuchstellerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-gesuchstellerin-ja": True,
                                            "juristische-person-gesuchstellerin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-gesuchstellerin",
                    }
                },
            ),
            "building_owners": (
                "table",
                "personalien-gebaudeeigentumerin",
                {
                    "column_mapping": {
                        "last_name": "name-gebaeudeeigentuemerin",
                        "first_name": "vorname-gebaeudeeigentuemerin",
                        "street": "strasse-gebaeudeeigentuemerin",
                        "street_number": "nummer-gebaeudeeigentuemerin",
                        "zip": "plz-gebaeudeeigentuemerin",
                        "town": "ort-gebaeudeeigentuemerin",
                        "is_juristic_person": (
                            "juristische-person-gebaeudeeigentuemerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-gebaeudeeigentuemer-ja": True,
                                            "juristische-person-gebaeudeeigentuemer-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-gebaeudeeigentuemerin",
                    }
                },
            ),
            "landowners": (
                "table",
                "personalien-grundeigentumerin",
                {
                    "column_mapping": {
                        "last_name": "name-grundeigentuemerin",
                        "first_name": "vorname-grundeigentuemerin",
                        "street": "strasse-grundeigentuemerin",
                        "street_number": "nummer-grundeigentuemerin",
                        "zip": "plz-grundeigentuemerin",
                        "town": "ort-grundeigentuemerin",
                        "is_juristic_person": (
                            "juristische-person-grundeigentuemerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-grundeigentuemerin-ja": True,
                                            "juristische-person-grundeigentuemerin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-grundeigentuemerin",
                    }
                },
            ),
            "project_authors": (
                "table",
                "personalien-projektverfasserin",
                {
                    "column_mapping": {
                        "last_name": "name-projektverfasserin",
                        "first_name": "vorname-projektverfasserin",
                        "street": "strasse-projektverfasserin",
                        "street_number": "nummer-projektverfasserin",
                        "zip": "plz-projektverfasserin",
                        "town": "ort-projektverfasserin",
                        "is_juristic_person": (
                            "juristische-person-projektverfasserin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-projektverfasserin-ja": True,
                                            "juristische-person-projektverfasserin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-projektverfasserin",
                    }
                },
            ),
            "legal_representatives": (
                "table",
                "personalien-vertreterin-mit-vollmacht",
                {
                    "column_mapping": {
                        "last_name": "name-vertreterin",
                        "first_name": "vorname-vertreterin",
                        "street": "strasse-vertreterin",
                        "street_number": "nummer-vertreterin",
                        "zip": "plz-vertreterin",
                        "town": "ort-vertreterin",
                        "is_juristic_person": (
                            "juristische-person-vertreterin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-vertreterin-ja": True,
                                            "juristische-person-vertreterin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-vertreterin",
                    }
                },
            ),
            "dossier_number": ("case_meta", "ebau-number"),
            "project": ("answer", "baubeschrieb", {"value_parser": "option"}),
            "proposal": ("answer", "beschreibung-bauvorhaben"),
            "street": ("answer", "strasse-flurname"),
            "street_number": ("answer", "nr"),
            "city": ("answer", "ort-grundstueck"),
            "construction_costs": ("answer", "baukosten-in-chf"),
            "municipality": ("answer", "gemeinde", {"value_parser": "dynamic_option"}),
            "municipality_name": (
                "answer",
                "gemeinde",
                {"value_parser": "dynamic_option", "prop": "label"},
            ),
            "plot_data": (
                "table",
                "parzelle",
                {
                    "column_mapping": {
                        "plot_number": "parzellennummer",
                        "egrid_number": "e-grid-nr",
                        "coord_east": "lagekoordinaten-ost",
                        "coord_north": "lagekoordinaten-nord",
                    }
                },
            ),
            "submit_date": ("case_meta", "submit-date", {"value_parser": "datetime"}),
            "paper_submit_date": (
                "case_meta",
                "paper-submit-date",
                {"value_parser": "datetime"},
            ),
            "is_paper": (
                "answer",
                "is-paper",
                {
                    "value_parser": (
                        "value_mapping",
                        {"mapping": {"is-paper-yes": True, "is-paper-no": False}},
                    )
                },
            ),
        },
    },
    "kt_gr": {
        "ENABLED": True,
        "CONFIG": {
            "applicants": (
                "table",
                "personalien-gesuchstellerin",
                {
                    "column_mapping": {
                        "last_name": "name-gesuchstellerin",
                        "first_name": "vorname-gesuchstellerin",
                        "street": "strasse-gesuchstellerin",
                        "street_number": "nummer-gesuchstellerin",
                        "zip": "plz-gesuchstellerin",
                        "town": "ort-gesuchstellerin",
                        "email": "e-mail-gesuchstellerin",
                        "tel": "telefon-oder-mobile-gesuchstellerin",
                        "is_juristic_person": (
                            "juristische-person-gesuchstellerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-gesuchstellerin-ja": True,
                                            "juristische-person-gesuchstellerin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-gesuchstellerin",
                    }
                },
            ),
            "building_owners": (
                "table",
                "personalien-gebaudeeigentumerin",
                {
                    "column_mapping": {
                        "last_name": "name-gesuchstellerin",
                        "first_name": "vorname-gesuchstellerin",
                        "street": "strasse-gesuchstellerin",
                        "street_number": "nummer-gesuchstellerin",
                        "zip": "plz-gesuchstellerin",
                        "town": "ort-gesuchstellerin",
                        "email": "e-mail-gesuchstellerin",
                        "tel": "telefon-oder-mobile-gesuchstellerin",
                        "is_juristic_person": (
                            "juristische-person-gesuchstellerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-gesuchstellerin-ja": True,
                                            "juristische-person-gesuchstellerin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-gesuchstellerin",
                    }
                },
            ),
            "landowners": (
                "table",
                "personalien-grundeigentumerin",
                {
                    "column_mapping": {
                        "last_name": "name-gesuchstellerin",
                        "first_name": "vorname-gesuchstellerin",
                        "street": "strasse-gesuchstellerin",
                        "street_number": "nummer-gesuchstellerin",
                        "zip": "plz-gesuchstellerin",
                        "town": "ort-gesuchstellerin",
                        "email": "e-mail-gesuchstellerin",
                        "tel": "telefon-oder-mobile-gesuchstellerin",
                        "is_juristic_person": (
                            "juristische-person-gesuchstellerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-gesuchstellerin-ja": True,
                                            "juristische-person-gesuchstellerin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-gesuchstellerin",
                    }
                },
            ),
            "project_authors": (
                "table",
                "personalien-projektverfasserin",
                {
                    "column_mapping": {
                        "last_name": "name-gesuchstellerin",
                        "first_name": "vorname-gesuchstellerin",
                        "street": "strasse-gesuchstellerin",
                        "street_number": "nummer-gesuchstellerin",
                        "zip": "plz-gesuchstellerin",
                        "town": "ort-gesuchstellerin",
                        "email": "e-mail-gesuchstellerin",
                        "tel": "telefon-oder-mobile-gesuchstellerin",
                        "is_juristic_person": (
                            "juristische-person-gesuchstellerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-gesuchstellerin-ja": True,
                                            "juristische-person-gesuchstellerin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-gesuchstellerin",
                    }
                },
            ),
            "legal_representatives": (
                "table",
                "personalien-vertreterin-mit-vollmacht",
                {
                    "column_mapping": {
                        "last_name": "name-gesuchstellerin",
                        "first_name": "vorname-gesuchstellerin",
                        "street": "strasse-gesuchstellerin",
                        "street_number": "nummer-gesuchstellerin",
                        "zip": "plz-gesuchstellerin",
                        "town": "ort-gesuchstellerin",
                        "email": "e-mail-gesuchstellerin",
                        "tel": "telefon-oder-mobile-gesuchstellerin",
                        "is_juristic_person": (
                            "juristische-person-gesuchstellerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-gesuchstellerin-ja": True,
                                            "juristische-person-gesuchstellerin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-gesuchstellerin",
                    }
                },
            ),
            "dossier_number": ("case_meta", "dossier-number"),
            "project": ("answer", "baubeschrieb", {"value_parser": "option"}),
            "proposal": ("answer", "beschreibung-bauvorhaben"),
            "street": ("answer", "street-and-housenumber"),
            "street_number": ("answer", "nr"),  # unused
            "zip": ("answer", "plz"),
            "city": ("answer", "ort-grundstueck"),
            "construction_costs": ("answer", "baukosten"),
            "municipality": ("answer", "gemeinde", {"value_parser": "dynamic_option"}),
            "municipality_name": (
                "answer",
                "gemeinde",
                {"value_parser": "dynamic_option", "prop": "label"},
            ),
            "plot_data": (
                "table",
                "parzelle",
                {
                    "column_mapping": {
                        "plot_number": "parzellennummer",
                        "egrid_number": "e-grid-nr",
                    }
                },
            ),
            "submit_date": ("case_meta", "submit-date", {"value_parser": "datetime"}),
            "paper_submit_date": (
                "case_meta",
                "paper-submit-date",
                {"value_parser": "datetime"},
            ),
            "is_paper": (
                "answer",
                "is-paper",
                {
                    "value_parser": (
                        "value_mapping",
                        {"mapping": {"is-paper-yes": True, "is-paper-no": False}},
                    )
                },
            ),
            "description_modification": ("answer", "beschreibung-projektaenderung"),
            "decision_date": (
                "answer",
                "decision-date",
                {
                    "document_from_work_item": "decision",
                    "value_key": "date",
                },
            ),
            "buildings": (
                "table",
                "gebaeude-und-anlagen",
                {
                    "column_mapping": {
                        "insurance_number": "amtliche-gebaeudenummer",
                        "heating_heat_generator": (
                            "waermeerzeuger-heizung",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "waermeerzeuger-heizung-7400": 7400,
                                            "waermeerzeuger-heizung-7410": 7410,
                                            "waermeerzeuger-heizung-7411": 7411,
                                            "waermeerzeuger-heizung-7420": 7420,
                                            "waermeerzeuger-heizung-7421": 7421,
                                            "waermeerzeuger-heizung-7430": 7430,
                                            "waermeerzeuger-heizung-7431": 7431,
                                            "waermeerzeuger-heizung-7432": 7432,
                                            "waermeerzeuger-heizung-7433": 7433,
                                            "waermeerzeuger-heizung-7434": 7434,
                                            "waermeerzeuger-heizung-7435": 7435,
                                            "waermeerzeuger-heizung-7436": 7436,
                                            "waermeerzeuger-heizung-7440": 7440,
                                            "waermeerzeuger-heizung-7441": 7441,
                                            "waermeerzeuger-heizung-7450": 7450,
                                            "waermeerzeuger-heizung-7451": 7451,
                                            "waermeerzeuger-heizung-7452": 7452,
                                            "waermeerzeuger-heizung-7460": 7460,
                                            "waermeerzeuger-heizung-7461": 7461,
                                            "waermeerzeuger-heizung-7499": 7499,
                                            "waermeerzeuger-heizung-noch-nicht-festgelegt": None,
                                        }
                                    },
                                )
                            },
                        ),
                        "additional_heating_heat_generator": (
                            "weitere-waermeerzeuger-heizung",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "weitere-waermeerzeuger-heizung-7400": 7400,
                                            "weitere-waermeerzeuger-heizung-7410": 7410,
                                            "weitere-waermeerzeuger-heizung-7411": 7411,
                                            "weitere-waermeerzeuger-heizung-7420": 7420,
                                            "weitere-waermeerzeuger-heizung-7421": 7421,
                                            "weitere-waermeerzeuger-heizung-7430": 7430,
                                            "weitere-waermeerzeuger-heizung-7431": 7431,
                                            "weitere-waermeerzeuger-heizung-7432": 7432,
                                            "weitere-waermeerzeuger-heizung-7433": 7433,
                                            "weitere-waermeerzeuger-heizung-7434": 7434,
                                            "weitere-waermeerzeuger-heizung-7435": 7435,
                                            "weitere-waermeerzeuger-heizung-7436": 7436,
                                            "weitere-waermeerzeuger-heizung-7440": 7440,
                                            "weitere-waermeerzeuger-heizung-7441": 7441,
                                            "weitere-waermeerzeuger-heizung-7450": 7450,
                                            "weitere-waermeerzeuger-heizung-7451": 7451,
                                            "weitere-waermeerzeuger-heizung-7452": 7452,
                                            "weitere-waermeerzeuger-heizung-7460": 7460,
                                            "weitere-waermeerzeuger-heizung-7461": 7461,
                                            "weitere-waermeerzeuger-heizung-7499": 7499,
                                            "weitere-waermeerzeuger-heizung-noch-nicht-festgelegt": None,
                                        }
                                    },
                                )
                            },
                        ),
                        "heating_energy_source": (
                            "energie-waermequelle-heizung",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "energie-waermequelle-heizung-7500": 7500,
                                            "energie-waermequelle-heizung-7501": 7501,
                                            "energie-waermequelle-heizung-7510": 7510,
                                            "energie-waermequelle-heizung-7511": 7511,
                                            "energie-waermequelle-heizung-7512": 7512,
                                            "energie-waermequelle-heizung-7513": 7513,
                                            "energie-waermequelle-heizung-7520": 7520,
                                            "energie-waermequelle-heizung-7530": 7530,
                                            "energie-waermequelle-heizung-7540": 7540,
                                            "energie-waermequelle-heizung-7541": 7541,
                                            "energie-waermequelle-heizung-7542": 7542,
                                            "energie-waermequelle-heizung-7550": 7550,
                                            "energie-waermequelle-heizung-7560": 7560,
                                            "energie-waermequelle-heizung-7570": 7570,
                                            "energie-waermequelle-heizung-7580": 7580,
                                            "energie-waermequelle-heizung-7581": 7581,
                                            "energie-waermequelle-heizung-7582": 7582,
                                            "energie-waermequelle-heizung-7598": 7598,
                                            "energie-waermequelle-heizung-7599": 7599,
                                            "energie-waermequelle-heizung-noch-nicht-festgelegt": None,
                                        }
                                    },
                                )
                            },
                        ),
                        "additional_heating_energy_source": (
                            "weitere-energie-waermequelle-heizung",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "weitere-energie-waermequelle-heizung-7500": 7500,
                                            "weitere-energie-waermequelle-heizung-7501": 7501,
                                            "weitere-energie-waermequelle-heizung-7510": 7510,
                                            "weitere-energie-waermequelle-heizung-7511": 7511,
                                            "weitere-energie-waermequelle-heizung-7512": 7512,
                                            "weitere-energie-waermequelle-heizung-7513": 7513,
                                            "weitere-energie-waermequelle-heizung-7520": 7520,
                                            "weitere-energie-waermequelle-heizung-7530": 7530,
                                            "weitere-energie-waermequelle-heizung-7540": 7540,
                                            "weitere-energie-waermequelle-heizung-7541": 7541,
                                            "weitere-energie-waermequelle-heizung-7542": 7542,
                                            "weitere-energie-waermequelle-heizung-7550": 7550,
                                            "weitere-energie-waermequelle-heizung-7560": 7560,
                                            "weitere-energie-waermequelle-heizung-7570": 7570,
                                            "weitere-energie-waermequelle-heizung-7580": 7580,
                                            "weitere-energie-waermequelle-heizung-7581": 7581,
                                            "weitere-energie-waermequelle-heizung-7582": 7582,
                                            "weitere-energie-waermequelle-heizung-7598": 7598,
                                            "weitere-energie-waermequelle-heizung-7599": 7599,
                                            "weitere-energie-waermequelle-heizung-noch-nicht-festgelegt": None,
                                        }
                                    },
                                )
                            },
                        ),
                        "warmwater_heat_generator": (
                            "waermeerzeuger-warmwasser",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "waermeerzeuger-warmwasser-7600": 7600,
                                            "waermeerzeuger-warmwasser-7610": 7610,
                                            "waermeerzeuger-warmwasser-7620": 7620,
                                            "waermeerzeuger-warmwasser-7630": 7630,
                                            "waermeerzeuger-warmwasser-7632": 7632,
                                            "waermeerzeuger-warmwasser-7634": 7634,
                                            "waermeerzeuger-warmwasser-7640": 7640,
                                            "waermeerzeuger-warmwasser-7650": 7650,
                                            "waermeerzeuger-warmwasser-7651": 7651,
                                            "waermeerzeuger-warmwasser-7660": 7660,
                                            "waermeerzeuger-warmwasser-7699": 7699,
                                        }
                                    },
                                )
                            },
                        ),
                        "additional_warmwater_heat_generator": (
                            "weitere-waermeerzeuger-warmwasser",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "weitere-waermeerzeuger-warmwasser-7600": 7600,
                                            "weitere-waermeerzeuger-warmwasser-7610": 7610,
                                            "weitere-waermeerzeuger-warmwasser-7620": 7620,
                                            "weitere-waermeerzeuger-warmwasser-7630": 7630,
                                            "weitere-waermeerzeuger-warmwasser-7632": 7632,
                                            "weitere-waermeerzeuger-warmwasser-7634": 7634,
                                            "weitere-waermeerzeuger-warmwasser-7640": 7640,
                                            "weitere-waermeerzeuger-warmwasser-7650": 7650,
                                            "weitere-waermeerzeuger-warmwasser-7651": 7651,
                                            "weitere-waermeerzeuger-warmwasser-7660": 7660,
                                            "weitere-waermeerzeuger-warmwasser-7699": 7699,
                                        }
                                    },
                                )
                            },
                        ),
                        "warmwater_energy_source": (
                            "energie-waermequelle-warmwasser",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "energie-waermequelle-warmwasser-7500": 7500,
                                            "energie-waermequelle-warmwasser-7501": 7501,
                                            "energie-waermequelle-warmwasser-7510": 7510,
                                            "energie-waermequelle-warmwasser-7511": 7511,
                                            "energie-waermequelle-warmwasser-7512": 7512,
                                            "energie-waermequelle-warmwasser-7513": 7513,
                                            "energie-waermequelle-warmwasser-7520": 7520,
                                            "energie-waermequelle-warmwasser-7530": 7530,
                                            "energie-waermequelle-warmwasser-7540": 7540,
                                            "energie-waermequelle-warmwasser-7541": 7541,
                                            "energie-waermequelle-warmwasser-7550": 7550,
                                            "energie-waermequelle-warmwasser-7560": 7560,
                                            "energie-waermequelle-warmwasser-7570": 7570,
                                            "energie-waermequelle-warmwasser-7580": 7580,
                                            "energie-waermequelle-warmwasser-7581": 7581,
                                            "energie-waermequelle-warmwasser-7582": 7582,
                                            "energie-waermequelle-warmwasser-7598": 7598,
                                            "energie-waermequelle-warmwasser-7599": 7599,
                                            "energie-waermequelle-warmwasser-noch-nicht-festgelegt": None,
                                        }
                                    },
                                )
                            },
                        ),
                        "additional_warmwater_energy_source": (
                            "weitere-energie-waermequelle-warmwasser",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "weitere-energie-waermequelle-warmwasser-7500": 7500,
                                            "weitere-energie-waermequelle-warmwasser-7501": 7501,
                                            "weitere-energie-waermequelle-warmwasser-7510": 7510,
                                            "weitere-energie-waermequelle-warmwasser-7511": 7511,
                                            "weitere-energie-waermequelle-warmwasser-7512": 7512,
                                            "weitere-energie-waermequelle-warmwasser-7513": 7513,
                                            "weitere-energie-waermequelle-warmwasser-7520": 7520,
                                            "weitere-energie-waermequelle-warmwasser-7530": 7530,
                                            "weitere-energie-waermequelle-warmwasser-7540": 7540,
                                            "weitere-energie-waermequelle-warmwasser-7541": 7541,
                                            "weitere-energie-waermequelle-warmwasser-7550": 7550,
                                            "weitere-energie-waermequelle-warmwasser-7560": 7560,
                                            "weitere-energie-waermequelle-warmwasser-7570": 7570,
                                            "weitere-energie-waermequelle-warmwasser-7580": 7580,
                                            "weitere-energie-waermequelle-warmwasser-7581": 7581,
                                            "weitere-energie-waermequelle-warmwasser-7582": 7582,
                                            "weitere-energie-waermequelle-warmwasser-7598": 7598,
                                            "weitere-energie-waermequelle-warmwasser-7599": 7599,
                                            "weitere-energie-waermequelle-warmwasser-noch-nicht-festgelegt": None,
                                        }
                                    },
                                )
                            },
                        ),
                    },
                },
            ),
        },
    },
    "kt_so": {
        "ENABLED": True,
        "CONFIG": {
            "applicants": (
                "table",
                "bauherrin",
                {"column_mapping": SO_PERSONAL_DATA_MAPPING},
            ),
            "landowners": (
                "table",
                "grundeigentuemerin",
                {"column_mapping": SO_PERSONAL_DATA_MAPPING},
            ),
            "project_authors": (
                "table",
                "projektverfasserin",
                {"column_mapping": SO_PERSONAL_DATA_MAPPING},
            ),
            "proposal": ("answer", "umschreibung-bauprojekt"),
            "street": ("answer", "strasse-flurname"),
            "street_number": ("answer", "strasse-nummer"),
            "zip": ("answer", "plz"),
            "city": ("answer", "ort"),
            "construction_costs": ("answer", "gesamtkosten"),
            "municipality": ("answer", "gemeinde", {"value_parser": "dynamic_option"}),
            "municipality_name": (
                "answer",
                "gemeinde",
                {"value_parser": "dynamic_option", "prop": "label"},
            ),
            "dossier_number": ("case_meta", "dossier-number"),
            "plot_data": (
                "table",
                "parzellen",
                {
                    "column_mapping": {
                        "plot_number": "parzellennummer",
                        "egrid_number": "e-grid",
                        "coord_east": "lagekoordinaten-ost",
                        "coord_north": "lagekoordinaten-nord",
                    }
                },
            ),
            "submit_date": ("case_meta", "submit-date", {"value_parser": "datetime"}),
            "is_paper": (
                "answer",
                "is-paper",
                {
                    "value_parser": (
                        "value_mapping",
                        {"mapping": {"is-paper-yes": True, "is-paper-no": False}},
                    )
                },
            ),
            "land_use_planning_land_use": ("answer", "nutzungsplanung-grundnutzung"),
        },
    },
}
