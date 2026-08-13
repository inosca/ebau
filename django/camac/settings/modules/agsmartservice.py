from pydantic import Field

from camac.settings.ebau_schema import ModuleApplicationConfig, ModuleConfig
from camac.settings.env import env


class AGSmartServiceConfig(ModuleApplicationConfig):
    service_id: str = Field(
        description="AG SmartService service ID.",
        default_factory=lambda: env.str(
            "AGSMARTSERVICE_SERVICE_ID", default="ABCD001337"
        ),
    )
    base_url: str = Field(
        description="Base URL of the AG SmartService API.",
        default_factory=lambda: env.str(
            "AGSMARTSERVICE_BASE_URL",
            default="https://my.example.url/meine-vorgaenge-service",
        ),
    )
    token_url: str = Field(
        description="OAuth token URL for the AG SmartService API.",
        default_factory=lambda: env.str(
            "AGSMARTSERVICE_TOKEN_URL", default="https://my.example.url/api/v1/token"
        ),
    )
    client_id: str = Field(
        description="OAuth client ID for the AG SmartService API.",
        default_factory=lambda: env.str("AGSMARTSERVICE_CLIENT_ID", default=""),
    )
    client_secret: str = Field(
        description="OAuth client secret for the AG SmartService API.",
        default_factory=lambda: env.str("AGSMARTSERVICE_CLIENT_SECRET", default=""),
    )
    timeout_seconds: int = Field(
        description="Timeout in seconds for AG SmartService API calls.",
        default_factory=lambda: env.int("AGSMARTSERVICE_TIMEOUT_SECONDS", default=30),
    )


AGSMARTSERVICE = ModuleConfig[AGSmartServiceConfig](
    default=AGSmartServiceConfig(enabled=False),
    kt_ag=AGSmartServiceConfig(
        enabled=env.bool("AGSMARTSERVICE_ENABLED", default=True)
    ),
)
