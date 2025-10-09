import pytest

from .. import switcher
from ..switcher import PERMISSION_MODE, is_permission_module_fully_enabled


@pytest.fixture(
    params=[
        None,  # to test fallback behaviour
        switcher.PERMISSION_MODE.OFF,
        switcher.PERMISSION_MODE.CHECKING,
        switcher.PERMISSION_MODE.LOGGING,
        switcher.PERMISSION_MODE.FULL,
    ]
)
def permission_mode(permissions_settings, request):
    """Parametrized to run once with every permissions mode available."""
    permissions_settings["PERMISSION_MODE"] = request.param
    return request.param


def test_permission_method(permissions_settings, permission_mode):
    class TestThingy:
        foo = switcher.permission_switching_method()

        @foo.register_old
        def foo_old(self):
            return 99

        @foo.register_new
        def foo_new(self):
            return 99

    thing = TestThingy()

    with pytest.raises(RuntimeError) as excinfo:
        thing.foo_old()

    assert excinfo.match(
        "`TestThingy.foo_old` is a permission switcher method. "
        "Call `TestThingy.foo` instead"
    )
    with pytest.raises(RuntimeError) as excinfo:
        thing.foo_new()
    assert excinfo.match(
        "`TestThingy.foo_new` is a permission switcher method. "
        "Call `TestThingy.foo` instead"
    )

    # Whatever the config, it should always return the same
    assert thing.foo() == 99


@pytest.mark.parametrize(
    "mode, expect_error, expect_log, expect_result",
    [
        (None, False, False, "oldvalue"),
        (PERMISSION_MODE.OFF, False, False, "oldvalue"),
        (PERMISSION_MODE.CHECKING, True, None, None),
        (PERMISSION_MODE.LOGGING, False, True, "oldvalue"),
        (PERMISSION_MODE.FULL, False, False, "newvalue"),
        (PERMISSION_MODE.DEV, False, True, "newvalue"),
    ],
)
def test_permission_mismatch(
    caplog, mode, permissions_settings, expect_error, expect_log, expect_result
):
    permissions_settings["PERMISSION_MODE"] = mode

    class TestThingy:
        # Here we at the same time test the "decorator" variant of the
        # permission switching method
        @switcher.permission_switching_method
        def foo(self):
            return "newvalue"

        @foo.register_old
        def foo_old(self):
            return "oldvalue"

    thing = TestThingy()

    if expect_error:
        with pytest.raises(RuntimeError) as excinfo:
            thing.foo()
        assert excinfo.match("Permissions module discrepancy in `TestThingy.foo`")
    else:
        value_name = "NEW" if expect_result == "newvalue" else "OLD"
        warning = (
            "Permissions module discrepancy in `TestThingy.foo`: "
            f"OLD says oldvalue, NEW says newvalue. Returning {value_name}"
        )
        assert expect_result == thing.foo()
        assert (warning in caplog.messages) == expect_log


@pytest.mark.parametrize("as_string", [True, False])
@pytest.mark.parametrize(
    "env, mode, expected_out",
    [
        ("development", PERMISSION_MODE.FULL, PERMISSION_MODE.FULL),
        ("development", PERMISSION_MODE.CHECKING, PERMISSION_MODE.CHECKING),
        ("development", PERMISSION_MODE.LOGGING, PERMISSION_MODE.LOGGING),
        ("development", PERMISSION_MODE.DEV, PERMISSION_MODE.DEV),
        ("development", PERMISSION_MODE.OFF, PERMISSION_MODE.OFF),
        ("development", PERMISSION_MODE.AUTO_ON, PERMISSION_MODE.CHECKING),
        ("production", PERMISSION_MODE.AUTO_ON, PERMISSION_MODE.LOGGING),
        ("development", PERMISSION_MODE.AUTO_OFF, PERMISSION_MODE.LOGGING),
        ("production", PERMISSION_MODE.AUTO_OFF, PERMISSION_MODE.OFF),
    ],
)
def test_get_permission_mode(
    settings, permissions_settings, env, mode, as_string, expected_out
):
    if as_string:
        mode = mode.value

    permissions_settings["PERMISSION_MODE"] = mode
    settings.ENV = env

    output = switcher.get_permission_mode()
    assert output == expected_out


@pytest.mark.parametrize(
    "use_permissions_module, expect_result",
    [
        (False, "oldvalue"),
        (True, "newvalue"),
    ],
)
def test_permissions_switcher_call_new_variant(
    permissions_settings,
    use_permissions_module,
    expect_result,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF

    class TestThingy:
        @switcher.permission_switching_method
        def foo(self):
            return "newvalue"

        @foo.register_old
        def foo_old(self):
            if use_permissions_module:
                return self.foo.call_new_variant(self)

            return "oldvalue"

    thing = TestThingy()
    assert expect_result == thing.foo()


@pytest.mark.parametrize(
    "role__name, config, expect_result",
    [
        (None, [], "oldvalue"),
        ("Applicant", [], "oldvalue"),
        ("Municipality", [], "oldvalue"),
        ("Applicant", ["applicant"], "newvalue"),
        ("Municipality", ["applicant"], "oldvalue"),
        ("Municipality", ["municipality"], "newvalue"),
    ],
)
def test_permissions_switcher_role_based(
    db,
    fake_request,
    permissions_settings,
    role,
    config,
    expect_result,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF
    permissions_settings["MIGRATED_ROLE_PERMISSIONS"] = config

    class TestThingy:
        request = fake_request if role.name else None

        @switcher.permission_switching_method
        def foo(self):
            return "newvalue"

        @foo.register_old
        def foo_old(self):
            return "oldvalue"

    thing = TestThingy()
    assert expect_result == thing.foo()


@pytest.mark.parametrize(
    "role__name, mode, config, expected_result",
    [
        ("Applicant", PERMISSION_MODE.FULL, [], True),
        ("Applicant", PERMISSION_MODE.OFF, [], False),
        ("Municipality", PERMISSION_MODE.FULL, [], True),
        ("Municipality", PERMISSION_MODE.OFF, [], False),
        ("Applicant", PERMISSION_MODE.FULL, ["municipality"], True),
        ("Applicant", PERMISSION_MODE.OFF, ["applicant"], True),
        ("Municipality", PERMISSION_MODE.OFF, ["applicant"], False),
        ("Municipality", PERMISSION_MODE.OFF, ["municipality"], True),
    ],
)
def test_permission_module_fully_enabled(
    db,
    group,
    permissions_settings,
    mode,
    config,
    expected_result,
):
    permissions_settings["PERMISSION_MODE"] = mode
    permissions_settings["MIGRATED_ROLE_PERMISSIONS"] = config

    assert is_permission_module_fully_enabled(group) == expected_result
