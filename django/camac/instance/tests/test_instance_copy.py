from datetime import date

import pytest
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status

from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.models import Instance, InstanceState
from camac.permissions.models import AccessLevel, InstanceACL
from camac.permissions.switcher import PERMISSION_MODE
from camac.tests.form_utils import FormUtils


@pytest.fixture
def instance_for_copy(
    admin_client,
    application_settings,
    multilang,
    be_instance,
    caluma_admin_user,
    instance_state_factory,
    mocker,
    settings,
    use_instance_service,
    service_factory,
    instance_service_factory,
):
    call_command(
        "loaddata", settings.ROOT_DIR("kt_bern/config/caluma_ebau_number_form.json")
    )

    mocker.patch("camac.notification.utils.send_mail", return_value=None)
    instance_state_factory(name="new")
    instance_state_factory(name="subm")
    instance_state_factory(name="circulation_init")
    instance_state_factory(name="coordination")
    instance_state_factory(name="sb1")
    instance_state_factory(name="conclusion")
    instance_state_factory(name="rejected")
    instance_state_factory(name="finished")
    instance_state_factory(name="finished_internal")
    instance_state_factory(name="archived")
    instance_state_factory(name="evaluated")

    def wrapper(instance_state_name):
        be_instance.case.meta.update({"ebau-number": "2026-456"})
        be_instance.case.save()

        be_instance.instance_state = InstanceState.objects.get(name=instance_state_name)

        last_active_municipality = service_factory(
            service_group__name="municipality",
            trans__name="Last Active Leitbehörde",
            trans__language="de",
        )
        # add last active municipality to test it is copied to new instance
        be_instance.instance_services.add(
            instance_service_factory(service=last_active_municipality, active=1)
        )

        other_inactive_municipality = service_factory(
            service_group__name="municipality",
            trans__name="Another Inactive Leitbehörde",
            trans__language="de",
        )

        # add other active services to test they are copied to new instance
        be_instance.instance_services.add(
            instance_service_factory(service=other_inactive_municipality, active=0)
        )

        construction_control = service_factory(
            service_group__name="construction-control",
            trans__name="Baukontrolle Bern",
            trans__language="de",
        )
        # add construction-control to test it is not copied to new instance
        be_instance.instance_services.add(
            instance_service_factory(service=construction_control, active=1)
        )

        # create another involved applicant to test that all involved applicants
        # are copied to new instance
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )

        be_instance.save()

        return be_instance

    return wrapper


@pytest.mark.django_db
def test_instance_copy_404(instance, admin_client):
    response = admin_client.post(reverse("instance-copy", args=[instance.pk]))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    (
        "role__name",
        "access_level",
        "grant_type",
        "instance_state_name",
        "expected_status",
    ),
    [
        # Forbidden: wrong access level,
        (
            "applicant",
            "applicant",
            "USER",
            "archived",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "service-lead",
            "distribution-service",
            "SERVICE",
            "archived",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "municipality-lead",
            "lead-authority",
            "SERVICE",
            "archived",
            status.HTTP_403_FORBIDDEN,
        ),
        # Forbidden: right access level, wrong instance state
        ("Support", "support", "ROLE", "new", status.HTTP_403_FORBIDDEN),
        ("Support", "support", "ROLE", "subm", status.HTTP_403_FORBIDDEN),
        # Allowed: right access level, right instance state
        ("Support", "support", "ROLE", "archived", status.HTTP_201_CREATED),
        ("Support", "support", "ROLE", "finished", status.HTTP_201_CREATED),
    ],
)
@pytest.mark.django_db
def test_instance_copy_with_permissions_module_be(
    admin_client,
    access_level,
    grant_type,
    expected_status,
    instance_for_copy,
    instance_state_name,
    permissions_settings,
    application_settings,
    be_permissions_settings,
    be_access_levels,
    instance_acl_factory,
    settings,
    multilang,
    mock_generate_and_store_pdf,
    be_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    be_permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    be_permissions_settings["EVENT_HANDLER"] = (
        "camac.permissions.config.kt_bern.PermissionEventHandlerBE"
    )

    instance = instance_for_copy(instance_state_name)

    granted_access_level = AccessLevel.objects.get(pk=access_level)
    granting_service = admin_client.user.get_default_group().service
    granting_user = admin_client.user
    granting_role = admin_client.user.groups.first().role

    granting_entity_by_grant_type = {
        "USER": ("user", granting_user),
        "SERVICE": ("service", granting_service),
        "ROLE": ("role", granting_role),
    }

    key, value = granting_entity_by_grant_type[grant_type]

    instance_acl_factory(
        instance=instance,
        access_level=granted_access_level,
        grant_type=grant_type,
        **{key: value},
    )

    lead_authority_service = (
        instance.instance_services.filter(service__service_group__name="municipality")
        .first()
        .service
    )

    # add a lead-authority ACL to original instance to test that it is copied over.
    instance_acl_factory(
        instance=instance,
        service=lead_authority_service,
        access_level=AccessLevel.objects.get(pk="lead-authority"),
        grant_type="SERVICE",
    )

    original_municipality_service_ids = set(
        instance.instance_services.filter(
            service__service_group__name="municipality"
        ).values_list("service_id", flat=True)
    )

    original_service_ids_to_be_copied = set(
        instance.instance_services.exclude(
            service__service_group__name="construction-control"
        ).values_list("service_id", flat=True)
    )

    original_applicant_user_ids = set(
        instance.involved_applicants.values_list("user_id", flat=True)
    )

    assert instance.instance_services.count() == 4
    assert instance.involved_applicants.count() == 2

    response = admin_client.post(reverse("instance-copy", args=[instance.pk]))

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_201_CREATED:
        new_instance = Instance.objects.get(pk=response.json()["data"]["id"])

        assert new_instance.case.meta.get("is-copy") is True
        assert new_instance.instance_state.name == "subm"

        copied_municipality_service_ids = set(
            new_instance.instance_services.filter(
                service__service_group__name="municipality"
            ).values_list("service_id", flat=True)
        )

        all_copied_service_ids = set(
            new_instance.instance_services.all().values_list("service_id", flat=True)
        )

        # municipality services are copied
        assert copied_municipality_service_ids == original_municipality_service_ids

        # construction-control services are not copied
        assert original_service_ids_to_be_copied == all_copied_service_ids
        assert new_instance.instance_services.count() == 3

        # involved applicants are all copied
        copied_applicant_user_ids = set(
            new_instance.involved_applicants.values_list("user_id", flat=True)
        )
        assert copied_applicant_user_ids == original_applicant_user_ids
        assert new_instance.involved_applicants.count() == 2

        # instance ACLs are granted on the copy
        new_acls = InstanceACL.objects.filter(instance=new_instance)

        # instance ACL granted by InstanceCreationHandlerMixin.instance_created()
        assert new_acls.filter(access_level_id="support").exists()

        # instance ACL granted by InstanceCopyHandlerMixin.instance_copied()
        assert new_acls.filter(
            service=lead_authority_service,
            access_level_id="lead-authority",
        ).exists()

        mock_generate_and_store_pdf.assert_called_once()
        called_instance = mock_generate_and_store_pdf.call_args[0][0]
        assert called_instance.pk == new_instance.pk

        history = new_instance.history.exclude(history_type="notification").last()
        assert (
            history.get_trans_attr(name="title", lang="de")
            == "Kopie des Dossiers erstellt"
        )


@pytest.mark.django_db
def test_copy_caluma_data_ag(
    ag_instance,
    instance_with_case,
    instance_factory,
    ag_instance_copy_settings,
    caluma_question_factory,
    form_utils: FormUtils,
):
    target_instance = instance_with_case(instance_factory())
    question_slug = ag_instance_copy_settings.demolition_payment.special_id_slug
    date_question_slug = "allowlisted-date-question"
    date_value = date(2026, 7, 17)
    caluma_question_factory(
        slug=question_slug,
        type="text",
    )
    ag_instance_copy_settings.demolition_payment.simple_questions.append(
        date_question_slug
    )
    form_utils.add_answer(
        ag_instance.case.document,
        date_question_slug,
        date_value,
    )
    ag_instance.case.meta["dossier-number"] = "2026-123"
    ag_instance.case.save()
    CreateInstanceLogic.copy_caluma_data(
        target_instance,
        ag_instance,
        copy_type="demolition_payment",
        user=None,
    )
    assert (
        target_instance.case.document.answers.filter(question_id=question_slug)
        .first()
        .value
        == "2026-123"
    )
    assert (
        target_instance.case.document.answers.get(question_id=date_question_slug).date
        == date_value
    )


@pytest.mark.django_db
def test_copy_caluma_data_denylisted_gr(
    gr_instance,
    instance_with_case,
    instance_factory,
    gr_instance_copy_settings,
    caluma_question_factory,
    form_utils: FormUtils,
):
    target_instance = instance_with_case(instance_factory())

    non_excluded_slug = "non-excluded-question"
    non_excluded_date_slug = "non-excluded-date-question"
    non_excluded_table_slug = "non-excluded-table-question"
    excluded_slug = "excluded-question"
    excluded_table_slug = "excluded-table-question"

    gr_instance_copy_settings.ebbw_next_phase.exclude_questions.append(excluded_slug)
    gr_instance_copy_settings.ebbw_next_phase.exclude_questions.append(
        excluded_table_slug
    )

    form_utils.add_answer(
        gr_instance.case.document, non_excluded_slug, "non-excluded-value"
    )
    form_utils.add_answer(
        gr_instance.case.document, non_excluded_date_slug, date(2026, 7, 17)
    )
    form_utils.add_table_answer(
        gr_instance.case.document,
        non_excluded_table_slug,
        [{"col1": "a", "col2": "b"}],
    )
    form_utils.add_answer(gr_instance.case.document, excluded_slug, "excluded-value")
    form_utils.add_table_answer(
        gr_instance.case.document,
        excluded_table_slug,
        [{"col1": "c", "col2": "d"}],
    )
    gr_instance.case.document.meta["copied-meta"] = True
    gr_instance.case.document.save(update_fields=["meta"])

    target_form = target_instance.case.document.form

    CreateInstanceLogic.copy_caluma_data(
        target_instance,
        gr_instance,
        copy_type="ebbw_next_phase",
        user=None,
    )

    source_answers = gr_instance.case.document.flat_answer_map()
    target_answers = target_instance.case.document.flat_answer_map()

    # non-excluded answers should be equal for simple and table questions.
    assert source_answers[non_excluded_slug] == target_answers[non_excluded_slug]
    assert (
        source_answers[non_excluded_date_slug] == target_answers[non_excluded_date_slug]
    )
    assert (
        source_answers[non_excluded_table_slug]
        == target_answers[non_excluded_table_slug]
    )
    # excluded answers should not be copied to the target instance
    # for both simple and table questions.
    assert excluded_slug not in target_answers
    assert excluded_table_slug not in target_answers
    assert target_instance.case.document.form == target_form
    assert target_instance.case.document.source == gr_instance.case.document
    assert target_instance.case.document.meta["copied-meta"] is True


@pytest.mark.parametrize(
    ("is_modification", "expect_confirmation_copied"),
    [(True, False), (False, True)],
)
@pytest.mark.django_db
def test_copy_caluma_data_excludes_confirmation_answers_be(
    be_instance,
    be_instance_copy_settings,
    caluma_form_factory,
    caluma_form_question_factory,
    form_utils: FormUtils,
    instance_factory,
    instance_with_case,
    is_modification,
    expect_confirmation_copied,
    set_application_be,
):
    target_instance = instance_with_case(instance_factory())

    confirmation_answer = form_utils.add_answer(
        be_instance.case.document,
        "confirmation-answer",
        "confirmation-value",
    )
    caluma_form_question_factory(
        form=caluma_form_factory(slug="7-bestaetigung"),
        question=confirmation_answer.question,
    )

    receipt_answer = form_utils.add_answer(
        be_instance.case.document,
        "receipt-answer",
        "receipt-value",
    )
    caluma_form_question_factory(
        form=caluma_form_factory(slug="8-freigabequittung"),
        question=receipt_answer.question,
    )

    CreateInstanceLogic.copy_caluma_data(
        target_instance,
        be_instance,
        copy_type="full" if not is_modification else "full_without_confirmation",
        user=None,
    )

    copied_answers = target_instance.case.document.answers
    assert (
        copied_answers.filter(question_id="confirmation-answer").exists()
        is expect_confirmation_copied
    )
    assert not copied_answers.filter(question_id="receipt-answer").exists()
