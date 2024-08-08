from datetime import timedelta

from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.utils import timezone

from camac.constants import kt_gr as gr_constants
from camac.instance.models import Instance
from camac.permissions import api as permissions_api, models as permissions_models
from camac.permissions.events import EmptyEventHandler
from camac.permissions.models import InstanceACL
from camac.user.models import Group, Service

from .common import (
    ApplicantsEventHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
)


def _gr_include_special_service(instance, service_name):
    """
    Check if a 'special' service should be included in the given instance.

    In Kt. GR, two 'special' services can be given access by ticking a checkbox
    in the workflow:

    - Gebäudeversicherung Graubünden (GVG) in the decision form
    - Amt für Immobilienbewertung (AIB) in the construction acceptance form

    This method returns true if one of those services is supposed to be included
    in a specific dossier.
    """
    if settings.APPLICATION_NAME != "kt_gr":
        return False

    if service_name == "gvg":
        # GVG can only be included in "building permit"-type decisions
        # TODO(GR): replace this once preliminary clarification workflow
        # has been introduced
        if instance.case.document.form.slug in [
            "bauanzeige",
            "vorlaeufige-beurteilung",
        ]:  # pragma: no cover
            return False
        task_id = settings.DECISION["TASK"]
        question_id = "fuer-gvg-freigeben"
    elif service_name == "aib":
        task_id = "construction-acceptance"
        question_id = "fuer-aib-freigeben"
    else:  # pragma: no cover
        raise RuntimeError(
            f"unknown special service {service_name}, expected 'gvg' or 'aib'."
        )

    work_item = instance.case.work_items.filter(
        task_id=task_id,
        status=WorkItem.STATUS_COMPLETED,
    ).first()

    if not work_item:  # pragma: no cover
        return False

    answer = work_item.document.answers.filter(question_id=question_id).first()
    if not answer:
        return False
    return f"{question_id}-ja" in answer.value


def gr_include_gvg(instance):
    return _gr_include_special_service(instance, "gvg")


def gr_include_aib(instance):
    return _gr_include_special_service(instance, "aib")


class PermissionEventHandlerGR(
    ApplicantsEventHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
    EmptyEventHandler,
):
    def decision_decreed(self, instance: Instance):
        if gr_include_gvg(instance):
            self.manager.grant(
                instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level=permissions_models.AccessLevel.objects.get(pk="read"),
                service=Service.objects.get(name=gr_constants.GVG_SERVICE_SLUG),
            )

    def construction_acceptance_completed(self, instance: Instance):
        if gr_include_aib(instance):
            self.manager.grant(
                instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level=permissions_models.AccessLevel.objects.get(pk="read"),
                service=Service.objects.get(name=gr_constants.AIB_SERVICE_SLUG),
            )

    def inquiry_sent(self, instance: Instance, work_item):
        # USOs have 7 days to open an instance after being invited.
        for addr in work_item.addressed_groups:
            addr_service = Service.objects.get(pk=addr)
            access_level = "distribution-service"
            ends_at = None
            if "uso" in addr_service.groups.values_list("role__name", flat=True):
                access_level = "uso"
                ends_at = timezone.now() + timedelta(days=7)

            self.manager.grant(
                instance,
                grant_type="SERVICE",
                access_level=access_level,
                service=addr_service,
                event_name="inquiry-sent",
                ends_at=ends_at,
            )

    def inquiry_completed(self, instance: Instance, work_item):
        # USOs keep their access if they respond to an inquiry.
        for addr in work_item.addressed_groups:
            service = Service.objects.get(pk=addr)
            if "uso" in service.groups.values_list("role__name", flat=True):
                for acl in InstanceACL.currently_active().filter(
                    instance=instance, service_id=service
                ):
                    self.manager.revoke(acl, event_name="inquiry-completed")
                self.manager.grant(
                    instance,
                    grant_type="SERVICE",
                    access_level="uso",
                    service=service,
                    event_name="inquiry-completed",
                )

    def instance_retrieved(self, instance: Instance, group: Group):
        # USOs have 7 days to reply to an inquiry after they first accessed the instance.
        if group.role.name != "uso":  # pragma: no cover
            return

        deadline = timezone.now() + timedelta(days=7)

        # revoke all existing ACLs
        invite_acls = InstanceACL.currently_active().filter(
            instance=instance,
            service_id=group.service.pk,
            created_by_event="inquiry-sent",
        )
        if invite_acls.exists():
            for invite_acl in invite_acls:
                self.manager.revoke(invite_acl, event_name="dossier-retrieved")
            # grant a new ACL that expires in 7 days
            self.manager.grant(
                instance,
                grant_type="SERVICE",
                access_level="uso",
                service=group.service,
                event_name="dossier-retrieved",
                ends_at=deadline,
            )
