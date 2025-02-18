import uuid

from django.db import models


class SanctionQuerySet(models.QuerySet):
    def for_instance_id(self, instance_id):
        return self.filter(instance_id=instance_id)

    def assigned_to_service_id(self, service_id):
        return self.filter(assigned_service_id=service_id)

    def pending(self):
        return self.filter(controlled_at__isnull=True)

    def for_step(self, control_step):
        return self.filter(control_step=control_step)


class BaseSanction(models.Model):
    CONTROL_STEPS = (
        ("baufreigabe", "Baufreigabe"),
        ("realisierung", "Realisierung"),
        ("endabnahme", "Endabnahme"),
        ("variabel", "Variabel"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_service = models.ForeignKey(
        "user.Service",
        on_delete=models.DO_NOTHING,
        related_name="+",
    )
    created_by_user = models.ForeignKey(
        "user.User",
        on_delete=models.DO_NOTHING,
        related_name="+",
    )
    control_step = models.CharField(choices=CONTROL_STEPS, max_length=20)
    assigned_service = models.ForeignKey(
        "user.Service",
        on_delete=models.DO_NOTHING,
        related_name="+",
    )

    class Meta:
        abstract = True


class Sanction(BaseSanction):
    objects = SanctionQuerySet.as_manager()

    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        related_name="+",
    )
    controlled_by_user = models.ForeignKey(
        "user.User",
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="+",
    )
    controlled_at = models.DateTimeField(null=True)
    control_notes = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    controlled_at__isnull=True,
                    controlled_by_user__isnull=True,
                )
                | models.Q(
                    controlled_at__isnull=False,
                    controlled_by_user__isnull=False,
                ),
                name="controlled_consistently",
            ),
        ]


class SanctionTemplate(BaseSanction):
    pass
