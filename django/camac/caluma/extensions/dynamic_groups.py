import logging

from caluma.caluma_workflow.dynamic_groups import (
    BaseDynamicGroups,
    register_dynamic_group,
)

from camac.core.models import Activation, Circulation
from camac.instance.models import Instance
from camac.user.models import Service

log = logging.getLogger()


class CustomDynamicGroups(BaseDynamicGroups):
    def _get_activation(self, context):
        if not context:
            return Activation.objects.none()

        return Activation.objects.filter(pk=context.get("activation-id")).first()

    def _get_circulation(self, context):
        if not context:
            return Circulation.objects.none()

        return Circulation.objects.filter(pk=context.get("circulation-id")).first()

    def _get_responsible_service(self, case, filter_type, context):
        instance = (
            case.family.instance
            if hasattr(case.family, "instance")
            else Instance.objects.get(pk=context.get("instance"))
        )
        service = instance.responsible_service(filter_type=filter_type)

        if not service:
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

    @register_dynamic_group("circulation_service")
    def resolve_circulation_service(
        self, task, case, user, prev_work_item, context, **kwargs
    ):
        circulation = self._get_circulation(context)

        if not circulation:
            log.error("No service group found with the given context")
            return []

        return [str(circulation.service.pk)]

    @register_dynamic_group("activation_service")
    def resolve_activation_service(
        self, task, case, user, prev_work_item, context, **kwargs
    ):
        activation = self._get_activation(context)

        if not activation:
            log.error("No service group found with the given context")

            return []

        return [str(activation.service.pk)]

    @register_dynamic_group("activation_service_parent")
    def resolve_activation_service_parent(
        self, task, case, user, prev_work_item, context, **kwargs
    ):
        activation = self._get_activation(context)

        if not activation:
            log.error("No service_parent group found with the given context")

            return []

        return [str(activation.service_parent.pk)]

    @register_dynamic_group("distribution_create_inquiry")
    def resolve_distribution_create_inquiry(
        self, task, case, user, prev_work_item, context, **kwargs
    ):
        if context and context.get("addressed_groups") and prev_work_item:
            services = Service.objects.filter(
                pk__in=[
                    # Target service for the inquiry
                    *context.get("addressed_groups", []),
                    # Service that created an inquiry
                    *prev_work_item.addressed_groups,
                ],
                service_parent__isnull=True,  # Subservices can't create any inquiries
            )
            return [str(pk) for pk in services.values_list("pk", flat=True)]

        # If no context is given it's the first "create-inquiry" work item in
        # the distribution case which must be assigned to the municipality
        return self.resolve_municipality(
            task, case, user, prev_work_item, context, **kwargs
        )
