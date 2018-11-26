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
pure_config_models = (
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
    "core.BGroupAcl",
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
    "core.InstanceResource",
    "core.InstanceResourceT",
    "core.InstanceResourceAction",
    "core.IrAllformpages",
    "core.IrCirculation",
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
    # journal
    "core.JournalActionConfig",
    "core.JournalActionConfigT",
    "core.TemplateGenerateAction",
    "core.WorkflowAction",
    "core.WorkflowRole",
    "document.AttachmentSectionRoleAcl",
    "document.AttachmentSectionServiceAcl",
    "document.Template",
    "notification.NotificationTemplate",
    "notification.NotificationTemplateT",
    "responsible.IrEditresponsibleuser",
    "responsible.IrEditresponsiblegroup",
    "responsible.ASetresponsiblegroup",
    "responsible.ResponsibleServiceAllocation",
    # officeexporter
    "officeexporter.OfficeExporterDocx",
    "officeexporter.OfficeExporterDocxT",
    "officeexporter.OfficeExporterDocxRole",
)

# List of models that have foreign keys referencing non-config tables
# (directly or indirectly). All models which are not in this list can
# be safely flushed and re-imported.
models_referencing_data = (
    "core.AnswerQuery",
    "core.BuildingAuthoritySection",
    "core.BuildingAuthorityButton",
    "core.Chapter",
    "core.CirculationAnswer",
    "core.CirculationAnswerType",
    "core.CirculationState",
    "core.CirculationType",
    "core.Mapping",
    "core.NoticeType",
    "core.Question",
    "core.QuestionT",
    "core.QuestionType",
    "core.WorkflowItem",
    "core.WorkflowSection",
    "document.AttachmentSection",
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
    "user.ServiceGroup",
    "user.ServiceGroupT",
)


class Command(BaseCommand):
    help = (
        "Output the camac configuration of the database as a fixture of the "
        " given format."
    )

    def handle(self, *app_labels, **options):
        options["indent"] = 2

        try:
            output = options.pop("output")
        except KeyError:  # pragma: no cover
            output = settings.APPLICATION_DIR("config.json")
        tmp_output = io.StringIO()
        options["stdout"] = tmp_output
        call_command(
            "dumpdata", *(pure_config_models + models_referencing_data), **options
        )
        tmp_output.seek(0)
        data = json.load(tmp_output)
        data = sorted(data, key=lambda k: (k["model"], k["pk"]))

        with open(output, "w") as f:
            json.dump(data, f, indent=2, sort_keys=True)
            f.flush()
