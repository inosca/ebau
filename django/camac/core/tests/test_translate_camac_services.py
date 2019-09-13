import os

import pytest
from django.core.management import call_command

from camac.user.models import Service, ServiceGroup, ServiceT


@pytest.fixture
def translation_ok(db):
    service_group_ok = ServiceGroup.objects.create(name="")
    service_ok = Service.objects.create(
        name="",
        description="",
        sort=0,
        phone="",
        zip="",
        city="",
        address="",
        email="",
        website="",
        service_group_id=service_group_ok.service_group_id,
        service_parent_id="",
        disabled=0,
        notification=0,
    )
    servicet_ok = ServiceT.objects.create(
        language="de",
        name="Test",
        description="Test",
        city="Trubschachen",
        service_id=service_ok.service_id,
    )
    return servicet_ok


@pytest.fixture
def translation_not_ok(db):
    service_group_not_ok = ServiceGroup.objects.create(name="")
    service_not_ok = Service.objects.create(
        name="",
        description="",
        sort=0,
        phone="",
        zip="",
        city="",
        address="",
        email="",
        website="",
        service_group_id=service_group_not_ok.service_group_id,
        service_parent_id="",
        disabled=0,
        notification=0,
    )
    servicet_not_ok = ServiceT.objects.create(
        language="de",
        name="Thisdoesnotexist",
        description="Thisdoesnotexist",
        city="Thisdoesnotexist",
        service_id=service_not_ok.service_id,
    )
    return servicet_not_ok


def create_test_file(tmpdir):
    test_file = tmpdir.join("test_insert_services.sql")
    return test_file


def test_translate(translation_ok, translation_not_ok, tmpdir):
    call_command("translate_camac_services", create_test_file(tmpdir))
    translations_ok = ServiceT.objects.filter(service_id=translation_ok.service_id)
    translations_not_ok = ServiceT.objects.filter(
        service_id=translation_not_ok.service_id
    )

    assert translation_ok.name == "Test"
    with pytest.raises(Exception) as e:
        assert translations_not_ok.name
    assert str(e.value) == "'QuerySet' object has no attribute 'name'"
    call_command("translate_camac_services", create_test_file(tmpdir))
    assert translations_ok.get(language="de").name == "Test"
    assert os.path.getsize(create_test_file(tmpdir)) > 0
