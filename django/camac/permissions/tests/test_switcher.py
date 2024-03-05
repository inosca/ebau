import pytest

from .. import switcher


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


def test_permission_modes(permission_mode):
    print((permission_mode))
    pass


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
        (None, False, False, 11),
        (switcher.PERMISSION_MODE.OFF, False, False, 11),
        (switcher.PERMISSION_MODE.CHECKING, True, None, None),
        (switcher.PERMISSION_MODE.LOGGING, False, True, 99),
        (switcher.PERMISSION_MODE.FULL, False, False, 99),
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
            return 99

        @foo.register_old
        def foo_old(self):
            return 11

    thing = TestThingy()

    if expect_error:
        with pytest.raises(RuntimeError) as excinfo:
            thing.foo()
        assert excinfo.match("Permissions module discrepancy in `TestThingy.foo`")
    else:
        warning = (
            "Permissions module discrepancy in `TestThingy.foo`: "
            "OLD says 11, NEW says 99. Returning NEW"
        )
        assert expect_result == thing.foo()
        assert (warning in caplog.messages) == expect_log
