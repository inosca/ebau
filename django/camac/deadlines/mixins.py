from camac.caluma.models import Instance
from camac.constants.kt_gr import ARE_SERVICE_GROUP
from camac.core.utils import canton_aware
from camac.user.models import Service


class DeadlinePermissionMixin:
    @canton_aware
    def allowed_service_groups(self):
        """Decide which service groups are allowed to use deadlines."""
        return ["municipality"]

    def allowed_service_groups_gr(self):
        """In GR, deadlines are also enabled for ARE."""
        return ["municipality", ARE_SERVICE_GROUP]

    def allowed_service_groups_ag(self):
        """
        In AG, deadlines are also enabled for AfB.

        Service-cantonal will also see the suspensions, but they query for the
        AfB service directly.
        Subservices will query for their parent service, and they will query
        for their parent service directly.
        """
        return ["municipality", "service-afb"]

    def has_deadline_access(self, service: Service) -> bool:
        """Check if the service group is allowed."""
        return (
            service
            and service.service_group
            and service.service_group.name in self.allowed_service_groups()
        )

    @canton_aware
    def has_instance_access(self, instance: Instance, service: Service) -> bool:
        """Check if a service has access to an instance."""
        return self.has_deadline_access(service) and (
            service.pk == instance.responsible_service().pk
            or instance.has_inquiry(service.pk)
        )

    def has_instance_access_gr(self, instance: Instance, service: Service) -> bool:
        """In GR, some dossier types do not allow deadlines."""
        if str(instance.case.family.document.form.pk).startswith(
            "vorlaeufige-beurteilung"
        ):
            return False

        return self.has_deadline_access(service) and (
            service.pk == instance.responsible_service().pk
            or instance.has_inquiry(service.pk)
        )
