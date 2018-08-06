import json
import os

import pytest
from django.conf import settings
from django.core.management import call_command


@pytest.mark.parametrize("application", settings.APPLICATIONS.keys())
def test_loadconfig(db, application, settings, tmpdir):
    settings.APPLICATION_DIR = settings.ROOT_DIR.path(application)

    # load data including test data
    call_command("loadconfig", stdout=open(os.devnull, "w"))

    # overwrite configuration
    call_command("loadconfig", stdout=open(os.devnull, "w"))

    dumped_config = tmpdir.join("config.json")
    call_command("dumpconfig", output=str(dumped_config), stdout=open(os.devnull, "w"))

    dumped_data = tmpdir.join("data.json")
    call_command("dumpcamacdata", output=str(dumped_data), stdout=open(os.devnull, "w"))

    def sort_fixture(fixture):
        return sorted(fixture, key=lambda k: (k["model"], k["pk"]))

    config = settings.APPLICATION_DIR.file("config.json")
    dumped_config_json = json.loads(dumped_config.read())
    config_json = json.loads(config.read())
    # verify that load config is still the same
    assert sort_fixture(dumped_config_json) == sort_fixture(config_json)

    data = settings.APPLICATION_DIR.file("data.json")
    dumped_data_json = json.loads(dumped_data.read())
    data_json = json.loads(data.read())
    # verify that camac data is still the same
    assert sort_fixture(dumped_data_json) == sort_fixture(data_json)
