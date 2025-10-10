from django.db import models
from django.utils.translation import gettext_lazy as _


class AlertMessage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    title = models.CharField(
        max_length=200, blank=True, null=True, verbose_name=_("Title")
    )
    start_date = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Start Date")
    )
    end_date = models.DateTimeField(blank=True, null=True, verbose_name=_("End Date"))
    message = models.TextField()

    class Meta:
        verbose_name = _("Alert Message")
        verbose_name_plural = _("Alert Messages")
        ordering = ["-created_at"]

    def __str__(self):
        if self.title:
            return f"Alert Message ({self.id}) - {self.title}"
        return f"Alert Message ({self.id}) - {self.message[:50]}..."
