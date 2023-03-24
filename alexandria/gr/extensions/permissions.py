from alexandria.core.permissions import (
    BasePermission,
    permission_for,
    object_permission_for,
)
from alexandria.core.models import BaseModel, Document


class CustomPermission(BasePermission):
    @permission_for(BaseModel)
    def has_permission_default(self, request):
        """
        import logging
        logging.error(request)
        logging.error(vars(request.user))
        return False
        """
        return True

    @permission_for(Document)
    def has_permission_for_document(self, request):
        return True

    @object_permission_for(Document)
    def has_object_permission_for_document(self, request, instance):
        return True
