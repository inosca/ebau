import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "use_filter, expect_result",
    [
        ("instance", 1),
        ("none", 1),
        ("other_instance", 0),
        ("search", 1),
        ("other_search", 0),
    ],
)
@pytest.mark.parametrize("document_backend", ["camac-ng", "alexandria"])
@pytest.mark.parametrize("role__name", ["Municipality"])
def test_filters(
    admin_client,
    file_setup,
    gr_ech0211_settings,
    application_settings,
    reload_ech0211_urls,
    instance,
    use_filter,
    expect_result,
    instance_factory,
    document_backend,
    set_document_backend,
):
    set_document_backend(document_backend)

    visible_file, secondary_file, invisible_file_instance = file_setup()

    other_instance = instance_factory()

    filters = {
        "none": {},
        "instance": {"instance": str(instance.pk)},
        "other_instance": {"instance": str(other_instance.pk)},
        "search": {"search": visible_file.name[:3]},
        "other_search": {"search": "hello world"},
    }

    list_url = reverse("ech-document-list")

    # We request all files - but at least the last one is invisible, and we
    # ensure that it's not in the result even though it was requested
    resp = admin_client.get(
        list_url, {**filters.get(use_filter), "page[number]": 1, "page[size]": 10}
    )

    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()["data"]) == expect_result
