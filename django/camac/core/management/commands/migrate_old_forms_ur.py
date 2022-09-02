from caluma.caluma_form.models import Answer, Question
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Form, Instance

FORM_ID_MAPPING = {
    # Reklame
    249: 121,
    # Cantonal territory usage
    291: 247,
    # Mitbericht Kanton
    42: 300,
    43: 300,
    45: 300,
    46: 300,
    161: 300,
    181: 300,
    201: 300,
    221: 300,
    222: 300,
    223: 300,
    224: 300,
    225: 300,
    241: 300,
    242: 300,
    243: 300,
    245: 300,
    246: 300,
    248: 300,
    251: 300,
    252: 300,
    253: 300,
    254: 300,
    255: 300,
    256: 300,
    257: 300,
    258: 300,
    259: 300,
    260: 300,
    286: 300,
    287: 300,
    288: 300,
    289: 300,
    # Mitbericht Bundesstelle
    244: 292,
    250: 292,
    # Meldung Vorhaben
    295: 290,
}

FORM_TYPE_MAPPING = {
    247: "form-type-veranstaltungsgesuch",
    121: "form-type-commercial-permit",
    300: "form-type-mitbericht-kanton",
    292: "form-type-mitbericht-bundesstelle",
    290: "form-type-project-announcement",
}

ANSWER_MITBERICHT_BUND_MAPPING = {
    244: "mbv-bund-type-pgv-eisenbahn",
    250: "mbv-bund-type-pgv-seilbahn",
}


class Command(BaseCommand):
    help = """Migrate the old forms to new ones."""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        instances_with_old_forms = Instance.objects.filter(
            form_id__in=list(FORM_ID_MAPPING.keys())
        )

        for instance in instances_with_old_forms:
            new_form = Form.objects.get(pk=FORM_ID_MAPPING[instance.form.pk])
            old_form = instance.form
            instance.form = new_form
            instance.save()
            self.stdout.write(
                f"The form for instance {instance.instance_id} has changed from {old_form} to {new_form}"
            )

            if new_form.pk == 300:  # Mitberichtsverfahren Kanton
                special_cases = {
                    43: 42,  # Int. Genehmigungsverf. -> Int. Mitbericht
                }
                value = special_cases.get(old_form.form_id, old_form.form_id)
                Answer.objects.create(
                    value=str(value),
                    document=instance.case.document,
                    question=Question.objects.get(slug="mbv-type"),
                )
            elif new_form.pk == 292:  # Mitberichtsverfahren Bundesstelle
                Answer.objects.create(
                    value=ANSWER_MITBERICHT_BUND_MAPPING[old_form.form_id],
                    document=instance.case.document,
                    question=Question.objects.get(slug="mbv-bund-type"),
                )

            try:
                answer = instance.case.document.answers.filter(
                    question_id="form-type"
                ).first()

                old_value = answer.value

                answer.value = FORM_TYPE_MAPPING[new_form.pk]

                answer.save()
                self.stdout.write(
                    f"Fixed form type of instance {instance.pk} (was {old_value})"
                )
            except AttributeError:

                Answer.objects.create(
                    value=FORM_TYPE_MAPPING[new_form.pk],
                    document=instance.case.document,
                    question=Question.objects.get(slug="form-type"),
                )
                self.stdout.write(
                    f"There was no old form-type answer for the instance {instance.pk}. Therefore the new form-type {FORM_TYPE_MAPPING[new_form.pk]} was created"
                )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
