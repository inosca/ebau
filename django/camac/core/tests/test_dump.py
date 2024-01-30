import json
import os
from glob import glob
from uuid import uuid4

import pytest
from django.conf import settings
from django.core.management import call_command

from camac.core.models import Resource


@pytest.mark.parametrize("application", settings.APPLICATIONS.keys())
def test_dump_and_load(db, application, request, resource_factory, settings, tmp_path):
    short_name = settings.APPLICATIONS[application]["SHORT_NAME"]
    request.getfixturevalue(f"{short_name}_dump_settings")

    settings.APPLICATION_DIR = settings.ROOT_DIR.path(application)

    uuid = uuid4()
    resource_factory(name=uuid)
    assert Resource.objects.filter(name=uuid).exists()

    # load config including test data
    call_command(
        "camac_load",
        user="test-dummy@adfinis.com",
        stdout=open(os.devnull, "w"),
    )

    # make sure pure config models are flushed
    assert not Resource.objects.filter(name=uuid).exists()

    for dump_type in ["config", "data"]:
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
