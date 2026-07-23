"""
Tests for specific migration tooling behaviour for the AnnotateDocumentsMigrator.

These mostly are meant to cover (and verify!) code paths that are
not covered by the end-to-end tests.
"""

import hashlib

import pytest
from alexandria.core import models as alexandria_models
from django.contrib.postgres.search import SearchVector
from django.core.files.base import ContentFile
from django.db.models import Value

from camac.alexandria_migration.domain_logic import annotate_documents


@pytest.mark.parametrize(
    ("checksum_enabled", "already_has_checksum", "expect_checksum"),
    [
        (False, False, False),
        (False, True, True),
        (True, False, True),
        (True, True, True),
    ],
)
@pytest.mark.django_db
def test_set_checksum(
    settings,
    # parametrization
    checksum_enabled,
    already_has_checksum,
    expect_checksum,
):
    settings.ALEXANDRIA_ENABLE_CHECKSUM = checksum_enabled

    content = b"asdf"
    checksum = f"sha256:{hashlib.sha256(content).hexdigest()}"

    # Note: we don't save the file - the annotator modifies the models but does
    # not save them, so we don't have to either
    file = alexandria_models.File(
        content=ContentFile(content, name="somedata.txt"),
        checksum=(checksum if already_has_checksum else None),
    )

    did_checksum = annotate_documents.AnnotateDocumentsMigrator._set_checksum(
        file, content
    )

    if expect_checksum:
        assert did_checksum != already_has_checksum
        assert file.checksum == checksum
    else:
        assert not did_checksum
        assert file.checksum is None


@pytest.mark.parametrize(
    (
        "search_enabled",
        "is_original",
        "has_content_vector",
        "has_content",
        "expected_did_work",
        "expected_vector",
    ),
    [
        # en    orig  cvec   cont  expw  expv
        (True, False, True, True, False, True),
        (True, False, False, True, False, False),
        (True, True, True, True, False, True),
        (True, True, False, True, True, True),
        (True, False, True, False, False, True),
        (True, False, False, False, False, False),
        (True, True, True, False, False, True),
        (True, True, False, False, True, True),
        (False, False, True, True, False, True),
        (False, False, False, True, False, False),
        (False, True, True, True, False, True),
        (False, True, False, True, False, True),
        (False, False, True, False, False, True),
        (False, False, False, False, False, False),
        (False, True, True, False, False, True),
        (False, True, False, False, False, True),
    ],
)
@pytest.mark.django_db
def test_set_content_vector(
    settings,
    mocker,
    # parametrization
    search_enabled,
    is_original,
    has_content_vector,
    has_content,
    expected_did_work,
    expected_vector,
):
    settings.ALEXANDRIA_ENABLE_CONTENT_SEARCH = search_enabled

    content = b"asdf hello world" if has_content else b""

    # tika should not do any real work
    mocker.patch(
        "alexandria.core.tika.TikaClient.get_content_from_buffer",
        return_value=content.decode("utf-8"),
    )

    variant = (
        alexandria_models.File.Variant.ORIGINAL
        if is_original
        else alexandria_models.File.Variant.THUMBNAIL
    )
    vector = SearchVector(Value(content), weight="D")

    # doc needed for getting the title
    doc = alexandria_models.Document(title="Some Data")
    file = alexandria_models.File(
        content=ContentFile(content, name="somedata.txt"),
        variant=variant,
        document=doc,
        name="data.txt",
        content_vector=vector if has_content_vector else None,
    )

    did_work = annotate_documents.AnnotateDocumentsMigrator._set_content_vector(
        file, content
    )

    assert did_work == expected_did_work

    full_vector = "SearchVector(Value('data')) || SearchVector(Value('Some Data')) || SearchVector(Value('')) || SearchVector(Value('asdf hello world'))"

    title_vector = "SearchVector(Value('data')) || SearchVector(Value('Some Data')) || SearchVector(Value(''))"

    exp_vectors = {
        # (did_work, has_content, has_content_vector): resulting vector
        # did work: expecting *something* happened
        (True, False, True): str(vector),
        (True, False, False): title_vector,
        (True, True, True): full_vector,
        (True, True, False): full_vector,
        # did no work: resulting vector is what was in there before
        (False, False, True): str(vector),
        (False, False, False): "None",
        (False, True, True): str(vector),
        (False, True, False): "None",
    }

    if expected_vector:
        # TODO calculate exact expected vector
        expect = exp_vectors[(did_work, has_content, has_content_vector)]
        assert str(file.content_vector) == expect
    else:
        assert file.content_vector is None


@pytest.mark.parametrize(
    ("failure_mode", "expected_result"),
    [
        (FileNotFoundError("Missing"), "Missing"),
        (lambda _: None, "could not get content for file {} (name:data.txt)"),
    ],
)
def test_annotate_without_content(mocker, failure_mode, expected_result):
    content = b""

    file = alexandria_models.File(
        content=ContentFile(content, name="somedata.txt"),
        variant=alexandria_models.File.Variant.ORIGINAL,
        name="data.txt",
    )

    mocker.patch.object(
        annotate_documents.AnnotateDocumentsMigrator,
        "_get_file_content",
        side_effect=failure_mode,
    )

    run = mocker.Mock(pk=1)

    results = annotate_documents.AnnotateDocumentsMigrator.annotate_file(
        file, 123, True, prefix="", run=run
    )

    assert results == {
        "error": expected_result.format(file.pk),
    }
