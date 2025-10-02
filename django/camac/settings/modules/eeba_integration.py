from camac.settings.env import env
from camac.utils import build_url

EEBA_INTEGRATION = {
    "default": {
        "ENABLED": False,
    },
    "kt_gr": {
        "ENABLED": True,
        "KEYCLOAK_EEBA_TOKEN_EXCHANGE_CLIENT": env.str(
            "KEYCLOAK_EEBA_TOKEN_EXCHANGE_CLIENT", default="eeba-token-exchange"
        ),
        "KEYCLOAK_EEBA_TOKEN_EXCHANGE_CLIENT_SECRET": env.str(
            "KEYCLOAK_EEBA_TOKEN_EXCHANGE_CLIENT_SECRET",
            default="FNVoLgpLjowJGYCQoBLLiZAq2CCpRod9",
        ),
        "KEYCLOAK_EEBA_TOKEN_EXCHANGE_SCOPE": env.str(
            "KEYCLOAK_EEBA_TOKEN_EXCHANGE_SCOPE", default="eeba-export"
        ),
        "EEBA_HIDDEN_QUESTIONS_SLUGS": {
            "integration_id": "eeba-integration-id",
            "state": "eeba-state",
            "required": "eeba-required",
            "web_url": "eeba-web-url",
        },
        "EEBA_BASE_URL": build_url(
            env.str("EEBA_BASE_URL", default="http://dummy-eeba:9000/dummy-eeba")
        ),
        "EEBA_SHARED_SECRET": env.str(
            "EEBA_SHARED_SECRET", "4z5hKJ2eQYXaGxvG9B8JfQ6C5L4A2mX5k7P0dQvNc4g="
        ),
        "EEBA_TIMEOUT_SECONDS": env.int("EEBA_TIMEOUT_SECONDS", default=60),
    },
}
