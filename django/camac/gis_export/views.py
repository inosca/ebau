from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from django.db import transaction
from django.http import StreamingHttpResponse
from django.utils.timezone import now
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from camac.gis_export.domain_logic import export_so
from camac.gis_export.models import SOGISExport
from camac.gis_export.serializers import export_sogis_xml
from camac.user.permissions import IsSogisClientToken

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Iterator
    from io import BytesIO

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
        SOGISExport.objects.filter(pk__in=pks).update(exported_at=now())
    except Exception as e:  # pragma: no cover
        log.warning("Failed to mark GIS exports as delivered: %s", e)


class ExportSOGISView(APIView):
    permission_classes = [IsSogisClientToken & IsAuthenticated]

    @transaction.atomic
    def get(self, request: Request) -> response.Response | StreamingHttpResponse:
        exports = export_so()

        xml = export_sogis_xml(exports)

        if xml is None:
            return response.Response([], status=status.HTTP_204_NO_CONTENT)

        streaming_response = StreamingHttpResponse(
            _stream_and_mark_exported(xml, [export.pk for export in exports]),
            content_type="application/xml",
        )
        streaming_response["Content-Length"] = str(xml.getbuffer().nbytes)
        streaming_response["Content-Disposition"] = (
            'inline; filename="so_gis_export.xtf"'
        )
        return streaming_response
