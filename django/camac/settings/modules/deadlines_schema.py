from typing import Any, Literal

from camac.settings.ebau_schema import ModuleApplicationConfig

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
