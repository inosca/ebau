from django.core.exceptions import ObjectDoesNotExist
from rest_framework_json_api.relations import ResourceRelatedField


class FormDataResourceReleatedField(ResourceRelatedField):
    """Resource related field with support to be posted as form data."""

    # TODO: might be better fixed in django-json-api itself?
    # I think ResourceRelated field should work in cases
    # where request and response content types are different.

    def to_internal_value(self, data):
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        try:
            return self.get_queryset().get(pk=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            return super().to_internal_value(data)
