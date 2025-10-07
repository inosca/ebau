from django.db import models
from django.utils.translation import gettext_lazy as _


class AlertMessage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    message = models.TextField()

    class Meta:
        verbose_name = _("Alert Message")
        verbose_name_plural = _("Alert Messages")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Alert Message ({self.id}) - {self.message[:50]}..."
