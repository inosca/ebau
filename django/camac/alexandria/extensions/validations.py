from alexandria.core.models import Document
from django.conf import settings
from django.utils.translation import gettext as _
from generic_permissions.validation import validator_for
from rest_framework.exceptions import ValidationError


class CustomValidation:
    @validator_for(Document)
    def validate_void_mark(self, data, context):
        marks = data.get("marks", [])

        for mark in marks:
            if mark.pk in settings.ALEXANDRIA["EXCLUSIVE_MARKS"] and len(marks) > 1:
                raise ValidationError(
                    _('Mark "%(mark)s" can not be combined with other marks')
                    % {"mark": mark.name.translate()}
                )

        return data
