from caluma.caluma_workflow.models import WorkItem

from camac.instance import domain_logic, utils as instance_utils
from camac.instance.models import Instance
from camac.permissions import api as permissions_api
from camac.permissions.events import EmptyEventHandler
from camac.permissions.models import InstanceACL
from camac.user.models import ServiceRelation

from .common import (
    ApplicantsEventHandlerMixin,
    ChangeResponsibleServiceHandlerMixin,
    DistributionHandlerMixin,
    GrantSupportOnCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
)


class PermissionEventHandlerBE(
    ApplicantsEventHandlerMixin,
    InstanceSubmissionHandlerMixin,
    ChangeResponsibleServiceHandlerMixin,
    DistributionHandlerMixin,
    GrantSupportOnCreationHandlerMixin,
    # EmptyEventHandler needs to be last!
    EmptyEventHandler,
):
    def decision_decreed(self, instance: Instance):
        decision = instance.case.work_items.filter(
            task_id="decision",
            status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
        ).first()

        # TODO: Do we only grant an ACL to the geometer if the process continues?
        if (
            not decision
            or not domain_logic.DecisionLogic.should_continue_after_decision(
                instance, decision
            )
        ):  # pragma: no cover
            return

        self._grant_construction_control(instance)
        self._grant_geometer_if_needed(decision, instance)

    def _grant_geometer_if_needed(self, decision, instance):
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

    def _grant_construction_control(self, instance):
        construction_control = instance_utils.get_construction_control(
            instance_utils.get_municipality(instance)
        )
        self.manager.grant(
            instance,
            grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
            access_level="construction-control",
            service=construction_control,
        )

    def instance_copied(self, instance: Instance, from_instance: Instance):
        current_acls = InstanceACL.currently_active().filter(
            instance=from_instance,
        )

        if instance.case.meta.get("is-appeal") or instance.case.meta.get(
            "is-rejected-appeal"
        ):
            current_acls = current_acls.filter(
                access_level_id__in=["lead-authority", "applicant"]
            )
        # else: if we don't have any appeal flag, copy everything. This is a
        # commandline copy, not a "part-of-the-process-process" copy

        for acl in current_acls:
            acl.pk = None
            acl.instance = instance
            acl.save()
