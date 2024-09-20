import pytest
from caluma.caluma_form.models import Answer, Question
from caluma.caluma_workflow.models import WorkItem

from camac.caluma.extensions.dynamic_groups import CustomDynamicGroups
from camac.constants import kt_uri as uri_constants
from camac.user.models import ServiceRelation


def test_dynamic_group_municipality_be(db, be_instance):
    assert CustomDynamicGroups().resolve("municipality")(
        None, be_instance.case, None, None, None
    ) == [str(be_instance.responsible_service(filter_type="municipality").pk)]


@pytest.mark.parametrize("workflow", ["building-permit", "internal-document"])
def test_dynamic_group_municipality_sz(
    db, caluma_workflow_config_sz, instance_with_case, instance, workflow
):
    instance = instance_with_case(instance=instance, workflow=workflow)

    assert CustomDynamicGroups().resolve("municipality")(
        None, instance.case, None, None, None
    ) == [str(instance.group.service.pk)]


def test_dynamic_group_construction_control(db, be_instance):
    assert CustomDynamicGroups().resolve("construction_control")(
        None, be_instance.case, None, None, None
    ) == [str(be_instance.responsible_service(filter_type="construction_control").pk)]


@pytest.mark.parametrize("has_context", [True, False])
def test_dynamic_group_distribution_create_inquiry(
    db,
    be_instance,
    caluma_admin_user,
    distribution_settings,
    has_context,
    service_factory,
    service,
    work_item_factory,
):
    prev_work_item = work_item_factory(
        case=be_instance.case, addressed_groups=[str(service.pk)]
    )
    context = {}

    if has_context:
        target_service = service_factory()
        target_subservice = service_factory(service_parent=service_factory())
        target_existing = service_factory()

        work_item_factory(
            task_id=distribution_settings["INQUIRY_CREATE_TASK"],
            case=be_instance.case,
            addressed_groups=[str(target_existing.pk)],
            status=WorkItem.STATUS_READY,
        )

        context = {
            "addressed_groups": [
                str(target_service.pk),
                str(target_subservice.pk),
                str(target_existing.pk),
            ]
        }

    resolved_groups = CustomDynamicGroups().resolve("distribution_create_inquiry")(
        task=None,
        case=be_instance.case,
        user=caluma_admin_user,
        prev_work_item=prev_work_item,
        context=context,
    )

    if has_context:
        assert str(target_service.pk) in resolved_groups
        assert str(target_subservice.pk) not in resolved_groups
        assert str(target_existing.pk) not in resolved_groups
        assert str(service.pk) in resolved_groups
    else:
        assert (
            str(be_instance.responsible_service(filter_type="municipality").pk)
            in resolved_groups
        )


@pytest.mark.parametrize("allow_subservices", [True, False])
def test_dynamic_create_additional_demand(
    db,
    work_item_factory,
    service_factory,
    distribution_settings,
    additional_demand_settings,
    caluma_admin_user,
    be_instance,
    application_settings,
    allow_subservices,
):
    target_service = service_factory()
    target_subservice = service_factory(service_parent=service_factory())
    target_existing = service_factory()

    additional_demand_settings["ALLOW_SUBSERVICES"] = allow_subservices

    # create already existing "init-additional-demand" work item
    work_item_factory(
        task_id=additional_demand_settings["CREATE_TASK"],
        case=be_instance.case,
        addressed_groups=[str(target_existing.pk)],
        status=WorkItem.STATUS_READY,
    )

    # context for when the "init-additional-demand" work item is created through
    # completion of a "create-inquiry" work item
    context = {
        "addressed_groups": [
            str(target_service.pk),
            str(target_subservice.pk),
            str(target_existing.pk),
        ]
    }

    groups_without_prev = set(
        CustomDynamicGroups().resolve("create_init_additional_demand")(
            task=None,
            case=be_instance.case,
            user=caluma_admin_user,
            prev_work_item=None,
            context={},
        )
    )

    # if no previous work item is given, fallback to municipality
    assert (
        str(be_instance.responsible_service(filter_type="municipality").pk)
        in groups_without_prev
    )

    groups_submit = set(
        CustomDynamicGroups().resolve("create_init_additional_demand")(
            task=None,
            case=be_instance.case,
            user=caluma_admin_user,
            prev_work_item=work_item_factory(
                task_id=application_settings["CALUMA"]["SUBMIT_TASKS"][0],
            ),
            context={},
        )
    )

    # if previous work item is submit, fallback to municipality
    assert (
        str(be_instance.responsible_service(filter_type="municipality").pk)
        in groups_submit
    )

    groups_additional_demand = set(
        CustomDynamicGroups().resolve("create_init_additional_demand")(
            task=None,
            case=be_instance.case,
            user=caluma_admin_user,
            prev_work_item=work_item_factory(
                task_id=additional_demand_settings["CREATE_TASK"],
                addressed_groups=[
                    str(target_service.pk),
                    str(target_subservice.pk),
                    str(target_existing.pk),
                ],
            ),
            context={},
        )
    )

    # if previous work item is "init-additional-demand" return addressed_groups
    # of previous work item exluding services that already have a ready
    # "init-additional-demand" work items and subservices
    assert str(target_service.pk) in groups_additional_demand
    assert (str(target_subservice.pk) in groups_additional_demand) == allow_subservices

    groups_inquiry = set(
        CustomDynamicGroups().resolve("create_init_additional_demand")(
            task=None,
            case=be_instance.case,
            user=caluma_admin_user,
            prev_work_item=work_item_factory(
                task_id=distribution_settings["INQUIRY_CREATE_TASK"]
            ),
            context=context,
        )
    )

    # if previous work item is "create-inquiry" return addressed_groups from
    # context exluding services that already have a ready
    # "init-additional-demand" work items and subservices
    assert str(target_service.pk) in groups_inquiry
    assert (str(target_subservice.pk) in groups_inquiry) == allow_subservices


def test_dynamic_group_geometer_be(
    db,
    be_instance,
    service_factory,
    instance_service_factory,
    use_instance_service,
    application_settings,
):
    geometer_service = service_factory(
        service_group__name="geometer",
    )

    municipality_service = service_factory(
        service_group__name="municipality",
    )

    instance_service_factory(
        instance=be_instance, service=municipality_service, active=1
    )

    ServiceRelation.objects.create(
        function=ServiceRelation.FUNCTION_GEOMETER,
        receiver=be_instance.responsible_service(filter_type="municipality"),
        provider=geometer_service,
    )

    application_settings["ACTIVE_SERVICES"]["MUNICIPALITY"]["FILTERS"] = {
        "service__service_group__name__in": [
            "municipality",
        ]
    }

    assert CustomDynamicGroups().resolve("geometer")(
        None, be_instance.case, None, None, None
    ) == [
        str(
            be_instance.responsible_service(filter_type="municipality")
            .functional_services.values_list("pk", flat=True)
            .first()
        )
    ]


@pytest.mark.parametrize(
    "given_slug,expected_group_pk",
    [
        ("geometer-ur", uri_constants.GEOMETER_SERVICE_ID),
        ("gebaeudeschaetzung-ur", uri_constants.FGS_SERVICE_ID),
    ],
)
def test_dynamic_groups_ur(
    db,
    service_factory,
    caluma_admin_user,
    ur_instance,
    given_slug,
    expected_group_pk,
):
    service_factory(pk=expected_group_pk)

    result = CustomDynamicGroups().resolve(given_slug)(
        task=None,
        case=ur_instance.case,
        user=caluma_admin_user,
        prev_work_item=None,
        context={},
    )

    assert result == [str(expected_group_pk)]


def test_dynamic_group_service_bab(
    db,
    application_settings,
    instance_service_factory,
    service_factory,
    settings,
    so_bab_settings,
    so_instance,
):
    application_settings["USE_INSTANCE_SERVICE"] = True
    application_settings["ACTIVE_SERVICES"] = settings.APPLICATIONS["kt_so"][
        "ACTIVE_SERVICES"
    ]

    service_bab = service_factory(service_group__name=so_bab_settings["SERVICE_GROUP"])
    service_canton = service_factory(service_group__name="canton")

    instance_service_factory(instance=so_instance, service=service_canton, active=1)

    assert CustomDynamicGroups().resolve("service-bab")(
        None, so_instance.case, None, None, None
    ) == [str(service_canton.pk)]

    service_canton.service_group.name = "municipality"
    service_canton.service_group.save()

    assert CustomDynamicGroups().resolve("service-bab")(
        None, so_instance.case, None, None, None
    ) == [str(service_bab.pk)]


@pytest.mark.parametrize(
    "location_id,bab_name",
    [
        (1, "ARE BaB Kreis 2"),
        (2, "ARE BaB Kreis 1"),
        (3, "ARE BaB Kreis 3"),
    ],
)
def test_dynamic_group_service_bab_ur(
    db, service_factory, ur_instance, location_id, bab_name, location_factory
):
    ur_instance.location_id = location_id
    ur_instance.save()

    location_factory(pk=location_id)

    bab_service = service_factory(
        name=bab_name, service_group__name="Fachstellen Justizdirektion"
    )

    assert CustomDynamicGroups().resolve("service-bab-ur")(
        None, ur_instance.case, None, None, None
    ) == [str(bab_service.pk)]


def test_dynamic_group_abwasser_uri(
    db,
    service_factory,
    ur_instance,
):
    service_factory(pk=uri_constants.ABWASSER_URI_SERVICE_ID)

    assert CustomDynamicGroups().resolve("abwasser-uri")(
        None, ur_instance.case, None, None, None
    ) == [str(uri_constants.ABWASSER_URI_SERVICE_ID)]


def test_dynamic_group_schnurgeruestabnahme_uri(
    db,
    service_factory,
    ur_instance,
    answer_factory,
    work_item_factory,
    document_factory,
    mocker,
    construction_monitoring_settings,
):
    service = service_factory()
    ur_instance.responsible_service = mocker.PropertyMock(return_value=service)

    planning_work_item = work_item_factory(
        case=ur_instance.case,
        task_id=construction_monitoring_settings[
            "CONSTRUCTION_STEP_PLAN_CONSTRUCTION_STAGE_TASK"
        ],
        document=document_factory(),
    )

    question = Question.objects.get(pk="schnurgeruestabnahme-durch")

    answer_factory(
        document=planning_work_item.document,
        question=question,
        value="schnurgeruestabnahme-durch-gemeinde",
    )

    assert CustomDynamicGroups().resolve("schnurgeruestabnahme-uri")(
        None, ur_instance.case, None, None, None
    ) == [str(service.pk)]

    Answer.objects.all().delete()

    geometer_service = service_factory(pk=uri_constants.GEOMETER_SERVICE_ID)

    answer_factory(
        document=planning_work_item.document,
        question=question,
        value="wer-fuehrt-die-schnurgeruestabnahme-durch-geometer",
    )

    assert CustomDynamicGroups().resolve("schnurgeruestabnahme-uri")(
        None, ur_instance.case, None, None, None
    ) == [str(geometer_service.pk)]


def test_dynamic_group_building_commission(
    db, ur_instance, service_factory, group_factory, location_factory, mocker
):
    municipality_service = service_factory(
        service_group__name="Sekretariate Gemeindebaubehörden"
    )
    group1 = group_factory()
    group2 = group_factory()
    location = location_factory()

    group1.locations.add(location)
    group2.locations.add(location)
    group1.save()
    group2.save()

    building_commission = service_factory(
        service_group__name="Mitglieder Baukommissionen"
    )
    municipality_service.groups.add(group1)
    building_commission.groups.add(group2)
    municipality_service.save()
    building_commission.save()

    # Mock the implementation details of the municipality property on the instance
    type(ur_instance).municipality = mocker.PropertyMock(
        return_value=municipality_service
    )

    assert CustomDynamicGroups().resolve("building-commission")(
        None, ur_instance.case, None, None, None
    ) == [str(building_commission.pk)]
