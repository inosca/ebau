import json
import os
from glob import glob

import pytest
from django.conf import settings
from django.core.management import call_command


def sort_fixture(fixture, unordered_fields=[]):
    fixture = sorted(fixture, key=lambda k: (k["model"], k["pk"]))

    if not unordered_fields:
        return fixture

    # make lists insensitive to order
    for entry in fixture:
        for field in unordered_fields:
            if field in entry["fields"]:
                entry["fields"][field] = set(entry["fields"][field])

    return fixture


@pytest.mark.parametrize("application", settings.APPLICATIONS.keys())
def test_dump_and_load(db, settings, application, tmpdir):
    settings.APPLICATION_DIR = settings.ROOT_DIR.path(application)
    settings.APPLICATION = settings.APPLICATIONS[application]
    settings.APPLICATION_NAME = application

    # load data including test data
    call_command(
        "camac_load", user="test-dummy@adfinis.com", stdout=open(os.devnull, "w"),
    )

    # overwrite configuration
    call_command(
        "camac_load", user="test-dummy@adfinis.com", stdout=open(os.devnull, "w"),
    )

    for dump_type in ["config", "data"]:
        outdir = tmpdir.join(dump_type)
        outdir.mkdir()

        call_command(
            f"camac_dump_{dump_type}",
            output_dir=str(outdir),
            stdout=open(os.devnull, "w"),
        )

        for filepath in glob(settings.APPLICATION_DIR(f"{dump_type}/*.json")):
            filename = filepath.split("/")[-1]
            test_filepath = os.path.join(outdir, filename)

            with open(test_filepath, "r") as test_dumped, open(filepath, "r") as dumped:
                unordered_fields = (
                    ["allow_forms"] if "caluma_workflow" in filename else []
                )

                test_dumped_json = sort_fixture(
                    json.load(test_dumped), unordered_fields,
                )
                dumped_json = sort_fixture(json.load(dumped), unordered_fields,)

                #  verify that dump is still the same
                assert (
                    test_dumped_json == dumped_json
                ), f"Dumped file '{filename}' does not match '{filepath}'"
