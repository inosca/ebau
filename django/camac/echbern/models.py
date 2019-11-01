from uuid import uuid4

from django.db import models
from lxml import etree


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    body = models.TextField(help_text="XML body")
    created_at = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey("user.service", on_delete=models.PROTECT)

    def pretty_print(self):  # pragma: no cover
        """
        Pretty print the XML body.

        This is a convenience method for testing.
        """
        root = etree.fromstring(self.body)
        print(etree.tostring(root, pretty_print=True).decode())

    class Meta:
        managed = True
        ordering = ["created_at"]
