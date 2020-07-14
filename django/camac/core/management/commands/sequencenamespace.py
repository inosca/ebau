#!/usr/bin/env python
from __future__ import unicode_literals

import re

import django.core.management.color as color
from django.conf import settings
from django.core.management.base import AppCommand
from django.db import DEFAULT_DB_ALIAS, connections


class Command(AppCommand):
    help = (
        "Prints or executes the SQL statements for resetting "
        "sequences for the given app name(s).\n"
        "The sequences are set to a distinct range for each user"
    )

    output_transaction = True

    def sequence_reset_sql(self, ops, style, model_list, ns_start, ns_end):
        from django.db import models

        output = []

        qn = ops.quote_name
        for model in model_list:

            query_tpl = re.sub(
                r"\s+",
                " ",
                """
                %(with)s sub %(as)s (
                    %(select)s max(%(field_q)s) current_id
                    %(from)s %(table)s
                    %(where)s
                        %(field_q)s %(between)s %(ns_start)d %(and)s %(ns_end)d
                )
                %(select)s
                    setval(
                        pg_get_serial_sequence('%(table)s','%(field)s'),
                        coalesce(sub.current_id, %(ns_start)d),
                        sub.current_id %(isnot)s null
                    )
                %(from)s sub;
            """,
            ).strip()

            common_args = {
                "ns_start": ns_start,
                "ns_end": ns_end,
                "between": style.SQL_KEYWORD("BETWEEN"),
                "and": style.SQL_KEYWORD("AND"),
                "with": style.SQL_KEYWORD("WITH"),
                "as": style.SQL_KEYWORD("AS"),
                "select": style.SQL_KEYWORD("SELECT"),
                "isnot": style.SQL_KEYWORD("IS NOT"),
                "from": style.SQL_KEYWORD("FROM"),
                "where": style.SQL_KEYWORD("WHERE"),
            }

            for f in model._meta.local_fields:
                if isinstance(f, models.AutoField):
                    output.append(
                        query_tpl
                        % dict(
                            table=style.SQL_TABLE(qn(model._meta.db_table)),
                            field=style.SQL_FIELD(f.column),
                            field_q=style.SQL_FIELD(qn(f.column)),
                            **common_args,
                        )
                    )
                    # Only one AutoField is allowed per model, so don't bother
                    # continuing.
                    break
            for f in model._meta.many_to_many:
                if not f.remote_field.through:
                    output.append(
                        query_tpl
                        % dict(
                            table=style.SQL_TABLE(qn(model._meta.db_table)),
                            field=style.SQL_FIELD("id"),
                            field_q=style.SQL_FIELD(qn("id")),
                            **common_args,
                        )
                    )

        return output

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "--database",
            default=DEFAULT_DB_ALIAS,
            help="Nominates a database to print the SQL for. "
            'Defaults to the "default" database.',
        )

        parser.add_argument(
            "--user",
            default=None,
            help="Username to set the namespace to. "
            "See settings.SEQUENCE_NAMESPACES",
            required=False,
        )

        parser.add_argument(
            "--execute",
            default=False,
            help="Execute the queries instead of printing them",
            action="store_true",
        )

    def handle_app_config(self, app_config, **options):
        if app_config.models_module is None:
            return
        connection = connections[options["database"]]
        models = app_config.get_models(include_auto_created=True)

        if options.get("execute"):
            # The DB does not want colored SQL
            self.style = color.no_style()

        if not options.get("user"):
            print("Argument --user missing!")
            return

        user = options.get("user").lower()
        try:
            ns_start = settings.SEQUENCE_NAMESPACES[user]
        except KeyError:
            if settings.ENV == "production":
                ns_start = 1
            else:
                print(
                    "User %s not configured! "
                    "Update SEQUENCE_NAMESPACES in settings" % user
                )
                return

        ns_end = ns_start + settings.SEQUENCE_NAMESPACES_SIZE - 1

        statements = self.sequence_reset_sql(
            connection.ops, self.style, models, ns_start, ns_end
        )
        if options.get("execute"):

            print(
                "Updating SEQUENCEs for user %s (range %d..%d) in app %s"
                % (user, ns_start, ns_end, app_config.verbose_name)
            )
            with connection.cursor() as cursor:
                for stmt in statements:
                    cursor.execute(stmt)

        else:
            return "\n".join(statements)
