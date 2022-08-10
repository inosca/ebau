import logging

from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db.models import Exists, OuterRef, Q
from django.db.models.constants import LOOKUP_SEP
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import exceptions

from camac.attrs import nested_getattr
from camac.constants import kt_uri as uri_constants
from camac.core.models import Circulation, CommissionAssignment, InstanceService
from camac.instance.models import Instance
from camac.mixins import AttributeMixin
from camac.request import get_request
from camac.user.models import User
from camac.user.permissions import get_group, get_role_name, permission_aware

from . import models

log = logging.getLogger(__name__)


class InstanceQuerysetMixin(object):
    """
    Mixin to filter queryset by instances which may be read by given role.

    Define `instance_field` where instance is located on model (dot annotation).

    This mixin was written for usage in views. Meanwhile we also use it in different
    places. To make it work outside of a view, make sure you set the `user` and `group`
    attributes.
    """

    instance_field = "instance"

    def _get_instance_filter_expr(self, field, expr=None):
        """Get filter expression of field on given model."""
        result = field

        if self.instance_field:
            instance_field = self.instance_field.replace(".", LOOKUP_SEP)
            result = instance_field + LOOKUP_SEP + result

        if (
            hasattr(super(), "get_queryset")
            and super().get_queryset().model.__name__ == "Case"
        ):
            # This removes duplicate lookups like "instance__case__xy" if
            # querying cases directly
            result = result.replace(f"instance{LOOKUP_SEP}case{LOOKUP_SEP}", "")

        if expr:
            result = result + LOOKUP_SEP + expr

        return result

    def _get_group(self, group=None):
        return group or getattr(self, "group", None) or self._get_request().group

    def _get_user(self):
        user = getattr(self, "user", None) or self._get_request().user

        return user if isinstance(user, User) else None

    def _get_request(self):
        """Ensure that the mixin works in serializers and views."""
        return self.request if hasattr(self, "request") else self.context["request"]

    def get_base_queryset(self):
        """Get base query queryset for role specific filters.

        Per default `self.queryset` is used but may be overwritten.
        """
        # instance state is always used to determine permissions
        instance_state_expr = self._get_instance_filter_expr("instance_state")
        role_name = get_role_name(get_group(self))
        hidden_states = settings.APPLICATION.get("INSTANCE_HIDDEN_STATES", {}).get(
            role_name, []
        )
        queryset = (
            super().get_queryset()
            if hasattr(super(), "get_queryset")
            else Instance.objects.all()
        )
        queryset = queryset.select_related(instance_state_expr)

        if len(hidden_states):
            state_field = self._get_instance_filter_expr("instance_state__name", "in")
            return queryset.exclude(**{state_field: hidden_states})

        return queryset

    @permission_aware
    def get_queryset(self, group=None):
        queryset = self.get_base_queryset()

        # A user should see dossiers which he submitted or has been invited to.
        return queryset.filter(
            **{
                self._get_instance_filter_expr(
                    "involved_applicants__invitee"
                ): self._get_user()
            }
        )

    def get_queryset_for_public_reader(self, group=None):
        queryset = self.get_base_queryset()
        instance_field = self._get_instance_filter_expr("pk", "in")

        instances = models.Instance.objects.filter(
            publication_entries__publication_date__date__lte=timezone.localdate(),
            publication_entries__publication_end_date__date__gte=timezone.localdate(),
            publication_entries__is_published=True,
            location__in=self._get_group().locations.all(),
        )

        return queryset.filter(**{instance_field: instances})

    def get_queryset_for_reader(self, group=None):
        return self.get_queryset_for_municipality()

    def get_queryset_for_coordination(self, group=None):
        group = self._get_group(group)
        queryset = self.get_base_queryset()
        instance_field = self._get_instance_filter_expr("pk", "in")
        form_field = self._get_instance_filter_expr("form", "in")

        instances_created_by_group = self._instances_created_by(group)

        return queryset.filter(
            (
                Q(**{instance_field: instances_created_by_group})
                | Q(
                    **{
                        form_field: uri_constants.RESPONSIBLE_KOORS.get(
                            group.service_id, []
                        )
                    }
                )
            )
        )

    def get_queryset_for_municipality(self, group=None):
        group = self._get_group(group)
        queryset = self.get_base_queryset()
        instance_field = self._get_instance_filter_expr("pk", "in")

        instances_for_location = models.Instance.objects.filter(
            location__in=group.locations.all()
        )
        instances_for_service = InstanceService.objects.filter(
            service=group.service
        ).values("instance_id")
        instances_for_responsible_service = self._instances_for_responsible_service(
            group
        )
        instances_for_activation = self._instances_with_activation(group)

        return queryset.filter(
            Q(**{instance_field: instances_for_location})
            | Q(**{instance_field: instances_for_service})
            | Q(**{instance_field: instances_for_activation})
            | Q(**{instance_field: instances_for_responsible_service})
        )

    def get_queryset_for_service(self, group=None):
        group = self._get_group(group)
        queryset = self.get_base_queryset()
        instance_field = self._get_instance_filter_expr("pk", "in")

        instances_for_responsible_service = self._instances_for_responsible_service(
            group
        )
        instances_for_activation = self._instances_with_activation(group)

        # use subquery to avoid duplicates
        return queryset.filter(
            Q(**{instance_field: instances_for_responsible_service})
            | Q(**{instance_field: instances_for_activation})
        )

    def get_queryset_for_trusted_service(self, group=None):
        # "Trusted" services see all submitted instances (Kt. UR)
        return self.get_base_queryset()

    def get_queryset_for_canton(self, group=None):
        return self.get_base_queryset()

    def get_queryset_for_support(self, group=None):
        return self.get_base_queryset()

    def get_queryset_for_organization_readonly(self, group=None):
        group = self._get_group(group)
        queryset = self.get_base_queryset()
        instance_field = self._get_instance_filter_expr("pk", "in")
        instance_states = ["ext", "ext_gem", "circ", "redac", "done"]
        form_ids = [
            uri_constants.FORM_VORABKLAERUNG,
            uri_constants.FORM_BAUGESUCH,
        ]

        instances_for_location = models.Instance.objects.filter(
            location__in=group.locations.all(),
            instance_state__name__in=instance_states,
            form__form_id__in=form_ids,
        )

        return queryset.filter(**{instance_field: instances_for_location})

    def get_queryset_for_commission(self, group=None):
        group = self._get_group(group)
        queryset = self.get_base_queryset()
        instance_field = self._get_instance_filter_expr("pk", "in")
        instances_with_invite = CommissionAssignment.objects.filter(group=group).values(
            "instance"
        )
        return queryset.filter(**{instance_field: instances_with_invite})

    def get_queryset_for_public(self, group=None):
        queryset = self.get_base_queryset()

        if settings.APPLICATION.get("PUBLICATION_BACKEND") == "caluma":
            public_access_key = self._get_request().META.get(
                "HTTP_X_CAMAC_PUBLIC_ACCESS_KEY"
            )

            filters = {
                "case": OuterRef(self._get_instance_filter_expr("case__pk")),
                "task_id": "fill-publication",
                "meta__is-published": True,
                "status": WorkItem.STATUS_COMPLETED,
            }
            start_question = "publikation-startdatum"
            end_question = "publikation-ablaufdatum"

            if public_access_key:
                filters.update(
                    {
                        "task_id": "information-of-neighbors",
                        "document__pk__startswith": public_access_key,
                    }
                )
                start_question = "information-of-neighbors-start-date"
                end_question = "information-of-neighbors-end-date"

            return queryset.filter(
                Exists(
                    WorkItem.objects.filter(**filters)
                    .filter(
                        document__answers__question_id=start_question,
                        document__answers__date__lte=timezone.now(),
                    )
                    .filter(
                        document__answers__question_id=end_question,
                        document__answers__date__gte=timezone.now(),
                    )
                )
            )
        elif settings.APPLICATION.get("PUBLICATION_BACKEND") == "camac-ng":
            return (
                queryset.filter(
                    **{
                        self._get_instance_filter_expr(
                            "publication_entries__publication_date__date__lte"
                        ): timezone.localdate(),
                        self._get_instance_filter_expr(
                            "publication_entries__publication_end_date__date__gte"
                        ): timezone.localdate(),
                        self._get_instance_filter_expr(
                            "publication_entries__is_published"
                        ): True,
                    },
                )
                .exclude(
                    **{
                        self._get_instance_filter_expr(
                            "form_id"
                        ): settings.APPLICATION.get("OEREB_FORM", None)
                    }
                )
                .distinct()
            )

        return queryset.none()

    def get_queryset_for_oereb_api(self, group=None):
        queryset = self.get_base_queryset()

        return queryset.filter(
            Q(
                **{
                    self._get_instance_filter_expr("form_id"): settings.APPLICATION.get(
                        "OEREB_FORM", None
                    ),
                }
            )
        )

    def _instances_with_activation(self, group):
        if settings.DISTRIBUTION:
            # WARNING: if this logic changes, `hasInquiry` in
            # php/library/Custom/CalumaDistribution.php needs to be updated as
            # well
            return (
                WorkItem.objects.filter(
                    task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                    addressed_groups=[str(group.service.pk)],
                )
                .exclude(
                    status__in=[
                        WorkItem.STATUS_SUSPENDED,
                        WorkItem.STATUS_CANCELED,
                    ],
                )
                .values("case__family__instance__pk")
            )

        return Circulation.objects.filter(activations__service=group.service).values(
            "instance_id"
        )

    def _instances_for_responsible_service(self, group):
        if settings.APPLICATION.get("USE_INSTANCE_SERVICE"):
            return models.Instance.objects.none()

        return models.Instance.objects.filter(group__service=group.service)

    def _instances_created_by(self, group):
        return Instance.objects.filter(group=group).values("instance_id")


class InstanceEditableMixin(AttributeMixin):
    """Mixin to determine whether action is allowed on given instance.

    Define `instance_editable_permission` what permission is needed to edit.
    Currently there are `document` for attachments and `form` for form data.
    Set it to None if no specific permission is required.
    """

    def get_instance(self, obj):
        instance = obj
        instance_field = self.serializer_getattr("instance_field")
        if instance_field:
            instance = nested_getattr(obj, self.instance_field)

        return instance

    def has_editable_permission(self, instance):
        editable_permission = self.serializer_getattr("instance_editable_permission")

        return editable_permission is None or editable_permission in self.get_editable(
            instance
        )

    @permission_aware
    def get_editable(self, instance):
        # TODO: should be replaced with can-read and can-edit permissions
        # in form config. Difficulty is that documents are no real questions.
        form_backend = settings.APPLICATION.get("FORM_BACKEND")
        state = instance.instance_state.name

        if state in ["new", "rejected"]:
            return {"instance", "form", "document"}

        if state == "nfd":
            return {"document"}

        # Kt. Bern
        if form_backend == "caluma" and state in [
            "subm",  # eBau-Nummer vergeben
            "circulation_init",  # Zirkulation initialisieren
            "circulation",  # In Zirkulation
            "coordination",  # In Koordination
            "correction",  # In Korrektur
            "corrected",  # Korrigiert von Leitbehörde
            "sb1",  # Selbstdeklaration 1
            "sb2",  # Selbstdeklaration 2
            "in_progress",  # In Bearbeitung
        ]:
            return {"document"}

        return set()

    def get_editable_for_service(self, instance):
        service = get_request(self).group.service
        if instance.responsible_service() == service:
            return {"form", "document"}

        return {"document"}

    def get_editable_for_municipality(self, instance):
        return {"form", "document"}

    def get_editable_for_canton(self, instance):
        return {"form", "document"}

    def get_editable_for_coordination(self, instance):
        return {"form", "document"}

    def get_editable_for_reader(self, instance):
        return set()

    def get_editable_for_public(self, instance):
        return set()

    def get_editable_for_public_reader(self, instance):
        return set()

    def get_editable_for_organization_readonly(self, instance):  # pragma: no cover
        return set()

    def get_editable_for_commission(self, instance):
        return set()

    def get_editable_for_support(self, instance):
        return {"instance", "form", "document"}

    def has_object_update_permission(self, obj):
        instance = self.get_instance(obj)
        return self.has_editable_permission(instance)

    def _validate_instance_editablity(
        self, instance, is_editable_callable=lambda: True
    ):
        if not self.has_editable_permission(instance) or not is_editable_callable():
            # TODO log user's current group's role
            raise exceptions.ValidationError(
                _("Not allowed to add data to instance %(instance)s")
                % {"instance": instance.pk}
            )

        return instance

    @permission_aware
    def validate_instance(self, instance):
        user = get_request(self).user
        return self._validate_instance_editablity(
            instance, lambda: instance.involved_applicants.filter(invitee=user).exists()
        )

    def validate_instance_for_municipality(self, instance):
        group = get_request(self).group
        service = group.service
        circulations = instance.circulations.all()
        responsible_service = instance.responsible_service()

        return self._validate_instance_editablity(
            instance,
            lambda: (
                group.locations.filter(pk=instance.location_id).exists()
                or circulations.filter(activations__service=service).exists()
                or InstanceService.objects.filter(
                    service=service, instance=instance
                ).exists()
                or responsible_service == service
            ),
        )

    def validate_instance_for_coordination(self, instance):
        # TODO: Map form types to responsible KOORS
        hidden_states = settings.APPLICATION.get("INSTANCE_HIDDEN_STATES", {}).get(
            "coordination", []
        )
        if instance.instance_state.name in hidden_states:
            raise exceptions.ValidationError(
                _("Not allowed to add data to instance %(instance)s as coordination")
                % {"instance": instance.pk}
            )

        return self._validate_instance_editablity(instance)

    def validate_instance_for_service(self, instance):
        service = get_request(self).group.service
        responsible_service = instance.responsible_service()

        return self._validate_instance_editablity(
            instance,
            lambda: (
                self.has_activations(instance, service)
                or responsible_service == service
            ),
        )

    def validate_instance_for_canton(self, instance):
        return self._validate_instance_editablity(instance)

    def validate_instance_for_support(self, instance):
        return self._validate_instance_editablity(instance)

    def has_activations(self, instance, service):
        if settings.DISTRIBUTION:
            return WorkItem.objects.filter(
                case__family__instance=instance,
                task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                addressed_groups=[str(service.pk)],
            ).exclude(status__in=[WorkItem.STATUS_CANCELED, WorkItem.STATUS_SUSPENDED])

        return instance.circulations.filter(activations__service=service).exists()
