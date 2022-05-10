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
    override_urls_be,
    input,
    output,
):
    response = admin_client.get(input)

    assert response.status_code == 302
    assert response.url == output
