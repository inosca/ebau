from itertools import chain

from caluma.caluma_form.models import Answer, Document
from caluma.caluma_workflow.models import Case, WorkItem
from django.conf import settings
from django.contrib.postgres.aggregates import JSONBAgg
from django.contrib.postgres.fields import JSONField
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import (
    CharField,
    Count,
    Exists,
    F,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    Value,
)
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast, Concat

from camac.core.models import Activation, Circulation, Notice
from camac.instance.models import Instance


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.faulty_instances = []

    def add_arguments(self, parser):
        parser.add_argument("--clean", dest="clean", action="store_true", default=False)
        parser.add_argument(
            "--samples", dest="samples", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["samples"]:
            self._get_edge_case_samples()
        else:
            self._check_activation_count()
            self._check_create_inquiry_services()
            self._check_complete_distribution()
            self._check_pre_circulation()
            self._check_ready_work_items_only_in_circulation()
            self._check_distribution_work_items()
            self._check_check_inquiries_services()
            self._check_inquiry_answer_distribution_completed()
            self._check_inquiry_answer()

        if len(self.faulty_instances):
            self.stdout.write()
            self.stdout.write(
                self.style.WARNING(f"{len(self.faulty_instances)} faulty instances")
            )

            if options["clean"]:
                self.stdout.write(
                    self.style.WARNING(
                        "Deleting migrated distribution for faulty instances"
                    )
                )

                Case.objects.filter(
                    workflow_id__in=[
                        settings.DISTRIBUTION["DISTRIBUTION_WORKFLOW"],
                        settings.DISTRIBUTION["INQUIRY_WORKFLOW"],
                    ],
                    family__instance__in=self.faulty_instances,
                ).delete()

                WorkItem.objects.filter(
                    task_id=settings.DISTRIBUTION["DISTRIBUTION_TASK"],
                    case__instance__in=self.faulty_instances,
                ).delete()

                Answer.objects.filter(
                    document__case__family__instance__in=self.faulty_instances,
                    document__form_id__in=["inquiry-answer", "inquiry"],
                ).delete()

                Document.objects.filter(
                    case__family__instance__in=self.faulty_instances,
                    form_id__in=["inquiry-answer", "inquiry"],
                ).delete()

    def _format_instance(self, instance):
        info = filter(
            None,
            [
                instance.identifier or instance.case.meta.get("ebau-number"),
                instance.instance_state.get_name(),
                instance.responsible_service(filter="municipality").get_name(),
            ],
        )

        return f"Instance {instance.pk} ({', '.join(info)})"

    def _log_instance(self, instance, info):
        self.faulty_instances.append(instance.pk)

        self.stdout.write(f"\t- {self._format_instance(instance)}: {info}")

    def _log_analysis_result(self, label, condition, additional_information=[]):
        result = (
            self.style.SUCCESS("PASSED")
            if bool(condition)
            else self.style.ERROR("FAILED")
        )

        self.stdout.write(f"{label}: {result}")

        for info in additional_information:
            self.stdout.write(f"\t- {info}")

    def _check_activation_count(self):
        activation_count = Activation.objects.count()
        inquiry_count = WorkItem.objects.filter(task_id="inquiry").count()

        condition = activation_count == inquiry_count

        self._log_analysis_result(
            "There is the same amount of inquiries as there are activations", condition
        )

        if not condition:
            unmigrated_activations = Activation.objects.exclude(
                pk__in=WorkItem.objects.filter(
                    **{
                        "task_id": settings.DISTRIBUTION["INQUIRY_TASK"],
                        "meta__migrated-from-activation-id__isnull": False,
                    }
                )
                .annotate(
                    activation_id=Cast(
                        KeyTextTransform("migrated-from-activation-id", "meta"),
                        IntegerField(),
                    )
                )
                .values("activation_id")
            )

            self.stdout.write(
                f"Unmigrated activations: {unmigrated_activations.count()}"
            )

            for instance in Instance.objects.filter(
                pk__in=unmigrated_activations.values_list(
                    "circulation__instance__pk", flat=True
                )
            ).order_by("pk"):
                self._log_instance(
                    instance,
                    f"{Activation.objects.filter(circulation__instance=instance).count()} activations",
                )

    def _check_create_inquiry_services(self):
        create_inquiry_work_items = WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_CREATE_TASK"]
        ).annotate(
            addressed_groups_count=Count("addressed_groups"),
            duplicate_id=Concat(
                F("addressed_groups"),
                Value("-"),
                F("case__family__instance__pk"),
                output_field=CharField(),
            ),
        )

        create_inquiry_unique_addressed_service = create_inquiry_work_items.exclude(
            addressed_groups_count=1
        )
        create_inquiry_unique_addressed_service_exists = (
            create_inquiry_unique_addressed_service.exists()
        )
        self._log_analysis_result(
            "There is always only one addressed service on create inquiry work items",
            not create_inquiry_unique_addressed_service_exists,
        )

        if create_inquiry_unique_addressed_service_exists:
            for instance in Instance.objects.filter(
                pk__in=create_inquiry_unique_addressed_service.values(
                    "case__family__instance"
                )
            ).order_by("pk"):

                work_items = ""
                for work_item in create_inquiry_unique_addressed_service:
                    work_items += f"{work_item.task_id} {work_item.status} {work_item.addressed_groups} | "

                self._log_instance(instance, ", ".join(work_items))

        single_create_inquiry_per_service = create_inquiry_work_items.count() == len(
            set(create_inquiry_work_items.values_list("duplicate_id", flat=True))
        )
        self._log_analysis_result(
            "There is only one create inquiry work item per service per instance",
            single_create_inquiry_per_service,
        )

        if not single_create_inquiry_per_service:
            duplicates = WorkItem.objects.filter(
                Exists(
                    WorkItem.objects.filter(
                        task_id=settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
                        addressed_groups=OuterRef("addressed_groups"),
                        case__family__instance=OuterRef("case__family__instance"),
                    ).exclude(pk=OuterRef("pk"))
                ),
                task_id=settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
            )

            for instance in Instance.objects.filter(
                pk__in=duplicates.values("case__family__instance")
            ).order_by("pk"):
                work_items = ""
                for work_item in duplicates.filter(case__family__instance=instance):
                    work_items += f"{work_item.task_id} {work_item.status} {work_item.addressed_groups} | "

                self._log_instance(instance, work_items)

    def _check_check_inquiries_services(self):
        work_items = (
            WorkItem.objects.filter(
                task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                status=WorkItem.STATUS_COMPLETED,
            )
            .annotate(
                check_inquiries_count=Subquery(
                    WorkItem.objects.filter(
                        task_id=settings.DISTRIBUTION["INQUIRY_CHECK_TASK"],
                        case_id=OuterRef("case_id"),
                        addressed_groups=OuterRef("controlling_groups"),
                    )
                    .annotate(count=Count("*"))
                    .values("count")
                )
            )
            .exclude(check_inquiries_count=1)
        )

        work_items_exists = work_items.exists()
        self._log_analysis_result(
            "A check-inquiries exists for every controlling group that has received an answer",
            not work_items_exists,
        )

        if work_items_exists:
            for instance in Instance.objects.filter(
                pk__in=work_items.values("case__family__instance")
            ):
                self._log_instance(
                    instance,
                    f"No check-inquiries work item for services: {','.join(chain(*work_items.values_list('controlling_groups', flat=True)))}",
                )

    def _check_complete_distribution(self):
        instances = (
            Instance.objects.filter(
                instance_state__name__in=[
                    "nfd",
                    "circ",
                    "comm",
                    "circulation",
                    "circulation_init",
                ]
            )
            .annotate(
                complete_distribution_count=Subquery(
                    WorkItem.objects.filter(
                        task_id=settings.DISTRIBUTION["DISTRIBUTION_COMPLETE_TASK"],
                        case__family__instance=OuterRef("pk"),
                        status=WorkItem.STATUS_READY,
                    )
                    .annotate(count=Count("*"))
                    .values("count")
                )
            )
            .exclude(complete_distribution_count=1)
        )

        self._log_analysis_result(
            "There is a ready complete distribution work item for instances in circulation",
            not instances.exists(),
        )

        for instance in instances.order_by("pk"):
            self._log_instance(
                instance,
                f"{instance.complete_distribution_count} complete distribution work items",
            )

    def _check_pre_circulation(self):
        instances = Instance.objects.annotate(
            init_distribution_count=Subquery(
                WorkItem.objects.filter(
                    task_id=settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
                    case__family__instance=OuterRef("pk"),
                    status=WorkItem.STATUS_READY,
                )
                .annotate(count=Count("*"))
                .values("count")
            ),
            inquiry_count=Subquery(
                WorkItem.objects.filter(
                    task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                    case__family__instance=OuterRef("pk"),
                )
                .exclude(status=WorkItem.STATUS_SUSPENDED)
                .annotate(count=Count("*"))
                .values("count")
            ),
        )

        pre_instances = instances.filter(
            instance_state__name__in=["comm", "circulation_init"]
        )
        not_pre_instances = instances.exclude(
            Q(instance_state__name__in=["comm", "circulation_init"])
            | (
                Q(instance_state__name="circ")
                & ~Q(
                    Exists(
                        Activation.objects.filter(circulation__instance=OuterRef("pk"))
                    )
                )
            )
        ).exclude(init_distribution_count=0)

        faulty_pre_instances = pre_instances.exclude(
            init_distribution_count__isnull=False, init_distribution_count=1
        )
        self._log_analysis_result(
            "There is a ready init distribution work item for instances pre circulation",
            not faulty_pre_instances.exists(),
        )

        for instance in Instance.objects.filter(
            pk__in=faulty_pre_instances.values_list("pk", flat=True)
        ):
            init_work_items = [
                f"{w.task_id} ({w.status})"
                for w in WorkItem.objects.filter(
                    case__family__instance=instance.pk,
                    task_id=settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
                )
            ]
            self._log_instance(instance, ", ".join(init_work_items))

        self._log_analysis_result(
            "There are only suspended (unsent) inquiries for instances pre circulation",
            not pre_instances.exclude(inquiry_count=0).exists(),
        )

        self._log_analysis_result(
            "There are no init distribution work items for instances in / post circulation",
            not not_pre_instances.exists(),
        )

        for instance in not_pre_instances:
            self._log_instance(
                instance,
                f"{instance.init_distribution_count} ready init distribution work items",
            )

    def _check_ready_work_items_only_in_circulation(self):
        distribution_tasks = [
            settings.DISTRIBUTION["DISTRIBUTION_TASK"],
            settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
            settings.DISTRIBUTION["DISTRIBUTION_COMPLETE_TASK"],
            settings.DISTRIBUTION["INQUIRY_TASK"],
            settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
            settings.DISTRIBUTION["INQUIRY_CHECK_TASK"],
            settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
        ]

        if settings.APPLICATION_NAME == "kt_schwyz":
            distribution_tasks += [
                settings.DISTRIBUTION["INQUIRY_ANSWER_CHECK_TASK"],
                settings.DISTRIBUTION["INQUIRY_ANSWER_REVISE_TASK"],
                settings.DISTRIBUTION["INQUIRY_ANSWER_ALTER_TASK"],
            ]

        work_items = WorkItem.objects.filter(
            task_id__in=distribution_tasks,
            status__in=[WorkItem.STATUS_READY, WorkItem.STATUS_SUSPENDED],
        ).exclude(
            Q(
                case__family__instance__instance_state__name__in=[
                    "nfd",
                    "circ",
                    "comm",
                    "circulation",
                    "circulation_init",
                ]
            )
            | Q(
                # Instances in state correction or rejected will have suspended control work items (but not inquiries)
                Q(
                    case__family__instance__instance_state__name__in=[
                        "correction",
                        "rejected",
                    ]
                )
                & ~Q(
                    task_id__in=[
                        settings.DISTRIBUTION["INQUIRY_TASK"],
                        settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
                    ]
                )
                & ~Q(status=WorkItem.STATUS_READY)
            )
        )

        self._log_analysis_result(
            "There are only suspended or ready distribution work items for instances pre or in circulation",
            not work_items.exists(),
        )

        for instance in Instance.objects.filter(
            pk__in=work_items.values("case__family__instance")
        ).order_by("pk"):
            active_work_items = [
                f"{i.task_id} ({i.status})"
                for i in work_items.filter(case__family__instance=instance)
            ]

            self._log_instance(instance, ", ".join(active_work_items))

    def _check_distribution_work_items(self):
        instances = (
            Instance.objects.filter(
                Exists(Circulation.objects.filter(instance=OuterRef("pk"))[:1])
            )
            .annotate(
                distribution_count=Subquery(
                    WorkItem.objects.filter(
                        task_id=settings.DISTRIBUTION["DISTRIBUTION_TASK"],
                        case__family__instance=OuterRef("pk"),
                    )
                    .annotate(count=Count("*"))
                    .values("count")
                ),
                init_distribution_count=Subquery(
                    WorkItem.objects.filter(
                        task_id=settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
                        case__family__instance=OuterRef("pk"),
                    )
                    .annotate(count=Count("*"))
                    .values("count")
                ),
                complete_distribution_count=Subquery(
                    WorkItem.objects.filter(
                        task_id=settings.DISTRIBUTION["DISTRIBUTION_COMPLETE_TASK"],
                        case__family__instance=OuterRef("pk"),
                    )
                    .annotate(count=Count("*"))
                    .values("count")
                ),
            )
            .exclude(init_distribution_count=1)
            .exclude(complete_distribution_count=1)
            .exclude(distribution_count=1)
            .exclude(
                Exists(
                    WorkItem.objects.filter(
                        task_id=settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
                        case__family__instance=OuterRef("pk"),
                    )
                )
            )
        )

        work_items = WorkItem.objects.filter(
            task_id__in=[
                settings.DISTRIBUTION["DISTRIBUTION_TASK"],
                settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
                settings.DISTRIBUTION["DISTRIBUTION_COMPLETE_TASK"],
                settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
            ]
        )

        self._log_analysis_result(
            "All distribution work-items exist for instances with a circulation",
            not instances.exists(),
        )

        for instance in instances.order_by("pk"):
            active_work_items = [
                f"{i.task_id} ({i.status})"
                for i in work_items.filter(case__family__instance=instance)
            ]
            self._log_instance(instance, ", ".join(active_work_items))

    def _check_inquiry_answer_distribution_completed(self):
        inquiry_answer_tasks = [
            settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
        ]

        if settings.APPLICATION_NAME == "kt_schwyz":
            inquiry_answer_tasks += [
                settings.DISTRIBUTION["INQUIRY_ANSWER_CHECK_TASK"],
                settings.DISTRIBUTION["INQUIRY_ANSWER_REVISE_TASK"],
                settings.DISTRIBUTION["INQUIRY_ANSWER_ALTER_TASK"],
            ]

        undone_work_items = (
            WorkItem.objects.filter(task_id=settings.DISTRIBUTION["INQUIRY_TASK"])
            .exclude(status=WorkItem.STATUS_READY)
            .filter(
                Exists(
                    WorkItem.objects.filter(
                        case__parent_work_item=OuterRef("pk"),
                        task_id__in=inquiry_answer_tasks,
                        status=WorkItem.STATUS_READY,
                    )
                ),
            )
        )

        no_ready_work_items = WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"], status=WorkItem.STATUS_READY
        ).exclude(
            Exists(
                WorkItem.objects.filter(
                    case__parent_work_item=OuterRef("pk"),
                    task_id__in=inquiry_answer_tasks,
                    status=WorkItem.STATUS_READY,
                )
            ),
        )

        undone_work_items_exists = undone_work_items.exists()
        self._log_analysis_result(
            "There are no ready inquiry answer work-items belonging to a no longer running inquiry",
            not undone_work_items_exists,
        )

        if undone_work_items_exists:
            instances = Instance.objects.filter(
                pk__in=undone_work_items.values("case__family__instance")
            )
            for instance in instances.order_by("pk"):
                active_work_items = [
                    f"{i.task_id} ({i.status})"
                    for i in undone_work_items.filter(case__family__instance=instance)
                ]
                self._log_instance(instance, ", ".join(active_work_items))

        no_ready_work_items_exists = no_ready_work_items.exists()
        self._log_analysis_result(
            "There is always at least one ready inquiry answer work-item belonging to a running inquiry",
            not no_ready_work_items_exists,
        )

        if no_ready_work_items_exists:
            instances = Instance.objects.filter(
                pk__in=no_ready_work_items.values("case__family__instance")
            )
            for instance in instances.order_by("pk"):
                active_work_items = [
                    f"{i.task_id} ({i.status})"
                    for i in no_ready_work_items.filter(case__family__instance=instance)
                ]
                self._log_instance(instance, ", ".join(active_work_items))

    def _check_inquiry_answer(self):

        answer_status_draft_be = 20000

        circulation_answer_count = (
            Activation.objects.filter(circulation_answer__isnull=False)
            .exclude(circulation_answer=answer_status_draft_be)
            .count()
        )

        inquiry_answer_status_count = Answer.objects.filter(
            question__slug="inquiry-answer-status"
        ).count()

        self._log_analysis_result(
            "There are the same amount of activation circulation answers as inquiry status answers",
            circulation_answer_count == inquiry_answer_status_count,
        )

        notices_count = Notice.objects.count()

        inquiry_answer_count = (
            Answer.objects.filter(question__slug__startswith="inquiry-answer-")
            .exclude(question__slug="inquiry-answer-status")
            .count()
        )

        self._log_analysis_result(
            "There are the same amount of activation notices as inquiry answers",
            notices_count == inquiry_answer_count,
        )

        work_items_status = (
            WorkItem.objects.filter(
                **{
                    "task_id": settings.DISTRIBUTION["INQUIRY_TASK"],
                    "meta__migrated-from-activation-id__isnull": False,
                }
            )
            .annotate(
                activation_id=Cast(
                    KeyTextTransform("migrated-from-activation-id", "meta"),
                    IntegerField(),
                ),
            )
            .annotate(
                activation_circulation_answer=Subquery(
                    Activation.objects.filter(pk=OuterRef("activation_id"))[:1].values(
                        "circulation_answer"
                    )
                ),
                inquiry_status=Answer.objects.filter(
                    document__case__parent_work_item=OuterRef("pk"),
                    question_id="inquiry-answer-status",
                )[:1].values("value"),
            )
            .exclude(
                activation_circulation_answer__isnull=True, inquiry_status__isnull=True
            )
            .exclude(
                activation_circulation_answer__isnull=False,
                inquiry_status__0__startswith="inquiry-answer-status-",
            )
        )

        work_items_status_count = work_items_status.count()
        self._log_analysis_result(
            "All activations with a circulation answer are mapped to an inquiry status answer",
            not work_items_status_count,
        )

        if work_items_status_count:
            instances = Instance.objects.filter(
                pk__in=work_items_status.values("case__family__instance__pk")
            )

            for instance in instances:
                active_work_items = [
                    f"{i.task_id} ({i.status})"
                    for i in work_items_status.filter(
                        case__family__instance__pk=instance.pk
                    )
                ]
                self._log_instance(instance, ", ".join(active_work_items))

        activations = Activation.objects.annotate(
            activation_notices=JSONBAgg("notices__content", ordering="notices__content")
        )

        documents = Document.objects.filter(form_id="inquiry-answer").annotate(
            inquiry_answers=JSONBAgg(
                "answers__value",
                ordering="answers__value",
                filter=Q(answers__question__slug__startswith="inquiry-answer-")
                & ~Q(answers__question__slug="inquiry-answer-status"),
            )
        )

        work_items_answers = (
            WorkItem.objects.filter(
                **{
                    "task_id": settings.DISTRIBUTION["INQUIRY_TASK"],
                    "meta__migrated-from-activation-id__isnull": False,
                }
            )
            .annotate(
                activation_id=Cast(
                    KeyTextTransform("migrated-from-activation-id", "meta"),
                    IntegerField(),
                ),
            )
            .annotate(
                activation_answer=Cast(
                    activations.filter(pk=OuterRef("activation_id")).values(
                        "activation_notices"
                    ),
                    JSONField(),
                ),
                inquiry_answer=Cast(
                    documents.filter(case__parent_work_item=OuterRef("pk")).values(
                        "inquiry_answers"
                    ),
                    JSONField(),
                ),
            )
            .exclude(activation_answer=F("inquiry_answer"))
        )

        work_items_answers_count = work_items_answers.count()
        self._log_analysis_result(
            "All notices are mapped to an inquiry answer", not work_items_answers_count
        )

        if work_items_answers_count:
            instances = Instance.objects.filter(
                pk__in=work_items_answers.values("case__family__instance__pk")
            )

            for instance in instances:
                active_work_items = [
                    f"{i.pk} {i.task_id} ({i.status})"
                    for i in work_items_answers.filter(
                        case__family__instance__pk=instance.pk
                    )
                ]
                self._log_instance(instance, ", ".join(active_work_items))

    def _get_edge_case_samples(self):
        self.stdout.write(self.style.WARNING("Edge case samples:"))

        has_running_activation = Exists(
            Activation.objects.filter(
                circulation_state__name="RUN", circulation__instance=OuterRef("pk")
            )
        )

        self.stdout.write("Rejected instance with running activations:")
        for instance in (
            Instance.objects.filter(instance_state__name="rejected")
            .filter(has_running_activation)
            .order_by("pk")
        ):
            self.stdout.write(f"\t - {self._format_instance(instance)}")

        self.stdout.write("Archived instance with running activations:")
        for instance in (
            Instance.objects.filter(instance_state__name="archived")
            .filter(has_running_activation)
            .order_by("pk")
        ):
            self.stdout.write(f"\t - {self._format_instance(instance)}")
