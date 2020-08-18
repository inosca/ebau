from camac.constants.kt_bern import (
    SERVICE_GROUP_BAUKONTROLLE,
    SERVICE_GROUP_LEITBEHOERDE_GEMEINDE,
    SERVICE_GROUP_RSTA,
)
from camac.core.models import InstanceService
from camac.user.models import ServiceT


def get_baukontrolle(instance, active_service):
    """
    Find correct service for Baukontrolle.

    kt_bern specific.

    When switching to SB1, it's necessary to set baukontrolle as active service.
    """
    defining_leitbehoerde = active_service
    if active_service.service_group.pk == SERVICE_GROUP_RSTA:
        defining_leitbehoerde = instance.services.filter(
            service_group_id=SERVICE_GROUP_LEITBEHOERDE_GEMEINDE
        ).first()
    elif (
        active_service.service_group.pk == SERVICE_GROUP_BAUKONTROLLE
    ):  # pragma: no cover
        return active_service

    service_t = ServiceT.objects.get(
        language="de", service=defining_leitbehoerde, service__disabled=0
    )
    city = service_t.name.replace("Leitbehörde ", "")
    return (
        ServiceT.objects.filter(
            language="de", name=f"Baukontrolle {city}", service__disabled=False
        )
        .first()
        .service
    )


def set_baukontrolle(instance):
    """
    Switch active service to baukontrolle.

    kt_bern specific.

    When switching to SB1, it's necessary to set baukontrolle as active service.
    """
    active_service = instance.responsible_service()
    baukontrolle = get_baukontrolle(instance, active_service)

    if baukontrolle != active_service:
        # Note: In this special case, we DO NOT deactive the previously
        # active service. "Baukontrolle" is a separate instance service
        # and from now on, there will be two active entries.
        # The `Instance.active_service` is filtering out the "Baukontrolle"
        # service.
        InstanceService.objects.get_or_create(
            service=baukontrolle, instance=instance, defaults={"active": 1}
        )


def unpack_service_emails(queryset):
    """
    In some cases (kt_schwyz) the email field is used as a comma-separated list.

    This accessor returns the email addresses as a flat list.
    """

    for emails in queryset.values_list("email", flat=True):
        if not emails:
            return []

        yield from emails.split(",")
