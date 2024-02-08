from collections import namedtuple
from datetime import datetime, timedelta
from functools import wraps

import pytz
from caluma.caluma_form.models import Answer, Document
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.models import Case, Task, WorkItem
from deepmerge import always_merger
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, reset_queries, transaction
from django.db.models import (
    Case as DjangoCase,
    Exists,
    F,
    Func,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.functions import Cast, Concat
from django.utils.timezone import now
from tqdm import tqdm

from camac.core import models as core_models
from camac.instance.models import HistoryEntry
from camac.responsible.models import ResponsibleService
from camac.user.models import Service, User


def get_config(application_name):
    default = {
        "DISTRIBUTION_TASK": settings.DISTRIBUTION["DISTRIBUTION_TASK"],
        "INQUIRY_TASK": settings.DISTRIBUTION["INQUIRY_TASK"],
        "CREATE_INQUIRY_TASK": settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
        "CHECK_INQUIRIES_TASK": settings.DISTRIBUTION["INQUIRY_CHECK_TASK"],
        "FILL_INQUIRY_TASK": settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
        "REDO_INQUIRY_TASK": "redo-inquiry",
        "DISTRIBUTION_COMPLETE_TASK": settings.DISTRIBUTION[
            "DISTRIBUTION_COMPLETE_TASK"
        ],
        "DISTRIBUTION_INIT_TASK": settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
        "DISTRIBUTION_WORKFLOW": settings.DISTRIBUTION["DISTRIBUTION_WORKFLOW"],
        "INQUIRY_WORKFLOW": settings.DISTRIBUTION["INQUIRY_WORKFLOW"],
        "META": {
            "migrated-at": now().isoformat(),
            "not-viewed": True,
            "notify-completed": False,
            "notify-deadline": False,
        },
    }

    if application_name == "kt_bern":
        return always_merger.merge(
            default,
            {
                "EXCLUDED_WORKFLOWS": [
                    "migrated",  # Migrierte Dossiers (RSTA Migration)
                    "internal",  # Baupolizeiliches Verfahren
                ],
                "PRECEEDING_TASK": "ebau-number",
                "SUCCEEDING_TASK": "decision",
                "STATUS_DRAFT": 20000,
                "STATUS_MAPPING": {
                    20001: "inquiry-answer-status-positive",
                    20003: "inquiry-answer-status-negative",
                    20004: "inquiry-answer-status-not-involved",
                    20005: "inquiry-answer-status-claim",
                    150000: "inquiry-answer-status-obligated",
                    150001: "inquiry-answer-status-not-obligated",
                    15000000: "inquiry-answer-status-unknown",
                },
                "NOTICE_TYPE_MAPPING": {
                    1: "inquiry-answer-statement",
                    20000: "inquiry-answer-ancillary-clauses",
                },
            },
        )
    elif application_name == "kt_schwyz":
        return always_merger.merge(
            default,
            {
                "CHECK_INQUIRY_TASK": settings.DISTRIBUTION[
                    "INQUIRY_ANSWER_CHECK_TASK"
                ],
                "REVISE_INQUIRY_TASK": settings.DISTRIBUTION[
                    "INQUIRY_ANSWER_REVISE_TASK"
                ],
                "ALTER_INQUIRY_TASK": settings.DISTRIBUTION[
                    "INQUIRY_ANSWER_ALTER_TASK"
                ],
                "EXCLUDED_WORKFLOWS": ["internal"],  # Interne Geschäfte
                "PRECEEDING_TASK": "complete-check",
                "SUCCEEDING_TASK": "make-decision",
                "ADDITIONAL_DEMAND_TASK": "additional-demand",
                "DEPRECIATE_CASE_TASK": "depreciate-case",
                "DEPRECIATE_CASE_INSTANCE_STATE": "stopped",
                "POST_CIRCULATION_INSTANCE_STATES": [
                    "redac",
                    "done",
                    "denied",
                    "stopped",
                    "arch",
                ],
                "STATUS_MAPPING": {
                    12: "inquiry-answer-status-further-clarification",
                    1: "inquiry-answer-status-not-involved",
                    2: "inquiry-answer-status-claim",
                    3: "inquiry-answer-status-legal-hearing",
                    4: "inquiry-answer-status-claim-legal-hearing",
                    9: "inquiry-answer-status-final",
                    10: "inquiry-answer-status-opposition",
                    11: "inquiry-answer-status-inspection",
                },
                "NOTICE_TYPE_MAPPING": {
                    1: "inquiry-answer-request",
                    3: "inquiry-answer-ancillary-clauses",
                    5: "inquiry-answer-reason",
                    6: "inquiry-answer-recommendation",
                    7: "inquiry-answer-hint",
                },
            },
        )


def num_queries(reset=True):
    print(len(connection.queries))
    if reset:
        reset_queries()


def canton_aware(include_base_method=False):
    def decorator(func, *_):
        @wraps(func)
        def wrapper(self, *args, **kwargs):

            canton = (
                "be"
                if settings.APPLICATION_NAME == "kt_bern"
                else "sz" if settings.APPLICATION_NAME == "kt_schwyz" else None
            )
            func_name = f"{func.__name__}_{canton}" if canton else f"{func.__name__}"
            if hasattr(self, func_name):
                if include_base_method:
                    result = func(self, *args, **kwargs)
                    return getattr(self, func_name)(*args, result, **kwargs)

                return getattr(self, func_name)(*args, **kwargs)

            return func(self, *args, **kwargs)

        return wrapper

    return decorator


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._responsible = {}

        raw_config = get_config(settings.APPLICATION_NAME)
        Config = namedtuple("DistributionMigrationConfig", raw_config.keys())

        self.config = Config(
            **{
                k: Task.objects.get(pk=v) if k.endswith("_TASK") else v
                for k, v in raw_config.items()
            }
        )

    def add_arguments(self, parser):
        parser.add_argument("--reset", dest="reset", action="store_true", default=False)

    def reset(self):
        with connection.cursor() as cursor:
            task_ids = [
                settings.DISTRIBUTION["DISTRIBUTION_TASK"],
                settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
                settings.DISTRIBUTION["DISTRIBUTION_COMPLETE_TASK"],
                settings.DISTRIBUTION["INQUIRY_TASK"],
                settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
                settings.DISTRIBUTION["INQUIRY_CHECK_TASK"],
                settings.DISTRIBUTION["INQUIRY_REDO_TASK"],
                settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
            ]
            workflow_ids = [
                settings.DISTRIBUTION["DISTRIBUTION_WORKFLOW"],
                settings.DISTRIBUTION["INQUIRY_WORKFLOW"],
            ]

            if settings.APPLICATION_NAME == "kt_schwyz":
                task_ids.extend(
                    [
                        settings.DISTRIBUTION["INQUIRY_ANSWER_CHECK_TASK"],
                        settings.DISTRIBUTION["INQUIRY_ANSWER_REVISE_TASK"],
                        settings.DISTRIBUTION["INQUIRY_ANSWER_ALTER_TASK"],
                    ]
                )

            cursor.execute(
                "UPDATE caluma_workflow_workitem SET previous_work_item_id = NULL WHERE previous_work_item_id IN (SELECT id FROM caluma_workflow_workitem WHERE task_id = ANY(%s))",
                [task_ids],
            )
            cursor.execute(
                "DELETE FROM caluma_workflow_workitem WHERE task_id = ANY(%s)",
                [task_ids],
            )
            cursor.execute(
                "DELETE FROM caluma_workflow_case WHERE workflow_id = ANY(%s)",
                [workflow_ids],
            )
            cursor.execute(
                "DELETE FROM caluma_form_answer WHERE document_id IN (SELECT id FROM caluma_form_document WHERE form_id = %s)",
                [settings.DISTRIBUTION["INQUIRY_FORM"]],
            )
            cursor.execute(
                "DELETE FROM caluma_form_document WHERE form_id = %s",
                [settings.DISTRIBUTION["INQUIRY_FORM"]],
            )

    @transaction.atomic
    def handle(self, *args, **options):
        if options.get("reset"):
            self.reset()

        base_filters = Exists(
            WorkItem.objects.filter(
                case_id=OuterRef("pk"),
                task=self.config.PRECEEDING_TASK,
                status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
            )
        )

        filters = self.cases_to_migrate_filters(base_filters)

        cases_to_migrate = (
            Case.objects.select_related("instance", "instance__instance_state")
            .prefetch_related("instance__circulations")
            .exclude(workflow_id__in=self.config.EXCLUDED_WORKFLOWS)
            .exclude(instance__isnull=True)
            .exclude(
                Exists(
                    WorkItem.objects.filter(
                        case_id=OuterRef("pk"), task=self.config.DISTRIBUTION_TASK
                    )
                )
            )
            .filter(filters)
        )

        for case in tqdm(cases_to_migrate, mininterval=1, maxinterval=2):
            try:
                self.migrate_case(case)
            except Exception as e:  # noqa: B902
                raise CommandError(
                    f"Exception ocurred during migration of instance {case.instance.pk}: {str(e)}"
                )

        self.post_migrate()

    def migrate_case(self, case):
        responsible_service = case.instance.responsible_service(
            filter_type="municipality"
        )

        user = BaseUser(group=str(responsible_service.pk))

        activations = (
            core_models.Activation.objects.select_related("circulation_state")
            .prefetch_related("notices")
            .filter(circulation__instance=case.instance)
            .defer("activation_parent", "version", "suspension_date", "user")
        )

        previous_work_item = case.work_items.filter(
            task=self.config.PRECEEDING_TASK,
            status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
        ).first()

        next_work_item = (
            case.work_items.filter(task=self.config.SUCCEEDING_TASK)
            .exclude(status=WorkItem.STATUS_CANCELED)  # Circulation was reopened
            .first()
        )

        # create distribution work item
        distribution_work_item = self.initialize_distribution(
            case, user, activations, previous_work_item, next_work_item
        )

        if next_work_item:
            next_work_item.previous_work_item = distribution_work_item
            next_work_item.save()

        self.on_migrate_case(
            case,
            user,
            activations,
            previous_work_item,
            next_work_item,
            distribution_work_item,
        )

        if activations.exists():
            self.migrate_activations(
                distribution_work_item.child_case,
                activations,
                case.instance,
                responsible_service,
            )

    def initialize_distribution(
        self, case, user, activations, previous_work_item, next_work_item
    ):
        work_items = []

        # Differentiate between skipped and completed circulation
        has_circulations = case.instance.circulations.exists()

        distribution_is_initialized = self.distribution_is_initialized(
            case, previous_work_item, next_work_item, has_circulations
        )
        distribution_is_canceled = self.distribution_is_canceled(
            case, previous_work_item, next_work_item, has_circulations
        )
        distribution_is_closed = self.distribution_is_closed(
            case, previous_work_item, next_work_item, has_circulations
        )
        distribution_is_suspended = self.distribution_is_suspended(
            case, previous_work_item, next_work_item, has_circulations
        )
        distribution_closed_at = self.distribution_closed_at(
            previous_work_item, next_work_item
        )
        previous_work_item_closed_at = self.previous_work_item_closed_at(
            case, previous_work_item
        )

        # Create distribution work-item and child case

        distribution_case = Case.objects.create(
            workflow_id="distribution",
            family=case,
            status=(
                Case.STATUS_COMPLETED
                if distribution_is_closed
                else (
                    Case.STATUS_CANCELED
                    if distribution_is_canceled
                    else (
                        Case.STATUS_SUSPENDED
                        if distribution_is_suspended
                        else Case.STATUS_RUNNING
                    )
                )
            ),
            closed_at=distribution_closed_at,
        )

        distribution_work_item = WorkItem(
            task=self.config.DISTRIBUTION_TASK,
            name=self.config.DISTRIBUTION_TASK.name,
            addressed_groups=[user.group],
            assigned_users=self.responsible_user(user.group, case.instance),
            case=case,
            status=(
                WorkItem.STATUS_COMPLETED
                if distribution_is_closed
                else (
                    WorkItem.STATUS_CANCELED
                    if distribution_is_canceled
                    else (
                        WorkItem.STATUS_SUSPENDED
                        if distribution_is_suspended
                        else WorkItem.STATUS_READY
                    )
                )
            ),
            closed_at=distribution_closed_at,
            previous_work_item=previous_work_item,
            child_case=distribution_case,
            meta=self.config.META,
        )

        work_items.append(distribution_work_item)

        # create "init-distribution", "create-inquiry" and "complete-distribution"
        # work items for leading authority

        earliest_activation_sent = (
            self.activations_sent(activations).order_by("start_date").first()
        )

        earliest_activation_sent_start_date = (
            earliest_activation_sent.start_date if earliest_activation_sent else None
        )

        work_items.extend(
            [
                WorkItem(
                    task=self.config.CREATE_INQUIRY_TASK,
                    name=self.config.CREATE_INQUIRY_TASK.name,
                    addressed_groups=[user.group],
                    assigned_users=self.responsible_user(user.group, case.instance),
                    case=distribution_case,
                    status=(
                        WorkItem.STATUS_CANCELED
                        if distribution_is_closed or distribution_is_canceled
                        else (
                            WorkItem.STATUS_SUSPENDED
                            if distribution_is_suspended
                            else WorkItem.STATUS_READY
                        )
                    ),
                    meta=self.config.META,
                ),
                WorkItem(
                    task=self.config.DISTRIBUTION_COMPLETE_TASK,
                    name=self.config.DISTRIBUTION_COMPLETE_TASK.name,
                    addressed_groups=[user.group],
                    assigned_users=self.responsible_user(user.group, case.instance),
                    case=distribution_case,
                    status=(
                        WorkItem.STATUS_COMPLETED
                        if distribution_is_closed
                        else (
                            WorkItem.STATUS_CANCELED
                            if distribution_is_canceled
                            else (
                                WorkItem.STATUS_SUSPENDED
                                if distribution_is_suspended
                                else WorkItem.STATUS_READY
                            )
                        )
                    ),
                    closed_at=distribution_closed_at,
                    meta=self.config.META,
                ),
                WorkItem(
                    task=self.config.DISTRIBUTION_INIT_TASK,
                    name=self.config.DISTRIBUTION_INIT_TASK.name,
                    addressed_groups=[user.group],
                    controlling_groups=[user.group],
                    assigned_users=self.responsible_user(user.group, case.instance),
                    case=distribution_case,
                    status=(
                        WorkItem.STATUS_COMPLETED
                        if earliest_activation_sent_start_date
                        or (distribution_is_closed and has_circulations)
                        or (
                            distribution_is_initialized
                            and not distribution_is_canceled
                            and not distribution_is_closed
                        )
                        else (
                            WorkItem.STATUS_CANCELED
                            if distribution_is_canceled
                            or (distribution_is_closed and not has_circulations)
                            else (
                                WorkItem.STATUS_SUSPENDED
                                if distribution_is_suspended
                                else WorkItem.STATUS_READY
                            )
                        )
                    ),
                    meta=self.config.META,
                    deadline=pytz.utc.localize(
                        datetime.combine(
                            (
                                previous_work_item_closed_at
                                + timedelta(
                                    seconds=self.config.DISTRIBUTION_INIT_TASK.lead_time
                                )
                            ).date(),
                            datetime.min.time(),
                        )
                    ),
                    closed_at=earliest_activation_sent_start_date
                    or distribution_closed_at,
                ),
            ]
        )

        # create a "create-inquiry" work item for all services allowed to create

        services_allowed_to_create = (
            Service.objects.filter(
                # Only allow services to create, that have a pending inquiry
                pk__in=self.activations_ready(activations).values("service_id"),
                service_parent__isnull=True,
            )
            # Already generated for leading authority
            .exclude(pk=user.group).values_list("pk", flat=True)
        )

        for service_id in services_allowed_to_create:
            work_items.append(
                WorkItem(
                    task=self.config.CREATE_INQUIRY_TASK,
                    name=self.config.CREATE_INQUIRY_TASK.name,
                    addressed_groups=[str(service_id)],
                    assigned_users=self.responsible_user(service_id, case.instance),
                    case=distribution_case,
                    status=(
                        WorkItem.STATUS_CANCELED
                        if distribution_is_closed or distribution_is_canceled
                        else (
                            WorkItem.STATUS_SUSPENDED
                            if distribution_is_suspended
                            else WorkItem.STATUS_READY
                        )
                    ),
                    meta=self.config.META,
                )
            )

        answered_activations = self.activations_answered(activations)

        # create a "check-inquiries" work item for all services allowed to check
        # with at least one answered activation

        services_allowed_to_check = Service.objects.filter(
            pk__in=answered_activations.values("service_parent_id")
        ).values_list("pk", flat=True)

        for service_id in services_allowed_to_check:
            has_pending_activations = any(
                [
                    self.activation_is_ready(activation)
                    for activation in activations.filter(service_parent_id=service_id)
                ]
            )

            last_answered_activation = answered_activations.filter(
                service_parent_id=service_id,
                end_date__isnull=False,
            ).latest("end_date")

            # The "check-inquiries" work item only has a deadline if all of the
            # activation that were created by this service are answered
            if not has_pending_activations and last_answered_activation:
                deadline = pytz.utc.localize(
                    datetime.combine(
                        (
                            last_answered_activation.end_date
                            + timedelta(
                                seconds=self.config.CHECK_INQUIRIES_TASK.lead_time
                            )
                        ).date(),
                        datetime.min.time(),
                    )
                )
            else:
                deadline = None

            # If the activation of this service already answered their
            # activation, the "check-inquiries" work item is completed
            last_addressed_activation_answered_at = (
                answered_activations.filter(service_id=service_id)
                .order_by("-end_date")
                .values_list("end_date", flat=True)
                .first()
            )

            is_completed = distribution_is_closed or (
                last_addressed_activation_answered_at and deadline
            )

            work_items.append(
                WorkItem(
                    task=self.config.CHECK_INQUIRIES_TASK,
                    name=self.config.CHECK_INQUIRIES_TASK.name,
                    addressed_groups=[str(service_id)],
                    controlling_groups=[str(service_id)],
                    case=distribution_case,
                    meta=self.config.META,
                    status=(
                        WorkItem.STATUS_COMPLETED
                        if is_completed
                        else (
                            WorkItem.STATUS_CANCELED
                            if distribution_is_canceled
                            else (
                                WorkItem.STATUS_SUSPENDED
                                if distribution_is_suspended
                                else WorkItem.STATUS_READY
                            )
                        )
                    ),
                    deadline=deadline,
                    closed_at=(
                        (
                            last_addressed_activation_answered_at
                            or distribution_closed_at
                        )
                        if is_completed
                        else None
                    ),
                )
            )

        WorkItem.objects.bulk_create(work_items)
        WorkItem.objects.filter(
            pk__in=[work_item.pk for work_item in work_items]
        ).update(
            created_at=DjangoCase(
                When(
                    task_id__in=[
                        self.config.DISTRIBUTION_TASK.pk,
                        self.config.DISTRIBUTION_COMPLETE_TASK.pk,
                        self.config.DISTRIBUTION_INIT_TASK.pk,
                    ],
                    then=previous_work_item_closed_at,
                ),
                When(
                    task_id__in=[self.config.CHECK_INQUIRIES_TASK.pk],
                    then=Subquery(
                        answered_activations.filter(
                            service_parent=Func(
                                Cast(
                                    OuterRef("addressed_groups"),
                                    output_field=ArrayField(IntegerField()),
                                ),
                                function="ANY",
                            ),
                        )
                        .order_by("end_date")
                        .values("end_date")[:1]
                    ),
                ),
                default=F("created_at"),
            )
        )
        return distribution_work_item

    def migrate_activations(
        self, distribution_case, activations, instance, responsible_service
    ):
        documents = []
        cases = []
        work_items = []
        answers = []

        for activation in activations:
            is_completed = self.activation_is_completed(activation)
            is_skipped = self.activation_is_skipped(activation, instance)
            is_ready = self.activation_is_ready(activation)
            is_draft = self.activation_is_draft(activation)

            # create inquiry work-item and document
            document = Document(form_id="inquiry")
            documents.append(document)

            work_item = WorkItem(
                task=self.config.INQUIRY_TASK,
                name=self.config.INQUIRY_TASK.name,
                addressed_groups=[str(activation.service_id)],
                controlling_groups=[str(activation.service_parent_id)],
                assigned_users=self.responsible_user(activation.service_id, instance),
                case=distribution_case,
                meta={**self.config.META, "migrated-from-activation-id": activation.pk},
                status=(
                    WorkItem.STATUS_COMPLETED
                    if is_completed
                    else (
                        WorkItem.STATUS_SKIPPED
                        if is_skipped
                        else (
                            WorkItem.STATUS_READY
                            if is_ready
                            else WorkItem.STATUS_SUSPENDED if is_draft else None
                        )
                    )
                ),
                document=document,
                created_by_group=str(activation.service_parent_id),
                deadline=pytz.utc.localize(
                    datetime.combine(
                        activation.deadline_date.date(),
                        datetime.min.time(),
                    )
                ),
                closed_at=activation.end_date,
            )

            answers.append(
                Answer(
                    question_id="inquiry-deadline",
                    document=document,
                    date=activation.deadline_date.date(),
                )
            )

            if activation.reason:
                answers.append(
                    Answer(
                        question_id="inquiry-remark",
                        document=document,
                        value=activation.reason,
                    )
                )

            # create inquiry answer child-case, document and work-items

            if is_ready or is_completed or is_skipped:
                (
                    child_document,
                    child_case,
                    inquiry_answer_work_items,
                ) = self.initialize_inquiry_answer(
                    activation, distribution_case, work_item, instance
                )

                documents.append(child_document)
                cases.append(child_case)
                work_item.child_case = child_case
                work_items.extend(inquiry_answer_work_items)

                if self.activation_has_answer(activation):
                    answers.append(
                        Answer(
                            question_id="inquiry-answer-status",
                            document=child_document,
                            value=self.config.STATUS_MAPPING[
                                activation.circulation_answer_id
                            ],
                        )
                    )

                for notice in activation.notices.all():
                    answers.append(
                        Answer(
                            question_id=self.config.NOTICE_TYPE_MAPPING[
                                notice.notice_type_id
                            ],
                            document=child_document,
                            value=notice.content,
                        )
                    )

            if is_completed or is_skipped:
                work_items.append(
                    WorkItem(
                        task=self.config.REDO_INQUIRY_TASK,
                        name=self.config.REDO_INQUIRY_TASK.name,
                        previous_work_item=work_item,
                        addressed_groups=[str(activation.service_parent_id)],
                        controlling_groups=[],
                        case=distribution_case,
                        meta=self.config.META,
                        status=(
                            WorkItem.STATUS_CANCELED
                            if is_skipped
                            or (
                                distribution_case.parent_work_item.status
                                == WorkItem.STATUS_COMPLETED
                            )
                            # redo-inquiry work-item canceled for services without pending inquiries
                            # that are not the responsible service
                            or (
                                activation.service_parent_id != responsible_service.pk
                                and not self.activations_ready(activations)
                                .filter(service_id=activation.service_parent_id)
                                .exists()
                            )
                            else distribution_case.parent_work_item.status
                        ),
                        deadline=None,
                        closed_at=distribution_case.parent_work_item.closed_at,
                    )
                )

            work_items.append(work_item)

        Document.objects.bulk_create(documents)
        Answer.objects.bulk_create(answers)
        Case.objects.bulk_create(cases)
        WorkItem.objects.bulk_create(work_items)

    @canton_aware()
    def case_is_depreciated(self, case):
        return False

    def case_is_depreciated_sz(self, case):
        return (
            WorkItem.objects.filter(
                task=self.config.DEPRECIATE_CASE_TASK,
                name=self.config.DEPRECIATE_CASE_TASK.name,
                case=case,
                status=WorkItem.STATUS_COMPLETED,
            ).exists()
            or case.family.instance.instance_state.name
            == self.config.DEPRECIATE_CASE_INSTANCE_STATE
            or case.family.instance.previous_instance_state.name
            == self.config.DEPRECIATE_CASE_INSTANCE_STATE
        )

    @canton_aware()
    def cases_to_migrate_filters(self, filters):
        return filters

    def cases_to_migrate_filters_be(self, filters):
        return (
            filters
            # Case is in a state before the circulation could happen (pre camac-ng)
            & ~Q(instance__instance_state__name__in=["new", "subm"])
            # Case was rejected before the circulation could happen (pre camac-ng)
            & ~Q(
                instance__instance_state__name="rejected",
                instance__previous_instance_state__name="subm",
            )
            # Case was archived before the circulation could happen (pre camac-ng)
            & ~Q(
                instance__instance_state__name="archived",
                instance__previous_instance_state__name__in=["new", "subm"],
            )
        )

    def cases_to_migrate_filters_sz(self, filters):
        # Migrate instances that don't have a preceeding task
        # due to a previous migration
        return filters | Exists(
            # Dossier formell vollständig
            core_models.WorkflowEntry.objects.filter(
                instance__pk=OuterRef("instance__pk"),
                workflow_item__pk=14,
                workflow_date__isnull=False,
            )
        )

    @canton_aware()
    def distribution_is_closed(
        self, case, previous_work_item, next_work_item, has_circulations
    ):
        return next_work_item

    def distribution_is_closed_be(
        self, case, previous_work_item, next_work_item, has_circulations
    ):
        return case.instance.instance_state.name not in [
            "circulation_init",
            "circulation",
            "rejected",
            "correction",
        ]

    def distribution_is_closed_sz(
        self, case, previous_work_item, next_work_item, has_circulations
    ):
        if next_work_item:
            return True

        # handle depreciated cases
        case_is_depreciated = self.case_is_depreciated(case)

        if not case_is_depreciated:
            return case.instance.instance_state.name in [
                "redac",
                "done",
                "denied",
                "arch",
            ]

        return (
            case.instance.instance_state.name == "stopped"
            and case.instance.previous_instance_state.name == "redac"
        ) or (
            # approximation, archived depreciated case with no
            # (distribution-)succeeding work-item cannot be fully
            # reconstructed
            case.instance.instance_state.name == "arch"
            and has_circulations
        )

    @canton_aware()
    def distribution_closed_at(self, previous_work_item, next_work_item):
        return next_work_item.created_at if next_work_item else None

    def distribution_closed_at_sz(self, previous_work_item, next_work_item):
        if previous_work_item:
            return next_work_item.created_at if next_work_item else None

        # cannot be reconstructed
        return None

    @canton_aware()
    def distribution_is_initialized(
        self, case, previous_work_item, next_work_item, has_circulations
    ):
        return False

    def distribution_is_initialized_be(
        self, case, previous_work_item, next_work_item, has_circulations
    ):
        return case.instance.instance_state.name not in [
            "circulation_init",
            "correction",
            "rejected",
        ]

    @canton_aware()
    def distribution_is_canceled(
        self, case, previous_work_item, next_work_item, has_circulations
    ):
        return False

    def distribution_is_canceled_be(
        self, case, previous_work_item, next_work_item, has_circulations
    ):
        return case.instance.instance_state.name == "archived"

    def distribution_is_canceled_sz(
        self, case, previous_work_item, next_work_item, has_circulations
    ):
        # handle depreciated cases
        case_is_depreciated = self.case_is_depreciated(case)

        return (
            case_is_depreciated
            and not next_work_item
            or (
                case.instance.instance_state.name == "stopped"
                and case.instance.previous_instance_state.name in ["comm", "circ"]
            )
            or (
                # approximation, archived depreciated case with no
                # (distribution-)succeeding work-item cannot be fully
                # reconstructed
                case.instance.instance_state.name == "arch"
                and not has_circulations
            )
        )

    @canton_aware()
    def distribution_is_suspended(
        self, case, previous_work_item, next_work_item, has_circulations
    ):
        return False

    def distribution_is_suspended_be(
        self, case, previous_work_item, next_work_item, has_circulations
    ):
        return case.instance.instance_state.name in ["rejected", "correction"]

    @canton_aware()
    def previous_work_item_closed_at(self, case, previous_work_item):
        if previous_work_item:
            return previous_work_item.closed_at

        history_entry = HistoryEntry.objects.filter(
            instance=case.instance,
            trans__language="de",
            trans__title="eBau-Nr. vergeben",
        ).first()

        return history_entry.created_at

    def previous_work_item_closed_at_sz(self, case, previous_work_item):
        if previous_work_item:
            return previous_work_item.closed_at

        # Dossier formell vollständig
        return (
            core_models.WorkflowEntry.objects.filter(
                instance__pk=case.instance.pk, workflow_item__pk=14
            )
            .order_by("workflow_date")
            .values_list("workflow_date", flat=True)
            .first()
        )

    @canton_aware()
    def activation_is_draft(self, activation):
        pass

    def activation_is_draft_be(self, activation):
        return (
            activation.circulation_state.name == "RUN"
            and not activation.circulation_answer_id
            and not activation.email_sent
        )

    def activation_is_draft_sz(self, activation):
        return activation.circulation_state.name == "IDLE"

    @canton_aware()
    def activation_has_answer(self, activation):
        pass

    def activation_has_answer_be(self, activation):
        return (
            activation.circulation_answer_id
            and activation.circulation_answer_id != self.config.STATUS_DRAFT
        )

    def activation_has_answer_sz(self, activation):
        return (
            activation.circulation_answer_id
            and activation.circulation_state.name != "IDLE"
        )

    @canton_aware()
    def activations_sent(self, activations):
        pass

    def activations_sent_be(self, activations):
        return activations.exclude(
            circulation_state__name="RUN", circulation_answer__isnull=True, email_sent=0
        )

    def activations_sent_sz(self, activations):
        return activations.exclude(circulation_state__name="IDLE")

    @canton_aware()
    def activations_ready(self, activations):
        pass

    def activations_ready_be(self, activations):
        return activations.filter(circulation_state__name="RUN").exclude(
            circulation_answer__isnull=True, email_sent=0
        )

    def activations_ready_sz(self, activations):
        return activations.filter(circulation_state__name__in=["RUN", "REVIEW"])

    @canton_aware()
    def activations_answered(self, activations):
        pass

    def activations_answered_be(self, activations):
        return activations.filter(
            circulation_state__name__in=["DONE"],
            end_date__isnull=False,
            circulation_answer__isnull=False,
        ).exclude(circulation_answer_id=self.config.STATUS_DRAFT)

    def activations_answered_sz(self, activations):
        return activations.filter(
            circulation_state__name__in=["OK", "DONE"],
            end_date__isnull=False,
            circulation_answer__isnull=False,
        )

    @canton_aware()
    def activation_is_ready(self, activation):
        pass

    def activation_is_ready_be(self, activation):
        return activation.circulation_state.name == "RUN" and (
            activation.circulation_answer_id or activation.email_sent
        )

    def activation_is_ready_sz(self, activation):
        return (
            activation.circulation_state.name == "RUN"
            or activation.circulation_state.name == "REVIEW"
        )

    @canton_aware()
    def activation_is_completed(self, activation):
        pass

    def activation_is_completed_be(self, activation):
        return activation.circulation_state.name == "DONE" and activation.end_date

    def activation_is_completed_sz(self, activation):
        return activation.circulation_state.name == "OK" or (
            activation.circulation_state.name == "DONE" and activation.end_date
        )

    @canton_aware()
    def activation_is_skipped(self, activation, instance):
        return False

    def activation_is_skipped_be(self, activation, instance):
        return (
            activation.circulation_state.name == "DONE" and not activation.end_date
        ) or (
            # Those should have been closed...
            activation.circulation_state.name == "RUN"
            and instance.instance_state.name
            in [
                # rejection was later prevented if the instance had running activations
                "rejected",
                # circulation is over
                "coordination",
                "sb1",
                "sb2",
                "conclusion",
                "finished",
                "evaluated",
                "archived",
            ]
        )

    def activation_is_skipped_sz(self, activation, instance):
        return (
            activation.circulation_state.name == "DONE" and not activation.end_date
        ) or self.case_is_depreciated(instance.case)

    @canton_aware()
    def on_migrate_case(
        self,
        case,
        user,
        activations,
        previous_work_item,
        next_work_item,
        distribution_work_item,
    ):
        pass

    def on_migrate_case_sz(
        self,
        case,
        user,
        activations,
        previous_work_item,
        next_work_item,
        distribution_work_item,
    ):

        # handle depreciated cases
        case_is_depreciated = self.case_is_depreciated(case)

        # create additional-demand work-item or rewrite previous_work_item
        additional_demand_work_item = WorkItem.objects.filter(
            task=self.config.ADDITIONAL_DEMAND_TASK, case=case
        ).first()

        if additional_demand_work_item:
            additional_demand_work_item.previous_work_item = previous_work_item
            additional_demand_work_item.save()
        else:
            additional_demand_work_item = WorkItem.objects.create(
                task=self.config.ADDITIONAL_DEMAND_TASK,
                name=self.config.ADDITIONAL_DEMAND_TASK.name,
                addressed_groups=[user.group],
                assigned_users=self.responsible_user(user.group, case.instance),
                case=case,
                status=(
                    WorkItem.STATUS_CANCELED
                    if next_work_item
                    or (case_is_depreciated and not next_work_item)
                    or (
                        case.instance.previous_instance_state.name
                        in self.config.POST_CIRCULATION_INSTANCE_STATES
                    )
                    else WorkItem.STATUS_READY
                ),
                previous_work_item=previous_work_item,
                meta=self.config.META,
            )

            if previous_work_item:
                additional_demand_work_item.created_at = previous_work_item.closed_at
                additional_demand_work_item.save()

    @canton_aware(include_base_method=True)
    def post_migrate(self):
        WorkItem.objects.filter(task_id=self.config.INQUIRY_TASK.pk).annotate(
            activation_id=Cast("meta__migrated-from-activation-id", IntegerField())
        ).update(
            created_at=Subquery(
                core_models.Activation.objects.filter(
                    pk=OuterRef("activation_id")
                ).values("start_date")[:1]
            )
        )

        Case.objects.filter(workflow_id=self.config.INQUIRY_WORKFLOW).update(
            created_at=Subquery(
                WorkItem.objects.filter(
                    task_id=self.config.INQUIRY_TASK.pk, child_case=OuterRef("pk")
                ).values("created_at")[:1]
            )
        )

    def post_migrate_be(self, result_base_method=None):
        WorkItem.objects.filter(task_id=self.config.FILL_INQUIRY_TASK.pk).update(
            # Joined field references are not permitted in update query
            # therefore directly using case__parent_work_item__created_at
            # isn't possible
            created_at=Subquery(
                WorkItem.objects.filter(
                    task_id=self.config.INQUIRY_TASK.pk,
                    child_case=OuterRef("case"),
                ).values("created_at")[:1]
            ),
        )

    def post_migrate_sz(self, result_base_method=None):
        # TODO: reduce queries
        WorkItem.objects.filter(
            task_id__in=[
                self.config.FILL_INQUIRY_TASK.pk,
                self.config.CHECK_INQUIRY_TASK.pk,
                self.config.REVISE_INQUIRY_TASK.pk,
                self.config.ALTER_INQUIRY_TASK.pk,
            ],
        ).update(
            # Joined field references are not permitted in update query
            # therefore directly using case__parent_work_item__created_at
            # isn't possible
            created_at=DjangoCase(
                When(
                    task_id__in=[self.config.FILL_INQUIRY_TASK.pk],
                    then=Subquery(
                        WorkItem.objects.filter(
                            task_id=self.config.INQUIRY_TASK.pk,
                            child_case=OuterRef("case"),
                        ).values("created_at")[:1]
                    ),
                ),
                When(
                    task_id__in=[
                        self.config.CHECK_INQUIRY_TASK.pk,
                        self.config.REVISE_INQUIRY_TASK.pk,
                    ],
                    then=Subquery(
                        WorkItem.objects.filter(
                            task_id=self.config.FILL_INQUIRY_TASK.pk,
                            case=OuterRef("case"),
                        ).values("closed_at")[:1]
                    ),
                ),
                default=F("created_at"),
            ),
            previous_work_item=DjangoCase(
                When(
                    task_id__in=[
                        self.config.CHECK_INQUIRY_TASK.pk,
                        self.config.REVISE_INQUIRY_TASK.pk,
                    ],
                    then=Subquery(
                        WorkItem.objects.filter(
                            task_id=self.config.FILL_INQUIRY_TASK.pk,
                            case=OuterRef("case"),
                        ).values("pk")[:1]
                    ),
                ),
                default=F("previous_work_item"),
            ),
        )

    @canton_aware(include_base_method=True)
    def initialize_inquiry_answer(
        self, activation, distribution_case, inquiry_work_item, instance
    ):
        child_document = Document(form_id="inquiry-answer")
        child_case = Case(
            workflow_id="inquiry",
            document=child_document,
            status=(
                Case.STATUS_COMPLETED
                if self.activation_is_completed(activation)
                or self.activation_is_skipped(activation, instance)
                else Case.STATUS_RUNNING
            ),
            closed_at=activation.end_date,
            family=distribution_case.family,
        )

        return child_document, child_case

    def initialize_inquiry_answer_be(
        self,
        activation,
        distribution_case,
        inquiry_work_item,
        instance,
        result_base_method=None,
    ):
        child_document, child_case = result_base_method

        work_item = WorkItem(
            task=self.config.FILL_INQUIRY_TASK,
            name=self.config.FILL_INQUIRY_TASK.name,
            case=child_case,
            addressed_groups=[str(activation.service_id)],
            assigned_users=self.responsible_user(activation.service_id, instance),
            status=(
                WorkItem.STATUS_COMPLETED
                if self.activation_is_completed(activation)
                else (
                    WorkItem.STATUS_CANCELED
                    if self.activation_is_skipped(activation, instance)
                    else (
                        WorkItem.STATUS_READY
                        if self.activation_is_ready(activation)
                        else None
                    )
                )
            ),
            closed_at=activation.end_date,
            meta=self.config.META,
        )

        if not work_item.status:
            tqdm.write(f"Inconsistent activation state for activation {activation.pk}")

        return child_document, child_case, [work_item]

    def initialize_inquiry_answer_sz(
        self,
        activation,
        distribution_case,
        inquiry_work_item,
        instance,
        result_base_method=None,
    ):
        child_document, child_case = result_base_method

        activation_state = activation.circulation_state.name
        review_date = core_models.ActivationAnswer.objects.filter(
            activation=activation.pk, chapter=1, question=4, item=1
        ).first()
        activation_answer_draft_completed = review_date.answer if review_date else None

        find_user = (
            lambda chapter, question, item: User.objects.filter(
                groups__service=str(activation.service_id)
            )
            .annotate(fullname=Concat(F("name"), Value(" "), F("surname")))
            .filter(
                fullname=Value(
                    core_models.ActivationAnswer.objects.filter(
                        activation=activation.pk,
                        chapter=chapter,
                        question=question,
                        item=item,
                    )
                    .values_list("answer", flat=True)
                    .first()
                )
            )
            .distinct()
            .values_list("username", flat=True)
            .first()
        )

        assignee = find_user(chapter=1, question=5, item=1)

        if activation_answer_draft_completed:
            try:
                activation_answer_draft_completed = datetime.strptime(
                    activation_answer_draft_completed, "%Y-%m-%d %H:%M:%S%z"
                )
            except ValueError:
                try:
                    timezone = pytz.timezone(settings.TIME_ZONE)
                    activation_answer_draft_completed = timezone.localize(
                        datetime.strptime(
                            activation_answer_draft_completed, "%d.%m.%y %H:%M"
                        )
                    )
                except ValueError:
                    tqdm.write(
                        f"Couldn't parse activation.review_date {activation.review_date} for activation {activation.pk}"
                    )
                    tqdm.write(f"Manually fix {self.config.FILL_INQUIRY_TASK} task")
                    activation_answer_draft_completed = pytz.utc.localize(
                        datetime.combine(datetime.min.date(), datetime.min.time())
                    )

        activation_is_running = activation_state == "RUN"
        activation_is_in_review = activation_state == "REVIEW"
        activation_is_done = activation_state == "DONE"
        case_is_depreciated = self.case_is_depreciated(distribution_case.family)

        work_items = []
        work_items.append(
            WorkItem(
                task=self.config.FILL_INQUIRY_TASK,
                name=self.config.FILL_INQUIRY_TASK.name,
                case=child_case,
                addressed_groups=[str(activation.service_id)],
                assigned_users=self.responsible_user(activation.service_id, instance),
                status=(
                    WorkItem.STATUS_COMPLETED
                    if activation_answer_draft_completed
                    else (
                        WorkItem.STATUS_CANCELED
                        if (
                            activation_is_done and not activation_answer_draft_completed
                        )
                        or case_is_depreciated
                        else (
                            WorkItem.STATUS_READY
                            if activation_is_running
                            and not activation_answer_draft_completed
                            else ""
                        )
                    )
                ),
                meta=self.config.META,
                closed_at=activation_answer_draft_completed,
                closed_by_user=assignee,
                closed_by_group=(
                    str(activation.service_id)
                    if activation_answer_draft_completed
                    else None
                ),
            )
        )

        if activation_answer_draft_completed:
            reviewer = find_user(chapter=1, question=7, item=1)

            inquiry_work_item.closed_by_user = reviewer
            inquiry_work_item.closed_by_group = str(activation.service_id)

            work_items.extend(
                [
                    WorkItem(
                        task=self.config.CHECK_INQUIRY_TASK,
                        name=self.config.CHECK_INQUIRY_TASK.name,
                        case=child_case,
                        addressed_groups=[str(activation.service_id)],
                        controlling_groups=[str(activation.service_id)],
                        assigned_users=self.responsible_user(
                            activation.service_id, instance
                        ),
                        status=(
                            WorkItem.STATUS_COMPLETED
                            if self.activation_is_completed(activation)
                            else (
                                WorkItem.STATUS_CANCELED
                                if self.activation_is_skipped(activation, instance)
                                or activation_is_running
                                else (
                                    WorkItem.STATUS_READY
                                    if activation_is_in_review
                                    else ""
                                )
                            )
                        ),
                        meta=self.config.META,
                        closed_at=activation.end_date,
                        closed_by_user=reviewer,
                        closed_by_group=(
                            str(activation.service_id) if activation.end_date else None
                        ),
                        deadline=pytz.utc.localize(
                            datetime.combine(
                                activation_answer_draft_completed
                                + timedelta(
                                    seconds=self.config.CHECK_INQUIRY_TASK.lead_time
                                ),
                                datetime.min.time(),
                            )
                        ),
                    ),
                    WorkItem(
                        task=self.config.REVISE_INQUIRY_TASK,
                        name=self.config.REVISE_INQUIRY_TASK.name,
                        case=child_case,
                        addressed_groups=[str(activation.service_id)],
                        assigned_users=self.responsible_user(
                            activation.service_id, instance
                        ),
                        meta=self.config.META,
                        status=(
                            WorkItem.STATUS_COMPLETED
                            if activation_is_running
                            else (
                                WorkItem.STATUS_CANCELED
                                if self.activation_is_completed(activation)
                                or self.activation_is_skipped(activation, instance)
                                else (
                                    WorkItem.STATUS_READY
                                    if activation_is_in_review
                                    else ""
                                )
                            )
                        ),
                    ),
                ]
            )

            if activation_is_running:
                work_items.append(
                    WorkItem(
                        task=self.config.ALTER_INQUIRY_TASK,
                        name=self.config.ALTER_INQUIRY_TASK.name,
                        case=child_case,
                        addressed_groups=[str(activation.service_id)],
                        controlling_groups=[str(activation.service_id)],
                        assigned_users=self.responsible_user(
                            activation.service_id, instance
                        ),
                        meta=self.config.META,
                        status=(
                            WorkItem.STATUS_CANCELED
                            if case_is_depreciated
                            else WorkItem.STATUS_READY
                        ),
                        deadline=pytz.utc.localize(
                            datetime.combine(
                                datetime.now().date(),
                                datetime.min.time(),
                            )
                        ),
                    )
                )

        if any(not work_item.status for work_item in work_items):
            tqdm.write(f"Inconsistent activation state for activation {activation.pk}")

        return child_document, child_case, work_items

    def responsible_user(self, service_id, instance):
        responsible = self._responsible.get((service_id, instance.pk))

        if responsible is None:
            responsible = list(
                ResponsibleService.objects.filter(
                    instance=instance, service_id=service_id
                ).values_list("responsible_user__username", flat=True)
            )

            self._responsible[(service_id, instance.pk)] = responsible

        return responsible
