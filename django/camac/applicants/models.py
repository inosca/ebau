from django.db import models
from django.db.models import EmailField


def email_prep(self, value=None):
    """Lower-cases the value returned by super."""
    prep_value = super(EmailField, self).get_prep_value(value)
    if prep_value is not None:
        return prep_value.lower()
    return prep_value


# make EmailField case-insensitive
# see: https://code.djangoproject.com/ticket/17561#comment:7
EmailField.get_prep_value = email_prep


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
    email = EmailField()

    class Meta:
        managed = True
        db_table = "APPLICANTS"
        unique_together = (("instance", "invitee"),)
