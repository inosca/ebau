from caluma.caluma_workflow.models import WorkItem

from camac.instance import domain_logic, utils as instance_utils
from camac.instance.models import Instance
from camac.instance.utils import (
    be_should_prevent_process_step_for_deactivated_municipality,
)
from camac.permissions import api as permissions_api
from camac.permissions.events import EmptyEventHandler
from camac.user.models import Service, ServiceRelation

from .common import (
    ApplicantsEventHandlerMixin,
    ChangeResponsibleServiceHandlerMixin,
    DistributionHandlerMixin,
    InstanceCopyHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
)


class PermissionEventHandlerBE(
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

        self._grant_geometer_if_needed(decision, instance)

    def instance_submitted(self, instance: Instance):
        if instance.case.document.form.slug not in [
            "heat-generator",
            "heat-generator-v2",
            "heat-generator-v3",
        ]:  # pragma: no cover
            return

        answer = (
            instance.case.document.answers.filter(
                question_id="heat-generator-combustion-database-v2"
            )
            .values_list("value", flat=True)
            .first()
        )

        if answer and "heat-generator-combustion-database-v2-ja" in answer:
            heat_generator_combustion_service = Service.objects.filter(
                slug="feuerungskontrolle-weu"
            ).first()

            if not heat_generator_combustion_service:  # pragma: no cover
                return

            self.manager.grant(
                instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level="read",
                service=heat_generator_combustion_service,
            )

    def _grant_geometer_if_needed(self, decision, instance):
        # If the instance is prevented to submit don't grant acces to the geometer
        if be_should_prevent_process_step_for_deactivated_municipality(instance):
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
                event_name="grant-geometer-access",
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


class GeneralPermissionEventHandlerBE(
    ApplicantsEventHandlerMixin,
    InstanceSubmissionHandlerMixin,
    ChangeResponsibleServiceHandlerMixin,
    DistributionHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceCopyHandlerMixin,
    PermissionEventHandlerBE,
    # EmptyEventHandler needs to be last!
    EmptyEventHandler,
):
    def decision_decreed(self, instance: Instance):
        super().decision_decreed(instance)
        self._grant_construction_control(instance)
