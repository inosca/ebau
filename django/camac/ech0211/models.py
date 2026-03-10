import xml.dom.minidom
from functools import cached_property, reduce
from logging import getLogger
from operator import or_
from uuid import uuid4

from alexandria.core import models as alexandria_models
from django.db import models
from django.db.models import Prefetch, Q, QuerySet
from django.utils import timezone

from camac.document import models as document_models

log = getLogger(__name__)


def tag_value(dom, tag_name):
    try:
        return dom.getElementsByTagNameNS("*", tag_name)[0].firstChild.nodeValue
    except Exception:  # pragma: no cover
        return None


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    body = models.TextField(help_text="XML body")
    created_at = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey("user.Service", on_delete=models.PROTECT)

    @cached_property
    def dom(self):
        return xml.dom.minidom.parseString(self.body)

    def pretty_print(self):  # pragma: no cover
        """
        Pretty print the XML body.

        This is a convenience method for testing / debugging.
        """
        print(self.dom.toprettyxml())

    def get_event_type(self):
        """
        Return the event type of the message.

        This is a convenience method for testing / debugging.
        """
        return tag_value(self.dom, "eventType")

    def get_documents(self):
        """
        Return metadata about the documents that are part of the message.

        This is a convenience method for testing / debugging.
        """
        documents = self.dom.getElementsByTagNameNS("*", "document")
        return [
            {
                "uuid": tag_value(document, "uuid"),
                "title": tag_value(document, "title"),
                "category": tag_value(document, "documentKind"),
            }
            for document in documents
        ]

    class Meta:
        managed = True
        ordering = ["created_at"]


class ECH0211CamacCategory(document_models.AttachmentSection):
    class Meta:
        proxy = True

    class JSONAPIMeta:
        resource_name = "ech0211-document-categories"


class ECH0211AlexandriaCategory(alexandria_models.Category):
    class Meta:
        proxy = True

    class JSONAPIMeta:
        resource_name = "ech0211-document-categories"


class ECH0211AlexandriaDocumentManager(models.Manager):
    def get_queryset(self) -> QuerySet["ECH0211AlexandriaDocument"]:
        """Annotate and prefetch document for downstream convenience.

        Annotate and prefetch the queryset so we have immediate access to
        the most recent file, for example.
        """

        return (
            super()
            .get_queryset()
            .prefetch_related(
                Prefetch(
                    "files",
                    queryset=alexandria_models.File.objects.filter(
                        variant=alexandria_models.File.Variant.ORIGINAL
                    ).order_by("-created_at")[:1],
                    to_attr="_most_recent_file",
                )
            )
        )


class ECH0211DocumentQuerySet(QuerySet["ECH0211Document"]):
    def filter(self, *args, **kwargs):
        if pk := kwargs.pop("pk", None):
            # In case of the detail view, we get a `.filter(pk=...)`
            # call, which we need to intercept for proper handling and improved
            # performance - we don't want to do most filtering on an annotated
            # field.
            cat, doc = pk.split("-")
            new_qs = self.filter(*args, category=cat, attachment=doc, **kwargs)
            return new_qs
        elif pk_in := kwargs.pop("pk__in", None):
            # In the multi-download endpoint, we ave an `ids` filter, which
            # turns into a `pk__in` lookup. We need to decode that here to
            # fetch the correct documents
            q_fragments = [
                Q(category=cat, attachment=doc)
                for cat, doc in [val.split("-") for val in pk_in]
            ]
            q_expr = reduce(or_, q_fragments)
            return self.filter(q_expr)

        return super().filter(*args, **kwargs)


class ECH0211Document(models.Model):
    """Represent a document from the document model in a denormalized way.

    Each ECH0211Document exists in exactly one category, as opposed to the
    old document module's "Attachments". Otherwise, they are equal.
    """

    id = models.CharField(max_length=100, primary_key=True)

    name = models.CharField(db_column="NAME", max_length=255)
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    path = models.FileField(
        db_column="PATH",
        max_length=1024,
        upload_to=document_models.attachment_path_directory_path,
    )
    size = models.IntegerField(db_column="SIZE")
    date = models.DateTimeField(db_column="DATE", default=timezone.now)
    user = models.ForeignKey(
        "user.User",
        db_column="USER_ID",
        related_name="+",
        on_delete=models.DO_NOTHING,
    )
    service = models.ForeignKey(
        "user.Service",
        db_column="SERVICE_ID",
        related_name="+",
        on_delete=models.DO_NOTHING,
    )
    mime_type = models.CharField(db_column="MIME_TYPE", max_length=255)

    category = models.ForeignKey(
        "ECH0211CamacCategory",
        related_name="+",
        on_delete=models.DO_NOTHING,
        db_column="attachmentsection_id",
    )
    attachment = models.ForeignKey(
        "document.Attachment",
        related_name="+",
        on_delete=models.DO_NOTHING,
        db_column="ATTACHMENT_ID",
    )

    @property
    def content(self):
        return self.attachment.path

    @classmethod
    def from_attachment(self, att):
        return self.objects.get(
            category=att.attachment_sections.first(), attachment=att
        )

    objects = ECH0211DocumentQuerySet.as_manager()

    def delete(self, *args, **kwargs):
        self.attachment.delete(*args, **kwargs)

    class Meta:
        managed = False
        db_table = "ech0211_document"

    class JSONAPIMeta:
        resource_name = "ech0211-documents"


class ECH0211AlexandriaDocument(alexandria_models.Document):
    objects = ECH0211AlexandriaDocumentManager()

    @cached_property
    def most_recent_file(self) -> alexandria_models.File | None:
        """Return the most recent (original) file for this document.

        Note: When used with the `ECH0211AlexandriaDocumentQueryset`, this should
        pose no additional query, but for freshly-created documents, it can still
        hit the DB
        """

        most_recent_file = None

        if hasattr(self, "_most_recent_file"):
            # obj.files is prefetched, so we're looping in
            # python to avoid triggering a DB query.
            most_recent_file = next(
                iter(self._most_recent_file),
                # If no file is attached yet, we don't crash but just return None
                None,
            )
        else:
            # Not constructed via annotated queryset: either freshly
            # created or some error, but we can't tell which
            most_recent_file = (
                self.files.order_by("-created_at")
                .filter(variant=alexandria_models.File.Variant.ORIGINAL)
                .first()
            )

        if most_recent_file is None:
            log.error(
                f"Document {self.pk} has no original files attached. This is "
                "likely an issue of data corruption as this should never happen "
                "in the first place."
            )

        return most_recent_file

    class Meta:
        proxy = True

    class JSONAPIMeta:
        resource_name = "ech0211-documents"
