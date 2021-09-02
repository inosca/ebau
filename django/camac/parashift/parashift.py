import io

import requests
from django.conf import settings
from PyPDF2 import PdfFileReader, PdfFileWriter

from camac.constants import kt_uri as uri_constants
from camac.core.import_dossiers import import_dossiers
from camac.utils import build_url

GROUP_KOOR_ARE_BG_ID = 142


class ParashiftValidationError(Exception):
    def __init__(self, msg, original_exception=None):
        super().__init__(msg)
        self.original_exception = original_exception


class ParashiftDataError(Exception):
    pass


class ParashiftImporter:
    """Import dossier from parashift."""

    DATA_URI_FORMAT = build_url(
        settings.PARASHIFT_BASE_URI,
        "/documents/{document_id}/?include="
        "document_fields&extra_fields[document_fields]=extraction_candidates",
    )

    LINK_URI_FORMAT = build_url(
        settings.PARASHIFT_SOURCE_FILES_URI,
        f"{settings.PARASHIFT_TENANT_ID}/documents/{{document_id}}?include=source_files",
    )
    LIST_URI_FORMAT = build_url(
        settings.PARASHIFT_BASE_URI,
        "/documents?filter[id_lte]={to_id}&filter[id_gte]={from_id}",
    )

    schema = {
        "gesuchsteller": None,
        "erfassungsjahr": None,
        "parzelle-nr": None,
        "baurecht-nr": None,
        "gemeinde": None,
        "ort": None,
        "vorhaben": None,
        "parashift-id": None,
        "barcodes": [],
        "document": None,
    }

    post_process = {
        "erfassungsjahr": (
            lambda a: int(a) + 1900 if int(a) > 70 else int(a) + 2000,
            "Must be an integer!",
        ),
        "parzelle-nr": (lambda a: int(a), "Must be an integer!"),
        "baurecht-nr": (lambda a: int(a), "Must be an integer!"),
    }

    @property
    def _record_blueprint(self):
        return dict(self.schema)

    def _get(self, *args, auth=True, **kwargs):
        return self._request(requests.get, *args, auth=auth, **kwargs)

    def _request(self, method, *args, auth=True, **kwargs):
        headers = {}
        if auth:
            headers = {"Authorization": f"Bearer {settings.PARASHIFT_API_KEY}"}

        response = method(*args, **kwargs, headers=headers)
        response.raise_for_status()
        return response

    def crop_pdf(self, record):
        pdf = PdfFileReader(record["document"])

        record["barcodes"].pop(0)
        documents = []
        for index, code in enumerate(record["barcodes"], start=1):
            start = code["page"]
            stop = None
            for c in record["barcodes"]:
                if c["page"] > start:
                    stop = c["page"] - 1
                    break

            if stop is None:
                stop = pdf.numPages - 1

            output = PdfFileWriter()

            for page in range(start, stop + 1):
                output.addPage(pdf.getPage(page))

            bytes_file = io.BytesIO()
            output.write(bytes_file)
            documents.append(
                {
                    "section": uri_constants.PARASHIFT_ATTACHMENT_SECTION_MAPPING[
                        code["type"]
                    ],
                    "name": f"{index}.pdf",
                    "data": bytes_file,
                }
            )
        return documents

    def run(self, from_id, to_id):
        result = self._get(
            self.LIST_URI_FORMAT.format(to_id=to_id, from_id=from_id)
        ).json()

        records = [self.fetch_data(rec["id"]) for rec in result["data"]]

        for record in records:
            record["documents"] = self.crop_pdf(record)

        return import_dossiers(records)

    def _post_process_value(self, identifier, value):
        post_process = self.post_process.get(identifier)

        if post_process is None:
            return value

        try:
            return post_process[0](value)
        except Exception as e:
            raise ParashiftValidationError(
                f"{identifier}: {post_process[1]}",
                original_exception=e,
            )

    def _fetch_document(self, para_id):
        result = self._get(self.LINK_URI_FORMAT.format(document_id=para_id)).json()

        try:
            url = result["included"][0]["attributes"]["url"]
        except (KeyError, IndexError):
            raise ParashiftDataError("Couldn't fetch original PDF.")

        file_resp = self._get(url, auth=False)
        file = io.BytesIO(file_resp.content)

        return file

    def fetch_data(self, para_id):
        json_doc = self._get(self.DATA_URI_FORMAT.format(document_id=para_id)).json()
        record = self._record_blueprint

        record["parashift-id"] = json_doc["data"]["id"]

        for field in json_doc["included"]:
            identifier = field["attributes"]["identifier"]
            value = field["attributes"]["value"]

            if identifier == "barcodes":
                record["barcodes"] = sorted(
                    [
                        {"type": code["extraction_value"], "page": code["page_number"]}
                        for code in field["attributes"]["extraction_candidates"]
                    ],
                    key=lambda k: k["page"],
                )
                record["gemeinde"] = value

                continue

            if identifier not in record or value is None:
                continue

            value = self._post_process_value(identifier, value)

            record[identifier] = value

        record["document"] = self._fetch_document(para_id)

        return record
