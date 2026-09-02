from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.change_responsible_service_schema import (
    ChangeResponsibleServiceConfig,
    ChangeResponsibleServiceTypeConfig,
)

CHANGE_RESPONSIBLE_SERVICE = ModuleConfig[ChangeResponsibleServiceConfig](
    default=ChangeResponsibleServiceConfig(),
    kt_bern=ChangeResponsibleServiceConfig(
        enabled=True,
        municipality=ChangeResponsibleServiceTypeConfig(
            services_for_type=["agr-bauen"],
            service_groups_for_type=["municipality", "district", "lead-service"],
            allowed_services_for_change_by_form={
                "antrag-auf-auszahlung": ["agr-bauen"]
            },
            allowed_service_groups_for_change_by_form={
                "default": ["municipality", "district", "lead-service"]
            },
        ),
        construction_control=ChangeResponsibleServiceTypeConfig(
            service_groups_for_type=["construction-control"],
            allowed_service_groups_for_change_by_form={
                "default": ["construction-control"]
            },
        ),
    ),
    kt_ag=ChangeResponsibleServiceConfig(
        enabled=True,
        municipality=ChangeResponsibleServiceTypeConfig(
            service_groups_for_type=[
                "municipality",
                "municipality-light",
                "service-afb",
            ],
            allowed_service_groups_for_change_by_form={
                "auszahlung-abbruchpraemie": ["service-afb"]
            },
        ),
    ),
)
