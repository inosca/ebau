from collections import defaultdict
from logging import getLogger

from django.conf import settings
from django.core.management.base import BaseCommand

from camac.core.models import (
    InstanceResource,
)
from camac.permissions.utils import extract_allowed_states

log = getLogger(__name__)

STATE_ACTIVE = "ACTIVE"
STATE_REVOKED = "REVOKED"


class Command(BaseCommand):
    """Validate instance resource permissions."""

    help = (
        "Check if instance-resource permissions are complete "
        "and configured in permisisons module"
    )

    ROLE_TO_ACCESSLEVEL = {
        "Einsichtsberechtigte Leitbehörde": "lead-authority-read",
        "construction-control-lead": "construction-control",
        "municipality-lead": "lead-authority",
        "service-lead": "distribution-service",
        "subservice": "distribution-service",
        "support": "support",
    }

    def __init__(self, *args, **kwargs):
        self._seen_logs = set()
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for ir in InstanceResource.objects.all():
            if not ir.require_permission:
                self.log_once(
                    log.info,
                    f"IR {ir.pk} ({ir.get_name()}) has no `require_permission` set - skippping",
                )
                continue
            self._check_ir_and_role(ir)

    def _check_ir_and_role(self, ir):
        mapped_permissions = defaultdict(list)

        for role_acl in ir.role_acls.all():
            role_name = role_acl.role.name
            access_level = self.ROLE_TO_ACCESSLEVEL.get(role_name)
            if not access_level:
                self.log_once(
                    log.info, f"Role {role_name} not mapped to access level - skippping"
                )
                continue
            if access_level not in settings.PERMISSIONS["ACCESS_LEVELS"]:
                self.log_once(
                    log.warning,
                    f"Access level {access_level} not configured yet - skipping",
                )
                continue
            mapped_permissions[role_name].append(role_acl.instance_state.name)

        for role_name, instance_states in mapped_permissions.items():
            access_level = self.ROLE_TO_ACCESSLEVEL.get(role_name)
            permissions = settings.PERMISSIONS["ACCESS_LEVELS"][access_level]
            try:
                permission_cond = next(
                    (
                        cond
                        for perm, cond in permissions
                        if perm == ir.require_permission
                    )
                )
            except StopIteration:
                # This role has no permission defined that maps to the IR
                self.log_once(
                    log.warning,
                    f"{ir.pk} ({ir.get_name()}): Permissions config for "
                    f"'{access_level}': '{ir.require_permission}' is entirely "
                    f"missing. Should be RequireInstanceState({instance_states})",
                )
                return

            permission_module_states = set(extract_allowed_states(permission_cond))
            camac_acl_states = set(instance_states)

            too_much_in_config = permission_module_states - camac_acl_states
            missing_in_config = camac_acl_states - permission_module_states

            for state in sorted(too_much_in_config):
                self.log_once(
                    log.warning,
                    f"{ir.pk} ({ir.get_name()}): Permissions config for "
                    f"'{access_level}': '{ir.require_permission}': State "
                    f"'{state}' should not be there",
                )

            for state in sorted(missing_in_config):
                self.log_once(
                    log.warning,
                    f"{ir.pk} ({ir.get_name()}): Permissions config for "
                    f"'{access_level}': '{ir.require_permission}': State "
                    f"'{state}' is missing",
                )

    def log_once(self, log_fn, message):
        if message not in self._seen_logs:
            self._seen_logs.add(message)
            log_fn(message)
