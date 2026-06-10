import pytest
from caluma.caluma_form.models import Document
from caluma.caluma_workflow.models import WorkItem

from camac.caluma.extensions.events.rpg2 import (
    is_rpg2_relevant_form,
    is_rpg2_service_addressed,
)
from camac.user.models import Service
from camac.utils import get_unversioned_slug


def _rpg2_work_items(case):
    return case.work_items.filter(task_id="rpg2")


@pytest.fixture
def be_rpg2_services(db, service_factory):
    return (
        service_factory(slug="agr-bauen"),
        service_factory(slug="agr-kantonsplanung"),
    )


@pytest.fixture
def ag_rpg2_service():
    return Service.objects.get(slug="afb")


@pytest.mark.parametrize(
    "allowed_forms,case_form,expected",
    [
        (["baugesuch"], "baugesuch", True),
        (["baugesuch"], "reklame", False),
        (["baugesuch"], "baugesuch-v6", True),
        ([], "baugesuch", False),
    ],
)
def test_is_rpg2_relevant_form(
    db,
    rpg2_settings,
    caluma_work_item_factory,
    allowed_forms,
    case_form,
    expected,
):
    rpg2_settings.allowed_forms = allowed_forms
    work_item = caluma_work_item_factory(case__document__form__slug=case_form)
    assert is_rpg2_relevant_form(work_item) == expected


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


def test_created_on_inquiry_send_be(
    db,
    be_rpg2_settings,
    be_rpg2_services,
    distribution_case_be,
    inquiry_factory_be,
    disable_ech0211_settings,
):
    # add the distribution_case's document form slug to the allowed_forms list
    be_rpg2_settings.allowed_forms.append(
        get_unversioned_slug(distribution_case_be.document.form_id)
    )
    agr_bauen, agr_kantonsplanung = be_rpg2_services
    inquiry_factory_be(to_service=agr_bauen, sent=True)
    work_items = _rpg2_work_items(case=distribution_case_be)
    assert work_items.count() == 1
    work_item = work_items.get()
    assert work_item.status == WorkItem.STATUS_READY
    assert set(work_item.addressed_groups) == {
        str(agr_bauen.pk),
        str(agr_kantonsplanung.pk),
    }
    assert work_item.document
    assert work_item.document.form_id == "rpg2"


def test_not_created_for_other_services_be(
    db,
    be_rpg2_settings,
    inquiry_factory_be,
    disable_ech0211_settings,
    service_factory,
    distribution_case_be,
):
    # add the distribution_case's document form slug to the allowed_forms list
    be_rpg2_settings.allowed_forms.append(
        get_unversioned_slug(distribution_case_be.document.form_id)
    )
    inquiry_factory_be(
        to_service=service_factory(slug="some-other-fachstelle"), sent=True
    )
    assert _rpg2_work_items(distribution_case_be).count() == 0


def test_not_created_for_drafted_inquiry_be(
    db,
    be_rpg2_settings,
    distribution_case_be,
    inquiry_factory_be,
    disable_ech0211_settings,
    be_rpg2_services,
):
    # add the distribution_case's document form slug to the allowed_forms list
    be_rpg2_settings.allowed_forms.append(
        get_unversioned_slug(distribution_case_be.document.form_id)
    )
    agr_bauen, agr_kantonsplanung = be_rpg2_services
    inquiry_factory_be(to_service=agr_bauen, sent=False)
    assert _rpg2_work_items(distribution_case_be).count() == 0


def test_not_created_when_disabled_be(
    db,
    rpg2_settings,
    distribution_case_be,
    inquiry_factory_be,
    disable_ech0211_settings,
    be_rpg2_services,
):
    rpg2_settings.enabled = False
    agr_bauen, agr_kantonsplanung = be_rpg2_services
    inquiry_factory_be(to_service=agr_bauen, sent=True)
    assert _rpg2_work_items(distribution_case_be).count() == 0


def test_not_created_when_allowed_forms_unset_be(
    db,
    be_rpg2_settings,
    distribution_case_be,
    inquiry_factory_be,
    disable_ech0211_settings,
    be_rpg2_services,
):
    be_rpg2_settings.allowed_forms = []
    agr_bauen, agr_kantonsplanung = be_rpg2_services
    inquiry_factory_be(to_service=agr_bauen, sent=True)
    assert _rpg2_work_items(distribution_case_be).count() == 0


def test_not_created_for_disallowed_forms_be(
    db,
    be_rpg2_settings,
    distribution_case_be,
    caluma_form_factory,
    inquiry_factory_be,
    disable_ech0211_settings,
    be_rpg2_services,
):
    caluma_form_factory(slug="vorabklaerung-vollstaendig-v6")
    Document.objects.filter(pk=distribution_case_be.document.pk).update(
        form_id="vorabklaerung-vollstaendig-v6",
    )
    agr_bauen, agr_kantonsplanung = be_rpg2_services
    inquiry_factory_be(to_service=agr_bauen, sent=True)
    assert _rpg2_work_items(distribution_case_be).count() == 0


def test_work_item_creation_idempotent_be(
    db,
    be_rpg2_settings,
    be_rpg2_services,
    distribution_case_be,
    inquiry_factory_be,
    disable_ech0211_settings,
):
    # add the distribution_case's document form slug to the allowed_forms list
    be_rpg2_settings.allowed_forms.append(
        get_unversioned_slug(distribution_case_be.document.form_id)
    )
    agr_bauen, agr_kantonsplanung = be_rpg2_services
    inquiry_factory_be(to_service=agr_bauen, sent=True)
    inquiry_factory_be(to_service=agr_kantonsplanung, sent=True)
    work_items = _rpg2_work_items(case=distribution_case_be)
    assert work_items.count() == 1


def test_created_on_inquiry_send_ag(
    db,
    ag_rpg2_settings,
    distribution_case_ag,
    inquiry_factory_ag,
    disable_ech0211_settings,
    ag_rpg2_service,
):
    # add the distribution_case's document form slug to the allowed_forms list
    ag_rpg2_settings.allowed_forms.append(
        get_unversioned_slug(distribution_case_ag.document.form_id)
    )
    inquiry_factory_ag(to_service=ag_rpg2_service, sent=True)

    work_items = _rpg2_work_items(case=distribution_case_ag)
    assert work_items.count() == 1
    work_item = work_items.get()
    assert work_item.status == WorkItem.STATUS_READY
    assert work_item.addressed_groups == [str(ag_rpg2_service.pk)]
    assert work_item.document
    assert work_item.document.form_id == "rpg2"


def test_not_created_for_other_services_ag(
    db,
    ag_rpg2_settings,
    inquiry_factory_ag,
    disable_ech0211_settings,
    service_factory,
    distribution_case_ag,
):
    # add the distribution_case's document form slug to the allowed_forms list
    ag_rpg2_settings.allowed_forms.append(
        get_unversioned_slug(distribution_case_ag.document.form_id)
    )
    inquiry_factory_ag(
        to_service=service_factory(slug="some-other-fachstelle"), sent=True
    )
    assert _rpg2_work_items(distribution_case_ag).count() == 0


def test_not_created_for_drafted_inquiry_ag(
    db,
    ag_rpg2_settings,
    distribution_case_ag,
    inquiry_factory_ag,
    disable_ech0211_settings,
    ag_rpg2_service,
):
    # add the distribution_case's document form slug to the allowed_forms list
    ag_rpg2_settings.allowed_forms.append(
        get_unversioned_slug(distribution_case_ag.document.form_id)
    )
    inquiry_factory_ag(to_service=ag_rpg2_service, sent=False)
    assert _rpg2_work_items(distribution_case_ag).count() == 0


def test_not_created_when_disabled_ag(
    db,
    rpg2_settings,
    distribution_case_ag,
    inquiry_factory_ag,
    disable_ech0211_settings,
    ag_rpg2_service,
):
    rpg2_settings.enabled = False
    inquiry_factory_ag(to_service=ag_rpg2_service, sent=True)
    assert _rpg2_work_items(distribution_case_ag).count() == 0


def test_not_created_when_allowed_forms_unset_ag(
    db,
    ag_rpg2_settings,
    distribution_case_ag,
    inquiry_factory_ag,
    disable_ech0211_settings,
    ag_rpg2_service,
):
    ag_rpg2_settings.allowed_forms = []
    inquiry_factory_ag(to_service=ag_rpg2_service, sent=True)
    assert _rpg2_work_items(distribution_case_ag).count() == 0


def test_not_created_for_disallowed_form_ag(
    db,
    ag_rpg2_settings,
    distribution_case_ag,
    inquiry_factory_ag,
    disable_ech0211_settings,
    ag_rpg2_service,
):
    Document.objects.filter(pk=distribution_case_ag.document.pk).update(
        form_id="internes-dossier",
    )
    inquiry_factory_ag(to_service=ag_rpg2_service, sent=True)
    assert _rpg2_work_items(distribution_case_ag).count() == 0


def test_work_item_creation_idempotent_ag(
    db,
    ag_rpg2_settings,
    distribution_case_ag,
    inquiry_factory_ag,
    disable_ech0211_settings,
    ag_rpg2_service,
):
    # add the distribution_case's document form slug to the allowed_forms list
    ag_rpg2_settings.allowed_forms.append(
        get_unversioned_slug(distribution_case_ag.document.form_id)
    )
    inquiry_factory_ag(to_service=ag_rpg2_service, sent=True)
    inquiry_factory_ag(to_service=ag_rpg2_service, sent=True)
    work_items = _rpg2_work_items(case=distribution_case_ag)
    assert work_items.count() == 1
