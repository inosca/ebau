from logging import getLogger
from typing import Literal

from caluma.caluma_workflow.models import WorkItem

from camac.caluma.api import CalumaApi
from camac.instance.models import Instance
from camac.instance.utils import get_provider_services
from camac.permissions import api as permissions_api
from camac.permissions.models import AccessLevel, InstanceACL
from camac.rulesets.utils import assign_responsible_user
from camac.user.models import Service, ServiceRelation
from camac.user.utils import get_support_role

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
            )
        except AccessLevel.DoesNotExist:
            log.warning(f"Access level '{APPLICANT_ACCESS_LEVEL}' is not configured")

    def applicant_removed(self, instance, applicant):
        # See if our applicant has a permission, then revoke if
        # it exists
        acls = InstanceACL.currently_active().filter(
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
        if CalumaApi().is_paper(instance):
            # Paper dossiers get the lead authority ACL upon creation, so no need to do it here.
            # See InstanceCreationHandlerMixin.instance_created()

            # We have to do the assignement here manually because the ACL was already granted
            # and otherwise the responsible user will not be assigned after submission.
            assign_responsible_user(instance, instance.responsible_service())
            return

        self.manager.grant(
            instance,
            grant_type="SERVICE",
            access_level="lead-authority",
            service=instance.responsible_service(),
            event_name="instance-submitted",
        )


class ChangeResponsibleServiceHandlerMixin:
    def changed_responsible_service(
        self,
        instance: Instance,
        from_service: Service,
        to_service: Service,
        service_type: Literal["municipality", "construction_control"],
    ):
        if service_type not in [
            "municipality",
            "construction_control",
        ]:  # pragma: no cover
            log.warning(
                f"Changing responsible service with service type"
                f"{service_type} on instance {instance.pk} is not supported."
            )
            return

        active_access_level = (
            "construction-control"
            if service_type == "construction_control"
            else "lead-authority"
        )

        involved_access_level = (
            "involved-construction-control"
            if service_type == "construction_control"
            else "involved-authority"
        )

        # Degrade old active responsible service to involved
        # responsible service
        old_active_acl = (
            InstanceACL.currently_active()
            .filter(
                service=from_service,
                access_level=active_access_level,
                instance=instance,
            )
            .first()
        )
        if old_active_acl:
            self.manager.revoke(
                old_active_acl, event_name="changed-responsible-service"
            )
        else:  # pragma: no cover
            log.warning(
                f"Old responsible service {from_service.pk} on instance "
                f"{instance.pk} had no responsible service ACL!"
            )

        self.manager.grant(
            instance,
            grant_type="SERVICE",
            access_level=involved_access_level,
            service=from_service,
            event_name="changed-responsible-service",
        )

        # Revoke involved responsible service acl, if the new active
        # responsible service was previously already involved
        old_involved_acl = (
            InstanceACL.currently_active()
            .filter(
                service=to_service,
                access_level=involved_access_level,
                instance=instance,
            )
            .first()
        )
        if old_involved_acl:
            self.manager.revoke(
                old_involved_acl, event_name="changed-responsible-service"
            )

        # Grant new responsible service the lead
        self.manager.grant(
            instance,
            grant_type="SERVICE",
            access_level=active_access_level,
            service=to_service,
            event_name="changed-responsible-service",
        )

    def unsubscribed_responsible_service(
        self,
        instance: Instance,
        service: Service,
        service_type: Literal["municipality", "construction_control"],
    ):
        if service_type not in [
            "municipality",
            "construction_control",
        ]:  # pragma: no cover
            log.warning(
                f"Unsubscribing involved responsible service with service type"
                f"{service_type} on instance {instance.pk} is not supported."
            )
            return

        involved_access_level = (
            "involved-construction-control"
            if service_type == "construction_control"
            else "involved-authority"
        )

        acl = (
            InstanceACL.currently_active()
            .filter(
                service=service,
                access_level=involved_access_level,
                instance=instance,
            )
            .first()
        )

        if acl:
            self.manager.revoke(acl, event_name="unsubscribed-responsible-service")
        else:  # pragma: no cover
            log.warning(
                f"Old involved responsible service {service.pk} on instance "
                f"{instance.pk} had no involved responsible service ACL!"
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
                event_name="inquiry-sent",
            )


class InstanceCreationHandlerMixin:
    def instance_created(self, instance: Instance):
        if CalumaApi().is_paper(instance):
            # Paper dossiers are created by the municipality and need access immediately, so
            # we're creating the required lead authority ACL right here
            self.manager.grant(
                instance,
                grant_type="SERVICE",
                access_level="lead-authority",
                service=instance.responsible_service(),
                event_name="instance-created",
            )

        support_role = get_support_role()
        self.manager.grant(
            instance,
            grant_type="ROLE",
            access_level="support",
            role=support_role,
            event_name="instance-created",
        )


class InstanceCopyHandlerMixin:
    def instance_copied(
        self,
        instance: Instance,
        from_instance: Instance,
    ):
        current_acls = InstanceACL.currently_active().filter(
            instance=from_instance,
        )
        if (
            instance.case.meta.get("is-appeal")
            or instance.case.meta.get("is-rejected-appeal")
            or instance.case.meta.get("is-copy")
        ):
            # Handle lead authority and involved lead authority acls (matches
            # logic in copy instance, which adds all instance services from
            # previous instance, excluding construction controls) - applicant
            # and support acls are handled by instance creation
            current_acls = current_acls.filter(
                access_level_id__in=[
                    "lead-authority",
                    "involved-authority",
                ]
            )

            # Grant new acls to reflect creation date of copied instance
            for acl in current_acls:
                self.manager.grant(
                    instance=instance,
                    grant_type=acl.grant_type,
                    access_level=acl.access_level,
                    service=acl.service,
                    user=acl.user,
                    event_name="instance-copied",
                )

            return

        # else: if we don't have any appeal flag, copy everything. This is a
        # commandline copy, not a "part-of-the-process-process" copy
        for acl in current_acls:
            acl.pk = None
            acl.instance = instance
            acl.save()


class ConstructionMonitoringHandlerMixin:
    def geometer_work_item_created(self, work_item: WorkItem):
        if "geometer" in work_item.task.address_groups:
            for addr in work_item.addressed_groups:
                if (
                    not InstanceACL.currently_active()
                    .filter(
                        instance=work_item.case.family.instance,
                        service=addr,
                    )
                    .exists()
                ):
                    self.manager.grant(
                        work_item.case.family.instance,
                        grant_type="SERVICE",
                        access_level="geometer",
                        service=Service.objects.get(pk=addr),
                        event_name="received-work-item",
                    )


class GeometerHandlerMixin:
    def grant_geometer_permission(self, work_item: WorkItem):
        instance = work_item.case.instance
        geometer_service = get_provider_services(
            instance.responsible_service(),
            ServiceRelation.FUNCTION_GEOMETER,
        ).first()

        if geometer_service:
            self.manager.grant(
                instance,
                grant_type="SERVICE",
                access_level="geometer",
                service=geometer_service,
                event_name="formal-exam-completed",
            )
