from django.conf import settings
from django.core.management.commands import dumpdata

# TODO: once deployed on production this list
# needs to be reduced to tables which are not
# managed by customer

# Configuration models that do not have any foreign key relationships
# to non-config models (direct or indirect).
# These models can be safely deleted and re-imported anytime.
pure_config_models = (
    'core.ACheckquery',
    'core.ACirculationEmail',
    'core.ACirculationtransition',
    'core.ACopyanswer',
    'core.ACopyanswerMapping',
    'core.ACopydata',
    'core.ACopydataMapping',
    'core.Action',
    'core.ADeleteCirculation',
    'core.AEmail',
    'core.AFormtransition',
    'core.AirAction',
    'core.ALocation',
    'core.ALocationQc',
    'core.ANotice',
    'core.ANotification',
    'core.AnswerList',
    'core.APageredirect',
    'core.APhp',
    'core.AProposal',
    'core.AProposalHoliday',
    'core.ArAction',
    'core.ASavepdf',
    'core.AttachmentExtension',
    'core.AttachmentExtensionRole',
    'core.AttachmentExtensionService',
    'core.Authority',
    'core.AuthorityAuthorityType',
    'core.AuthorityLocation',
    'core.AuthorityType',
    'core.AvailableAction',
    'core.AvailableInstanceResource',
    'core.AvailableResource',
    'core.AValidate',
    'core.BGroupAcl',
    'core.BillingConfig',
    'core.BRoleAcl',
    'core.BServiceAcl',
    'core.BuildingAuthorityDoc',
    'core.BuildingAuthorityEmail',
    'core.Button',
    'core.ChapterPage',
    'core.ChapterPageGroupAcl',
    'core.ChapterPageRoleAcl',
    'core.ChapterPageServiceAcl',
    'core.CirculationReason',
    'core.DocgenActivationAction',
    'core.DocgenActivationactionAction',
    'core.DocgenDocxAction',
    'core.DocgenPdfAction',
    'core.DocgenTemplate',
    'core.DocgenTemplateClass',
    'core.FormGroup',
    'core.FormGroupForm',
    'core.InstanceResource',
    'core.InstanceResourceAction',
    'core.IrAllformpages',
    'core.IrCirculation',
    'core.IrEditcirculation',
    'core.IrEditcirculationSg',
    'core.IrEditformpage',
    'core.IrEditformpages',
    'core.IrEditletter',
    'core.IrEditletterAnswer',
    'core.IrEditnotice',
    'core.IrFormerror',
    'core.IrFormpage',
    'core.IrFormpages',
    'core.IrFormwizard',
    'core.IrGroupAcl',
    'core.IrLetter',
    'core.IrNewform',
    'core.IrPage',
    'core.IrRoleAcl',
    'core.IrServiceAcl',
    'core.Page',
    'core.PageAnswerActivation',
    'core.PageForm',
    'core.PageFormGroup',
    'core.PageFormGroupAcl',
    'core.PageFormMode',
    'core.PageFormRoleAcl',
    'core.PageFormServiceAcl',
    'core.PublicationSetting',
    'core.QuestionChapter',
    'core.QuestionChapterGroupAcl',
    'core.QuestionChapterRoleAcl',
    'core.QuestionChapterServiceAcl',
    'core.RApiListCirculationState',
    'core.RApiListCirculationType',
    'core.RApiListInstanceState',
    'core.Resource',
    'core.RFormlist',
    'core.RGroupAcl',
    'core.RList',
    'core.RListColumn',
    'core.RPage',
    'core.RRoleAcl',
    'core.RSearch',
    'core.RSearchColumn',
    'core.RSearchFilter',
    'core.RServiceAcl',
    'core.RSimpleList',
    'core.ServiceAnswerActivation',
    'core.TemplateGenerateAction',
    'core.WorkflowAction',
    'core.WorkflowRole',
    'document.AttachmentSectionRoleAcl',
    'document.AttachmentSectionServiceAcl',
    'document.Template',
    'notification.NotificationTemplate',
    'notification.NotificationTemplateT',
    'user.GroupLocation',
)

# List of models that have foreign keys referencing non-config tables
# (directly or indirectly). All models which are not in this list can
# be safely flushed and re-imported.
models_referencing_data = (
    'core.AnswerQuery',
    'core.BuildingAuthoritySection',
    'core.BuildingAuthorityButton',
    'core.Chapter',
    'core.CirculationAnswer',
    'core.CirculationAnswerType',
    'core.CirculationState',
    'core.CirculationType',
    'core.Mapping',
    'core.NoticeType',
    'core.Question',
    'core.QuestionType',
    'core.WorkflowItem',
    'core.WorkflowSection',
    'document.AttachmentSection',
    'instance.Form',
    'instance.FormState',
    'instance.InstanceState',
    'instance.InstanceStateDescription',
    'user.Group',
    'user.Location',
    'user.Role',
    'user.Service',
    'user.ServiceGroup',
)


class Command(dumpdata.Command):
    help = (
        "Output the camac configuration of the database as a fixture of the "
        " given format."
    )

    def handle(self, *app_labels, **options):
        options['indent'] = 2
        options['output'] = (
            options.get('output') or settings.APPLICATION_DIR('config.json')
        )
        super().handle(
            *(pure_config_models + models_referencing_data),
            **options
        )
