from caluma.caluma_workflow.models import WorkItem

from camac.instance import domain_logic, utils as instance_utils
from camac.instance.models import Instance
from camac.permissions import api as permissions_api
from camac.permissions.events import EmptyEventHandler
from camac.user.models import ServiceRelation

from .common import (
    ApplicantsEventHandlerMixin,
    ChangeResponsibleServiceHandlerMixin,
    InstanceSubmissionHandlerMixin,
)


class PermissionEventHandlerBE(
    ApplicantsEventHandlerMixin,
    InstanceSubmissionHandlerMixin,
    ChangeResponsibleServiceHandlerMixin,
    EmptyEventHandler,
):
    # applicant_added is in ApplicantEvents
    # applicant_removed is in ApplicantEvents

    def decision_decreed(self, instance: Instance):
        decision = instance.case.work_items.filter(
            task_id="decision",
            status=WorkItem.STATUS_COMPLETED,
        ).first()

        # TODO: Do we only grant an ACL to the geometer if the process continues?
        if (
            not decision
            or not domain_logic.DecisionLogic.should_continue_after_decision(
                instance, decision
            )
        ):  # pragma: no cover
            return

        # Provide ACL on instance to geometer belonging to municipality
        # if the geometer question was answered with yes on decision
        answer = (
            decision.document.answers.filter(question_id="decision-geometer")
            .values_list("value", flat=True)
            .first()
        )

        if answer == "decision-geometer-yes":
            geometer_service = instance_utils.get_municipality_provider_services(
                instance, ServiceRelation.FUNCTION_GEOMETER
            ).first()

            if not geometer_service:
                # No geometer connected to muncipality
                return

            self.manager.grant(
                instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level="geometer",
                service=geometer_service,
            )
