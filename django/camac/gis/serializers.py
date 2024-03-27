from dataclasses import dataclass
from typing import List

from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Document, Question
from django.core.cache import cache
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from camac.caluma.extensions.permissions import CustomPermission
from camac.instance.models import Instance


@dataclass
class GISApplyResponse:
    pk: None
    instance: Instance
    questions: List[str]


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

    def _write_row(self, form_slug, row_data):
        row_document = Document.objects.create(form_id=form_slug)

        for question_slug, value in row_data.items():
            self._write_answer(row_document, question_slug, value)

        return str(row_document.pk)

    def _write_answer(self, document, question_slug, value):
        try:
            question = Question.objects.get(pk=question_slug)
        except Question.DoesNotExist:  # pragma: no cover
            return False

        answer_value = value["value"]

        if question.type == Question.TYPE_TABLE:
            answer_value = [
                self._write_row(value["form"], row) for row in value["value"]
            ]
        elif question.type == Question.TYPE_MULTIPLE_CHOICE:
            answer_value = [opt["value"] for opt in answer_value]

        save_answer(
            question=question,
            document=document,
            user=self.context["request"].caluma_info.context.user,
            value=answer_value,
            meta={"gis-value": answer_value},
        )

        return True

    def create(self, validated_data):
        data = cache.get(validated_data["cache"])
        document = validated_data["instance"].case.document
        written_questions = set()

        if not CustomPermission().has_camac_edit_permission(
            document, self.context["request"].caluma_info
        ):
            raise PermissionDenied()

        for question_slug, value in data.items():
            success = self._write_answer(document, question_slug, value)

            if success:
                written_questions.add(question_slug)

        return GISApplyResponse(
            pk=None,
            instance=validated_data["instance"],
            questions=written_questions,
        )
