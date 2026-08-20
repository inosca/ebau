from camac.permissions.conditions import Always, RequireInstanceState

from .conditions import HasAdditionalDemand

INTERNAL_PERMISSIONS = [
    ("intern:create", Always()),
    ("intern:update", Always()),
    ("intern:tag", Always()),
    ("intern:move", Always()),
    ("intern:replace", Always()),
    ("intern:delete", Always()),
    ("intern-mit-unterfachstellen:create", Always()),
    ("intern-mit-unterfachstellen:update", Always()),
    ("intern-mit-unterfachstellen:tag", Always()),
    ("intern-mit-unterfachstellen:move", Always()),
    ("intern-mit-unterfachstellen:replace", Always()),
    ("intern-mit-unterfachstellen:delete", Always()),
]

SG_PERMISSIONS_ALEXANDRIA = {
    "ENABLED": True,
    "ACCESS_LEVELS": {
        "applicant": [
            ("beilagen-zum-gesuch:create", RequireInstanceState(["new"])),
            ("beilagen-zum-gesuch:delete", RequireInstanceState(["new"])),
            ("nachforderung:create", HasAdditionalDemand()),
            ("nachforderung:delete", HasAdditionalDemand()),
        ],
        "lead-authority": [
            ("abnahme:all", Always()),
            ("baubegleitung:all", Always()),
            ("beilagen-zum-gesuch:all", Always()),
            ("beteiligte-behoerden:all", Always()),
            ("einsprachen-rechtsmittel:all", Always()),
            ("migrierte-dokumente:all", Always()),
            ("nachforderung:all", Always()),
            *INTERNAL_PERMISSIONS,
        ],
        "distribution-service": [
            ("abnahme:all", Always()),
            ("baubegleitung:all", Always()),
            ("beilagen-zum-gesuch:all", Always()),
            ("beteiligte-behoerden:all", Always()),
            ("einsprachen-rechtsmittel:all", Always()),
            ("migrierte-dokumente:all", Always()),
            ("nachforderung:all", Always()),
            *INTERNAL_PERMISSIONS,
        ],
        "support": [
            ("abnahme:all", Always()),
            ("baubegleitung:all", Always()),
            ("beilagen-zum-gesuch:all", Always()),
            ("beteiligte-behoerden:all", Always()),
            ("einsprachen-rechtsmittel:all", Always()),
            ("intern:all", Always()),
            ("intern-mit-unterfachstellen:all", Always()),
            ("migrierte-dokumente:all", Always()),
            ("nachforderung:all", Always()),
        ],
    },
}
