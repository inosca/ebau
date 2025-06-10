from pydantic import Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig


class CalculationConfig(EBauConfig):
    exclude_weekends: bool = Field(
        description="Exclude weekends when calculating deadlines.",
        default=True,
    )
    exclude_public_holidays: bool = Field(
        description="Exclude public holidays when calculating deadlines.",
        default=True,
    )


class DeadlinesConfig(ModuleApplicationConfig):
    enabled: bool = Field(
        description="Enable the deadlines module.",
        default=False,
    )
    calculation: CalculationConfig = CalculationConfig()
