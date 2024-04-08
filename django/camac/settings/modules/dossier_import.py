from camac.constants.kt_bern import (
    INSTANCE_STATE_DONE,
    INSTANCE_STATE_EVALUATED,
    INSTANCE_STATE_NEW,
    INSTANCE_STATE_SB1,
)
from camac.settings.env import env

DOSSIER_IMPORT = {
    "default": {
        "WRITER_CLASS": "camac.dossier_import.writers.DossierWriter",
        "USER": "service-account-camac-admin",
    },
    "kt_schwyz": {
        "ENABLED": True,
        "WRITER_CLASS": "camac.dossier_import.config.kt_schwyz.KtSchwyzDossierWriter",
        "INSTANCE_STATE_MAPPING": {
            "SUBMITTED": 2,
            "APPROVED": 8,
            "DONE": 10,
        },
        "FORM_ID": 29,  # "migriertes-dossier"
        "CALUMA_FORM": "baugesuch",  # "dummy"-Form
        "ATTACHMENT_SECTION_ID": 7,  # attachmentsection for imported documents
        "LOCATION_REQUIRED": True,  # this is a workaround to account for differing validation requirements per config
        "TRANSFORM_COORDINATE_SYSTEM": "epsg:4326",  # use world wide coordinates instead of swiss ones
        "PROD_URL": env.str(
            "DJANGO_DOSSIER_IMPORT_PROD_URL", "https://behoerden.ebau-sz.ch/"
        ),
        "PROD_AUTH_URL": env.str(
            "DJANGO_DOSSIER_IMPORT_PROD_AUTH_URL",
            "https://ebau-sz.ch/auth/realms/ebau/protocol/openid-connect/token",
        ),
        "PROD_SUPPORT_GROUP_ID": 486,
        "RESOURCE_ID_PATH": "/index/template/resource-id/25#/dossier-import/",  # That's required for `reversing` the URL to the dossier-import resource tab in the UI
    },
    "kt_bern": {
        "ENABLED": True,
        "WRITER_CLASS": "camac.dossier_import.config.kt_bern.KtBernDossierWriter",
        "INSTANCE_STATE_MAPPING": {
            "BUILDINGPERMIT": {
                "SUBMITTED": INSTANCE_STATE_NEW,
                "APPROVED": INSTANCE_STATE_SB1,
                "REJECTED": INSTANCE_STATE_DONE,
                "WRITTEN OFF": INSTANCE_STATE_DONE,
                "DONE": INSTANCE_STATE_DONE,
            },
            "PRELIMINARY": {
                "SUBMITTED": INSTANCE_STATE_NEW,
                "APPROVED": INSTANCE_STATE_EVALUATED,
                "REJECTED": INSTANCE_STATE_EVALUATED,
                "WRITTEN OFF": INSTANCE_STATE_EVALUATED,
                "DONE": INSTANCE_STATE_EVALUATED,
            },
        },
        "WORKFLOW_MAPPING": {
            "BUILDINGPERMIT": "building-permit",
            "PRELIMINARY": "preliminary-clarification",
        },
        "CALUMA_FORM": "migriertes-dossier",
        "FORM_ID": 1,
        "ATTACHMENT_SECTION_ID": 4,  # Internal
        "PROD_URL": env.str(
            "DJANGO_DOSSIER_IMPORT_PROD_URL",
            "https://ebau.apps.be.ch/",
        ),
        "PROD_AUTH_URL": env.str(
            "DJANGO_DOSSIER_IMPORT_PROD_AUTH_URL",
            "https://sso.be.ch/auth/realms/ebau/protocol/openid-connect/token",
        ),
        "PROD_SUPPORT_GROUP_ID": 10000,
        "RESOURCE_ID_PATH": "/index/template/resource-id/2000000#/dossier-import/",  # That's required for `reversing` the URL to the dossier-import resource tab in the UI
    },
}
