from logging import getLogger

from django.conf import settings

from camac.instance.models import Instance
from camac.permissions import api as permissions_api
from camac.permissions.models import AccessLevel, InstanceACL
from camac.user.models import Service

log = getLogger(__name__)

APPLICANT_ACCESS_LEVEL = "applicant"


class ApplicantsEventHandlerMixin:
    def applicant_added(self, instance, applicant):
        # Add an applicant ACL when an applicant is added to the
        # instance (instance.involved_applicants).
        if not applicant.invitee:
            # Non-user applicant, can't do anything right now.
            # This will be called again once the invitee logs in
            return
        try:
            self.manager.grant(
                instance,
                grant_type=permissions_api.GRANT_CHOICES.USER.value,
                access_level=APPLICANT_ACCESS_LEVEL,
                user=applicant.invitee,
                event_name="applicant_added",
                metainfo={"disable-notification-on-creation": True},
            )
        except AccessLevel.DoesNotExist:
            log.warning(f"Access level '{APPLICANT_ACCESS_LEVEL}' is not configured")

    def applicant_removed(self, instance, applicant):
        # See if our applicant has a permission, then revoke if
        # it exists
        acls = InstanceACL.objects.filter(
            instance=instance,
            user=applicant.invitee,
            access_level=APPLICANT_ACCESS_LEVEL,
        )
        if not acls and getattr(applicant, "invitee"):  # pragma: no cover
            # applicant (with invitee, so not an email invite) didn't have an
            # ACL - this is no good
            log.warning(
                f"Applicant on instance {instance.pk} ({applicant.invitee}) "
                "removed, but no matching ACL found. This should never happen!"
            )
            return
        for acl in acls:
            # Note: There should never be multiple acls for the same
            # applicant, but as there's no DB constraint enforcing this,
            # we loop to make sure we get all the affected ACLs
            self.manager.revoke(acl, event_name="applicant_removed")


class InstanceSubmissionHandlerMixin:
    def instance_submitted(self, instance: Instance):
        if settings.APPLICATION.get("USE_INSTANCE_SERVICE"):
            self.manager.grant(
                instance,
                grant_type="SERVICE",
                access_level="lead-authority",
                service=instance.responsible_service(),
                event_name="instance-submitted",
            )
        else:
            group_service = instance.group.service
            self.manager.grant(
                instance,
                grant_type="SERVICE",
                access_level="lead-authority",
                service=group_service,
                event_name="instance-submitted",
            )


class ChangeResponsibleServiceHandlerMixin:
    def changed_responsible_service(
        self, instance: Instance, from_service: Service, to_service: Service
    ):
        # First: Degrade old lead authority to involved authority
        old_acl = (
            InstanceACL.currently_active()
            .filter(
                service=from_service,
                access_level="lead-authority",
                instance=instance,
            )
            .first()
        )
        if old_acl:
            self.manager.revoke(old_acl)
        else:  # pragma: no cover
            log.warning(
                f"Old lead authority service {from_service.pk} on instance "
                f"{instance.pk} had no lead-authority ACL!"
            )

        self.manager.grant(
            instance,
            grant_type="SERVICE",
            access_level="involved-authority",
            service=from_service,
        )

        # Second: Grant new authority the lead
        self.manager.grant(
            instance,
            grant_type="SERVICE",
            access_level="lead-authority",
            service=to_service,
        )


class DistributionHandlerMixin:
    def inquiry_sent(self, instance: Instance, work_item):
        for addr in work_item.addressed_groups:
            addr_service = Service.objects.get(pk=addr)
            self.manager.grant(
                instance,
                grant_type="SERVICE",
                access_level="distribution-service",
                service=addr_service,
            )
