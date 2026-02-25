from pydantic import Field

from camac.settings.ebau_schema import ModuleApplicationConfig


class TagsConfig(ModuleApplicationConfig):
    use_legacy_tags: bool = Field(
        default=False,
        description="Use the legacy Tags model instead of the newer Keywords model.",
    )
