from django.db import models


class Tags(models.Model):
    """Legacy model, use Keywords for new apps."""

    name = models.CharField(db_column="NAME", max_length=50)
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, db_column="SERVICE_ID", related_name="+"
    )
    instance = models.ForeignKey(
        "instance.Instance",
        models.CASCADE,
        db_column="INSTANCE_ID",
        related_name="tags",
    )

    class Meta:
        managed = True
        db_table = "TAGS"


class Keyword(models.Model):
    name = models.CharField(max_length=50)
    service = models.ForeignKey("user.Service", models.CASCADE, related_name="+")
    instances = models.ManyToManyField("instance.Instance", related_name="keywords")

    class Meta:
        managed = True
        unique_together = (("name", "service"),)
