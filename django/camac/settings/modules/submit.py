from pydantic import Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig, ModuleConfig


class SubmitButtonConfig(EBauConfig):
    question_submit: str = Field(
        description="Question slug of the submit button that will be answered on submit",
        default="einreichen-button",
    )
    question_report: str = Field(
        description="Question slug of the submit button that will be answered on report (SB1)",
        default="einreichen-button-sb1",
    )
    question_finalize: str = Field(
        description="Question slug of the submit button that will be answered on finalize (SB2)",
        default="einreichen-button-sb2",
    )


class SubmitConfig(ModuleApplicationConfig):
    enabled: bool = True
    button: SubmitButtonConfig = SubmitButtonConfig()


# TODO: There are lots of settings that would actually belong in this module,
# but are currently still in the application settings. We'll need to migrate
# those piece by piece in order to make it viable - migrating everything now is
# out of scope.
#
# Examples of settings that could be migrated here:
# - STORE_PDF
# - COPY_RESPONSIBLE_PERSON_ON_SUBMIT
# - GENERATE_IDENTIFIER
# - ...
SUBMIT = ModuleConfig[SubmitConfig](
    # This module needs to be enabled for all cantons which is why we explicitly
    # added it for every canton here.
    default=SubmitConfig(),
    demo=SubmitConfig(),
    test=SubmitConfig(),
    kt_schwyz=SubmitConfig(),
    kt_bern=SubmitConfig(),
    kt_so=SubmitConfig(),
    kt_uri=SubmitConfig(),
    kt_gr=SubmitConfig(),
    kt_ag=SubmitConfig(),
    kt_sg=SubmitConfig(),
)
