import pytest
from caluma.caluma_form.models import Document
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.models import WorkItem

from camac.caluma.extensions.events.rpg2 import (
    is_rpg2_relevant_form,
    is_rpg2_service_addressed,
)
from camac.instance.models import HistoryEntry
from camac.user.models import Service
from camac.utils import get_unversioned_slug


def _rpg2_work_items(case):
    return case.work_items.filter(task_id="rpg2")


@pytest.fixture
def be_rpg2_service(db, service_factory):
    return service_factory(slug="agr-bauen")


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
@pytest.mark.django_db
def test_is_rpg2_relevant_form(
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
@pytest.mark.django_db
def test_is_rpg2_service_addressed(
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


@pytest.mark.django_db
def test_created_on_inquiry_send_be(
    be_rpg2_settings,
    be_rpg2_service,
    distribution_case_be,
    inquiry_factory_be,
    disable_ech0211_settings,
):
    # add the distribution_case's document form slug to the allowed_forms list
    be_rpg2_settings.allowed_forms.append(
        get_unversioned_slug(distribution_case_be.document.form_id)
    )
    inquiry_factory_be(to_service=be_rpg2_service, sent=True)
    work_items = _rpg2_work_items(case=distribution_case_be)
    assert work_items.count() == 1
    work_item = work_items.get()
    assert work_item.status == WorkItem.STATUS_READY
    assert set(work_item.addressed_groups) == {
        str(be_rpg2_service.pk),
    }
    assert work_item.document
    assert work_item.document.form_id == "rpg2"


@pytest.mark.django_db
def test_not_created_for_other_services_be(
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


@pytest.mark.django_db
def test_not_created_for_drafted_inquiry_be(
    be_rpg2_settings,
    distribution_case_be,
    inquiry_factory_be,
    disable_ech0211_settings,
    be_rpg2_service,
):
    # add the distribution_case's document form slug to the allowed_forms list
    be_rpg2_settings.allowed_forms.append(
        get_unversioned_slug(distribution_case_be.document.form_id)
    )
    inquiry_factory_be(to_service=be_rpg2_service, sent=False)
    assert _rpg2_work_items(distribution_case_be).count() == 0


@pytest.mark.django_db
def test_not_created_when_disabled_be(
    disable_rpg2_settings,
    distribution_case_be,
    inquiry_factory_be,
    disable_ech0211_settings,
    be_rpg2_service,
):
    inquiry_factory_be(to_service=be_rpg2_service, sent=True)
    assert _rpg2_work_items(distribution_case_be).count() == 0


@pytest.mark.django_db
def test_not_created_when_allowed_forms_unset_be(
    be_rpg2_settings,
    distribution_case_be,
    inquiry_factory_be,
    disable_ech0211_settings,
    be_rpg2_service,
):
    be_rpg2_settings.allowed_forms = []
    inquiry_factory_be(to_service=be_rpg2_service, sent=True)
    assert _rpg2_work_items(distribution_case_be).count() == 0


@pytest.mark.django_db
def test_not_created_for_disallowed_forms_be(
    be_rpg2_settings,
    distribution_case_be,
    caluma_form_factory,
    inquiry_factory_be,
    disable_ech0211_settings,
    be_rpg2_service,
):
    caluma_form_factory(slug="vorabklaerung-einfach-v5")
    Document.objects.filter(pk=distribution_case_be.document.pk).update(
        form_id="vorabklaerung-einfach-v5",
    )
    inquiry_factory_be(to_service=be_rpg2_service, sent=True)
    assert _rpg2_work_items(distribution_case_be).count() == 0


@pytest.mark.django_db
def test_work_item_creation_idempotent_be(
    be_rpg2_settings,
    be_rpg2_service,
    distribution_case_be,
    inquiry_factory_be,
    disable_ech0211_settings,
):
    # add the distribution_case's document form slug to the allowed_forms list
    be_rpg2_settings.allowed_forms.append(
        get_unversioned_slug(distribution_case_be.document.form_id)
    )
    inquiry_factory_be(to_service=be_rpg2_service, sent=True)
    inquiry_factory_be(to_service=be_rpg2_service, sent=True)
    work_items = _rpg2_work_items(case=distribution_case_be)
    assert work_items.count() == 1


@pytest.mark.django_db
def test_created_on_inquiry_send_ag(
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


@pytest.mark.django_db
def test_not_created_for_other_services_ag(
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


@pytest.mark.django_db
def test_not_created_for_drafted_inquiry_ag(
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


@pytest.mark.django_db
def test_not_created_when_disabled_ag(
    disable_rpg2_settings,
    distribution_case_ag,
    inquiry_factory_ag,
    disable_ech0211_settings,
    ag_rpg2_service,
):
    inquiry_factory_ag(to_service=ag_rpg2_service, sent=True)
    assert _rpg2_work_items(distribution_case_ag).count() == 0


@pytest.mark.django_db
def test_not_created_when_allowed_forms_unset_ag(
    ag_rpg2_settings,
    distribution_case_ag,
    inquiry_factory_ag,
    disable_ech0211_settings,
    ag_rpg2_service,
):
    ag_rpg2_settings.allowed_forms = []
    inquiry_factory_ag(to_service=ag_rpg2_service, sent=True)
    assert _rpg2_work_items(distribution_case_ag).count() == 0


@pytest.mark.django_db
def test_not_created_for_disallowed_form_ag(
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


@pytest.mark.django_db
def test_work_item_creation_idempotent_ag(
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


@pytest.mark.django_db
def test_pay_demolition_premium_history_sz(
    application_settings,
    caluma_admin_user,
    caluma_work_item_factory,
    form_factory,
    instance_state_factory,
    mocker,
    set_application_sz,
    service,
    sz_instance,
):
    done_state = instance_state_factory(name="done")

    form = form_factory(name="abbruchpraemie")
    form.family = form
    form.save()

    sz_instance.instance_state = done_state
    sz_instance.form = form
    sz_instance.save()

    wi_pay_premium = caluma_work_item_factory(
        task_id="pay-demolition-premium",
        case=sz_instance.case,
        child_case=None,
        addressed_groups=[service.pk],
        status=WorkItem.STATUS_READY,
    )

    assert (
        HistoryEntry.objects.filter(
            instance=sz_instance,
            history_type="status-change",
            title="RPG2-Abbruchprämie ausgezahlt",
        ).count()
        == 0
    )

    complete_work_item(work_item=wi_pay_premium, user=caluma_admin_user)
    sz_instance.refresh_from_db()

    assert sz_instance.instance_state == done_state
    assert (
        HistoryEntry.objects.filter(
            instance=sz_instance,
            history_type="status-change",
            title="RPG2-Abbruchprämie ausgezahlt",
        ).count()
        == 1
    )
