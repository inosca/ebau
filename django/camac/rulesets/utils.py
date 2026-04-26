from django.conf import settings

from camac.instance.models import Instance
from camac.responsible.domain_logic import ResponsibleServiceDomainLogic
from camac.rulesets.models import ResponsibleUserRule
from camac.settings.modules.rulesets_schema import ResponsibleUserRuleConfig
from camac.user.models import Service


def assign_responsible_user(instance: Instance, service: Service) -> None:
    """Assign the responsible user for a service on an instance.

    This function is currently only being called in a signal
    (`camac.rulesets.signals.assign_responsible_user_on_acl_creation`) that is
    triggered whenever a new ACL from the permissions module is created.
    """

    module_settings: ResponsibleUserRuleConfig = settings.RULESETS.responsible_user_rule

    if (
        not settings.RULESETS.enabled or not module_settings.automatically_assign
    ):  # pragma: no cover
        return

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
