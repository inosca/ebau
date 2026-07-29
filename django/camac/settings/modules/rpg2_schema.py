from pydantic import Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig


class ImportMappingEntry(EBauConfig):
    """One target to source mapping for the rpg2 import flow."""

    source_slugs: list[str] = Field(
        description="Versioned source slugs of questions from the main form or another source form. "
        "Whenever bumping the version of the source slug, the new version slug needs to be added to this list. "
        "Same behaviour as MasterData (via _get_first_field_from_lookup_list)",
    )
    from_work_item: str | None = Field(
        default=None,
        description="Slug of the work item whose document holds the source question. If omitted, the source is the main form document",
    )
    transform: str | None = Field(
        default=None, description="Name of the transform method"
    )
    row_mapping: dict[str, "ImportMappingEntry"] = Field(
        default_factory=dict,
        description="For TABLE targets only. Keys are target column question slugs on the rpg2 table, values are nested ImportMappingEntry instances",
    )
    is_option_target: bool = Field(
        default=False,
        description="Set True when the target is a choice question."
        "Keep False for other types of targets (integer, text etc.). "
        "For TABLE targets, set per column in row_mapping.",
    )


class RPG2Config(ModuleApplicationConfig):
    task: str = Field(
        default="rpg2",
        description="Slug of the caluma task for the rpg2 work item",
    )
    form: str = Field(
        default="rpg2",
        description="Slug of the caluma form for the rpg2 document.",
    )
    service_slugs: list[str] = Field(
        description="Service slugs of the services that trigger the creation of rpg2 work item via inquiry.",
        default_factory=list,
    )
    allowed_forms: list[str] = Field(
        description="Unversioned main form slugs for which the rpg2 work item is created via inquiry.",
        default_factory=list,
    )
    import_mapping: dict[str, ImportMappingEntry] = Field(
        default_factory=dict,
        description="Target rpg2 question slug to source config mapping. The order of the target questions in the mapping determines the preview order",
    )
