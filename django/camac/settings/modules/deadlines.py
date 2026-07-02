from django.utils.translation import gettext_lazy as _

from camac.settings.ebau_schema import ModuleConfig
from camac.settings.env import env
from camac.settings.modules.deadlines_schema import DeadlinesConfig, ProcedureTypeConfig

DEADLINES = ModuleConfig[DeadlinesConfig](
    default=DeadlinesConfig(),
    kt_gr=DeadlinesConfig(
        enabled=env.bool("DEADLINES_ENABLED", default=False),
        allowed_suspension_reasons=[
            "additional_demand_suspension",
            "incomplete_suspension",
            "inquiry_claim_suspension",
            "request_project_change_suspension",
            "manual_suspension",
        ],
        suspension_translation_overrides={
            "additional_demand_suspension": _("Additional demand"),
            "inquiry_claim_suspension": _("Negative inquiry claim suspension"),
            "manual_suspension": _("Other suspension"),
        },
        procedure_type=ProcedureTypeConfig(enabled=True),
    ),
    kt_ag=DeadlinesConfig(enabled=True),
)
