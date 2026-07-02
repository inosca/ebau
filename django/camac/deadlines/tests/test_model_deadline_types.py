import pytest
from caluma.caluma_form import models as form_models
from caluma.caluma_workflow import models as workflow_models
from django.urls import reverse
from rest_framework import status

from camac.constants.kt_gr import ARE_SERVICE_GROUP
from camac.deadlines import models as deadlines_models
from camac.tests.form_utils import FormUtils


@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name,expected_count",
    [
        # services can not see any deadline types
        ("distribution-service", "service-lead", "service", 0),
        # municipality can see deadline types
        ("lead-authority", "municipality-lead", "municipality", 5),
        # ARE can see deadline types
        ("lead-authority", "service-lead", ARE_SERVICE_GROUP, 5),
    ],
)
@pytest.mark.django_db
def test_deadline_types_list_gr(
    admin_client,
    service_factory,
    service,
    deadline_type_factory,
    service_group_factory,
    service_group,
    expected_count,
    access_level,
    role,
    gr_deadlines_settings,
    set_application_gr,
    disable_deadline_side_effects,
):
    """Test the deadline types visibilities for GR."""

    # Visible deadline types
    global_deadline_type = deadline_type_factory()
    service_deadline_type = deadline_type_factory()
    service_deadline_type.services.set([service])
    service_group_deadline_type = deadline_type_factory()
    service_group_deadline_type.service_groups.set([service_group])

    # Not visible deadline types
    other_service_deadline_type = deadline_type_factory()
    other_service_deadline_type.services.set([service_factory()])
    other_service_group_deadline_type = deadline_type_factory()
    other_service_group_deadline_type.service_groups.set([service_group_factory()])

    # procedure type deadline types
    only_regular = deadline_type_factory(
        procedure_type=deadlines_models.DeadlineType.ProcedureTypeChoices.PROCEDURE_TYPE_REGULAR.value
    )
    only_simplified = deadline_type_factory(
        procedure_type=deadlines_models.DeadlineType.ProcedureTypeChoices.PROCEDURE_TYPE_SIMPLIFIED.value
    )

    response = admin_client.get(reverse("deadline-types-list"))

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    assert len(result) == expected_count

    if expected_count > 0:
        actual_ids = set([str(r["id"]) for r in result])
        expected_ids = {
            str(global_deadline_type.pk),
            str(service_deadline_type.pk),
            str(service_group_deadline_type.pk),
            # when no instance filter is set, all procedure type deadline types
            # are visible.
            str(only_regular.pk),
            str(only_simplified.pk),
        }

        assert actual_ids == expected_ids


@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name",
    [
        ("lead-authority", "municipality-lead", "municipality"),
    ],
)
@pytest.mark.parametrize(
    "form_slug,procedure_type,expected_count",
    [
        ("baugesuch", None, 6),
        ("baugesuch-v2", None, 6),
        ("baugesuch-v3", None, 3),
        ("bauanzeige", None, 3),
        ("bauanzeige-v2", None, 5),
        ("bauanzeige-v3", None, 3),
        ("baugesuch", "regular", 6),
        ("baugesuch", "simplified", 6),
    ],
)
@pytest.mark.django_db
def test_deadline_types_list_instance_gr(
    admin_client,
    service_factory,
    service,
    deadline_type_factory,
    service_group_factory,
    caluma_work_item_factory,
    instance_factory,
    caluma_case_factory,
    service_group,
    form_slug,
    procedure_type,
    expected_count,
    access_level,
    role,
    gr_deadlines_settings,
    set_application_gr,
    disable_deadline_side_effects,
    form_utils: FormUtils,
):
    """Test the deadline types visibilities for GR."""

    # Baugesuch deadlines
    for _ in range(1, 4):
        deadline_type = deadline_type_factory(form_types=["baugesuch", "baugesuch-v2"])
        deadline_type.service_groups.set([service_group])

    # bauanzeige deadlines
    for _ in range(1, 3):
        deadline_type = deadline_type_factory(
            form_types=["bauanzeige-v2", "bauanzeige-v4"]
        )
        deadline_type.services.set([service])

    # show for all deadline types
    deadline_type_factory(form_types=None)
    deadline_type_factory(form_types=[])

    # Not visible deadline types
    other_service_deadline_type = deadline_type_factory()
    other_service_deadline_type.services.set([service_factory()])
    other_service_group_deadline_type = deadline_type_factory()
    other_service_group_deadline_type.service_groups.set([service_group_factory()])

    # procedure type deadline types
    type_regular = deadline_type_factory(
        procedure_type=deadlines_models.DeadlineType.ProcedureTypeChoices.PROCEDURE_TYPE_REGULAR.value
    )
    type_simplified = deadline_type_factory(
        procedure_type=deadlines_models.DeadlineType.ProcedureTypeChoices.PROCEDURE_TYPE_SIMPLIFIED.value
    )

    instance_case = caluma_case_factory(document__form__pk=form_slug)
    instance = instance_factory(case=instance_case)

    wi = caluma_work_item_factory(
        case=instance.case,
        task=workflow_models.Task.objects.create(slug="formal-exam"),
        status=workflow_models.WorkItem.STATUS_COMPLETED,
    )
    if procedure_type:
        form_utils.add_answer(
            wi.document,
            "verfahrensart",
            "verfahrensart-vereinfachtes-baubewilligungsverfahren"
            if procedure_type == "simplified"
            else "verfahrensart-ordentliches-baubewilligungsverfahren",
        )

    response = admin_client.get(
        reverse("deadline-types-list"),
        {"instance": str(instance.pk)},
    )

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    assert len(result) == expected_count

    actual_ids = set([str(r["id"]) for r in result])
    if procedure_type == "regular":
        expected_ids = {str(type_regular.pk)}
    elif procedure_type == "simplified":
        expected_ids = {str(type_simplified.pk)}
    else:  # only regular deadline type visible until formal exam answer is set.
        expected_ids = {str(type_regular.pk)}

    assert actual_ids.issuperset(expected_ids)


@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name",
    [("lead-authority", "municipality-lead", "municipality")],
)
@pytest.mark.parametrize(
    "search_name,expected_count",
    [
        # No search term, expect all deadline types
        (None, 3),
        # Search for "G", all visible
        ("G", 3),
        # Search for "Global", all visible
        ("Global", 3),
        # Search for "Global Type", expect "Globaltest" not to match
        ("Global Type", 2),
        # Search for " Type", all visible
        (" Type ", 3),
        # Search specific fro "Type C", only one match
        ("Type C ", 1),
    ],
)
@pytest.mark.django_db
def test_deadline_types_filters(
    gr_deadlines_settings,
    admin_client,
    deadline_type_factory,
    service_group,
    access_level,
    role,
    search_name,
    expected_count,
    disable_deadline_side_effects,
):
    """Test the deadline types filtering by name."""
    deadline_type_factory(name="Global Type A")
    deadline_type_factory(name="Global Type B")
    deadline_type_factory(name="Globaltest Type C")

    filters = {
        "name": search_name if search_name is not None else "",
    }
    response = admin_client.get(reverse("deadline-types-list"), filters)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    assert len(result) == expected_count


@pytest.mark.parametrize(
    (
        "enabled_procedure_type",
        "service_group_name",
        "procedure_type",
        "form_type",
        "expected_type",
    ),
    [
        (
            False,
            "municipality",
            deadlines_models.DeadlineType.ProcedureTypeChoices.PROCEDURE_TYPE_REGULAR.value,
            "solaranlage",
            "global-fallback",
        ),
        (
            False,
            "municipality",
            deadlines_models.DeadlineType.ProcedureTypeChoices.PROCEDURE_TYPE_REGULAR.value,
            "baugesuch",
            "baugesuch-default",
        ),
        (
            True,
            "municipality",
            deadlines_models.DeadlineType.ProcedureTypeChoices.PROCEDURE_TYPE_REGULAR.value,
            "baugesuch",
            "baugesuch-regular",
        ),
        (
            True,
            "municipality",
            deadlines_models.DeadlineType.ProcedureTypeChoices.PROCEDURE_TYPE_SIMPLIFIED.value,
            "baugesuch",
            "baugesuch-simplified",
        ),
        (
            True,
            "are",
            deadlines_models.DeadlineType.ProcedureTypeChoices.PROCEDURE_TYPE_SIMPLIFIED.value,
            "baugesuch",
            "baugesuch-are-simplified",
        ),
        (
            True,
            "municipality",
            deadlines_models.DeadlineType.ProcedureTypeChoices.PROCEDURE_TYPE_REGULAR.value,
            "solaranlage",
            "global-fallback",
        ),
        # fallback to regular when formal exam answer is not yet set.
        (
            True,
            "municipality",
            None,
            "baugesuch",
            "baugesuch-regular",
        ),
    ],
)
@pytest.mark.django_db
def test_deadline_type_get_default(
    deadline_type_factory,
    service_group_factory,
    caluma_document_factory,
    caluma_work_item_factory,
    service_factory,
    enabled_procedure_type,
    gr_instance,
    procedure_type,
    form_type,
    service_group_name,
    expected_type,
    disable_deadline_side_effects,
    set_application_gr,
    gr_deadlines_settings,
    form_utils: FormUtils,
):
    """Test the get_default method of the DeadlineType model."""
    gr_deadlines_settings.procedure_type.enabled = enabled_procedure_type

    service_group_municipality = service_group_factory(name="municipality")
    service_group_are = service_group_factory(name=ARE_SERVICE_GROUP)

    service_municipality = service_factory(
        name="municipality-service", service_group=service_group_municipality
    )
    service_are = service_factory(name="are-service", service_group=service_group_are)

    REGULAR = (
        deadlines_models.DeadlineType.ProcedureTypeChoices.PROCEDURE_TYPE_REGULAR.value
    )
    SIMPLIFIED = deadlines_models.DeadlineType.ProcedureTypeChoices.PROCEDURE_TYPE_SIMPLIFIED.value

    for setup in [
        ("global-fallback", [], None, "municipality", False, 20),
        ("baugesuch-default", ["baugesuch"], None, "municipality", True, 10),
        ("baugesuch-regular", ["baugesuch"], REGULAR, "municipality", True, 30),
        ("baugesuch-simplified", ["baugesuch"], SIMPLIFIED, "municipality", True, 30),
        ("baugesuch-are-simplified", ["baugesuch"], SIMPLIFIED, "are", True, 30),
        ("fallback-regular", [], REGULAR, "municipality", False, 100),
    ]:
        deadline_type = deadline_type_factory(
            name=setup[0],
            form_types=setup[1],
            procedure_type=setup[2],
            is_default=setup[4],
            lead_time=setup[5],
        )
        if setup[3] == "municipality":
            deadline_type.service_groups.set([service_group_municipality])
        elif setup[3] == "are":
            deadline_type.service_groups.set([service_group_are])

    if form_type:
        gr_instance.case.family.document.form.pk = form_type
        gr_instance.case.family.document.form.save()

    formal_exam = caluma_work_item_factory(
        case=gr_instance.case.family,
        document=caluma_document_factory(
            form=form_models.Form.objects.get(pk="formal-exam")
        ),
        task_id=gr_deadlines_settings.procedure_type.task_id,
        status=workflow_models.WorkItem.STATUS_COMPLETED,
    )
    if procedure_type:
        form_utils.add_answer(
            document=formal_exam.document,
            question=gr_deadlines_settings.procedure_type.question_id,
            value="verfahrensart-vereinfachtes-baubewilligungsverfahren"
            if procedure_type == SIMPLIFIED
            else "verfahrensart-ordentliches-baubewilligungsverfahren",
            question_type=form_models.Question.TYPE_CHOICE,
        )

    assert (
        deadlines_models.DeadlineType.objects.get_default(
            instance=gr_instance,
            service=service_municipality
            if service_group_name == "municipality"
            else service_are,
        ).name["de"]
        == expected_type
    )
