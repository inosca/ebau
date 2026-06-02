from pydantic import Field

from camac.settings.ebau_schema import ModuleApplicationConfig


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
