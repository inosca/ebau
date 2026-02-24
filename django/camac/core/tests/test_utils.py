import pytest

from camac.core import utils
from camac.settings.utils import InvalidFixtureUseError


@pytest.mark.freeze_time("2020-10-16")
def test_max_ebau_nr(db, caluma_case_factory, instance_factory, question, chapter):
    assert utils.generate_ebau_nr(None, 2020) == "2020-1"

    caluma_case_factory(meta={"ebau-number": "2020-123"})
    caluma_case_factory(meta={"ebau-number": "2020-99"})
    assert utils.generate_ebau_nr(None, 2020) == "2020-124"

    caluma_case_factory(meta={"ebau-number": "2019-100"})
    assert utils.generate_ebau_nr(None, 2019) == "2019-101"
    assert utils.generate_ebau_nr(None, 2020) == "2020-124"
    assert utils.generate_ebau_nr(None, 2021) == "2021-1"


@pytest.mark.freeze_time("2020-10-16")
def test_assign_ebau_nr(
    db,
    question,
    caluma_case_factory,
    chapter,
    instance_with_case,
    instance_factory,
    caluma_workflow_config_be,
):
    inst = instance_with_case(instance_factory())
    ebau_nr = utils.assign_ebau_nr(inst)

    assert ebau_nr == "2020-1"

    # no double assignment
    assert utils.assign_ebau_nr(inst) == "2020-1"

    # no change of year
    assert utils.assign_ebau_nr(inst, 2019) == "2020-1"

    inst2 = instance_with_case(instance_factory())
    assert utils.assign_ebau_nr(inst2, 2020) == "2020-2"

    inst3 = instance_with_case(instance_factory())
    assert utils.assign_ebau_nr(inst3, 2019) == "2019-1"

    caluma_case_factory(meta={"ebau-number": "2017-420"})
    inst4 = instance_with_case(instance_factory())
    assert utils.assign_ebau_nr(inst4, 2017) == "2017-421"


class FakeClass:
    @utils.canton_aware
    def foo(self):
        return "fallback"

    def foo_be(self):
        return "BE"


@pytest.mark.parametrize(
    "canton,expected",
    [
        ("be", "BE"),
        ("gr", "fallback"),
    ],
)
def test_canton_aware_decorator(db, role, expected, canton, application_settings):
    application_settings["SHORT_NAME"] = canton
    assert FakeClass().foo() == expected


@pytest.mark.freeze_time("2020-10-16")
def test_generate_sort_key(db, caluma_case_factory):
    assert utils.generate_sort_key(utils.generate_ebau_nr(None, 2020)) == 2020000001

    caluma_case_factory(meta={"ebau-number": "2020-123"})
    caluma_case_factory(meta={"ebau-number": "2020-99"})
    assert utils.generate_sort_key(utils.generate_ebau_nr(None, 2020)) == 2020000124

    assert utils.generate_sort_key("2020-999999") == 2020999999
    assert utils.generate_sort_key("KW-07-21-999999") == 721999999
    assert utils.generate_sort_key("1201-2021-13") == 12012021000013


def test_module_settings_fixture_reject_conflicting_fixtures(request):

    # First - generic fixture ("default" entry)
    settings0 = request.getfixturevalue("permissions_settings")

    # Fetch canton-specific fixture
    settings1 = request.getfixturevalue("be_permissions_settings")

    # both settings must be the same object
    assert settings0 is settings1

    # Fetch fixture from same module, different canton. Should fail
    with pytest.raises(InvalidFixtureUseError) as exc:
        request.getfixturevalue("ag_permissions_settings")
    assert exc.match(
        "Requested fixture `ag_permissions_settings` is in conflict with "
        "`be_permissions_settings`. Only one of these is allowed to be "
        "in use at a time"
    )
    with pytest.raises(InvalidFixtureUseError) as exc:
        request.getfixturevalue("disable_permissions_settings")

    assert exc.match(
        "Requested fixture `disable_permissions_settings` is in conflict with "
        "`be_permissions_settings`. Only one of these is allowed to be "
        "in use at a time"
    )
