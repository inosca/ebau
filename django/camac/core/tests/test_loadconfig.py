import json
import os

import pytest
from django.conf import settings
from django.core.management import call_command


@pytest.mark.parametrize("application", settings.APPLICATIONS.keys())
def test_loadconfig(db, settings, application, tmpdir):
    settings.APPLICATION_DIR = settings.ROOT_DIR.path(application)
    settings.APPLICATION_NAME = application
    caluma = settings.APPLICATIONS[application].get("FORM_BACKEND") == "caluma"

    # load data including test data
    call_command(
        "loadconfig",
        caluma=caluma,
        user="test-dummy@adfinis.com",
        stdout=open(os.devnull, "w"),
    )

    # overwrite configuration
    call_command(
        "loadconfig",
        caluma=caluma,
        user="test-dummy@adfinis.com",
        stdout=open(os.devnull, "w"),
    )

    dumped_config = tmpdir.join("config.json")
    dumped_config_caluma_form = tmpdir.join("config-caluma-form.json")
    dumped_config_caluma_workflow = tmpdir.join("config-caluma-workflow.json")

    call_command(
        "dumpconfig",
        caluma=caluma,
        output_caluma_form=str(dumped_config_caluma_form),
        output_caluma_workflow=str(dumped_config_caluma_workflow),
        output=str(dumped_config),
        stdout=open(os.devnull, "w"),
    )

    dumped_data = tmpdir.join("data.json")
    dumped_data_caluma_form = tmpdir.join("data-caluma-form.json")
    dumped_data_caluma_workflow = tmpdir.join("data-caluma-workflow.json")

    call_command(
        "dumpcamacdata",
        caluma=caluma,
        output_caluma_form=str(dumped_data_caluma_form),
        output_caluma_workflow=str(dumped_data_caluma_workflow),
        output=str(dumped_data),
        stdout=open(os.devnull, "w"),
    )

    def sort_fixture(fixture):
        return sorted(fixture, key=lambda k: (k["model"], k["pk"]))

    config = settings.APPLICATION_DIR.file("config.json")
    dumped_config_json = json.loads(dumped_config.read())
    config_json = json.loads(config.read())
    # verify that camac config is still the same
    assert sort_fixture(dumped_config_json) == sort_fixture(config_json)

    data = settings.APPLICATION_DIR.file("data.json")
    dumped_data_json = json.loads(dumped_data.read())
    data_json = json.loads(data.read())
    # verify that camac data is still the same
    assert sort_fixture(dumped_data_json) == sort_fixture(data_json)

    if caluma:
        config_caluma_form = settings.APPLICATION_DIR.file("config-caluma-form.json")
        config_caluma_workflow = settings.APPLICATION_DIR.file(
            "config-caluma-workflow.json"
        )
        dumped_config_caluma_form_json = json.loads(dumped_config_caluma_form.read())
        dumped_config_caluma_workflow_json = json.loads(
            dumped_config_caluma_workflow.read()
        )
        config_caluma_form_json = json.loads(config_caluma_form.read())
        config_caluma_workflow_json = json.loads(config_caluma_workflow.read())
        # verify that caluma config is still the same
        assert sort_fixture(dumped_config_caluma_form_json) == sort_fixture(
            config_caluma_form_json
        )
        assert sort_fixture(dumped_config_caluma_workflow_json) == sort_fixture(
            config_caluma_workflow_json
        )

        data_caluma_form = settings.APPLICATION_DIR.file("data-caluma-form.json")
        dumped_data_caluma_form_json = json.loads(dumped_data_caluma_form.read())
        data_caluma_form_json = json.loads(data_caluma_form.read())
        # verify that caluma data is still the same
        assert sort_fixture(dumped_data_caluma_form_json) == sort_fixture(
            data_caluma_form_json
        )
        data_caluma_workflow = settings.APPLICATION_DIR.file(
            "data-caluma-workflow.json"
        )
        dumped_data_caluma_workflow_json = json.loads(
            dumped_data_caluma_workflow.read()
        )
        data_caluma_workflow_json = json.loads(data_caluma_workflow.read())
        # verify that caluma data is still the same
        assert sort_fixture(dumped_data_caluma_workflow_json) == sort_fixture(
            data_caluma_workflow_json
        )
