from django.contrib.postgres.fields import DateTimeRangeField
from django.core.validators import MaxValueValidator
from django.db import models


class ObjectionTimeframe(models.Model):
    instance = models.OneToOneField(
        "instance.Instance", models.CASCADE, related_name="objection_timeframes"
    )
    timeframe = DateTimeRangeField(null=True)


class Objection(models.Model):
    instance = models.ForeignKey(
        "instance.Instance", models.CASCADE, related_name="objections"
    )
    creation_date = models.DateField()


class ObjectionParticipant(models.Model):
    objection = models.ForeignKey(
        Objection, models.CASCADE, related_name="objection_participants"
    )
    company = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    representative = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(1)]
    )
