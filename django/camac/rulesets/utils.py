from camac.instance.models import Instance
from camac.responsible.domain_logic import ResponsibleServiceDomainLogic
from camac.rulesets.models import ResponsibleUserRule
from camac.user.models import Service


def assign_responsible_user(instance: Instance, service: Service) -> None:
    """Assign the responsible user for a service on an instance."""

    if instance.responsible_services.filter(service=service).exists():
        return

    responsible_user = ResponsibleUserRule.objects.get_responsible_user_for_instance(
        instance, service
    )

    if not responsible_user:
        return

    responsible_service = instance.responsible_services.create(
        service=service,
        responsible_user=responsible_user,
    )

    ResponsibleServiceDomainLogic.update_work_item_assigned_user(responsible_service)
