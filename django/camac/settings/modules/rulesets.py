from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.rulesets_schema import (
    AvailableServicesRuleConfig,
    DistributionDeadlineRuleConfig,
    ResponsibleUserRuleConfig,
    RulesetsConfig,
)

AG_ADMIN_ROLES = [
    "municipality-admin",
    "service-admin",
    "trusted-service-admin",
]

RULESETS = ModuleConfig[RulesetsConfig](
    default=RulesetsConfig(),
    kt_ag=RulesetsConfig(
        enabled=True,
        responsible_user_rule=ResponsibleUserRuleConfig(
            allowed_roles=AG_ADMIN_ROLES,
            ignored_access_levels=["read"],
        ),
        distribution_deadline_rule=DistributionDeadlineRuleConfig(
            exclude_holidays_for_service_groups=["service-afb", "service-cantonal"],
            allowed_roles=AG_ADMIN_ROLES,
        ),
        available_services_rule=AvailableServicesRuleConfig(
            service_configurations={
                "service-afb": ["service-cantonal", "service-external"],
                "municipality": ["subservice"],
            }
        ),
    ),
)
