from caluma.caluma_form.models import Document
from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.db.models import F

from camac.instance.models import Instance


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--dry", action="store_true", dest="dry")

    @transaction.atomic
    def handle(self, *args, **options):
        tid = transaction.savepoint()

        self.fix_documents_without_family()
        self.delete_instances()
        self.delete_cases()
        self.delete_documents()

        if options.get("dry"):
            transaction.savepoint_rollback(tid)
        else:
            transaction.savepoint_commit(tid)

    def fix_documents_without_family(self):
        documents = Document.objects.filter(family__isnull=True)

        if documents.exists():
            self.stdout.write(f"Add missing family of {documents.count()} documents")
            documents.update(family_id=F("pk"))

    def delete_instances(self):
        ids = list(
            Instance.objects.filter(case__isnull=True).values_list("pk", flat=True)
        )
        self.stdout.write(f"Delete {len(ids)} instances without a case")
        self.delete("INSTANCE", "INSTANCE_ID", ids)

    def delete_cases(self):
        ids = list(
            Case.objects.filter(family__instance__isnull=True).values_list(
                "pk", flat=True
            )
        )
        self.stdout.write(f"Delete {len(ids)} cases without and instance")
        self.delete("caluma_workflow_case", "id", ids)

    def delete_documents(self):
        ids = list(
            Document.objects.exclude(form_id="dashboard")
            .filter(family__case__isnull=True, family__work_item__isnull=True)
            .values_list("pk", flat=True)
        )
        Document.objects.filter(source__in=ids).update(source=None)
        self.stdout.write(f"Delete {len(ids)} documents without an instance")
        self.delete("caluma_form_document", "id", ids)

    def _get_foreign_keys(self, table):
        query = """select kcu.table_name as foreign_table,
                   string_agg(kcu.column_name, ';') as fk_columns
            from information_schema.table_constraints tco
            join information_schema.key_column_usage kcu
                      on tco.constraint_schema = kcu.constraint_schema
                      and tco.constraint_name = kcu.constraint_name
            join information_schema.referential_constraints rco
                      on tco.constraint_schema = rco.constraint_schema
                      and tco.constraint_name = rco.constraint_name
            join information_schema.table_constraints rel_tco
                      on rco.unique_constraint_schema = rel_tco.constraint_schema
                      and rco.unique_constraint_name = rel_tco.constraint_name
            where tco.constraint_type = 'FOREIGN KEY' AND rel_tco.table_name = %s
            group by kcu.table_name;"""
        with connection.cursor() as cursor:
            cursor.execute(query, [table])

            results = []

            for row in cursor.fetchall():
                if row[0] != table:
                    results.extend([row[0], fk] for fk in row[1].split(";"))

            return results

    def delete(self, table, pk, ids):
        if not len(ids):
            return

        with connection.cursor() as cursor:
            for t, fk in self._get_foreign_keys(table):
                cursor.execute(f'DELETE FROM "{t}" WHERE "{fk}" = ANY(%s)', [ids])

            cursor.execute(
                f'DELETE FROM "{table}" WHERE "{pk}" = ANY(%s)',
                [ids],
            )
