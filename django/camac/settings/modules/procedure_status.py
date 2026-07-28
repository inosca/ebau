from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.procedure_status_schema import (
    ProcedureStatusConfig,
    StepMapping,
)

PROCEDURE_STATUS = ModuleConfig[ProcedureStatusConfig](
    default=ProcedureStatusConfig(),
    kt_sg=ProcedureStatusConfig(
        enabled=True,
        steps=[
            "submit",
            "exam",
            "distribution",
            "decision",
            "construction-monitoring",
            "finish",
        ],
        instance_state_map={
            "new": StepMapping(step="submit"),
            "subm": StepMapping(step="exam"),
            "init-distribution": StepMapping(step="distribution"),
            "distribution": StepMapping(step="distribution"),
            "decision": StepMapping(step="decision"),
            "decided": StepMapping(step="decision"),
            "construction-monitoring": StepMapping(step="construction-monitoring"),
            "to-finish": StepMapping(step="finish"),
            "finished": StepMapping(step="finish", done=True),
            "rejected": StepMapping(step="finish", done=True),
        },
    ),
)
