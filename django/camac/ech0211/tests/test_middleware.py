import pytest
from django.http import HttpRequest

from camac.ech0211.middleware import GeofenceMiddleware


@pytest.mark.vcr()
def test_geofencing(vcr, gr_ech0211_settings):
    request = HttpRequest()
    request.META["REMOTE_ADDR"] = "2a02:168:a856:0:618:9d26:5d4c:cc0c"  # Switzerland
    view = type("View", (), {"request": request})
    response = GeofenceMiddleware(None).process_view(view, None, None, None)

    assert vcr.play_count == 1
    assert response is None


@pytest.mark.vcr()
def test_geofencing_disabled(vcr, gr_ech0211_settings):
    gr_ech0211_settings["GEOFENCE"]["ENABLE"] = False
    request = HttpRequest()
    request.META["REMOTE_ADDR"] = "2a02:168:a856:0:618:9d26:5d4c:cc0c"  # Switzerland
    view = type("View", (), {"request": request})
    response = GeofenceMiddleware(None).process_view(view, None, None, None)

    assert vcr.play_count == 0
    assert response is None
    gr_ech0211_settings["GEOFENCE"]["ENABLE"] = True


def test_geofencing_no_ip(mocker, gr_ech0211_settings):
    mocker.patch("ipware.get_client_ip", return_value=(None, False))
    request = HttpRequest()
    view = type("View", (), {"request": request})
    response = GeofenceMiddleware(None).process_view(view, None, None, None)
    assert "Unable to get the client's IP address" in response.content.decode()


@pytest.mark.vcr()
def test_geofencing_wrong_region(vcr, gr_ech0211_settings):
    request = HttpRequest()
    request.META["REMOTE_ADDR"] = "85.214.132.117"  # Germany
    view = type("View", (), {"request": request})
    response = GeofenceMiddleware(None).process_view(view, None, None, None)
    assert "Outside of allowed region" in response.content.decode()
    assert vcr.play_count == 1


@pytest.mark.vcr()
def test_geofencing_no_api(vcr, caplog, gr_ech0211_settings):
    request = HttpRequest()
    request.META["REMOTE_ADDR"] = "85.195.233.243"
    view = type("View", (), {"request": request})
    response = GeofenceMiddleware(None).process_view(view, None, None, None)

    assert response is None
    assert vcr.play_count == 1
    assert (
        "500 Server Error: OK for url: http://www.geoplugin.net/json.gp?ip=85.195.233.243"
        in caplog.text
    )


def test_geofencing_malformed_ip(gr_ech0211_settings):
    request = HttpRequest()
    request.META["REMOTE_ADDR"] = "85,195,233,243"
    view = type("View", (), {"request": request})
    response = GeofenceMiddleware(None).process_view(view, None, None, None)
    assert "Unable to get the client's IP address" in response.content.decode()
