import pytest


@pytest.mark.parametrize(
    "config,input,output",
    [
        (
            "kt_bern",
            "/ech/v1/instance/123/",
            "/page/index/instance-resource-id/20074/instance-id/123",
        ),
        (
            "kt_bern",
            "/ech/v1/instance/456/?a=b",
            "/page/index/instance-resource-id/20074/instance-id/456",
        ),
    ],
)
def test_redirect(admin_client, config, settings, input, output):
    settings.APPLICATION = settings.APPLICATIONS[config]
    response = admin_client.get(input)

    assert response.status_code == 302
    assert response.url == output
