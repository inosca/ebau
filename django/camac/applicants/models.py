from django.db import models


class Applicant(models.Model):
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    invitee = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="APPLICANT_USER_ID", related_name="+"
    )
    created = models.DateTimeField(db_column="CREATED")

    class Meta:
        managed = True
        db_table = "APPLICANTS"
        unique_together = (("instance", "invitee"),)
