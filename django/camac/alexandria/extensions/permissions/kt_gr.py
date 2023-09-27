from datetime import datetime
from uuid import UUID

from alexandria.core.models import Category
from dateutil.parser import parse
from localized_fields.value import LocalizedStringValue

from .classes import AdminNewPermission, AdminPaperPermission


class AdminBeilagenMunicipalityPermission(AdminNewPermission, AdminPaperPermission):
    """
    Allow to edit the description and tags.

    Used for municipality in the beilagen-zum-gesuch category.
    """

    def can_update(self, group, document):
        # when its new we check if its paper, otherwise we have to check what is being edited
        if self.in_writable_state(document.instance_document.instance):
            return super().can_update(group, document)

        editable_fields = {
            "description",
            "tags",
        }

        for k, v in self.request.data.items():
            if k in editable_fields or not hasattr(document, k):
                continue

            old_value = getattr(document, k)
            new_value = v

            # convert to correct type for comparison
            if isinstance(old_value, LocalizedStringValue):
                new_value = LocalizedStringValue(new_value)
            elif isinstance(old_value, UUID):
                new_value = UUID(new_value)
            elif isinstance(old_value, datetime):
                new_value = parse(new_value)
            elif isinstance(old_value, Category):
                old_value = old_value.pk
                new_value = new_value["id"]

            if old_value != new_value:
                return False

        return True
