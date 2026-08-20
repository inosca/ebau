from camac.agsmartservice import tasks

TITLE = "Baugesuch EB-123 (Aarau): Umbau"


def _client(mocker, settings):
    settings.PUBLIC_INSTANCE_URL_TEMPLATE = (
        "https://portal.example.url/instances/{instance_id}"
    )
    return mocker.patch(
        "camac.agsmartservice.tasks.AGSmartServiceClient.put_procedure",
    )


def test_submit_procedure_task(mocker, snapshot, settings, ag_agsmartservice_settings):
    put_procedure = _client(mocker, settings)

    assert tasks.submit_procedure_task("INSTANCEID", TITLE, "N123456") is None

    put_procedure.assert_called_once()
    instance_id, payload = put_procedure.call_args.args
    assert instance_id == "INSTANCEID"
    assert payload == snapshot


def test_complete_preliminary_check_task(
    mocker, snapshot, settings, ag_agsmartservice_settings
):
    put_procedure = _client(mocker, settings)

    assert tasks.complete_preliminary_check_task("INSTANCEID", TITLE) is None

    put_procedure.assert_called_once()
    instance_id, payload = put_procedure.call_args.args
    assert instance_id == "INSTANCEID"
    assert payload == snapshot


def test_start_construction_monitoring_task(
    mocker, snapshot, settings, ag_agsmartservice_settings
):
    put_procedure = _client(mocker, settings)

    assert tasks.start_construction_monitoring_task("INSTANCEID", TITLE) is None

    put_procedure.assert_called_once()
    instance_id, payload = put_procedure.call_args.args
    assert instance_id == "INSTANCEID"
    assert payload == snapshot


def test_complete_procedure_task(
    mocker, snapshot, settings, ag_agsmartservice_settings
):
    put_procedure = _client(mocker, settings)

    assert tasks.complete_procedure_task("INSTANCEID", TITLE) is None

    put_procedure.assert_called_once()
    instance_id, payload = put_procedure.call_args.args
    assert instance_id == "INSTANCEID"
    assert payload == snapshot


def test_delete_procedure_task(mocker, ag_agsmartservice_settings):
    delete_procedure = mocker.patch(
        "camac.agsmartservice.tasks.AGSmartServiceClient.delete_procedure"
    )

    assert tasks.delete_procedure_task("INSTANCEID") is None

    delete_procedure.assert_called_once_with("INSTANCEID")
