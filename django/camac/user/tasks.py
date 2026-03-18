from logging import getLogger

from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow.models import WorkItem
from django.db import transaction
from django.db.models import Exists, OuterRef
from django.utils import timezone

from camac.caluma.api import CalumaApi
from camac.constants import kt_bern as be_constants
from camac.instance import models as instance_models
from camac.permissions.events import core as permissions_events
from camac.permissions.models import InstanceACL
from camac.user.models import ServiceRelation

caluma_api = CalumaApi()
log = getLogger(__name__)


def _should_perform_geometer_change_for_instance(instance, selected_municipality):
    active_service = instance.responsible_service(filter_type="municipality")
    if not active_service:  # pragma: no cover
        return False

    perform_change = False
    # The selected municipality is the lead authority.
    if active_service.service_group.name == "municipality":
        if active_service == selected_municipality:
            perform_change = True
    else:
        # Lead authority is not a municipality. The selected municipality is the only involved municipality.
        involved_municipalities = instance.instance_services.filter(
            active=0, service__service_group__name="municipality"
        )
        count_involved_municipalities = involved_municipalities.count()
        if count_involved_municipalities == 1:
            if involved_municipalities.first().service == selected_municipality:
                perform_change = True

        # Lead authority is not a municipality. The selected municipality is one of multiple involved
        # municipalities and the municipality answer corresponds to the selected municipality.
        elif count_involved_municipalities > 1:
            if instance.municipality == selected_municipality:
                perform_change = True

    return perform_change


def change_geometer_task(task):
    """
    Task to change the geometer.

    The geometer service is changed for the given municipality, and all
    dossiers with geometers involved will be migrated over as well.

    This implies removing the old geometer's instance ACLs and granting new
    ACLs to the new geometer as well.
    """
    task.status = "running"
    task.save()

    with transaction.atomic():
        try:
            selected_municipality = task.municipality
            selected_geometer = task.geometer

            ServiceRelation.objects.update_or_create(
                receiver=selected_municipality,
                function="geometer",
                defaults={"provider": selected_geometer},
                create_defaults={
                    "receiver": selected_municipality,
                    "function": "geometer",
                    "provider": selected_geometer,
                },
            )

            instances = instance_models.Instance.objects.filter(
                Exists(
                    InstanceACL.currently_active().filter(
                        instance=OuterRef("pk"),
                        access_level_id="geometer",
                    )
                ),
                services=selected_municipality,
            )

            if not instances:  # pragma: no cover
                log.info(
                    "There are no instances in which the geometer needs to be reassigned"
                )

            instance_count = instances.count()
            reassigned_instance_count = 0
            for n, instance in enumerate(instances.iterator(), start=1):
                if not _should_perform_geometer_change_for_instance(
                    instance, selected_municipality
                ):
                    continue

                log.info(
                    "Geometer reassignement of instance %s started (%s/%s)",
                    instance.pk,
                    n,
                    instance_count,
                )

                attachments = instance.attachments.filter(
                    attachment_sections=be_constants.ATTACHMENT_SECTION_BEILAGEN_SB1_PAPIER
                )

                work_items = instance.case.work_items.filter(
                    status=WorkItem.STATUS_READY,
                    task_id__in=["geometer", "cadastral-survey"],
                )

                if work_items or attachments:
                    geometer_acls = InstanceACL.currently_active().filter(
                        access_level_id="geometer",
                        instance=instance,
                    )
                    attachment_count = 0
                    for instance_acl in geometer_acls:
                        # Reassign all geometer and cadastral-survey workitems from the old geometer to the new one.

                        if work_items:
                            caluma_api.reassign_work_items(
                                instance,
                                from_group_id=instance_acl.service.pk,
                                to_group_id=selected_geometer.pk,
                                user=AnonymousUser(),
                                work_items=work_items,
                            )

                        geometer_attachments = attachments.filter(
                            service=instance_acl.service
                        )

                        if geometer_attachments:
                            attachment_count = (
                                attachment_count + geometer_attachments.count()
                            )
                            for attachment in geometer_attachments:
                                attachment.context["for_geometer"] = True
                                attachment.save()

                    if work_items or attachment_count:
                        log.info(
                            "Reassigned %s work-items and %s attachments for instance %s",
                            work_items.count(),
                            attachment_count,
                            instance.pk,
                        )

                # Revoke active geometer ACLs and add new ACLs for the new geometer
                instance_acl_count = permissions_events.Trigger.geometer_changed(
                    None,
                    instance,
                    selected_geometer,
                )
                log.info(
                    "Revoked %s instance acls for instance %s",
                    instance_acl_count,
                    instance.pk,
                )
                reassigned_instance_count += 1

            log.info(f"{reassigned_instance_count} instances reassigned")
            task.status = "completed"
            task.completed_at = timezone.now()
            task.save()

        except Exception as e:
            task.status = "failed"
            task.errors = str(e)
            task.completed_at = timezone.now()
            task.save()
