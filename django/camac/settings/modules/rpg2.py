from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.rpg2_schema import RPG2Config

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
    ),
)
