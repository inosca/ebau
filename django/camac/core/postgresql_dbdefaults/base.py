from django.db.backends.postgresql.base import *  # NOQA

from .schema import DatabaseSchemaEditor


OldDatabaseWrapper = DatabaseWrapper # NOQA


class DatabaseWrapper(OldDatabaseWrapper):
    SchemaEditorClass = DatabaseSchemaEditor
