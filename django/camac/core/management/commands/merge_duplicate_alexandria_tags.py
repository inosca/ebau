from collections.abc import Iterator
from typing import Any

from alexandria.core.models import Document, Tag
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db import transaction
from django.db.models import CharField, Count, Exists, OuterRef, QuerySet, Subquery
from django.db.models.functions import Cast, Coalesce
from tqdm import tqdm

from camac.user.models import Service

MUNICIPALITY = "municipality"


class Command(BaseCommand):
    help = "Merge Alexandria tags with the same name that are visible to the same users"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:
        if settings.APPLICATION_NAME != "kt_so":
            raise CommandError("Only for Kt SO")

        sid = transaction.savepoint()

        # Tags are only merged when everybody who sees one of them also sees the
        # one that is kept, which leaves two cases:

        # - One of the duplicates was created by a municipality: municipality
        #   tags are visible to everybody, so all tags of that name are merged
        #   into the oldest municipality tag.
        # - None of them was: a tag is only visible in its own service family, so
        #   the oldest tag of every family remains.

        self.merge_duplicate_tags()

        if options["commit"]:
            transaction.savepoint_commit(sid)
            tqdm.write("Duplicate Alexandria tags merged.")
        else:
            transaction.savepoint_rollback(sid)
            tqdm.write(
                "Dry run finished. No changes were saved. Use --commit to apply changes."
            )

    def get_annotated_tags(self) -> QuerySet[Tag]:
        service = (
            Service.objects.order_by()
            .annotate(
                group=Cast("pk", CharField()),
                family=Coalesce(
                    Cast("service_parent_id", CharField()), Cast("pk", CharField())
                ),
            )
            .filter(group=OuterRef("created_by_group"))
        )

        return Tag.objects.annotate(
            family=Subquery(service.values("family")[:1]),
            is_municipality=Exists(service.filter(service_group__name=MUNICIPALITY)),
        )

    def get_merge_groups(self) -> Iterator[tuple[Tag, QuerySet[Tag]]]:
        tags = self.get_annotated_tags()

        duplicates = tags.filter(
            name__in=tags.values("name")
            .annotate(count=Count("pk"))
            .filter(count__gt=1)
            .values("name")
        )
        municipality_names = duplicates.filter(is_municipality=True).values("name")

        for duplicate in municipality_names.distinct():
            same_name = tags.filter(name=duplicate["name"])

            yield (
                same_name.filter(is_municipality=True).earliest("created_at"),
                same_name,
            )

        duplicate_families = (
            duplicates.exclude(name__in=municipality_names)
            .values("name", "family")
            .annotate(count=Count("pk"))
            .filter(count__gt=1)
        )

        for duplicate in duplicate_families:
            same_family = tags.filter(
                name=duplicate["name"], family=duplicate["family"]
            )

            yield same_family.earliest("created_at"), same_family

    def merge_duplicate_tags(self) -> None:
        tqdm.write("Starting duplicate Alexandria tag merge")

        merge_groups = list(self.get_merge_groups())

        if not merge_groups:
            tqdm.write("No duplicate tags found.")
            return

        total_duplicate_tags = 0
        total_transferred_documents = 0
        total_documents_already_linked = 0

        for tag_to_keep, tags in tqdm(merge_groups, desc="Duplicate tags"):
            merged_tags, transferred, already_linked = self.merge_tags(
                tag_to_keep, tags
            )

            total_duplicate_tags += merged_tags
            total_transferred_documents += transferred
            total_documents_already_linked += already_linked

        tqdm.write("Finished duplicate Alexandria tag merge")
        tqdm.write(f"Duplicate tags merged: {total_duplicate_tags}")
        tqdm.write(f"Transferred document relations: {total_transferred_documents}")
        tqdm.write(f"Documents already linked: {total_documents_already_linked}")

    def merge_tags(self, tag_to_keep: Tag, tags: QuerySet[Tag]) -> tuple[int, int, int]:
        duplicate_tags = tags.exclude(pk=tag_to_keep.pk)
        duplicate_pks = list(duplicate_tags.values_list("pk", flat=True))
        duplicate_groups = list(
            duplicate_tags.values_list("created_by_group", flat=True)
        )

        tqdm.write(
            f'Merging tag "{tag_to_keep.name}" of groups {duplicate_groups} '
            f'into group "{tag_to_keep.created_by_group}"'
        )

        transferred_documents = 0
        documents_already_linked = 0

        for document in tqdm(
            Document.objects.filter(tags__in=duplicate_pks).distinct(),
            desc=f"{tag_to_keep.name} documents",
            leave=False,
        ):
            already_has_tag_to_keep = document.tags.filter(pk=tag_to_keep.pk).exists()

            document.tags.remove(*duplicate_pks)

            if already_has_tag_to_keep:
                documents_already_linked += 1
            else:
                document.tags.add(tag_to_keep)
                transferred_documents += 1

        Tag.objects.filter(pk__in=duplicate_pks).delete()

        tqdm.write(f"  Duplicate tags merged: {len(duplicate_pks)}")
        tqdm.write(f"  Transferred documents: {transferred_documents}")
        tqdm.write(f"  Documents already linked: {documents_already_linked}")

        return len(duplicate_pks), transferred_documents, documents_already_linked
