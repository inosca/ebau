import pytest

from camac.core import utils


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


def test_tika_does_not_write_own_log():
    """Tika wants to write it's own log file. Ensure our settings disable it.

    Tika uses env variables to configure it's own logging, but we want our
    logging config to take precedence, and most importantly, don't want Tika
    to try starting/writing a logfile in /tmp (which is it's default behaviour).
    """

    # lazy import to avoid test discovery from tripping up
    # the settings - loading order is important here
    from tika import tika

    # If we've successfully disabled tika's own log, it's logfile won't point
    # to that path
    assert tika.log_file != "/tmp/tika.log"
