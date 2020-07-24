import io
import json

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

# TODO: once deployed on production this list
# needs to be reduced to tables which are not
# managed by customer

# Configuration models that do not have any foreign key relationships
# to non-config models (direct or indirect).
# These models can be safely deleted and re-imported anytime.
pure_config_models = [
    "core.ACheckquery",
    "core.ACirculationEmail",
    "core.ACirculationEmailT",
    "core.ACirculationtransition",
    "core.ACopyanswer",
    "core.ACopyanswerMapping",
    "core.ACopydata",
    "core.ACopydataMapping",
    "core.Action",
    "core.ActionT",
    "core.ADeleteCirculation",
    "core.AEmail",
    "core.AEmailT",
    "core.AFormtransition",
    "core.AirAction",
    "core.ALocation",
    "core.ALocationQc",
    "core.ANotice",
    "core.ANotification",
    "core.AnswerList",
    "core.APageredirect",
    "core.APhp",
    "core.AProposal",
    "core.AProposalT",
    "core.AProposalHoliday",
    "core.ArAction",
    "core.ASavepdf",
    "core.AttachmentExtension",
    "core.AttachmentExtensionRole",
    "core.AttachmentExtensionService",
    "core.Authority",
    "core.AuthorityAuthorityType",
    "core.AuthorityLocation",
    "core.AuthorityType",
    "core.AnswerListT",
    "core.AvailableAction",
    "core.AvailableInstanceResource",
    "core.AvailableResource",
    "core.AValidate",
    "core.BillingConfig",
    "core.BRoleAcl",
    "core.BServiceAcl",
    "core.BuildingAuthorityDoc",
    "core.BuildingAuthorityEmail",
    "core.Button",
    "core.ButtonT",
    "core.ChapterT",
    "core.ChapterPage",
    "core.ChapterPageGroupAcl",
    "core.ChapterPageRoleAcl",
    "core.ChapterPageServiceAcl",
    "core.CirculationAnswerT",
    "core.CirculationAnswerTypeT",
    "core.CirculationReason",
    "core.DocgenActivationAction",
    "core.DocgenActivationactionAction",
    "core.DocgenDocxAction",
    "core.DocgenPdfAction",
    "core.DocgenTemplate",
    "core.DocgenTemplateClass",
    "core.CirculationStateT",
    "core.CirculationTypeT",
    "core.FormGroup",
    "core.FormGroupT",
    "core.FormGroupForm",
    "core.GroupPermission",
    "core.InstanceResource",
    "core.InstanceResourceT",
    "core.InstanceResourceAction",
    "core.IrAllformpages",
    "core.IrEditcirculation",
    "core.IrEditcirculationT",
    "core.IrEditcirculationSg",
    "core.IrEditformpage",
    "core.IrEditformpages",
    "core.IrEditletter",
    "core.IrEditletterAnswer",
    "core.IrEditletterAnswerT",
    "core.IrEditnotice",
    "core.IrFormerror",
    "core.IrFormpage",
    "core.IrFormpages",
    "core.IrFormwizard",
    "core.IrFormwizardT",
    "core.IrGroupAcl",
    "core.IrLetter",
    "core.IrNewform",
    "core.IrPage",
    "core.IrRoleAcl",
    "core.IrServiceAcl",
    "core.Municipality",
    "core.NoticeTypeT",
    "core.Page",
    "core.PageT",
    "core.PageAnswerActivation",
    "core.PageForm",
    "core.PageFormGroup",
    "core.PageFormGroupT",
    "core.PageFormGroupAcl",
    "core.PageFormMode",
    "core.PageFormRoleAcl",
    "core.PageFormServiceAcl",
    "core.PublicationSetting",
    "core.QuestionChapter",
    "core.QuestionChapterGroupAcl",
    "core.QuestionChapterRoleAcl",
    "core.QuestionChapterServiceAcl",
    "core.RApiListCirculationState",
    "core.RApiListCirculationType",
    "core.RApiListInstanceState",
    "core.Resource",
    "core.ResourceT",
    "core.RFormlist",
    "core.RGroupAcl",
    "core.RList",
    "core.RListColumn",
    "core.RListColumnT",
    "core.RPage",
    "core.RRoleAcl",
    "core.RSearch",
    "core.RSearchColumn",
    "core.RSearchColumnT",
    "core.RSearchFilter",
    "core.RSearchFilterT",
    "core.RServiceAcl",
    "core.RSimpleList",
    "core.RCalumaList",
    "core.ServiceAnswerActivation",
    # file
    "file.AFilecheckcontent",
    "file.AFilesavepdf",
    "file.AFilesavepdfContentpage",
    "file.AFilesavepdfT",
    "file.AFilesdownload",
    "file.AFilesdownloadContent",
    "file.AFiletransition",
    "file.AFiletransitionDate",
    "file.FileComplementStateT",
    "file.FileContentCategoryT",
    "file.FileContentForm",
    "file.FileContentMimeType",
    "file.FileContentRequired",
    "file.FileContentT",
    "file.FileFormat",
    "file.FileFormatT",
    "file.FileMimeType",
    "file.FileValidationType",
    "file.FileValidationTypeT",
    "file.IrFilecomplementanswer",
    "file.IrFilecomplementrequest",
    "file.IrFilecomplementreqCc",
    "file.IrFilelist",
    "file.IrFileupload",
    "file.IrFileuploadCc",
    "file.IrFilevalidation",
    "file.IrFileAccessType",
    "core.TemplateGenerateAction",
    "core.WorkflowAction",
    "core.WorkflowRole",
    "document.AttachmentSectionRoleAcl",
    "document.AttachmentSectionServiceAcl",
    "responsible.IrEditresponsibleuser",
    "responsible.IrEditresponsiblegroup",
    "responsible.ASetresponsiblegroup",
    "responsible.ResponsibleServiceAllocation",
    # history
    "core.HistoryActionConfig",
    "core.HistoryActionConfigT",
    # work item action
    "core.ActionWorkitem",
]

# List of models that have foreign keys referencing non-config tables
# (directly or indirectly). All models which are not in this list can
# be safely flushed and re-imported.
models_referencing_data = [
    "core.AnswerQuery",
    "core.BGroupAcl",
    "core.BuildingAuthoritySection",
    "core.BuildingAuthorityButton",
    "core.Chapter",
    "core.CirculationAnswer",
    "core.CirculationAnswerType",
    "core.CirculationState",
    "core.CirculationType",
    "core.IrCirculation",
    "core.Mapping",
    "core.NoticeType",
    "core.PublicationType",
    "core.Question",
    "core.QuestionT",
    "core.QuestionType",
    "core.WorkflowItem",
    "core.WorkflowSection",
    "document.AttachmentSection",
    "document.AttachmentSectionT",
    "document.Template",
    "file.FileComplementState",
    "file.FileContent",
    "file.FileContentCategory",
    "instance.Form",
    "instance.FormT",
    "instance.FormState",
    "instance.InstanceState",
    "instance.InstanceStateT",
    "instance.InstanceStateDescription",
    "user.Group",
    "user.GroupT",
    "user.GroupLocation",
    "user.Location",
    "user.LocationT",
    "user.Role",
    "user.RoleT",
    "user.Service",
    "user.ServiceT",
    "user.ServiceGroup",
    "user.ServiceGroupT",
    "notification.NotificationTemplate",
    "notification.NotificationTemplateT",
]

pure_config_models_caluma_form = []
models_referencing_data_caluma_form = [
    "caluma_form.Option",
    "caluma_form.Question",
    "caluma_form.Form",
    "caluma_form.QuestionOption",
    "caluma_form.FormQuestion",
    "caluma_form.HistoricalOption",
    "caluma_form.HistoricalQuestion",
    "caluma_form.HistoricalForm",
    "caluma_form.HistoricalQuestionOption",
    "caluma_form.HistoricalFormQuestion",
]

pure_config_models_caluma_workflow = []
models_referencing_data_caluma_workflow = [
    "caluma_workflow.Workflow",
    "caluma_workflow.Task",
    "caluma_workflow.TaskFlow",
    "caluma_workflow.Flow",
    "caluma_workflow.HistoricalWorkflow",
    "caluma_workflow.HistoricalTask",
    "caluma_workflow.HistoricalTaskFlow",
    "caluma_workflow.HistoricalFlow",
]

# exclude models which are managed by the customer alone from sync
models_managed_by_customer = {
    "kt_schwyz": [
        "document.Template",
        "user.Group",
        "user.GroupT",
        "user.GroupLocation",
        "user.Service",
        "user.ServiceT",
        "notification.NotificationTemplate",
        "notification.NotificationTemplateT",
    ],
    "kt_bern": [
        "user.Group",
        "user.GroupT",
        "user.GroupLocation",
        "user.Service",
        "user.ServiceT",
        "notification.NotificationTemplate",
        "notification.NotificationTemplateT",
    ],
    "kt_uri": [],
    "demo": [],
}


class Command(BaseCommand):
    help = (
        "Output the camac configuration of the database as a fixture of the "
        " given format."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default=settings.APPLICATION_DIR("config.json"),
            help="Output file for camac config",
        )
        parser.add_argument(
            "--output-caluma-form",
            dest="output_caluma_form",
            type=str,
            default=settings.APPLICATION_DIR("config-caluma-form.json"),
            help="Output file for caluma form config",
        )
        parser.add_argument(
            "--output-caluma-workflow",
            dest="output_caluma_workflow",
            type=str,
            default=settings.APPLICATION_DIR("config-caluma-workflow.json"),
            help="Output file for caluma workflow config",
        )

        parser.add_argument(
            "--caluma",
            dest="caluma",
            action="store_true",
            help="Dump caluma config as well",
        )
        parser.add_argument(
            "--no-caluma",
            dest="caluma",
            action="store_false",
            help="Don't dump caluma config",
        )

        parser.set_defaults(caluma=settings.APPLICATION.get("FORM_BACKEND") == "caluma")

    def dump_config(self, export_models, output):
        tmp_output = io.StringIO()
        call_command("dumpdata", *export_models, indent=2, stdout=tmp_output)
        tmp_output.seek(0)
        data = json.load(tmp_output)
        data = sorted(data, key=lambda k: (k["model"], k["pk"]))

        with open(output, "w") as f:
            json.dump(data, f, indent=2, sort_keys=True)
            f.flush()

    def handle(self, *app_labels, **options):
        self.dump_config(
            [
                m
                for m in pure_config_models + models_referencing_data
                if m not in models_managed_by_customer[settings.APPLICATION_NAME]
            ],
            options["output"],
        )

        if options["caluma"]:
            self.dump_config(
                pure_config_models_caluma_form + models_referencing_data_caluma_form,
                options["output_caluma_form"],
            )
            self.dump_config(
                pure_config_models_caluma_workflow
                + models_referencing_data_caluma_workflow,
                options["output_caluma_workflow"],
            )
