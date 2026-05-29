from logging import getLogger

from django.db import transaction
from django.db.models import CharField, F, OuterRef
from django.db.models.functions import MD5, Cast, JSONObject
from django.utils.timezone import now

from .models import AGGISExport, InstanceProxyAG, InstanceProxySO, SOGISExport

log = getLogger(__name__)


@transaction.atomic
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

    log.info(f"Updated export entries for {updated} instances(s).")

    try:
        created = AGGISExport.objects.bulk_create(export_instances_to_create)
        log.info(f"Created export entries for {len(created)} instance(s).")
    except Exception as e:  # pragma: no cover
        log.warning(f"Failed to create export entries for instances {to_create}")
        log.warning(e)


@transaction.atomic
def export_so() -> list[SOGISExport]:
    """Create a SOGISExport model for all new Instances and update existing models for changed Instances."""

    # Hash all fields as JSONObject for comparing changed values
    hashed = InstanceProxySO.objects.annotate(
        last_exported_hash=SOGISExport.objects.filter(
            instance_id=OuterRef("pk")
        ).values("hash")[:1],
        hash=MD5(
            Cast(
                JSONObject(**{name: F(name) for name in InstanceProxySO.fields}),
                output_field=CharField(),
            )
        ),
    )

    new = hashed.filter(last_exported_hash__isnull=True).iterator(chunk_size=1000)

    # For new Instances, last_exported_hash will be null.
    created = SOGISExport.objects.bulk_create(
        [
            SOGISExport(**instance.fields_to_dict(), hash=instance.hash)
            for instance in new
        ],
        batch_size=500,
    )

    # Compare the hash in Python: `.exclude(hash=F("last_exported_hash"))` would inline the whole
    # MD5(JSONObject(...)) into the WHERE. So we first fetch only pk + the two hashes (each subquery
    # runs once, inside the hash instead of twice for a full select) and diff in Python, then select
    # the full field columns only for the rows we actually update.
    existing = (
        hashed.filter(last_exported_hash__isnull=False)
        .values("pk", "hash", "last_exported_hash")
        .iterator(chunk_size=2000)
    )
    ids_to_update = [
        row["pk"] for row in existing if row["hash"] != row["last_exported_hash"]
    ]

    updated_at = now()
    updated = [
        SOGISExport(
            **instance.fields_to_dict(),
            hash=instance.hash,
            modified_at=updated_at,
        )
        for instance in hashed.filter(pk__in=ids_to_update).iterator(chunk_size=1000)
    ]

    SOGISExport.objects.bulk_update(
        updated,
        [
            *InstanceProxySO.fields_for_update,
            "hash",
            "modified_at",
        ],
        batch_size=500,
    )

    log.info(f"Updated export entries for {len(updated)} instance(s).")
    log.info(f"Created export entries for {len(created)} instance(s).")

    return [*created, *updated]
