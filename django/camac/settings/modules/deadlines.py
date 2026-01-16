from camac.settings.ebau_schema import ModuleConfig
from camac.settings.env import env
from camac.settings.modules.deadlines_schema import DeadlinesConfig

DEADLINES = ModuleConfig[DeadlinesConfig](
    default=DeadlinesConfig(),
    kt_gr=DeadlinesConfig(enabled=env.bool("DEADLINES_ENABLED", default=False)),
    kt_so=DeadlinesConfig(enabled=True),
    kt_uri=DeadlinesConfig(),
    kt_schwyz=DeadlinesConfig(),
    kt_ag=DeadlinesConfig(enabled=True),
)
