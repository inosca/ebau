from django.core.management.base import BaseCommand

from camac.ech0211.models import Message


class Command(BaseCommand):
    help = """Debug-print all eCH messages of a specific dossier.

    Example:
    $ ./manage.py debug_ech_messages --instance 1 --documents
    Message #0 (ID 88905794-989f-4724-a23f-5a3337aacf2d): status notification (2026-03-04 08:06:22.926644+00:00)
    (no documents)
    Message #1 (ID 12f06ec0-2962-4d16-a07a-a998e0810025): accompanying report (2026-03-04 08:30:39.656797+00:00)
    Documents:
    - 94439a70-e177-4caa-a373-f80b976b22c5: pdf-test.pdf (Beteiligte Behörden)"""

    def add_arguments(self, parser):
        parser.add_argument(
            "--instance",
            type=int,
            help="Instance ID",
            required=True,
        )
        parser.add_argument(
            "--documents",
            action="store_true",
            default=False,
            help="print contained documents",
        )
        parser.add_argument(
            "--body",
            action="store_true",
            default=False,
            help="print full XML message body",
        )

    def handle(self, *args, **options):
        instance_id = options["instance"]
        body = options["body"]
        documents = options["documents"]

        messages = Message.objects.filter(
            body__contains=f"dossierIdentification>{instance_id}</"
        )
        for index, message in enumerate(messages):
            print(
                f"Message #{index} (ID {message.pk}): {message.get_event_type()} ({message.created_at})"
            )
            if documents:
                docs = message.get_documents()
                if docs:
                    print("Documents:")
                    for d in docs:
                        print(f"- {d['uuid']}: {d['title']} ({d['category']})")
                else:
                    print("(no documents)")

            if body:
                message.pretty_print()
