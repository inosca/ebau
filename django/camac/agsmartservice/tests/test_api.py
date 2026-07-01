import pytest

from camac.agsmartservice import api, tasks

TITLE = "Baugesuch EB-123 (Aarau): Umbau"


@pytest.mark.django_db
def test_build_procedure_title_with_master_data(
    ag_master_data_case, set_application_ag
):
    assert api.build_procedure_title(ag_master_data_case.instance) == (
        'Baugesuch 2025-1 (Aarburg): Überbauung "Westfeld"'
    )


@pytest.mark.parametrize(
    ("method", "task", "extra_args", "expected_extra_args"),
    [
        (
            "submit",
            tasks.submit_procedure_task,
            ("N123456",),
            (TITLE, "N123456"),
        ),
        (
            "complete_preliminary_check",
            tasks.complete_preliminary_check_task,
            (),
            (TITLE,),
        ),
        (
            "start_construction_monitoring",
            tasks.start_construction_monitoring_task,
            (),
            (TITLE,),
        ),
        ("complete", tasks.complete_procedure_task, (), (TITLE,)),
        ("delete_procedure", tasks.delete_procedure_task, (), ()),
    ],
)
@pytest.mark.django_db
def test_schedule(
    method,
    task,
    extra_args,
    expected_extra_args,
    ag_instance,
    ag_agsmartservice_settings,
    mocker,
):
    mocker.patch("camac.agsmartservice.api.CalumaApi.is_paper", return_value=False)
    mocker.patch("camac.agsmartservice.api.build_procedure_title", return_value=TITLE)
    delay_on_commit = mocker.patch.object(task, "delay_on_commit")

    assert (
        getattr(api, method)(ag_instance, *extra_args) == delay_on_commit.return_value
    )
    delay_on_commit.assert_called_once_with(ag_instance.pk, *expected_extra_args)


@pytest.mark.parametrize(
    ("method", "task", "extra_args"),
    [
        ("submit", tasks.submit_procedure_task, ("N123456",)),
        ("complete_preliminary_check", tasks.complete_preliminary_check_task, ()),
        (
            "start_construction_monitoring",
            tasks.start_construction_monitoring_task,
            (),
        ),
        ("complete", tasks.complete_procedure_task, ()),
        ("delete_procedure", tasks.delete_procedure_task, ()),
    ],
)
@pytest.mark.django_db
def test_paper_dossier_does_not_schedule_task(
    method,
    task,
    extra_args,
    ag_instance,
    ag_agsmartservice_settings,
    mocker,
):
    mocker.patch("camac.agsmartservice.api.CalumaApi.is_paper", return_value=True)
    build_procedure_title = mocker.patch(
        "camac.agsmartservice.api.build_procedure_title"
    )
    delay_on_commit = mocker.patch.object(task, "delay_on_commit")

    assert getattr(api, method)(ag_instance, *extra_args) is None
    delay_on_commit.assert_not_called()
    build_procedure_title.assert_not_called()


@pytest.mark.django_db
def test_disabled_module_does_not_schedule_task(
    ag_instance, disable_agsmartservice_settings, mocker
):
    is_paper = mocker.patch("camac.agsmartservice.api.CalumaApi.is_paper")
    delay_on_commit = mocker.patch.object(
        tasks.submit_procedure_task, "delay_on_commit"
    )

    assert api.submit(ag_instance, "N123456") is None
    delay_on_commit.assert_not_called()
    is_paper.assert_not_called()
