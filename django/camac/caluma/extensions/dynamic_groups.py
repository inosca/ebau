import logging

from caluma.caluma_workflow.dynamic_groups import (
    BaseDynamicGroups,
    register_dynamic_group,
)

from camac.core.models import Activation
from camac.instance.models import Instance

log = logging.getLogger()


class CustomDynamicGroups(BaseDynamicGroups):
    def _get_instance(self, case):
        return Instance.objects.get(pk=case.meta.get("camac-instance-id"))

    def _get_activation(self, context):
        if not context:
            return Activation.objects.none()

        return Activation.objects.filter(pk=context.get("activation-id")).first()

    def _get_responsible_service(self, case, filter_type):
        instance = self._get_instance(case)
        service = instance.responsible_service(filter_type=filter_type)

        if not service:
            log.error(f"No {filter_type} group found for instance {instance.pk}")

            return []

        return [str(service.pk)]

    @register_dynamic_group("municipality")
    def resolve_municipality(self, task, case, user, prev_work_item, context, **kwargs):
        return self._get_responsible_service(case, "municipality")

    @register_dynamic_group("construction_control")
    def resolve_construction_control(
        self, task, case, user, prev_work_item, context, **kwargs
    ):
        return self._get_responsible_service(case, "construction_control")

    @register_dynamic_group("service")
    def resolve_service(self, task, case, user, prev_work_item, context, **kwargs):
        activation = self._get_activation(context)

        if not activation:
            log.error("No service group found with the given context")

            return []

        return [str(activation.service.pk)]

    @register_dynamic_group("service_parent")
    def resolve_service_parent(
        self, task, case, user, prev_work_item, context, **kwargs
    ):
        activation = self._get_activation(context)

        if not activation:
            log.error("No service_parent group found with the given context")

            return []

        return [str(activation.service_parent.pk)]
