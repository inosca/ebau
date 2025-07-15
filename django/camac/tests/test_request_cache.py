from camac.request_cache import get_or_set


def test_get_or_set(fake_request, mocker):
    value = 100
    value_factory = mocker.Mock(return_value=999)

    assert not hasattr(fake_request, "test1")
    assert get_or_set(fake_request, "test1", value) == 100
    assert getattr(fake_request, "test1") == 100
    assert get_or_set(fake_request, "test1", "something") == 100

    assert not hasattr(fake_request, "test2")
    assert get_or_set(fake_request, "test2", value_factory) == 999
    assert getattr(fake_request, "test2") == 999
    assert value_factory.call_count == 1
    assert get_or_set(fake_request, "test2", "something") == 999

    get_or_set(fake_request, "test2", value_factory)
    assert value_factory.call_count == 1
