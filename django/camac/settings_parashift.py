import environ

env = environ.Env()

PARASHIFT = {
    "test": {
        "ENABLED": True,
    },
    "kt_uri": {
        "ENABLED": True,
    },
    "default": {
        "BASE_URI": env.str(
            "PARASHIFT_BASE_URI", default="https://api.parashift.io/v2"
        ),
        "SOURCE_FILES_URI": env.str(
            "PARASHIFT_SOURCE_FILES_URI",
            default="https://individual-extraction.api.parashift.io/v1",
        ),
        "KOOR_BG": {
            "TENANT_ID": env.int("PARASHIFT_TENANT_ID_KOOR_BG", default=0000),
            "API_KEY": env.str("PARASHIFT_API_KEY_KOOR_BG", default="ey..."),
            "CAMAC_GROUP_ID": 142,
        },
        # Seedorf
        "1214": {
            "TENANT_ID": env.int("PARASHIFT_TENANT_ID_1214", default=0000),
            "API_KEY": env.str("PARASHIFT_API_KEY_1214", default="ey..."),
            "CAMAC_GROUP_ID": 151,
        },
        # Erstfeld
        "1206": {
            "TENANT_ID": env.int("PARASHIFT_TENANT_ID_1206", default=0000),
            "API_KEY": env.str("PARASHIFT_API_KEY_1206", default="ey..."),
            "CAMAC_GROUP_ID": 145,
        },
        # Seelisberg
        "1215": {
            "TENANT_ID": env.int("PARASHIFT_TENANT_ID_1215", default=0000),
            "API_KEY": env.str("PARASHIFT_API_KEY_1215", default="ey..."),
            "CAMAC_GROUP_ID": 152,
        },
    },
}
