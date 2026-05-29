from pydantic import Field

from camac.settings.ebau_schema import ModuleApplicationConfig


class GISExportConfig(ModuleApplicationConfig):
    keycloak_client: str | None = Field(
        description="Name of the Keycloak client used for the SO GIS export API.",
        default="gis-client",
    )
