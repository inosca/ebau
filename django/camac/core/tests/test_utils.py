import pytest

from camac.core import utils


@pytest.mark.freeze_time("2020-10-16")
def test_max_ebau_nr(db, case_factory, question, chapter):
    assert utils.generate_ebau_nr(2020) == "2020-1"

    case_factory(meta={"ebau-number": "2020-123"})
    case_factory(meta={"ebau-number": "2020-99"})
    assert utils.generate_ebau_nr(2020) == "2020-124"

    case_factory(meta={"ebau-number": "2019-100"})
    assert utils.generate_ebau_nr(2019) == "2019-101"
    assert utils.generate_ebau_nr(2020) == "2020-124"
    assert utils.generate_ebau_nr(2021) == "2021-1"


@pytest.mark.freeze_time("2020-10-16")
def test_assign_ebau_nr(
    db,
    question,
    case_factory,
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

    case_factory(meta={"ebau-number": "2017-420"})
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
