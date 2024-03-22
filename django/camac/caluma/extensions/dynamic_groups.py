import logging
from itertools import chain

from caluma.caluma_workflow.dynamic_groups import (
    BaseDynamicGroups,
    register_dynamic_group,
)
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.constants import kt_uri as uri_constants
from camac.instance import utils as instance_utils
from camac.instance.models import Instance
from camac.user.models import Service, ServiceRelation

log = logging.getLogger()


class CustomDynamicGroups(BaseDynamicGroups):
    def _get_responsible_service(self, case, filter_type, context):
        instance = (
            case.family.instance
            if hasattr(case.family, "instance")
            else Instance.objects.get(pk=context.get("instance"))
        )
        service = instance.responsible_service(filter_type=filter_type)

        if not service:  # pragma: no cover
            log.error(f"No {filter_type} group found for instance {instance.pk}")

            return []

        return [str(service.pk)]

    @register_dynamic_group("municipality")
    def resolve_municipality(self, task, case, user, prev_work_item, context, **kwargs):
        return self._get_responsible_service(case, "municipality", context)

    @register_dynamic_group("construction_control")
    def resolve_construction_control(
        self, task, case, user, prev_work_item, context, **kwargs
    ):
        return self._get_responsible_service(case, "construction_control", context)

    @register_dynamic_group("distribution_create_inquiry")
    def resolve_distribution_create_inquiry(
        self, task, case, user, prev_work_item, context, **kwargs
    ):
        if context and context.get("addressed_groups") and prev_work_item:
            # We should not create a new "create-inquiry" work item if there
            # already is a ready one for that service.
            existing_ids = set(
                chain(
                    *case.work_items.filter(
                        task_id=settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
                        status=WorkItem.STATUS_READY,
                    ).values_list("addressed_groups", flat=True)
                )
            )

            target_ids = {
                # Target service for the inquiry
                *context.get("addressed_groups", []),
                # Service that created the inquiry
                *prev_work_item.addressed_groups,
            }

            services = Service.objects.filter(
                pk__in=target_ids - existing_ids,
                service_parent__isnull=True,  # Subservices can't create any inquiries
            )

            return [str(pk) for pk in services.values_list("pk", flat=True)]

        # If no context is given it's the first "create-inquiry" work item in
        # the distribution case which must be assigned to the municipality
        return self.resolve_municipality(
            task, case, user, prev_work_item, context, **kwargs
        )

    @register_dynamic_group("create_init_additional_demand")
    def resolve_create_init_additional_demand(
        self, task, case, user, prev_work_item, context, **kwargs
    ):
        if prev_work_item and prev_work_item.task_id not in settings.APPLICATION[
            "CALUMA"
        ].get("SUBMIT_TASKS", []):
            target_ids = set()

            if prev_work_item.task_id == settings.ADDITIONAL_DEMAND["CREATE_TASK"]:
                target_ids = set(prev_work_item.addressed_groups)
            elif prev_work_item.task_id == settings.DISTRIBUTION["INQUIRY_CREATE_TASK"]:
                target_ids = set(context.get("addressed_groups", []))

            # We should not create a new "init-additional-demand" work item if
            # there already is a ready one for that service.
            existing_ids = set(
                chain(
                    *case.work_items.filter(
                        task_id=settings.ADDITIONAL_DEMAND["CREATE_TASK"],
                        status=WorkItem.STATUS_READY,
                    ).values_list("addressed_groups", flat=True)
                )
            )

            services = Service.objects.filter(pk__in=target_ids - existing_ids)

            if not settings.ADDITIONAL_DEMAND["ALLOW_SUBSERVICES"]:
                # Subservices can't create any additional demands
                services = services.filter(service_parent__isnull=True)

            return [str(pk) for pk in services.values_list("pk", flat=True)]

        # If no context is given it's the first "init-additional-demand" work
        # item in the case (either main case or distribution child case) which
        # must be assigned to the municipality
        return self.resolve_municipality(
            task, case, user, prev_work_item, context, **kwargs
        )

    @register_dynamic_group("geometer")
    def resolve_geometer(self, task, case, user, prev_work_item, context, **kwargs):
        geometers = instance_utils.get_municipality_provider_services(
            case.family.instance, ServiceRelation.FUNCTION_GEOMETER
        )
        return [str(geometer.pk) for geometer in geometers]

    @register_dynamic_group("geometer-ur")
    def resolve_geometer_ur(self, task, case, user, prev_work_item, context, **kwargs):
        return [
            str(Service.objects.get(pk=uri_constants.GEOMETER_SERVICE_ID).pk)
        ]  # AGO (Geometer), Kt. Uri

    @register_dynamic_group("gebaeudeschaetzung-ur")
    def resolve_gebaeudeschaetzung_ur(
        self, task, case, user, prev_work_item, context, **kwargs
    ):
        return [
            str(Service.objects.get(pk=uri_constants.FGS_SERVICE_ID).pk)
        ]  # FGS Fachstelle für Gebäudeschätzung
