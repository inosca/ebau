import io
import os
from datetime import date, datetime, time, timedelta

import openpyxl
from django.conf import settings
from django.http import FileResponse
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView

from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance

from .filters import InstanceFilterBackend, WorkItemFilterBackend


def _resolve_template_path(export_type, role_slug=None, service_group_slug=None):
    """Return the best-matching XLSX template path, or None.

    Priority: service_group > role > type-only default.
    """

    # normalize export_type _ to - to get base of template name
    base_type = export_type.replace("_", "-")

    stats_dir = os.path.join(
        os.path.dirname(__file__),
        "config",
        settings.APPLICATION_NAME,
    )

    candidates = []
    if service_group_slug:
        candidates.append(f"{base_type}_{service_group_slug}.xlsx")
    if role_slug:
        candidates.append(f"{base_type}_{role_slug}.xlsx")
    candidates.append(f"{base_type}_export.xlsx")

    for filename in candidates:
        path = os.path.join(stats_dir, filename)
        if os.path.isfile(path):
            return path

    return None


class _StatisticsExportBaseView(InstanceQuerysetMixin, ListAPIView):
    """Base class for statistics XLSX exports.

    Subclasses set base_type to control which
    columns / filter backend / template are used.

    The first worksheet of the template is filled with the queried data.
    Further worksheets (e.g. pivot tables) are preserved as-is from the
    template file.
    """

    # Overridden by concrete subclasses.
    base_type: str  # e.g. "dossier" or "work-items"

    instance_field = None
    queryset = Instance.objects
    filter_backends = [InstanceFilterBackend]

    def get_queryset_for_public(self):  # pragma: no cover
        return self.queryset.none()

    def _get_columns(self, request):
        """Resolve export columns from the statistics module config.

        Resolution order (first match wins): by_service_group, by_role.
        Raises PermissionDenied if no configuration matches.
        """
        stats_config = settings.STATISTICS
        columns_config = None

        service = getattr(request.group, "service", None)
        sg_slug = getattr(service.service_group, "slug", None) if service else None
        sg_columns = stats_config.by_service_group.get(sg_slug) if sg_slug else None
        if sg_columns:
            columns_config = sg_columns
        else:
            role = getattr(request.group, "role", None)
            role_slug = getattr(role, "slug", None) if role else None
            role_columns = stats_config.by_role.get(role_slug) if role_slug else None
            if role_columns:
                columns_config = role_columns

        if columns_config is None:
            raise PermissionDenied()

        return getattr(columns_config, self.base_type)

    def _get_template(self, request):
        """Resolve the XLSX template for the current export."""
        service = getattr(request.group, "service", None)
        sg_slug = getattr(service.service_group, "slug", None) if service else None
        role = getattr(request.group, "role", None)
        role_slug = getattr(role, "slug", None) if role else None

        return _resolve_template_path(self.base_type, role_slug, sg_slug)

    def _write_data_sheet(self, workbook, header, rows):
        """Clear and rewrite the "Data" sheet with *header* and *rows*."""
        if "Data" in workbook.sheetnames:
            del workbook["Data"]
        data_sheet = workbook.create_sheet("Data", 0)

        bold_font = Font(bold=True)
        col_widths = [0] * len(header)

        for col_idx, value in enumerate(header, start=1):
            cell = data_sheet.cell(row=1, column=col_idx, value=value)
            cell.font = bold_font
            col_widths[col_idx - 1] = len(str(value))

        _NATIVE_TYPES = (str, int, float, bool, datetime, date, time, timedelta)
        _DATE_FORMAT = "DD.MM.YYYY"
        num_cols = len(header)
        for row_idx, row in enumerate(rows, start=2):
            for col_idx, value in enumerate(row):
                if col_idx >= num_cols:
                    break
                if value is not None and not isinstance(value, _NATIVE_TYPES):
                    value = str(value)
                cell = data_sheet.cell(row=row_idx, column=col_idx + 1, value=value)
                if isinstance(value, (date, datetime)):
                    cell.number_format = _DATE_FORMAT
                col_widths[col_idx] = max(col_widths[col_idx], len(str(value or "")))

        for col_idx, width in enumerate(col_widths):
            col_letter = get_column_letter(col_idx + 1)
            data_sheet.column_dimensions[col_letter].width = min(width + 2, 60)

    @staticmethod
    def _set_pivot_refresh(workbook):
        """Set refreshOnLoad on pivot caches (openpyxl private API)."""
        for cache in getattr(workbook, "_pivot_caches", []):
            cache.refreshOnLoad = True

    def _build_workbook(self, header, rows, template_path):
        """Return a BytesIO buffer with the finished XLSX workbook."""
        if template_path and os.path.isfile(template_path):
            workbook = openpyxl.load_workbook(template_path)
        else:
            workbook = openpyxl.Workbook()

        self._write_data_sheet(workbook, header, rows)
        self._set_pivot_refresh(workbook)

        buf = io.BytesIO()
        workbook.save(buf)
        buf.seek(0)
        return buf

    def get(self, request):
        columns = self._get_columns(request)
        backend = self._get_filter_backend()

        annotation_names = [col for col, _ in columns]
        header = [str(label) for _, label in columns]

        queryset = backend.filter_queryset(
            request, self.get_queryset(), set(annotation_names)
        )

        rows = list(queryset.values_list(*annotation_names))

        template_path = self._get_template(request)
        buf = self._build_workbook(header, rows, template_path)

        return FileResponse(
            buf,
            as_attachment=True,
            filename=os.path.basename(template_path)
            if template_path
            else f"{self.base_type.replace('_', '-')}_export.xlsx",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


class DossierStatisticsExportView(_StatisticsExportBaseView):
    """Export one row per matching instance (dossier)."""

    base_type = "dossiers"

    def _get_filter_backend(self):
        return InstanceFilterBackend()


class WorkItemStatisticsExportView(_StatisticsExportBaseView):
    """Export one row per completed work item."""

    base_type = "work_items"

    def _get_filter_backend(self):
        return WorkItemFilterBackend()
