import pytest
from alexandria.core.factories import DocumentFactory, TagFactory
from alexandria.core.models import Tag
from django.core.management import call_command
from django.core.management.base import CommandError

pytestmark = pytest.mark.django_db


def create_tag(name, service):
    return TagFactory(
        name=name,
        created_by_group=str(service.pk),
        modified_by_group=str(service.pk),
    )


def test_merge_duplicate_alexandria_tags(set_application_so, service_factory):
    service = service_factory()
    other_service = service_factory()

    tag = create_tag("AfU", service)
    duplicate_tag = create_tag("AfU", service)
    other_service_tag = create_tag("AfU", other_service)

    document_with_duplicate = DocumentFactory()
    document_with_both_tags = DocumentFactory()

    document_with_duplicate.tags.add(duplicate_tag)
    document_with_both_tags.tags.add(tag, duplicate_tag)

    call_command("merge_duplicate_alexandria_tags", commit=True)

    assert set(Tag.objects.filter(name="AfU")) == {tag, other_service_tag}

    assert set(document_with_duplicate.tags.all()) == {tag}
    assert set(document_with_both_tags.tags.all()) == {tag}


def test_merge_duplicate_alexandria_tags_dry_run(set_application_so, service_factory):
    service = service_factory()

    tag = create_tag("Dry Run Tag", service)
    duplicate_tag = create_tag("Dry Run Tag", service)

    document = DocumentFactory()
    document.tags.add(duplicate_tag)

    call_command("merge_duplicate_alexandria_tags")

    assert set(Tag.objects.filter(name="Dry Run Tag")) == {tag, duplicate_tag}
    assert set(document.tags.all()) == {duplicate_tag}


def test_merge_duplicate_alexandria_tags_without_duplicates(
    set_application_so, service_factory
):
    tag = create_tag("Unique Tag", service_factory())

    call_command("merge_duplicate_alexandria_tags")

    assert set(Tag.objects.filter(name="Unique Tag")) == {tag}


def test_merge_duplicate_alexandria_tags_keeps_municipality_tag(
    set_application_so, service_factory, service_group_factory
):
    municipality_service = service_factory(
        service_group=service_group_factory(name="municipality")
    )
    other_service = service_factory()

    municipality_tag = create_tag("AfU", municipality_service)
    other_service_tag = create_tag("AfU", other_service)

    document = DocumentFactory()
    document.tags.add(other_service_tag)

    call_command("merge_duplicate_alexandria_tags", commit=True)

    assert set(Tag.objects.filter(name="AfU")) == {municipality_tag}
    assert set(document.tags.all()) == {municipality_tag}


def test_merge_duplicate_alexandria_tags_by_service_family(
    set_application_so, service_factory
):
    parent_service = service_factory()
    child_service = service_factory(service_parent=parent_service)
    sibling_service = service_factory(service_parent=parent_service)
    unrelated_service = service_factory()

    parent_tag = create_tag("AfU", parent_service)
    child_tag = create_tag("AfU", child_service)
    sibling_tag = create_tag("AfU", sibling_service)
    unrelated_tag = create_tag("AfU", unrelated_service)

    document = DocumentFactory()
    document.tags.add(child_tag, sibling_tag, unrelated_tag)

    call_command("merge_duplicate_alexandria_tags", commit=True)

    assert set(Tag.objects.filter(name="AfU")) == {parent_tag, unrelated_tag}
    assert set(document.tags.all()) == {parent_tag, unrelated_tag}


def test_merge_duplicate_alexandria_tags_of_all_services(
    set_application_so, service_factory, service_group_factory
):
    municipality = service_group_factory(name="municipality")
    cantonal = service_group_factory(name="service-cantonal")

    solothurn = service_factory(name="Gemeinde Solothurn", service_group=municipality)
    messen = service_factory(name="Gemeinde Messen", service_group=municipality)
    afu = service_factory(name="Amt für Umwelt", service_group=cantonal)
    jagd_und_fischerei = service_factory(
        name="Amt Für Umwelt, Jagd und Fischerei", service_group=cantonal
    )
    anlagesicherheit = service_factory(
        name="AS; Anlagesicherheit (Amt für Umwelt(AfU))",
        service_group=cantonal,
        service_parent=afu,
    )
    arp = service_factory(name="Amt für Raumplanung (ARP)", service_group=cantonal)
    arp_sub_service = service_factory(
        name="ARP Kreisplanung", service_group=cantonal, service_parent=arp
    )

    cantonal_services = [
        afu,
        jagd_und_fischerei,
        anlagesicherheit,
        arp,
        arp_sub_service,
    ]

    solothurn_tag = create_tag("AfU", solothurn)
    for service in [messen, *cantonal_services]:
        create_tag("AfU", service)

    afu_groups_tag = create_tag("Groups", afu)
    jagd_und_fischerei_groups_tag = create_tag("Groups", jagd_und_fischerei)
    arp_groups_tag = create_tag("Groups", arp)
    for service in [anlagesicherheit, arp_sub_service]:
        create_tag("Groups", service)

    all_tags = set(Tag.objects.all())
    call_command("merge_duplicate_alexandria_tags")

    assert set(Tag.objects.all()) == all_tags
    call_command("merge_duplicate_alexandria_tags", commit=True)

    # A municipality tag is visible to everybody, so it replaces all others.
    assert set(Tag.objects.filter(name="AfU")) == {solothurn_tag}

    # Without a municipality tag, one tag per service family remains.
    assert set(Tag.objects.filter(name="Groups")) == {
        afu_groups_tag,
        jagd_und_fischerei_groups_tag,
        arp_groups_tag,
    }


def test_merge_duplicate_alexandria_tags_wrong_application(set_application_be):
    with pytest.raises(CommandError, match="Only for Kt SO"):
        call_command("merge_duplicate_alexandria_tags", commit=True)
