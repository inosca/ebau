from functools import lru_cache

from alexandria.core.models import Category
from django.conf import settings

from camac.document.models import AttachmentSection


@lru_cache
def get_available_categories() -> dict[str, Category]:
    """Get all available alexandria categories as a dict using the slug as key."""

    return {category.pk: category for category in Category.objects.all()}


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
            "Could not find category for attachment section"
            f"{attachment_section.pk} with bucket {bucket}. Please check the"
            "category mapping in the module configuration."
        )

    full_slug = category

    if suffix is not None:
        full_slug += suffix

    if full_slug not in available_categories.keys():
        full_slug = category

    return available_categories[full_slug]
