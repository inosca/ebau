from typing import Type

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from camac.permissions.models import InstanceACL
from camac.rulesets.utils import assign_responsible_user
from camac.settings.modules.rulesets_schema import ResponsibleUserRuleConfig
from camac.settings.utils import is_module_enabled


@receiver(post_save, sender=InstanceACL)
def assign_responsible_user_on_acl_creation(
    sender: Type[InstanceACL],
    instance: InstanceACL,
    created: bool,
    **kwargs: dict,
) -> None:
    """Assign the responsible user for a service on ACL creation."""
    module_settings: ResponsibleUserRuleConfig = settings.RULESETS.responsible_user_rule

    if (
        # Signal is emitted by loading fixtures
        # https://docs.djangoproject.com/en/4.2/ref/signals/#post-save
        kwargs.get("raw")
        # Module is disabled
        or not is_module_enabled("RULESETS")
        or not module_settings.automatically_assign
        # Access level is ignored
        or instance.access_level_id in module_settings.ignored_access_levels
        # ACL is updated
        or not created
        # ACL is not for a service
        or not instance.service
    ):  # pragma: no cover
        return

    assign_responsible_user(instance.instance, instance.service)
