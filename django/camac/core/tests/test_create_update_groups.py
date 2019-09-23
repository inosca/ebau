import os

import pytest
from django.core.management import call_command

from camac.user.models import Group, GroupT, Role


@pytest.fixture
def translation_ok(db):
    role_ok = Role.objects.create(name="admin", role_parent_id="")
    group_ok = Group.objects.create(
        name="Leitung",
        phone="",
        zip="",
        city="",
        address="",
        email="",
        website="",
        role_id=role_ok.role_id,
        service_id="",
        disabled=0,
    )
    groupt_ok = GroupT.objects.create(
        language="fr", name="Leitung", city="Trubschachen", group_id=group_ok.group_id
    )
    return groupt_ok


@pytest.fixture
def translation_not_ok(db):
    role_not_ok = Role.objects.create(name="admin", role_parent_id="")
    group_not_ok = Group.objects.create(
        name="",
        phone="",
        zip="",
        city="",
        address="",
        email="",
        website="",
        role_id=role_not_ok.role_id,
        service_id="",
        disabled=0,
    )
    groupt_not_ok = GroupT.objects.create(
        language="de",
        name="Thisdoesnotexist",
        city="Thisdoesnotexist",
        group_id=group_not_ok.group_id,
    )
    return groupt_not_ok


def create_test_file(tmpdir):
    test_file = tmpdir.join("test_update_groups.sql")
    return test_file


def test_translate(translation_ok, translation_not_ok, tmpdir):
    call_command("create_update_groups", create_test_file(tmpdir))
    translations_ok = GroupT.objects.filter(group_id=translation_ok.group_id)
    translations_not_ok = GroupT.objects.filter(group_id=translation_not_ok.group_id)

    assert translation_ok.name == "Leitung"
    with pytest.raises(Exception) as e:
        assert translations_not_ok.name
    assert str(e.value) == "'QuerySet' object has no attribute 'name'"
    call_command("create_update_groups", create_test_file(tmpdir))
    assert translations_ok.get(language="fr").name == "Leitung"
    assert os.path.getsize(create_test_file(tmpdir)) > 0
