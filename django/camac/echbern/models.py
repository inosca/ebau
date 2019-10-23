from uuid import uuid4

from django.db import models


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    body = models.TextField(help_text="XML body")
    created_at = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey("user.service", on_delete=models.PROTECT)

    class Meta:
        managed = True
        ordering = ["created_at"]
