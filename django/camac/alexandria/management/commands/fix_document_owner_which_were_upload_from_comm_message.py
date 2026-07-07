from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.communications.models import CommunicationsAttachment
from camac.instance.models import Instance
from camac.user.models import Service, User


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
    def handle(self, *args, **options):  # noqa C901
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
            instance_string = doc.metainfo.get("camac-instance-id")

            try:
                if instance_string:
                    instance = Instance.objects.filter(pk=instance_string).first()
                    dossier_number = (
                        instance.case.meta.get("dossier-number", "?")
                        if instance
                        else "?"
                    )
                    instance_string = f"{instance_string}:{dossier_number}"
            except Exception:
                pass

            prefix = f"doc={doc.pk}:{doc.title} attachment={comm_attachment.pk} instance={instance_string}"

            sender_entity = message.created_by
            recipient_services = [
                e
                for e in topic.involved_entities
                if e != sender_entity and e != "APPLICANT"
            ]

            if not recipient_services:
                tqdm.write(f"[SKIP/no-recipient]  {prefix}")
                skipped_no_recipient += 1
                continue

            if len(recipient_services) > 1:
                try:
                    recipient_services = [
                        f"{s.pk}:{s.get_name()}"
                        for s in Service.objects.filter(pk__in=recipient_services)
                    ]
                except Exception:
                    pass

                tqdm.write(
                    f"[SKIP/ambiguous]     {prefix} recipients={recipient_services}"
                )
                skipped_ambiguous += 1
                continue

            recipient_service_id = recipient_services[0]

            if doc.created_by_group == recipient_service_id:
                skipped_already_correct += 1
                continue

            old_user = doc.created_by_user
            old_group = doc.created_by_group

            doc.created_by_user = user_id
            doc.created_by_group = recipient_service_id
            doc.save(update_fields=["created_by_user", "created_by_group"])

            file_obj.created_by_user = user_id
            file_obj.created_by_group = recipient_service_id
            file_obj.save(update_fields=["created_by_user", "created_by_group"])

            new_user_string = user_id
            old_user_string = old_user
            new_group_string = recipient_service_id
            old_group_string = old_group
            try:
                new_service = Service.objects.get(pk=recipient_service_id)
                new_group_string = f"{new_service.pk}:{new_service.get_name()}"

                old_service = Service.objects.get(pk=old_group)
                old_group_string = f"{old_service.pk}:{old_service.get_name()}"

                new_user = User.objects.get(pk=user_id)
                new_user_string = f"{new_user.pk}:{new_user.username}"

                old_user_model = User.objects.get(pk=old_user)
                old_user_string = f"{old_user_model.pk}:{old_user_model.username}"
            except Exception:
                pass

            tqdm.write(
                f"[FIXED]              {prefix} "
                f"user: {old_user_string!r} -> {new_user_string!r}  "
                f"group: {old_group_string!r} -> {new_group_string!r}"
            )
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
