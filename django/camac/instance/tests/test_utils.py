import pytest
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Document, Question
from caluma.caluma_workflow.models import Case

from camac.instance.models import Instance
from camac.instance.utils import (
    be_should_prevent_process_step_for_deactivated_municipality,
    get_municipality,
    get_pdf_category,
    get_pdf_section,
    set_construction_control,
)
from camac.tests.form_utils import FormUtils


@pytest.mark.parametrize(
    ("form_slug", "case_form_slug", "expected_category"),
    [
        (None, None, "main-category"),
        ("special-form", None, "special-category"),
        (None, "special-form", "special-category"),
        ("special-form", "other-form", "special-category"),
        (None, "other-form", "main-category"),
    ],
)
def test_get_pdf_category(
    application_settings, form_slug, case_form_slug, expected_category
):
    application_settings["DOCUMENT_BACKEND"] = "alexandria"
    application_settings["STORE_PDF"] = {
        "CATEGORY": {
            "MAIN": "main-category",
            "SPECIAL-FORM": "special-category",
        }
    }
    document = Document()
    if case_form_slug:
        document.form_id = case_form_slug
    case = Case(document=document)
    instance = Instance(case=case)

    assert get_pdf_category(instance, form_slug) == expected_category


@pytest.mark.parametrize(
    ("form_slug", "paper", "expected_section"),
    [
        (None, False, 1),  # Beilagen zum Gesuch
        (None, True, 13),  # Beilagen zum Gesuch (Papier und Nachrichten)
        ("sb1", False, 6),  # Beilagen SB1
        ("sb1", True, 10),  # Beilagen SB1 (Papier und Nachrichten)
        ("sb1-v2", False, 6),  # Beilagen SB1
        ("sb1-v2", True, 10),  # Beilagen SB1 (Papier und Nachrichten)
        ("sb2", False, 5),  # Beilagen SB2
        ("sb2", True, 11),  # Beilagen SB2 (Papier und Nachrichten)
    ],
)
def test_get_pdf_section(
    set_application_be,
    mocker,
    form_slug,
    paper,
    expected_section,
):
    mocker.patch("camac.instance.utils.CalumaApi.is_paper", return_value=paper)
    instance = Instance()

    assert get_pdf_section(instance, form_slug) == expected_section


@pytest.mark.parametrize(
    (
        "current_service_name",
        "is_rsta",
        "involved_municipality_name",
        "caluma_form_municipality_name",
        "expected_service_name",
    ),
    [
        ("Leitbehörde Bern", False, None, None, "Baukontrolle Bern"),
        (
            "Regierungsstatthalteramt Bern-Mittelland",
            True,
            "Leitbehörde Bern",
            None,
            "Baukontrolle Bern",
        ),
        (
            "Regierungsstatthalteramt Bern-Mittelland",
            True,
            None,
            "Leitbehörde Bern",
            "Baukontrolle Bern",
        ),
    ],
)
@pytest.mark.django_db
def test_set_construction_control(
    be_instance,
    caluma_admin_user,
    multilang,
    service_factory,
    instance_service_factory,
    current_service_name,
    is_rsta,
    involved_municipality_name,
    caluma_form_municipality_name,
    caluma_dynamic_option_factory,
    expected_service_name,
    form_utils: FormUtils,
):
    # create construction control service
    construction_control = service_factory(
        trans__name=expected_service_name,
        trans__language="de",
        service_group__name="construction-control",
    )

    form_utils.add_answer(
        be_instance.case.document, "gemeinde", str(construction_control.pk)
    )
    caluma_dynamic_option_factory(
        slug=str(construction_control.pk),
        question_id="gemeinde",
        document=be_instance.case.document,
    )

    # create currently responsible municipality or district
    instance_service_factory(
        instance=be_instance,
        active=1,
        service=service_factory(
            trans__name=current_service_name,
            trans__language="de",
            service_group__name=("district" if is_rsta else "municipality"),
        ),
    )

    if involved_municipality_name:
        # create involved but not active municipality
        instance_service_factory(
            instance=be_instance,
            active=0,
            service=service_factory(
                trans__name=involved_municipality_name,
                trans__language="de",
                service_group__name="municipality",
            ),
        )

    if caluma_form_municipality_name:
        # create municipality filled in caluma form
        caluma_service = service_factory(
            trans__name=caluma_form_municipality_name,
            trans__language="de",
            service_group__name="municipality",
        )
        save_answer(
            document=be_instance.case.document,
            question=Question.objects.get(pk="gemeinde"),
            value=str(caluma_service.pk),
            user=caluma_admin_user,
        )

    assert set_construction_control(be_instance) == construction_control
    assert be_instance.instance_services.filter(
        service__service_group__name="construction-control",
        active=1,
        service=construction_control,
    ).exists()


@pytest.mark.freeze_time("2025-11-05 15:15:15+02:00")
@pytest.mark.parametrize(
    ("service_group_name", "meta_config", "expected_result"),
    [
        # No configuration (not deactivated)
        ("municipality", {}, False),
        # Faulty configuration (not deactivated)
        ("municipality", {"deactivated-municipality-at": True}, False),
        ("municipality", {"deactivated-municipality-at": "test"}, False),
        # No time given, defaults to midnight (start) of given date
        # in current timezone (deactivated)
        ("municipality", {"deactivated-municipality-at": "2025-11-05"}, True),
        # Not timezone aware, defaults to current timezone (not deactivated)
        ("municipality", {"deactivated-municipality-at": "2025-11-05T18:15:15"}, False),
        # Deactivation on or before current time (deactivated)
        (
            "municipality",
            {"deactivated-municipality-at": "2025-11-05T15:14:15+02:00"},
            True,
        ),
        (
            "municipality",
            {"deactivated-municipality-at": "2025-11-05T15:15:15+02:00"},
            True,
        ),
        (
            "municipality",
            {"deactivated-municipality-at": "2025-11-04T15:15:15+02:00"},
            True,
        ),
        # Deactivation after current time (not deactivated)
        (
            "municipality",
            {"deactivated-municipality-at": "2025-11-05T15:16:15+02:00"},
            False,
        ),
        (
            "municipality",
            {"deactivated-municipality-at": "2025-11-06T15:15:15+02:00"},
            False,
        ),
        # Active service isn't a municipality (not deactivated)
        (
            "district",
            {"deactivated-municipality-at": "2025-11-04T15:15:15+02:00"},
            False,
        ),
    ],
)
@pytest.mark.django_db
def test_deactivated_municipality(
    be_instance,
    service_factory,
    instance_service_factory,
    freezer,
    service_group_name,
    meta_config,
    expected_result,
):
    lead_auth = service_factory(
        service_group__name=service_group_name, meta=meta_config
    )
    be_instance.instance_services.all().delete()
    be_instance.instance_services.add(instance_service_factory(service=lead_auth))

    assert (
        be_should_prevent_process_step_for_deactivated_municipality(be_instance)
        == expected_result
    )


@pytest.mark.django_db
def test_get_municipality_returns_active_municipality(
    be_instance, service_factory, instance_service_factory
):
    """
    Verify get_municipality() behaviour when active service is a municipality.

    When the active service is a municipality return it, disregarding any
    attached inactive municipalities and active non-municipality services.
    """

    active_municipality = service_factory(service_group__name="municipality")
    instance_service_factory(
        instance=be_instance, active=1, service=active_municipality
    )

    # Inactive municipality attached to the same instance
    inactive_municipality = service_factory(service_group__name="municipality")
    instance_service_factory(
        instance=be_instance, active=0, service=inactive_municipality
    )

    # Active non-municipality service attached to the same instance
    other_service = service_factory(service_group__name="other")
    instance_service_factory(instance=be_instance, active=1, service=other_service)

    result = get_municipality(be_instance)

    assert result == active_municipality


@pytest.mark.django_db
def test_get_municipality_fallback_to_form_answer(
    be_instance,
    service_factory,
    instance_service_factory,
    form_utils: FormUtils,
):
    """
    Ensure get_municipality() behavour when active service is not a municipality.

    If the active service isn't a municipality, or there is no active
    service, we expect to get the involved but not active municipality
    as a result.

    If multiple municipalities are involved, we expect the Caluma form to be
    consulted, and the selected municipality from the form to be returned.
    """

    first_municipality = service_factory(service_group__name="municipality")
    involved_municipality = service_factory(service_group__name="municipality")

    instance_service_factory(instance=be_instance, active=0, service=first_municipality)
    instance_service_factory(
        instance=be_instance, active=0, service=involved_municipality
    )

    form_utils.add_answer(
        be_instance.case.document, "gemeinde", str(involved_municipality.pk)
    )

    result = get_municipality(be_instance)

    assert result == involved_municipality


@pytest.mark.django_db
def test_get_municipality_fallback_to_first_involved(
    be_instance,
    service_factory,
    instance_service_factory,
    form_utils: FormUtils,
):
    """
    Ensure get_municipality() behavour when active service is not a municipality.

    If the active service isn't a municipality, or there is no active
    service, we expect to get the involved but not active municipality
    as a result.

    If multiple municipalities are involved and the question "gemeinde" does not
    match an involved municipality, we expect the first involved municipality to
    be returned.
    """

    first_municipality = service_factory(service_group__name="municipality")
    involved_municipality = service_factory(service_group__name="municipality")

    instance_service_factory(instance=be_instance, active=0, service=first_municipality)
    instance_service_factory(
        instance=be_instance, active=0, service=involved_municipality
    )

    form_utils.add_answer(be_instance.case.document, "gemeinde", "999999")

    result = get_municipality(be_instance)

    assert result == first_municipality


@pytest.mark.django_db
def test_get_municipality_fallback_to_form_answer_no_involved_municipality(
    be_instance,
    service_factory,
    form_utils: FormUtils,
):
    """
    Ensure get_municipality() fallback when there are no active or involved municipalities.

    If no municipalities are active or involved, we expect the Caluma form to be
    consulted, and the selected municipality from the form to be returned.
    """

    form_municipality = service_factory(service_group__name="municipality")

    form_utils.add_answer(
        be_instance.case.document, "gemeinde", str(form_municipality.pk)
    )

    result = get_municipality(be_instance)

    assert result == form_municipality
