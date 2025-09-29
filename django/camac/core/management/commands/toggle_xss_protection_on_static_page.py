from django.core.management.base import BaseCommand

from camac.core.models import StaticContent


class Command(BaseCommand):
    help = "Toggle the field disable_xss_protection on StaticContent model."

    def add_arguments(self, parser):
        parser.add_argument(
            "--page",
            default=None,
            help="The PK/slug of the StaticContent model on which to toggle the XSS protection.",
            required=True,
        )

    def handle(self, *args, **options):
        content = StaticContent.objects.get(pk=options["page"])
        content.disable_xss_protection = not content.disable_xss_protection
        content.save()
        self.stdout.write(
            f"Set disable_xss_protection of StaticContent(pk={content.pk}) to {content.disable_xss_protection}"
        )
