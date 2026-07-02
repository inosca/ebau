from typing import Any, Literal

from pydantic import Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig


class ProcedureTypeConfig(EBauConfig):
    enabled: bool = Field(
        description="Whether the procedure type field should be enabled for deadlines.",
        default=False,
    )
    task_id: str = Field(
        description="ID of the task which contains the question for procedure type.",
        default="formal-exam",
    )
    question_id: str = Field(
        description="Slug of the question that contains the answer for the procedure type.",
        default="verfahrensart",
    )
    value: str = Field(
        description="Value of the answer that indicates a simplified procedure.",
        default="verfahrensart-vereinfachtes-baubewilligungsverfahren",
    )


SuspensionReason = Literal[
    "additional_demand_suspension",  # required
    "incomplete_suspension",
    "inquiry_claim_suspension",  # required
    "request_project_change_suspension",
    "manual_suspension",  # required
]


class DeadlinesConfig(ModuleApplicationConfig):
    allowed_suspension_reasons: list[SuspensionReason] = [
        "additional_demand_suspension",
        "inquiry_claim_suspension",
        "manual_suspension",
    ]
    suspension_translation_overrides: dict[str, Any] = {}
    procedure_type: ProcedureTypeConfig = ProcedureTypeConfig()
