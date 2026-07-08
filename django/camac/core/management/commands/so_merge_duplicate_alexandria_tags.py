from alexandria.core.models import Tag
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from tqdm import tqdm


class Command(BaseCommand):
    help = "Merge duplicate Alexandria tags for Solothurn by name and created_by_group"

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        self.merge_duplicate_tags()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
            print("Dry run finished. No changes were saved.")
        else:
            transaction.savepoint_commit(sid)
            print("Duplicate Alexandria tags merged.")

    def merge_duplicate_tags(self):
        print("Starting duplicate Alexandria tag merge")

        duplicate_groups = (
            Tag.objects.exclude(created_by_group__isnull=True)
            .exclude(created_by_group="")
            .values("name", "created_by_group")
            .annotate(count=Count("pk"))
            .filter(count__gt=1)
            .order_by("created_by_group", "name")
        )

        if not duplicate_groups.exists():
            print("No duplicate tags found.")
            return

        total_duplicate_tags = 0
        total_transferred_documents = 0
        total_removed_duplicate_relations = 0

        for group in duplicate_groups:
            name = group["name"]
            created_by_group = group["created_by_group"]

            tags = list(
                Tag.objects.filter(
                    name=name,
                    created_by_group=created_by_group,
                ).order_by("pk")
            )

            tag_to_keep = tags[0]
            duplicate_tags = tags[1:]

            print(f'Merging tag "{name}" for created_by_group "{created_by_group}"')
            print(f"Keeping tag {tag_to_keep.pk}")

            for duplicate_tag in duplicate_tags:
                print(f"  Merging duplicate tag {duplicate_tag.pk}")

                transferred_documents = 0
                removed_duplicate_relations = 0

                documents = list(duplicate_tag.documents.all())

                for document in tqdm(documents):
                    if document.tags.filter(pk=tag_to_keep.pk).exists():
                        removed_duplicate_relations += 1
                    else:
                        document.tags.add(tag_to_keep)
                        transferred_documents += 1

                    document.tags.remove(duplicate_tag)

                assert duplicate_tag.documents.count() == 0

                duplicate_tag.delete()

                total_duplicate_tags += 1
                total_transferred_documents += transferred_documents
                total_removed_duplicate_relations += removed_duplicate_relations

                print(f"    Transferred documents: {transferred_documents}")
                print(
                    "    Removed duplicate document relations: "
                    f"{removed_duplicate_relations}"
                )

        print("Finished duplicate Alexandria tag merge")
        print(f"Duplicate tags merged: {total_duplicate_tags}")
        print(f"Transferred document relations: {total_transferred_documents}")
        print(
            f"Removed duplicate document relations: {total_removed_duplicate_relations}"
        )
