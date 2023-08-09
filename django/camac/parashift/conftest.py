from pathlib import Path

import pytest
from caluma.caluma_form import factories as caluma_form_factories, models as form_models
from django.conf import settings

from camac.constants import kt_uri as uri_constants
from camac.instance.models import Form, FormState
from camac.parashift.parashift import ParashiftImporter
from camac.utils import build_url

DATA_DIR = Path(settings.ROOT_DIR) / "camac" / "parashift" / "tests" / "data"


@pytest.fixture(params=[True, False])
def parashift_mock(request, requests_mock):
    values = {
        "parzelle-nr": "11",
        "erfassungsjahr": "92",
        "vorhaben": "Erschliessungsstrasse",
        "vorhaben-backup": "Erschliessungsstrasse",
        "nähere ortsbezeichnung": "Platti, Amsteg",
        "ort": "Platti, Amsteg",
        "ort-backup": "Platti, Amsteg",
        "baurecht-nr": None,
        "gesuchsteller": "Kanton Uri, v.d. Baudirektion Uri" if request.param else None,
        "gesuchsteller-backup": "Kanton Uri, v.d. Baudirektion Uri"
        if not request.param
        else None,
    }

    parashift_dossier_data = {
        "data": {
            "id": "138866",
            "attributes": {
                "status": "done",
            },
        },
        "included": [
            {"attributes": {"identifier": i, "value": v}} for i, v in values.items()
        ]
        + [
            {
                "type": "document_fields",
                "attributes": {
                    "identifier": "barcodes",
                    "value": "Gurtnellen 1209",
                    "extraction_candidates": [
                        {"prediction_value": "Gurtnellen 1209", "page_number": 0},
                        {"prediction_value": "Fachstellen", "page_number": 1},
                        {"prediction_value": "Fachstellen", "page_number": 3},
                        {"prediction_value": "Fachstellen", "page_number": 4},
                        {"prediction_value": "Gesuchsteller", "page_number": 6},
                    ],
                },
            },
        ],
    }

    requests_mock.register_uri(
        "GET",
        ParashiftImporter.LIST_URI_FORMAT.format(
            from_id=138866, to_id=138867, page_number=1
        ),
        json={"data": [{"id": "138866", "attributes": {"status": "done"}}]},
    )

    requests_mock.register_uri(
        "GET",
        ParashiftImporter.TOTAL_RECORDS_URI.format(
            from_id=138866, to_id=138867, page_number=1
        ),
        json={
            "data": [{"id": "138866", "attributes": {"status": "done"}}],
            "meta": {"stats": {"total": {"count": 1}}},
        },
    )

    requests_mock.register_uri(
        "GET",
        build_url(
            settings.PARASHIFT["BASE_URI"],
            "/documents/138866/?include="
            "document_fields&extra_fields[document_fields]=extraction_candidates",
        ),
        json=parashift_dossier_data,
    )

    parashift_source_files_data = {
        "data": {
            "id": "138866",
            "attributes": {
                "status": "done",
            },
            "type": "documents",
        },
        "included": [
            {
                "id": "683880",
                "type": "active_storage_attachments",
                "attributes": {
                    "url": "https://storage.googleapis.com/documentcenter-individual-extraction-api/blablabla",
                },
            }
        ],
    }

    requests_mock.register_uri(
        "GET",
        build_url(
            settings.PARASHIFT["BASE_URI"],
            "/documents/138866/?include="
            "document_fields&extra_fields[document_fields]=extraction_candidates",
        ),
        json=parashift_dossier_data,
    )

    parashift_source_files_data = {
        "data": {
            "id": "138866",
            "attributes": {
                "status": "done",
            },
            "type": "documents",
        },
        "included": [
            {
                "id": "683880",
                "type": "active_storage_attachments",
                "attributes": {
                    "url": "https://storage.googleapis.com/documentcenter-individual-extraction-api/blablabla",
                },
            }
        ],
    }

    tenant_id = settings.PARASHIFT["KOOR_BG"]["TENANT_ID"]
    requests_mock.register_uri(
        "GET",
        build_url(
            settings.PARASHIFT["SOURCE_FILES_URI"],
            f"/{tenant_id}/documents/138866?include=source_files",
        ),
        json=parashift_source_files_data,
    )

    requests_mock.register_uri(
        "GET",
        "https://storage.googleapis.com/documentcenter-individual-extraction-api/blablabla",
        content=(DATA_DIR / "dossier.pdf").open("br").read(),
    )


@pytest.fixture()
def parashift_data(
    db,
    admin_user,
    instance_state_factory,
    group_factory,
    location_factory,
    question_factory,
    authority_location_factory,
    caluma_workflow_config_ur,
    attachment_section_factory,
    user_factory,
):
    user_factory(username="import@urec.ch")
    user_factory(username="import.gem@urec.ch")
    instance_state_factory(instance_state_id=25)
    group_factory(group_id=142)
    group_factory(group_id=151)
    location = location_factory(communal_federal_number=1209)
    authority_location_factory(location=location)
    form_models.Form.objects.create(slug="building-permit")
    FormState.objects.create(form_state_id=1, name="Published")
    Form.objects.create(form_id=293, name="Archivdossier", form_state_id=1)

    for id in list(set(uri_constants.PARASHIFT_ATTACHMENT_SECTION_MAPPING.values())):
        attachment_section_factory(pk=id)

    archiv_option = form_models.Option.objects.create(
        slug="form-type-archiv", label="Archivdossier"
    )
    form_models.QuestionOption.objects.create(
        question=form_models.Question.objects.get(slug="form-type"),
        option=archiv_option,
    )

    # Plot
    caluma_form_factories.QuestionFactory(slug="parcels")
    caluma_form_factories.QuestionFactory(slug="parcel-number")
    caluma_form_factories.QuestionFactory(slug="building-law-number")
    caluma_form_factories.FormFactory(slug="parcel-table")

    # Applicant
    caluma_form_factories.QuestionFactory(slug="applicant")
    caluma_form_factories.QuestionFactory(slug="last-name")
    caluma_form_factories.FormFactory(slug="personal-data-table")

    caluma_form_factories.QuestionFactory(slug="proposal-description")
    caluma_form_factories.QuestionFactory(slug="parcel-street")
    caluma_form_factories.QuestionFactory(slug="parzellen-oder-baurechtsnummer")
