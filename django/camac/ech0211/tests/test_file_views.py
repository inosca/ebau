import re
import urllib.parse
import zipfile
from io import BytesIO

import pytest
from alexandria.core.factories import FileFactory
from alexandria.core.models import Document, File
from django.urls import reverse
from rest_framework import status

from camac.document.models import Attachment, AttachmentSection
from camac.document.tests.data import django_file
from camac.ech0211.models import ECH0211Document
from camac.settings.modules.ech0211 import DocumentAPIFeature


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


@pytest.mark.parametrize("document_backend", ["camac-ng", "alexandria"])
@pytest.mark.parametrize("role__name", ["Municipality"])
def test_download_multi(
    admin_client,
    file_setup,
    gr_ech0211_settings,
    application_settings,
    reload_ech0211_urls,
    document_backend,
    set_document_backend,
):
    set_document_backend(document_backend)

    visible_file, secondary_file, invisible_file_instance = file_setup()

    # We want to test multi-file download, and also we're not testing
    # the file visibility here. Therefore the secondary_file, being
    # "invisible-by-category", is now moved to the visible file's category
    if document_backend == "camac-ng":
        secondary_file.attachment.attachment_sections.set(
            visible_file.attachment.attachment_sections.all()
        )
        # This does not suffice however, as it's now in another category,
        # we need to fetch it again..
        secondary_file = ECH0211Document.objects.get(
            category=visible_file.category, attachment=secondary_file.attachment
        )
    else:
        secondary_file.document.category = visible_file.document.category
        secondary_file.document.save()

    all_files = visible_file, secondary_file, invisible_file_instance

    download_url = reverse("ech-file-multi-download")

    # First: Check if ?ids=... is enforced
    resp_no_ids = admin_client.get(download_url)
    assert resp_no_ids.status_code == status.HTTP_400_BAD_REQUEST
    assert resp_no_ids.json() == [
        "Multi Download is only allowed when passing ?ids=..."
    ]

    # We request all files - but at least the last one is invisible, and we
    # ensure that it's not in the result even though it was requested
    resp = admin_client.get(
        download_url, {"ids": ",".join([str(f.pk) for f in all_files])}
    )

    assert resp.status_code == status.HTTP_200_OK

    data = BytesIO(b"".join(resp.streaming_content))

    with zipfile.ZipFile(data, "r") as archive:
        # the download prefixes the files with numbers to avoid any duplication
        # by filename. We un-prefix them here, as we know our example files
        # don't clash
        stripped_names = [
            re.sub(r"^\d+-", "", file.filename) for file in archive.filelist
        ]

        assert sorted(stripped_names) == sorted(
            [visible_file.name, secondary_file.name]
        )


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

    gr_ech0211_settings["DOCUMENT_API_FEATURES"].remove(DocumentAPIFeature.FILES_DELETE)

    visible_category, uploadable_category, invisible_category = category_setup()

    factory = {
        "camac-ng": lambda: (
            attachment_attachment_section_factory(
                attachmentsection=uploadable_category,
                attachment__instance=instance,
            ).attachment
        ),
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
@pytest.mark.parametrize("document_backend", ["camac-ng", "alexandria"])
def test_upload_switching(
    admin_client,
    category_setup,
    be_instance,
    mocker,
    application_settings,
    set_document_backend,
    ech0211_settings,
    disable_alexandria_features,
    document_backend,
):
    set_document_backend(document_backend)

    visible_category, uploadable_category, _ = category_setup()

    # clamav is not being tested here
    mocker.patch("camac.ech0211.serializers.validate_file_infection", return_value=None)

    ech0211_settings["DOCUMENT_API_FEATURES"] = [DocumentAPIFeature.FILES_UPLOAD]

    allowed_cats = [
        uploadable_category.pk,
        visible_category.pk,
    ]
    ech0211_settings["ALLOWED_ATTACHMENT_SECTIONS"] = allowed_cats
    ech0211_settings["ALLOWED_CATEGORIES"] = allowed_cats

    for category, expected_status in [
        (uploadable_category, status.HTTP_201_CREATED),
        (visible_category, status.HTTP_403_FORBIDDEN),
    ]:
        response = admin_client.post(
            reverse("ech-file-list"),
            data={
                "instance": be_instance.pk,
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

            if document_backend == "alexandria":
                assert Document.objects.filter(pk=result["document-uuid"]).exists()
                assert File.objects.filter(pk=result["file-uuid"]).exists()
            elif document_backend == "camac-ng":
                # in this case, document and file are actually the same object, but
                # we need to persist API consistency
                assert Attachment.objects.filter(uuid=result["file-uuid"]).exists()
                assert Attachment.objects.filter(uuid=result["document-uuid"]).exists()


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("document_backend", ["camac-ng", "alexandria"])
def test_upload_disabled_api_level(
    admin_client,
    category_setup,
    be_instance,
    mocker,
    application_settings,
    set_document_backend,
    ech0211_settings,
    disable_alexandria_features,
    document_backend,
):
    set_document_backend(document_backend)

    visible_category, uploadable_category, _ = category_setup()

    allowed_cats = [
        uploadable_category.pk,
        visible_category.pk,
    ]
    ech0211_settings["DOCUMENT_API_FEATURES"] = []  # disable all features
    ech0211_settings["ALLOWED_ATTACHMENT_SECTIONS"] = allowed_cats
    ech0211_settings["ALLOWED_CATEGORIES"] = allowed_cats

    for category in [uploadable_category, visible_category]:
        response = admin_client.post(
            reverse("ech-file-list"),
            data={
                "instance": be_instance.pk,
                "category": category.pk,
                "content": django_file("multiple-pages.pdf").file,
            },
            format="multipart",
        )

        # API disabled, this should result in a 404
        assert response.status_code == status.HTTP_404_NOT_FOUND
