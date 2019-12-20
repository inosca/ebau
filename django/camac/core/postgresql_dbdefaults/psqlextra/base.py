from psqlextra.backend.base import *  # NOQA

from .schema import DatabaseSchemaEditor

OldDatabaseWrapper = DatabaseWrapper  # NOQA


class DatabaseWrapper(OldDatabaseWrapper):
    SchemaEditorClass = DatabaseSchemaEditor
