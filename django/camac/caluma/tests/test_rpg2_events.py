import pytest

from camac.caluma.extensions.events.rpg2 import (
    is_rpg2_service_addressed,
    is_rpg2_workflow,
)


def _rpg2_work_items(case):  # pragma: no cover
    return case.work_items.filter(task_id="rpg2")


@pytest.mark.parametrize(
    "workflows,case_workflow,expected",
    [
        (["building-permit"], "building-permit", True),
        (["building-permit"], "internal-dossier", False),
        ([], "building-permit", False),
        (None, "building-permit", False),
    ],
)
def test_is_rpg2_workflow(
    db,
    rpg2_settings,
    caluma_work_item_factory,
    workflows,
    case_workflow,
    expected,
):
    rpg2_settings.workflows = workflows
    work_item = caluma_work_item_factory(case__workflow__slug=case_workflow)
    assert is_rpg2_workflow(work_item) == expected


@pytest.mark.parametrize(
    "service_slugs,addressed_slug,expected",
    [
        (["rpg2-service-slug"], "rpg2-service-slug", True),
        (["rpg2-service-slug"], "other-service-slug", False),
        ([], "rpg2-service-slug", False),
    ],
)
def test_is_rpg2_service_addressed(
    db,
    rpg2_settings,
    service_factory,
    caluma_work_item_factory,
    service_slugs,
    addressed_slug,
    expected,
):
    rpg2_settings.service_slugs = service_slugs
    addressed_service = service_factory(slug=addressed_slug)
    work_item = caluma_work_item_factory(
        addressed_groups=[str(addressed_service.pk)],
    )
    assert is_rpg2_service_addressed(work_item) == expected
