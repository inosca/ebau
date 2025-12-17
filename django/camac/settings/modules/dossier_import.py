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
        "RESOURCE_ID_PATH": "/dossier-import",
        "DELETE_KEYWORD": "<LÖSCHEN>",
        "QUEUE": "django-q",
    },
    "kt_schwyz": {
        "ENABLED": True,
        "WRITER_CLASS": "camac.dossier_import.config.kt_schwyz.KtSchwyzDossierWriter",
        "INSTANCE_STATE_MAPPING": {
            "SUBMITTED": 2,
            "APPROVED": 8,
            "DONE": 10,
            "WRITTEN OFF": 13,
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
    "kt_so": {
        "ENABLED": True,
        "WRITER_CLASS": "camac.dossier_import.config.kt_so.KtSolothurnDossierWriter",
        "INSTANCE_STATE_MAPPING": {
            "SUBMITTED": "subm",
            "APPROVED": "decided",
            "REJECTED": "finished",
            "WRITTEN OFF": "withdrawn",
            "DONE": "finished",
        },
        "CALUMA_FORM": "migriertes-dossier",
        "FORM_ID": 1,
        "ALEXANDRIA_CATEGORY": "migrierte-dokumente",
        "PROD_URL": env.str(
            "DJANGO_DOSSIER_IMPORT_PROD_URL",
            "https://ebau.so.ch/",
        ),
        "PROD_AUTH_URL": env.str(
            "DJANGO_DOSSIER_IMPORT_PROD_AUTH_URL",
            "https://ebau.so.ch/auth/realms/ebau/protocol/openid-connect/token",
        ),
        "QUEUE": "celery",
    },
    "kt_ag": {
        "ENABLED": True,
        "USER": "Migration",
        "GROUP": "Support",
        "WRITER_CLASS": "camac.dossier_import.config.kt_ag.dossier_import.dossier_writer.KtAargauDossierWriter",
        "LOADER_CLASS": "camac.dossier_import.config.kt_ag.dossier_import.dossier_loader.KtAargauDossierLoader",
        "CALUMA_FORM": "baugesuch-migration",
        "FORM_ID": 1,
        "MIGRATION_REPORTS_DIR": env.str(
            "MIGRATION_REPORTS_DIR", "/app/kt_ag/migration_reports"
        ),
        "SAP_ACCESS": {
            "enabled": False,
            "json_target_dir": "kt_ag_json",
            "host": "unknown",
            "port": -1,
            "user": "unknown",
            "password": "unknown",
            "db_name": "unknown",
            "schema": "unknown",
            "soap_server": "unknown",
            "soap_user": "unknown",
            "soap_password": "unknown",
        },
        "DOCS_MIGRATION_ENABLED": env.bool("EBAU_DOCS_MIGRATION_ENABLED", True),
        "EBAU_DOCUMENT_CLIENT": {
            "connection": {
                "base_url": env.str(
                    "EBAU_DOCUMENT_CLIENT_BASE_URL", "EBAU_DOCUMENT_CLIENT_BASE_URL"
                ),
                "username": env.str("EBAU_DOCUMENT_CLIENT_USERNAME", "testuser"),
                "password": env.str("EBAU_DOCUMENT_CLIENT_PASSWORD", "testpass"),
            },
            "check_replication_interval_seconds": env.int(
                "CHECK_REPLICATION_INTERVAL_SECONDS", 60
            ),
        },
        "S3": {
            "url": env.str("ALEXANDRIA_S3_ENDPOINT_URL", "http://minio:9000"),
            "access_key": env.str("ALEXANDRIA_S3_ACCESS_KEY", "minio"),
            "secret_key": env.str("ALEXANDRIA_S3_SECRET_KEY", "minio123"),
            "source_bucket": env.str(
                "EBAU_S3_MIGRATION_BUCKET_NAME", "migration-media"
            ),
        },
    },
    "kt_gr": {
        "ENABLED": True,
        "WRITER_CLASS": "camac.dossier_import.config.kt_gr.KtGraubundenDossierWriter",
        "INSTANCE_STATE_MAPPING": {
            "SUBMITTED": "subm",
            "APPROVED": "construction-acceptance",
            "REJECTED": "rejected",
            "WRITTEN OFF": "withdrawn",
            "DONE": "finished",
        },
        "CALUMA_FORM": "migriertes-dossier",
        "FORM_ID": 1,
        "ALEXANDRIA_CATEGORY": "migrierte-dokumente",
        # todo: enable for GR production
        # "PROD_URL": env.str(
        #     "DJANGO_DOSSIER_IMPORT_PROD_URL",
        #     "https://ebau.gr.ch/",
        # ),
        # "PROD_AUTH_URL": env.str(
        #     "DJANGO_DOSSIER_IMPORT_PROD_AUTH_URL",
        #     "https://ebau.gr.ch/auth/realms/ebau/protocol/openid-connect/token",
        # ),
        "QUEUE": "celery",
    },
}
