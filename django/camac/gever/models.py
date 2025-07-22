from django.db import models


class CMIObjectType(models.TextChoices):
    GESCHAEFT = "Geschaeft"
    AUFGABE = "Aufgabe"
    BETEILIGUNG = "Beteiligung"


class CMIField(models.TextChoices):
    VERFAHRENSSTAND = "Verfahrensstand"
    HERKUNFT = "Herkunft"


class CMIObjectTemplate(models.Model):
    slug = models.SlugField(primary_key=True)
    use_for = models.CharField(choices=CMIObjectType.choices, max_length=100)
    template_path = models.CharField(max_length=250)

    class Meta:
        ordering = ("use_for", "slug")


class CMIConstantValue(models.Model):
    slug = models.SlugField(primary_key=True)
    use_for = models.CharField(choices=CMIField.choices, max_length=100)
    label = models.CharField(max_length=250)

    class Meta:
        ordering = ("use_for", "slug")
