import datetime
import pathlib
import random

import pytest

from camac.gever import apimodels
from camac.gever.client import GEVERClient


@pytest.mark.vcr
@pytest.mark.freeze_time("2025-05-12 15:15:15+02:00")
def test_create_document(be_gever_settings, gever_geschaeft_in_cmi, tmp_path):
    client = GEVERClient()
    # This GUID is know to currently exist. This is just for development,
    # we don't expect this to be around forever

    geschaeft = gever_geschaeft_in_cmi

    folder = apimodels.Ordner(
        titel="2025-0331", guid=None, parent=geschaeft, geschaeft=geschaeft
    )
    folder_create_resp = client.folder.create(folder, raise_on_error=False)
    assert folder_create_resp.status_code <= 201, folder_create_resp.json()

    newdoc = apimodels.Dokument(
        guid=None,
        titel=f"Test Document {datetime.datetime.now().isoformat()}",
        geschaeft=None,
        # geschaeft=geschaeft.ref(),
        geschaeftPosteingangExplorer=folder,
    )

    resp_create_doc = client.document.create(newdoc, raise_on_error=False)
    assert resp_create_doc.status_code <= 201, resp_create_doc.json()

    temp_file = tmp_path / "test_file.dat"
    with temp_file.open("wb") as fh:
        fh.write(random.randbytes(5_000_000))  # ca 5 MB

    test_doc = (
        # from test back up to the main camac code dir
        pathlib.Path(__file__).parent.parent.parent
        / "document/tests/data/important.docx"
    )

    client.document.upload_version(
        newdoc,
        test_doc.open("rb"),
        apimodels.DocStatus.ZWISCHENVERSION,
        comment="asdf",
    )

    refreshed_doc = apimodels.Reference.make_ref(newdoc).resolve(client)

    # Verify the downloaded version matches what we've uploaede
    download_resp = client.document.download(refreshed_doc)

    assert download_resp.content == test_doc.read_bytes()


@pytest.mark.vcr
@pytest.mark.freeze_time("2025-05-12 15:15:15+02:00")
@pytest.mark.parametrize(
    # Note: The "versions" we see in the renditions are not the actual document
    # versions as counted in the API, but just a stupid counter (but as a
    # float ¯\_(ツ)_/¯)
    # This was verified with CMI. Also note that the comment we can send with
    # the checkin is also not available on the API
    "version_modes, expected_versions",
    [
        ([apimodels.DocStatus.ZWISCHENVERSION] * 3, [1.0, 2.0, 3.0]),
        (
            [
                apimodels.DocStatus.ZWISCHENVERSION,
                apimodels.DocStatus.HAUPTVERSION,
                apimodels.DocStatus.SCHLUSSVERSION,
            ],
            [1.0, 2.0, 3.0],
        ),
    ],
)
def test_update_document(
    be_gever_settings, gever_geschaeft_in_cmi, version_modes, expected_versions
):
    client = GEVERClient()
    # This GUID is know to currently exist. This is just for development,
    # we don't expect this to be around forever

    geschaeft = gever_geschaeft_in_cmi

    folder = apimodels.Ordner(
        titel="2025-0331", guid=None, parent=geschaeft, geschaeft=geschaeft
    )
    folder_create_resp = client.folder.create(folder, raise_on_error=False)
    assert folder_create_resp.status_code <= 201, folder_create_resp.json()

    newdoc = apimodels.Dokument(
        guid=None,
        titel=f"Test Document {datetime.datetime.now().isoformat()}",
        geschaeft=None,
        geschaeftPosteingangExplorer=folder,
    )

    resp_create_doc = client.document.create(newdoc, raise_on_error=False)
    assert resp_create_doc.status_code <= 201, resp_create_doc.json()

    testdoc_path = pathlib.Path(__file__).parent.parent.parent / "document/tests/data"

    test_docs = [
        testdoc_path / "important.docx",
        testdoc_path / "multiple-pages.pdf",
        testdoc_path / "libreoffice-template-after-dms.docx",
    ]

    for version_mode, file in zip(version_modes, test_docs):
        client.document.upload_version(
            newdoc,
            file.open("rb"),
            version_mode,
            comment="asdf",
        )
        # Need to fully refresh, so the client can do it's work
        newdoc: apimodels.Dokument = apimodels.Reference.make_ref(newdoc).resolve(
            client
        )

    # The versions will not necessarily be in order
    versions = sorted([rendition.version for rendition in newdoc.eDokument.renditions])

    assert versions == expected_versions
