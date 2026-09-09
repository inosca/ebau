from camac.constants.kt_gr import ARE_SERVICE_GROUP
from camac.permissions.conditions import (
    Always,
    HasAdditionalDemandWithFormEdit,
    HasRole,
    IsPaper,
    IsServiceGroup,
    RequireInstanceState,
)

from .conditions import ApplicantFile, HasAdditionalDemand, IsNewDocument, OwnDocument

# __________________________________________________________________

BEFORE_SUBMIT = RequireInstanceState(
    ["new"],
    condition_name="BeforeSubmit",
)

AFTER_SUBMIT = ~RequireInstanceState(
    ["subm"],
    condition_name="AfterSubmit",
)

BEFORE_DECISION = ~RequireInstanceState(
    [
        "construction-acceptance",
        "finished",
        "rejected",
        "withdrawn",
        "withdrawal",
        "decided",
    ],
    condition_name="BeforeDecision",
)

BEFORE_CONSTRUCTION_ACCEPTANCE = ~RequireInstanceState(
    [
        "correction",
        "finished",
        "rejected",
        "withdrawn",
        "withdrawal",
    ],
    condition_name="BeforeConstructionAcceptance",
)
# __________________________________________________________________

# DISTRIBUTION SERVICE
# municipalities are treated like service-leads if they are involved via distribution service.


DIST_ONLY_ARE = IsServiceGroup([ARE_SERVICE_GROUP])
DIST_ONLY_SERVICE = HasRole(
    [
        "service-lead",
        "municipality-lead",
    ]
)
DIST_SERVICE_AND_ARE = DIST_ONLY_ARE | DIST_ONLY_SERVICE
DIST_SERVICE_AND_SUBSERVICE = HasRole(
    [
        "service-lead",
        "municipality-lead",
        "subservice",
    ]
)

# __________________________________________________________________

INTERNAL_PERMISSIONS = [
    ("intern:create", IsNewDocument() | OwnDocument()),
    ("intern:update", OwnDocument()),
    ("intern:tag", OwnDocument()),
    ("intern:move", OwnDocument()),
    ("intern:replace", OwnDocument()),
    ("intern:delete", OwnDocument()),
]

# __________________________________________________________________

GR_PERMISSIONS_ALEXANDRIA = {
    "ENABLED": True,
    "ACCESS_LEVELS": {
        # __________________________________________________________________
        "applicant": [
            # 1. Beilagen zum Gesuch:
            (
                "beilagen-zum-gesuch:create",
                (BEFORE_SUBMIT | HasAdditionalDemandWithFormEdit()),
            ),
            (
                "ebbw-beilagen-zum-gesuch:create",
                (BEFORE_SUBMIT | HasAdditionalDemandWithFormEdit()),
            ),
            ("beilagen-zum-gesuch:mark:void", HasAdditionalDemandWithFormEdit()),
            ("ebbw-beilagen-zum-gesuch:mark:void", HasAdditionalDemandWithFormEdit()),
            ("beilagen-zum-gesuch:delete", BEFORE_SUBMIT),
            ("ebbw-beilagen-zum-gesuch:delete", BEFORE_SUBMIT),
            # 2. Nachforderungen:
            ("nachforderung:create", HasAdditionalDemand()),
            ("ebbw-nachforderung:create", HasAdditionalDemand()),
            ("nachforderung:delete", HasAdditionalDemand()),
            ("ebbw-nachforderung:delete", HasAdditionalDemand()),
            # 3. Alle Beteiligten: never
            # 4. Beteiligte Behörden: never
            # 5. Einsprachen Beschwerden: never
            # 6. Bauabnahme: never
            # 7. intern: never
            # 8. Intern mit Unterfachstellen: never
            # 9. Stellungnahmen ans ARE: never
            # 10. Alle Kanton: never
            # 11. Umweltschutzorganisationen: never
            # 12. Migrierte Dokumente: never
            # 13. System
            (
                "system:create",
                RequireInstanceState(["new"]) | HasAdditionalDemandWithFormEdit(),
            ),
            (
                "system:delete",
                RequireInstanceState(["new"]) | HasAdditionalDemandWithFormEdit(),
            ),
        ],
        # __________________________________________________________________
        "lead-authority": [
            # 1. Beilagen zum Gesuch:
            ("beilagen-zum-gesuch:create", BEFORE_DECISION),
            ("ebbw-beilagen-zum-gesuch:create", BEFORE_DECISION),
            ("beilagen-zum-gesuch:update", BEFORE_DECISION),
            ("ebbw-beilagen-zum-gesuch:update", BEFORE_DECISION),
            ("beilagen-zum-gesuch:tag", BEFORE_CONSTRUCTION_ACCEPTANCE),
            ("ebbw-beilagen-zum-gesuch:tag", BEFORE_CONSTRUCTION_ACCEPTANCE),
            ("beilagen-zum-gesuch:move", BEFORE_DECISION & ~ApplicantFile()),
            ("ebbw-beilagen-zum-gesuch:move", BEFORE_DECISION & ~ApplicantFile()),
            ("beilagen-zum-gesuch:mark:all", BEFORE_DECISION),
            ("ebbw-beilagen-zum-gesuch:mark:all", BEFORE_DECISION),
            (
                "beilagen-zum-gesuch:replace",
                ((IsPaper() & BEFORE_DECISION) | (OwnDocument() & BEFORE_DECISION))
                & ~ApplicantFile(),
            ),
            (
                "ebbw-beilagen-zum-gesuch:replace",
                ((IsPaper() & BEFORE_DECISION) | (OwnDocument() & BEFORE_DECISION))
                & ~ApplicantFile(),
            ),
            (
                "beilagen-zum-gesuch:delete",
                ((IsPaper() & BEFORE_SUBMIT) | (OwnDocument() & BEFORE_DECISION)),
            ),
            (
                "ebbw-beilagen-zum-gesuch:delete",
                ((IsPaper() & BEFORE_SUBMIT) | (OwnDocument() & BEFORE_DECISION)),
            ),
            # 2. Nachforderung:
            ("nachforderung:create", BEFORE_DECISION),
            ("ebbw-nachforderung:create", BEFORE_DECISION),
            ("nachforderung:update", BEFORE_DECISION),
            ("ebbw-nachforderung:update", BEFORE_DECISION),
            ("nachforderung:tag", BEFORE_DECISION),
            ("ebbw-nachforderung:tag", BEFORE_DECISION),
            (
                "nachforderung:move",
                ((OwnDocument() & BEFORE_DECISION) | (IsPaper() & BEFORE_DECISION))
                & ~ApplicantFile(),
            ),
            (
                "ebbw-nachforderung:move",
                ((OwnDocument() & BEFORE_DECISION) | (IsPaper() & BEFORE_DECISION))
                & ~ApplicantFile(),
            ),
            ("nachforderung:mark:all", BEFORE_DECISION),
            ("ebbw-nachforderung:mark:all", BEFORE_DECISION),
            (
                "nachforderung:replace",
                ((OwnDocument() & BEFORE_DECISION) | (IsPaper() & BEFORE_DECISION))
                & ~ApplicantFile(),
            ),
            (
                "ebbw-nachforderung:replace",
                ((OwnDocument() & BEFORE_DECISION) | (IsPaper() & BEFORE_DECISION))
                & ~ApplicantFile(),
            ),
            ("nachforderung:delete", OwnDocument() & BEFORE_DECISION),
            ("ebbw-nachforderung:delete", OwnDocument() & BEFORE_DECISION),
            # 3. Alle Beteiligten:
            ("alle-beteiligten:create", BEFORE_DECISION),
            ("alle-beteiligten:update", BEFORE_DECISION),
            ("alle-beteiligten:tag", BEFORE_DECISION),
            ("alle-beteiligten:move", BEFORE_DECISION),
            ("alle-beteiligten:mark:all", BEFORE_DECISION),
            ("alle-beteiligten:replace", BEFORE_DECISION),
            ("alle-beteiligten:delete", OwnDocument() & BEFORE_DECISION),
            # 4. Beteiligte Behörden:
            ("beteiligte-behörden:create", BEFORE_DECISION),
            ("beteiligte-behörden:update", BEFORE_DECISION),
            ("beteiligte-behörden:tag", BEFORE_DECISION),
            ("beteiligte-behörden:move", BEFORE_DECISION),
            ("beteiligte-behörden:mark:all", BEFORE_DECISION),
            ("beteiligte-behörden:replace", BEFORE_DECISION),
            ("beteiligte-behörden:delete", OwnDocument() & BEFORE_DECISION),
            # 5. Einsprachen Beschwerden:
            ("einsprachen-beschwerden:create", AFTER_SUBMIT),
            ("einsprachen-beschwerden:update", AFTER_SUBMIT),
            ("einsprachen-beschwerden:tag", AFTER_SUBMIT),
            ("einsprachen-beschwerden:move", AFTER_SUBMIT),
            ("einsprachen-beschwerden:mark:all", AFTER_SUBMIT),
            ("einsprachen-beschwerden:replace", AFTER_SUBMIT),
            ("einsprachen-beschwerden:delete", AFTER_SUBMIT),
            # 6. Bauabnahme:
            ("bauabnahme:create", BEFORE_CONSTRUCTION_ACCEPTANCE),
            ("bauabnahme:update", BEFORE_CONSTRUCTION_ACCEPTANCE),
            ("bauabnahme:tag", BEFORE_CONSTRUCTION_ACCEPTANCE),
            ("bauabnahme:move", BEFORE_CONSTRUCTION_ACCEPTANCE),
            ("bauabnahme:replace", BEFORE_CONSTRUCTION_ACCEPTANCE),
            ("bauabnahme:mark:all", BEFORE_CONSTRUCTION_ACCEPTANCE),
            ("bauabnahme:delete", BEFORE_CONSTRUCTION_ACCEPTANCE),
            # 7. Intern: allow everything but marking
            *INTERNAL_PERMISSIONS,
            # 8. Intern mit Unterfachstellen:
            (
                "intern-mit-unterfachstellen:create",
                IsNewDocument() | OwnDocument(include_subservice=True),
            ),
            (
                "intern-mit-unterfachstellen:update",
                OwnDocument(include_subservice=True),
            ),
            (
                "intern-mit-unterfachstellen:tag",
                OwnDocument(include_subservice=True),
            ),
            (
                "intern-mit-unterfachstellen:move",
                OwnDocument(include_subservice=True),
            ),
            (
                "intern-mit-unterfachstellen:replace",
                OwnDocument(include_subservice=True),
            ),
            (
                "intern-mit-unterfachstellen:delete",
                OwnDocument(include_subservice=True),
            ),
            # 9. Stellungnahmen ans ARE: never
            # 10. Alle Kanton: never
            # 11. Umweltschutzorganisationen: never
            # 12. Migrierte Dokumente:
            ("migrierte-dokumente:create", BEFORE_DECISION),
            ("migrierte-dokumente:update", BEFORE_DECISION),
            ("migrierte-dokumente:tag", BEFORE_DECISION),
            ("migrierte-dokumente:move", BEFORE_DECISION),
            ("migrierte-dokumente:mark:all", BEFORE_DECISION),
            ("migrierte-dokumente:replace", IsPaper() & BEFORE_DECISION),
            # 13. System: never
        ],
        # __________________________________________________________________
        "distribution-service": [
            # 1. Beilagen zum Gesuch:
            ("beilagen-zum-gesuch:create", DIST_SERVICE_AND_ARE & BEFORE_DECISION),
            ("ebbw-beilagen-zum-gesuch:create", DIST_SERVICE_AND_ARE & BEFORE_DECISION),
            (
                "beilagen-zum-gesuch:update",
                (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument())) & BEFORE_DECISION,
            ),
            (
                "ebbw-beilagen-zum-gesuch:update",
                (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument())) & BEFORE_DECISION,
            ),
            ("beilagen-zum-gesuch:tag", BEFORE_DECISION),
            ("ebbw-beilagen-zum-gesuch:tag", BEFORE_DECISION),
            (
                "beilagen-zum-gesuch:move",
                (
                    (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument()))
                    & BEFORE_DECISION
                )
                & ~ApplicantFile(),
            ),
            (
                "ebbw-beilagen-zum-gesuch:move",
                (
                    (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument()))
                    & BEFORE_DECISION
                )
                & ~ApplicantFile(),
            ),
            ("beilagen-zum-gesuch:mark:all", DIST_ONLY_ARE & BEFORE_DECISION),
            ("ebbw-beilagen-zum-gesuch:mark:all", DIST_ONLY_ARE & BEFORE_DECISION),
            (
                "beilagen-zum-gesuch:mark:void",
                DIST_ONLY_SERVICE & OwnDocument() & BEFORE_DECISION,
            ),
            (
                "ebbw-beilagen-zum-gesuch:mark:void",
                DIST_ONLY_SERVICE & OwnDocument() & BEFORE_DECISION,
            ),
            (
                "beilagen-zum-gesuch:replace",
                (
                    (DIST_ONLY_ARE & BEFORE_DECISION & (OwnDocument() | IsPaper()))
                    & ~ApplicantFile()
                )
                | (DIST_ONLY_SERVICE & OwnDocument() & BEFORE_DECISION),
            ),
            (
                "ebbw-beilagen-zum-gesuch:replace",
                (
                    (DIST_ONLY_ARE & BEFORE_DECISION & (OwnDocument() | IsPaper()))
                    & ~ApplicantFile()
                )
                | (DIST_ONLY_SERVICE & OwnDocument() & BEFORE_DECISION),
            ),
            (
                "beilagen-zum-gesuch:delete",
                DIST_SERVICE_AND_ARE & OwnDocument() & BEFORE_DECISION,
            ),
            (
                "ebbw-beilagen-zum-gesuch:delete",
                DIST_SERVICE_AND_ARE & OwnDocument() & BEFORE_DECISION,
            ),
            # 2. Nachforderung:
            ("nachforderung:create", DIST_SERVICE_AND_ARE & BEFORE_DECISION),
            ("ebbw-nachforderung:create", DIST_SERVICE_AND_ARE & BEFORE_DECISION),
            (
                "nachforderung:update",
                (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument())) & BEFORE_DECISION,
            ),
            (
                "ebbw-nachforderung:update",
                (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument())) & BEFORE_DECISION,
            ),
            ("nachforderung:tag", BEFORE_DECISION),
            ("ebbw-nachforderung:tag", BEFORE_DECISION),
            (
                "nachforderung:move",
                (DIST_SERVICE_AND_ARE & OwnDocument() & BEFORE_DECISION)
                & ~ApplicantFile(),
            ),
            (
                "ebbw-nachforderung:move",
                (DIST_SERVICE_AND_ARE & OwnDocument() & BEFORE_DECISION)
                & ~ApplicantFile(),
            ),
            ("nachforderung:mark:all", (DIST_ONLY_ARE & BEFORE_DECISION)),
            ("ebbw-nachforderung:mark:all", (DIST_ONLY_ARE & BEFORE_DECISION)),
            (
                "nachforderung:mark:void",
                DIST_ONLY_SERVICE & OwnDocument() & BEFORE_DECISION,
            ),
            (
                "ebbw-nachforderung:mark:void",
                DIST_ONLY_SERVICE & OwnDocument() & BEFORE_DECISION,
            ),
            (
                "nachforderung:replace",
                (
                    (DIST_ONLY_ARE & (OwnDocument() | IsPaper()))
                    | (DIST_ONLY_SERVICE & OwnDocument())
                )
                & BEFORE_DECISION
                & ~ApplicantFile(),
            ),
            (
                "ebbw-nachforderung:replace",
                (
                    (DIST_ONLY_ARE & (OwnDocument() | IsPaper()))
                    | (DIST_ONLY_SERVICE & OwnDocument())
                )
                & BEFORE_DECISION
                & ~ApplicantFile(),
            ),
            (
                "nachforderung:delete",
                DIST_SERVICE_AND_ARE & OwnDocument() & BEFORE_DECISION,
            ),
            (
                "ebbw-nachforderung:delete",
                DIST_SERVICE_AND_ARE & OwnDocument() & BEFORE_DECISION,
            ),
            # 3. Alle Beteiligten:
            ("alle-beteiligten:create", BEFORE_DECISION),
            (
                "alle-beteiligten:update",
                OwnDocument() & BEFORE_DECISION,
            ),
            ("alle-beteiligten:tag", BEFORE_DECISION),
            (
                "alle-beteiligten:move",
                (DIST_ONLY_ARE | (DIST_SERVICE_AND_SUBSERVICE & OwnDocument()))
                & BEFORE_DECISION,
            ),
            (
                "alle-beteiligten:replace",
                OwnDocument() & BEFORE_DECISION,
            ),
            (
                "alle-beteiligten:delete",
                OwnDocument() & BEFORE_DECISION,
            ),
            # 4. Beteiligte Behörden:
            ("beteiligte-behörden:create", BEFORE_DECISION),
            (
                "beteiligte-behörden:update",
                OwnDocument() & BEFORE_DECISION,
            ),
            ("beteiligte-behörden:tag", BEFORE_DECISION),
            (
                "beteiligte-behörden:move",
                (DIST_ONLY_ARE | (DIST_SERVICE_AND_SUBSERVICE & OwnDocument()))
                & BEFORE_DECISION,
            ),
            (
                "beteiligte-behörden:replace",
                OwnDocument() & BEFORE_DECISION,
            ),
            (
                "beteiligte-behörden:delete",
                OwnDocument() & BEFORE_DECISION,
            ),
            # 5. Einsprachen Beschwerden (read-only):
            # 6. Bauabnahme: never
            # 7. Intern: allow everything but marking
            *INTERNAL_PERMISSIONS,
            # 8. Intern mit Unterfachstellen:
            (
                "intern-mit-unterfachstellen:create",
                IsNewDocument() | OwnDocument(include_subservice=True),
            ),
            (
                "intern-mit-unterfachstellen:update",
                OwnDocument(include_subservice=True),
            ),
            (
                "intern-mit-unterfachstellen:tag",
                OwnDocument(include_subservice=True),
            ),
            (
                "intern-mit-unterfachstellen:move",
                OwnDocument(include_subservice=True),
            ),
            (
                "intern-mit-unterfachstellen:replace",
                OwnDocument(include_subservice=True),
            ),
            (
                "intern-mit-unterfachstellen:delete",
                OwnDocument(include_subservice=True),
            ),
            # 9. Stellungnahmen ans ARE:
            (
                "stellungnahmen-are:create",
                (
                    DIST_ONLY_ARE
                    | (DIST_ONLY_SERVICE & (IsNewDocument() | OwnDocument()))
                )
                & BEFORE_DECISION,
            ),
            (
                "stellungnahmen-are:update",
                (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument())) & BEFORE_DECISION,
            ),
            ("stellungnahmen-are:tag", DIST_SERVICE_AND_ARE & BEFORE_DECISION),
            (
                "stellungnahmen-are:move",
                (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument())) & BEFORE_DECISION,
            ),
            ("stellungnahmen-are:mark:all", DIST_ONLY_ARE & BEFORE_DECISION),
            (
                "stellungnahmen-are:replace",
                DIST_ONLY_SERVICE & OwnDocument() & BEFORE_DECISION,
            ),
            (
                "stellungnahmen-are:delete",
                (
                    (DIST_ONLY_ARE | DIST_ONLY_SERVICE)
                    & (OwnDocument() & BEFORE_DECISION)
                ),
            ),
            # 10. Alle Kanton:
            ("alle-kanton:create", DIST_SERVICE_AND_ARE & BEFORE_DECISION),
            (
                "alle-kanton:update",
                (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument())) & BEFORE_DECISION,
            ),
            ("alle-kanton:tag", DIST_SERVICE_AND_ARE & BEFORE_DECISION),
            (
                "alle-kanton:move",
                (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument())) & BEFORE_DECISION,
            ),
            (
                "alle-kanton:replace",
                (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument())) & BEFORE_DECISION,
            ),
            (
                "alle-kanton:delete",
                (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument())) & BEFORE_DECISION,
            ),
            # 11. Umweltschutzorganisationen:
            ("umweltschutzorganisationen:create", DIST_ONLY_ARE & BEFORE_DECISION),
            ("umweltschutzorganisationen:update", DIST_ONLY_ARE & BEFORE_DECISION),
            ("umweltschutzorganisationen:tag", DIST_ONLY_ARE & BEFORE_DECISION),
            ("umweltschutzorganisationen:move", DIST_ONLY_ARE & BEFORE_DECISION),
            ("umweltschutzorganisationen:mark:all", DIST_ONLY_ARE & BEFORE_DECISION),
            ("umweltschutzorganisationen:replace", DIST_ONLY_ARE & BEFORE_DECISION),
            (
                "umweltschutzorganisationen:delete",
                DIST_ONLY_ARE & OwnDocument() & BEFORE_DECISION,
            ),
            # 12. Migrierte Dokumente:
            ("migrierte-dokumente:create", DIST_SERVICE_AND_ARE & BEFORE_DECISION),
            (
                "migrierte-dokumente:update",
                (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument())) & BEFORE_DECISION,
            ),
            ("migrierte-dokumente:tag", BEFORE_DECISION),
            (
                "migrierte-dokumente:move",
                (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument())) & BEFORE_DECISION,
            ),
            (
                "migrierte-dokumente:mark:all",
                (DIST_ONLY_ARE | (DIST_ONLY_SERVICE & OwnDocument())) & BEFORE_DECISION,
            ),
            (
                "migrierte-dokumente:replace",
                DIST_ONLY_ARE & OwnDocument() & BEFORE_DECISION,
            ),
            (
                "migrierte-dokumente:delete",
                DIST_ONLY_ARE & OwnDocument() & BEFORE_DECISION,
            ),
            # 13. System: never
        ],
        # __________________________________________________________________
        "read": [
            # No permissions needed as it's only read
        ],
        # __________________________________________________________________
        "geometer": [
            # 1. Beilagen zum Gesuch: never
            # 2. Nachforderung: never
            # 3. Alle Beteiligten: never
            # 4. Beteiligte Behörden: never
            # 5. Einsprachen Beschwerden: never
            # 6. Bauabnahme:
            ("bauabnahme:create", Always()),
            ("bauabnahme:update", OwnDocument()),
            ("bauabnahme:tag", OwnDocument()),
            ("bauabnahme:move", OwnDocument()),
            ("bauabnahme:mark:all", OwnDocument()),
            ("bauabnahme:replace", OwnDocument()),
            ("bauabnahme:delete", OwnDocument()),
            # 7. Intern: allow everything but marking
            *INTERNAL_PERMISSIONS,
            # 8. Intern mit Unterfachstellen: never
            # 9. Stellungnahmen ans ARE: never
            # 10. Alle Kanton: never
            # 11. Umweltschutzorganisationen: never
            # 12. Migrierte Dokumente: never
            # 13. System: never
        ],
        # __________________________________________________________________
        "uso": [
            # 1. Beilagen zum Gesuch:
            ("beilagen-zum-gesuch:tag", BEFORE_DECISION),
            ("ebbw-beilagen-zum-gesuch:tag", BEFORE_DECISION),
            # 2. Nachforderung:
            ("nachforderung:tag", BEFORE_DECISION),
            ("ebbw-nachforderung:tag", BEFORE_DECISION),
            # 3. Alle Beteiligten: never
            # 4. Beteiligte Behörden: never
            # 5. Einsprachen Beschwerden: never
            # 6. Bauabnahme: never
            # 7. Intern: allow everything but marking
            *INTERNAL_PERMISSIONS,
            # 8. Intern mit Unterfachstellen: never
            # 9. Stellungnahmen ans ARE:
            (
                "stellungnahmen-are:create",
                (IsNewDocument() | OwnDocument()) & BEFORE_DECISION,
            ),
            (
                "stellungnahmen-are:update",
                OwnDocument() & RequireInstanceState(["circulation"]),
            ),
            ("stellungnahmen-are:tag", BEFORE_DECISION),
            (
                "stellungnahmen-are:move",
                OwnDocument() & RequireInstanceState(["circulation"]),
            ),
            (
                "stellungnahmen-are:replace",
                OwnDocument() & RequireInstanceState(["circulation"]),
            ),
            (
                "stellungnahmen-are:delete",
                OwnDocument() & RequireInstanceState(["circulation"]),
            ),
            # 10. Alle Kanton: never
            # 11. Umweltschutzorganisationen: never
            # 12. Migrierte Dokumente: never
            # 12. Migrierte Dokumente:
            ("migrierte-dokumente:tag", BEFORE_DECISION),
            # 13. System: never
        ],
        # __________________________________________________________________
        "support": [
            # For support, we Always() allow all actions on all categories
            # 1. Beilagen zum Gesuch:
            ("beilagen-zum-gesuch:all", Always()),
            ("ebbw-beilagen-zum-gesuch:all", Always()),
            # 2. Nachforderung:
            ("nachforderung:all", Always()),
            ("ebbw-nachforderung:all", Always()),
            # 3. Alle Beteiligten:
            ("alle-beteiligten:all", Always()),
            # 4. Beteiligte Behörden:
            ("beteiligte-behörden:all", Always()),
            # 5. Einsprachen Beschwerden:
            ("einsprachen-beschwerden:all", Always()),
            # 6. Bauabnahme:
            ("bauabnahme:all", Always()),
            # 7. Intern: allow everything but marking
            ("intern:all", Always()),
            # 8. Intern mit Unterfachstellen:
            ("intern-mit-unterfachstellen:all", Always()),
            # 9. Stellungnahmen ans ARE:
            ("stellungnahmen-are:all", Always()),
            # 10. Alle Kanton:
            ("alle-kanton:all", Always()),
            # 11. Umweltschutzorganisationen:
            ("umweltschutzorganisationen:all", Always()),
            # 12. Migrierte Dokumente:
            ("migrierte-dokumente:all", Always()),
            # 13. System:
            ("system:all", Always()),
        ],
    },
}
