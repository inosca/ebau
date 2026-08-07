from django.utils.translation import gettext_lazy as _

from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.statistics_schema import (
    ExportColumnsConfig,
    StatisticsConfig,
)

DEFAULT_DOSSIER_COLUMNS = [
    ("dossier_number", _("Instance number")),
    ("form_name", _("Application Type")),
    ("parcels", _("Parcels")),
    ("submit_date", _("Submission Date")),
    ("responsible_user", _("Responsible")),
    ("municipality", _("Municipality")),
]

DEFAULT_WORK_ITEM_COLUMNS = [
    ("task_name", _("Task name")),
    ("wi_created_at", _("Created at")),
    ("wi_deadline", _("Deadline")),
    ("wi_closed_at", _("Closed at")),
    ("wi_assigned_user", _("Assigned user")),
    ("wi_addressed_group", _("Addressed group")),
    ("wi_status", _("Status")),
    ("wi_processing_time", _("Processing time")),
    ("wi_on_time", _("On time")),
]

DEFAULT_RPG2_DOSSIER_COLUMNS = [
    ("dossier_number", _("Instance number")),
    ("form_name", _("Application Type")),
    ("rpg2_legal_basis", _("Legal basis RPG / RPV")),
    ("rpg2_new_buildings", _("Number of new buildings > 6 m²")),
    ("rpg2_demolished_buildings", _("Number of demolished buildings > 6 m²")),
    ("rpg2_protected_buildings", _("Number of newly protected buildings > 6 m²")),
    ("rpg2_approved", _("Approved")),
    ("rpg2_positive_afb", _("Positive AfB assessment")),
    ("rpg2_realized", _("Realized")),
    ("coordinate_x", _("X coordinate")),
    ("coordinate_y", _("Y coordinate")),
]

DEFAULT_RPG2_AREAS_COLUMNS = [
    ("dossier_number", _("Instance number")),
    ("ebau_number", _("eBau number")),
    ("area_type", _("Type of sealing / unsealing")),
    ("area_size", _("Area (m²)")),
    (
        "area_materialization",
        _("Materialisierung der neu ver- bzw. entsiegelten Flächen"),
    ),
    ("area_materialization_description", _("Beschreibung Materialisierung")),
    ("area_usage", _("Usage of sealed areas")),
    ("area_sealed_when", _("When was the area sealed")),
]

AG_SERVICE_DOSSIER_COLUMNS = [
    *DEFAULT_DOSSIER_COLUMNS,
    ("processing_time", _("Processing time")),
    ("first_inquiry_date", _("First inquiry date")),
    ("completing_date", _("Completing date")),
    ("on_time", _("On time")),
]

AG_SERVICE_WORK_ITEM_COLUMNS = [
    *DEFAULT_DOSSIER_COLUMNS,
    *DEFAULT_WORK_ITEM_COLUMNS,
]

AG_SERVICE_COLUMN_CONFIG = ExportColumnsConfig(
    dossiers=AG_SERVICE_DOSSIER_COLUMNS,
    work_items=AG_SERVICE_WORK_ITEM_COLUMNS,
)

AG_AFB_COLUMN_CONFIG = ExportColumnsConfig(
    dossiers=AG_SERVICE_DOSSIER_COLUMNS,
    work_items=AG_SERVICE_WORK_ITEM_COLUMNS,
    rpg2_dossiers=DEFAULT_RPG2_DOSSIER_COLUMNS,
    rpg2_areas=DEFAULT_RPG2_AREAS_COLUMNS,
)

DEFAULT_SLUGS = {
    "gis_coordinates": "gis-map",
    "rpg2_legal_basis": "rpg2-bewilligungsgrund",
    "rpg2_new_buildings": "rpg2-anzahl-neue-gebaeude",
    "rpg2_demolished_buildings": "rpg2-anzahl-gebaeude-abbruch",
    "rpg2_protected_buildings": "rpg2-anzahl-gebaeude-unter-schutz",
    "rpg2_realized": "rpg2-realisiert",
    "rpg2_realized_no": "rpg2-realisiert-nein",
    "rpg2_sealing": "rpg2-versiegelt-oder-entsiegelt",
    "rpg2_sealing_yes": "rpg2-versiegelt-oder-entsiegelt-ja",
    "rpg2_areas_table": "rpg2-versiegelte-entsiegelte-flaechen",
    "rpg2_area_type": "rpg2-art-versiegelung-entsiegelung",
    "rpg2_area_size": "rpg2-flaeche-quadrat-meter",
    "rpg2_area_materialization": "rpg2-materialisierung-neu-versiegelten-flaechen",
    "rpg2_area_materialization_description": "rpg2-materialisierung-neu-versiegelten-flaechen-beschreibung",
    "rpg2_area_usage": "rpg2-nutzung-versiegelten-flaechen",
    "rpg2_area_sealed_when": "rpg2-wann-wurde-flaeche-versiegelt",
    "rpg2_area_unsealed_prefix": "rpg2-art-versiegelung-entsiegelung-entsiegelte-renaturierte-flaechen",
}

STATISTICS = ModuleConfig[StatisticsConfig](
    default=StatisticsConfig(
        enabled=False,
        slugs=DEFAULT_SLUGS,
    ),
    kt_ag=StatisticsConfig(
        enabled=True,
        slugs=DEFAULT_SLUGS,
        by_service_group={
            "service-afb": AG_AFB_COLUMN_CONFIG,
            "service-external": AG_SERVICE_COLUMN_CONFIG,
            "service-cantonal": AG_SERVICE_COLUMN_CONFIG,
            "municipality": ExportColumnsConfig(
                dossiers=[
                    *DEFAULT_DOSSIER_COLUMNS,
                    ("processing_time", _("Processing time")),
                ],
            ),
        },
    ),
)
