import json
import os
from glob import glob

import pytest
from django.conf import settings
from django.core.management import call_command


@pytest.mark.parametrize("application", settings.APPLICATIONS.keys())
@pytest.mark.parametrize("dump_type", ["data", "config"])
def test_dump_and_load(db, settings, application, dump_type, tmp_path):
    settings.APPLICATION_DIR = settings.ROOT_DIR.path(application)
    settings.APPLICATION = settings.APPLICATIONS[application]
    settings.APPLICATION_NAME = application

    # load data including test data
    call_command(
        "camac_load",
        user="test-dummy@adfinis.com",
        stdout=open(os.devnull, "w"),
    )

    # overwrite configuration
    call_command(
        "camac_load",
        user="test-dummy@adfinis.com",
        stdout=open(os.devnull, "w"),
    )
    outdir = tmp_path / dump_type
    outdir.mkdir()

    call_command(
        f"camac_dump_{dump_type}",
        output_dir=str(outdir),
        stdout=open(os.devnull, "w"),
    )

    for filepath in glob(settings.APPLICATION_DIR(f"{dump_type}/*.json")):
        filename = filepath.split("/")[-1]
        test_filepath = outdir / filename

        with open(test_filepath, "r") as test_dumped, open(filepath, "r") as dumped:
            #  verify that dump is still the same
            assert json.load(test_dumped) == json.load(
                dumped
            ), f"Dumped file '{filename}' does not match '{filepath}'"
