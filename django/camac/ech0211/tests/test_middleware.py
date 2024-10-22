import pytest
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

from camac.ech0211.middleware import GeofenceMiddleware


@pytest.mark.vcr()
def test_geofencing(mocker, vcr, gr_ech0211_settings):
    get_response = mocker.stub()
    request = HttpRequest()
    request.META["REMOTE_ADDR"] = "2a02:168:a856:0:618:9d26:5d4c:cc0c"  # Switzerland
    GeofenceMiddleware(get_response=get_response)(request)

    get_response.assert_called_once()
    assert vcr.play_count == 1


@pytest.mark.vcr()
def test_geofencing_disabled(mocker, vcr, gr_ech0211_settings):
    gr_ech0211_settings["GEOFENCE"]["ENABLE"] = False
    get_response = mocker.stub()
    request = HttpRequest()
    request.META["REMOTE_ADDR"] = "2a02:168:a856:0:618:9d26:5d4c:cc0c"  # Switzerland
    GeofenceMiddleware(get_response=get_response)(request)

    get_response.assert_called_once()
    assert vcr.play_count == 0
    gr_ech0211_settings["GEOFENCE"]["ENABLE"] = True


def test_geofencing_no_ip(mocker, gr_ech0211_settings):
    mocker.patch("ipware.get_client_ip", return_value=(None, False))
    request = HttpRequest()
    with pytest.raises(PermissionDenied) as exc:
        GeofenceMiddleware()(request)
    assert "Unable to get the client's IP address" in exc.value.args[0]


@pytest.mark.vcr()
def test_geofencing_wrong_region(vcr, gr_ech0211_settings):
    request = HttpRequest()
    request.META["REMOTE_ADDR"] = "85.214.132.117"  # Germany
    with pytest.raises(PermissionDenied) as exc:
        GeofenceMiddleware()(request)
    assert "Outside of allowed region" in exc.value.args[0]
    assert vcr.play_count == 1


@pytest.mark.vcr()
def test_geofencing_no_api(vcr, mocker, caplog, gr_ech0211_settings):
    get_response = mocker.stub()
    request = HttpRequest()
    request.META["REMOTE_ADDR"] = "85.195.233.243"
    GeofenceMiddleware(get_response=get_response)(request)

    get_response.assert_called_once()
    assert vcr.play_count == 1
    assert (
        "500 Server Error: OK for url: http://www.geoplugin.net/json.gp?ip=85.195.233.243"
        in caplog.text
    )


def test_geofencing_malformed_ip(gr_ech0211_settings):
    request = HttpRequest()
    request.META["REMOTE_ADDR"] = "85,195,233,243"
    with pytest.raises(PermissionDenied) as exc:
        GeofenceMiddleware()(request)
    assert "Unable to get the client's IP address" in exc.value.args[0]
