from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.tags_schema import TagsConfig

TAGS = ModuleConfig[TagsConfig](
    default=TagsConfig(enabled=True),
    kt_bern=TagsConfig(enabled=True, use_legacy_tags=True),
)
