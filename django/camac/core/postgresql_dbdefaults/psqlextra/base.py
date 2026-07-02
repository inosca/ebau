from psqlextra.backend.base import *  # noqa: F403

from .schema import DatabaseSchemaEditor

OldDatabaseWrapper = DatabaseWrapper  # noqa: F405


class DatabaseWrapper(OldDatabaseWrapper):
    SchemaEditorClass = DatabaseSchemaEditor
