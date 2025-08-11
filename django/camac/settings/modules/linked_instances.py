from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.linked_instances_schema import LinkedInstancesConfig

LINKED_INSTANCES = ModuleConfig[LinkedInstancesConfig](
    default=LinkedInstancesConfig(enabled=True),
    kt_bern=LinkedInstancesConfig(enabled=False),
    kt_gr=LinkedInstancesConfig(enabled=True),
    kt_so=LinkedInstancesConfig(enabled=True),
    kt_uri=LinkedInstancesConfig(enabled=True),
    kt_schwyz=LinkedInstancesConfig(enabled=True),
    kt_ag=LinkedInstancesConfig(enabled=True),
)
