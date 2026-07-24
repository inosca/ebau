from django.contrib.admin import ModelAdmin, SimpleListFilter, TabularInline, register
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
            "success",
            "created_at",
            "info",
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
        fields = [
            "instance_id",
            "form",
            "identifier",
        ]


class MigrationLogInline(ReadOnlyAdminMixin, TabularInline):
    form = MigrationLogForm
    model = MigrationLog

    fields = [
        "created_at",
        "type",
        "success",
        "source_attachment",
        "target_document",
        "target_file",
        "info",
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .exclude(type__in=MigrationLog.Type.instance_types())
        )


class LogScopeFilter(SimpleListFilter):
    title = "Log scope"
    parameter_name = "scope"

    def lookups(self, request, model_admin):
        return (
            ("file", "Per-file logs"),
            ("instance", "Per-instance logs"),
            ("all", "Show all logs"),
        )

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == lookup,
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}
                ),
                "display": title,
            }

    def queryset(self, request, queryset):
        val = self.value()
        if val == "instance":
            return queryset.filter(type__in=MigrationLog.Type.instance_types())
        if val == "all":
            return queryset
        # "file" or None
        return queryset.exclude(type__in=MigrationLog.Type.instance_types())

    def value(self):
        val = super().value()
        if val is None:
            return "file"
        return val


@register(MigrationLog)
class MigrationLogAdmin(ReadOnlyAdminMixin, EbauAdminMixin, ModelAdmin):
    list_display = ["__str__", "instance_id", "type", "success", "created_at"]
    list_select_related = ["target_file", "target_document"]
    search_fields = ["instance__pk", "instance__identifier"]

    sortable_by = ["instance_id", "created_at"]

    list_filter = [LogScopeFilter, "type", "run", "success"]

    form = MigrationLogForm


class HasAnnotationErrorsFilter(SimpleListFilter):
    title = "Has annotation errors"
    parameter_name = "has_errors"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(num_annotation_failed_logs__gt=0)
        if self.value() == "no":
            return queryset.filter(num_annotation_failed_logs=0)
        return queryset


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
        "annotation_errors",
    ]
    search_fields = ["pk", "identifier"]

    list_filter = ["case__document__form__name", HasAnnotationErrorsFilter]

    def get_readonly_fields(self, request, obj=None):
        return list(self.form.Meta.fields) + [
            "has_documents_created",
            "has_documents_duplicated",
            "has_communication_links_fixed",
            "has_annotated",
        ]

    def get_fields(self, request, obj=None):
        return self.get_readonly_fields(request, obj)

    form = MigrationInstanceForm
    inlines = [MigrationLogInline]
