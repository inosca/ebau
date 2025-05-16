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
        # For "Bauen"
        "AGR_GROUPS": [20096],
        # For "Schiesslärm"
        "AGR_SHOOTING_GROUPS": [20038],
    },
}
