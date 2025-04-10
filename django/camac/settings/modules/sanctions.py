from pydantic import Field

from camac.settings.ebau_schema import ModuleApplicationConfig, ModuleConfig


class SanctionsConfig(ModuleApplicationConfig):
    available_service_groups: list[str] = Field(
        description=(
            "List of service group slugs. Services in the specified groups can be "
            "assigned sanctions. If unset/empty, all services can be assigned "
            "sanctions."
        ),
        default_factory=list,
    )


SANCTIONS = ModuleConfig[SanctionsConfig](
    default=SanctionsConfig(),
    kt_schwyz=SanctionsConfig(enabled=True),
    kt_uri=SanctionsConfig(
        enabled=True,
        available_service_groups=[
            # When adding a service group entry, make sure the slug is set on the
            # service group!
            "fachstellen-baudirektion",
            "fachstellen-justizdirektion",
        ],
    ),
)
