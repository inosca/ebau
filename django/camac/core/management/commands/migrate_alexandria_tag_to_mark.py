from alexandria.core.models import Mark, Tag
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm


class Command(BaseCommand):
    help = """Migrate alexandria tag to mark"""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        self.migrate()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def migrate(self):
        print("Starting migration alexandria tag to mark")
        tags = Tag.objects.filter(pk__in=settings.ALEXANDRIA["MARKS"]["ALL"])

        for tag in tags:
            print(f"Migrate tag {tag.slug} to mark")
            changed_documents = []
            mark = Mark.objects.get(slug=tag.slug)

            for document in tqdm(tag.documents.all()):
                document.marks.add(mark)
                document.tags.remove(tag)
                document.save()
                changed_documents.append(document)

            assert tag.documents.count() == 0
            tag.delete()

            print(f"Amount of affected documents: {len(changed_documents)}")

        print("Finished migration")
