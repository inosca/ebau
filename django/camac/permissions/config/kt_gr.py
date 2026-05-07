from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.constants import kt_gr as gr_constants
from camac.instance.models import Instance
from camac.permissions import api as permissions_api, models as permissions_models
from camac.permissions.events.core import EmptyEventHandler
from camac.permissions.models import InstanceACL
from camac.user.models import Service

from .common import (
    ApplicantsEventHandlerMixin,
    ConstructionMonitoringHandlerMixin,
    GeometerHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
)


def _should_include_special_service(instance, service_name):
    """
    Check if a 'special' service should be included in the given instance.

    In Kt. GR, two 'special' services can be given access by ticking a checkbox in the decision form:

    - Gebäudeversicherung Graubünden (GVG)
    - Amt für Immobilienbewertung (AIB)

    This method returns true if one of those services is supposed to be included
    in a specific dossier.
    """
    if settings.APPLICATION_NAME != "kt_gr":
        return False

    forms_no_construction_monitoring = [
        *gr_constants.BAUANZEIGE_FORMS,
        *gr_constants.SOLARANLAGE_FORMS,
        *gr_constants.VORLAEUFIGE_BEURTEILUNG_FORMS,
    ]
    is_special_form = (
        instance.case.document.form.slug in forms_no_construction_monitoring
    )

    if service_name == gr_constants.GVG_SERVICE_SLUG:
        if is_special_form:
            return False

        question_id = "fuer-gvg-freigeben"
        task_id = settings.DECISION["TASK"]

    elif service_name == gr_constants.AIB_SERVICE_SLUG:
        question_id = "fuer-aib-freigeben"
        task_id = (
            "construction-acceptance"
            if not is_special_form
            else settings.DECISION["TASK"]
        )

    else:  # pragma: no cover
        raise RuntimeError(
            f"unknown special service {service_name}, expected '{gr_constants.GVG_SERVICE_SLUG}' or '{gr_constants.AIB_SERVICE_SLUG}'"
        )

    # eCH instance should always include GVG / AIB.
    if instance.case.meta.get("ech0211-submitted", False):
        return True

    work_item = instance.case.work_items.filter(
        task_id=task_id,
        status=WorkItem.STATUS_COMPLETED,
    ).first()

    if work_item:
        answer = work_item.document.answers.filter(question_id=question_id).first()

        return answer and f"{question_id}-ja" in answer.value

    return False


def should_include_gvg(instance):
    return _should_include_special_service(instance, gr_constants.GVG_SERVICE_SLUG)


def should_include_aib(instance):
    return _should_include_special_service(instance, gr_constants.AIB_SERVICE_SLUG)


def _is_special_service_included(instance, special_service_slug):
    return (
        InstanceACL.currently_active()
        .filter(
            instance=instance,
            service__slug=special_service_slug,
        )
        .exists()
    )


class PermissionEventHandlerGR(
    GeometerHandlerMixin,
    ApplicantsEventHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
    ConstructionMonitoringHandlerMixin,
    EmptyEventHandler,
):
    def decision_decreed(self, instance: Instance):
        if should_include_gvg(instance):
            self.include_special_service(instance, gr_constants.GVG_SERVICE_SLUG)

        if should_include_aib(instance):
            self.include_special_service(instance, gr_constants.AIB_SERVICE_SLUG)

    def inquiry_sent(self, instance: Instance, work_item: WorkItem):
        for addr in work_item.addressed_groups:
            addr_service = Service.objects.get(pk=addr)
            access_level = "distribution-service"
            ends_at = None

            # USO ACL should end when the inquiry deadline is over (20 days).
            if "uso" in addr_service.groups.values_list("role__name", flat=True):
                access_level = "uso"
                ends_at = work_item.deadline

            self.manager.grant(
                instance,
                grant_type="SERVICE",
                access_level=access_level,
                service=addr_service,
                event_name="inquiry-sent",
                ends_at=ends_at,
            )

    def inquiry_completed(self, instance: Instance, work_item: WorkItem):
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

    def gvg_work_item_created(self, work_item: WorkItem):
        if (
            work_item.task.address_groups
            and "gebaudeversicherung" in work_item.task.address_groups
        ):
            for addr in work_item.addressed_groups:
                if (
                    not InstanceACL.currently_active()
                    .filter(
                        instance=work_item.case.family.instance,
                        service=addr,
                    )
                    .exists()
                ):
                    self.manager.grant(
                        work_item.case.family.instance,
                        grant_type="SERVICE",
                        access_level="distribution-service",
                        service=Service.objects.get(pk=addr),
                        event_name="received-work-item",
                    )

    def instance_completed(self, instance: Instance):
        if should_include_aib(instance):
            self.include_special_service(instance, gr_constants.AIB_SERVICE_SLUG)

    def include_special_service(self, instance, special_service_slug):
        if not _is_special_service_included(instance, special_service_slug):
            self.manager.grant(
                instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level=permissions_models.AccessLevel.objects.get(pk="read"),
                service=Service.objects.get(slug=special_service_slug),
            )
