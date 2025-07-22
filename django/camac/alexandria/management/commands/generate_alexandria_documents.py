from alexandria.core.api import create_document_file, create_file
from alexandria.core.models import Category
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.document.tests.data import django_file
from camac.user.models import Service, User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--service",
            dest="service",
            type=int,
            required=True,
        )
        parser.add_argument(
            "--instance",
            dest="instance",
            type=int,
            required=True,
        )
        parser.add_argument(
            "--count",
            dest="count",
            type=int,
            required=True,
        )
        parser.add_argument(
            "--category",
            dest="category",
            type=str,
            default="intern",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        content = django_file("multiple-pages.pdf")
        user = User.objects.first()
        category = Category.objects.get(pk=options["category"])
        service = Service.objects.get(pk=options["service"])

        self.stdout.write(
            f"Creating {options['count']} documents with 4 files each for {service.get_name()}"
        )

        for i in tqdm(range(options["count"])):
            document, _ = create_document_file(
                user=str(user.pk),
                group=str(service.pk),
                category=category,
                document_title=f"Generated document {i + 1}.pdf",
                file_name=f"generated-file-{i + 1}-1.pdf",
                file_content=content,
                mime_type="application/pdf",
                file_size=content.size,
                additional_document_attributes={
                    "metainfo": {"camac-instance-id": options["instance"]}
                },
            )

            for x in range(3):
                create_file(
                    document=document,
                    user=str(user.pk),
                    group=str(service.pk),
                    name=f"generated-file-{i + 1}-{x + 1}.pdf",
                    content=content,
                    mime_type="application/pdf",
                    size=content.size,
                )
