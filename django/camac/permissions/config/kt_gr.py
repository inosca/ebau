from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.constants import kt_gr as gr_constants
from camac.instance.models import Instance
from camac.permissions import api as permissions_api, models as permissions_models
from camac.permissions.events import EmptyEventHandler
from camac.user.models import Service


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


class PermissionEventHandlerGR(EmptyEventHandler):
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
