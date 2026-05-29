from camac.settings.ebau_schema import ModuleConfig
from camac.settings.env import env
from camac.settings.modules.gis_export_schema import GISExportConfig

GIS_EXPORT = ModuleConfig[GISExportConfig](
    default=GISExportConfig(),
    kt_so=GISExportConfig(
        enabled=True,
        keycloak_client=env.str("KEYCLOAK_SOGIS_CLIENT", default="sogis"),
    ),
)
