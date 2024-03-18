from logging import getLogger

from camac.permissions import api as permissions_api
from camac.permissions.events import EmptyEventHandler
from camac.permissions.models import AccessLevel, InstanceACL

log = getLogger(__name__)

APPLICANT_ACCESS_LEVEL = "applicant"


class ApplicantsEventHandlerMixin(EmptyEventHandler):
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
