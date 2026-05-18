from django.core.validators import RegexValidator
from django.db import models
from localized_fields.fields import LocalizedTextField

from camac.models import dynamic_default_value


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


class BaseKeyword(models.Model):
    name = models.CharField(max_length=50)
    service = models.ForeignKey("user.Service", models.CASCADE, related_name="+")

    class Meta:
        abstract = True


class Keyword(BaseKeyword):
    instances = models.ManyToManyField("instance.Instance", related_name="keywords")

    class Meta:
        managed = True
        unique_together = (("name", "service"),)


class StaticKeyword(BaseKeyword):
    is_archived = models.BooleanField(default=False)
    instances = models.ManyToManyField(
        "instance.Instance", blank=True, related_name="static_keywords"
    )

    class Meta:
        managed = True
        unique_together = (("name", "service"),)


@dynamic_default_value(0)
def next_instance_mark_sort():
    last = InstanceMark.objects.order_by("-sort").first()
    return last.sort + 1 if last else 0


class InstanceMark(models.Model):
    hex_color_validator = RegexValidator(
        regex=r"^#(?:[0-9a-fA-F]{3}){1,2}$",
        message="Enter a valid hex color (e.g. #RRGGBB)",
    )

    name = LocalizedTextField(max_length=50)
    icon = models.CharField(max_length=50)
    background_color = models.CharField(max_length=7, validators=[hex_color_validator])
    text_color = models.CharField(
        max_length=7,
        validators=[hex_color_validator],
        default="#000000",
    )
    sort = models.PositiveIntegerField(default=next_instance_mark_sort)

    class Meta:
        ordering = ["sort"]
