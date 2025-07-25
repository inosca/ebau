from logging import getLogger

from django.db.models import OuterRef
from django.utils.timezone import now

from .models import AGGISExport, InstanceProxyAG

log = getLogger(__name__)


def export_agis():
    exported = set(AGGISExport.objects.values_list("instance_id", flat=True))
    instances = set(InstanceProxyAG.objects.values_list("instance_id", flat=True))

    to_create = instances - exported
    to_remove = exported - instances
    to_update = exported - to_remove

    # Remove any exported instances, that no longer exist.
    # Usually shouldn't be necessary since the AGGISExport model should be
    # deleted if the corresponding instance is deleted. Only valid use-case if,
    # if the AfB had a read permission that was revoked afterwards.
    try:
        deleted = AGGISExport.objects.filter(pk__in=to_remove).delete()
        log.info(f"Removed export entries for {deleted[0]} instance(s).")
    except Exception as e:  # pragma: no cover
        log.warning(f"Failed to delete export entries for instances {to_remove}")
        log.warning(e)

    updated = 0
    export_instances_to_create = []

    instance_proxies = InstanceProxyAG.objects.annotate(
        exported_hash=AGGISExport.objects.filter(pk=OuterRef("pk")).values("hash")[:1]
    )
    for instance in instance_proxies.iterator(chunk_size=1000):
        try:
            if instance.pk in to_create:
                export_instances_to_create.append(
                    AGGISExport(
                        **instance.fields_to_dict(),
                        hash=instance.hash(),
                    )
                )

                continue

            instance_hash = instance.hash()
            exported_hash = instance.exported_hash
            if instance_hash != exported_hash:
                AGGISExport.objects.filter(pk=instance.pk).update(
                    **instance.fields_to_dict(), hash=instance_hash, modified_at=now()
                )
                updated += 1

        except Exception as e:  # pragma: no cover
            if instance.pk in to_create:
                log.warning(f"Failed to create export entry for instance {instance.pk}")
            elif instance.pk in to_update:
                log.warning(
                    f"Failed to diff or update export entry for instance {instance.pk}"
                )
            log.warning(e)
        finally:
            continue

    log.info(f"Updated export entries for {updated} instances(s).")

    try:
        created = AGGISExport.objects.bulk_create(export_instances_to_create)
        log.info(f"Created export entries for {len(created)} instance(s).")
    except Exception as e:  # pragma: no cover
        log.warning(f"Failed to create export entries for instances {to_create}")
        log.warning(e)
