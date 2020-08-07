import logging

from caluma.caluma_workflow.dynamic_groups import (
    BaseDynamicGroups,
    register_dynamic_group,
)
from django.conf import settings

from camac.instance.models import Instance

log = logging.getLogger()


class CustomDynamicGroups(BaseDynamicGroups):
    def _get_instance(self, case):
        return Instance.objects.get(pk=case.meta.get("camac-instance-id"))

    @register_dynamic_group("municipality")
    def resolve_municipality(self, task, case, user, prev_work_item, context, **kwargs):
        instance = self._get_instance(case)
        service = None

        if settings.APPLICATION_NAME in ["kt_bern", "demo"]:
            service = instance.active_service()
        elif settings.APPLICATION_NAME == "kt_schwyz":
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
