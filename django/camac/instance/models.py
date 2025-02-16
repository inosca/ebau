import logging
from functools import cached_property

import reversion
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import models
from django.db.models import Q

from camac.core.models import HistoryActionConfig
from camac.core.utils import canton_aware
from camac.instance.master_data import MasterData
from camac.user.models import Service, User
from camac.user.permissions import get_role_name
from camac.utils import build_url

from ..core import models as core_models

log = logging.getLogger(__name__)


class FormState(models.Model):
    form_state_id = models.AutoField(db_column="FORM_STATE_ID", primary_key=True)
    name = models.CharField(db_column="NAME", max_length=50)

    class Meta:
        managed = True
        db_table = "FORM_STATE"


class Form(core_models.MultilingualModel, models.Model):
    """Represents type of a form."""

    form_id = models.AutoField(db_column="FORM_ID", primary_key=True)
    form_state = models.ForeignKey(
        FormState, models.DO_NOTHING, db_column="FORM_STATE_ID", related_name="+"
    )
    name = models.CharField(db_column="NAME", max_length=500, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )
    family = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        db_column="FAMILY",
        related_name="+",
        blank=False,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "FORM"


class FormT(models.Model):
    form = models.ForeignKey(
        Form, models.CASCADE, db_column="FORM_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=500, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "FORM_T"


class InstanceState(core_models.MultilingualModel, models.Model):
    instance_state_id = models.AutoField(
        db_column="INSTANCE_STATE_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)
    sort = models.IntegerField(db_column="SORT", db_index=True, default=0)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "INSTANCE_STATE"


class InstanceStateT(models.Model):
    instance_state = models.ForeignKey(
        InstanceState,
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "INSTANCE_STATE_T"


class InstanceStateDescription(models.Model):
    """
    Instance state description.

    Obsolete as integrated into core now. Still added for backwards
    compatability with Kanton URI project.
    """

    instance_state = models.OneToOneField(
        InstanceState,
        models.DO_NOTHING,
        db_column="INSTANCE_STATE_ID",
        primary_key=True,
        related_name="+",
    )
    description = models.CharField(db_column="DESCRIPTION", max_length=255)

    class Meta:
        managed = True
        db_table = "INSTANCE_STATE_DESCRIPTION"


class InstanceGroup(models.Model):
    pass


@reversion.register()
class Instance(models.Model):
    """
    Instance is the case entity of any request.

    Instance is always based on a type of form.
    """

    instance_id = models.AutoField(db_column="INSTANCE_ID", primary_key=True)
    instance_state = models.ForeignKey(
        InstanceState,
        models.DO_NOTHING,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )
    form = models.ForeignKey(
        Form, models.DO_NOTHING, db_column="FORM_ID", related_name="+"
    )
    user = models.ForeignKey(
        User, models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    group = models.ForeignKey(
        "user.Group", models.DO_NOTHING, db_column="GROUP_ID", related_name="+"
    )
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    modification_date = models.DateTimeField(
        db_column="MODIFICATION_DATE", auto_now_add=True
    )
    previous_instance_state = models.ForeignKey(
        InstanceState,
        models.DO_NOTHING,
        db_column="PREVIOUS_INSTANCE_STATE_ID",
        related_name="+",
    )
    identifier = models.CharField(
        db_column="IDENTIFIER", max_length=50, blank=True, null=True
    )
    location = models.ForeignKey(
        "user.Location", models.PROTECT, null=True, blank=True, db_column="LOCATION_ID"
    )
    services = models.ManyToManyField("user.Service", through="core.InstanceService")
    case = models.OneToOneField(
        "caluma_workflow.Case",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="instance",
    )
    instance_group = models.ForeignKey(
        InstanceGroup, models.SET_NULL, related_name="instances", null=True
    )
    rejection_feedback = models.TextField(blank=True, null=True)

    def _get_queryset_for_linked_instances(self, queryset):
        return queryset if queryset else Instance.objects.all()

    @canton_aware
    def get_linked_instances(self, queryset=None):
        if not self.instance_group:  # pragma: no cover
            return Instance.objects.none()

        return (
            self._get_queryset_for_linked_instances(queryset)
            .filter(instance_group=self.instance_group)
            .exclude(pk=self.pk)
        )

    def get_linked_instances_sz(self, queryset=None):
        """
        Filter by instance_group to determine link.

        Current instance is excluded by identifier because
        the linking and displaying is performed using the identifier
        in the frontend.
        """
        if not self.instance_group:  # pragma: no cover
            return Instance.objects.none()

        return (
            self._get_queryset_for_linked_instances(queryset)
            .filter(instance_group=self.instance_group)
            .exclude(identifier=self.identifier)
        )

    def get_linked_instances_be(self, queryset=None):
        ebau_nr = self.case.meta.get("ebau-number")
        if not ebau_nr:  # pragma: no cover
            return []

        return (
            self._get_queryset_for_linked_instances(queryset)
            .filter(**{"case__meta__ebau-number": ebau_nr})
            .exclude(pk=self.pk)
        )

    def get_linked_instances_ur(self, queryset=None):
        # FIXME: instance groups should be extracted into a
        # proper relationship.
        if not self.instance_group:  # pragma: no cover
            return Instance.objects.none()

        return (
            InstanceGroup.objects.prefetch_related("instances")
            .get(pk=self.instance_group.pk)
            .instances.exclude(pk=self.pk)
        )

    def _responsible_service_instance_service(self, filter_type=None, **kwargs):
        active_services_settings = settings.APPLICATION.get("ACTIVE_SERVICES", {})

        if filter_type:
            filter_type = filter_type.upper()

            if filter_type not in active_services_settings.keys():  # pragma: no cover
                raise Exception(
                    f"Active service `filter_type` {filter_type} is not configured"
                )

            active_service_config = active_services_settings.get(filter_type)
        else:
            active_service_config = None
            default_active_service_config = None

            for config in active_services_settings.values():
                if config.get("DEFAULT"):
                    default_active_service_config = config

                if any(
                    [
                        self.instance_state.name == current_state
                        and self.previous_instance_state.name == previous_state
                        for current_state, previous_state in config.get(
                            "INSTANCE_STATES", []
                        )
                    ]
                ):
                    active_service_config = config

            active_service_config = (
                active_service_config or default_active_service_config
            )

        service_filters = active_service_config.get("FILTERS", {})

        instance_services = self.instance_services.filter(active=1, **service_filters)
        instance_service = instance_services.order_by("-pk").first()

        if instance_services.count() > 1:
            log.warning(
                f"Instance {self.pk}: Multiple active services, picking most recent one: {instance_service.service.get_name()}!"
            )

        return instance_service.service if instance_service else None

    def responsible_service(self, **kwargs):
        """
        Call application specific method and fallback to active_service.

        Application specific methods have to be named like this:
        _responsible_service_{application_name}
        """
        if settings.APPLICATION.get("USE_INSTANCE_SERVICE"):
            return self._responsible_service_instance_service(**kwargs)

        return self.group.service

    def is_active_or_involved_lead_authority(self, service_id):
        """Return true if the given service is a lead authority (active or involved)."""
        if not settings.APPLICATION.get("USE_INSTANCE_SERVICE"):  # pragma: no cover
            return self.responsible_service().pk == int(service_id)

        return self.services.filter(pk=int(service_id)).exists()

    def has_inquiry(self, service_id):
        """Return true if the given service is part of the circulation."""
        return (
            WorkItem.objects.filter(
                case__family=self.case,
                task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                addressed_groups=[str(service_id)],
            )
            .exclude(
                status__in=[
                    WorkItem.STATUS_SUSPENDED,
                    WorkItem.STATUS_CANCELED,
                ],
            )
            .exists()
        )

    def set_instance_state(self, instance_state_name: str, user: User) -> None:
        with reversion.create_revision():
            reversion.set_user(user)

            self.previous_instance_state = self.instance_state
            self.instance_state = InstanceState.objects.get(name=instance_state_name)
            self.save(update_fields=["previous_instance_state", "instance_state"])

    def get_internal_url(self):
        path = "/cases/"
        if settings.APPLICATION["INTERNAL_FRONTEND"] == "camac":
            path = "/index/redirect-to-instance-resource/instance-id/"

        return build_url(settings.INTERNAL_BASE_URL, path, self.pk)

    @cached_property
    def municipality(self):
        md = MasterData(self.case)

        if settings.APPLICATION_NAME == "kt_uri":
            communal_federal_number = md.municipality_slug
            return Service.objects.filter(
                Q(groups__locations__communal_federal_number=communal_federal_number)
                & Q(service_group__name="Sekretariate Gemeindebaubehörden")
            ).first()

        return (
            Service.objects.get(pk=md.municipality_slug)
            if md.municipality_slug
            else None
        )

    @cached_property
    def responsible_building_commission(self) -> Service | None:
        if not self.municipality:  # pragma: no cover
            return None

        return Service.objects.filter(
            service_group__name="Mitglieder Baukommissionen",
            groups__locations__in=self.municipality.groups.first().locations.all(),
        ).first()

    class Meta:
        managed = True
        db_table = "INSTANCE"


class InstanceAlexandriaDocument(models.Model):
    instance = models.ForeignKey(
        Instance, models.CASCADE, related_name="alexandria_instance_documents"
    )
    document = models.OneToOneField(
        "alexandria_core.Document", models.CASCADE, related_name="instance_document"
    )

    class Meta:
        unique_together = (("instance", "document"),)


class InstanceResponsibility(models.Model):
    instance = models.ForeignKey(
        Instance, models.CASCADE, related_name="responsibilities"
    )
    service = models.ForeignKey(
        "user.Service", models.CASCADE, db_column="SERVICE_ID", related_name="+"
    )
    user = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="USER_ID",
        related_name="responsibilities",
    )

    class Meta:
        unique_together = (("instance", "user", "service"),)


class JournalEntryManager(models.Manager):
    def get_queryset(self):
        return JournalEntryQuerySet(self.model, using=self._db)


class JournalEntry(models.Model):
    instance = models.ForeignKey(Instance, models.CASCADE, related_name="journal")
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, related_name="+", null=True
    )
    user = models.ForeignKey(User, models.DO_NOTHING, related_name="+")
    text = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField()
    modification_date = models.DateTimeField()
    VISIBILITIES = [
        ("all", "All"),
        ("own_organization", "Own Organization"),
        ("authorities", "Authorities"),
    ]
    visibility = models.CharField(
        max_length=16, choices=VISIBILITIES, default="own_organization"
    )
    duration = models.DurationField(blank=True, null=True)
    objects = JournalEntryManager()


class JournalEntryQuerySet(models.QuerySet):
    def visible_for(self, request) -> models.QuerySet[JournalEntry]:
        """
        Additional visibility logic for journal entries in relation to the group.

        The queryset is filtered according to the organisational visibility
        restriction on the journal entry. General visibility logic regarding the
        associated instance is handled in the instance queryset mixin.
        """

        group = request.group
        role = get_role_name(group)
        # TODO applicants or public users currently don't have access to journal entries at all.
        # Giving them access might require a dedicated "applicant" role in our permission layer?
        if not role or role == "public":
            return self.none()

        query_filter = models.Q(visibility="all")

        if group != settings.APPLICATION["PORTAL_GROUP"]:
            query_filter |= models.Q(
                visibility="own_organization", service=group.service
            )
            query_filter |= models.Q(visibility="authorities")

        return self.filter(query_filter)


class HistoryEntry(core_models.MultilingualModel, models.Model):
    instance = models.ForeignKey(Instance, models.CASCADE, related_name="history")
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, related_name="+", null=True
    )
    user = models.ForeignKey(User, models.DO_NOTHING, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    history_type = models.CharField(
        max_length=20, choices=HistoryActionConfig.HISTORY_TYPES_TUPLE
    )

    def __str__(self):
        return self.get_trans_attr("title")


class HistoryEntryT(models.Model):
    title = models.TextField()
    body = models.TextField(blank=True, null=True)
    history_entry = models.ForeignKey(
        HistoryEntry, models.CASCADE, related_name="trans"
    )
    language = models.CharField(max_length=2)


class IssueManager(models.Manager):
    def get_queryset(self):
        return IssueQuerySet(self.model, using=self._db)


class Issue(models.Model):
    STATE_OPEN = "open"
    STATE_DELAYED = "delayed"
    STATE_DONE = "done"
    STATE_CHOICES = (STATE_OPEN, STATE_DELAYED, STATE_DONE)
    STATE_CHOICES_TUPLE = ((choice, choice) for choice in STATE_CHOICES)

    instance = models.ForeignKey(Instance, models.CASCADE, related_name="issues")
    group = models.ForeignKey("user.Group", models.DO_NOTHING, related_name="+")
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, related_name="+", null=True
    )
    user = models.ForeignKey(
        User, models.DO_NOTHING, related_name="+", blank=True, null=True
    )
    deadline_date = models.DateField()
    state = models.CharField(
        max_length=20, choices=STATE_CHOICES_TUPLE, default=STATE_OPEN
    )
    text = models.TextField()
    objects = IssueManager()


class IssueQuerySet(models.QuerySet):
    def visible_for(self, request) -> models.QuerySet[Issue]:
        """
        Additional visibility logic for issues in relation to the group.

        The queryset is filtered according to the group's service.
        General visibility logic regarding the associated instance is
        handled in the instance queryset mixin.
        """

        group = request.group
        role = get_role_name(group)
        if not role or role == "public":
            return self.none()

        return self.filter(service=group.service)


class IssueTemplate(models.Model):
    group = models.ForeignKey("user.Group", models.DO_NOTHING, related_name="+")
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, related_name="+", null=True
    )
    user = models.ForeignKey(
        User, models.DO_NOTHING, related_name="+", blank=True, null=True
    )
    deadline_length = models.PositiveIntegerField()
    text = models.TextField()


class IssueTemplateSet(models.Model):
    group = models.ForeignKey("user.Group", models.DO_NOTHING, related_name="+")
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, related_name="+", null=True
    )
    issue_templates = models.ManyToManyField(
        IssueTemplate, related_name="issue_template_sets", blank=True
    )
    name = models.CharField(max_length=500)


class FormFieldManager(models.Manager):
    def get_queryset(self):
        return FormFieldQuerySet(self.model, using=self._db)


@reversion.register()
class FormField(models.Model):
    """
    Represents fields of an instance form.

    Which form type the field references is assigned on instance itself.
    """

    instance = models.ForeignKey(Instance, models.CASCADE, related_name="fields")
    name = models.CharField(max_length=500)
    value = models.JSONField()
    objects = FormFieldManager()

    class Meta:
        unique_together = (("instance", "name"),)


class FormFieldQuerySet(models.QuerySet):
    def visible_for(self, request) -> models.QuerySet[FormField]:
        """
        Additional visibility logic for form fields in relation to the group.

        The queryset is filtered according to the configured role restrictions
        on the form field. General visibility logic regarding the associated
        instance is handled in the instance queryset mixin.
        """
        role = get_role_name(request.group) or "applicant"
        questions = [
            question
            for question, value in settings.FORM_CONFIG["questions"].items()
            # all permissions may read per default once they have access to instance
            if role
            in value.get(
                "restrict",
                [
                    "applicant",
                    "public_reader",
                    "reader",
                    "canton",
                    "municipality",
                    "service",
                    "support",
                    "public",
                ],
            )
        ]
        return self.filter(name__in=questions)
