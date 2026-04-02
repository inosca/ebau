from typing import Any

from pydantic import ConfigDict, Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig


class ExportColumnsConfig(EBauConfig):
    """Column definitions for a single export type; each entry is an (annotation_name, label) tuple."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    dossiers: list[tuple[str, Any]] = Field(
        description=("Columns for the dossier export."),
        default_factory=list,
    )
    work_items: list[tuple[str, Any]] = Field(
        description=("Columns for the work-item export."),
        default_factory=list,
    )


class StatisticsConfig(ModuleApplicationConfig):
    """Statistics XLSX export config; resolution order: by_service_group → by_role."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    by_role: dict[str, ExportColumnsConfig] = Field(
        description="Column overrides keyed by Role.slug.",
        default_factory=dict,
    )
    by_service_group: dict[str, ExportColumnsConfig] = Field(
        description="Column overrides keyed by ServiceGroup.slug. Takes priority over by_role.",
        default_factory=dict,
    )
