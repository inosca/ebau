from __future__ import annotations

from io import BytesIO
from logging import getLogger
from typing import TYPE_CHECKING

from django.db import transaction
from django.http import StreamingHttpResponse
from rest_framework import response, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from camac.gis_export.domain_logic import collect_so_exports
from camac.gis_export.formatters import build_sogis_transfer_xml
from camac.gis_export.models import SOGISExport
from camac.settings.utils import is_module_enabled
from camac.user.permissions import IsSogisClientToken

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Iterator

    from rest_framework.request import Request

log = getLogger(__name__)


def _stream_and_mark_exported(
    buffer: BytesIO, pks: list[int], chunk_size: int = 8192
) -> Iterator[bytes]:
    """Stream the XTF, then mark the exported rows as delivered."""
    try:
        while chunk := buffer.read(chunk_size):
            yield chunk
    finally:
        buffer.close()

    try:
        SOGISExport.objects.mark_exported(pks)
    except Exception as e:  # pragma: no cover
        log.error("Failed to mark GIS exports as delivered: %s", e)


class ExportSOGISView(APIView):
    permission_classes = [IsSogisClientToken & IsAuthenticated]

    @transaction.atomic
    def get(self, request: Request) -> response.Response | StreamingHttpResponse:
        if not is_module_enabled("GIS_EXPORT"):
            raise NotFound

        exports = collect_so_exports()
        transfer = build_sogis_transfer_xml(exports)

        if transfer.errors:
            log.error(
                "Skipped %d invalid GIS export(s), retrying on the next run:\n%s",
                len(transfer.errors),
                "\n".join(str(error) for error in transfer.errors),
            )

        if not transfer.exported:
            return response.Response([], status=status.HTTP_204_NO_CONTENT)

        buffer = BytesIO(transfer.xml.encode("utf-8"))
        exported_pks = [export.pk for export in transfer.exported]
        content_length = buffer.getbuffer().nbytes

        streaming_response = StreamingHttpResponse(
            _stream_and_mark_exported(buffer, exported_pks),
            content_type="application/xml",
        )
        streaming_response["Content-Length"] = str(content_length)
        streaming_response["Content-Disposition"] = (
            'inline; filename="so_gis_export.xtf"'
        )

        return streaming_response
