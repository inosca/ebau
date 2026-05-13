from logging import getLogger

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, IntegerField, OuterRef, Value
from django.db.models.functions import Cast

from camac.applicants.models import Applicant
from camac.caluma.models import Inquiry
from camac.core.models import InstanceService
from camac.instance.models import Instance
from camac.permissions.models import InstanceACL
from camac.user.utils import get_support_role

log = getLogger(__name__)


class Command(BaseCommand):
    """Verify the permissions module migration."""

    help = "Verify migration of permission-relevant data onto the permissions module."
    results = {}

    @transaction.atomic
    def handle(self, *args, **options):
        passed = self.perform_acl_checks()
        passed &= self.perform_sanity_checks()

        log_message = f"Verification finished: {'PASSED' if passed else 'FAILED'}"
        if passed:
            log.info(log_message)
        else:
            log.error(log_message)

    def perform_sanity_checks(self):
        # Every instance should at least be accessible by the support
        passed = self.assert_instance_access("SUPPORT")

        return passed

    def assert_instance_access(self, access_level_key):
        """
        Ensure the access level (identified by the given config key) is migrated.

        This means that each instance has at least one ACL for this access level.
        """
        access_level = self.get_access_level(access_level_key)
        if not access_level:
            # Cannot be asserted if access level isn't configured for migration
            log.error(
                f"Check whether all instances have an ACL for access level "
                f"'{access_level_key}': NOT OK (missing access level configuration)"
            )
            return False

        # Assert that every instance has an acl for the defined access level
        instances_missing_acl = list(
            Instance.objects.filter(
                ~Exists(
                    InstanceACL.currently_active().filter(
                        access_level=access_level,
                        instance_id=OuterRef("pk"),
                        end_time__isnull=True,
                    )
                )
            ).values_list("pk", flat=True)
        )

        passed = not instances_missing_acl

        log_message = (
            f"Check whether all instances have an ACL for access level "
            f"'{access_level}': {'OK' if passed else 'NOT OK'} (instances without "
            f"ACL: {len(instances_missing_acl)})"
        )

        if passed:
            log.info(log_message)
        else:
            log.error(log_message)
            log.error(
                f"Instances without ACL for access level '{access_level}': "
                f"{instances_missing_acl}"
            )

        return passed

    def perform_acl_checks(self):
        if applicant := self.get_access_level("APPLICANT"):
            self.check_applicants(applicant)

        if lead_authority := self.get_access_level("MUNICIPALITY"):
            self.check_instance_services(
                lead_authority, is_municipality=True, is_active=True
            )

        if involved_lead_authority := self.get_access_level("MUNICIPALITY_INVOLVED"):
            self.check_instance_services(
                involved_lead_authority, is_municipality=True, is_active=False
            )

        if construction_control := self.get_access_level("CONSTRUCTION_CONTROL"):
            self.check_instance_services(
                construction_control, is_municipality=False, is_active=True
            )

        if involved_construction_control := self.get_access_level(
            "CONSTRUCTION_CONTROL_INVOLVED"
        ):
            self.check_instance_services(
                involved_construction_control, is_municipality=False, is_active=False
            )

        if invited_service := self.get_access_level("DISTRIBUTION_INVITEE"):
            self.check_distribution_services(invited_service)

        if _ := self.get_access_level("USO"):
            # TODO: Implement check for access level USO if needed for
            # other cantons
            raise NotImplementedError()

        if support := self.get_access_level("SUPPORT"):
            self.check_support(support)

        return self.log_results_acl_checks()

    def get_access_level(self, access_level_key):
        conf = settings.PERMISSIONS["MIGRATION"]

        access_level = conf.get(access_level_key)
        if not access_level:
            log.warning(
                f"WARNING: No access level for '{access_level_key}' "
                f"configured for permissions migration"
            )

        return access_level

    def log_results_acl_checks(self):
        passed = True

        for access_level, diff in self.results.items():
            num_objects = diff["num_objects"]
            num_deduplicated_objects = diff["num_deduplicated_objects"]
            num_acls = diff["num_acls"]
            missing = diff.get("missing", [])
            unexpected = diff.get("unexpected", [])

            failed = missing or unexpected

            log_message = (
                f"Access level '{access_level}': {'NOT OK' if failed else 'OK'}\n"
                f"Objects: {num_objects}\n"
                f"Deduplicated objects: {num_deduplicated_objects}\n"
                f"ACLs: {num_acls}\n"
                f"Missing: {len(missing)}\n"
                f"Unexpected: {len(unexpected)}"
            )

            if failed:
                log.error(log_message)
                log.error(f"Missing instance acls: {missing}")
                log.error(f"Unexpected instance acls: {unexpected}")
            else:
                log.info(log_message)

            passed &= not failed

        return passed

    def get_instance_acls(self, access_level, entity_lookup):
        return (
            InstanceACL.currently_active()
            .filter(access_level=access_level)
            .values_list("instance__pk", entity_lookup)
        )

    def write_differences(self, access_level, objects, acls):
        self.results[access_level] = {
            "num_objects": len(objects),
            "num_deduplicated_objects": len(set(objects)),
            "num_acls": len(acls),
        }
        if set(objects) != set(acls):
            self.results[access_level]["missing"] = list(set(objects) - set(acls))
            self.results[access_level]["unexpected"] = list(set(acls) - set(objects))

    def check_applicants(self, access_level):
        applicants = Applicant.objects.filter(
            invitee__isnull=False,
        ).values_list("instance__pk", "invitee__pk")

        applicant_acls = self.get_instance_acls(access_level, entity_lookup="user__pk")

        self.write_differences(access_level, applicants, applicant_acls)

    def check_instance_services(self, access_level, is_municipality, is_active):
        service_groups = (
            ["municipality", "district", "lead-service"]
            if is_municipality
            else ["construction-control"]
        )

        instance_services = InstanceService.objects.filter(
            service__service_group__name__in=service_groups,
            active=1 if is_active else 0,
        ).values_list("instance__pk", "service__pk")

        instance_service_acls = self.get_instance_acls(
            access_level, entity_lookup="service__pk"
        )

        self.write_differences(access_level, instance_services, instance_service_acls)

    def check_distribution_services(self, access_level):
        distribution_services = (
            Inquiry.objects.only_active()
            # Assume that there is only one addressed distribution service,
            # although multiple are technically possible
            .annotate(addressed=Cast("addressed_groups__0", IntegerField()))
            .values_list("case__family__instance__pk", "addressed")
        )

        distribution_service_acls = self.get_instance_acls(
            access_level, entity_lookup="service__pk"
        )

        self.write_differences(
            access_level, distribution_services, distribution_service_acls
        )

    def check_support(self, access_level):
        support_role_id = get_support_role().pk
        support_instances = Instance.objects.annotate(
            support_role_id=Value(support_role_id)
        ).values_list("pk", "support_role_id")

        support_acls = self.get_instance_acls(access_level, entity_lookup="role__pk")

        self.write_differences(access_level, support_instances, support_acls)
