from django.conf import settings

from camac.instance.models import Instance
from camac.instance.utils import get_geometer_service
from camac.permissions import api as permissions_api
from camac.permissions.events.core import EmptyEventHandler
from camac.user.models import Service
from camac.user.utils import get_tax_administration


class PermissionEventHandlerSZ(
    EmptyEventHandler,
):
    def instance_created(self, instance: Instance):
        super().instance_created(instance)
        if instance.case.document.form.slug == "are-geschaeft":
            are_services_slugs = settings.APPLICATION["ARE_SERVICES"]
            for are_service in Service.objects.filter(slug__in=are_services_slugs):
                self.manager.grant(
                    instance=instance,
                    grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                    access_level="are-service",
                    service=are_service,
                    event_name="instance-created",
                )

    def decision_decreed(self, instance: Instance):
        if geometer_service := get_geometer_service(instance):
            self.manager.grant(
                instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level="read",
                service=geometer_service,
            )
        if tax_admin_service := get_tax_administration():
            self.manager.grant(
                instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level="read",
                service=tax_admin_service,
            )
        if (
            form_family := instance.form.family
        ) and form_family.name == "abbruchpraemie":
            self.manager.grant(
                instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level="rpg2-demolition-premium-service",
                service=Service.objects.get(
                    slug=settings.APPLICATION.get(
                        "RPG2_DEMOLITION_PREMIUM_PAYMENT_SERVICE"
                    )
                ),
            )
