from camac.permissions.conditions import Always, RequireInstanceState

INTERNAL_PERMISSIONS = [
    ("intern:create", Always()),
    ("intern:update", Always()),
    ("intern:tag", Always()),
    ("intern:move", Always()),
    ("intern:replace", Always()),
    ("intern:delete", Always()),
]

SG_PERMISSIONS_ALEXANDRIA = {
    "ENABLED": True,
    "ACCESS_LEVELS": {
        "applicant": [
            ("beilagen-zum-gesuch:create", RequireInstanceState(["new"])),
            ("beilagen-zum-gesuch:delete", RequireInstanceState(["new"])),
        ],
        "lead-authority": [
            ("beilagen-zum-gesuch:all", Always()),
            ("nachforderungen:all", Always()),
            ("alle-beteiligten:all", Always()),
            ("beteiligte-behoerden:all", Always()),
            *INTERNAL_PERMISSIONS,
        ],
        "distribution-service": [
            *INTERNAL_PERMISSIONS,
        ],
        "support": [
            ("beilagen-zum-gesuch:all", Always()),
            ("nachforderungen:all", Always()),
            ("alle-beteiligten:all", Always()),
            ("beteiligte-behoerden:all", Always()),
            ("intern:all", Always()),
        ],
    },
}
