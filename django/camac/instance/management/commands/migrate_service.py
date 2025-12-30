from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection

from camac.caluma.extensions import data_sources
from camac.instance.master_data import MasterData


class Command(BaseCommand):
    help = "Moves all responsibilities from source service to target service"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--source",
            type=str,
            dest="source",
            help="Source service PKs (comma-separated)",
            required=True,
        )
        parser.add_argument(
            "-t",
            "--target",
            type=int,
            dest="target",
            help="Target service PK",
            required=True,
        )
        parser.add_argument(
            "-e",
            "--execute",
            default=False,
            dest="exec",
            action="store_true",
            help="Directly execute the query instead of just printing it",
        )
        parser.add_argument(
            "-d",
            "--disable",
            default=False,
            dest="disable",
            action="store_true",
            help="Disable 'source' services",
        )
        parser.add_argument(
            "-fa",
            "--form-answer",
            default=False,
            dest="form_answer",
            action="store_true",
            help="Migrate the form answer for the municipality as well",
        )
        parser.add_argument(
            "-l",
            "--log-to-case-meta",
            default=True,
            dest="log_to_case_meta",
            action="store_true",
            help="Log to the meta of all cases where the lead authority is migrated (for future reference).",
        )

    @staticmethod
    def _get_all_service_foreign_keys():
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
            where tco.constraint_type = 'FOREIGN KEY' AND rel_tco.table_name = 'SERVICE'
            group by kcu.table_name;"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            return [row for row in cursor.fetchall()]

    def _get_queries(self, table, column, source, target):
        if table == "rulesets_responsibleuserrule_municipalities":
            # this table has a composite unique constraint, which needs special
            # "only create if doesn't exist already" semantics
            return [
                f"""UPDATE rulesets_responsibleuserrule_municipalities AS r
  SET service_id = {target}
  WHERE service_id = {source}
    AND NOT EXISTS (
      SELECT 1
      FROM rulesets_responsibleuserrule_municipalities AS r2
      WHERE r2.responsibleuserrule_id = r.responsibleuserrule_id
        AND r2.service_id = {target}
    );""",
                f"DELETE FROM rulesets_responsibleuserrule_municipalities WHERE service_id = {source};",
            ]
        return [
            f'UPDATE "{table}" SET "{column}" = {target} WHERE "{column}" = {source};'
        ]

    def _get_workitem_queries(self, source, target):
        return [
            f"""UPDATE "caluma_workflow_workitem" SET "assigned_users" = '{{}}' WHERE "addressed_groups" = '{{{source}}}';""",
            f"""UPDATE "caluma_workflow_workitem" SET "addressed_groups" = '{{{target}}}' WHERE "addressed_groups" = '{{{source}}}';""",
            f"""UPDATE "caluma_workflow_workitem" SET "controlling_groups" = '{{{target}}}' WHERE "controlling_groups" = '{{{source}}}';""",
        ]

    def _filter(self, data):
        """Only change tables that handle `data`, not `configuration`."""
        config_tables = [
            apps.get_model(m)._meta.db_table
            for m in set(
                settings.DUMP["CONFIG"]["MODELS"]
                + settings.DUMP["CONFIG"]["MODELS_REFERENCING_DATA"]
            )
        ]
        return [(table, cols) for table, cols in data if table not in config_tables]

    def handle(self, *args, **options):
        sources = options["source"].split(",")
        queries = []
        if options["log_to_case_meta"]:
            for source in sources:
                queries.append(
                    f"""UPDATE caluma_workflow_case
    SET meta = jsonb_set(meta, \'{{migrated-from}}\', \'{source}\', true)
    FROM "INSTANCE"
        JOIN "INSTANCE_SERVICE" ON "INSTANCE_SERVICE"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID"
    WHERE "INSTANCE".case_id = caluma_workflow_case.id
        AND "INSTANCE_SERVICE"."SERVICE_ID" = {source};"""
                )
        for source in sources:
            queries.append(f"\n-- source: {source}, target: {options['target']}")
            for table, columns in self._filter(self._get_all_service_foreign_keys()):
                for column in columns.split(";"):
                    queries += self._get_queries(
                        table, column, source, options["target"]
                    )
            queries.extend(self._get_workitem_queries(source, options["target"]))

        if options["disable"]:
            queries.append("\n-- disable old services and groups")
            queries.append(
                f'UPDATE "SERVICE" SET "DISABLED"=1 WHERE "SERVICE_ID" IN ({options["source"]});'
            )
            queries.append(
                f'UPDATE "GROUP" SET "DISABLED"=1 WHERE "SERVICE_ID" IN ({options["source"]});'
            )

        if options["form_answer"]:
            question_slug = MasterData.get_question_slug("municipality_slug")
            queries.append(f"\n-- migrate form answers for question '{question_slug}'")

            # Use the data source to get the municipality labels.
            municipalities = data_sources.Municipalities().get_data(None, None, None)
            # Find the target municipality data
            municipality_target = next(
                (m for m in municipalities if str(m[0]) == str(options["target"])),
                None,
            )
            # Convert the target municipality label dict to a hstore literal.
            hstore_value = self.hstore_literal(municipality_target[1])

            for source in sources:
                # Update the form answer and the dynamic option with the target id of the municipality.
                # And update the label of the dynamic option to the target municipality label.
                queries.append(
                    f"""UPDATE "caluma_form_answer" SET "value" = '"{options["target"]}"' WHERE "value" = '"{source}"' AND "question_id" = '{question_slug}';"""
                )
                queries.append(
                    f"""UPDATE "caluma_form_dynamicoption" SET "slug" = '{options["target"]}', label = {hstore_value} WHERE "slug" = '{source}' AND "question_id" = '{question_slug}';"""
                )

        script = "\n".join(queries)

        if options["verbosity"] >= 2 or not options["exec"]:
            # If verbosity is high enough, we'll show the SQL, and if
            # we're not actually executing it, we'll show it as well (otherwise
            # there is a command that doesn't do anything and shows nothing)
            self.stdout.write(script)

        if options["exec"]:
            with connection.cursor() as cursor:
                cursor.execute(script)

    def hstore_literal(self, d: dict) -> str:
        """Convert a trans dict to a safe hstore SQL value.

        E.g.
        {'de': 'Gemeinde', 'fr': None, 'it': 'Com'une'}
        becomes
        '"de"=>"Gemeinde", "fr"=>NULL, "it"=>"Com''une"'::hstore

        with proper escaping of quotes and backslashes.
        """

        def esc_hstore_str(s: str) -> str:
            # escape \ and " in the double-quoted hstore string.
            return s.replace("\\", "\\\\").replace('"', '\\"')

        parts = []
        for k, v in d.items():
            k_esc = esc_hstore_str(str(k))
            if v is None:
                parts.append(f'"{k_esc}"=>NULL')
            else:
                v_esc = esc_hstore_str(str(v))
                parts.append(f'"{k_esc}"=>"{v_esc}"')

        # escape single quotes.
        hstore_text = ", ".join(parts).replace("'", "''")

        return f"'{hstore_text}'::hstore"
