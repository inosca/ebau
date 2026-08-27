from typing import Literal, get_args

from pydantic import Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig

ResponsibleServiceType = Literal["municipality", "construction_control"]


class ChangeResponsibleServiceTypeConfig(EBauConfig):
    services_for_type: list[str] = Field(
        description="Applicable services for the responsible service type. Configured as a list of service slugs.",
        default=[],
    )
    service_groups_for_type: list[str] = Field(
        description="Applicable service groups for the responsible service type. Configured as a list of service group names.",
        default=[],
    )
    allowed_services_for_change_by_form: dict[str, list[str]] = Field(
        description="Services that are allowed to be selected as the new responsible service during the responsible service change. Can be configured by form slug or by a default key, if there are certain services that are allowed, regardless of the form. Configured as a dict with the unversioned form slug as key, and a list of service slugs as the value.",
        default={},
    )
    allowed_service_groups_for_change_by_form: dict[str, list[str]] = Field(
        description="Service groups whose services are allowed to be selected as the new responsible service during the responsible service change. Can be configured by form slug or by a default key, if there are certain service groups that are allowed, regardless of the form. Configured as a dict with the unversioned form slug as key, and a list of service group names as the value.",
        default={},
    )

    def get_allowed_services_for_change(
        self, form_slug: str | None = None
    ) -> list[str]:
        """Return the slugs of configured services for a specific form or the default as fallback."""

        default_fallback = self.allowed_services_for_change_by_form.get("default", [])
        return self.allowed_services_for_change_by_form.get(form_slug, default_fallback)

    def get_allowed_service_groups_for_change(
        self, form_slug: str | None = None
    ) -> list[str]:
        """Return the names of configured service groups for a specific form or the default as fallback."""

        default_fallback = self.allowed_service_groups_for_change_by_form.get(
            "default", []
        )
        return self.allowed_service_groups_for_change_by_form.get(
            form_slug, default_fallback
        )


class ChangeResponsibleServiceConfig(ModuleApplicationConfig):
    def responsible_service_types(self) -> list[ResponsibleServiceType]:
        """Return all configured responsible service types."""

        target_fields = get_args(ResponsibleServiceType)
        return [field for field in target_fields if getattr(self, field) is not None]

    def has_responsible_service_type_config(
        self, responsible_service_type: ResponsibleServiceType
    ) -> bool:
        """Check if a specific responsible service type is configured."""

        return responsible_service_type in self.responsible_service_types()

    def get_responsible_service_type_config(
        self, responsible_service_type: ResponsibleServiceType
    ) -> ChangeResponsibleServiceTypeConfig:
        """Return the configuration for a specific responsible service type."""

        if (
            responsible_service_type not in self.responsible_service_types()
        ):  # pragma: no cover
            raise ValueError(
                f"Invalid responsible service type '{responsible_service_type}'. Valid responsible service types are: {self.responsible_service_types()}"
            )

        return getattr(self, responsible_service_type)

    municipality: ChangeResponsibleServiceTypeConfig | None = Field(
        description="Configuration for the 'municipality' (lead authority) responsible service type.",
        default=None,
    )
    construction_control: ChangeResponsibleServiceTypeConfig | None = Field(
        description="Configuration for the 'construction_control' (construction control) responsible service type.",
        default=None,
    )
