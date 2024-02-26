from django.db.models.expressions import Q


def generate_form_dump_config(regex=None, version=None):
    if regex:
        return {
            "caluma_form.Option": Q(questions__forms__pk__iregex=regex),
            "caluma_form.Question": Q(forms__pk__iregex=regex),
            "caluma_form.Form": Q(pk__iregex=regex),
            "caluma_form.QuestionOption": Q(question__forms__pk__iregex=regex),
            "caluma_form.FormQuestion": Q(form__pk__iregex=regex),
            "caluma_form.Answer": Q(
                question__forms__pk__iregex=regex,
                document__isnull=True,
            ),
        }
    elif version:
        v = f"-v{version}"
        return {
            "caluma_form.Form": Q(pk__endswith=v),
            "caluma_form.FormQuestion": Q(form__pk__endswith=v),
            "caluma_form.Question": Q(pk__endswith=v),
            "caluma_form.QuestionOption": Q(question__pk__endswith=v),
            "caluma_form.Option": Q(questions__pk__endswith=v),
            "caluma_form.Answer": Q(
                question__forms__pk__endswith=v,
                document__isnull=True,
            ),
        }

    return {}  # pragma: no cover


def generate_workflow_dump_config(regex, include_task_regex=False):
    filters = {
        "caluma_workflow.Workflow": Q(pk__iregex=regex),
        "caluma_workflow.Task": Q(pk__iregex=regex),
        "caluma_workflow.TaskFlow": Q(workflow__pk__iregex=regex),
        "caluma_workflow.Flow": Q(task_flows__workflow__pk__iregex=regex),
    }

    if include_task_regex:
        filters["caluma_workflow.TaskFlow"] |= Q(task__pk__iregex=regex)
        filters["caluma_workflow.Flow"] |= Q(task_flows__task__pk__iregex=regex)

    return filters


COMMON_QUESTION_SLUGS_BE = ["8-freigabequittung", "dokumente-platzhalter"]

COMMON_FORM_SLUGS_BE = [
    "personalien",
    "allgemeine-angaben-kurz",
    "parzelle-tabelle",
    "personalien-tabelle",
    "projektverfasserin",
    "grundeigentumerin",
    "gebaudeeigentumerin",
    "vertreterin-mit-vollmacht",
    "8-freigabequittung",
]

DISTRIBUTION_DUMP_CONFIG = {
    "caluma_distribution": {
        **generate_form_dump_config(r"(inquir(y|ies)|distribution)"),
        **generate_workflow_dump_config(r"(inquir(y|ies)|distribution)"),
    },
}

ADDITIONAL_DEMAND_DUMP_CONFIG = {
    "caluma_additional_demand": {
        **generate_form_dump_config(r"additional-demand"),
        **generate_workflow_dump_config(r"additional-demand"),
    }
}

CONSTRUCTION_MONITORING_REGEX = (
    r"(construction-monitoring|construction-stage|construction-step|complete-instance)"
)

CONSTRUCTION_MONITORING_DUMP_CONFIG = {
    "caluma_construction_monitoring_form": {
        **generate_form_dump_config(CONSTRUCTION_MONITORING_REGEX),
    },
    "caluma_construction_monitoring_workflow": {
        **generate_workflow_dump_config(CONSTRUCTION_MONITORING_REGEX, True),
    }
}

DUMP = {
    "default": {
        "CONFIG": {
            # Configuration models that do not have any foreign key relationships
            # to non-config models (direct or indirect).
            # These models can be safely deleted and re-imported anytime.
            "MODELS": [
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
                "core.IrTaskform",
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
                "core.Resource",
                "core.ResourceT",
                "core.REmberList",
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
                "core.ServiceAnswerActivation",
                "core.TemplateGenerateAction",
                "core.WorkflowAction",
                "core.WorkflowRole",
                "responsible.IrEditresponsibleuser",
                "responsible.IrEditresponsiblegroup",
                "responsible.ASetresponsiblegroup",
                "responsible.ResponsibleServiceAllocation",
                "core.HistoryActionConfig",
                "core.HistoryActionConfigT",
                "core.ActionWorkitem",
                "core.ActionCase",
                "caluma_form.Option",
                "caluma_form.QuestionOption",
                "caluma_form.FormQuestion",
                "caluma_workflow.TaskFlow",
                "caluma_workflow.Flow",
                "gis.GISDataSource",
            ],
            # List of models that have foreign keys referencing non-config
            # tables (directly or indirectly). All models which are not in this
            # list can be safely flushed and re-imported.
            "MODELS_REFERENCING_DATA": [
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
                "caluma_form.Question",
                "caluma_form.Form",
                "caluma_workflow.Workflow",
                "caluma_workflow.Task",
                "alexandria_core.Category",
                "alexandria_core.Mark",
                "permissions.AccessLevel",
            ],
            # Exclude models which are managed by the customer alone from sync -
            # instead it will be dumped as data. This will most likely be
            # configured in the application section of this config file.
            "EXCLUDED_MODELS": [
                # Example:
                # "user.Group",
                # "user.GroupT",
            ],
            # Define custom config groups that will be dumped in an extracted
            # fixture file. This will most likely be configured in the
            # application section of this config file.
            "GROUPS": {
                # Example:
                # "custom_form": {
                #     "caluma_form.Option": Q(questions__forms__pk="custom_form"),
                #     "caluma_form.Question": Q(forms__pk="custom_form"),
                #     "caluma_form.Form": Q(pk="custom_form"),
                #     "caluma_form.QuestionOption": Q(question__forms__pk="custom_form"),
                #     "caluma_form.FormQuestion": Q(form__pk__in="custom_form"),
                # },
            },
        },
        "DATA": {
            # List of django apps that include models which should be dumped
            # into the data dump files
            "APPS": [
                "circulation",
                "core",
                "document",
                "instance",
                "notification",
                "user",
                "applicants",
                "caluma_form",
                "caluma_workflow",
                "alexandria_core",
                "gis",
                "permissions",
            ],
            # List of models that are included in "APPS" but should not be
            # dumped into the data dump files
            "EXCLUDED_MODELS": [
                "caluma_form.HistoricalOption",
                "caluma_form.HistoricalQuestion",
                "caluma_form.HistoricalForm",
                "caluma_form.HistoricalQuestionOption",
                "caluma_form.HistoricalFormQuestion",
                "caluma_workflow.HistoricalWorkflow",
                "caluma_workflow.HistoricalTask",
                "caluma_workflow.HistoricalTaskFlow",
                "caluma_workflow.HistoricalFlow",
                "instance.InstanceAlexandriaDocument",
            ],
        },
    },
    "kt_bern": {
        "ENABLED": True,
        "CONFIG": {
            "GROUPS": {
                "email_notifications": {
                    "notification.NotificationTemplate": Q(type="email"),
                    "notification.NotificationTemplateT": Q(template__type="email"),
                },
                # required by several form-questions
                "caluma_form_common": {
                    "caluma_form.Form": Q(pk__in=COMMON_FORM_SLUGS_BE),
                    "caluma_form.FormQuestion": Q(form__pk__in=COMMON_FORM_SLUGS_BE),
                    "caluma_form.Question": Q(forms__pk__in=COMMON_FORM_SLUGS_BE)
                    | Q(pk__in=COMMON_QUESTION_SLUGS_BE),
                    "caluma_form.QuestionOption": Q(
                        question__forms__pk__in=COMMON_FORM_SLUGS_BE
                    )
                    | Q(question_id__in=COMMON_QUESTION_SLUGS_BE),
                    "caluma_form.Option": Q(
                        questions__forms__pk__in=COMMON_FORM_SLUGS_BE
                    )
                    | Q(questions__pk__in=COMMON_QUESTION_SLUGS_BE),
                },
                "caluma_form_v2": generate_form_dump_config(version=2),
                "caluma_form_v3": generate_form_dump_config(version=3),
                "caluma_form_v4": generate_form_dump_config(version=4),
                "caluma_dossier_import_form": generate_form_dump_config(
                    regex=r"^migriertes-dossier(-daten)?$"
                ),
                "caluma_form_sb2": generate_form_dump_config(regex=r"(-)?sb2$"),
                "caluma_information_of_neighbors_form": generate_form_dump_config(
                    regex=r"^information-of-neighbors$"
                ),
                "caluma_ebau_number_form": generate_form_dump_config(
                    regex=r"^ebau-number$"
                ),
                "caluma_solar_plants_form": generate_form_dump_config(
                    regex=r"^solaranlagen(-)?"
                ),
                "caluma_decision_form": generate_form_dump_config(regex=r"^decision$"),
                "caluma_audit_form": generate_form_dump_config(
                    regex=r"^(dossierpruefung|mp-|fp-|mp-|bab-)"
                ),
                "caluma_publication_form": generate_form_dump_config(
                    regex=r"^publikation$"
                ),
                "caluma_heat_generator_form": generate_form_dump_config(
                    regex=r"^heat-generator"
                ),
                "caluma_legal_submission_form": generate_form_dump_config(
                    r"^legal-submission"
                ),
                "caluma_appeal_form": generate_form_dump_config(r"^appeal"),
                "caluma_geometer_form": generate_form_dump_config(r"^geometer"),
                # Distribution
                **DISTRIBUTION_DUMP_CONFIG,
            },
            "EXCLUDED_MODELS": [
                "user.Group",
                "user.GroupT",
                "user.GroupLocation",
                "user.Service",
                "user.ServiceT",
                "notification.NotificationTemplate",
                "notification.NotificationTemplateT",
            ],
        },
    },
    "kt_schwyz": {
        "ENABLED": True,
        "CONFIG": {
            "GROUPS": {
                "email_notifications": {
                    "notification.NotificationTemplate": Q(type="email"),
                    "notification.NotificationTemplateT": Q(template__type="email"),
                },
                "buildingauthority": {
                    "caluma_form.Form": Q(pk="realisierung-tabelle"),
                    "caluma_form.FormQuestion": Q(form__pk="realisierung-tabelle"),
                    "caluma_form.Question": Q(
                        pk__startswith="baukontrolle-realisierung"
                    )
                    | Q(pk="bewilligungsverfahren-gr-sitzung-bewilligungsdatum"),
                    "caluma_form.QuestionOption": Q(
                        question__pk__startswith="baukontrolle-realisierung"
                    ),
                    "caluma_form.Option": Q(
                        questions__pk__startswith="baukontrolle-realisierung"
                    ),
                },
                # Distribution
                **DISTRIBUTION_DUMP_CONFIG,
                **CONSTRUCTION_MONITORING_DUMP_CONFIG,
            },
            "EXCLUDED_MODELS": [
                "document.Template",
                "user.Group",
                "user.GroupT",
                "user.GroupLocation",
                "user.Service",
                "user.ServiceT",
                "notification.NotificationTemplate",
                "notification.NotificationTemplateT",
            ],
        },
    },
    "kt_uri": {
        "ENABLED": True,
        "CONFIG": {
            "GROUPS": {
                "dashboard_document": {
                    "caluma_form.Document": Q(form="dashboard"),
                },
            },
            "EXCLUDED_MODELS": [
                "user.Group",
                "user.GroupT",
                "user.GroupLocation",
                "user.Service",
                "user.ServiceT",
                "notification.NotificationTemplate",
                "notification.NotificationTemplateT",
            ],
        },
    },
    "kt_gr": {
        "ENABLED": True,
        "CONFIG": {
            "GROUPS": {
                "email_notifications": {
                    "notification.NotificationTemplate": Q(type="email"),
                    "notification.NotificationTemplateT": Q(template__type="email"),
                },
                # required by several form-questions
                "caluma_form_common": {
                    "caluma_form.Form": Q(pk__in=COMMON_FORM_SLUGS_BE),
                    "caluma_form.FormQuestion": Q(form__pk__in=COMMON_FORM_SLUGS_BE),
                    "caluma_form.Question": Q(forms__pk__in=COMMON_FORM_SLUGS_BE)
                    | Q(pk__in=COMMON_QUESTION_SLUGS_BE),
                    "caluma_form.QuestionOption": Q(
                        question__forms__pk__in=COMMON_FORM_SLUGS_BE
                    )
                    | Q(question_id__in=COMMON_QUESTION_SLUGS_BE),
                    "caluma_form.Option": Q(
                        questions__forms__pk__in=COMMON_FORM_SLUGS_BE
                    )
                    | Q(questions__pk__in=COMMON_QUESTION_SLUGS_BE),
                    "caluma_form.Answer": Q(
                        document__isnull=True,
                    ),
                },
                "caluma_decision_form": generate_form_dump_config(regex=r"^decision$"),
                "caluma_formal_exam_form": generate_form_dump_config(
                    regex=r"^formal-exam$"
                ),
                "caluma_material_exam_form": generate_form_dump_config(
                    regex=r"^material-exam$"
                ),
                "dashboard_document": {
                    "caluma_form.Document": Q(form="dashboard"),
                },
                # Sync the "core" groups (admin, support, portal) between servers, the rest is treated as data
                "user_core_groups": {
                    "user.Group": Q(pk__lte=3),
                    "user.GroupT": Q(pk__lte=3),
                },
                # Distribution
                **DISTRIBUTION_DUMP_CONFIG,
                # Additional demand
                **ADDITIONAL_DEMAND_DUMP_CONFIG,
                "publication": {
                    **generate_form_dump_config(regex=r"^publikation?$"),
                },
            },
            "EXCLUDED_MODELS": [
                "user.Group",
                "user.GroupT",
                "user.Service",
                "user.ServiceT",
            ],
        },
    },
    "kt_so": {
        "ENABLED": True,
        "CONFIG": {
            "GROUPS": {
                "email_notifications": {
                    "notification.NotificationTemplate": Q(type="email"),
                    "notification.NotificationTemplateT": Q(template__type="email"),
                },
                # Sync the "core" groups (admin, support, portal) between servers, the rest is treated as data
                "user_core_groups": {
                    "user.Group": Q(role__name__in=["admin", "applicant", "support"]),
                    "user.GroupT": Q(
                        group__role__name__in=["admin", "applicant", "support"]
                    ),
                },
                # Dashboard
                "dashboard": {
                    **generate_form_dump_config(regex=r"^dashboard?$"),
                    "caluma_form.Document": Q(form="dashboard"),
                    # Static content
                    "caluma_form.Answer": Q(
                        question_id__in=[
                            "portal-faq-inhalt-de",
                            "portal-terms-inhalt-de",
                        ]
                    ),
                },
                "caluma_formal_exam_form": generate_form_dump_config(
                    regex=r"^formelle-pruefung"
                ),
                "caluma_material_exam_form": generate_form_dump_config(
                    regex=r"^materielle-pruefung"
                ),
                "caluma_publication_form": generate_form_dump_config(
                    regex=r"^publikation?$"
                ),
                "caluma_decision_form": generate_form_dump_config(regex=r"^entscheid$"),
                # Distribution
                **DISTRIBUTION_DUMP_CONFIG,
                # Additional demand
                **ADDITIONAL_DEMAND_DUMP_CONFIG,
                # Objections
                "caluma_objection_form": generate_form_dump_config(
                    regex=r"^einsprache(n)?"
                ),
                "caluma_appeal_form": generate_form_dump_config(regex=r"^beschwerde"),
            },
            "EXCLUDED_MODELS": [
                "user.Group",
                "user.GroupT",
                "user.Service",
                "user.ServiceT",
            ],
        },
    },
    "demo": {
        "ENABLED": True,
        "CONFIG": {
            "GROUPS": {
                "email_notifications": {
                    "notification.NotificationTemplate": Q(type="email"),
                    "notification.NotificationTemplateT": Q(template__type="email"),
                },
                # required by several form-questions
                "caluma_form_common": {
                    "caluma_form.Form": Q(pk__in=COMMON_FORM_SLUGS_BE),
                    "caluma_form.FormQuestion": Q(form__pk__in=COMMON_FORM_SLUGS_BE),
                    "caluma_form.Question": Q(forms__pk__in=COMMON_FORM_SLUGS_BE)
                    | Q(pk__in=COMMON_QUESTION_SLUGS_BE),
                    "caluma_form.QuestionOption": Q(
                        question__forms__pk__in=COMMON_FORM_SLUGS_BE
                    )
                    | Q(question_id__in=COMMON_QUESTION_SLUGS_BE),
                    "caluma_form.Option": Q(
                        questions__forms__pk__in=COMMON_FORM_SLUGS_BE
                    )
                    | Q(questions__pk__in=COMMON_QUESTION_SLUGS_BE),
                },
                "caluma_ebau_number_form": generate_form_dump_config(
                    regex=r"^ebau-number$"
                ),
                "caluma_decision_form": generate_form_dump_config(regex=r"^decision$"),
                # Distribution
                **DISTRIBUTION_DUMP_CONFIG,
            }
        },
    },
    "test": {"ENABLED": True},
}
