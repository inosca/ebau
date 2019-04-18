from logging import getLogger

from caluma.core.mutation import Mutation
from caluma.core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)
from caluma.form.schema import SaveDocument, SaveDocumentAnswer, SaveForm
from caluma.workflow.schema import StartCase

log = getLogger()

"""Caluma permissions for Kanton Bern"""


class CustomPermission(BasePermission):
    @object_permission_for(Mutation)
    def has_object_permission_default(self, mutation, info, instance):
        operation = mutation.__name__
        log.warning(
            f"ACL: fallback object permission: denying "
            f"mutation '{operation}' on {instance}"
        )
        return False

    @permission_for(Mutation)
    def has_permission_default(self, mutation, info):
        operation = mutation.__name__
        log.warning(f"fallback permission: denying mutation '{operation}'")
        return False

    @permission_for(SaveDocument)
    def has_permission_for_savedocument(self, mutation, info):
        log.debug(f"ACL DEBUG: save document")
        return True

    @permission_for(SaveForm)
    def has_permission_for_save_form(self, mutation, info):
        log.debug(f"ACL DEBUG: save form")
        return True

    @permission_for(SaveDocumentAnswer)
    def permission_for_savedocumentanswer(self, mutation, info):
        log.debug(f"ACL DEBUG: save answer")
        return True

    @object_permission_for(SaveDocumentAnswer)
    def object_permission_for_savedocumentanswer(self, mutation, info, instance):
        log.debug(f"ACL DEBUG: save answer")
        return True

    @object_permission_for(SaveForm)
    def has_object_permission_for_save_form(self, mutation, info, instance):
        log.debug(f"ACL DEBUG: object permission for save form")
        return instance.slug != "protected-form"

    @permission_for(StartCase)
    def has_permission_for_start_case(self, mutation, info):
        log.debug(f"ACL DEBUG: object permission for startcase")
        # everyone is allowed to start cases
        return True
