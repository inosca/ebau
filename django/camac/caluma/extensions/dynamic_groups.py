import logging

from caluma.caluma_workflow.dynamic_groups import (
    BaseDynamicGroups,
    register_dynamic_group,
)
from django.conf import settings

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

    @register_dynamic_group("municipality")
    def resolve_municipality(self, task, case, user, prev_work_item, context, **kwargs):
        instance = self._get_instance(case)

        if settings.APPLICATION_NAME == "kt_bern":
            service = instance.active_service()
        else:
            service = instance.group.service

        if not service:
            log.error(f"No municipality group found for instance {instance.pk}")

            return []

        return [str(service.pk)]

    @register_dynamic_group("construction_control")
    def resolve_construction_control(
        self, task, case, user, prev_work_item, context, **kwargs
    ):
        instance = self._get_instance(case)
        service = instance.active_service(
            settings.APPLICATION.get("ACTIVE_BAUKONTROLLE_FILTERS", {})
        )

        if not service:
            log.error(f"No construction_control group found for instance {instance.pk}")

            return []

        return [str(service.pk)]

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
