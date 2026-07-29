from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.rpg2_schema import ImportMappingEntry, RPG2Config

RPG2 = ModuleConfig[RPG2Config](
    default=RPG2Config(),
    kt_bern=RPG2Config(
        enabled=True,
        service_slugs=["agr-bauen"],
        allowed_forms=[
            "baugesuch",
            "baugesuch-generell",
            "baugesuch-mit-uvp",
            "verlaengerung-geltungsdauer",
            "vorabklaerung-vollstaendig",
        ],
        import_mapping={
            "rpg2-versiegelt-oder-entsiegelt": ImportMappingEntry(
                source_slugs=["versiegelt-oder-entsiegelt-v7"],
                is_option_target=True,
            ),
            "rpg2-versiegelte-entsiegelte-flaechen": ImportMappingEntry(
                source_slugs=["versiegelte-entsiegelte-flaechen-v7"],
                row_mapping={
                    "rpg2-art-versiegelung-entsiegelung": ImportMappingEntry(
                        source_slugs=["art-versiegelung-entsiegelung-v7"],
                        is_option_target=True,
                    ),
                    "rpg2-flaeche-quadrat-meter": ImportMappingEntry(
                        source_slugs=["flaeche-quadrat-meter-v7"],
                    ),
                },
            ),
        },
    ),
    kt_ag=RPG2Config(
        enabled=True,
        service_slugs=["afb"],
        allowed_forms=[
            "baugesuch",
            "baugesuch-migration",
            "baugesuch-mit-uvp",
            "uvp-migration",
            "vorentscheid",
            "vorentscheid-migration",
            "plangenehmigungsverfahren-gas",
            "plangenehmigungsverfahren-bund",
            "pgv-migration",
            "anfrage-intern",
            "importiertes-dossier",
        ],
        import_mapping={
            "rpg2-bewilligungsgrund": ImportMappingEntry(
                source_slugs=["kantonale-pruefung-gesuchscodes"],
                from_work_item="cantonal-exam",
                is_option_target=True,
                transform="first_choice_from_multiple",
            ),
            "rpg2-anzahl-neue-gebaeude": ImportMappingEntry(
                source_slugs=["anzahl-neue-gebaeude-greater-6m"],
            ),
            "rpg2-anzahl-gebaeude-abbruch": ImportMappingEntry(
                source_slugs=["anzahl-gebaeude-greater-6-m-die-abgebrochen-werden"],
            ),
            "rpg2-gebaeude-bemerkungen": ImportMappingEntry(
                source_slugs=["bemerkungsfeld"],
            ),
            "rpg2-versiegelt-oder-entsiegelt": ImportMappingEntry(
                source_slugs=["werden-flaechen-neu-versiegelt-oder-entsiegelt"],
                is_option_target=True,
            ),
            "rpg2-versiegelte-entsiegelte-flaechen": ImportMappingEntry(
                source_slugs=["versiegelte-entsiegelte-flaechen"],
                row_mapping={
                    "rpg2-art-versiegelung-entsiegelung": ImportMappingEntry(
                        source_slugs=["art-der-ver-bzw-entsiegelung"],
                        is_option_target=True,
                    ),
                    "rpg2-materialisierung-neu-versiegelten-flaechen": ImportMappingEntry(
                        source_slugs=["materialisierung-der-neu-versiegelten-flaechen"],
                        is_option_target=True,
                    ),
                    "rpg2-materialisierung-neu-versiegelten-flaechen-beschreibung": ImportMappingEntry(
                        source_slugs=["beschreibung-versiegelte-flaeche"],
                    ),
                    "rpg2-nutzung-versiegelten-flaechen": ImportMappingEntry(
                        source_slugs=["nutzung-der-versiegelten-flaeche"],
                        is_option_target=True,
                    ),
                    "rpg2-nutzung-versiegelten-flaechen-beschreibung": ImportMappingEntry(
                        source_slugs=["beschreibung-versiegelte-flaeche-andere"],
                    ),
                    "rpg2-wann-wurde-flaeche-versiegelt": ImportMappingEntry(
                        source_slugs=["wann-wurde-die-flaeche-versiegelt"],
                        is_option_target=True,
                    ),
                    "rpg2-flaeche-quadrat-meter": ImportMappingEntry(
                        source_slugs=["flaeche-m-versiegelt"],
                    ),
                },
            ),
        },
    ),
)
