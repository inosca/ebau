from collections import Counter, defaultdict
from collections.abc import Generator
from dataclasses import dataclass, field
from datetime import datetime
from functools import partial
from itertools import islice
from logging import getLogger
from typing import Optional

import tqdm
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from camac.applicants import models as applicants_models
from camac.core.models import InstanceService
from camac.instance.models import Instance
from camac.instance.utils import get_construction_control
from camac.permissions import models as permission_models
from camac.permissions.api import PermissionManager
from camac.permissions.exceptions import RevocationRejected

log = getLogger(__name__)

STATE_ACTIVE = "ACTIVE"
STATE_REVOKED = "REVOKED"


@dataclass
class ACL:
    instance_id: int
    access_level: str
    state: str
    type: permission_models.GRANT_CHOICES

    user_id: Optional[int] = field(default=None)
    service_id: Optional[int] = field(default=None)

    # Non-identifying optional attributes: These are used
    # to pass in additional data to be used during *creation*,
    # but are ignored when comparing ACLs
    start_time: Optional[datetime] = field(default=None)
    metainfo: Optional[dict] = field(default_factory=dict)
    created_by_event: Optional[str] = field(default=None)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        # explicitly exclude hidden attrs. Also, we compare the
        # string representation of the attributes, so as not to
        # get confused: Some data sources may give us stringified references
        # while the ORM gives int/uuid foreign keys.
        return hash(
            (
                str(self.instance_id),
                str(self.access_level),
                str(self.state),
                str(self.type),
                str(self.user_id),
                str(self.service_id),
            )
        )


class Command(BaseCommand):
    """
    Migrate permission-relevant data onto the permissions module.

    This works as follows: The code builds up an "expected" permission structure
    that is directly derived from the relevant data in the database, and similarly,
    builds a comparable structure from the permissions effectively granted.

    Depending on the mode, the differences are logged (--check-only), or
    ACLs are granted/revoked such that the result reflects the situation
    as needed.
    """

    help = "Migrate permission-relevant data onto the permissions module."

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit", help="Do commit the changes", action="store_true"
        )
        parser.add_argument(
            "--check-only",
            help="Check mode: Log a warning if a required permission is missing",
            action="store_true",
        )
        parser.add_argument(
            "--min-instance-id",
            help="Minimum instance ID to process. Defaults to zero",
        )
        parser.add_argument(
            "--max-instance-id",
            help="Maximum instance ID to process. Defaults to max instance id",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        savepoint = transaction.savepoint()

        # Keys virtual ACLs to actual ACLs, in case we need to revoke them
        self._existing_acls = {}

        self.min_instance_id = options.get("min_instance_id", 0) or 0
        self.max_instance_id = (
            options.get("max_instance_id", 0)
            # Yeah we go a bit too far in the max number - just to avoid off-by-one or
            # instance creations between *now* and when the script starts actually doing
            # work
            or Instance.objects.order_by("-pk").first().pk + 1000
        )
        self.do_check = options.get("check_only", False)
        self.verbosity = options.get("verbosity", 1)

        do_commit = options.get("commit")

        if errors := self._config_has_errors():
            log.warning(f"Permissions config broken, detected {errors} errors")
            return

        if do_commit and self.do_check:
            log.warning("Cannot run commit and check mode at the same time, aborting")
            return

        # Log before so user knows what's going to happen before (as this script
        # will run for quite a while)
        if do_commit:
            log.warning("Warning: changes will be written to database!")
        elif not self.do_check:
            log.info("Pretend mode - Database content will NOT been altered")
        elif self.do_check:
            log.info(
                "Check mode: No change will be written, but proposed changes are printed"
            )

        self.run_migration()

        # Log (and commit/rollback transaction) after the run
        if do_commit:
            log.info("Committing changes to DB")
            transaction.savepoint_commit(savepoint)
        else:
            if not self.do_check:
                # We're not in check mode - but we need to let the
                # user know what's happening. In check mode, the expectation
                # is that nothing changes,
                log.info("Pretend mode - DB has NOT been altered")
            transaction.savepoint_rollback(savepoint)

    def _config_has_errors(self):
        errors = 0
        for internal, level_slug in settings.PERMISSIONS.get("MIGRATION", {}).items():
            level_configured = level_slug in settings.PERMISSIONS["ACCESS_LEVELS"]
            level_in_db = permission_models.AccessLevel.objects.filter(
                pk=level_slug
            ).exists()
            # TODO should check internal name reference as well

            if not level_configured:
                errors += 1
                log.warning(f"Access level '{level_slug}' has no configuration")
            if not level_in_db:
                errors += 1
                log.warning(f"Access level '{level_slug}' is missing in database")

        return errors

    def run_migration(self):
        log.info("Building expected permissions structure. This will take a while")
        expected_permissions = self._build_permissions_structure()
        log.info("Loading actual permission data. This may take a while as well")
        actual_permissions = set(self._read_permissions_structure())

        if self.do_check:
            self._log_differences(expected_permissions, actual_permissions)
        else:
            self._apply_changes(expected_permissions, actual_permissions)

    def _iter_qs(self, qs, instance_prefix):
        """Turn given QS into progress-bar iterator, and optionally limit it.

        The given queryset is filtered, such that if the user passed
        `--min-instance-id` or `--max-instance-id`, only a subset of instances
        is actually used.

        Also, depending on verbosity level, a progress bar is added to the
        resulting iterator for better output on the terminal.
        """

        prefix = f"{instance_prefix}__" if instance_prefix else ""

        qs = qs.filter(
            **{
                f"{prefix}pk__gte": self.min_instance_id,
                f"{prefix}pk__lte": self.max_instance_id,
            }
        )
        return tqdm.tqdm(
            qs.iterator(),
            total=qs.count(),
            # If verbosity is high, this will just interfere
            disable=self.verbosity > 1,
        )

    def _log_differences(self, expected_permissions, actual_permissions):
        equal = expected_permissions.intersection(actual_permissions)
        to_create = expected_permissions - actual_permissions
        to_delete = actual_permissions - expected_permissions

        changes_by_instance = defaultdict(set)

        for acl in to_create:
            changes_by_instance[acl.instance_id].add(("grant", acl))
        for acl in to_delete:
            changes_by_instance[acl.instance_id].add(("revoke", acl))
        for instance, ops in changes_by_instance.items():
            if self.verbosity > 1:
                by_op = Counter(op for op, _ in ops)
                changes = ",".join([f"{n} {o}" for o, n in by_op.items()])
                log.info(
                    f"Instance {instance} has permission mismatches. Changes: {changes}"
                )
            if self.verbosity > 2:
                for op, acl in ops:
                    log.info(f"   {op} {acl}")

        log.info(
            f"Summary: {len(equal)} ACLs unchanged, {len(to_delete)} ACLs "
            f"to revoke, {len(to_create)} ACLs to create"
        )
        if to_delete or to_create:
            log.warning(
                "This is NOT expected if you ran the migration before. "
                "There should be only unchanged ACLs"
            )
        else:
            log.info("All good, everything as expected")

    def _build_permissions_structure(self):
        conf = settings.PERMISSIONS["MIGRATION"]

        permissions = set()
        if applicant_accesslevel := conf.get("APPLICANT"):
            permissions.update(self._build_applicant_permissions(applicant_accesslevel))
        if lead_authority := conf.get("MUNICIPALITY"):
            inactive_lead_authority = conf.get("MUNICIPALITY_INVOLVED")
            permissions.update(
                self._build_municipality_permissions(
                    lead_authority, inactive_lead_authority
                )
            )
        if invited_service := conf.get("DISTRIBUTION_INVITEE"):
            permissions.update(self._build_distribution_permissions(invited_service))
        if construction_control := conf.get("CONSTRUCTION_CONTROL"):
            permissions.update(
                self._build_construction_control_permissions(construction_control)
            )

        return permissions

    def _build_construction_control_permissions(self, construction_control):
        qs = Instance.objects.all()

        # TODO this is stolen from the attachment (document) module, but
        # serves the same purpose
        after_decision_states = settings.APPLICATION.get(
            "ATTACHMENT_AFTER_DECISION_STATES", None
        )

        if after_decision_states:
            qs = qs.filter(instance_state__name__in=after_decision_states)

        inst_iter = self._iter_qs(qs, instance_prefix=None)
        log.info(f"    Checking {inst_iter.total} instances for construction control")
        for instance in inst_iter:
            municipality_svc = instance.responsible_service()
            try:
                construction_control = get_construction_control(municipality_svc)
            except Exception:
                # TODO log?
                pass
                continue

            yield ACL(
                access_level="construction-control",
                state=STATE_ACTIVE,
                service_id=construction_control.pk,
                instance_id=instance.pk,
                type=permission_models.GRANT_CHOICES.SERVICE.value,
                start_time=timezone.now(),
            )

    def _build_municipality_permissions(self, level_active, level_inactive):
        # Note: This is roughly derived from
        # InstanceQuerysetMixin.get_queryset_for_municipality()
        log.info("  Checking for municipality access rules")

        make_lead_acl = partial(ACL, access_level=level_active, state=STATE_ACTIVE)
        make_involved_acl = partial(
            ACL, access_level=level_inactive, state=STATE_ACTIVE
        )

        # Instance Services map quite nicely. TODO: Only responsible services,
        # or only of a certain service group?
        is_iter = self._iter_qs(InstanceService.objects.filter(), "instance")
        log.info(f"    Checking {is_iter.total} instance services")

        for instance_service in is_iter:
            build_fn = make_lead_acl if instance_service.active else make_involved_acl
            yield build_fn(
                instance_id=instance_service.instance_id,
                type=permission_models.GRANT_CHOICES.SERVICE.value,
                service_id=instance_service.service_id,
                #
                start_time=instance_service.activation_date or timezone.now(),
                metainfo={"instance-service-id": instance_service.pk},
            )

        if not settings.APPLICATION.get("USE_INSTANCE_SERVICE"):
            inst_iter = self._iter_qs(Instance.objects.all(), "")
            log.info(f"    Checking {inst_iter.total} instance's groups")

            for inst in inst_iter:
                # submit date is set in the submit serializer:
                # CalumaInstanceSubmitSerializer._set_submit_date()
                submit_date = inst.case.meta.get("submit-date") if inst.case else None
                yield make_lead_acl(
                    instance_id=inst.pk,
                    type=permission_models.GRANT_CHOICES.SERVICE.value,
                    service_id=inst.group.service_id,
                    #
                    start_time=submit_date or timezone.now(),
                    metainfo={"instance-group-id": str(inst.group.pk)},
                )

    def _build_distribution_permissions(self, access_level):
        make_acl = partial(ACL, access_level=access_level, state=STATE_ACTIVE)

        if not settings.DISTRIBUTION:
            log.warning(
                "Non-Distribution workflows are not supported, "
                "as they are on the way out (Last canton is UR, and "
                "the next full release is dropping it)"
            )
            return

        wi_iter = self._iter_qs(
            WorkItem.objects.filter(
                task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
            ).exclude(
                status__in=[
                    WorkItem.STATUS_SUSPENDED,
                    WorkItem.STATUS_CANCELED,
                ],
            ),
            "case__family__instance",
        )
        log.info(f"    Checking {wi_iter.total} work items")
        for workitem in wi_iter:
            # Probably never multiple, but it's a list and we want to
            # be clean
            for service_id in workitem.addressed_groups:
                yield make_acl(
                    instance_id=workitem.case.family.instance.pk,
                    type=permission_models.GRANT_CHOICES.SERVICE.value,
                    service_id=service_id,
                    #
                    start_time=workitem.created_at or timezone.now(),
                    metainfo={"work-item-id": str(workitem.pk)},
                )

    def _build_applicant_permissions(self, level):
        appl_iter = self._iter_qs(
            applicants_models.Applicant.objects.all().filter(invitee__isnull=False),
            instance_prefix="instance",
        )
        log.info(f"  Checking {appl_iter.total} applicants")
        for app in appl_iter:
            app: applicants_models.Applicant
            # Note: non-invitee applicant entries are a "normal" situation.
            # They will get an ACL as soon as the invitee actually logs in and
            # can be linked.
            yield ACL(
                instance_id=app.instance.pk,
                access_level=level,
                state=STATE_ACTIVE,
                type=permission_models.GRANT_CHOICES.USER.value,
                user_id=app.invitee_id,
                #
                created_by_event="applicant_added",
                start_time=app.created,
                metainfo={"related-applicant-id": app.pk},
            )

    def _read_permissions_structure(self):
        # We exclude all manual ACLs. Those are granted/revoked by user and
        # therefore cannot, by definition, be derived from other structures /
        # data in the application.
        # Also, we're only reading the active ACLs - the revoked ones don't have
        # any effect on the *current* situation!
        qs = permission_models.InstanceACL.objects.exclude(
            created_by_event="manual-creation"
        ).exclude(end_time__lte=timezone.now())
        for acl in self._iter_qs(qs, instance_prefix="instance"):
            aclstate = STATE_ACTIVE if acl.is_active() else STATE_REVOKED
            virtual_acl = ACL(
                instance_id=acl.instance_id,
                access_level=acl.access_level_id,
                # TODO should we really handle scheduled ones? I guess they won't be
                # a thing for a while
                state=aclstate,
                type=acl.grant_type,
                user_id=acl.user_id,
                service_id=acl.service_id,
                start_time=acl.start_time,
                metainfo=acl.metainfo,
            )
            self._existing_acls[virtual_acl] = acl
            yield virtual_acl

    def _apply_changes(self, expected_permissions, actual_permissions):
        to_create = expected_permissions - actual_permissions
        to_delete = actual_permissions - expected_permissions

        # We create the instance ACLs in bulk, in batches of 500. This should
        # speed up things while also keeping memory usage at a sane level.
        # (naive bulk_create() would return all instance acls as one big list,
        # and since we don't actually *need* the result, we make smaller batches
        # and instantly forget about the results)

        if self.verbosity >= 1:
            log.info(f"Granting {len(to_create)} new ACLs")

        to_create_models = (
            permission_models.InstanceACL(
                instance_id=acl.instance_id,
                user_id=acl.user_id,
                service_id=acl.service_id,
                created_by_event=acl.created_by_event,
                grant_type=acl.type,
                access_level_id=acl.access_level,
                metainfo={**acl.metainfo, "migrated_at": timezone.now().isoformat()},
                start_time=acl.start_time,
            )
            for acl in to_create
        )

        # Needs to be generator to avoid too much memory usage by
        # having all the acls in memory at once (internal representation
        # is already enough)
        assert isinstance(to_create_models, Generator)

        proggy = tqdm.tqdm(total=len(to_create))
        batch_size = 200
        while True:
            batch = list(islice(to_create_models, batch_size))
            if not batch:
                break
            permission_models.InstanceACL.objects.bulk_create(batch)
            proggy.update(len(batch))
        proggy.close()

        manager = PermissionManager.for_anonymous()

        log.info(f"Revoking {len(to_delete)} ACLs...")
        for acl in tqdm.tqdm(to_delete, disable=self.verbosity > 1):
            if self.verbosity > 1:
                log.info(f"Revoking ACL: {acl}")
            try:
                manager.revoke(
                    self._existing_acls[acl], event_name="permissions-migration"
                )
            except RevocationRejected:  # pragma: no cover
                log.warning(
                    f"Already-revoked {acl} being revoked again! "
                    "This is likely a programming error"
                )

        log.info(
            f"Summary: {len(to_create)} ACLs created, {len(to_delete)} ACLs revoked"
        )
