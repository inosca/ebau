from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.communications.models import CommunicationsAttachment
from camac.user.models import User


class Command(BaseCommand):
    """
    Fix communications attachemnts uploaded to alexandria.

    Fix created_by_user/created_by_group on alexandria documents converted from
    communication attachments. They were previously set to the sender of the
    communication message.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        qs = (
            CommunicationsAttachment.objects.filter(
                alexandria_file__isnull=False,
                alexandria_file__document__metainfo__has_key="copied-from-communications-attachment",
            )
            .select_related(
                "message__topic",
                "message__created_by_user",
                "alexandria_file__document",
            )
            .iterator()
        )

        system_username = settings.APPLICATION.get("SYSTEM_USER")
        if not system_username:
            self.stdout.write(self.style.ERROR("SYSTEM_USER is not configured."))
            return
        users = User.objects.filter(username=system_username)
        if not users.count():
            self.stdout.write(
                self.style.ERROR("SYSTEM_USER was not found in User table.")
            )
            return
        [system_user] = users
        user_id = system_user.pk

        fixed = 0
        skipped_already_correct = 0
        skipped_no_recipient = 0
        skipped_ambiguous = 0

        for comm_attachment in tqdm(qs, desc="Checking communication attachments"):
            message = comm_attachment.message
            topic = message.topic
            file_obj = comm_attachment.alexandria_file
            doc = file_obj.document
            instance_id = doc.metainfo.get("camac-instance-id", "?")

            sender_entity = message.created_by
            recipient_services = [
                e
                for e in topic.involved_entities
                if e != sender_entity and e != "APPLICANT"
            ]

            if not recipient_services:
                self.stderr.write(
                    f"  Document {doc.pk} (attachment {comm_attachment.pk}, "
                    f"instance {instance_id}): no service recipient in topic, skipping"
                )
                skipped_no_recipient += 1
                continue

            if len(recipient_services) > 1:
                self.stderr.write(
                    f"  Document {doc.pk} (attachment {comm_attachment.pk}, "
                    f"instance {instance_id}): ambiguous recipients {recipient_services}, skipping"
                )
                skipped_ambiguous += 1
                continue

            recipient_service_id = recipient_services[0]

            if doc.created_by_group == recipient_service_id:
                skipped_already_correct += 1
                continue

            doc.created_by_user = user_id
            doc.created_by_group = recipient_service_id
            doc.save(update_fields=["created_by_user", "created_by_group"])

            file_obj.created_by_user = user_id
            file_obj.created_by_group = recipient_service_id
            file_obj.save(update_fields=["created_by_user", "created_by_group"])

            fixed += 1

        self.stdout.write(self.style.SUCCESS(f"Fixed {fixed} document(s)."))
        self.stdout.write(f"  Already correct: {skipped_already_correct}")
        if skipped_no_recipient:
            self.stdout.write(
                f"  Skipped (no service recipient): {skipped_no_recipient}"
            )
        if skipped_ambiguous:
            self.stdout.write(f"  Skipped (ambiguous recipients): {skipped_ambiguous}")

        if options["commit"]:
            transaction.savepoint_commit(sid)
        else:
            self.stdout.write(
                self.style.WARNING("Dry run, use --commit to write changes.")
            )
            transaction.savepoint_rollback(sid)
