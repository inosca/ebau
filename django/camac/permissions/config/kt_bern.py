from caluma.caluma_workflow.models import WorkItem

from camac.instance.models import Instance
from camac.permissions import api as permissions_api, models as permissions_models
from camac.permissions.events import EmptyEventHandler
from camac.user.models import ServiceRelation


class PermissionEventHandlerBE(EmptyEventHandler):
    def decision_decreed(self, instance: Instance):
        decision = instance.case.work_items.filter(
            task_id="decision",
            status=WorkItem.STATUS_COMPLETED,
        ).first()

        if not decision:
            return

        # Provide ACL on instance to geometer belonging to municipality
        # if the geometer question was answered with yes on decision
        answer = (
            decision.document.answers.filter(question_id="decision-geometer")
            .values_list("value", flat=True)
            .first()
        )

        if answer == "decision-geometer-yes":
            responsible_service = instance.responsible_service()
            geometer_service_relation = ServiceRelation.objects.filter(
                function=ServiceRelation.FUNCTION_GEOMETER,
                receiver=responsible_service,
            ).first()

            # No geometer connected to muncipality
            if not geometer_service_relation:
                return

            self.manager.grant(
                instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level=permissions_models.AccessLevel.objects.get(pk="geometer"),
                service=geometer_service_relation.provider,
            )
