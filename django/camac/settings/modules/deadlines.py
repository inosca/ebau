from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.deadlines_schema import DeadlinesConfig

DEADLINES = ModuleConfig[DeadlinesConfig](
    default=DeadlinesConfig(),
    kt_gr=DeadlinesConfig(enabled=True),
    kt_so=DeadlinesConfig(),
    kt_uri=DeadlinesConfig(),
    kt_schwyz=DeadlinesConfig(),
    kt_ag=DeadlinesConfig(),
)
