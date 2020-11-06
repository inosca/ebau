import functools
import json

from caluma.caluma_form.models import Answer, Document, Option, Question
from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.utils.timezone import now

from camac.caluma.api import CalumaApi
from camac.constants.kt_bern import SERVICE_GROUP_RSTA
from camac.core.models import Answer as CamacAnswer
from camac.instance.models import Instance
from camac.user.models import Service

from .config import bab, formal_exam, material_exam


def icq_dict(icq_tuple):
    item, chapter, question = icq_tuple
    return {"item": item, "chapter": chapter, "question": question}


def get_answers_by_mapping(instance, mapping):
    raw_filters = [Q(**icq_dict(icq_tuple)) for icq_tuple in mapping.values()]

    filters = functools.reduce(lambda a, b: a | b, raw_filters)

    return CamacAnswer.objects.filter(Q(instance=instance) & filters)


def get_question_slug(mapping, question_id):
    for slug, icq_tuple in mapping.items():
        if icq_dict(icq_tuple).get("question") == question_id:
            return slug

    raise Exception(f"No slug for question '{question_id}' found")


def get_value(value, question, value_mapping):
    if value.startswith("[") and value.endswith("]"):
        # multiple values
        return [get_value(raw, question, value_mapping) for raw in json.loads(value)]
    elif question.pk in value_mapping:
        # special mapping
        try:
            return value_mapping[question.pk][value]
        except KeyError:
            raise Exception(
                f"Question '{question.pk}' does not have a value mapping for value '{value}'"
            )
    elif value in ["JAA", "NEI", "EING", "MANG", "MABE"]:
        # static options
        suffix = {
            "JAA": "-ja",
            "NEI": "-nein",
            "EING": "-eingehalten",
            "MANG": "-mangel",
            "MABE": "-mangel-behoben",
        }
        option = question.pk + suffix[value]

        try:
            return question.options.get(pk=option).pk
        except Option.DoesNotExist:
            raise Exception(
                f"Question '{question.pk}' does not have an option '{option}'"
            )
    elif question.type == Question.TYPE_INTEGER:
        return int(value)
    elif question.type == Question.TYPE_FLOAT:
        return float(value)

    # fallback: plain value
    return value


class Command(BaseCommand):
    help = "Migrates the legacy audit to the new caluma audit"

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        audit_work_items = WorkItem.objects.filter(
            task_id="audit", document__isnull=True
        )
        count = audit_work_items.count()

        for i, work_item in enumerate(audit_work_items):
            instance = Instance.objects.get(
                pk=work_item.case.meta.get("camac-instance-id")
            )

            audit = Document.objects.create(form_id="dossierpruefung")

            work_item.document = audit
            work_item.save()

            self._migrate_formal_exam(instance, audit)
            self._migrate_formal_exam_rsta(instance, audit)
            self._migrate_material_exam(instance, audit)
            self._migrate_bab(instance, audit)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully migrated audit of instance {instance.pk}\t({i+1} / {count})"
                )
            )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def _get_rsta(self, instance):
        instance_service = (
            instance.instance_services.filter(
                service__service_group_id=SERVICE_GROUP_RSTA
            )
            .order_by("active")
            .first()
        )

        return instance_service and instance_service.service

    def _get_municipality(self, instance):
        instance_service = (
            instance.instance_services.filter(service__service_group=2)
            .order_by("active")
            .first()
        )

        if instance_service:
            return instance_service.service

        self.stdout.write(
            self.style.WARNING(
                f"No municipality for instance {instance.pk} found -- use fallback from form"
            )
        )

        return Service.objects.get(pk=CalumaApi().get_municipality(instance))

    def _fill_document(self, document, camac_answers, mapping, value_mapping):
        caluma_answers = []

        for answer in camac_answers:
            question = Question.objects.get(
                pk=get_question_slug(mapping, answer.question_id)
            )

            caluma_answers.append(
                Answer(
                    document=document,
                    question=question,
                    value=get_value(answer.answer, question, value_mapping),
                )
            )

        Answer.objects.bulk_create(caluma_answers)

    def _migrate_formal_exam(self, instance, audit):
        answers = get_answers_by_mapping(instance, formal_exam.MAPPING_MUNICIPALITY)

        if not answers.exists():
            return

        document = Document.objects.create(
            form_id="fp-form",
            family=audit,
            created_at=now(),
            created_by_group=str(self._get_municipality(instance).pk),
        )
        document_answer = audit.answers.create(
            question_id="fp-form", value=[str(document.pk)]
        )
        document_answer.documents.add(document)

        self._fill_document(
            document,
            answers,
            formal_exam.MAPPING_MUNICIPALITY,
            formal_exam.VALUE_MAPPING,
        )

    def _migrate_formal_exam_rsta(self, instance, audit):
        if not CamacAnswer.objects.filter(
            **icq_dict(formal_exam.RSTA_TRIAGE_QUESTION),
            instance=instance,
            answer="REG",
        ).exists():
            return

        answers = get_answers_by_mapping(instance, formal_exam.MAPPING_RSTA)

        if not answers.exists():
            return

        if not self._get_rsta(instance):
            self.stdout.write(
                self.style.WARNING(
                    f"Instance {instance.pk} has a filled RSTA formal exam but no assigned RSTA"
                )
            )
            return

        document = Document.objects.create(
            form_id="fp-form",
            family=audit,
            created_at=now(),
            created_by_group=str(self._get_rsta(instance).pk),
        )
        document_answer = audit.answers.get(question_id="fp-form")
        document_answer.value.append(str(document.pk))
        document_answer.documents.add(document)
        document_answer.save()

        self._fill_document(
            document,
            answers,
            formal_exam.MAPPING_RSTA,
            formal_exam.VALUE_MAPPING,
        )

    def _migrate_bab(self, instance, audit):
        if not CamacAnswer.objects.filter(
            **icq_dict(bab.TRIAGE_QUESTION),
            instance=instance,
            answer="JAA",
        ).exists():
            return

        answers = get_answers_by_mapping(instance, bab.MAPPING)

        document = Document.objects.create(
            form_id="bab-form",
            family=audit,
            created_at=now(),
            created_by_group=str(
                instance.responsible_service(filter_type="municipality").pk
            ),
        )
        document_answer = audit.answers.create(
            question_id="bab-form", value=[str(document.pk)]
        )
        document_answer.documents.add(document)

        self._fill_document(
            document,
            answers,
            bab.MAPPING,
            bab.VALUE_MAPPING,
        )

    def _migrate_material_exam(self, instance, audit):
        answers = get_answers_by_mapping(instance, material_exam.MAPPING)

        if not answers.exists():
            return

        document = Document.objects.create(
            form_id="mp-form",
            family=audit,
            created_at=now(),
            created_by_group=str(
                instance.responsible_service(filter_type="municipality").pk
            ),
        )
        document_answer = audit.answers.create(
            question_id="mp-form", value=[str(document.pk)]
        )
        document_answer.documents.add(document)

        self._fill_document(
            document,
            answers,
            material_exam.MAPPING,
            material_exam.VALUE_MAPPING,
        )
