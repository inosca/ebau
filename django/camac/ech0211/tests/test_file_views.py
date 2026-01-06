import urllib.parse

import pytest
from alexandria.core.factories import FileFactory
from alexandria.core.models import Document, File
from django.urls import reverse
from rest_framework import status

from camac.document.models import AttachmentSection
from camac.document.tests.data import django_file
from camac.ech0211.models import ECH0211Document


@pytest.mark.parametrize("document_backend", ["camac-ng", "alexandria"])
@pytest.mark.parametrize("role__name", ["Municipality"])
def test_download(
    admin_client,
    file_setup,
    gr_ech0211_settings,
    application_settings,
    reload_ech0211_urls,
    document_backend,
    set_document_backend,
):
    set_document_backend(document_backend)

    # FIXME: Leaky tests - sometimes this is not set as expected, despite the
    # default being "full" and GR using default
    gr_ech0211_settings["API_LEVEL"] = "full"

    visible_file, invisible_file_category, invisible_file_instance = file_setup()

    for file, expected_status in [
        (visible_file, status.HTTP_200_OK),
        (invisible_file_category, status.HTTP_404_NOT_FOUND),
        (invisible_file_instance, status.HTTP_404_NOT_FOUND),
    ]:
        response = admin_client.get(reverse("ech-file-detail", args=[file.pk]))

        assert response.status_code == expected_status

        if response.status_code == status.HTTP_200_OK:
            encoded_filename = urllib.parse.quote(file.name)
            assert (
                response.headers["content-disposition"]
                == f"attachment; filename*=UTF-8''{encoded_filename}"
            )
            assert response.headers["content-type"] == file.mime_type
            assert response.getvalue() == file.content.file.read()


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_upload_disabled_api_level(
    admin_client,
    category_setup,
    gr_ech0211_settings,
    application_settings,
    instance,
    reload_ech0211_urls,
    set_document_backend,
):
    set_document_backend("alexandria")
    gr_ech0211_settings["API_LEVEL"] = "basic"

    _, uploadable_category, __ = category_setup()

    gr_ech0211_settings["ALLOWED_CATEGORIES"] = [uploadable_category.pk]
    gr_ech0211_settings["ALLOWED_ATTACHMENT_SECTIONS"] = [uploadable_category.pk]

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
def test_upload_gr(
    admin_client,
    category_setup,
    gr_ech0211_settings,
    instance,
    mocker,
    application_settings,
    reload_ech0211_urls,
    set_document_backend,
):
    clamav = mocker.patch(
        "camac.ech0211.serializers.validate_file_infection", return_value=None
    )
    set_document_backend("alexandria")

    visible_category, uploadable_category, _ = category_setup()

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
            result = response.json()
            assert result["document-uuid"]
            assert result["file-uuid"]

            file = File.objects.get(pk=result["file-uuid"])
            document = Document.objects.get(pk=result["document-uuid"])

            assert document.category == category
            assert document.files.contains(file)

            # make sure file was scanned by clamav
            clamav.assert_called()

            assert document.title == "multiple-pages.pdf"
            assert document.files.filter(variant=File.Variant.ORIGINAL).count() == 1
            assert document.files.filter(variant=File.Variant.THUMBNAIL).count() == 1


@pytest.mark.parametrize("document_backend", ["camac-ng", "alexandria"])
@pytest.mark.parametrize("role__name", ["Municipality"])
def test_delete_disabled_api_level(
    admin_client,
    category_setup,
    gr_ech0211_settings,
    attachment_attachment_section_factory,
    application_settings,
    instance,
    reload_ech0211_urls,
    document_backend,
    set_document_backend,
):
    set_document_backend(document_backend)

    gr_ech0211_settings["API_LEVEL"] = "basic"

    visible_category, uploadable_category, invisible_category = category_setup()

    factory = {
        "camac-ng": lambda: attachment_attachment_section_factory(
            attachmentsection=uploadable_category,
            attachment__instance=instance,
        ).attachment,
        "alexandria": lambda: FileFactory(
            document__metainfo={"camac-instance-id": str(instance.pk)},
            document__category=uploadable_category,
        ),
    }
    file = factory[document_backend]()

    response = admin_client.delete(
        reverse("ech-file-detail", args=[file.pk]),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("has_remaining_files", [False, True])
@pytest.mark.parametrize(
    ("has_permission", "has_attachment", "expected_status"),
    [
        (True, False, status.HTTP_204_NO_CONTENT),
        (False, False, status.HTTP_403_FORBIDDEN),
        (True, True, status.HTTP_403_FORBIDDEN),
        (False, True, status.HTTP_403_FORBIDDEN),
    ],
)
def test_delete(
    admin_client,
    category_setup,
    communications_attachment_factory,
    has_remaining_files,
    has_attachment,
    has_permission,
    expected_status,
    instance,
    application_settings,
    file_setup,
    gr_ech0211_settings,
    reload_ech0211_urls,
    mocker,
    set_document_backend,
):
    # Testing deletion of eCH0211 documents, potentially with comms
    # attachment. Note: Exactly the same test case as for
    # test_delete_with_comms_attachment_camac(), but we're not parametrizing
    # as the asserts and checks differ too greatly, so we're duplicating the tests.
    # Any meaningful change here must also be replicated in the corresponding
    # "sibling test".

    set_document_backend("alexandria")

    mocker.patch(
        "camac.ech0211.views.has_alexandria_delete_permission",
        return_value=has_permission,
    )

    file = FileFactory(
        document__metainfo={"camac-instance-id": str(instance.pk)},
        document__category=category_setup()[1],
    )
    communications_attachment = (
        communications_attachment_factory(alexandria_file=file)
        if has_attachment
        else None
    )
    extra_file = (
        FileFactory(
            document=file.document,
            variant=File.Variant.ORIGINAL,
        )
        if has_remaining_files
        else None
    )

    document = file.document
    response = admin_client.delete(reverse("ech-file-detail", args=[file.pk]))
    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        if has_remaining_files:
            assert not File.objects.filter(pk=file.pk).exists()
            assert File.objects.filter(pk=extra_file.pk).exists(), (
                "Document and extra file should still exist"
            )
            assert Document.objects.filter(pk=document.pk).exists()
        else:
            assert not File.objects.filter(pk=file.pk).exists()
            assert not Document.objects.filter(pk=document.pk).exists(), (
                "Document should be deleted as well"
            )

    if communications_attachment:
        communications_attachment.delete()


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "has_attachment, has_other_category, expected_status",
    [
        (False, False, status.HTTP_204_NO_CONTENT),
        (True, False, status.HTTP_403_FORBIDDEN),
        (False, True, status.HTTP_204_NO_CONTENT),
        (True, True, status.HTTP_204_NO_CONTENT),
    ],
)
def test_delete_camac(
    admin_client,
    category_setup,
    communications_attachment_factory,
    has_other_category,
    has_attachment,
    expected_status,
    instance,
    application_settings,
    gr_ech0211_settings,
    reload_ech0211_urls,
    file_setup,
    set_document_backend,
):
    # Testing deletion of eCH0211 documents, potentially with comms
    # attachment. Note: Exactly the same test case as for
    # test_delete_with_comms_attachment_camac(), but we're not parametrizing
    # as the asserts and checks differ too greatly, so we're duplicating the tests.
    # Any meaningful change here must also be replicated in the corresponding
    # "sibling test".

    set_document_backend("camac-ng")

    file, invisible_by_category, __ = file_setup()

    # remaining files is not something that exists in the camac-document-module
    # context, so we're not testing for that.

    communications_attachment = (
        communications_attachment_factory(document_attachment=file.attachment)
        if has_attachment
        else None
    )
    if has_other_category:
        file.attachment.attachment_sections.add(
            AttachmentSection.objects.get(pk=invisible_by_category.category.pk)
        )

    response = admin_client.delete(reverse("ech-file-detail", args=[file.pk]))
    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        assert not ECH0211Document.objects.filter(pk=file.pk).exists()

    if communications_attachment:
        communications_attachment.delete()


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "use_file, expected_status",
    [
        ("visible", status.HTTP_204_NO_CONTENT),
        ("hidden_cat", status.HTTP_404_NOT_FOUND),
        ("hidden_inst", status.HTTP_404_NOT_FOUND),
    ],
)
def test_delete_camac_forbidden(
    admin_client,
    category_setup,
    use_file,
    expected_status,
    instance,
    application_settings,
    gr_ech0211_settings,
    reload_ech0211_urls,
    file_setup,
    set_document_backend,
):
    # Testing for correct deletion of ech0211 documents.
    # Especially, deleting of files must be disallowed if the instance
    # is not visible to the client, or the document is in an inaccessible
    # category

    set_document_backend("camac-ng")

    visible_file, invisible_by_category, invisible_by_instance = file_setup()

    files = {
        "visible": visible_file,
        "hidden_cat": invisible_by_category,
        "hidden_inst": invisible_by_instance,
    }

    file = files[use_file]

    # remaining files is not something that exists in the camac-document-module
    # context, so we're not testing for that.

    response = admin_client.delete(reverse("ech-file-detail", args=[file.pk]))
    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        assert not ECH0211Document.objects.filter(pk=visible_file.pk).exists()
