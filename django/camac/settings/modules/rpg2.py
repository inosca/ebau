from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.rpg2_schema import RPG2Config

RPG2 = ModuleConfig[RPG2Config](
    default=RPG2Config(),
    kt_bern=RPG2Config(
        enabled=False,  # TODO: Enable
        service_slugs=["agr-bauen", "agr-kantonsplanung"],
        allowed_forms=["baugesuch", "baugesuch-generell", "baugesuch-mit-uvp"],
    ),
    kt_ag=RPG2Config(
        enabled=False,  # TODO: Enable
        service_slugs=["afb"],
        allowed_forms=[
            "baugesuch",
            "baugesuch-mit-uvp",
            "vorentscheid",
            "plangenehmigungsverfahren-gas",
            "plangenehmigungsverfahren-bund",
            "anfrage-intern",
        ],
    ),
)
