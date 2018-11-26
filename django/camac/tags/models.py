from django.db import models


class Tags(models.Model):
    name = models.CharField(db_column="NAME", max_length=50)
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, db_column="SERVICE_ID", related_name="+"
    )
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="tags",
    )

    class Meta:
        managed = True
        db_table = "TAGS"
