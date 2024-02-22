import pytest


@pytest.mark.parametrize(
    "input,output",
    [
        (
            "/ech/v1/instance/123/",
            "/page/index/instance-resource-id/20074/instance-id/123",
        ),
        (
            "/ech/v1/instance/456/?a=b",
            "/page/index/instance-resource-id/20074/instance-id/456",
        ),
    ],
)
def test_redirect(
    admin_client,
    set_application_be,
    be_ech0211_settings,
    input,
    output,
    reload_ech0211_urls,
):
    response = admin_client.get(input)

    assert response.status_code == 302
    assert response.url == output
