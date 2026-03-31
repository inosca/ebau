from pydantic import Field

from camac.settings.ebau_schema import ModuleApplicationConfig, ModuleConfig


class ApplicantsConfig(ModuleApplicationConfig):
    applicant_identifier_question: str = Field(
        description="Caluma question slug used to identify an applicant per personal-table row",
        default="benutzer",
    )
    confirmation_question: str = Field(
        description="Caluma question slug used to save whether a document is confirmed",
        default="bestaetigung-komplett",
    )
    confirmation_answer: list[str] = Field(
        description="Answer for confirmation question",
        default_factory=lambda: ["bestaetigung-komplett-ja"],
    )


APPLICANTS = ModuleConfig[ApplicantsConfig](
    default=ApplicantsConfig(),
    kt_sg=ApplicantsConfig(enabled=True),
)
