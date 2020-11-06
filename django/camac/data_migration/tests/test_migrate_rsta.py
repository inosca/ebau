from pathlib import Path

import pytest

# from caluma.caluma_form import models as form_models
from django.core.management import call_command

from camac.constants.kt_bern import CHAPTER_EBAU_NR, QUESTION_EBAU_NR
from camac.user.models import Service

# from camac.instance.models import Instance


data_dir = Path(__file__).resolve().parent / "rsta_data"


@pytest.fixture
def setup_rsta(
    db,
    caluma_config_bern,
    instance_state_factory,
    form_factory,
    service_t_factory,
    camac_question_factory,
    camac_chapter_factory,
    group_factory,
    role_t_factory,
    settings,
):
    settings.APPLICATION["IS_MULTILINGUAL"] = True
    call_command("loaddata", settings.ROOT_DIR("kt_bern/config/user.json"))
    call_command("loaddata", settings.ROOT_DIR("kt_bern/data/user.json"))
    form_factory(form_id=1)
    camac_question_factory(question_id=QUESTION_EBAU_NR)
    camac_chapter_factory(chapter_id=CHAPTER_EBAU_NR)
    instance_state_factory(name="in_progress")
    instance_state_factory(name="finished")

    Service.objects.all().update(disabled=0)

    # user_factory(username="service-account-camac-admin")
    # service = service_t_factory(
    #     name="Leitbehörde Wangen an der Aare",
    #     service__service_group__name="municipality",
    # ).service
    # role = role_t_factory(name="Leitung Leitbehörde").role
    # group_factory(service=service, role=role)


@pytest.mark.parametrize(
    "filename,ebaunr",
    [
        # ("2020-10-12_15-14_410_1039488 bom.json", "bar"),
        ("2020-10-12_15-15_610_1039414.json", ""),
    ],
)
def test_migrate_rsta_command(
    setup_rsta,
    filename,
    ebaunr,
):
    call_command("migrate_rsta", data_dir)

    # assert Instance.objects.get()
