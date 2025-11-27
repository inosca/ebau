from camac.permissions.conditions import (
    Always,
    HasInquiry,
    IsPaper,
    RequireInstanceState,
    RequireWorkItem,
)

from .conditions import OwnDocument

BEFORE_DECISION = ~RequireInstanceState(
    [
        "rejected",
        "correction",
        "sb1",
        "sb2",
        "conclusion",
        "finished",
        "finished_internal",
        "evaluated",
    ],
    condition_name="AfterDecision",
)

ADDITIONAL_DEMAND = RequireWorkItem(
    "fill-additional-demand",
    status="ready",
    condition_name="HasAdditionalDemand",
)

SB1 = RequireInstanceState(["sb1"])
SB2 = RequireInstanceState(["sb2"])

INTERNAL_PERMISSIONS = [
    ("intern:create", Always()),
    ("intern:update", Always()),
    ("intern:tag", Always()),
    ("intern:move", Always()),
    ("intern:replace", Always()),
    ("intern:delete", Always()),
]

BE_PERMISSIONS_ALEXANDRIA = {
    "ENABLED": True,
    "ACCESS_LEVELS": {
        "applicant": [
            # Beilagen zum Gesuch: Create and delete allowed while instance is
            # in status new
            ("beilagen-zum-gesuch:create", RequireInstanceState(["new"])),
            ("beilagen-zum-gesuch:delete", RequireInstanceState(["new"])),
            # Nachforderungen: Create and delete allowed while we have an active
            # additional demand
            ("nachforderungen:create", ADDITIONAL_DEMAND),
            ("nachforderungen:delete", ADDITIONAL_DEMAND),
            # Beilagen SB1: Create and delete allowed while instance is in
            # status sb1
            ("beilagen-sb1:create", SB1),
            ("beilagen-sb1:delete", SB1),
            # Beilagen SB2: Create and delete allowed while instance is in
            # status sb2
            ("beilagen-sb2:create", SB2),
            ("beilagen-sb2:delete", SB2),
        ],
        "lead-authority": [
            # Beilagen zum Gesuch: Only tagging and marking is allowed
            # except for paper dossiers where everything is allowed except
            # move/replace/delete after the decision
            ("beilagen-zum-gesuch:create", IsPaper()),
            ("beilagen-zum-gesuch:update", IsPaper()),
            ("beilagen-zum-gesuch:tag", Always()),
            ("beilagen-zum-gesuch:mark:decision", BEFORE_DECISION),
            ("beilagen-zum-gesuch:mark:geometer", Always()),
            ("beilagen-zum-gesuch:mark:publication", Always()),
            ("beilagen-zum-gesuch:mark:void", Always()),
            ("beilagen-zum-gesuch:move", IsPaper() & BEFORE_DECISION),
            ("beilagen-zum-gesuch:replace", IsPaper() & BEFORE_DECISION),
            ("beilagen-zum-gesuch:delete", IsPaper() & BEFORE_DECISION),
            # Nachforderungen: Only tagging and marking is allowed except
            # for paper dossiers where everything is allowed except
            # move/replace/delete after the decision
            ("nachforderungen:create", Always()),
            ("nachforderungen:update", OwnDocument()),
            ("nachforderungen:tag", Always()),
            ("nachforderungen:mark:decision", BEFORE_DECISION),
            ("nachforderungen:mark:geometer", Always()),
            ("nachforderungen:mark:publication", Always()),
            ("nachforderungen:mark:void", Always()),
            ("nachforderungen:move", OwnDocument() & BEFORE_DECISION),
            ("nachforderungen:replace", OwnDocument() & BEFORE_DECISION),
            ("nachforderungen:delete", OwnDocument() & BEFORE_DECISION),
            # Beteiligte Behörden: Everything is allowed except
            # move/replace/delete after the decision and on documents not
            # owned by the service
            ("beteiligte-behoerden:create", Always()),
            ("beteiligte-behoerden:create", Always()),
            ("beteiligte-behoerden:update", Always()),
            ("beteiligte-behoerden:tag", Always()),
            ("beteiligte-behoerden:mark:decision", BEFORE_DECISION),
            ("beteiligte-behoerden:mark:geometer", Always()),
            ("beteiligte-behoerden:mark:publication", Always()),
            ("beteiligte-behoerden:mark:void", Always()),
            ("beteiligte-behoerden:move", OwnDocument() & BEFORE_DECISION),
            ("beteiligte-behoerden:replace", OwnDocument() & BEFORE_DECISION),
            ("beteiligte-behoerden:delete", OwnDocument() & BEFORE_DECISION),
            # Alle Beteiligten: Everything is allowed except
            # move/replace/delete after the decision.
            ("alle-beteiligten:create", Always()),
            ("alle-beteiligten:update", Always()),
            ("alle-beteiligten:tag", Always()),
            ("alle-beteiligten:mark:decision", BEFORE_DECISION),
            ("alle-beteiligten:mark:geometer", Always()),
            ("alle-beteiligten:mark:publication", Always()),
            ("alle-beteiligten:mark:void", Always()),
            ("alle-beteiligten:move", BEFORE_DECISION),
            ("alle-beteiligten:replace", BEFORE_DECISION),
            ("alle-beteiligten:delete", BEFORE_DECISION),
            # Rechtsbegehren: Everything is allowed except
            # move/replace/delete after the decision.
            ("rechtsbegehren:create", Always()),
            ("rechtsbegehren:update", Always()),
            ("rechtsbegehren:tag", Always()),
            ("rechtsbegehren:mark:decision", BEFORE_DECISION),
            ("rechtsbegehren:mark:geometer", Always()),
            ("rechtsbegehren:mark:publication", Always()),
            ("rechtsbegehren:mark:void", Always()),
            ("rechtsbegehren:move", BEFORE_DECISION),
            ("rechtsbegehren:replace", BEFORE_DECISION),
            ("rechtsbegehren:delete", BEFORE_DECISION),
            # Intern: allow everything but marking
            *INTERNAL_PERMISSIONS,
        ],
        "legal-authority": [
            # Intern: allow everything but marking
            *INTERNAL_PERMISSIONS
        ],
        "involved-authority": [
            # Geometer mark is allowed on all categories
            ("beilagen-zum-gesuch:mark:geometer", Always()),
            ("nachforderungen:mark:geometer", Always()),
            ("beteiligte-behoerden:mark:geometer", Always()),
            ("alle-beteiligten:mark:geometer", Always()),
            ("rechtsbegehren:mark:geometer", Always()),
            # Intern: allow everything but marking
            *INTERNAL_PERMISSIONS,
        ],
        "construction-control": [
            # Geometer mark is allowed on all categories
            ("beilagen-zum-gesuch:mark:geometer", Always()),
            ("nachforderungen:mark:geometer", Always()),
            ("beteiligte-behoerden:mark:geometer", Always()),
            ("alle-beteiligten:mark:geometer", Always()),
            ("rechtsbegehren:mark:geometer", Always()),
            # Beteiligte Behörden: Everything allowed but move/replace/delete
            # only on own documents
            ("beteiligte-behoerden:create", Always()),
            ("beteiligte-behoerden:update", Always()),
            ("beteiligte-behoerden:tag", Always()),
            ("beteiligte-behoerden:move", OwnDocument()),
            ("beteiligte-behoerden:replace", OwnDocument()),
            ("beteiligte-behoerden:delete", OwnDocument()),
            ("beteiligte-behoerden:mark:void", Always()),
            # Beilagen SB1: Changes only allowed while in SB1 and on own
            # documents
            ("beilagen-sb1:create", SB1),
            ("beilagen-sb1:update", OwnDocument() & SB1),
            ("beilagen-sb1:tag", Always()),
            ("beilagen-sb1:move", OwnDocument() & SB1),
            ("beilagen-sb1:replace", OwnDocument() & SB1),
            ("beilagen-sb1:delete", OwnDocument() & SB1),
            # Beilagen SB1: Changes only allowed while in SB2 and on own
            # documents
            ("beilagen-sb2:create", SB2),
            ("beilagen-sb2:update", OwnDocument() & SB2),
            ("beilagen-sb2:tag", Always()),
            ("beilagen-sb2:move", OwnDocument() & SB2),
            ("beilagen-sb2:replace", OwnDocument() & SB2),
            ("beilagen-sb2:delete", OwnDocument() & SB2),
            # Intern: allow everything but marking
            *INTERNAL_PERMISSIONS,
        ],
        "involved-construction-control": [
            # Geometer mark is allowed on all categories
            ("beilagen-zum-gesuch:mark:geometer", Always()),
            ("nachforderungen:mark:geometer", Always()),
            ("beteiligte-behoerden:mark:geometer", Always()),
            ("alle-beteiligten:mark:geometer", Always()),
            ("rechtsbegehren:mark:geometer", Always()),
            # Intern: allow everything but marking
            *INTERNAL_PERMISSIONS,
        ],
        "distribution-service": [
            ("beteiligte-behoerden:create", HasInquiry()),
            ("beteiligte-behoerden:update", OwnDocument() & HasInquiry()),
            ("beteiligte-behoerden:move", OwnDocument() & HasInquiry()),
            ("beteiligte-behoerden:replace", OwnDocument() & HasInquiry()),
            ("beteiligte-behoerden:delete", OwnDocument() & HasInquiry()),
            # Intern: allow everything but marking
            *INTERNAL_PERMISSIONS,
        ],
        "geometer": [
            ("beilagen-sb1:create", SB1),
            ("beilagen-sb1:update", SB1),
            ("beilagen-sb1:move", OwnDocument() & SB1),
            ("beilagen-sb1:replace", OwnDocument() & SB1),
            ("beilagen-sb1:delete", OwnDocument() & SB1),
            # Intern: allow everything but marking
            *INTERNAL_PERMISSIONS,
        ],
        "support": [
            # For support, we always allow all actions on all categories
            ("beilagen-zum-gesuch:all", Always()),
            ("nachforderungen:all", Always()),
            ("beteiligte-behoerden:all", Always()),
            ("alle-beteiligten:all", Always()),
            ("rechtsbegehren:all", Always()),
            ("intern:all", Always()),
            ("beilagen-sb1:all", Always()),
            ("beilagen-sb2:all", Always()),
        ],
    },
}
