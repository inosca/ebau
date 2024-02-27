import pytest
from alexandria.core.factories import CategoryFactory, FileFactory
from alexandria.core.models import File
from django.urls import reverse
from rest_framework import status

from camac.document.tests.data import django_file


@pytest.fixture
def category_setup(db):
    visible_category = CategoryFactory(
        metainfo={"access": {"Municipality": {"visibility": "all"}}}
    )
    uploadable_category = CategoryFactory(
        metainfo={
            "access": {
                "Municipality": {
                    "visibility": "all",
                    "permissions": [{"permission": "create"}],
                }
            }
        }
    )
    invisible_category = CategoryFactory(
        metainfo={"access": {"Support": {"visibility": "all"}}}
    )

    return visible_category, uploadable_category, invisible_category


@pytest.fixture
def file_setup(category_setup, instance_factory, instance):
    visible_category, _, invisible_category = category_setup

    visible_file = FileFactory(
        name="foo.pdf",
        mime_type="application/pdf",
        document__metainfo={"camac-instance-id": str(instance.pk)},
        document__category=visible_category,
    )
    invisible_file_category = FileFactory(
        document__metainfo={"camac-instance-id": str(instance.pk)},
        document__category=invisible_category,
    )
    invisible_file_instance = FileFactory(
        document__metainfo={"camac-instance-id": str(instance_factory().pk)},
        document__category=visible_category,
    )

    return visible_file, invisible_file_category, invisible_file_instance


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_download_disabled(admin_client, ech0211_settings, file_setup, settings):
    settings.APPLICATION["DOCUMENT_BACKEND"] = "camac-ng"

    visible_file, _, __ = file_setup

    response = admin_client.get(reverse("ech-file-detail", args=[visible_file.pk]))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_download(admin_client, file_setup, gr_ech0211_settings, settings):
    settings.APPLICATION["DOCUMENT_BACKEND"] = "alexandria"

    visible_file, invisible_file_category, invisible_file_instance = file_setup

    for file, expected_status in [
        (visible_file, status.HTTP_200_OK),
        (invisible_file_category, status.HTTP_404_NOT_FOUND),
        (invisible_file_instance, status.HTTP_404_NOT_FOUND),
    ]:
        response = admin_client.get(reverse("ech-file-detail", args=[file.pk]))

        assert response.status_code == expected_status

        if response.status_code == status.HTTP_200_OK:
            assert (
                response.headers["content-disposition"]
                == f'attachment; filename="{file.name}"'
            )
            assert response.headers["content-type"] == file.mime_type


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_upload_disabled_document_backend(
    admin_client, category_setup, gr_ech0211_settings, settings, instance
):
    settings.APPLICATION["DOCUMENT_BACKEND"] = "camac-ng"

    _, uploadable_category, __ = category_setup

    gr_ech0211_settings["ALLOWED_CATEGORIES"] = [uploadable_category.slug]

    response = admin_client.post(
        reverse("ech-file-list"),
        data={
            "instance": instance.pk,
            "category": uploadable_category.pk,
            "content": django_file("multiple-pages.pdf").file,
        },
        format="multipart",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_upload_disabled_api_level(
    admin_client, category_setup, gr_ech0211_settings, settings, instance
):
    settings.APPLICATION["DOCUMENT_BACKEND"] = "alexandria"
    gr_ech0211_settings["API_LEVEL"] = "basic"

    _, uploadable_category, __ = category_setup

    gr_ech0211_settings["ALLOWED_CATEGORIES"] = [uploadable_category.slug]

    response = admin_client.post(
        reverse("ech-file-list"),
        data={
            "instance": instance.pk,
            "category": uploadable_category.pk,
            "content": django_file("multiple-pages.pdf").file,
        },
        format="multipart",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_upload(
    admin_client,
    category_setup,
    gr_ech0211_settings,
    instance,
    mocker,
    settings,
):
    clamav = mocker.patch(
        "camac.ech0211.serializers.validate_file_infection", return_value=None
    )

    settings.APPLICATION["DOCUMENT_BACKEND"] = "alexandria"

    visible_category, uploadable_category, _ = category_setup

    gr_ech0211_settings["ALLOWED_CATEGORIES"] = [
        visible_category.slug,
        uploadable_category.slug,
    ]

    for category, expected_status in [
        (uploadable_category, status.HTTP_201_CREATED),
        (visible_category, status.HTTP_403_FORBIDDEN),
    ]:
        response = admin_client.post(
            reverse("ech-file-list"),
            data={
                "instance": instance.pk,
                "category": category.pk,
                "content": django_file("multiple-pages.pdf").file,
            },
            format="multipart",
        )

        assert response.status_code == expected_status

        if response.status_code == status.HTTP_201_CREATED:
            document = category.documents.first()

            # make sure file was scanned by clamav
            clamav.assert_called()

            assert document.title.translate() == "multiple-pages.pdf"
            assert document.files.filter(variant=File.Variant.ORIGINAL).count() == 1
            assert document.files.filter(variant=File.Variant.THUMBNAIL).count() == 1
