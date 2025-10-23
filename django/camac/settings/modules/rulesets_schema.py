from pydantic import Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig


class ResponsibleUserRuleConfig(EBauConfig):
    automatically_assign: bool = Field(
        description="If enabled, responsible users defined in the module will be assigned automatically",
        default=True,
    )
    allowed_roles: list[str] = Field(
        description="Roles that are allowed to create responsible user rules.",
        default_factory=list,
    )
    ignored_access_levels: list[str] = Field(
        description="Access levels for which no responsible users will be assigned automatically",
        default_factory=list,
    )


class DistributionDeadlineRuleConfig(EBauConfig):
    exclude_holidays_for_service_groups: list[str] = Field(
        description="Service groups for which public holidays will be excluded from the calculated deadline.",
        default_factory=list,
    )
    allowed_roles: list[str] = Field(
        description="Roles that are allowed to create distribution deadline rules.",
        default_factory=list,
    )


class AvailableServicesRuleConfig(EBauConfig):
    """Configuration for available services in rulesets."""

    service_configurations: dict[str, list[str]] = Field(
        description="Dictionary mapping service keys to arrays of service groups that are available for that service.",
        default_factory=dict,
    )


class RulesetsConfig(ModuleApplicationConfig):
    """Configuration of the rulesets module."""

    responsible_user_rule: ResponsibleUserRuleConfig = ResponsibleUserRuleConfig()
    distribution_deadline_rule: DistributionDeadlineRuleConfig = (
        DistributionDeadlineRuleConfig()
    )
    available_services_rule: AvailableServicesRuleConfig = AvailableServicesRuleConfig()
    municipality_service_groups: list[str] = Field(
        description="List of service group names that contain municipalities, typically just 'municipality'.",
        default=["municipality"],
    )
