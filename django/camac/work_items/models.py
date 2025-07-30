from functools import partial
from typing import Any

import uuid_extensions
from caluma.caluma_form.models import Answer, AnswerDocument, DynamicOption
from caluma.caluma_workflow.models import Case as CalumaCase, WorkItem
from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models import Case, Exists, F, OuterRef, Q, Value, When
from django.db.models.functions import Cast, Concat, JSONObject, Trim
from django.utils.translation import get_language, gettext_lazy as _
from localized_fields.fields import LocalizedCharField

from camac.instance.export.filters import StringAggSubquery, caluma_answer
from camac.models import dynamic_default_value
from camac.settings.modules.work_item_list_schema import (
    AnnotationsConfig,
    PersonConfig,
)
from camac.user.models import Service, User


@dynamic_default_value(0)
def next_sort(model_name=None):
    # Previous migrations rely on this method without
    # passing a value for model_name
    if not model_name:
        return 0  # pragma: no cover

    model = apps.get_model("work_items", model_name)
    last = model.objects.order_by("-sort").values_list("sort", flat=True).first()

    return last + 1 if last else 0


class WorkItemTemplateQuerySet(models.QuerySet["WorkItemTemplate"]):
    def for_service(self, service: Service) -> models.QuerySet["WorkItemTemplate"]:
        return self.filter(
            # Template for current service
            Q(services=service)
            # Template for current service group
            | Q(service_groups=service.service_group)
            # Global template
            | Q(services__isnull=True, service_groups__isnull=True)
        )


class WorkItemTemplate(models.Model):
    class ResponsibilityRuleChoices(models.TextChoices):
        NONE = "NONE", _("No service")
        RESPONSIBLE_USER = (
            "RESPONSIBLE_USER",
            _("Current service and responsible user (if exists)"),
        )
        CURRENT_USER = "CURRENT_USER", _("Current service and current user")
        SPECIFIC_USER = "SPECIFIC_USER", _("Current service and specific user")
        NO_USER = "NO_USER", _("Current service and no user")

    id = models.UUIDField(
        primary_key=True,
        default=uuid_extensions.uuid7,
        editable=False,
        verbose_name=_("ID"),
    )
    sort = models.PositiveIntegerField(default=partial(next_sort, "WorkItemTemplate"))
    services = models.ManyToManyField(
        "user.Service",
        blank=True,
        verbose_name=_("Services"),
    )
    service_groups = models.ManyToManyField(
        "user.ServiceGroup",
        blank=True,
        verbose_name=_("Service groups"),
    )
    name = models.CharField(
        blank=False,
        null=False,
        verbose_name=_("Name"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
    )
    lead_time = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Lead time in days"),
        help_text=_(
            "The current date in addition to this value will determine the deadline"
        ),
    )
    responsibility_rule = models.CharField(
        choices=ResponsibilityRuleChoices.choices,
        max_length=20,
        verbose_name=_("Responsibility rule"),
    )
    assigned_user = models.ForeignKey(
        "user.User",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Assigned user"),
        help_text=_(
            'The assigned user will only be considered if the responsibility rule "%(rule)s" is selected above'
        )
        % dict(rule=ResponsibilityRuleChoices.SPECIFIC_USER.label),
    )

    objects: WorkItemTemplateQuerySet = WorkItemTemplateQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Work item template")
        verbose_name_plural = _("Work item templates")
        ordering = ["sort"]


class WorkItemListFilterPreset(models.Model):
    class PresetCategoryChoices(models.TextChoices):
        STANDARD = "STANDARD", _("Standard filter preset category")
        SERVICE = (
            "SERVICE",
            _("Service filter preset category"),
        )
        SERVICE_GROUP = "SERVICE_GROUP", _("Service group filter preset category")

    id = models.UUIDField(
        primary_key=True,
        default=uuid_extensions.uuid7,
        editable=False,
        verbose_name=_("ID"),
    )
    sort = models.PositiveIntegerField(
        default=partial(next_sort, "WorkItemListFilterPreset")
    )
    name = LocalizedCharField(verbose_name=_("Name"))
    services = models.ManyToManyField(
        "user.Service",
        blank=True,
        verbose_name=_("Services"),
    )
    service_groups = models.ManyToManyField(
        "user.ServiceGroup",
        blank=True,
        verbose_name=_("Service groups"),
    )
    query_params = models.JSONField(verbose_name=_("Query params"))
    prefilter_work_item_templates = models.BooleanField(
        default=False, verbose_name=_("Prefilter work item templates")
    )
    work_item_templates = models.ManyToManyField(
        "work_items.WorkItemTemplate",
        related_name="filter_presets",
        blank=True,
        verbose_name=_("Work item templates"),
    )
    prefilter_tasks = models.BooleanField(
        default=False, verbose_name=_("Prefilter tasks")
    )
    tasks = models.ManyToManyField(
        "caluma_workflow.Task",
        related_name="+",
        blank=True,
        verbose_name=_("Tasks"),
    )

    def __str__(self):
        return self.name.get()

    class Meta:
        verbose_name = _("Work item list filter preset")
        verbose_name_plural = _("Work item list filter presets")
        ordering = ["sort"]


class WorkItemListRowQuerySet(models.QuerySet["WorkItemListRow"]):
    def count(self) -> int:
        """Override count method to avoid unnecessary annotations in the query.

        The base queryset is already adding all the necessary annotations for
        displaying the model properly. However, some of those annotations can be
        a bit costly and should be avoided if not necessary. For the pagination,
        we do a count on the base queryset - for this purpose we make sure to
        only count the PKs and avoid annotations and joins completely.
        """

        # We explicitly create a new query that completely ignores the proxy
        # model in order to avoid all annotations and joins.

        # WARNING: If there was ever a use-case where we'd filter by any
        # annotated properties (don't do this, it would not perform at all) this
        # method would break.
        queryset = WorkItem.objects.all()
        queryset.query.where = self.query.where
        return queryset.values("pk").count()


class WorkItemListRowManager(models.Manager["WorkItemListRow"]):
    def get_queryset(self):
        """Override base queryset for work item list rows to annotate the needed data.

        The goal of this queryset is to annotate as much of the needed
        information for the work item list as possible on the DB instead of
        writing serializer code. This queryset should contain all information
        for using a work item list row without the serializer.
        """

        # This may contain highly complex and often performance expensive
        # annotations - however, it's still alot faster than gathering and
        # computing this information on the serializers (or somewhere else). The
        # idea is, that this queryset becomes much slimmer, as soon as we
        # denormalize this information.

        # If we achieve this, we can just remove the complex annotations after
        # denormalizing and don't need to touch the serializers and views. That's
        # the ultimate long-term goal of this approach.

        annotations: AnnotationsConfig = settings.WORK_ITEM_LIST.annotations

        queryset = super().get_queryset()

        queryset = (
            queryset.select_related("task")
            .filter(deadline__isnull=False)
            .annotate(
                instance_id=F("case__family__instance__pk"),
                instance_name=F(
                    f"case__family__document__form__name__{get_language()}"
                ),
                special_id=annotations.special_id,
                assigned_user=F("assigned_users__0"),
                addressed_service=Cast(
                    F("addressed_groups__0"), output_field=models.IntegerField()
                ),
                controlling_service=Cast(
                    F("controlling_groups__0"), output_field=models.IntegerField()
                ),
                instance_description=caluma_answer(
                    annotations.description, "case__family__document_id"
                ),
                municipality=self._annotate_municipality(),
                applicants=self._annotate_applicants(),
                direct_link_config=F("task__meta__directLink"),
                direct_link_models=self._annotate_direct_link_models(),
            )
        )

        return queryset

    def _annotate_municipality(self) -> DynamicOption:
        """Annotate the municipality name from the main form.

        Since the municipality is a dynamic option, we annotate the selected
        label from the dynamic option model in the correct language.
        """

        annotations: AnnotationsConfig = settings.WORK_ITEM_LIST.annotations

        return (
            DynamicOption.objects.filter(
                question_id=annotations.municipality,
                document_id=OuterRef("case__family__document_id"),
            )
            .order_by("-created_at")
            .values(f"label__{get_language()}")[:1]
        )

    def _annotate_applicants(self) -> StringAggSubquery | Value:
        """Annotate a comma separated list of applicant names.

        This will sanitize and compile all applicants from the main form of a
        work item. It also considers whether each applicant is a juristic person
        or not and will change the display value accordingly.
        """

        applicants_config: PersonConfig = settings.WORK_ITEM_LIST.annotations.applicants

        if applicants_config is None:
            return Value(None, output_field=models.CharField())

        return StringAggSubquery(
            AnswerDocument.objects.filter(
                answer__question_id=applicants_config.table_question,
                answer__document_id=OuterRef("case__family__document_id"),
            )
            .annotate(
                is_juristic=Exists(
                    Answer.objects.filter(
                        question_id=applicants_config.is_juristic,
                        document_id=OuterRef("document_id"),
                        value=applicants_config.is_juristic_yes,
                    )
                ),
                name=Case(
                    When(
                        is_juristic=True,
                        then=caluma_answer(
                            applicants_config.juristic_name, "document_id"
                        ),
                    ),
                    default=Trim(
                        Concat(
                            caluma_answer(applicants_config.first_name, "document_id"),
                            Value(" "),
                            caluma_answer(applicants_config.last_name, "document_id"),
                        )
                    ),
                ),
            )
            .values("name"),
            column_name="name",
            delimiter=", ",
        )

    def _annotate_direct_link_models(self) -> JSONObject:
        """Annotate all needed properties to generate a direct link."""

        INQUIRY_ANNOTATION = WorkItem.objects.filter(
            Q(task_id=settings.DISTRIBUTION["INQUIRY_TASK"])
            & Q(Q(pk=OuterRef("pk")) | Q(pk=OuterRef("case__parent_work_item")))
        )
        CONSTRUCTION_STEP_ANNOTATION = WorkItem.objects.filter(
            Q(**{"meta__construction-step-id__isnull": False})
            & Q(Q(pk=OuterRef("pk")) | Q(pk=OuterRef("case__parent_work_item")))
        )

        return JSONObject(
            instance_id=F("instance_id"),
            task_slug=F("task_id"),
            distribution_case_uuid=CalumaCase.objects.filter(
                Q(workflow_id=settings.DISTRIBUTION["DISTRIBUTION_WORKFLOW"])
                & Q(
                    Q(pk=OuterRef("case"))
                    | Q(pk=OuterRef("case__parent_work_item__case"))
                )
            ).values("pk")[:1],
            inquiry_uuid=INQUIRY_ANNOTATION.values("pk")[:1],
            inquiry_addressed=Cast(
                INQUIRY_ANNOTATION.values("addressed_groups__0")[:1],
                output_field=models.IntegerField(),
            ),
            inquiry_controlling=Cast(
                INQUIRY_ANNOTATION.values("controlling_groups__0")[:1],
                output_field=models.IntegerField(),
            ),
            construction_stage_uuid=CONSTRUCTION_STEP_ANNOTATION.values(
                "case__parent_work_item__pk"
            )[:1],
            construction_step_id=CONSTRUCTION_STEP_ANNOTATION.values(
                "meta__construction-step-id"
            )[:1],
        )


class WorkItemListRow(WorkItem):
    """Proxy model representing a row in the work item list.

    The manager of this model makes sure that all information needed to display
    this work item exists on the model. It also includes methods that are used
    as quick actions in the work item list.
    """

    objects: WorkItemListRowQuerySet = WorkItemListRowManager.from_queryset(
        WorkItemListRowQuerySet
    )()

    @property
    def is_ready(self) -> bool:
        return self.status == WorkItem.STATUS_READY

    @property
    def is_manually_completable(self) -> bool:
        return self.task.meta.get("is-manually-completable", False)

    @property
    def unread(self) -> bool:
        return self.meta.get("not-viewed", True)

    @property
    def edit_link(self) -> dict[str, str | list[int | str]]:
        return {
            "route": "cases.detail.work-items.edit",
            "models": [self.instance_id, str(self.pk)],
        }

    @property
    def direct_link(self) -> dict[str, str | list[Any]] | None:
        """Direct link to jump to the respective frontend module.

        If a direct link is configured on the task, this property will compile
        the needed models for the frontend to generate a link directly to the
        frontend module of that work item.
        """

        config = self.direct_link_config

        if self.status != WorkItem.STATUS_READY or not config:
            return None

        return {
            "route": config["route"],
            "models": [
                self.direct_link_models.get(placeholder.lower(), placeholder)
                for placeholder in config["models"]
            ],
        }

    def assign_to_user(self, user: User):
        self.assigned_users = [str(user.username)]
        self.save(update_fields=["assigned_users"])

        # Update annotated value manually to avoid running the expensive
        # annotated query again
        self.assigned_user = str(user.username)

    def toggle_read(self):
        self.meta["not-viewed"] = not self.meta.get("not-viewed", False)
        self.save(update_fields=["meta"])

    class Meta:
        proxy = True
