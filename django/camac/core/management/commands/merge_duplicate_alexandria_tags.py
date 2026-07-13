from alexandria.core.models import Document, Tag
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from tqdm import tqdm


class Command(BaseCommand):
    help = "Merge duplicate Alexandria tags by name and created_by_group"

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        self.merge_duplicate_tags()

        if options["commit"]:
            transaction.savepoint_commit(sid)
            tqdm.write("Duplicate Alexandria tags merged.")
        else:
            transaction.savepoint_rollback(sid)
            tqdm.write(
                "Dry run finished. No changes were saved. Use --commit to apply changes."
            )

    def merge_duplicate_tags(self):
        tqdm.write("Starting duplicate Alexandria tag merge")

        duplicate_tag_groups = (
            Tag.objects.values("name", "created_by_group")
            .annotate(count=Count("pk"))
            .filter(count__gt=1)
            .order_by("created_by_group", "name")
        )

        if not duplicate_tag_groups.exists():
            tqdm.write("No duplicate tags found.")
            return

        total_duplicate_tags = 0
        total_transferred_documents = 0
        total_documents_already_linked = 0

        for duplicate_tag_group in tqdm(
            duplicate_tag_groups, desc="Duplicate tag groups"
        ):
            name = duplicate_tag_group["name"]
            created_by_group = duplicate_tag_group["created_by_group"]

            tags = Tag.objects.filter(
                name=name,
                created_by_group=created_by_group,
            )

            tag_to_keep = tags[0]
            duplicate_tags = tags.exclude(pk=tag_to_keep.pk)

            tqdm.write(
                f'Merging tag "{name}" for created_by_group "{created_by_group}"'
            )
            tqdm.write(f"Keeping tag {tag_to_keep.pk}")

            affected_documents = Document.objects.filter(
                tags__in=duplicate_tags
            ).distinct()

            transferred_documents = 0
            documents_already_linked = 0

            for document in tqdm(
                affected_documents,
                desc=f"{name} documents",
                leave=False,
            ):
                already_has_tag_to_keep = document.tags.filter(
                    pk=tag_to_keep.pk
                ).exists()

                document.tags.remove(*duplicate_tags)

                if already_has_tag_to_keep:
                    documents_already_linked += 1
                else:
                    document.tags.add(tag_to_keep)
                    transferred_documents += 1

            assert not (
                duplicate_tags.annotate(
                    document_count=Count("documents", distinct=True)
                )
                .filter(document_count__gt=0)
                .exists()
            )

            total_duplicate_tags += duplicate_tags.count()
            duplicate_tags.delete()
            total_transferred_documents += transferred_documents
            total_documents_already_linked += documents_already_linked

            tqdm.write(f"  Duplicate tags merged: {len(duplicate_tags)}")
            tqdm.write(f"  Transferred documents: {transferred_documents}")
            tqdm.write(f"  Documents already linked: {documents_already_linked}")

        tqdm.write("Finished duplicate Alexandria tag merge")
        tqdm.write(f"Duplicate tags merged: {total_duplicate_tags}")
        tqdm.write(f"Transferred document relations: {total_transferred_documents}")
        tqdm.write(f"Documents already linked: {total_documents_already_linked}")
