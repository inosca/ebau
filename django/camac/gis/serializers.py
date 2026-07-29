from dataclasses import dataclass
from typing import Any

from django.core.cache import cache
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from camac.caluma.extensions.permissions import CustomPermission
from camac.caluma.form_import_utils import FormImportWriter
from camac.instance.models import Instance


def convert_answer_value(question_type: str, value: Any) -> int | float | Any:
    match question_type:
        case "integer":
            return int(value)
        case "float":
            return float(value)
        case _:
            return value


@dataclass
class GISApplyResponse:
    pk: None
    instance: Instance
    questions: list[str]


class GISApplySerializer(serializers.Serializer):
    instance = serializers.PrimaryKeyRelatedField(queryset=Instance.objects)
    cache = serializers.UUIDField(write_only=True)
    questions = serializers.ListField(child=serializers.CharField(), read_only=True)

    def validate_cache(self, value):
        if not cache.has_key(value):
            raise ValidationError(
                _("Cache for key %(key)s does not exist") % {"key": value}
            )

        return value

    def create(self, validated_data):
        data = cache.get(validated_data["cache"])
        document = validated_data["instance"].case.document
        written_questions = set()

        if not CustomPermission(self.context["request"]).has_camac_edit_permission(
            document, self.context["request"].caluma_info
        ):
            raise PermissionDenied

        writer = FormImportWriter(
            user=self.context["request"].caluma_info.context.user,
            instance_pk=validated_data["instance"].pk,
            meta_key="gis-value",
            convert_answer_value=convert_answer_value,
        )
        for question_slug, value in data.items():
            success = writer.write_answer(document, question_slug, value)
            if success:
                written_questions.add(question_slug)

        return GISApplyResponse(
            pk=None,
            instance=validated_data["instance"],
            questions=written_questions,
        )
