from camac.settings.env import env

GEVER = {
    "default": {
        "ENABLED": False,
    },
    "kt_bern": {
        "ENABLED": True,
        # For dev purposes, run the following, then put the results in .env
        # tools/get_gever_credentials.py
        "CLIENT_ID": env.str("GEVER_CLIENT_ID", default="gever-client-id"),
        "CLIENT_SECRET": env.str("GEVER_CLIENT_SECRET", default="gever-client-secret"),
        "TOKEN_URL": env.str(
            "GEVER_TOKEN_URL",
            # Note: For testing purposes, the path must match the DEV
            # env (but the host should not). This ensures VCR can match in CI
            default="http://gever-server.example/sts/dij/identity/connect/token",
        ),
        "API_BASE_URL": env.str(
            "GEVER_API_BASE_URL",
            # Note: For testing purposes, the path must match the DEV
            # env (but the host should not). This ensures VCR can match in CI
            default="http://gever-server.example/api/dij/groups/ebau/",
        ),
        "INSTANCE_TYPE_SHORT": {
            "Einfache Vorabklärung": "VA",
            "Vollständige Vorabklärung": "VA",
            "Verlängerung Geltungsdauer": "VA",
            "Baugesuch": "BG",
            "Baugesuch mit UVP": "BG",
            "Baupolizeiliches Verfahren": "BG",
            "Voranfrage": "VA",
            "Projektänderung": "PÄ",
            "Hecken / Feldgehölze / Bäume": "BG",
            "Klärung Baubewilligungspflicht": "BG",
            "Meldung Benützung von öffentlichem Terrain": "BG",
            "Meldung Solaranlagen": "BG",
            "Meldung Wärmeerzeugerersatz": "BG",
            "Migriertes Dossier": "BG",
            "Zutrittsermächtigung": "VA",
        },
        "GEVER_TASK_SLUG": "gever",
        "AGR_SERVICE_SLUG_BAUEN": "agr-bauen",
        "AGR_SERVICE_SLUG_SHOOTING_NOISE": "agr-schiesslaerm",
        "GESCHAEFT_TEMPLATES": {
            "TEMPLATE_GESCHAEFT_EBAU_BG_GEMEINDE": "ebau-bg-gemeinde",
            "TEMPLATE_GESCHAEFT_EBAU_BG_RSTA": "ebau-bg-rsta",
            "TEMPLATE_GESCHAEFT_EBAU_VA_GEMEINDE": "ebau-va-gemeinde",
            "TEMPLATE_GESCHAEFT_EBAU_VA_RSTA": "ebau-va-rsta",
        },
        "VERFAHRENSSTAND_COMPLETED": "verfahrensstand-completed",
        "VERFAHRENSSTAND_OPEN": "verfahrensstand-open",
        "HERKUNFT_MUNICIPALITY": "herkunft-gemeinde",
        "HERKUNFT_RSTA": "herkunft-rsta",
    },
}
