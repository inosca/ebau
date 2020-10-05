KOOR_BG_ROLE_ID = 3

KOOR_NP_ROLE_ID = 1061

CIRCULATION_STATE_RUN = 1
CIRCULATION_STATE_OK = 2
CIRCULATION_STATE_IDLE = 21
CIRCULATION_STATE_NFD = 41

ROLE_MUNICIPALITY = 6  # Sekretariat der Gemeindebaubehörde

INSTANCE_STATE_COMM = 21
INSTANCE_STATE_EXT = 22
INSTANCE_STATE_EXT_GEM = 32
INSTANCE_STATE_CIRC = 23
INSTANCE_STATE_REDAC = 24
INSTANCE_STATE_DONE = 25
INSTANCE_STATE_ARCH = 26
INSTANCE_STATE_DEL = 27
INSTANCE_STATE_NEW = 1
INSTANCE_STATE_NEW_PORTAL = 28
INSTANCE_STATE_CONTROL = 34

# TODO theoretically, we'd like to hide COMM as well, but instances can be sent
# "back" into "COMM" if the canton didn't do a circulation
INSTANCE_STATES_HIDDEN_FOR_KOOR = [INSTANCE_STATE_NEW, INSTANCE_STATE_NEW_PORTAL]

# Question identifiers (Chapter/Question/Item) for various information that we need
# Format: List of 3-tuples to implement fallback
CQI_FOR_VORHABEN = [(21, 98, 1)]
CQI_FOR_PARZELLE = [(21, 91, 1), (101, 91, 1), (102, 91, 1)]
CQI_FOR_GESUCHSTELLER = [(1, 23, 1)]
CQI_FOR_NFD_COMPLETION_DATE = (41, 243, 1)


NOTIFICATION_TEMPLATE_DEADLINE_DATE_FACHSTELLE = (
    "aktivierung-deadline-überzogen-fachstelle"  # 1448
)
NOTIFICATION_TEMPLATE_COMPLETION_DATE_FACHSTELLE = (
    "aktivierung-nfd-vollständig-überzogen-fachstelle"  # 1449
)
NOTIFICATION_TEMPLATE_DEADLINE_DATE_LEITBEHOERDE = (
    "aktivierung-deadline-überzogen-leitbehoerde"  # 1450
)
NOTIFICATION_TEMPLATE_COMPLETION_DATE_LEITBEHOERDE = (
    "aktivierung-nfd-vollständig-überzogen-leitbehoerde"  # 1451
)
CQI_FOR_GESUCHSTELLER = [(1, 23, 1)]
