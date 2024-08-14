from alexandria.core.models import Document
from alexandria.core.validations import AlexandriaValidator
from django.conf import settings
from django.utils.translation import gettext as _
from generic_permissions.validation import validator_for
from rest_framework.exceptions import ValidationError


class CustomValidation(AlexandriaValidator):
    @validator_for(Document)
    def validate_marks(self, data, context):
        marks = data.get("marks", [])
        mark_ids = {mark.pk for mark in marks}

        for mark in marks:
            if mark.pk in settings.ALEXANDRIA["EXCLUSIVE_MARKS"] and len(marks) > 1:
                raise ValidationError(
                    _('Mark "%(mark)s" can not be combined with other marks.')
                    % {"mark": mark.name.translate()}
                )

            if (
                mark.pk in settings.ALEXANDRIA["MARK_VISIBILITY"].get("SENSITIVE", [])
                and len(
                    mark_ids & set(settings.ALEXANDRIA["MARK_VISIBILITY"]["PUBLIC"])
                )
                > 0
            ):
                raise ValidationError(
                    _('Mark "%(mark)s" can not be combined with public marks.')
                    % {"mark": mark.name.translate()}
                )

        return data
