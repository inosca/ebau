from caluma.caluma_form.models import Answer, Document

from camac.core.dataimport import ImportCommand
from camac.core.models import Answer as Camac_Answer
from camac.instance.models import Instance


class Command(ImportCommand):
    help = """
    (Bern): (Partially) duplicates an instance.

    Covered:
    - INSTANCE
    - ANSWER
    - caluma_form_document
    - caluma_form_answer (currently only top-level, no tables)
    """

    def add_arguments(self, parser):
        parser.add_argument("--instance_ids", nargs="+", type=int)
        parser.add_argument("--count", default=1, type=int)

    def handle(self, *args, **option):
        duplicate_instance(option["instance_ids"], option["count"])


def duplicate_instance(instance_ids, count):
    for _ in range(count):
        for instance_id in instance_ids:
            inst = Instance.objects.get(pk=instance_id)
            inst.pk = None
            inst.save()

            camac_answers = Camac_Answer.objects.filter(instance_id=instance_id)
            for answer in camac_answers:
                answer.instance_id = inst.pk
                answer.pk = None
                answer.save()

            # possible improvement: call Document.copy() instead!
            doc = Document.objects.get(
                **{
                    "meta__camac-instance-id": instance_id,
                    "form__meta__is-main-form": True,
                }
            )
            old_doc_pk = doc.pk
            doc.pk = None
            doc.meta["camac-instance-id"] = inst.pk
            doc.save()

            answers = Answer.objects.filter(document_id=old_doc_pk)
            for answer in answers:
                answer.document = doc
                answer.pk = None
                answer.save()

            print(f"duplicated instance {instance_id}: new ID is {inst.pk}")
