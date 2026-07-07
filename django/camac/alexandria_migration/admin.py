from django.contrib.admin import ModelAdmin, TabularInline, register
from django.forms import ModelForm

from camac.admin import EbauAdminMixin, ReadOnlyAdminMixin
from camac.alexandria_migration.models import (
    InstanceMigration,
    MigrationLog,
    MigrationRun,
)


class MigrationLogForm(ModelForm):
    class Meta:
        model = MigrationLog
        fields = [
            "instance",
            "type",
            "created_at",
        ]

        read_only_fields = fields


class MigrationRunForm(ModelForm):
    class Meta:
        model = MigrationRun
        fields = []
        read_only_fields = fields


class MigrationInstanceForm(ModelForm):
    class Meta:
        model = InstanceMigration
        fields = ["form", "user", "location"]
        read_only_fields = fields + ["creation_date"]


class MigrationLogInline(ReadOnlyAdminMixin, TabularInline):
    form = MigrationLogForm
    model = MigrationLog

    fields = [
        "created_at",
        "type",
        "source_attachment",
        "target_document",
        "target_file",
    ]


@register(MigrationLog)
class MigrationLogAdmin(ReadOnlyAdminMixin, EbauAdminMixin, ModelAdmin):
    list_display = ["__str__", "id", "instance_id", "type", "created_at"]
    filter_fields = ["instance_id"]

    sortable_by = ["instance_id", "created_at"]

    list_filter = ["type", "run"]

    form = MigrationLogForm


@register(InstanceMigration)
class MigrationInstanceLog(ReadOnlyAdminMixin, EbauAdminMixin, ModelAdmin):
    list_display = [
        "instance_id",
        "dossier_type",
        "old_documents",
        "documents_created",
        "documents_duplicated",
        "communication_links_fixed",
        "num_annotated_thumbnail",
        "num_annotated_fulltext_search",
        "num_annotated_checksum",
    ]
    filter_fields = ["instance_id"]

    list_filter = ["case__document__form__name"]

    form = MigrationInstanceForm
    inlines = [MigrationLogInline]
