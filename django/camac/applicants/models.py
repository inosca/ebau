from django.db import models


class ROLE_CHOICES(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    EDITOR = "EDITOR", "Editor"
    READ_ONLY = "READ_ONLY", "Read only"


class Applicant(models.Model):
    instance = models.ForeignKey(
        "instance.Instance",
        models.CASCADE,
        db_column="INSTANCE_ID",
        # NOTE: The "involved_" prefix is required because the instance views annotate
        # "applicants". And we did not wanted to break backwards compatibility
        related_name="involved_applicants",
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    invitee = models.ForeignKey(
        "user.User",
        models.DO_NOTHING,
        db_column="APPLICANT_USER_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    created = models.DateTimeField(db_column="CREATED", auto_now=True)
    email = models.EmailField(db_collation="case_insensitive")
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES.choices,
        default=ROLE_CHOICES.ADMIN.value,
    )

    class Meta:
        managed = True
        db_table = "APPLICANTS"
        unique_together = (("instance", "invitee"),)
