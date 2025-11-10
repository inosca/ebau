from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.deadlines_schema import CalculationConfig, DeadlinesConfig

DEADLINES = ModuleConfig[DeadlinesConfig](
    default=DeadlinesConfig(),
    kt_gr=DeadlinesConfig(
        enabled=False,
        calculation=CalculationConfig(
            exclude_weekends=False,
        ),
    ),
    kt_so=DeadlinesConfig(),
    kt_uri=DeadlinesConfig(),
    kt_schwyz=DeadlinesConfig(),
    kt_ag=DeadlinesConfig(
        enabled=True,
        calculation=CalculationConfig(
            exclude_weekends=False,
        ),
    ),
)
