from django.utils.translation import gettext_lazy as _

from camac.settings.modules.caluma_simple_workflow_schema import (
    CalumaSimpleWorkflowConfig,
    EventConfig,
)

SG_CALUMA_SIMPLE_WORKFLOW_SETTINGS = CalumaSimpleWorkflowConfig(
    enabled=True,
    events={
        "material-exam": {
            "completed": [
                EventConfig(
                    history_text=_("Material exam performed"),
                ),
            ],
        },
        "formal-exam": {
            "completed": [
                EventConfig(
                    next_instance_state="init-distribution",
                    history_text=_("Formal exam performed"),
                ),
            ],
        },
        "init-distribution": {
            "completed": [
                EventConfig(
                    next_instance_state="distribution",
                    history_text=_("Circulation started"),
                ),
            ],
        },
        "complete-distribution": {
            "completed": [
                EventConfig(
                    next_instance_state="decision",
                ),
            ],
        },
        "complete-construction-monitoring": {
            "completed": [
                EventConfig(
                    next_instance_state="to-finish",
                ),
            ],
        },
        "complete-instance": {
            "completed": [
                EventConfig(
                    next_instance_state="finished",
                    history_text=_("Procedure completed"),
                ),
            ],
        },
    },
)
