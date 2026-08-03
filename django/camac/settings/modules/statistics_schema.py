from django.utils.functional import Promise
from pydantic import ConfigDict, Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig

type ColumnLabel = str | Promise


class ExportColumnsConfig(EBauConfig):
    """Column definitions for a single export type; each entry is an (annotation_name, label) tuple."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    dossiers: list[tuple[str, ColumnLabel]] = Field(
        description=("Columns for the dossier export."),
        default_factory=list,
    )
    work_items: list[tuple[str, ColumnLabel]] = Field(
        description=("Columns for the work-item export."),
        default_factory=list,
    )
    rpg2_dossiers: list[tuple[str, ColumnLabel]] = Field(
        description=("Columns for the RPG2 export (one row per dossier)."),
        default_factory=list,
    )
    rpg2_areas: list[tuple[str, ColumnLabel]] = Field(
        description=(
            "Columns for the RPG2 areas sheet (one row per sealed/unsealed area)."
        ),
        default_factory=list,
    )


class StatisticsConfig(ModuleApplicationConfig):
    """Statistics XLSX export config; resolution order: by_service_group → by_role."""

    slugs: dict[str, str] = Field(
        description=(
            "Caluma question/option slugs used by the exports (e.g. RPG2). "
            "Override per canton when different slugs are in use."
        ),
        default_factory=dict,
    )
    by_role: dict[str, ExportColumnsConfig] = Field(
        description="Column overrides keyed by Role.slug.",
        default_factory=dict,
    )
    by_service_group: dict[str, ExportColumnsConfig] = Field(
        description="Column overrides keyed by ServiceGroup.slug. Takes priority over by_role.",
        default_factory=dict,
    )
