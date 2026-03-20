from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.timelines_schema import TimelinesConfig

TIMELINES = ModuleConfig[TimelinesConfig](
    default=TimelinesConfig(),
    kt_gr=TimelinesConfig(enabled=True),
)
