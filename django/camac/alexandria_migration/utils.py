from datetime import timedelta
from functools import lru_cache

from alexandria.core.models import Category, Mark
from django.conf import settings

from camac.document.models import AttachmentSection


@lru_cache
def get_available_categories() -> dict[str, Category]:
    """Get all available alexandria categories as a dict using the slug as key."""

    return {category.pk: category for category in Category.objects.all()}


@lru_cache
def get_available_marks() -> dict[str, Mark]:
    return {mark.pk: mark for mark in Mark.objects.all()}


@lru_cache
def get_fallback_category() -> Category:
    return get_available_categories()[settings.ALEXANDRIA_MIGRATION.fallback_category]


@lru_cache
def get_target_category(
    attachment_section: AttachmentSection,
    bucket: str | None,
) -> Category:
    """Get the correct alexandria category given an attachment section and bucket name."""

    available_categories = get_available_categories()

    category = settings.ALEXANDRIA_MIGRATION.category_mapping.get(attachment_section.pk)
    suffix = settings.ALEXANDRIA_MIGRATION.category_suffix_mapping.get(bucket)

    if not category:
        raise ValueError(
            "Could not find category for attachment section "
            f"{attachment_section.pk} with bucket {bucket}. Please check the "
            "category mapping in the module configuration."
        )

    full_slug = category

    if suffix is not None:
        full_slug += suffix

    if full_slug not in available_categories.keys():
        full_slug = category

    return available_categories[full_slug]


def get_marks_from_context(context: dict[str, bool]) -> list[Mark]:
    """Get the correct marks from a given context dictionary containing legacy marks."""

    available_marks = get_available_marks()

    return [
        available_marks[mark_slug]
        for context_key, mark_slug in settings.ALEXANDRIA_MIGRATION.context_mark_mapping.items()
        if context.get(context_key) is True
    ]


def humanize_timedelta(delta: timedelta) -> str:
    """Format timedelta in a human-readable way.

    E.g.: "1h 16m 30s"
    """

    total_seconds = int(delta.total_seconds())

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts)
