import json
import os

import pytest
from django.conf import settings
from django.core.management import call_command


@pytest.mark.parametrize("application", settings.APPLICATIONS.keys())
def test_loadconfig(db, application, settings, tmpdir):
    settings.APPLICATION_DIR = settings.ROOT_DIR.path(application)

    # load data including test data
    call_command('loadconfig', stdout=open(os.devnull, 'w'))

    # overwrite configuration
    call_command('loadconfig', stdout=open(os.devnull, 'w'))

    dumped_config = tmpdir.join('config.json')
    call_command(
        'dumpconfig',
        output=str(dumped_config),
        stdout=open(os.devnull, 'w')
    )

    def sort_fixture(fixture):
        return sorted(fixture, key=lambda k: (k['model'], k['pk']))

    config = settings.APPLICATION_DIR.file('config.json')
    dumped_json = json.loads(dumped_config.read())
    config_json = json.loads(config.read())
    # verify that load config is still as check in
    assert sort_fixture(dumped_json) == sort_fixture(config_json)
