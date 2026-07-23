import time
from collections import OrderedDict
from contextlib import nullcontext as no_exception
from datetime import timedelta

import pytest

from camac.alexandria_migration.utils import (
    get_available_categories,
    get_target_category,
    humanize_timedelta,
    timeout,
)


@pytest.mark.django_db
def test_get_target_category(
    alexandria_category_factory,
    alexandria_migration_settings,
    attachment_section_factory,
    clear_category_cache,
    django_assert_num_queries,
):
    section1 = attachment_section_factory()
    section2 = attachment_section_factory()

    category = alexandria_category_factory(slug="category")
    subcategory = alexandria_category_factory(
        slug="category-subcategory", parent=category
    )

    alexandria_migration_settings.category_mapping = {section1.pk: "category"}
    alexandria_migration_settings.category_suffix_mapping = {"foo": "-subcategory"}

    with django_assert_num_queries(1):
        assert get_target_category(section1, "foo") == subcategory
        assert get_target_category(section1, "bar") == category
        assert get_target_category(section1, None) == category

        with pytest.raises(
            ValueError, match="Could not find category for attachment section"
        ):
            get_target_category(section2, None)


@pytest.mark.parametrize("canton", ["be"])
def test_category_mapping(canton, request, snapshot):
    request.getfixturevalue(f"{canton}_alexandria_migration_settings")
    sections, buckets = request.getfixturevalue(f"{canton}_category_setup")

    if canton == "be":
        request.getfixturevalue("multilang")

    data = OrderedDict()

    get_available_categories.cache_clear()
    for section in sections:
        section_key = section.get_name()
        data[section_key] = OrderedDict()

        for bucket in buckets + [None]:
            data[section_key][bucket] = get_target_category(section, bucket).pk

    assert data == snapshot


@pytest.mark.parametrize(
    ("delta", "expect_results"),
    [
        (timedelta(seconds=3600), "1h"),
        (timedelta(hours=2, minutes=5), "2h 5m"),
        (timedelta(hours=2, minutes=5, seconds=30), "2h 5m 30s"),
    ],
)
def test_humanize_timedelta(delta, expect_results):
    assert humanize_timedelta(delta) == expect_results


@pytest.mark.freeze_time("2024-04-15", tick=True)
@pytest.mark.parametrize(
    ("test_fn", "expectation"),
    [
        (lambda: time.sleep(2), pytest.raises(TimeoutError)),
        (lambda: 3, no_exception()),
    ],
)
def test_timeout_context_manager(test_fn, expectation):

    with expectation, timeout(1):
        test_fn()
