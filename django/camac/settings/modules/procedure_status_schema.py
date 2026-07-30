from typing import Self

from pydantic import Field, model_validator

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig


class StepMapping(EBauConfig):
    step: str = Field(description="Active timeline step for this instance state.")
    done: bool = Field(
        default=False,
        description=(
            "Whether the active step is `done` rather than `running`. "
            "Preceding steps are `done`, following ones `pending`."
        ),
    )


class ProcedureStatusConfig(ModuleApplicationConfig):
    steps: list[str] = Field(
        default_factory=list,
        description="Timeline steps in chronological order.",
    )
    instance_state_map: dict[str, StepMapping] = Field(
        default_factory=dict,
        description="Maps each instance state name to its timeline step mapping.",
    )

    @model_validator(mode="after")
    def validate_instance_state_map(self) -> Self:
        final_step = self.steps[-1] if self.steps else None

        for instance_state, mapping in self.instance_state_map.items():
            if mapping.step not in self.steps:
                raise ValueError(
                    f"Instance state '{instance_state}' maps to unknown step "
                    f"'{mapping.step}'."
                )

            # A `done` step has no following `running` step, so it only makes
            # sense for the final step (e.g. a rejected or finished dossier)
            if mapping.done and mapping.step != final_step:
                raise ValueError(
                    f"Instance state '{instance_state}' maps to non-final step "
                    f"'{mapping.step}' but is marked as done."
                )

        return self
