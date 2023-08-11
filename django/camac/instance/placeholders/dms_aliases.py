from django.conf import settings

CANTON_SPECIFIC_ALIASES = {
    "test": {"DOSSIER_NUMBER": "EBAU_NUMMER", "INSTANCE_ID": "DOSSIER_NUMMER"},
    "kt_be": {"DOSSIER_NUMBER": "EBAU_NUMMER", "INSTANCE_ID": "DOSSIER_NUMMER"},
    "kt_gr": {"DOSSIER_NUMBER": "DOSSIER_NUMMER", "INSTANCE_ID": "ID"},
}


def get(key):
    return CANTON_SPECIFIC_ALIASES[settings.APPLICATION_NAME].get(key, key)
